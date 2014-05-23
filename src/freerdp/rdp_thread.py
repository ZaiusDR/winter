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
        print(desktop_process)
         
    def show_error(self, process_output):
        if process_output:
            print(process_output)
            for line in process_output:
                line = str(line, encoding='utf8')
                if "Failed to check xfreerdp file descriptor" in line:
                    error_message = "You have been disconected from %s" % self.desktop_process[len(self.desktop_process) - 1]
                elif "0x00000005" in line:
                    error_message = "Another user connected to the server, forcing the disconnection of the current connection."
                elif "unable to connect" in line:
                    error_message = line
                elif "Authentication failure" in line:
                    error_message = line

            message=Gtk.MessageDialog(self.main_window,
                                    Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                    Gtk.MessageType.ERROR,
                                    Gtk.ButtonsType.OK,
                                    error_message)
            message.set_size_request(50, 100)
            message.set_title("Error")
            message.run()
            
            message.destroy()
            return False
     
    def run(self):
        p = subprocess.Popen(self.desktop_process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        # I really don't know how it works but it works :D
        GObject.idle_add(self.show_error, p.stdout.readlines())
        time.sleep(0.1)