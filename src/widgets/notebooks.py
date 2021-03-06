'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk

# Import Custom Modules
from widgets.tablabels import TabLabelCloseButton
from freerdp.rdp_launcher import freerdp_plug

class DesktopNotebook(Gtk.Notebook):
    def __init__(self, main_window):
        Gtk.Notebook.__init__(self)
        
        self.set_scrollable(True)

        # Initialize Tabs inventory
        self.open_tabs = []
        
        # Add Empty Initial Tab
        self.resolution_box = Gtk.Box()
        self.init_tab = self.append_page(self.resolution_box, tab_label=Gtk.Label("No connections"))
        self.show_all()

        # Connect Box to continuously get its size stored
        self.resolution_box.connect("size-allocate", self.__get_widget_size)

    def __get_widget_size(self, widget, size_allocation):
        self.widget_size = widget.get_allocation()
        #print("Height: %i" % self.widget_size.height)
        #print("Width: %i " % self.widget_size.width)

    def add_tab(self, tree_view, path, column, main_window):
        """Adds a new tab to Notbook Widget and Tab Inventory"""
        
        # Close Default Initial Tab
        if self.init_tab != None:
            #print("Removing")
            self.remove_page(self.init_tab)
            self.init_tab = None

        # Desktop Box. Needed to get resolution (with size)
        desktop_box = Gtk.Box()

        # Add a Box Attribute Variable where to store Box size
        desktop_box.widget_size = desktop_box.get_allocation()

        # Create Tab Label And connect Close Button Signal
        tab_label = TabLabelCloseButton(main_window.selected_host["ObjectName"], Gtk.STOCK_NETWORK)
        tab_label.connect("close-clicked", self.on_tab_close_clicked, main_window)
        
        # Create Socket and add it to the Box
        self.desktop_socket = Gtk.Socket()
        desktop_box.pack_start(self.desktop_socket, False, False, 0)
        
        # Get Box Resolution
        self.resolution = self.get_box_size()
        print(self.resolution.width, self.resolution.height) 
        
        # Add the page
        tab_id = self.append_page(desktop_box, tab_label)        
        self.show_all()
        self.set_current_page(tab_id)
        
        # Add Tab data to Tabs Inventory
        self.open_tabs.append({ "child" : desktop_box, "label" : tab_label})
        # Connect Box to continuously get its size stored
        desktop_box.connect("size-allocate", self.__get_widget_size)
        #print(self.resolution.width, self.resolution.height)
        
        # Get Socket ID
        desktop_socket_id = hex(self.desktop_socket.get_id())
        
        # Create Desktop
        desktop = freerdp_plug(main_window, desktop_socket_id)
        
        # Launch Desktop
        desktop.launch(main_window)
        
        # If RDP Session is Disconnected
        self.desktop_socket.connect("plug-removed", self.on_plug_removed)
        
    def get_box_size(self):
        return self.widget_size

    def on_plug_removed(self, socket):
        self.remove_page(self.get_current_page())
        
    def on_tab_close_clicked(self, widget, main_window):
        """Search for tab in inventory and close it"""
        confirm_message = Gtk.MessageDialog(main_window,
                                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                            Gtk.MessageType.WARNING,
                                            Gtk.ButtonsType.OK_CANCEL,
                                            "Do you really want to disconnect?")
        confirm_message.set_title("Disconnecting")
        
        response = confirm_message.run()
        
        if response == Gtk.ResponseType.OK:
            for tab in self.open_tabs:
                if tab["label"] == widget:
                    self.remove_page(self.open_tabs.index(tab))
                    break
            self.open_tabs.pop(self.open_tabs.index(tab))
        confirm_message.destroy()