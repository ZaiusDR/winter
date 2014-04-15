'''
Created on Apr 14, 2014

@author: eduardo
'''
from gi.repository import Gtk, Gdk
import subprocess, threading

class freerdp_plug():
    
    def __init__(self, main_window, desktop_socket_id):
        
        self.width = main_window.desktop_notebook.resolution.width
        self.height = main_window.desktop_notebook.resolution.height
        self.user = main_window.selected_host["CredentialUsername"]
        self.password = main_window.selected_host["Password"]
        self.id = desktop_socket_id
        self.host = main_window.selected_host["PhysicalAddress"]
        self.
        
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

        thread1 = threading.Thread(target=self.run_subprocess, args=(desktop_process, main_window,))
        subproc_exit = thread1.start()
        
    def run_subprocess(self, desktop_process, main_window):
        p = subprocess.Popen(desktop_process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
                     
        print(main_window)
        
        for line in p.stdout.readlines():
            print("hay salida: ")
            print(line)
            
        message = Gtk.MessageDialog(main_window,
                                    Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                    Gtk.MessageType.ERROR,
                                    Gtk.ButtonsType.OK,
                                    "lalala")
        message.set_size_request(50, 100)
        message.set_title("Error")
        message.run()

        message.destroy()
