'''
Created on Sep 8, 2013

@author: eduardo
'''

from gi.repository import Gtk, Gdk

# Import Custom Modules
from widgets.notebooks import DesktopNotebook
from widgets.trees import ConnectionsTreeStore, ConnectionsTreeView
from widgets.uimanager import MainUIManager


class MainWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Winter Connection Manager")
        
        # Set minimum Window size
        self.set_size_request(600, 500)

        self.maximize()
        
        self.connect("key_press_event", self.on_key_press)

        self.tree_structure = "No File Selected"
        
        # Initialize Open File Attribute
        # I want to control the file name for Save File
        self.open_file = None

        # Add Main Box
        main_box = Gtk.Box()
        main_box.set_property("orientation", Gtk.Orientation.VERTICAL)
        main_box.set_homogeneous(False)
        self.add(main_box)

        # Initialize Connections Tree Store
        self.conn_tree = ConnectionsTreeStore(self.tree_structure)
        
        # Initialize Desktop Notebook
        self.desktop_notebook = DesktopNotebook(self)
        self.desktop_notebook.set_size_request(800, -1)
        
        # Initialize Tree View
        self.tree_view = ConnectionsTreeView(self)
        
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
        tree_scrolled_win.set_size_request(200, -1)

        tree_scrolled_win.add(self.tree_view)

        main_panel.add1(tree_scrolled_win)
        #main_panel.pack1(tree_scrolled_win, True, False)
        self.tree_view.connect("cursor-changed", self.get_row_data)
        self.tree_view.connect("button-press-event",
                               self.tree_view.on_tree_right_mouse,
                               self)
        # Add Connections Notebook
        main_panel.add2(self.desktop_notebook)#, True, False)
        #main_panel.pack2(self.desktop_notebook, True, False)
        
        # Set Search Properties
        self.tree_view.set_enable_search(False)
        

    def get_row_data(self, tree_view):

        tree_selection = self.tree_view.get_selection()
        if tree_selection:
            model, self.selected_iter = tree_selection.get_selected()
            len(model)
            value = model.get_value(self.selected_iter, 2)
            
            if value:
                if value != self.conn_tree.get_value(self.conn_tree.get_iter_first(), 1):
                    self.selected_host = self.tree_structure[value]
                    print(self.selected_host)

    def on_key_press(self, widget, event):
        print(Gdk.keyval_name(event.keyval))
        print(self.desktop_notebook.has_focus())
        print(self.desktop_notebook.resolution_box.has_focus())
        print(self.desktop_notebook.desktop_socket.has_focus())
