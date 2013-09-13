'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk

import os
import collections
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Import Custom Modules
from widgets.filechoosers import OpenFileWtmChooser, SaveFileChooser
from widgets.assistants import ImportAssistant
from widgets.dialogs import NewFileDialog, WinterAboutDialog


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
        
        # Save
        action_save = Gtk.Action("FileSave", "_Save", "Save Selected Opened File", Gtk.STOCK_SAVE)
        action_save.connect("activate", self.on_activate_save, main_window)
        main_action_group.add_action_with_accel(action_save, "<Ctrl>s")
        
        # Save As
        action_save_as = Gtk.Action("FileSaveAs", "Save as...", "Save to File", Gtk.STOCK_SAVE_AS)
        action_save_as.connect("activate", self.on_activate_save_as, main_window)
        main_action_group.add_action_with_accel(action_save_as, "<Ctrl><Shift>s")

        # Import
        action_import = Gtk.Action("FileImport", "_Import", "Import Passwords", Gtk.STOCK_INDENT)
        action_import.connect("activate", self.on_activate_import_passwords_show_assistant, main_window)
        main_action_group.add_action_with_accel(action_import, "<Ctrl>i")

        # Quit
        action_quit = Gtk.Action("FileQuit", "_Quit", "Quit Program", Gtk.STOCK_QUIT)
        action_quit.connect("activate", self.quit_program, main_window)
        main_action_group.add_action_with_accel(action_quit, "<Ctrl>q")
        
        # Options Menu
        action_optsmenu = Gtk.Action("OptsMenu", "Options", None, None)
        main_action_group.add_action(action_optsmenu)
        
        # Host Defaults
        action_opts_default = Gtk.Action("OptsDefaults", "Host Defaults", None, None)
        action_opts_default.connect("activate", self.on_activate_opts_default, main_window)
        main_action_group.add_action(action_opts_default)
        
        # Help Menu
        action_helpmenu = Gtk.Action("HelpMenu", "Help", None, None)
        main_action_group.add_action(action_helpmenu)
        
        # About
        action_about = Gtk.Action("HelpAbout", "About...", None, Gtk.STOCK_ABOUT)
        action_about.connect("activate", self.on_activate_about)
        main_action_group.add_action(action_about)
        
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
        
        # New Folder
        action_popup_new_folder = Gtk.Action("PopupNewFolder", "New Folder", None, None)
        action_popup_new_folder.connect("activate",
                                        main_window.tree_view.on_activate_popup_new_folder,
                                        main_window)
        tree_popup_menu.add_action(action_popup_new_folder)
        
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
            main_window.open_file = wtm_file
            self.parse_wtm(wtm_file, main_window)
            main_window.conn_tree.create_storage_tree(main_window.tree_structure)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()
        
        main_window.tree_view.expand_row(Gtk.TreePath("0"), False)    

    def on_activate_save(self, action, main_window):
        if main_window.open_file:
            self.save_to_wtm(main_window)
    
    def on_activate_save_as(self, action, main_window):
        if main_window.open_file:
            save_chooser = SaveFileChooser(main_window)
            save_chooser.set_current_folder(os.environ['HOME'])
        
            response = save_chooser.run()
        
            if response == Gtk.ResponseType.ACCEPT:
                save_file = save_chooser.get_filename()
                if not ".wtm" in save_file:
                    save_file = save_file + ".wtm"
                if not "/" in save_file:
                    save_file = os.environ['HOME'] + save_file
                main_window.open_file = save_file
                self.save_to_wtm(main_window)
                    
            save_chooser.destroy()
            
    def on_activate_opts_default(self, action, main_window):
        pass
            
    def on_activate_about(self, action):
        WinterAboutDialog() 
    
    def save_to_wtm(self, main_window):
        print("Saving to %s" % main_window.open_file)
        root = ET.Element("wtm_file")
        for k in main_window.tree_structure:
            if main_window.tree_structure[k]["ObjectType"] == "RoyalDocument":
                element = ET.SubElement(root, "winter_object")
                for attr in main_window.tree_structure[k]:
                    element.set(attr, main_window.tree_structure[k][attr])
                        
            else:
                if root.find(".//winter_object[@ObjectID='" + main_window.tree_structure[k]["ParentID"] + "']") is not None:
                    parent = root.find(".//winter_object[@ObjectID='" + main_window.tree_structure[k]["ParentID"] + "']")
                    element = ET.SubElement(parent, "winter_object")
                    for attr in main_window.tree_structure[k]:
                        if not main_window.tree_structure[k][attr]:
                            main_window.tree_structure[k][attr] = ""
                        element.set(attr, main_window.tree_structure[k][attr])
                        
        result = ET.tostring(root)
        result = result.decode("us-ascii")
        parsed = minidom.parseString(result)
        pretty = parsed.toprettyxml(indent="  ")
        
        f = open(main_window.open_file, "w+")
        f.write(pretty)
        f.close()
    
    def parse_wtm(self, wtm_file, main_window):
        
        main_window.tree_structure = collections.OrderedDict()
        tree = ET.parse(wtm_file)
        tree.getroot()
        
        for elem in tree.iter():
            if elem.tag != "wtm_file":
                main_window.tree_structure[elem.attrib["ObjectID"]] = elem.attrib

