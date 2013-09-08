'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk

class FormField(Gtk.Box):
    def __init__(self, label, widget):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_spacing(10)

        # Attach Label
        label.set_size_request(100, 29)
        label.set_alignment(0, .5)
        self.pack_start(label,False, False, 0)

        # Attach Widget
        self.pack_start(widget, True, True, 0)

        self.show_all()