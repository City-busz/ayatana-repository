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

import gettext
import locale
import sys, os
from gi.repository import GLib, GObject, Gio, Unity, Dee
import time, datetime
import shutil
import sqlite3

APP_NAME = "unity-lens-photos"
LOCAL_PATH = "/usr/share/locale/"

gettext.bindtextdomain(APP_NAME, LOCAL_PATH)
gettext.textdomain(APP_NAME)
_ = gettext.gettext

# Translatable strings
SOURCE = _("This Computer")
NO_RESULTS_HINT = _("Sorry, there are no photos that match your search.")

CACHE = "%s/unity-lens-photos" % GLib.get_user_cache_dir()
THUMB_CACHE = "%s/shotwell/thumbs/" % GLib.get_user_cache_dir()
HOME_FOLDER = GLib.get_home_dir()

class Scope:

    """Creation of the Shotwell scope."""
    def __init__ (self, lens):
        self._enabled = True
        self._scope = Unity.Scope.new ("/net/launchpad/scope/photo/shotwell")
        self._scope.connect ("search-changed", self.on_search_changed)
        self._scope.connect ("filters-changed", self.on_lens_active)
        self._scope.connect("notify::active", self.on_lens_active)
        self._scope.props.sources.connect("notify::filtering", self.on_filtering_changed)
        self._scope.connect('preview-uri', self.on_preview_uri)
        self._scope.props.provides_personal_content=True
        source_name = SOURCE
        self.last_db_change = None
        self._sources_options = []
        self._sources_options.append(source_name)
        self._scope.props.sources.add_option(source_name,source_name, None)
        self._scope.export()
        lens.add_local_scope (self._scope)
        self.tagdb = []
        self.db = None
        self.cancel_running_search = False


    def on_filtering_changed(self, *_):
        """Update results when a filter change is notified."""
        for source in self._sources_options:
            filtering = self._scope.props.sources.props.filtering
            active = self._scope.props.sources.get_option(source).props.active
            if (active and filtering) or (not active and not filtering):
                if not self._enabled:
                    self._enabled = True
                    self._scope.queue_search_changed(Unity.SearchType.DEFAULT)
            else:
                self._enabled = False
                self._scope.queue_search_changed(Unity.SearchType.DEFAULT)
            print ("    %s enabled : %s" % (source, self._enabled))


    def on_lens_active(self, *_):
        """ Update results when the lens is opened """
