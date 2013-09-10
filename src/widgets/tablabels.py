'''
Created on Sep 6, 2013

@author: eduardo
'''
from gi.repository import Gtk, GObject

class TabLabelCloseButton(Gtk.Box):
    __gsignals__ = {
        "close-clicked": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ())
    }
    def __init__(self, label_text, stock_icon):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_spacing(5) # spacing: [icon|5px|label|5px|close]  
        
        # icon
        icon = Gtk.Image.new_from_stock(stock_icon, Gtk.IconSize.MENU)
        self.pack_start(icon, False, False, 0)
        
        # label 
        label = Gtk.Label(label_text)
        self.pack_start(label, True, True, 0)
        
        # close button
        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.set_focus_on_click(False)
        button.add(Gtk.Image.new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU))
        button.connect("clicked", self.button_clicked)
        data =  b".button {\n" \
                b"-GtkButton-default-border : 0px;\n" \
                b"-GtkButton-default-outside-border : 0px;\n" \
                b"-GtkButton-inner-border: 0px;\n" \
                b"-GtkWidget-focus-line-width : 0px;\n" \
                b"-GtkWidget-focus-padding : 0px;\n" \
                b"padding: 0px;\n" \
                b"}"
        provider = Gtk.CssProvider()
        provider.load_from_data(data)
        # 600 = GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
        button.get_style_context().add_provider(provider, 600) 
        self.pack_start(button, False, False, 0)
        
        self.show_all()
    
    def button_clicked(self, button, data=None):
        self.emit("close-clicked")


class EditHostTabLabel(Gtk.Box):
    def __init__(self, label_text, stock_icon):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_spacing(5) # spacing: [icon|5px|label|5px|close]  
        
        # icon
        icon = Gtk.Image.new_from_stock(stock_icon, Gtk.IconSize.MENU)
        self.pack_start(icon, False, False, 0)
        
        # label 
        label = Gtk.Label(label_text)
        self.pack_start(label, True, True, 0)
        
        self.show_all()
