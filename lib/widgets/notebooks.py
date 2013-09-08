'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk
# Set Python Path to Custom Modules
import sys
sys.path.append('/home/eduardo/workspace/Winter/lib/')
# Import Custom Modules
from widgets.tablabels import TabLabelCloseButton


class DesktopNotebook(Gtk.Notebook):
    def __init__(self):
        Gtk.Notebook.__init__(self)
        self.set_scrollable(True)

        # Add Empty Initial Tab
        resolution_box = Gtk.Box()
        self.init_tab = self.append_page(resolution_box, tab_label=Gtk.Label("No connections"))
        self.show_all()

        # Connect Box to continuously get its size stored
        resolution_box.connect("size-allocate", self.__get_widget_size)

    def __get_widget_size(self, widget, size_allocation):
        self.widget_size = widget.get_allocation()
        print("Height: %i" % self.widget_size.height)
        print("Width: %i " % self.widget_size.width)

    def add_tab(self, label):
        if self.init_tab != None:
            print("Removing")
            self.remove_page(self.init_tab)
            self.init_tab = None

        # Desktop Box. Needed to get resolution (with size)
        desktop_box = Gtk.Box()

        # Add Variable to store size
        desktop_box.widget_size = desktop_box.get_allocation()

        # Create Socket and add it to the Box
        desktop_socket = Gtk.Socket()
        desktop_box.pack_start(desktop_socket, False, False, 0)
        tab_id = self.append_page(desktop_box, label)

        desktop_socket.connect("plug-removed", self.on_plug_removed)
        self.show_all()

        self.set_current_page(tab_id)

        # Connect Box to continuously get its size stored
        desktop_box.connect("size-allocate", self.__get_widget_size)

        return hex(desktop_socket.get_id())

    def get_box_size(self):
        return self.widget_size

    def on_plug_removed(self, socket):
        tab_id = self.get_current_page()
        self.remove_page(tab_id)