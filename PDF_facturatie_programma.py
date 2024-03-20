import sys
from os import getcwd
from pathlib import Path
from view import GraphicalInterface


if __name__ == "__main__":
    resource_path = Path(getattr(sys, "_MEIPASS", getcwd()))
    gui = GraphicalInterface(resource_path)
    gui.start()
