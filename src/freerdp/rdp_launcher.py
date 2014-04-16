'''
Created on Apr 14, 2014

@author: eduardo
'''
from gi.repository import Gtk, Gdk, GObject

import subprocess, threading, time

from freerdp.rdp_thread import rdpThread 

class freerdp_plug():
    
    def __init__(self, main_window, desktop_socket_id):
        
        self.width = main_window.desktop_notebook.resolution.width
        self.height = main_window.desktop_notebook.resolution.height
        self.user = main_window.selected_host["CredentialUsername"]
        self.password = main_window.selected_host["Password"]
        self.id = desktop_socket_id
        self.host = main_window.selected_host["PhysicalAddress"]
        
    def launch(self, main_window):

        print(self.width, self.height, self.user, self.password, self.id, self.host)
        desktop_process = [
            "xfreerdp",
            "-g", str(self.width) + "x" + str(self.height),
            "-u", self.user,
            "-p", self.password,
            "-X", self.id,
            "-a", "24",
            "--ignore-certificate",
            "--plugin", "cliprdr",
            "--plugin", "rdpdr", "--data", "disk:HOME:/home/eduardo", "--",
            self.host]
        
        desktop_thread = rdpThread(main_window, desktop_process)
        desktop_thread.start()