'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk, GdkPixbuf, Gdk

# Set Python Path to Custom Modules
#import sys
import subprocess

#sys.path.append('/home/eduardo/workspace/Winter/lib/')

# Import Custom Modules
from widgets.forms import HostEditLayoutObject, FolderEditLayoutObject
from widgets.tablabels import TabLabelCloseButton


class ConnectionsTreeStore(Gtk.TreeStore):
    def __init__(self, tree_structure):
        Gtk.TreeStore.__init__(self, GdkPixbuf.Pixbuf, str, str)

        # Define Tree Icons
        self.folder_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("images/Folder_Icon.png", 15, 15)
        self.conn_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("images/Connection_Icon.png", 15, 15)
        self.file_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("images/File_Icon.png", 15, 15)

        # Add default Message
        print("adding default message to store")
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
                    if tree_structure[k]["ParentID"] == parent_object_id:
                        self.append(self.tree_iter, (self.conn_icon, tree_structure[k]["ObjectName"], tree_structure[k]["ObjectID"]))


class ConnectionsTreeView(Gtk.TreeView):
    def __init__(self, main_window, tree_store, tree_structure, popup_menu):
        Gtk.TreeView.__init__(self, tree_store)
        
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

        self.connect("row-activated", self.on_activate_row, main_window)
        self.connect("button-press-event", self.on_tree_right_mouse, popup_menu)
        

        self.show_all()

    def on_activate_row(self, tree_view, path, column, main_window):
        print(main_window.selected_host)
        self.tab_label = TabLabelCloseButton(main_window.selected_host["ObjectName"], Gtk.STOCK_NETWORK)
        self.tab_label.connect("close-clicked", main_window.on_tab_close_clicked, main_window.desktop_notebook, main_window.desktop_notebook.get_current_page())

        self.socket_id = main_window.desktop_notebook.add_tab(self.tab_label)
        self.resolution = main_window.desktop_notebook.get_box_size()
        print(self.resolution.width, self.resolution.height)
        print(self.socket_id)
        
        desktop_process = [
            "xfreerdp", "-g", str(self.resolution.width) + "x" + str(self.resolution.height), 
            "-u", main_window.selected_host["CredentialUsername"],
            "-p", main_window.selected_host["Password"],
            "-X", self.socket_id,
            "--ignore-certificate",
            main_window.selected_host["PhysicalAddress"]]

        print(desktop_process)

        # desktop_process = [
        #     "xfreerdp", "-g", str(self.resolution.width) + "x" + str(self.resolution.height), 
        #     "-u", "Test", "-p", "Sokatira", "-X", self.socket_id, "192.168.1.103" 
        #     ]

        # print(str(self.widget_size.width) + "x" + str(self.widget_size.height))
        subprocess.Popen(desktop_process)

    def on_tree_right_mouse(self, widget, event, popup_menu):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            path_tuple = widget.get_path_at_pos(int(event.x), int(event.y))
            widget.set_cursor(path_tuple[0], path_tuple[1], False)            
            popup_menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False

    def open_host_edition(self, widget):
        print(widget.selected_host)
        if widget.selected_host["ObjectType"] == "RoyalFolder":
            folder_edit_win = Gtk.Dialog("Folder Properties", widget, (Gtk.DialogFlags.MODAL),
                (Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
            folder_edit_win.set_size_request(300,100)
            
            folder_edit_box = folder_edit_win.get_content_area()
            
            layout = FolderEditLayoutObject(widget.selected_host)
            folder_edit_box.add(layout)
            
            folder_edit_win.show_all()
            
            response = folder_edit_win.run()

            if response == Gtk.ResponseType.OK:
                print("Pressed OK")
            elif response == Gtk.ResponseType.CANCEL:
                print("Pressend CANCEL")
                folder_edit_win.destroy()
    
            folder_edit_win.destroy()
            
        else:    
            # Define Window
            host_edit_win = Gtk.Dialog("Connection Properties", widget, (Gtk.DialogFlags.MODAL),
                (Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
            host_edit_win.set_size_request(400,300)
    
            # Dialog Box sets a default Box container
            # Get access to this Box
            host_edit_box = host_edit_win.get_content_area()
    
            # Add Form Fileds to Box
            layout = HostEditLayoutObject(widget.selected_host)
            host_edit_box.add(layout)
    
            # Show all widgets
            host_edit_win.show_all()
    
            # Get and process Response
            response = host_edit_win.run()
    
            if response == Gtk.ResponseType.OK:
                print("Pressed OK")
            elif response == Gtk.ResponseType.CANCEL:
                print("Pressend CANCEL")
                host_edit_win.destroy()
    
            host_edit_win.destroy()