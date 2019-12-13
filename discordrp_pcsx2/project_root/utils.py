import re
from os import SEEK_END, SEEK_SET
from typing import Optional


game_pattern = re.compile(r'cdrom0:\\+([A-Z_0-9.]+);')
meta_pattern = '''
Serial = {0}
Name   = (.*?)
'''


class Game:
    """Class representing a displayed game."""

    def __init__(self, path: str, line: Optional[str] = None):
        self.path = path
        self.image = 'pcsx2'
        self.description = 'Idle'
        if line is not None:
            if self.check_line(line):
                self.parse_line(line)

    def parse_line(self, line: str):
        """Get game data from a ROM log."""
        game_id = ''
        match = game_pattern.search(line)
        if match is not None:
            game_id = match.group(1).replace('_', '-').replace('.', '')
        try:
            file = open(f'{self.path}/bin/GameIndex.dbf')
        except FileNotFoundError:
            file = open(f'{self.path}/GameIndex.dbf')
        metadata = file.read()
        file.close()
        match = re.search(
            meta_pattern.format(game_id),
            metadata
        )
        if match is not None:
            name = match.group(1)
            self.description = name
            self.image = game_id.lower()

    @staticmethod
    def check_line(line: str) -> bool:
        """Check if a line contains a valid Game."""
        return (
            game_pattern.search(line) is not None
        )


def latest_game(path: str) -> Optional[Game]:
    "Find the latest loaded game from emuLog.txt."
    line = ''
    try:
        log_file = open(f'{path}/bin/logs/emuLog.txt')
    except FileNotFoundError:
        log_file = open(f'{path}/logs/emuLog.txt')

    for block in _reverse_read(log_file):
        for char in block:
            if char == '\n' and line:
                if Game.check_line(line):
                    return Game(line=line, path=path)
                line = ''
            line += char
    log_file.close()
    if Game.check_line(line):
        return Game(line=line, path=path)
    else:
        return Game(path=path)


def _reverse_read(file):
    """Read file in reverse order."""
    file.seek(0, SEEK_END)
    location = file.tell()
    while location > 0:
        delta = min(4096, location)
        location -= delta
        file.seek(location, SEEK_SET)
        yield file.read(delta)
