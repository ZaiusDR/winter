'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk, GdkPixbuf

import random

# Import Custom Modules
from widgets.formfields import FormField
from widgets.tablabels import EditHostTabLabel


class HostEditDialog(Gtk.Dialog):
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, "Connection Properties", main_window, (Gtk.DialogFlags.MODAL),
                (Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_size_request(400,300)
        
        # Dialog Box sets a default Box container
        # Get access to this Box
        host_edit_box = self.get_content_area()
        #Box Properties
        host_edit_box.set_orientation(Gtk.Orientation.VERTICAL)
        host_edit_box.set_spacing(5)

        print(main_window.selected_host)
        # Host Name Entry
        host_name_label = Gtk.Label("Host Name")
        self.host_name_entry = Gtk.Entry()
        if main_window.selected_host["ObjectName"]:
            self.host_name_entry.set_text(main_window.selected_host["ObjectName"])
        host_name_form = FormField(host_name_label, self.host_name_entry)
        host_edit_box.pack_start(host_name_form, True, True, 5)

        # Notebook and Config Tabs
        edit_notebook = Gtk.Notebook()

        #############################################################################
        # Basic Tab Layout
        basic_box = Gtk.Box()
        basic_box.set_orientation(Gtk.Orientation.VERTICAL)
        basic_box.set_spacing(5)
        basic_box.set_homogeneous(True)

        # IP Field
        server_label = Gtk.Label("Server/IP")
        self.server_entry = Gtk.Entry()
        if main_window.selected_host["PhysicalAddress"]:
            self.server_entry.set_text(main_window.selected_host["PhysicalAddress"])
        server_form = FormField(server_label, self.server_entry)

        # Username Field
        username_label = Gtk.Label("User Name")
        self.username_entry = Gtk.Entry()
        if main_window.selected_host["CredentialUsername"]:
            self.username_entry.set_text(main_window.selected_host["CredentialUsername"])
        username_form = FormField(username_label, self.username_entry)

        # Password Field
        password_label = Gtk.Label("Password")
        self.password_entry = Gtk.Entry()
        if main_window.selected_host["Password"]:
            self.password_entry.set_text(main_window.selected_host["Password"])
        self.password_entry.set_visibility(False)
        password_form = FormField(password_label, self.password_entry)

        # Resolution Field
        resol_label = Gtk.Label("Label")
        resol_combo = Gtk.ComboBoxText()
        resolutions = [ "Workarea (Default)", "640x480", "1024x768", "1152x864", "1280x960", "1400x1050" ]
        for resolution in resolutions:
            resol_combo.append_text(resolution)
        resol_combo.set_active(0)
        resol_form = FormField(resol_label, resol_combo)

        # Color Depth
        color_label = Gtk.Label("Color Depth")
        color_combo = Gtk.ComboBoxText()
        colors = [ "True Color (32 bit)", "True Color (24 bit)", "High Color (16 bit)"
            , "High Color (15 bit)", "256 colors (8 bit)"]
        for color in colors:
            color_combo.append_text(color)
        color_combo.set_active(1)
        color_form = FormField(color_label, color_combo)

        # Add Widgets to Basic Box
        basic_box.pack_start(server_form, True, True, 0)
        basic_box.pack_start(username_form, True, True, 0)
        basic_box.pack_start(password_form, True, True, 0)
        basic_box.pack_start(resol_form, True, True, 0)
        basic_box.pack_start(color_form, True, True, 0)

        # Add Basic Tab to Notebook
        basic_tab_label = EditHostTabLabel("Basic", Gtk.STOCK_PROPERTIES)
        edit_notebook.append_page(basic_box, basic_tab_label)
        
        #############################################################################
        # Advanced Tab Layout
        advanced_box = Gtk.Box()
        advanced_box.set_orientation(Gtk.Orientation.VERTICAL)
        advanced_box.set_spacing(5)
        advanced_box.set_homogeneous(True)

        # Quality Combo
        speed_label = Gtk.Label("Quality")
        speed_combo = Gtk.ComboBoxText()
        speeds = [ "Modem", "BroadBand", "LAN" ]
        for speed in speeds:
            speed_combo.append_text(speed)
        speed_combo.set_active(1)
        speed_form = FormField(speed_label, speed_combo)

        # Add Widgets to Advanced Box
        advanced_box.pack_start(speed_form, True, False, 0)

        # Add Advanced Tab to Notebook
        advanced_tab_label = EditHostTabLabel("Advanced", Gtk.STOCK_PREFERENCES)
        edit_notebook.append_page(advanced_box, advanced_tab_label)

        # Finally add Notebook to Box
        host_edit_box.pack_start(edit_notebook, True, True, 10)
        
        self.show_all()

        # Get and process Response
        while True:
            response = self.run()                

            if response == Gtk.ResponseType.APPLY:
                self.save_host_info(main_window)
            elif response == Gtk.ResponseType.OK:
                self.save_host_info(main_window)
                self.destroy()
                break
            elif response == Gtk.ResponseType.CANCEL:
                self.destroy()
                break
            
    def save_host_info(self, main_window):
        # Server Name
        if main_window.selected_host["ObjectName"] != self.host_name_entry.get_text():
            for_each_value = main_window.selected_host["ObjectName"]
            main_window.conn_tree.foreach(self.for_each_row, for_each_value)
            main_window.tree_structure[main_window.selected_host["ObjectID"]]["ObjectName"] = self.host_name_entry.get_text()
        
        # IP
        if main_window.selected_host["PhysicalAddress"] != self.server_entry.get_text():
            main_window.tree_structure[main_window.selected_host["ObjectID"]]["PhysicalAddress"] = self.server_entry.get_text()
            
    
    def for_each_row(self, tree_model, path, tree_iter, value):
        if tree_model.get_value(tree_iter, 1) == value:
            tree_model.set_value(tree_iter, 1, self.host_name_entry.get_text())
            

class HostNewDialog(Gtk.Dialog):
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, "Connection Properties", main_window, (Gtk.DialogFlags.MODAL),
                (Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_size_request(400,300)
        
        # Dialog Box sets a default Box container
        # Get access to this Box
        host_edit_box = self.get_content_area()
        #Box Properties
        host_edit_box.set_orientation(Gtk.Orientation.VERTICAL)
        host_edit_box.set_spacing(5)

        print(main_window.selected_host)
        # Host Name Entry
        host_name_label = Gtk.Label("Host Name")
        self.host_name_entry = Gtk.Entry()
        host_name_form = FormField(host_name_label, self.host_name_entry)
        host_edit_box.pack_start(host_name_form, True, True, 5)

        # Notebook and Config Tabs
        edit_notebook = Gtk.Notebook()

        #############################################################################
        # Basic Tab Layout
        basic_box = Gtk.Box()
        basic_box.set_orientation(Gtk.Orientation.VERTICAL)
        basic_box.set_spacing(5)
        basic_box.set_homogeneous(True)

        # IP Field
        server_label = Gtk.Label("Server/IP")
        self.server_entry = Gtk.Entry()
        server_form = FormField(server_label, self.server_entry)

        # Username Field
        username_label = Gtk.Label("User Name")
        self.username_entry = Gtk.Entry()
        username_form = FormField(username_label, self.username_entry)

        # Password Field
        password_label = Gtk.Label("Password")
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        password_form = FormField(password_label, self.password_entry)

        # Resolution Field
        resol_label = Gtk.Label("Label")
        resol_combo = Gtk.ComboBoxText()
        resolutions = [ "Workarea (Default)", "640x480", "1024x768", "1152x864", "1280x960", "1400x1050" ]
        for resolution in resolutions:
            resol_combo.append_text(resolution)
        resol_combo.set_active(0)
        resol_form = FormField(resol_label, resol_combo)

        # Color Depth
        color_label = Gtk.Label("Color Depth")
        color_combo = Gtk.ComboBoxText()
        colors = [ "True Color (32 bit)", "True Color (24 bit)", "High Color (16 bit)"
            , "High Color (15 bit)", "256 colors (8 bit)"]
        for color in colors:
            color_combo.append_text(color)
        color_combo.set_active(1)
        color_form = FormField(color_label, color_combo)

        # Add Widgets to Basic Box
        basic_box.pack_start(server_form, True, True, 0)
        basic_box.pack_start(username_form, True, True, 0)
        basic_box.pack_start(password_form, True, True, 0)
        basic_box.pack_start(resol_form, True, True, 0)
        basic_box.pack_start(color_form, True, True, 0)

        # Add Basic Tab to Notebook
        basic_tab_label = EditHostTabLabel("Basic", Gtk.STOCK_PROPERTIES)
        edit_notebook.append_page(basic_box, basic_tab_label)
        
        #############################################################################
        # Advanced Tab Layout
        advanced_box = Gtk.Box()
        advanced_box.set_orientation(Gtk.Orientation.VERTICAL)
        advanced_box.set_spacing(5)
        advanced_box.set_homogeneous(True)

        # Quality Combo
        speed_label = Gtk.Label("Quality")
        speed_combo = Gtk.ComboBoxText()
        speeds = [ "Modem", "BroadBand", "LAN" ]
        for speed in speeds:
            speed_combo.append_text(speed)
        speed_combo.set_active(1)
        speed_form = FormField(speed_label, speed_combo)

        # Add Widgets to Advanced Box
        advanced_box.pack_start(speed_form, True, False, 0)

        # Add Advanced Tab to Notebook
        advanced_tab_label = EditHostTabLabel("Advanced", Gtk.STOCK_PREFERENCES)
        edit_notebook.append_page(advanced_box, advanced_tab_label)

        # Finally add Notebook to Box
        host_edit_box.pack_start(edit_notebook, True, True, 10)
        
        self.show_all()

        # Get and process Response
        while True:
            response = self.run()                

            if response == Gtk.ResponseType.APPLY:
                self.save_new_host_info(main_window)
            elif response == Gtk.ResponseType.OK:
                self.save_new_host_info(main_window)
                self.destroy()
                break
            elif response == Gtk.ResponseType.CANCEL:
                self.destroy()
                break
            
    def save_new_host_info(self, main_window):
        # Initialize Node Values
        object_id = str(random.randrange(20**15))
        conn_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("images/Connection_Icon.png", 15, 15)
        
        # Append to Tree and Expand for visibility
        main_window.conn_tree.append(main_window.selected_iter, (conn_icon, 
                                                                 self.host_name_entry.get_text(),
                                                                 object_id))
        main_window.tree_view.expand_row(main_window.conn_tree.get_path(main_window.selected_iter),
                                         False)
        
        # Append to Tree Structure Dict
        main_window.tree_structure[object_id] = { "ObjectType" : "RoyalRDSConnection",
                                                  "ObjectName" : self.host_name_entry.get_text(),
                                                  "ObjectID" : object_id,
                                                  "PhysicalAddress" : self.server_entry.get_text(),
                                                  "CredentialUsername" : self.username_entry.get_text(),
                                                  "Password" : self.password_entry.get_text(),
                                                  "ParentID" : main_window.selected_host["ObjectID"] }
        

class FolderEditDialog(Gtk.Dialog):
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, "Folder Properties", main_window, (Gtk.DialogFlags.MODAL),
                (Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_size_request(300,100)
        
        folder_edit_box = self.get_content_area()
        
        folder_edit_box.set_orientation(Gtk.Orientation.VERTICAL)
        folder_edit_box.set_spacing(5)

        # Folder Name Entry
        folder_name_label = Gtk.Label("Folder Name")
        self.folder_name_entry = Gtk.Entry()
        if main_window.selected_host["ObjectName"]:
            self.folder_name_entry.set_text(main_window.selected_host["ObjectName"])
        folder_name_form = FormField(folder_name_label, self.folder_name_entry)
        folder_edit_box.pack_start(folder_name_form, True, True, 5)
        
        self.show_all()

        while True:
            response = self.run()                

            if response == Gtk.ResponseType.APPLY:
                self.save_folder_info(main_window)
            elif response == Gtk.ResponseType.OK:
                self.save_folder_info(main_window)
                self.destroy()
                break
            elif response == Gtk.ResponseType.CANCEL:
                self.destroy()
                break
            
    def save_folder_info(self, main_window):
        # Server Name
        if main_window.selected_host["ObjectName"] != self.folder_name_entry.get_text():
            print("Voy a guardar FolderName")
            for_each_value = main_window.selected_host["ObjectName"]
            main_window.conn_tree.foreach(self.for_each_row, for_each_value)
            main_window.tree_structure[main_window.selected_host["ObjectID"]]["ObjectName"] = self.folder_name_entry.get_text()
    
    def for_each_row(self, tree_model, path, tree_iter, value):
        #print(tree_model.get_value(tree_iter, 1))
        if tree_model.get_value(tree_iter, 1) == value:
            print("Setting Value")
            tree_model.set_value(tree_iter, 1, self.folder_name_entry.get_text())
            
class FolderNewDialog(Gtk.Dialog):
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, "Folder Properties", main_window, (Gtk.DialogFlags.MODAL),
                (Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_size_request(300,100)
        
        folder_edit_box = self.get_content_area()
        
        folder_edit_box.set_orientation(Gtk.Orientation.VERTICAL)
        folder_edit_box.set_spacing(5)

        # Folder Name Entry
        folder_name_label = Gtk.Label("Folder Name")
        self.folder_name_entry = Gtk.Entry()
        folder_name_form = FormField(folder_name_label, self.folder_name_entry)
        folder_edit_box.pack_start(folder_name_form, True, True, 5)
        
        self.show_all()

        while True:
            response = self.run()                

            if response == Gtk.ResponseType.APPLY:
                self.save_new_folder_info(main_window)
            elif response == Gtk.ResponseType.OK:
                self.save_new_folder_info(main_window)
                self.destroy()
                break
            elif response == Gtk.ResponseType.CANCEL:
                self.destroy()
                break
            
    def save_new_folder_info(self, main_window):
        # Initialize Node Values
        object_id = str(random.randrange(20**15))
        folder_icon = GdkPixbuf.Pixbuf.new_from_file_at_size("images/Folder_Icon.png", 15, 15)
        
        # Append to Tree and Expand for visibility
        main_window.conn_tree.append(main_window.selected_iter, (folder_icon, 
                                                                 self.folder_name_entry.get_text(),
                                                                 object_id))
        main_window.tree_view.expand_row(main_window.conn_tree.get_path(main_window.selected_iter),
                                         False)
        
        # Append to Tree Structure Dict
        main_window.tree_structure[object_id] = { "ObjectType" : "RoyalFolder",
                                                  "ObjectName" : self.folder_name_entry.get_text(),
                                                  "ObjectID" : object_id,
                                                  "ParentID" : main_window.selected_host["ObjectID"] }
        