'''
Created on Sep 7, 2013

@author: eduardo
'''
from gi.repository import Gtk

class MainUIManager(Gtk.Dialog):

    def __init__(self, file, parent):
        Gtk.UIManager.__init__(self, parent,
                               Gtk.DialogFlags.DESTROY_WITH_PARENT,
                               Gtk.MessageType.WARNING,
                               Gtk.ButtonsType.OK_CANCEL,
                               "File % Exists. Do you want to overwrite it?" % file)
        