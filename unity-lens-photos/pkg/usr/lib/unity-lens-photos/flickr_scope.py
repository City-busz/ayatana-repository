#! /usr/bin/python3
# -*- coding: utf-8 -*-

#    Copyright (c) 2012 David Calle <davidc@framli.eu>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import gettext
import locale
import oauth2
import time
import datetime
import urllib
import json
from gi.repository import Accounts
from gi.repository import Signon
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio
from gi.repository import Dee
from gi.repository import Unity
from gi.repository import Soup
from gi.repository import SoupGNOME

APP_NAME = "unity-lens-photos"
LOCAL_PATH = "/usr/share/locale/"

gettext.bindtextdomain(APP_NAME, LOCAL_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext

NO_RESULTS_HINT = _("Sorry, there are no photos that match your search.")

class Scope:

    def __init__(self, lens):
        """Set some initial values for the scope and connect to Unity"""
        self._scope = Unity.Scope.new("/net/launchpad/scope/photos/flickr")
        self._sources_options = []

        # Storage for results waiting to be displayed
        self.results_waiting = {1:[], 2:[], 3:[]}

        self.init_session_management ()
        self._enabled = False
        self._authenticating = False
        self._get_accounts_for_service ('flickr')
        self._scope.connect("search-changed", self.on_search_changed)
        self._scope.connect ("filters-changed", self.on_lens_active_or_preference_changed)
        self._scope.connect("notify::active", self.on_lens_active_or_preference_changed)
        self._scope.props.sources.connect("notify::filtering", self.on_filtering_changed)
        self._scope.connect('preview-uri', self.on_preview_uri)

        self.preferences = Unity.PreferencesManager.get_default()
        self.preferences.connect("notify::remote-content-search", self.on_lens_active_or_preference_changed)

        self._scope.export ()
        lens.add_local_scope (self._scope)


    def init_session_management (self):
        """ Define a set of variables used for Soup session management """
        self._pending = []
        self._http = []
        for i in range(4):
            self._pending.append(None)
            self._http.append(self._get_http_session ())


    def _get_http_session (self):
        """Create an async Soup session"""
        session = Soup.SessionAsync()
        session.add_feature_by_type(SoupGNOME.ProxyResolverGNOME)
        return session


########
# Account management
########

    def _get_accounts_for_service (self, service):
        """Get online accounts matching the scope service"""
        self._accounts = []
        try:
            self._account_manager = Accounts.Manager.new_for_service_type("sharing")
        except TypeError as e:
            print ("Error (flickr): Unable to initialise accounts manager: %s" % e)
            return
        self._account_manager.connect("enabled-event", self._on_enabled_event)
        self._account_manager.connect("account-deleted", self._on_deleted_event)
        for account_service in self._account_manager.get_enabled_account_services():
            if account_service.get_account().get_provider_name() == service:
                self._add_account_service(account_service)
            else:
                self._remove_account_service(account_service)


    def _add_account_service(self, account_service):
        """Add account to scope and add Sources filter option"""
        for account in self._accounts:
            if account:
                if account.get_account_service() == account_service:
                    return
        self._accounts.append(self._account_to_login(account_service))
        print ('Added Flickr account %s' % (account_service,))
        source_name = account_service.get_account().get_provider_name ().title()
        if not source_name in self._sources_options:
            self._sources_options.append(source_name)
            self._scope.props.sources.add_option(source_name, source_name, None)


    def _remove_account_service(self, account_service):
        """Remove account from Sources filter"""
        self._enabled = False
        print ('Removed Flickr account %s' % (account_service))
        source_name = account_service.get_account().get_provider_name ().title()
        if source_name in self._sources_options:
            self._sources_options.remove(source_name)
            self._scope.props.sources.remove_option(source_name)
            self.on_lens_active_or_preference_changed ()


    def get_account_service(self):
        return self._account_service


    def _on_account_enabled (self, account, enabled):
        self._enabled = enabled


    def _account_to_login(self,account_service):
        """Initialize default values for the account"""
        self._account_service = account_service
        self._account_service.connect("enabled", self._on_account_enabled)
        self._enabled = self._account_service.get_enabled()
        self._authenticating = False
        self._auth_token = None
        self._queued_search = None
        self._login()


    def _on_enabled_event(self, account_manager, account_id):
        """Listen to the account enabled signal 
        and remove/add the service accordingly"""
        account = self._account_manager.get_account(account_id)
        if account.get_provider_name() != "flickr": return
        for service in account.list_services():
            account_service = Accounts.AccountService.new(account, service)
            if account_service.get_enabled():
                self._add_account_service(account_service)
            else:
                self._remove_account_service(account_service)


    def _on_deleted_event(self, account_manager, account_id):
        """Listen to the account deleted signal, 
        remove the service and silence the scope"""
        account = self._account_manager.get_account(account_id)
        source_name = account.get_provider_name ().title()
        if source_name in self._sources_options:
            self.enabled = False
            self._sources_options.remove(source_name)
            self._scope.props.sources.remove_option(source_name)
            self.on_lens_active_or_preference_changed ()
            print ('Removed Flickr account')


    def _login(self):
        """Trigger a service login with account credentials"""
        if self._authenticating:
            return
        print ("Flickr : logging in")
        self._authenticating = True
        # Get the global account settings
        auth_data = self._account_service.get_auth_data()
        identity = auth_data.get_credentials_id()
        session_data = auth_data.get_parameters()
        self.consumer = oauth2.Consumer(key=session_data['ConsumerKey'], secret=session_data['ConsumerSecret'])
        self.auth_session = Signon.AuthSession.new(identity,
                auth_data.get_method())
        self.auth_session.process(session_data,
                auth_data.get_mechanism(),
                self._login_cb, None)


    def _login_cb(self, session, reply, error, user_data):
        """Verify login token"""
        print ("Flickr : login finished")
        self._authenticating = False
        if error:
            print ("Flickr: Got authentication error")
            return
        old_token = self._auth_token
        if not "AccessToken" in reply or not "TokenSecret" in reply:
            print ("Flickr: Didn't find token in session")
            return
        self._auth_token = reply["AccessToken"]
        if self._auth_token == old_token:
            return
        if self._queued_search:
            self.on_search_changed(*self._queued_search)
        self.token = oauth2.Token(key=reply["AccessToken"], secret=reply["TokenSecret"])


########
# Flickr query generators
########

    def query_for_cat (self, cat, search):
        """Select the correct query depending on search parameters"""
        method, args = None, None
        date = self.check_date_filter ()
        if date > 0:
            taken = 'min_taken_date'
        elif date < 0:
            date = 180*86400
            now = int(time.time())
            date = now - date
            taken = 'max_taken_date'
        else:
            taken = 'forget_this'
        method = 'flickr.photos.search'
        if cat == 1:
            if search:
                args = {'text':search,
                        'per_page':'50',
                        'user_id':'me',
                        taken:str(date),
                        'extras':'url_t,date_taken'}
            else:
                args = {'per_page':'100',
                        'user_id':'me',
                        taken:str(date),
                        'extras':'url_t,date_taken'}
        elif cat == 2:
            if search:
                args = {'text':search, 
                        'per_page':'150',
                        'contacts':'all',
                        taken:str(date),
                        'extras':'url_t,date_taken'}
            else:
                args = {'per_page':'150',
                        'contacts':'all',
                        'text':'*',
                        taken:str(date),
                        'extras':'url_t,date_taken'}
        elif cat == 3:
            if search:
                args = {'text':search, 
                        'per_page':'50',
                        taken:str(date),
                        'extras':'url_t,date_taken'}
        elif cat == 0:
            if not search and date == 0:
                self.recent_expected = True
                args = {'per_page':'25',
                        'contacts':'all',
                        'user_id':'me',
                        'text':'*',
                        'extras':'url_t,date_taken'}
        return [method, args]


    def _url_maker(self, method, args):
        """Prepare the query url for the service"""
        url = None
        if method:
            try:
                params = {
                    'nojsoncallback':'1',
                    'format':'json',
                    'oauth_callback': "http://www.ubuntu.com/",
                    'oauth_consumer_key': self.consumer.key,
                    'oauth_nonce': oauth2.generate_nonce(),
                    'oauth_signature_method':"HMAC-SHA1",
                    'oauth_timestamp': str(int(time.time())),
                    'oauth_token': self.token.key,
                    'oauth_version': "1.0"}
                params['method'] = method
                params = dict(params.items())
                params.update(dict(args.items()))
                req = oauth2.Request(method="GET", url='https://secure.flickr.com/services/rest', parameters=params)
                signature = oauth2.SignatureMethod_HMAC_SHA1().sign(req,self.consumer,self.token)
                signature_url = urllib.parse.urlencode({"oauth_signature":signature})
                url = 'https://secure.flickr.com/services/rest?%s&%s' % (urllib.parse.urlencode(params),signature_url)
            except:
                pass
        return url


########
# Lens functions
########

    def on_lens_active_or_preference_changed(self, *_):
        """ Update results when the lens is opened """
        self._scope.queue_search_changed(Unity.SearchType.DEFAULT)


    def on_filtering_changed(self, *_):
        """Run another search when a filter change is notified."""
        for source in self._sources_options:
            filtering = self._scope.props.sources.props.filtering
            active = self._scope.props.sources.get_option(source).props.active
            if (active and filtering) or (not active and not filtering):
                if not self._enabled:
                    self._enabled = True
                    self._scope.queue_search_changed(Unity.SearchType.DEFAULT)
            else:
                self.cancel_all_searches ()
            print ("    %s enabled : %s" % (source, self._enabled))


    def cancel_all_searches (self):
        """Cancel all searches and clear the lens"""
        self._enabled = False
        for i in range(len(self._pending)):
            try:
                self._http[i].cancel_message(self._pending[i],Soup.KnownStatusCode.CANCELLED)
            except:
                pass
        self._scope.props.results_model.clear ()


    def check_date_filter(self):
        """Get active option for a filter name"""
        try:
            date = self._scope.get_filter("date").get_active_option().props.id
            date = int(date)*86400
            now = int(time.time())
            date = now - date
        except (AttributeError):
            date = 0
        return date


    def on_search_changed (self, scope, search, search_type, cancellable):
        """Trigger a search for each category when the lens requests it"""
        self.recent_expected = False
        model = search.props.results_model
        search.set_reply_hint ("no-results-hint", GLib.Variant.new_string(NO_RESULTS_HINT))
        model.clear()

        # only perform the request if the user has not disabled
        # online results. That will hide the category as well.
        if self.preferences.props.remote_content_search != Unity.PreferencesManagerRemoteContent.ALL:
            search.finished()
            return

        self._queued_search = (scope, search, search_type, cancellable)
        if self._authenticating:
            print ("authenticating, queuing search")
            return
        search_string = search.props.search_string.strip()
        if self._enabled:
            if search_type is Unity.SearchType.DEFAULT:
                print ('Flickr : new search %s' % search_string)
                for i in range(4):
                    if self._pending[i] is not None:
                        self._http[i].cancel_message(self._pending[i],
                                                    Soup.KnownStatusCode.CANCELLED)
                    if search_string:
                        if i > 0:
                            args = self.query_for_cat(i, search_string)
                            url = self._url_maker(args[0], args[1])
                            if url:
                                self._pending[i] = Soup.Message.new("GET", url)
                                self._http[i].queue_message(self._pending[i],self._search_cb,[search_string, model, i, search, 3])
                    else:
                        if i < 3:
                            args = self.query_for_cat(i, search_string)
                            url = self._url_maker(args[0], args[1])
                            if url:
                                self._pending[i] = Soup.Message.new("GET", url)
                                self._http[i].queue_message(self._pending[i],self._search_cb,[search_string, model, i, search, 2])
            else:
                search.finished ()
        else:
            search.finished ()


    def recent_cat_is_done (self, search, model):
        """ Wait for Recent category results to be fetched before displaying others.
        It allows results deduplication to prioritize results from Recent"""
        for cat in self.results_waiting.keys ():
            print ("Releasing Flickr results for cat %i" % cat)
            self.update_results_model(search, model, self.results_waiting[cat], cat, True)


    def update_results_model(self, search, model, results, cat, recent_done):
        """Update results for category 0, then the others"""
        if self.recent_expected and not recent_done and cat != 0:
            self.results_waiting[cat] = results
        else:
            counter = 0
            if len(results) > 0:
                for photo in results['photos']['photo']:
                    counter += 1
                    title = photo['title']
                    timestamp = (time.mktime(time.strptime(photo['datetaken'], '%Y-%m-%d %H:%M:%S')))
                    comment = str(photo['id'])+"_ulp-date_"+str(timestamp)[:-2]
                    uri = 'http://www.flickr.com/photos/%s/%s' % (photo['owner'], photo['id'])
                    icon_hint = photo['url_t']
                    model.append (uri, icon_hint, cat,"text/html", title, comment, uri)
                    model.flush_revision_queue ()
            print ('Flickr : Added %i results to category %i' % (counter, cat))
            if cat == 0:
                self.recent_cat_is_done (search, model)


########
# Service answer handling
########

    def _search_cb(self, session, msg, search_args):
        """Handle async Soup callback"""
        results = self._handle_search_msg(msg, search_args[2])
        self.update_results_model(search_args[0], search_args[1], results, search_args[2], False)
        if search_args[2] == 2:
            search_args[3].finished ()


    def _handle_search_msg(self, msg, cat):
        """ Handle response message"""
        results = []
        if msg.status_code != 200:
            self._pending[cat] = None
            print ("Error: Unable to get results from the server")
            print ("       %d: %s" % (msg.status_code, msg.reason_phrase))
        else:
            self._pending[cat] = None
            try:
                results = json.loads(msg.response_body.data)
            except:
                pass
        return results


########
# Previews
########

    def on_preview_uri(self, scope, uri):
            """Preview request handler"""
            preview = None
            model = self._scope.props.results_model
            iter = model.get_first_iter()
            end_iter = model.get_last_iter()
            while iter != end_iter:
                if model.get_value(iter, 0) == uri:
                    title = model.get_value(iter, 4)
                    photo_id = model.get_value(iter, 5).split("_ulp-date_")[0]
                    meta = self.getMetadataForPhoto(photo_id)
                    exif = self.getEXIFForPhoto(photo_id)
                    image = model.get_value(iter, 1).replace('_t.', '.')
                    title = meta[0]
                    subtitle = _("By %s, %s") % (meta[1], meta[3])
                    description = meta[2]
                    license = meta[4]
                    tags = meta[5]
                    camera = exif[0]
                    if not title:
                        title = ''
                    if not description:
                        description = ''
                    preview = Unity.GenericPreview.new(title.strip (), description.strip (), None)
                    if image:
                        preview.props.image_source_uri = image
                    if subtitle:
                        preview.props.subtitle = subtitle
                    if camera:
                        preview.add_info(Unity.InfoHint.new("camera", _("Camera"), None, camera))
                    if license:
                        preview.add_info(Unity.InfoHint.new("license", _("License"), None, license))
                    if tags:
                        preview.add_info(Unity.InfoHint.new("tags", _("Tags"), None, tags))
                    gfile_icon = Gio.file_new_for_path("/usr/share/icons/unity-icon-theme/places/svg/service-flickr.svg")
                    gicon = Gio.FileIcon.new (gfile_icon)
                    view_action = Unity.PreviewAction.new("view", _("View"), gicon)
                    view_action.connect('activated', self.view_action)
                    preview.add_action(view_action)
                    break
                iter = model.next(iter)
            if preview == None:
                print ("Couldn't find model row for requested preview uri: '%s'", uri)
            return preview


    def view_action (self, scope, uri):
        """On item clicked, close the Dash and display the photo"""
        return


    def getMetadataForPhoto(self, photo):
        """Fetch photo metadata from service"""
        method = 'flickr.photos.getInfo'
        args = {'photo_id':photo}
        url = self._url_maker(method, args)
        raw_results = urllib.request.urlopen(url).read ()
        meta = json.loads(raw_results.decode("utf8"))
        title, owner, description = None, None, None
        date, license = None, None
        tags_raw = []
        title = meta['photo']['title']['_content']
        owner = meta['photo']['owner']['realname']
        if not owner:
            owner = meta['photo']['owner']['username']
        description = meta['photo']['description']['_content']
        date = meta['photo']['dates']['taken']
        try:
            tme_struct = time.strptime(date, '%Y-%m-%d %H:%M:%S')
            date = datetime.datetime(*tme_struct[0:6]).strftime('%d %b %Y %H:%M')
        except:
            pass
        license_nb = meta['photo']['license']
        if license_nb:
            license_list = ["All Rights Reserved",
                        "Attribution-NonCommercial-ShareAlike License",
                        "Attribution-NonCommercial License",
                        "Attribution-NonCommercial-NoDerivs License",
                        "Attribution License",
                        "Attribution-ShareAlike License",
                        "Attribution-NoDerivs License",
                        "No known copyright restrictions",
                        "United States Government Work"]
            license = license_list[int(license_nb)]
        tags_raw = meta['photo']['tags']['tag']
        tag_list = []
        for tag in tags_raw:
            tag_list.append(tag['_content'])
        tags = ', '.join(tag_list)
        return [title, owner, description, date, license, tags]


    def getEXIFForPhoto(self, photo):
        """fetch EXIF metadata from service"""
        method = 'flickr.photos.getExif'
        args = {'photo_id':photo}
        url = self._url_maker(method, args)
        raw_results = urllib.request.urlopen(url).read ()
        exif = json.loads(raw_results.decode("utf8"))
        camera, make, model = None, None, None
        try:
            for e in exif['photo']['exif']:
                if e['tag'] == "Camera":
                    camera = e['raw']['_content']
                elif e['tag'] == "Make":
                    make = e['raw']['_content']
                elif e['tag'] == "Model":
                    model = e['raw']['_content']
                else:
                    pass
            if not camera:
                if make and model:
#                    camera = "%s %s" % (make, model)
                    camera = model
        except:
            pass
        return [camera]
