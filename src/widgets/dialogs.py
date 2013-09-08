'''
Created on Sep 7, 2013

@author: eduardo
'''
from gi.repository import Gtk

import random
import sys

sys.path.append(".")

from widgets.formfields import FormField


class NewFileDialog(Gtk.Dialog):
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, "New File", main_window,
                      Gtk.DialogFlags.DESTROY_WITH_PARENT,
                      [Gtk.STOCK_CANCEL , Gtk.ResponseType.CANCEL,
                       Gtk.STOCK_OK, Gtk.ResponseType.OK])
        
        # Create Main Box 
        vbox = self.get_content_area()
        
        # Create description Label
        desc_label = Gtk.Label("Please, select Name for New File: ")
        
        # Create Filename Entry
        filename_entry = Gtk.Entry()
        filename_form = FormField(desc_label, filename_entry)
        
        # Add all to box
        vbox.pack_start(filename_form, False, False, 0)
        
        self.show_all()
    
        while True:
            response = self.run()        
            if response == Gtk.ResponseType.OK:
                if filename_entry.get_text():
                    main_window.conn_tree.clear()
                    object_id = str(random.randrange(20**15))
                    main_window.tree_structure = { object_id : { "ObjectID" : object_id,
                                                                "ObjectType" : "RoyalDocument",
                                                                "ObjectName" : filename_entry.get_text() } }
                                  
                    print(main_window.tree_structure)                
                    main_window.conn_tree.create_storage_tree(main_window.tree_structure)
                    self.destroy()
                    break
                else:
                    message = Gtk.MessageDialog(self,
                                                Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                                Gtk.MessageType.ERROR,
                                                Gtk.ButtonsType.OK,
                                                "Please Enter a Winter File Name")
                    message.set_size_request(50, 100)
                    message.set_title("Error")
                    message.run()
    
                    message.destroy()