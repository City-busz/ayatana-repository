#
# @file geisview/filter_list.py
# @brief A geisview filter list dialog
#
# Copyright (C) 2011 Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#



import geisview.defaults
import geisview.filter_definition
import os
from gi.repository import Gtk

class FilterList(object):

    def __init__(self):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(os.path.join(geisview.defaults.ui_dir,
                                           "filter_list.ui"))
        self._builder.connect_signals(self)

        self._dialog = self._builder.get_object("filter_list");
        self._name_entry = self._builder.get_object("name_entry");
        self._facility_combo = self._builder.get_object("facility_combo");
        self._filter_list_store = self._builder.get_object("filter_list_store")

        self._dialog.show_all()
     
    def run(self):
        print("FilterList.run() begins")
        response = self._dialog.run()
        self._dialog.destroy()
        print("FilterList.run() ends, response=%s" % response)

    def on_add_filter(self, widget, data=None):
        print("FilterList.on_add_filter()")
        dlg = geisview.filter_definition.FilterDefinition()
        dlg.run()

    def on_edit_filter(self, widget, data=None):
        print("FilterList.on_edit_filter()")

    def on_remove_filter(self, widget, data=None):
        print("FilterList.on_remove_filter()")

