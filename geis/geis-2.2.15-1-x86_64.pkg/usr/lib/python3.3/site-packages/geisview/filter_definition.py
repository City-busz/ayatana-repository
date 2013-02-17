#
# @file geisview/filter_definition.py
# @brief A GEIS filter definition dialog
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



import geis
import geisview.defaults
import os
from gi.repository import Gtk

# A list of filter facilities to choose from
geis_filter_facilities = ('GEIS_FILTER_REGION',
                          'GEIS_FILTER_DEVICE',
                          'GEIS_FILTER_CLASS')

geis_region_terms = ('GEIS_REGION_ATTRIBUTE_WINDOWID')

geis_device_terms = ('GEIS_DEVICE_ATTRIBUTE_ID', 
                     'GEIS_DEVICE_ATTRIBUTE_DIRECT_TOUCH')

geis_gesture_terms = ('GEIS_GESTURE_ATTRIBUTE_TOUCHES',
                      'GEIS_CLASS_ATTRIBUTE_NAME')

geis_term_op = {'GEIS_FILTER_OP_EQ': '==',
                'GEIS_FILTER_OP_NE': '!=',
                'GEIS_FILTER_OP_GT': '>',
                'GEIS_FILTER_OP_GE': '>=',
                'GEIS_FILTER_OP_LT': '<',
                'GEIS_FILTER_OP_LE': '<='}

facility_combo_name_col  = 0
facility_combo_value_col = 1


def populate_term_op(store):
    for (name, symbol) in geis_term_op:
        row = store.append()
        store.set(row, symbol, geis.__dict__[name])


class FilterDefinition(object):

    def __init__(self):
        print("FilterDefinition.__init__() begins")
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(geisview.defaults.ui_dir,
                                           "filter_definition.ui"))
        builder.connect_signals(self)

        # prime the name field
        self._dialog = builder.get_object("filter_definition");
        self._name_entry = builder.get_object("name_entry");

        # prime the facility combo
        self._facility_store = builder.get_object("facility_store");
        for fac in geis_filter_facilities:
            row = self._facility_store.append()
            self._facility_store.set(row,
                                     facility_combo_name_col,  fac,
                                     facility_combo_value_col, geis.__dict__[fac])
        self._facility_combo = builder.get_object("facility_combo");
        self._facility_combo.set_active(0)

        # prime the filter terms
        self._term_list_view = builder.get_object("term_list_view");
        self._term_list_store = builder.get_object("term_list_store")

        self._ok_button = builder.get_object("ok_button");
        self._dialog.show_all()
        print("FilterDefinition.__init__() ends")
     
    def run(self):
        print("FilterDefinition.run() begins")
        response = self._dialog.run()
        if (response):
            name = self._name_entry.get_text()
            print("FilterDefinition.run() name=%s" % name)
            print("FilterDefinition.run() facility=%s" % self._facility_store[self._facility_combo.get_active()][facility_combo_value_col])
        self._dialog.destroy()
        print("FilterDefinition.run() ends, response=%s" % response)

    def on_name_changed(self, widget, data=None):
        name = self._name_entry.get_text()
        if len(name) > 0:
            self._ok_button.set_sensitive(True)
        else:
            self._ok_button.set_sensitive(False)
        
    def on_add_term(self, widget, data=None):
        print("FilterDefinition.on_add_term()")
        row = self._term_list_store.append()
        self._term_list_store.set(row,
                                  0, "<attr name>",
                                  1, "==",
                                  2, "<value>")

    def on_edit_term(self, widget, data=None):
        print("FilterDefinition.on_edit_term()")

    def on_remove_term(self, widget, data=None):
        print("FilterDefinition.on_remove_term()")

    def on_term_attr_editing_started(self, widget, entry, path, data=None):
        print("FilterDefinition.on_term_attr_editing_started()")
        choices = Gtk.ListStore(str, str)
        for c in geis_gesture_terms:
            choices.append([c, geis.__dict__[c]])
        completion = Gtk.EntryCompletion()
        completion.set_model(choices)
        completion.set_text_column(0)
        completion.set_inline_completion(True)
        completion.set_popup_completion(False)
        entry.set_completion(completion)
        entry.set_text("")

    def on_term_op_edited(self, widget, path, new_text, data=None):
        print("FilterDefinition.on_term_op_edited(%s, %s, %s)" % (widget, path, new_text))

