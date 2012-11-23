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
import time
import datetime
import urllib
import json
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio
from gi.repository import Accounts
from gi.repository import Signon
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
        self._scope = Unity.Scope.new("/net/launchpad/scope/photos/facebook")
        self._sources_options = []

        # Storage for results waiting to be displayed
        self.results_waiting = {1:[], 2:[], 3:[]}

        self.init_session_management ()
        self._enabled = False
        self._authenticating = False
        self._get_accounts_for_service ('facebook')
        self._scope.connect("search-changed", self.on_search_changed)
        self._scope.connect("filters-changed", self.on_lens_active_or_preference_changed)
        self._scope.connect("notify::active", self.on_lens_active_or_preference_changed)
        self._scope.connect('preview-uri', self.on_preview_uri)
        self._scope.props.sources.connect("notify::filtering", self.on_filtering_changed)

        self.preferences = Unity.PreferencesManager.get_default()
        self.preferences.connect("notify::remote-content-search", self.on_lens_active_or_preference_changed)

        self._scope.export ()
        lens.add_local_scope (self._scope)


    def init_session_management (self):
        """ Define a set of variables used for Soup session management """
        self._pending = []
        self._http = []
        for i in range(3):
            self._pending.append(None)
            self._http.append(self._get_http_session ())


    def _get_http_session (self):
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
            print ("Error (facebook): Unable to initialise accounts manager: %s" % e)
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
        print ('Added Facebook account %s' % (account_service))
        source_name = account_service.get_account().get_provider_name ().title()
        if not source_name in self._sources_options:
            self._sources_options.append(source_name)
            self._scope.props.sources.add_option(source_name, source_name, None)


    def _remove_account_service(self, account_service):
        """Remove account from Sources filter"""
        self._enabled = False
        print ('Removed Facebook account %s' % (account_service))
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
        if account.get_provider_name() != "facebook": return
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
            print ('Removed Facebook account')


    def _login(self):
        """Trigger a service login with account credentials"""
        if self._authenticating:
            return
        print ("Facebook : logging in")
        self._authenticating = True
        # Get the global account settings
        auth_data = self._account_service.get_auth_data()
        identity = auth_data.get_credentials_id()
        session_data = auth_data.get_parameters()
        self.auth_session = Signon.AuthSession.new(identity,
                auth_data.get_method())
        self.auth_session.process(session_data,
                auth_data.get_mechanism(),
                self._login_cb, None)


    def _login_cb(self, session, reply, error, user_data):
        """Verify login token"""
        print ("Facebook : login finished")
        self._authenticating = False
        if error:
            print ("Facebook: Got authentication error")
            return
        old_token = self._auth_token
        self._auth_token = reply["AccessToken"]
        if self._auth_token == old_token:
            return
        if self._queued_search:
            self.on_search_changed(*self._queued_search)