#        if self._scope.props.active:
        self._scope.queue_search_changed(Unity.SearchType.DEFAULT)


    def on_search_changed(self, scope, search, search_type, *_):
        """Run another search when a filter change is notified."""
        self.cancel_running_search = True
        model = search.props.results_model
        search.set_reply_hint ("no-results-hint", GLib.Variant.new_string(NO_RESULTS_HINT))
        model.clear()
        search_string = search.props.search_string.strip()
        print ("Search changed to \"%s\"" % search_string)
        if self._enabled:
            date = self.check_date_filter ()
            if search_type is Unity.SearchType.GLOBAL:
                if len(search_string) > 0:
                    cats = [4]
                    GLib.idle_add(self.update_results_model,search_string, model, cats, date, search)
                else:
                    search.finished()
            else:
                if search_string or date:
                    cats = [1]
                else:
                    cats = [0,1]
                GLib.idle_add(self.update_results_model,search_string, model, cats, date, search)
        else:
            search.finished()
        


    def update_results_model(self, search, model, cats, date, s):
        """Update model with Shotwell results"""
        for cat in cats:
            if cat == 0:
                limit = 50
            else:
                limit = 100
            for i in self.shotwell(search, date, limit):
                if not self.cancel_running_search:
                    hex_id = "%x" % i[4]
                    thumb_id = ("thumb" + "0"*(16 - len(hex_id)) + hex_id)
                    try:
                        extension = i[1].split('.')[-1].lower ()
                    except:
                        extension = "jpg"
                    icon_hint = THUMB_CACHE + "thumbs128/" + thumb_id + "." + extension
                    if not self.is_file (icon_hint):
                        icon_hint = THUMB_CACHE + "thumbs360/" + thumb_id + "." + extension
                        if not self.is_file (icon_hint):
                            icon_hint = i[1]
                            if not self.is_file (icon_hint):
                                icon_hint = "image"
                    title = i[0]
                    comment = i[3]
                    uri = "file://"+i[1]
                    model.append (uri, icon_hint, cat,"text/html", title, comment, uri)
        s.finished ()


    def on_preview_uri(self, scope, uri):
            """Preview request handler"""
            preview = None
            for model in [self._scope.props.results_model, self._scope.props.global_results_model]:
                iter = model.get_first_iter()
                end_iter = model.get_last_iter()
                while iter != end_iter:
                    if model.get_value(iter, 0) == uri:
                        title = model.get_value(iter, 4)
                        desc = ''
                        out_of_drive = False
                        if self.is_file (uri.replace("file://", "")):
                            title = self.getTitle (uri.replace("file://", ""), model.get_value(iter, 4))
                            # Test existence of a jpg thumb for raw files
                            raw_thumb = uri.replace("file://", "")
                            raw_thumb = raw_thumb.replace(".", "_")+"_shotwell.jpg"
                            if self.is_file(raw_thumb):
                                image = "file://"+raw_thumb
                            else:
                                image = uri
                        else:
                            image = "file://"+model.get_value(iter, 1)
                            desc = _("<b>This photo is missing.</b>\nYou can open Shotwell to retrieve it or remove it from your library.")
                            out_of_drive = True
                        preview = Unity.GenericPreview.new(title, desc, None)
                        preview.props.image_source_uri = image
                        subtitle = model.get_value(iter, 5).split("_ulp-date_")[0]
                        if subtitle:
                            preview.props.subtitle = subtitle
                        db = self.getDB ()
                        if db:
                            photo = self.getPhotoForUri (db, uri)
                            if photo:
                                width = str(photo[2])
                                height = str(photo[3])
                                filesize = self.humanize_bytes(photo[4])
                                dimensions = _("%s x %s pixels") % (width, height)
                                tags_raw = self.getTagsForPhotoId(db, photo[0])
                                tags = ', '.join(tags_raw.split("__"))[2:]
                                if dimensions:
                                    preview.add_info(Unity.InfoHint.new("dimensions", _("Dimensions"), None, dimensions))
                                if filesize:
                                    preview.add_info(Unity.InfoHint.new("size", _("Size"), None, filesize))
                                if tags:
                                    preview.add_info(Unity.InfoHint.new("tags", _("Tags"), None, tags))
                        if not out_of_drive:
                            view_action = Unity.PreviewAction.new("view", _("View"), None)
                            view_action.connect('activated', self.view_action)
                            preview.add_action(view_action)
                            
                            show_action = Unity.PreviewAction.new("show", _("Show in Folder"), None)
                            show_action.connect('activated', self.show_action)
                            preview.add_action(show_action)
                            
                            email_action = Unity.PreviewAction.new("email", _("Email"), None)
                            email_action.connect('activated', self.email_action)
                            preview.add_action(email_action)
                            
                            print_action = Unity.PreviewAction.new("print", _("Print"), None)
                            print_action.connect('activated', self.print_action)
                            preview.add_action(print_action)
                        else:
                            shotwell_action = Unity.PreviewAction.new("shotwell", _("Open Shotwell"), None)
                            shotwell_action.connect('activated', self.shotwell_action)
                            preview.add_action(shotwell_action)
                        break
                    iter = model.next(iter)
            if preview == None:
                print ("Couldn't find model row for requested preview uri: '%s'", uri)
            return preview


    def print_action (self, scope, uri):
        """On item clicked, print photo"""
        GLib.spawn_async(["/usr/bin/lpr", uri.replace("file://", "")])
        return Unity.ActivationResponse(goto_uri='', handled=2 )


    def email_action (self, scope, uri):
        """On item clicked, email photo"""
        mail_app = Gio.AppInfo.get_default_for_uri_scheme("mailto")
        if mail_app:
            attach = Gio.file_new_for_uri(uri)
            mail_app.launch ([attach], None)
        return Unity.ActivationResponse(goto_uri='', handled=2 )


    def show_action (self, scope, uri):
        """On item clicked, show photo in folder"""
        GLib.spawn_async(["/usr/bin/nautilus", uri])
        return Unity.ActivationResponse(goto_uri='', handled=2 )

    def view_action (self, scope, uri):
        """On item clicked, view photo"""
        return
    
    def shotwell_action (self, scope, uri):
        """On item clicked, open Shotwell"""
        GLib.spawn_async(["/usr/bin/shotwell"])
        return Unity.ActivationResponse(goto_uri='', handled=2 )


    def check_date_filter(self):
        """Get active option for a filter name"""
        try:
            date = self._scope.get_filter("date").get_active_option().props.id
            date = int(date)*86400
            now = time.time()
            date = now - date
        except (AttributeError):
            date = None
        return date


    def is_file(self, uri):
        """Check if the photo is an actual existing file"""
        g_file = Gio.file_new_for_path(uri)
        if g_file.query_exists(None):
            file_type = g_file.query_file_type(Gio.FileQueryInfoFlags.NONE,
                None)
            if file_type is Gio.FileType.REGULAR:
                return True
    
    def last_modification(self, uri):
        """Check if the photo is an actual existing file"""
        g_file = Gio.file_new_for_path(uri)
        time = g_file.query_info(Gio.FILE_ATTRIBUTE_TIME_MODIFIED,
                                 Gio.FileQueryInfoFlags.NONE,
                                 None).get_attribute_uint64('time::modified')
        return time


    def shotwell(self, search, date, limit):
        """Create a list of results by querying the DB and parsing Shotwell data"""
        data_list = []
        db = self.getDB ()
        if db:
            eventcursor = db.cursor()
            self.cancel_running_search = False
            try:
                photos = self.getPhotos (db, date)
            except:
                photos = []
            i = 0
            for photo in photos:
                if photo[16] != 4 and photo[16] != 8 and not self.cancel_running_search:
                    item_list = []
                    event_id = str(photo[10])
                    uri = photo[1]
                    pid = photo[0]
                    try:
                        event = self.getEventNameForEventId (db, event_id, eventcursor)
                    except:
                        event = ''
                    icon_hint = photo[1]
                    title = photo[19]
                    if not title:
                        title = uri.split("/")[-1]
                    timestamp = photo[6]
                    if timestamp == 0:
                        timestamp = photo[5]
                    date = datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %Y %H:%M')
                    match = False
                    if not search:
                        match = True
                    else:
                        match_list = []
                        search_items = search.split(" ")
                        for item in search_items:
                            if (title.lower().find(item.lower())  > -1
                                or event.lower().find(item.lower())  > -1
                                or self.isInTagDB (item.lower (), pid)):
                                match_list.append (True)
                            else:
                                match_list.append (False)
                        if all(match_list):
                            match = True
                    if match and i < limit:
                        item_list.append(title)
                        item_list.append(uri)
                        item_list.append(icon_hint)
                        item_list.append(date+"_ulp-date_"+str(timestamp))
                        item_list.append(pid)
                        data_list.append(item_list)
                        i += 1
            eventcursor.close ()
        return data_list

    def isInTagDB (self, term, photo):
        for tag in self.tagdb:
            if tag[0].lower().find(term)  > -1:
                hex_id = "%x" % photo
                thumb_id = ("thumb" + "0"*(16 - len(hex_id)) + hex_id)
                if tag[1]:
                    if tag[1].find(thumb_id) > -1:
                        return True
        return False


    def getDB (self):
        """Check existence of our copy of Shotwell DB"""
        db = None
        newdb = False
        shotwell_desktop = "/usr/share/applications/shotwell.desktop"
        if self.is_file(shotwell_desktop):
            if not Gio.file_new_for_path(CACHE).query_exists(None):
                Gio.file_new_for_path(CACHE).make_directory(None)
            shotwell_db_oldversion = HOME_FOLDER +"/.shotwell/data/photo.db"
            shotwell_db = HOME_FOLDER +"/.local/share/shotwell/data/photo.db"
            if self.is_file(shotwell_db):
                if self.last_db_change != self.last_modification (shotwell_db):
                    print ("Shotwell: DB update detected")
                    shutil.copy2(shotwell_db, CACHE+"/photos.db")
                    self.last_db_change = self.last_modification (shotwell_db)
                    newdb = True
                if self.is_file(CACHE+"/photos.db") and newdb:
                    db = sqlite3.connect(CACHE+"/photos.db")
                else:
                   db = self.db
            elif self.is_file(shotwell_db_oldversion):
                if self.last_db_change != self.last_modification (shotwell_db_oldversion):
                    print ("Shotwell: DB update detected")
                    shutil.copy2(shotwell_db_oldversion, CACHE+"/photos.db")
                    self.last_db_change = self.last_modification (shotwell_db_oldversion)
                    newdb = True
                if self.is_file(CACHE+"/photos.db") and newdb:
                    db = sqlite3.connect(CACHE+"/photos.db")
                else:
                    db = self.db
            else:
                pass
        if db and newdb:
            self.getAllTags (db)
            self.db = db
        return db


    def getPhotos (self, db, date):
        """Get all photos in DB"""
        if date:
            if date > 0:
                sql = 'select * from PhotoTable where exposure_time > '+str(date)+' or timestamp > '+str(date)+' order by timestamp desc, exposure_time desc'
            else:
                date = 180*86400
                now = int(time.time())
                date = now - date
                sql = 'select * from PhotoTable where exposure_time < '+str(date)+' and exposure_time != 0 or timestamp < '+str(date)+' and exposure_time = 0 order by timestamp desc, exposure_time desc'
        else:
            sql='select * from PhotoTable order by timestamp desc, exposure_time desc'
        cursor = db.cursor()
        photos = cursor.execute(sql).fetchall()
        cursor.close ()
        return photos


    def getPhotoForUri (self, db, uri):
        filename = uri.replace("file://", "")
        print (filename)
        sql='select * from PhotoTable where filename = \"'+filename+'\"'
        cursor = db.cursor()
        photo = cursor.execute(sql).fetchone()
        return photo


    def getAllTags (self, db):
        """Get all tags"""
        sql='SELECT name, photo_id_list FROM TagTable'
        cursor = db.cursor()
        tags = cursor.execute(sql).fetchall()
        cursor.close ()
        self.tagdb = tags


    def getEventNameForEventId (self, db, event_id, cursor):
        """Get event name related for a photo's event id"""
        raw_event = []
        event = None
        sql='select name from EventTable where id='+event_id
        raw_event = cursor.execute(sql).fetchone()
        if raw_event:
            event = raw_event[0]
        return str(event)


    def getTitle(self, uri, title):
        """Get date from timestamp in db or from file"""
        if not title:
            g_file = Gio.file_new_for_path(uri)
            title = g_file.query_info(Gio.FILE_ATTRIBUTE_STANDARD_DISPLAY_NAME,
                                    Gio.FileQueryInfoFlags.NONE,
                                    None).get_attribute_string('standard::display-name')
        return title

    def getDate(self, uri, time):
        """Get date from timestamp in db or from file"""
        if time > 0:
            timestamp = time
        else:
            g_file = Gio.file_new_for_path(uri)
            timestamp = g_file.query_info(Gio.FILE_ATTRIBUTE_TIME_CREATED,
                                    Gio.FileQueryInfoFlags.NONE,
                                    None).get_attribute_uint64('time::created')
        if timestamp > 0:
            date = datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %Y %H:%M')
        else:
            date = ''
        return date, timestamp


    def getTagsForPhotoId (self, db, photo):
        """Get all tags related to a photo"""
        hex_id = "%x" % photo
        thumb_id = ("thumb" + "0"*(16 - len(hex_id)) + hex_id)
        sql='SELECT name FROM TagTable WHERE photo_id_list LIKE ?'
        args=['%'+thumb_id+'%']
        cursor = db.cursor ()
        tags = cursor.execute(sql, args).fetchall()
        cursor.close ()
        string_of_tags = ""
        if len(tags) > 0:
            for t in tags:
                string_of_tags = string_of_tags +"__"+t[0]
        return string_of_tags


    def humanize_bytes(self, bytes, precision=1):
        """Get a humanized string representation of a number of bytes."""
        abbrevs = ((10**15, 'PB'),(10**12, 'TB'),(10**9, 'GB'),(10**6, 'MB'),(10**3, 'kB'),(1, 'b'))
        if bytes == 1:
            return '1 b'
        for factor, suffix in abbrevs:
            if bytes >= factor:
                break
        return '%.*f%s' % (precision, bytes / factor, suffix)
