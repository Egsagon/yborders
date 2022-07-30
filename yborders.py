import gi
import draw
import cairo
import winfo
import threading
from os import system
from time import sleep

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from gi.repository import Gtk, Gdk

######## Settings #########

DRAWING_CLOCK = 0.4
REFRESH_CLOCK = 0.2

WIDTH, HEIGHT = 1920, 1080
BORDER_RADIUS = 10
BORDER_WIDTH = 3
BORDER_COLOR = [166, 211, 160, 1]

###########################

class Border(Gtk.Window):
    def __init__(self, winId) -> None:
        super().__init__(type=Gtk.WindowType.POPUP)
        
        self.winId = winId

        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        self.set_visual(visual)
        
        try: self.set_wmclass("xborders", "xborder")
        except: pass
        self.show_all()

        self.resize(WIDTH, HEIGHT)
        self.move(0, 0)

        self.fullscreen()
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.NOTIFICATION)

        self.set_accept_focus(False)
        self.set_focus_on_map(False)

        self.drawingarea = Gtk.DrawingArea()
        self.drawingarea.set_events(Gdk.EventMask.EXPOSURE_MASK)
        self.add(self.drawingarea)
        self.input_shape_combine_region(cairo.Region())

        self.connect('draw', self.draw)
        # self.connect('queue-draw', self.draw)
        
        def _loop(*_) -> None:
            # print(f'Started draw loop for window {self.winId}')
            
            while 1:
                sleep(DRAWING_CLOCK)
                self.queue_draw()
        
        threading.Thread(target = _loop).start()
    
    def draw(self, _wid, ctx) -> None:
        
        # print('drawing...')
        
        # Get window data
        win_data = winfo.get_win(self.winId)
        
        if win_data is None:
            # Remove
            self.move(1e6, 1e6)
            self.destroy()
            BORDERS.remove(self)
            del self
        
        # Check if window if visible
        desk = winfo.get_desk()
        
        # print(f"Drawing window from desk {win_data['wk']} ({desk})")
        
        if desk != win_data['wk']:
            # print('Window is from another wk.')
            # self.hide()
            self.move(1e6, 1e6)
            return
        
        self.show_all()
        self.move(0, 0)
        # self.show()
        
        x, y, w, h = win_data['geom'][0][0], win_data['geom'][0][1], \
            win_data['geom'][1][0], win_data['geom'][1][1],
            
        x, y, w, h = map(int, (x, y, w, h))
        
        # Correct
        CC = 4
        
        x -= CC
        y -= CC
        
        w += CC // 2
        h += CC // 2
        
        # Send to draw
        draw.draw_rectangle(ctx,
                            x, y, w, h,
                            BORDER_RADIUS, BORDER_WIDTH, [0, 0, 0, 0],
                            BORDER_COLOR)


# --- Main --- #

BORDERS = []

def main():
    # system('clear')
    # Get ids
    ids = [w['id'] for w in winfo.get_wins()]
    
    # print(f'RELOADED ({len(ids)} ids).')
    
    ids_done = []
    
    for obj in BORDERS:
        obj: Border
        
        # Check if id already in borders
        if obj.winId in ids:
            # print(f'Window {obj.winId} still running')
            ids_done.append(obj.winId)
            continue
        
        # Else, destroy border
        print(f'[{obj.winId}] Closed window')
        
        # Attempts at deleting it
        
        # obj.hide()
        obj.move(1e6, 1e6)
        obj.destroy()
        BORDERS.remove(obj)
        del obj
    
    # Create missing borders
    new = list(set(ids) - set(ids_done))
    
    for _id in new:
        print(f'[{_id}] Opened window')
        b = Border(_id)
        b.set_keep_above(True)
        b.set_title("xborders")
        b.show_all()
        BORDERS.append(b)
    
    # print(f'FINISHED reloading ({len(BORDERS)})')

def loop():
    sleep(1)
    system('clear')
    try:
        while 1:
            main()
            sleep(REFRESH_CLOCK)
    
    except KeyboardInterrupt: pass

if __name__ == '__main__':
    threading.Thread(target = Gtk.main).start()
    loop()

# TODO - feature - change color when window unfocused