########
# Facebook query generators
########


    def _url_maker(self, cat, search_string, date):
        """Select the correct query depending on search parameters"""
        fql, url = None, None
        if date < 0:
            date = 180*86400
            now = int(time.time())
            date = now - date
            date_query = "and created < '%s'" % date
        elif date > 0:
            date_query = "and created > '%s'" % date
        else:
            date_query = ""
        if search_string:
            fql = {'q':'{"q0":"SELECT object_id, src, link, caption, owner, created FROM photo WHERE aid in (SELECT aid FROM album where owner=me() ) and strpos(lower(caption),\'%s\') >= 0 %s LIMIT 50","q3":"SELECT uid, name FROM user where uid in (SELECT uid2 from friend where uid1=me ()) and strpos(lower(name),\'%s\') >= 0","q1":"SELECT object_id, cover_object_id, location, link, name, description, owner FROM album where owner in (SELECT uid2 from friend where uid1=me ()) ORDER BY modified_major DESC","q2":"SELECT object_id, src, link, caption, owner, created FROM photo WHERE album_object_id IN (SELECT object_id FROM #q1) and strpos(lower(caption),\'%s\') >= 0 OR album_object_id IN (SELECT object_id FROM #q1) and owner IN (SELECT uid FROM #q3) %s ORDER BY created DESC LIMIT 50"}' % ( search_string.lower (), date_query, search_string.lower (), search_string.lower (), date_query)}
        else:
            if date == 0:
                self.recent_expected = True
                fql = {'q':'{"qr":"SELECT attachment, message, created_time FROM stream WHERE source_id = me() or source_id in (SELECT uid2 from friend where uid1=me ()) and type = 247 %s LIMIT 100","q0":"SELECT object_id, src, link, caption, owner, created FROM photo WHERE aid in (SELECT aid FROM album where owner=me() ) %s LIMIT 50","q1":"SELECT object_id, cover_object_id, location, link, name, description, owner FROM album where owner in (SELECT uid2 from friend where uid1=me ()) ORDER BY modified_major DESC","q2":"SELECT object_id, src, link, caption, owner, created FROM photo WHERE album_object_id IN (SELECT object_id FROM #q1) %s ORDER BY created DESC LIMIT 100"}' % (date_query.replace("created", "created_time"), date_query.replace("created", "created_time"), date_query)}
            else:
                fql = {'q':'{"q0":"SELECT object_id, src, link, caption, owner, created FROM photo WHERE aid in (SELECT aid FROM album where owner=me() ) %s LIMIT 50","q1":"SELECT object_id, cover_object_id, location, link, name, description, owner FROM album where owner in (SELECT uid2 from friend where uid1=me ()) ORDER BY modified_major DESC","q2":"SELECT object_id, src, link, caption, owner, created FROM photo WHERE album_object_id IN (SELECT object_id FROM #q1) %s ORDER BY created DESC LIMIT 100"}' % (date_query, date_query)}
        if fql:
            url = 'https://graph.facebook.com/fql?%s&access_token=%s' % (urllib.parse.urlencode(fql), self._auth_token)
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
                print ('Facebook : new search %s' % search_string)
                date = self.check_date_filter ()
                i = 0
                if search_string:
#                    for i in range(1,3):
                    if self._pending[i] is not None:
                        self._http[i].cancel_message(self._pending[i],
                                                    Soup.KnownStatusCode.CANCELLED)
                    url = self._url_maker(i, search_string, date)
                    if url:
                        self._pending[i] = Soup.Message.new("GET", url)
                        self._http[i].queue_message(self._pending[i],self._search_cb,[search_string, model, i, search])
                else:
