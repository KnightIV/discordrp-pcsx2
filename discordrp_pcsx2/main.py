"""Discord Rich Presence support for PCSX2.

Usage:
    discordrp-pcsx2 [--path=<path>]

Options:
    --path=<path> Path to your PCSX2 directory, optional.

"""

__version__ = '0.1.1'

import getpass
import time

from docopt import docopt
from pypresence import Presence

from discordrp_pcsx2.project_root.utils import latest_game


presence = Presence('540759287379525632')
presence.connect()


def main():
    start = int(time.time())
    arguments = docopt(__doc__, version=f'discordrp_pcsx2 {__version__}')
    path = arguments.get('--path')
    if path is None:
        path = f'/home/{getpass.getuser()}/.config/PCSX2'
    while True:
        game = latest_game(path)
        presence.update(
            large_image=game.image,
            large_text=game.description,
            small_image='pcsx2',
            small_text='PCSX2 Emulator',
            details=game.description,
            start=start
        )
        time.sleep(15)
