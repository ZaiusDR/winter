'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk

# Set Python Path to Custom Modules
import collections
import xml.etree.ElementTree as ET

# Import Custom Modules
from widgets.filechoosers import OpenFileWtmChooser
from widgets.assistants import ImportAssistant
from widgets.dialogs import NewFileDialog


class MainUIManager(Gtk.UIManager):

    def __init__(self, main_window):
        Gtk.UIManager.__init__(self)

        # Create an Action Group
        main_action_group = Gtk.ActionGroup("my_actions")
        
        # Create an Action For File Menu
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        main_action_group.add_action(action_filemenu)
        
        # Create File Menu Actions:
        
        # New
        action_new = Gtk.Action("FileNew", "_New", "Creates a New File", Gtk.STOCK_NEW)
        action_new.connect("activate", self.on_activate_new, main_window)
        main_action_group.add_action_with_accel(action_new, "<Ctrl>n")
        
        # Open
        action_open = Gtk.Action("FileOpen", "_Open", "Open Selected File", Gtk.STOCK_OPEN)
        action_open.connect("activate", self.on_activate_open, main_window)
        main_action_group.add_action_with_accel(action_open, "<Ctrl>o")

        # Import
        action_import = Gtk.Action("FileImport", "_Import", "Import Passwords", Gtk.STOCK_INDENT)
        action_import.connect("activate", self.on_activate_import_passwords_show_assistant, main_window)
        main_action_group.add_action_with_accel(action_import, "<Ctrl>i")

        # Quit
        action_quit = Gtk.Action("FileQuit", "_Quit", "Quit Program", Gtk.STOCK_QUIT)
        action_quit.connect("activate", self.quit_program, main_window)
        main_action_group.add_action_with_accel(action_quit, "<Ctrl>q")
        
        # Create PopUp Menu
        tree_popup_menu = Gtk.ActionGroup("HostPopupMenu")

        # Add Actions to PopUp
        # New Menu
        action_popup_new = Gtk.Action("PopupNew", "New", None, None)
        tree_popup_menu.add_action(action_popup_new)
        
        # New RDP Connection
        action_popup_new_conn = Gtk.Action("PopupNewConn", "New RDP Connection",
                                                 "Creates a New RDP Connection", None)
        action_popup_new_conn.connect("activate",
                                           main_window.tree_view.on_activate_popup_new_conn,
                                           main_window)
        tree_popup_menu.add_action(action_popup_new_conn)
        
        # Edit
        action_popup_edit = Gtk.Action("HostEdit", "Edit", None, None)
        action_popup_edit.connect("activate", main_window.tree_view.open_host_edition, main_window)
        tree_popup_menu.add_action(action_popup_edit)
        
        action_popup_delete = Gtk.Action("HostDel", "Delete", None, None)
        action_popup_delete.connect("activate", self.on_delete_element) # To be created
        tree_popup_menu.add_action(action_popup_delete)

        # Throws exception if something went wrong
        self.add_ui_from_file("./ui_config/main_ui_config")

        # Add the accelerator group to the toplevel window
        accelgroup = self.get_accel_group()
        main_window.add_accel_group(accelgroup)
        
        # Add Action Groups    
        self.insert_action_group(main_action_group)
        self.insert_action_group(tree_popup_menu)
        
    def on_delete_element(self, action):
        pass
        
    def quit_program(self, action, main_window):
        main_window.destroy()

    def on_activate_import_passwords_show_assistant(self, widget, main_window):
        ImportAssistant(main_window)
        
    def on_activate_new(self, widget, main_window):
        NewFileDialog(main_window)
        
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
                main_window.tree_structure[elem.attrib["ObjectID"]] = elem.attrib

