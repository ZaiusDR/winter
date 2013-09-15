'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk, GdkPixbuf, Gdk

# Import Custom Modules
from widgets.forms import HostEditDialog, HostNewDialog, FolderEditDialog, FolderNewDialog


class ConnectionsTreeStore(Gtk.TreeStore):
    def __init__(self, tree_structure):
        Gtk.TreeStore.__init__(self, GdkPixbuf.Pixbuf, str, str)

        # Define Tree Icons
        self.folder_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("images/Folder_Icon.png", 15, 15)
        self.conn_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("images/Connection_Icon.png", 15, 15)
        self.file_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("images/File_Icon.png", 15, 15)

        # Add default Message
        self.tree_iter = self.append(None, [self.file_icon, tree_structure, ""])


    def create_storage_tree(self, tree_structure):

        # Draw Main Doc, end loop and Get Root Iter and set parent ObjectID
        for k in tree_structure:
            if tree_structure[k]["ObjectType"] == "RoyalDocument":
                self.clear()
                tree_structure[k]["ObjectName"]
                parent_object_id = tree_structure[k]["ObjectID"]
                self.tree_iter = self.append(None, [self.file_icon, tree_structure[k]["ObjectName"], tree_structure[k]["ObjectID"]])
                break

        # Draw Folders and RDP Connections
        for k in tree_structure:
            # Bypass the Root Document
            if tree_structure[k]["ObjectType"] != "RoyalDocument":
                # Check if Object is Folder. The loop go up on tree levels
                # until the Folder parent ID is his real Parent ID
                if tree_structure[k]["ObjectType"] == "RoyalFolder":
                    while parent_object_id != tree_structure[k]["ParentID"]:
                        self.tree_iter = self.iter_parent(self.tree_iter)
                        parent_object_id = tree_structure[self.get(self.tree_iter, 2)[0]]["ObjectID"]
                    
                    self.tree_iter = self.append(self.tree_iter, (self.folder_icon, tree_structure[k]["ObjectName"], tree_structure[k]["ObjectID"]))
                    parent_object_id = tree_structure[k]["ObjectID"]
                # If Object is RDP Conn, just Add it
                elif tree_structure[k]["ObjectType"] == "RoyalRDSConnection":
                    while parent_object_id != tree_structure[k]["ParentID"]:
                        self.tree_iter = self.iter_parent(self.tree_iter)
                        parent_object_id = tree_structure[self.get(self.tree_iter, 2)[0]]["ObjectID"]
                    self.append(self.tree_iter, (self.conn_icon, tree_structure[k]["ObjectName"], tree_structure[k]["ObjectID"]))
                    

class ConnectionsTreeView(Gtk.TreeView):
    def __init__(self, main_window):
        Gtk.TreeView.__init__(self, main_window.conn_tree)
        
        #Create Tree View and Columns Text and Icons
        (COL_PIXBUF, COL_STRING) = range(2)
        
        self.column = Gtk.TreeViewColumn()
        self.column.set_title("Hosts")
        self.append_column(self.column)
        
        self.renderer_pixbuf = Gtk.CellRendererPixbuf()
        self.column.pack_start(self.renderer_pixbuf,expand=False)
        self.column.add_attribute(self.renderer_pixbuf, 'pixbuf', COL_PIXBUF)
        
        self.renderer_text = Gtk.CellRendererText()
        self.column.pack_start(self.renderer_text, expand=True)
        self.column.add_attribute(self.renderer_text, 'text', COL_STRING)

        self.connect("row-activated", main_window.desktop_notebook.add_tab, main_window)

        self.show_all()
        
    def on_tree_right_mouse(self, widget, event, main_window):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            path_tuple = widget.get_path_at_pos(int(event.x), int(event.y))
            widget.set_cursor(path_tuple[0], path_tuple[1], False)
            # If Clicked a RDP disable New Objects Menu
            if main_window.selected_host["ObjectType"] == "RoyalRDSConnection":
                main_window.uimanager.action_popup_new.set_sensitive(False)
            else:
                main_window.uimanager.action_popup_new.set_sensitive(True)
            main_window.popup_menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False

    def open_host_edition(self, widget, main_window):
        if main_window.selected_host["ObjectType"] == "RoyalFolder":
            # Show Folder Properties Object
            FolderEditDialog(main_window)
        else:    
            # Show Host Properties Object
            HostEditDialog(main_window)
            
    def on_activate_popup_new_conn(self, action, main_window):
        # Show Host Properties Object
        HostNewDialog(main_window)
        
    def on_activate_popup_new_folder(self, action, main_window):
        # Show Folder Properties Object
        FolderNewDialog(main_window)
