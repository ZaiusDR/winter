'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk

# Set Python Path to Custom Modules
#import sys
import os
import collections
import xml.etree.ElementTree as ET
from xml.dom import minidom

#sys.path.append('/home/eduardo/quickly/winter/lib/')
# Import Custom Modules
from widgets.filechoosers import OpenFileChooser, OpenFilePassChooser, SaveFileChooser


class ImportAssistant(Gtk.Assistant):
    def __init__(self, main_window):
        Gtk.Assistant.__init__(self)

        #Create Assistant Object with properties
        self.set_size_request(600, 400)
        self.set_resizable(False)
        self.set_title("Royal Import Assistant")
        self.set_property("window-position", Gtk.WindowPosition.CENTER)
        self.set_property("modal", True)
        self.connect("delete-event", self.delete_widget)
        self.connect("cancel", self.button_pressed, "Cancel")
        self.connect("close", self.delete_widget, self)
        """Simulates appply signal"""
        self.get_child().get_children()[1].get_children()[1].get_children()[4].connect(
            "clicked", self.on_continue_clicked)

        #Add Intro Page
        intro_vbox = Gtk.VBox()
        self.append_page(intro_vbox)

        self.set_page_title(intro_vbox, "Welcome")
        self.set_page_type(intro_vbox, Gtk.AssistantPageType.INTRO)
        label_intro = Gtk.Label("<b>Welcome to RoyalTS Data import!</b>\n\nHere you will find the needed steps to import your RoyalTS Connections Data Files stored on the application.")
        label_intro.set_use_markup(True)
        label_intro.set_line_wrap(True)
        intro_vbox.pack_start(label_intro, True, True, 0)

        self.set_page_complete(intro_vbox, True)

        #Add Rtsx file selection Page

        rtsx_vbox = Gtk.VBox()
        self.append_page(rtsx_vbox)

        self.set_page_title(rtsx_vbox, "Select RTSX")
        self.set_page_type(rtsx_vbox, Gtk.AssistantPageType.CONTENT)
        label_rtsx = Gtk.Label("\n\n<b>RoyalTS RTSX File Selection.</b>\n\n\nPlease select a RoyalTS File:\n")
        label_rtsx.set_alignment(0, .5)
        label_rtsx.set_use_markup(True)
        label_rtsx.set_line_wrap(True)

        rtsx_selection_box = Gtk.HBox()
        path_rtsx_entry = Gtk.Entry()
        path_rtsx_entry.set_size_request(200, -1)
        rtsx_selection_button = Gtk.Button("Browse...")
        rtsx_selection_button.connect("clicked", self.select_assistant_rtsx,
                                         main_window, path_rtsx_entry)
        rtsx_selection_box.pack_start(path_rtsx_entry, True, True, 0)
        rtsx_selection_box.pack_start(rtsx_selection_button, False, False, 0)
        rtsx_vbox.pack_start(label_rtsx, False, True, 0)
        rtsx_vbox.pack_start(rtsx_selection_box, False, True, 0)

        self.set_page_complete(rtsx_vbox, True)

        #Add CSV Passwords File selection Page

        csv_vbox = Gtk.VBox()
        self.append_page(csv_vbox)

        self.set_page_title(csv_vbox, "Select CSV")
        self.set_page_type(csv_vbox, Gtk.AssistantPageType.CONTENT)

        label_csv = Gtk.Label("\n\n<b>RoyalTS CSV File Selection.</b>\n\n\n"
                                "Please select a RoyalTS CSV Exported File:\n")
        label_csv.set_alignment(0, .5)
        label_csv.set_use_markup(True)
        label_csv.set_line_wrap(True)

        csv_selection_box = Gtk.HBox()
        path_csv_entry = Gtk.Entry()
        path_csv_entry.set_size_request(200, -1)
        csv_selection_button = Gtk.Button("Browse...")
        csv_selection_button.connect("clicked", self.select_assistant_csv, main_window, path_csv_entry)
        csv_selection_box.pack_start(path_csv_entry, True, True, 0)
        csv_selection_box.pack_start(csv_selection_button, False, False, 0)
        csv_vbox.pack_start(label_csv, False, True, 0)
        csv_vbox.pack_start(csv_selection_box, False, True, 0)

        self.set_page_complete(csv_vbox, True)

        # Add WTM File selection Page
        wtm_vbox = Gtk.VBox()
        self.append_page(wtm_vbox)

        self.set_page_title(wtm_vbox, "Select Winter File")
        self.set_page_type(wtm_vbox, Gtk.AssistantPageType.CONTENT)

        label_wtm = Gtk.Label("\n\n<b>Winter Manager File Selection.</b>\n\n\n"
                                "Please select a new Winter Manager File where"
                                "import new connections data:\n")
        label_wtm.set_alignment(0, .5)
        label_wtm.set_use_markup(True)
        label_wtm.set_line_wrap(True)

        wtm_selection_box = Gtk.HBox()
        path_wtm_entry = Gtk.Entry()
        path_wtm_entry.set_size_request(200, -1)
        wtm_selection_button = Gtk.Button("Browse...")
        wtm_selection_button.connect("clicked", self.select_assistant_wtm,
                                        main_window, path_wtm_entry)
        wtm_selection_box.pack_start(path_wtm_entry, True, True, 0)
        wtm_selection_box.pack_start(wtm_selection_button, False, False, 0)
        wtm_vbox.pack_start(label_wtm, False, True, 0)
        wtm_vbox.pack_start(wtm_selection_box, False, True, 0)

        self.set_page_complete(wtm_vbox, True)

        # Add Confirmation Page
        confirm_vbox = Gtk.VBox()
        self.append_page(confirm_vbox)

        self.set_page_title(confirm_vbox, "Confirmation")
        self.set_page_type(confirm_vbox, Gtk.AssistantPageType.CONFIRM)
        label_confirm = Gtk.Label("")
        label_confirm.set_alignment(0, .5)
        label_confirm.set_use_markup(True)
        label_confirm.set_line_wrap(True)
        confirm_vbox.pack_start(label_confirm, True, True, 0)

        self.set_page_complete(confirm_vbox, True)

        # Add Progress Page
        progress_vbox = Gtk.VBox()
        self.append_page(progress_vbox)

        self.set_page_title(progress_vbox, "Importing")
        self.set_page_type(confirm_vbox, Gtk.AssistantPageType.PROGRESS)

        label_progress = Gtk.Label("<b>Importing...</b>")
        label_progress.set_use_markup(True)
        label_progress.set_alignment(0, .5)
        progress_vbox.pack_start(label_progress, True, True, 0)
        self.label_progress2 = Gtk.Label("Importing Connections...")
        self.progress_bar = Gtk.ProgressBar()
        self.label_progress2.set_alignment(0, .5)
        progress_vbox.pack_start(self.label_progress2, True, True, 0)
        progress_vbox.pack_start(self.progress_bar, False, True, 0)

        # Add Summary Page

        summary_vbox = Gtk.VBox()
        self.append_page(summary_vbox)

        self.set_page_title(summary_vbox, "Finished")
        self.set_page_type(summary_vbox, Gtk.AssistantPageType.SUMMARY)

        label_summary = Gtk.Label("<b>Import Finished!\n\n</b>"
                                    "Files Imported Succesfully!")
        label_summary.set_use_markup(True)
        label_summary.set_alignment(0, .5)
        summary_vbox.pack_start(label_summary, True, True, 0)
        self.set_page_complete(summary_vbox, True)

        self.connect("prepare", self.validate_pages, path_rtsx_entry,
                        path_csv_entry, path_wtm_entry, label_confirm,
                        main_window)

        self.show_all()

    def validate_pages(self, next_page, box, path_rtsx_entry,
                        path_csv_entry, path_wtm_entry, label_confirm,
                        main_window):

        page = self.get_current_page()

        if page == 2:
            if not os.path.isfile(path_rtsx_entry.get_text()):
                message = Gtk.MessageDialog(self,
                                        Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                        Gtk.MessageType.ERROR,
                                        Gtk.ButtonsType.OK,
                                        "The Selected File has not been found.")
                message.set_size_request(50, 100)
                message.set_title("Error")
                message.connect("delete-event", self.delete_widget)
                message.run()

                message.destroy()
                self.set_current_page(1)
            else:
                self.rtsx_file = path_rtsx_entry.get_text()
                self.set_current_page(2)
        elif page == 3:
            if not os.path.isfile(path_csv_entry.get_text()):
                message = Gtk.MessageDialog(self,
                                        Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                        Gtk.MessageType.ERROR,
                                        Gtk.ButtonsType.OK,
                                        "The Selected File has not been found.")
                message.set_size_request(50, 100)
                message.set_title("Error")
                message.connect("delete-event", self.delete_widget)
                message.run()

                message.destroy()
                self.set_current_page(2)
            else:
                self.set_current_page(3)
        elif page == 4:
            if not path_wtm_entry.get_text():
                message = Gtk.MessageDialog(self,
                                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                            Gtk.MessageType.ERROR,
                                            Gtk.ButtonsType.OK,
                                            "Please Select a Winter File")
                message.set_size_request(50, 100)
                message.set_title("Error")
                message.connect("delete-event", self.delete_widget)
                message.run()

                message.destroy()
                self.set_current_page(3)
            else:
                if path_wtm_entry.get_text():
                    self.wtm_file = path_wtm_entry.get_text()
                if not ".wtm" in self.wtm_file:
                    self.wtm_file = self.wtm_file + ".wtm"
                    path_wtm_entry.set_text(self.wtm_file)
                if not "/" in self.wtm_file:
                    self.wtm_file = os.environ['HOME'] + "/" + self.wtm_file
                    path_wtm_entry.set_text(self.wtm_file)

                self.set_current_page(4)
                label_confirm.set_text("<b>This is the Confirmation Page!</b>\n\n\n"
                                        "You have selected the following Files:\n\n"
                                        "- RTSX File:\n<i>" + path_rtsx_entry.get_text() + "</i>"
                                        "\n\n- CSV File:\n<i>" + path_csv_entry.get_text() + "</i>"
                                        "\n\n- WTM File:\n<i>" + path_wtm_entry.get_text() + "</i>"
                                        "\n\nPlease, press continue to start importing data.")
                label_confirm.set_use_markup(True)
                label_confirm.set_line_wrap(True)
                label_confirm.set_alignment(0, .5)
        elif page == 6:
            self.parse_rtsx_file(main_window)
            self.parse_csv_file(main_window)
            self.save_to_wtm(main_window)
            open_file_dialog = Gtk.MessageDialog(self,
                                        Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                        Gtk.MessageType.QUESTION,
                                        Gtk.ButtonsType.YES_NO,
                                        "Import Finished. Do you want to open it now?")
            response = open_file_dialog.run()
            
            if response == Gtk.ResponseType.YES:
                main_window.uimanager.parse_wtm(self.wtm_file, main_window)
                main_window.conn_tree.create_storage_tree(main_window.tree_structure)
            
            open_file_dialog.destroy()
            
    def parse_rtsx_file(self, main_window):

        main_window.tree_structure = collections.OrderedDict()
        object_id = ''
        get_next_item = False

        tree = ET.parse(self.rtsx_file)
        tree.getroot()

        keys_list = ["ObjectID", "RoyalObjectType", "Name", "PositionNr",
                    "ParentID", "URI", "CredentialUsername"]

        for elem in tree.iter():

            # Break at royal BinTrash
            if elem.tag == "Value" and elem.text == "RoyalTrash":
                break

            #Parse Object ID
            if elem.tag == "ObjectID":
                if object_id != elem.text:
                    object_id = elem.text

            if elem.tag == "Key" and elem.text in keys_list:
                get_next_item = True
                next_item = elem.text

            elif get_next_item:

                # Parsing Object Type
                if next_item == "RoyalObjectType":
                    object_type = elem.text
                    get_next_item = False
                # Parse Object Name
                elif next_item == "Name":
                    object_name = elem.text
                    main_window.tree_structure.update({ object_id : { "ObjectID" : object_id,
                                                    "ObjectType" : object_type,
                                                    "ObjectName" : object_name }})
                    get_next_item = False
                # Parse Object Parent ID
                elif next_item == "ParentID":
                    object_parent = elem.text
                    get_next_item = False
                    main_window.tree_structure[object_id].update({ "ParentID" : object_parent })
                # Parse Object IP
                elif next_item == "URI":
                    if object_type is not "RoyalFolder":
                        object_ip = elem.text
                        get_next_item = False
                        main_window.tree_structure[object_id].update({ "PhysicalAddress" : object_ip })
                    else:
                        get_next_item = False
                # Parse Object Username
                elif next_item == "CredentialUsername":
                    if object_type == "RoyalFolder":
                        get_next_item = False
                    else:
                        object_username = elem.text
                        get_next_item = False
                        main_window.tree_structure[object_id].update({ "CredentialUsername" : object_username })

    def parse_csv_file(self, main_window):
        
        self.label_progress2.set_text("Importing Passwords...")
        self.progress_bar.set_fraction(0.33)
        while Gtk.events_pending():
            Gtk.main_iteration_do(self.progress_bar)
        

        f = open(self.csv_file)
        passwords = {}

        for line in f.readlines():
            passwords.update({ line.split(",")[0].split('"')[1] : line.split(",")[36].split('"')[1] } )

        for k in main_window.tree_structure:
            if main_window.tree_structure[k]["ObjectType"] == "RoyalRDSConnection":
                if main_window.tree_structure[k]["ObjectName"] in passwords:
                    main_window.tree_structure[k].update({ "Password" : passwords[main_window.tree_structure[k]["ObjectName"]] })

        f.close()

    def save_to_wtm(self, main_window):

        self.label_progress2.set_text("Saving Data...")
        self.progress_bar.set_fraction(0.66)
        while Gtk.events_pending():
            Gtk.main_iteration_do(self.progress_bar)
            
        # Get XML Tree Root Element
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
        
        f = open(self.wtm_file, "w+")
        f.write(pretty)
        f.close()
        
        self.progress_bar.set_fraction(1)
        while Gtk.events_pending():
            Gtk.main_iteration_do(self.progress_bar)
        

    def select_assistant_rtsx(self, widget, main_window, path_text_box):

        # Open File Open Chooser custom object
        dialog = OpenFileChooser(main_window)

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            self.rtsx_file = dialog.get_filename()
            path_text_box.set_text(self.rtsx_file)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()

    def select_assistant_csv(self, widget, main_window, path_text_box):

        # Open File Open Chooser custom object
        dialog = OpenFilePassChooser(main_window)

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            self.csv_file = dialog.get_filename()
            path_text_box.set_text(self.csv_file)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()

    def select_assistant_wtm(self, widget, main_window, path_text_box):

        # Open File Open Chooser custom object
        dialog = SaveFileChooser(self)
        dialog.set_current_folder(os.environ['HOME'])

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            self.wtm_file = dialog.get_filename()
            if not ".wtm" in self.wtm_file:
                self.wtm_file = self.wtm_file + ".wtm"
            if not "/" in self.wtm_file:
                self.wtm_file = os.environ['HOME'] + self.wtm_file
            path_text_box.set_text(self.wtm_file)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()

    def button_pressed(self, import_assist, button):
        if button == "Cancel":
            import_assist.destroy()

    def delete_widget(self, widget, event):
        widget.destroy()

    def on_continue_clicked(self, button):
        page = self.get_current_page()
        #print("apply emited")
        if page == 5:
            self.commit()
            self.set_current_page(5)
            while Gtk.events_pending():
                Gtk.main_iteration_do(self)
            self.set_current_page(6)