#                    for i in range(3):
                    if self._pending[i] is not None:
                        self._http[i].cancel_message(self._pending[i],
                                                    Soup.KnownStatusCode.CANCELLED)
                    url = self._url_maker(i, search_string, date)
                    if url:
                        self._pending[i] = Soup.Message.new("GET", url)
                        self._http[i].queue_message(self._pending[i],self._search_cb,[search_string, model, i, search])
            else:
                search.finished ()
        else:
            search.finished ()


    def update_results_model(self, search, model, results, cat, recent_done):
        """Update results for category 0, then the others"""
        counter = 0
        if len(results) > 0:
            for photo in results['data']:
                uri = ''
                icon_hint = ''
                comment = ''
                title = ''
                if photo['name'] == 'qr':
                    for p in photo['fql_result_set']:
                        timestamp = p['created_time']
                        try:
                            for media in p['attachment']['media']:
                                counter += 1
                                title = media['alt']
                                comment = str(media['photo']['pid'])+"_ulp-date_"+str(timestamp)
                                uri = media['href']
                                icon_hint = media['src']
                                model.append (uri, icon_hint, 0,"text/html", title, comment, uri)
                                model.flush_revision_queue ()
                        except:
                            pass
                if photo['name'] == 'q0':
                    for p in photo['fql_result_set']:
                        counter += 1
                        timestamp = p['created']
                        title = p['caption']
                        comment = str(p['object_id'])+"_ulp-date_"+str(timestamp)
                        uri = p['link']
                        icon_hint = p['src']
                        model.append (uri, icon_hint, 1,"text/html", title, comment, uri)
                        model.flush_revision_queue ()
                if photo['name'] == 'q2':
                    for p in photo['fql_result_set']:
                        counter += 1
                        timestamp = p['created']
                        title = p['caption']
                        comment = str(p['object_id'])+"_ulp-date_"+str(timestamp)
                        uri = p['link']
                        icon_hint = p['src']
                        model.append (uri, icon_hint, 2,"text/html", title, comment, uri)
                        model.flush_revision_queue ()
            print ('Facebook : Added %i results' % (counter))


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
                photo_id = model.get_value(iter, 5).split("_ulp-date_")[0]
                meta = self.getMetadataForPhoto (photo_id,model.get_value(iter, 2))
                location, date, image, title, description, album, position, album_size = None, None, None, '', '', None, None, None
                if meta[6]:
                    title = meta[6]
                elif meta[5]:
                    title = meta[5]
                else:
                    title = model.get_value(iter, 4)
                if meta[1]:
                    description = meta[1]
                preview = Unity.GenericPreview.new(title.strip (), description.strip (), None)
                if meta[2]:
                    preview.props.image_source_uri = meta[2]
                else:
                    preview.props.image_source_uri = model.get_value(iter, 1)
                if meta[8]:
                    preview.props.subtitle = meta[8]
                if meta[7]:
                    preview.add_info(Unity.InfoHint.new("location", _("Location"), None, meta[7]))
                if meta[9]:
                    album = meta[9]
                    if meta[10] and meta[11]:
                        album = "%s, %i of %i" % (meta[9], meta[10], meta[11])
                    preview.add_info(Unity.InfoHint.new("album", _("Album"), None, album))
                if meta[4]:
                    preview.add_info(Unity.InfoHint.new("with", _("With"), None, meta[4]))

                gfile_icon = Gio.file_new_for_path("/usr/share/icons/unity-icon-theme/places/svg/service-facebook.svg")
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


    def getMetadataForPhoto(self, oid, cat):
        """Fetch photo metadata from service"""
        if cat == 0:
            fql = {'q':'{"query1":"SELECT images, owner, link, caption, created, place_id, album_object_id, position FROM photo WHERE pid=\'%s\'","query2":"SELECT subject, text FROM photo_tag WHERE pid=\'%s\'","query3":"SELECT username, name FROM user WHERE uid IN (SELECT owner FROM #query1)","query4":"SELECT name FROM place WHERE page_id IN (SELECT place_id FROM #query1)","query5":"SELECT name, size FROM album WHERE object_id IN (SELECT album_object_id FROM #query1)"}' % (oid, oid)}
        else:
            fql = {'q':'{"query1":"SELECT images, owner, link, caption, created, place_id, album_object_id, position FROM photo WHERE object_id=%s","query2":"SELECT subject, text FROM photo_tag WHERE object_id=%s","query3":"SELECT username, name FROM user WHERE uid IN (SELECT owner FROM #query1)","query4":"SELECT name FROM place WHERE page_id IN (SELECT place_id FROM #query1)","query5":"SELECT name, size FROM album WHERE object_id IN (SELECT album_object_id FROM #query1)"}' % (oid, oid)}
        url = 'https://graph.facebook.com/fql?%s&access_token=%s' % (urllib.parse.urlencode(fql), self._auth_token)
        raw_results = urllib.request.urlopen(url).read ()
        meta = json.loads(raw_results.decode("utf8"))
        link, caption, image, date = None, None, None, None
        subject, tags, album, position = None, None, None, None
        place, name, username, album_size = None, None, None, None
        tag_list = []
        for m in meta['data'][0]['fql_result_set']:
            date = datetime.datetime.fromtimestamp(m['created']).strftime('%d %b %Y')
            link = m['link']
            caption = m['caption']
            position = m['position']
            image = m['images'][0]['source']
        for m in meta['data'][1]['fql_result_set']:
            if m['text'] not in tag_list:
                tag_list.append(m['text'])
            tags = ", ".join(tag_list)
        for m in meta['data'][2]['fql_result_set']:
            username = m['username']
            name = m['name']
        for m in meta['data'][3]['fql_result_set']:
            place = m['name']
        for m in meta['data'][4]['fql_result_set']:
            album = m['name']
            album_size = m['size']
        return [link,caption, image, subject, tags, username, name, place, date, album, position, album_size]
