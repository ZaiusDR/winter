'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk

# Set Python Path to Custom Modules
import sys
sys.path.append('/home/eduardo/workspace/Winter/lib/')

# Import Custom Modules
from widgets.formfields import FormField
from widgets.tablabels import EditHostTabLabel

class HostEditLayoutObject(Gtk.Box):
    def __init__(self, host_info):
        Gtk.Box.__init__(self) # Missing param host data
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(5)

        print(host_info)
        # Host Name Entry
        host_name_label = Gtk.Label("Host Name")
        host_name_entry = Gtk.Entry()
        if host_info["ObjectName"]:
            host_name_entry.set_text(host_info["ObjectName"])
        host_name_form = FormField(host_name_label, host_name_entry)
        self.pack_start(host_name_form, True, True, 5)

        # Notebook and Config Tabs
        edit_notebook = Gtk.Notebook()

        #############################################################################
        # Basic Tab Layout
        basic_box = Gtk.Box()
        basic_box.set_orientation(Gtk.Orientation.VERTICAL)
        basic_box.set_spacing(5)
        basic_box.set_homogeneous(True)

        # IP Field
        server_label = Gtk.Label("Server")
        server_entry = Gtk.Entry()
        if host_info["PhysicalAddress"]:
            server_entry.set_text(host_info["PhysicalAddress"])
        server_form = FormField(server_label, server_entry)

        # Username Field
        username_label = Gtk.Label("User Name")
        username_entry = Gtk.Entry()
        if host_info["CredentialUsername"]:
            username_entry.set_text(host_info["CredentialUsername"])
        username_form = FormField(username_label, username_entry)

        # Password Field
        password_label = Gtk.Label("Password")
        password_entry = Gtk.Entry()
        if host_info["Password"]:
            password_entry.set_text(host_info["Password"])
        password_entry.set_visibility(False)
        password_form = FormField(password_label, password_entry)

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
        self.pack_start(edit_notebook, True, True, 10)
        
class FolderEditLayoutObject(Gtk.Box):
    def __init__(self, host_info):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_spacing(5)

        # Folder Name Entry
        folder_name_label = Gtk.Label("Folder Name")
        folder_name_entry = Gtk.Entry()
        if host_info["ObjectName"]:
            folder_name_entry.set_text(host_info["ObjectName"])
        folder_name_form = FormField(folder_name_label, folder_name_entry)
        self.pack_start(folder_name_form, True, True, 5)
