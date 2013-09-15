from gi.repository import Gtk


class OpenFileWtmChooser(Gtk.FileChooserDialog):
    def __init__(self, parent):
        Gtk.FileChooserDialog.__init__(self, "Please choose a file", parent, 
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

    # Add Filters

        filter_rts = Gtk.FileFilter()
        filter_rts.set_name("Winter Files")
        filter_rts.add_mime_type("xml/wtmfile")
        filter_rts.add_pattern("*.wtm")
        self.add_filter(filter_rts)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        self.add_filter(filter_any)

        self.show_all()

      
class OpenFileChooser(Gtk.FileChooserDialog):
    def __init__(self, parent):
        Gtk.FileChooserDialog.__init__(self, "Please choose a file", parent, 
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

    # Add Filters

        filter_rts = Gtk.FileFilter()
        filter_rts.set_name("RoyalTS Files")
        filter_rts.add_mime_type("text/rtsfile")
        filter_rts.add_pattern("*.rtsx")
        self.add_filter(filter_rts)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        self.add_filter(filter_any)

        self.show_all()

class OpenFilePassChooser(Gtk.FileChooserDialog):
    def __init__(self, parent):
        Gtk.FileChooserDialog.__init__(self, "Please choose a Passwords File", parent, 
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

    # Add Filters

        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV File")
        filter_csv.add_mime_type("text/csv")
        self.add_filter(filter_csv)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        self.add_filter(filter_any)

        self.show_all()


class SaveFileChooser(Gtk.FileChooserDialog):
    def __init__(self, parent):
        Gtk.FileChooserDialog.__init__(self, "Please choose a file", parent, 
                                        Gtk.FileChooserAction.SAVE,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        self.set_do_overwrite_confirmation(True)

    # Add Filters

        filter_wtm = Gtk.FileFilter()
        filter_wtm.set_name("Winter Manager Files")
        filter_wtm.add_mime_type("text/wtmfile")
        filter_wtm.add_pattern("*.wtm")
        self.add_filter(filter_wtm)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        self.add_filter(filter_any)

        self.show_all()