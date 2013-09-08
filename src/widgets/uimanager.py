'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk

# Set Python Path to Custom Modules
import sys
import collections
import xml.etree.ElementTree as ET
sys.path.append('/home/eduardo/workspace/Winter/lib/')
# Import Custom Modules
from widgets.filechoosers import OpenFileWtmChooser
from widgets.assistants import ImportAssistant

class MainUIManager(Gtk.UIManager):

    def __init__(self, main_window):
        Gtk.UIManager.__init__(self)

        #Create an Action Group
        self.action_group = Gtk.ActionGroup("my_actions")
        
        #Create an Action For File Menu
        self.action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        self.action_group.add_action(self.action_filemenu)
        
        #Create File Menu Actions
        self.action_open = Gtk.Action("FileOpen", "_Open", "Open Selected File", Gtk.STOCK_OPEN)
        self.action_open.connect("activate", self.on_activate_open, main_window)
        self.action_group.add_action_with_accel(self.action_open, "<Ctrl>o")

        self.action_passwords = Gtk.Action("FileImportPass", "_Import", "Import Passwords", Gtk.STOCK_INDENT)
        self.action_passwords.connect("activate", self.on_activate_import_passwords_show_assistant, main_window)
        self.action_group.add_action_with_accel(self.action_passwords, "<Ctrl>i")

        self.action_quit = Gtk.Action("FileQuit", "_Quit", "Quit Program", Gtk.STOCK_QUIT)
        self.action_quit.connect("activate", self.quit_program, main_window)
        self.action_group.add_action_with_accel(self.action_quit, None)
        
        #Create PopUp Menu
        self.host_popup_menu = Gtk.ActionGroup("HostPopupMenu")

        #Add Actions to Action Group
        self.host_popup_menu.add_actions(
            [("HostEdit", Gtk.STOCK_EDIT, "Edit...", None, None, main_window.open_host_edition),
            ("HostDel", Gtk.STOCK_DELETE, "Delete", None)])
        self.insert_action_group(self.host_popup_menu)

        # Throws exception if something went wrong
        self.add_ui_from_file("./ui_config/main_ui_config")

        # Add the accelerator group to the toplevel window
        accelgroup = self.get_accel_group()
        main_window.add_accel_group(accelgroup)
            
        self.insert_action_group(self.action_group)
        
    def quit_program(self, action, main_window):
        main_window.destroy()

    def on_activate_import_passwords_show_assistant(self, widget, main_window):
        ImportAssistant(main_window)
    
    def on_activate_open(self, widget, main_window):
        
        # Open File Open Chooser custom object
        dialog = OpenFileWtmChooser(main_window)
        
        response = dialog.run()
        
        if response == Gtk.ResponseType.ACCEPT:
            wtm_file = dialog.get_filename()
            self.parse_wtm(wtm_file, main_window)
            main_window.conn_tree.create_storage_tree(main_window.tree_structure)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()
        
    def parse_wtm(self, wtm_file, main_window):
        
        main_window.tree_structure = collections.OrderedDict()
        tree = ET.parse(wtm_file)
        tree.getroot()
        
        for elem in tree.iter():
            if elem.tag != "wtm_file":
                main_window.tree_structure.update({ elem.attrib["ObjectID"] : elem.attrib })
