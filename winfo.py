import json
from os import popen
from time import time
# threading

"""
WIN_CACHE = []

def getRoot() -> dict:
    '''Get the i3 tree.'''
    
    return json.load(popen('i3-msg -t get_tree'))

def getEnd(parent: dict) -> list:
    nodes = parent['nodes']
    
    # End of branch
    if not len(nodes): WIN_CACHE.append(parent)
    
    # Reapeat for all parents inside the object
    else:
        for node in nodes: getEnd(node)

def getWindows() -> list:
    '''Get infos on all windows.'''
    
    # Get windows
    tree = getRoot()
    getEnd(tree)
    
    windows = filter(lambda el: el['type'] == 'con', WIN_CACHE)
    
    return windows

def getIds() -> list:
    '''Get the id of all windows.'''
    
    return [w['id'] for w in getWindows()]

def getInfo(winId: str) -> tuple:
    '''Get dims of a window knowing its id.'''
    
    windows = getWindows()
    
    for win in windows:
        if win['id'] == winId: return win['rect']
"""

def get_wins() -> list:
    '''Get a list of windows from wmctrl.'''

    res = [w.split() for w in popen('wmctrl -lG').readlines()]
    
    windows = [{'id': int(win[0], 16),
                'wk': int(win[1]),
                'geom': ((win[2], win[3]), (win[4], win[5]))}
               for win in res]
    
    # return json.dumps(windows, indent=4)
    return windows

def get_desk() -> int:
    '''Get the current desktop.'''
    
    return int(popen('xdotool get_desktop').read())

def get_win(_id: str) -> dict:
    '''Get win info from an id.'''
    
    for win in get_wins():
        if win['id'] == _id: return win


"""
def isVisible(winId: str) -> bool:
    '''Returns wheter a window is visible or not.'''

    wd = popen(f'xdotool get_desktop_for_window {winId}').read()
    
    print(wd)

    return popen('xdotool get_desktop').read() == wd

def crono_fn(fn) -> tuple:
    start = time()
    res = fn()
    return (time() - start, res)
"""