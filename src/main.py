import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio
from .window import SigloWindow
from .bluetooth import InfiniTimeManager
from bleson import get_provider

def get_adapter_name():
    adapter = get_provider().get_adapter(0)
    id = adapter.device_id
    return "hci" + str(id)

class Application(Gtk.Application):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(application_id='org.gnome.siglo',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = SigloWindow(application=self)
        win.present()
        self.manager.scan_for_infinitime()
        win.done_scanning(self.manager)

    def do_window_removed(self, window):
        self.manager.stop()

def main(version):
    manager = InfiniTimeManager(adapter_name=get_adapter_name())
    app = Application(manager)
    return app.run(sys.argv)

