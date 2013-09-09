#!/usr/bin/python3

from gi.repository import Gtk, Unity, Dbusmenu
import sys

sys.path.append('./src')
sys.path.append('.')

from widgets.mainwindow import MainWindow

def unity_integration():
    launcher = Unity.LauncherEntry.get_for_desktop_id("winter.desktop")
    launcher.set_property("urgent", True)
    ql = Dbusmenu.Menuitem.new()
    item = Dbusmenu.Menuitem.new()
    item.property_set(Dbusmenu.MENUITEM_PROP_LABEL, "Item 1")
    item.property_set_bool(Dbusmenu.MENUITEM_PROP_VISIBLE, True)
    ql.child_append(item)
    launcher.set_property("quicklist", ql)


unity_integration()
winter = MainWindow()
winter.connect("delete-event", Gtk.main_quit)
winter.show_all()
Gtk.main()