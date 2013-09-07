#!/usr/bin/python3

# Import GI Modules
from gi.repository import Gtk, Unity, Dbusmenu

# Set Python Path to Custom Modules
import sys

#sys.path.append('/home/eduardo/workspace/winter/src')

# Import Custom Modules
from widgets.notebooks import DesktopNotebook
from widgets.trees import ConnectionsTreeStore, ConnectionsTreeView
from widgets.uimanager import MainUIManager


class mainWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="WinCon")
        
        # Set minimum Window size
        self.set_size_request(600, 500)

        self.maximize()

        self.tree_structure = "No File Selected"

        # Add Main Box
        main_box = Gtk.Box()
        main_box.set_property("orientation", Gtk.Orientation.VERTICAL)
        main_box.set_homogeneous(False)
        self.add(main_box)

        # Initialize Connections Tree Store
        self.conn_tree = ConnectionsTreeStore(self.tree_structure)

        #Add Menu bar and Tool Bar to Main Grid
        self.uimanager = MainUIManager(self.conn_tree, self,
                                         self.tree_structure)

        #uimanager = self.draw_menu_bar()
        self.menu = self.uimanager.get_widget("/MenuBar")
        main_box.pack_start(self.menu, False, False, 0)

        self.toolbar = self.uimanager.get_widget("/ToolBar")
        self.toolbar.set_property("valign", 1)
        main_box.pack_start(self.toolbar, False, False, 0)

        self.popup_menu = self.uimanager.get_widget("/HostPopupMenu")

        #Add Paned Widget
        main_panel = Gtk.Paned()
        main_box.pack_end(main_panel, True, True, 0)

        #Add Tree View to Main Panel
        self.tree_scrolled_win = Gtk.ScrolledWindow()
        self.tree_scrolled_win.set_size_request(250, -1)

        self.tree_view = ConnectionsTreeView(self, self.conn_tree, self.tree_structure)
        self.tree_scrolled_win.add(self.tree_view)

        main_panel.add1(self.tree_scrolled_win)
        self.connect("cursor-changed", self.get_row_data, tree_structure)

        # Add Connections Notebook
        self.desktop_notebook = DesktopNotebook()
        main_panel.add2(self.desktop_notebook)

    def get_row_data(self, tree_view, tree_structure):
        tree_selection = self.get_selection()
        tree_store, treeiter = tree_selection.get_selected()
        value = tree_store.get_value(treeiter, 2)
        
        print(value)

        if value != tree_store.get_value(tree_store.get_iter_first(), 1):
            self.selected_host = tree_structure[value]

    def open_host_edition(self, widget):
        self.conn_tree.open_host_edition(self)

    def on_tab_close_clicked(self, tab_label, notebook, current_page):

        # Set Current Page and Close It
        print(self)
        notebook.set_current_page(current_page)
        notebook.remove_page(current_page)


def unity_integration():
    launcher = Unity.LauncherEntry.get_for_desktop_id("winter.desktop")
    launcher.set_property("urgent", True)
    ql = Dbusmenu.Menuitem.new()
    item = Dbusmenu.Menuitem.new()
    item.property_set(Dbusmenu.MENUITEM_PROP_LABEL, "Item 1")
    item.property_set_bool(Dbusmenu.MENUITEM_PROP_VISIBLE, True)
    ql.child_append(item)
    launcher.set_property("quicklist", ql)


win = mainWindow()
unity_integration()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()