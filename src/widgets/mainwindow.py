'''
Created on Sep 8, 2013

@author: eduardo
'''
#!/usr/bin/python3

# Import GI Modules
from gi.repository import Gtk

# Set Python Path to Custom Modules
import sys

sys.path.append('.')

# Import Custom Modules
from widgets.notebooks import DesktopNotebook
from widgets.trees import ConnectionsTreeStore, ConnectionsTreeView
from widgets.uimanager import MainUIManager


class MainWindow(Gtk.Window):

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
        self.uimanager = MainUIManager(self)


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
        tree_scrolled_win = Gtk.ScrolledWindow()
        tree_scrolled_win.set_size_request(250, -1)

        # Initialize Tree View
        self.tree_view = ConnectionsTreeView(self)
        tree_scrolled_win.add(self.tree_view)

        main_panel.add1(tree_scrolled_win)
        self.tree_view.connect("cursor-changed", self.get_row_data)

        # Add Connections Notebook
        self.desktop_notebook = DesktopNotebook()
        main_panel.add2(self.desktop_notebook)

    def get_row_data(self, tree_view):
        tree_selection = self.tree_view.get_selection()
        model, treeiter = tree_selection.get_selected()
        len(model)
        value = self.conn_tree.get_value(treeiter, 2)
        
        print(value)

        if value != self.conn_tree.get_value(self.conn_tree.get_iter_first(), 1):
            self.selected_host = self.tree_structure[value]
            print(self.selected_host)

    def open_host_edition(self, widget):
        """ Since there is a cycle dependency with Pop-up menu and
            Tree View on UIManager, the UIManager call this function
            when right click mouse in order to have all initialized 
            at time of calling the function.
            (Ugly but it makes the trick :P)"""
            
        self.tree_view.open_host_edition(self)

    def on_tab_close_clicked(self, tab_label, notebook, current_page):

        # Set Current Page and Close It
        print(self)
        notebook.set_current_page(current_page)
        notebook.remove_page(current_page)