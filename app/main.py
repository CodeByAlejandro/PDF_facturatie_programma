import sys
from pathlib import Path
from view import TkGraphicalInterface


if __name__ == "__main__":
    resource_path = Path(getattr(sys, "_MEIPASS", Path(__file__).parents[1]))
    ui = TkGraphicalInterface(resource_path)
    ui.start(resource_path)
