'''
Created on Apr 14, 2014

@author: eduardo
'''
from gi.repository import Gtk, Gdk, GObject
import subprocess, threading, time

class rdpThread(threading.Thread):
    def __init__(self, main_window, desktop_process):
        threading.Thread.__init__(self, name="Thread1")
        self.desktop_process = desktop_process
        self.main_window = main_window
        self.quit = False
        print("All init on rdp Thread")
         
    def show_error(self, process_output):
        if process_output:
            print("He recibido algo")
            message=Gtk.MessageDialog(self.main_window,
                                    Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                    Gtk.MessageType.ERROR,
                                    Gtk.ButtonsType.OK,
                                    process_output)
            message.set_size_request(50, 100)
            message.set_title("Error")
            message.run()
            
            message.destroy()
     
    def run(self):
        print("start process")
        p = subprocess.Popen(self.desktop_process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("start Waiting")
        p.wait()
        print("Process Died")
        #self.show_error(p.stdout.readlines())
        GObject.idle_add(self.show_error, p.stdout.readlines())
        time.sleep(0.1)