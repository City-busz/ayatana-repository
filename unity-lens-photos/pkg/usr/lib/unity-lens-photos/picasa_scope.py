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
import urllib.parse
import urllib.request
import time
import datetime
from gi.repository import Accounts
from gi.repository import Signon
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio
from gi.repository import Dee
from gi.repository import Unity
from gi.repository import GData
from xml.etree import ElementTree as ET

APP_NAME = "unity-lens-photos"
LOCAL_PATH = "/usr/share/locale/"

gettext.bindtextdomain(APP_NAME, LOCAL_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext

NO_RESULTS_HINT = _("Sorry, there are no photos that match your search.")

class Scope:

    def __init__(self, lens):
        """Set some initial values for the scope and connect to Unity"""
        self._scope = Unity.Scope.new ("/net/launchpad/scope/photos/picasa")
        self._sources_options = []

        # Storage for results waiting to be displayed
        self.results_waiting = {1:[]}

        self._enabled = False
        self._cancellable = [Gio.Cancellable (), Gio.Cancellable ()]
        self._get_accounts_for_service ('google')
        self._scope.connect("search-changed", self._on_search_changed)
        self._scope.connect ("filters-changed", self.on_lens_active_or_preference_changed)
        self._scope.connect("notify::active", self.on_lens_active_or_preference_changed)
        self._scope.props.sources.connect("notify::filtering", self.on_filtering_changed)
        self._scope.connect('preview-uri', self.on_preview_uri)

        self.preferences = Unity.PreferencesManager.get_default()
        self.preferences.connect("notify::remote-content-search", self.on_lens_active_or_preference_changed)

        self._scope.export ()
        lens.add_local_scope (self._scope)


########
# Account management
########

    def _get_accounts_for_service (self, service):
        """Get online accounts matching the scope service"""
        self._accounts = []
        try:
            self._account_manager = Accounts.Manager.new_for_service_type("sharing")
        except TypeError as e:
            print ("Error (google): Unable to initialise accounts manager: %s" % e)
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
        print ('Added Picasa account %s' % (account_service,))
        source_name = account_service.get_account().get_provider_name ().title()
        if not source_name in self._sources_options:
            self._sources_options.append(source_name)
            self._scope.props.sources.add_option(source_name, "Picasa", None)


    def _remove_account_service(self, account_service):
        """Remove account from Sources filter"""
        self._enabled = False
        print ('Removed Picasa account %s' % (account_service))
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
        authorizer = SignOnAuthorizer(self._account_service)
        authorizer.refresh_authorization(None)
        self._client = GData.PicasaWebService(authorizer=authorizer)
        self._queued_search = None


    def _on_enabled_event(self, account_manager, account_id):
        """Listen to the account enabled signal 
        and remove/add the service accordingly"""
        account = self._account_manager.get_account(account_id)
        if account.get_provider_name() != "google": return
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
            print ('Removed Picasa account')


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
        for c in self._cancellable:
            c.cancel ()
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


    def _on_search_changed (self, scope, search, search_type, cancellable):
        """Trigger a search for each category when the lens requests it"""
        self.recent_expected = False
        for c in self._cancellable:
            c.cancel ()
        model = search.props.results_model
        search.set_reply_hint ("no-results-hint", GLib.Variant.new_string(NO_RESULTS_HINT))
        model.clear ()

        # only perform the request if the user has not disabled
        # online results. That will hide the category as well.
        if self.preferences.props.remote_content_search != Unity.PreferencesManagerRemoteContent.ALL:
            search.finished()
            return

        search_string = search.props.search_string
        if self._enabled:
            if search_type == Unity.SearchType.DEFAULT:
                self.update_results_model (search_string, model, search)
                print("Picasa : new search %s" % search_string)
            else:
                search.finished ()
        else:
            search.finished ()


    def recent_cat_is_done (self, model):
        """ Wait for Recent category results to be fetched before displaying others.
        It allows results deduplication to prioritize results from Recent"""
        for cat in self.results_waiting.keys ():
            print ("Releasing Picasa results for cat %i" % cat)
            self.parse_results(self.results_waiting[cat], cat, model, True)


    def update_results_model (self, search, model, s):
        """Trigger Picasa queries for each cat"""
        if not self._enabled:
            return
        if self.check_date_filter() != 0 or search:
            cats = [1]
        else:
            cats = [0,1]
            self.recent_expected = True
        for cat in cats:
            xml_feed = self.get_photos_list(search, cat, model, s);


    def get_photos_list (self, search, cat, model, s):
        """Prepare Picasa async query"""
        if cat == 1:
            limit = 100
        else:
            limit = 50
        if not self._client.is_authorized():
            self._client.props.authorizer.refresh_authorization(None)
        timestamp = self.check_date_filter()
        if timestamp < 0:
            timestamp = 180*86400
            now = int(time.time())
            timestamp = now - timestamp
            operator = "<"
        else:
            operator = ">"
        d=datetime.datetime.fromtimestamp(timestamp)
        date = d.isoformat("T") + "Z"
        fields = urllib.parse.urlencode ({"fields":"entry[xs:dateTime(published)%sxs:dateTime('%s')],link,id,updated" % (operator, date)})
        url = "https://picasaweb.google.com/data/feed/api/user/default?kind=photo&max-results=%i&thumbsize=u150&%s" % (limit,fields)
        q = GData.Query.new (search)
        fquery = GData.Query.get_query_uri (q, url)
        self._cancellable[cat] = Gio.Cancellable ()
        self._client.query_async(None, fquery, q, GData.PicasaWebFile, self._cancellable[cat], None, None, self.get_query_async_feed, [cat, model, s])


    def get_query_async_feed (self, service, result, catmodel):
        """Handle query response"""
        try:
            feed = self._client.query_finish (result)
        except:
            feed = None
        if feed and catmodel:
            xml_feed = feed.get_xml ()
            GLib.idle_add(self.parse_results, xml_feed, catmodel[0], catmodel[1], False)
        if catmodel:
            catmodel[2].finished ()


    def parse_results (self, results, cat, model, recent_done):
        """Parse and update results for category 0, then the others"""
        if self.recent_expected and not recent_done and cat != 0:
            self.results_waiting[cat] = results
        else:
            counter = 0
            if results:
                feed = ET.XML(results)
                for elem in feed:
                    if elem.tag == '{http://www.w3.org/2005/Atom}entry':
                        title, photo_feed, photo_link = '', '', ''
                        date, thumb, summary = '', '', None
                        for sub in elem:
                            if sub.tag == "{http://www.w3.org/2005/Atom}summary":
                                summary = sub.text
                            if sub.tag == "{http://www.w3.org/2005/Atom}title":
                                title = sub.text
                            if sub.tag == "{http://www.w3.org/2005/Atom}link":
                                if sub.get("rel") == "http://schemas.google.com/g/2005#feed":
                                    photo_feed = sub.get("href")
                                if sub.get("rel") == "http://www.iana.org/assignments/relation/alternate":
                                    photo_link = sub.get("href")
                            if sub.tag == "{http://schemas.google.com/photos/2007}timestamp":
                                date = sub.text
                            if sub.tag == "{http://schemas.google.com/photos/2007}albumtitle":
                                album = sub.text
                            if sub.tag == "{http://www.w3.org/2005/Atom}content":
                                thumb = sub.get('src')
                        if summary:
                            title = summary
                        if thumb and photo_link and title and album and photo_feed and date:
                            counter += 1
                            model.append(photo_link,
                                         thumb,
                                         cat,
                                         "text/html",
                                         title,
                                         album+"_ulp-album_"+photo_feed+"_ulp-date_"+str(date),
                                         photo_link);
                            model.flush_revision_queue ()
            print ('Picasa : Added %i results to category %i' % (counter, cat))
            if cat == 0:
                self.recent_cat_is_done (model)

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
                photo_from_feed = model.get_value(iter, 5).split('_ulp-date_')[0]
                album = photo_from_feed.split('_ulp-album_')[0]
                photo_id = photo_from_feed.split('_ulp-album_')[1]
                timestamp = model.get_value(iter, 5).split('_ulp-date_')[1]
                date = datetime.datetime.fromtimestamp(float(timestamp[:-3])).strftime('%d %b %Y')
                try:
                    meta = self.getMetadataForPhoto(photo_id)
                except:
                    meta = [None, None, None, None, None, None] 
                title = model.get_value(iter, 4)
                description = ''
                preview = Unity.GenericPreview.new(title.strip (), description.strip (), None)
                if meta[0]:
                    preview.props.image_source_uri = meta[0]
                else:
                    preview.props.image_source_uri = model.get_value(iter, 1)
                if meta[1]:
                    preview.props.subtitle = _("By %s, %s") % (meta[1], date)
                if meta[2]:
                    preview.add_info(Unity.InfoHint.new("camera", _("Camera"), None, meta[2]))
                if meta[3]:
                    preview.add_info(Unity.InfoHint.new("dimensions", _("Dimensions"), None, meta[3]))
                if meta[4]:
                    preview.add_info(Unity.InfoHint.new("size", _("Size"), None, meta[4]))
                if meta[5]:
                    preview.add_info(Unity.InfoHint.new("license", _("License"), None, meta[5]))
                if album:
                    preview.add_info(Unity.InfoHint.new("album", _("Album"), None, album))
                gfile_icon = Gio.file_new_for_path("/usr/share/icons/unity-icon-theme/places/svg/service-picasa.svg")
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


    def getMetadataForPhoto (self, pid):
        """Fetch photo metadata from service"""
        image, author, camera = None, None, None
        size, dimensions, license = None, None, None
        raw_results = urllib.request.urlopen(pid).read ()
        xml_feed = (raw_results.decode("utf8"))
        feed = ET.XML(xml_feed)
        for elem in feed:
            if elem.tag == "{http://search.yahoo.com/mrss/}group":
                for sub in elem:
                    if sub.tag == "{http://search.yahoo.com/mrss/}content":
                        image = sub.get("url")
                    if sub.tag == "{http://search.yahoo.com/mrss/}credit":
                        author = sub.text
            if elem.tag == "{http://schemas.google.com/photos/exif/2007}tags":
                for sub in elem:
                    if sub.tag == "{http://schemas.google.com/photos/exif/2007}model":
                        camera = sub.text
            if elem.tag == "{http://schemas.google.com/photos/2007}license":
                license = elem.get("name")
            if elem.tag == "{http://schemas.google.com/photos/2007}size":
                size = elem.text
            if elem.tag == "{http://schemas.google.com/photos/2007}width":
                width = elem.text
            if elem.tag == "{http://schemas.google.com/photos/2007}height":
                height = elem.text
        dimensions = "%s x %s pixels" % (width, height)
        size = self.humanize_bytes(int(size))
        return [image, author, camera, dimensions, size, license]


    def humanize_bytes(self, bytes, precision=1):
        """Get a humanized string representation of a number of bytes."""
        abbrevs = ((10**15, 'PB'),(10**12, 'TB'),(10**9, 'GB'),(10**6, 'MB'),(10**3, 'kB'),(1, 'b'))
        if bytes == 1:
            return '1 b'
        for factor, suffix in abbrevs:
            if bytes >= factor:
                break
        return '%.*f%s' % (precision, bytes / factor, suffix)


########
# Service authorization handling
########

class SignOnAuthorizer(GObject.Object, GData.Authorizer):
    __g_type_name__ = "SignOnAuthorizer"
    def __init__(self, account_service):
        GObject.Object.__init__(self)
        self._account_service = account_service
        self._token = None

    def do_process_request(self, domain, message):
        message.props.request_headers.replace('Authorization', 'OAuth %s' % (self._token, ))

    def do_is_authorized_for_domain(self, domain):
        return True if self._token else False

    def do_refresh_authorization(self, cancellable):
        old_token = self._token
        # Get the global account settings
        auth_data = self._account_service.get_auth_data()
        identity = auth_data.get_credentials_id()
        session_data = auth_data.get_parameters()
        self._auth_session = Signon.AuthSession.new(identity, auth_data.get_method())
        self._main_loop = GObject.MainLoop()
        self._auth_session.process(session_data,
                        auth_data.get_mechanism(),
                        self.login_cb, None)
        if self._main_loop:
            self._main_loop.run()
        if self._token == old_token:
            return False
        else:
            return True

    def login_cb(self, session, reply, error, user_data):
        print("Picasa: login finished")
        self._main_loop.quit()
        self._main_loop = None
        if error:
            print("Picasa: Got authentication error:", error.message)
            return
        if "AuthToken" in reply:
            self._token = reply["AuthToken"]
        elif "AccessToken" in reply:
            self._token = reply["AccessToken"]
        else:
            print("Didn't find token in session:", reply)
