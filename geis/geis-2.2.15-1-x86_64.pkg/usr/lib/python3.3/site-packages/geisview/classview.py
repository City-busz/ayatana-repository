#
# @file geisview/gesture_classview.py
# @brief GestureClass viewer for geisview.
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



from gi.repository import Gtk

class GestureClassView(Gtk.Window):

    def __init__(self, gesture_classes):
        Gtk.Window.__init__(self)
        self.set_title("GEIS GestureClasss")
        self.set_size_request(200, 200)

        self._tree_store = Gtk.TreeStore(str, str)
        for (class_id, gclass) in gesture_classes.items():
            it = self._tree_store.append(None, ["%s" % gclass.id(),
                                                "%s" % gclass.name()])
        self._tree_view = Gtk.TreeView(self._tree_store)
#        self._tree_view.set_mode(Gtk.SELECTION_SINGLE)

        cell = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('ID')
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', 0)
        self._tree_view.append_column(col)

        cell = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Name')
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', 1)
        self._tree_view.append_column(col)

        self.add(self._tree_view)
        self.show_all()

