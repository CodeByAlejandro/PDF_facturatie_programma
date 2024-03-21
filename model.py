from pathlib import Path
import json
from exceptions import ErrorLevel, DisplayableError


class Defaults():


    def __init__(self, resource_path: Path) -> None:
        self.root = {}
        self.filepath = resource_path / "defaults.json"


    def add_property(
        self,
        name: str,
        value: str | int | float | bool | list | tuple | dict | None
    ) -> None:
        if not isinstance(name, str):
            raise DisplayableError(
                error_level=ErrorLevel.WARNING,
                raw_msg="Kan nieuwe standaardinstelling niet toevoegen!",
                detail_msg=f"Type '{type(name)}' is niet compatibel met " + \
                            "JSON key 'str' type!",
            )
        valid_value_types = (str, int, float, bool, list, tuple, dict, None)
        if type(value) not in valid_value_types:
            raise DisplayableError(
                error_level=ErrorLevel.WARNING,
                raw_msg="Kan nieuwe standaardinstelling niet toevoegen!",
                detail_msg=f"Type '{type(name)}' is niet compatibel met " + \
                            "JSON value types!",
            )
        self.root[name] = value


    def get_property(
        self,
        name: str
    ) -> str | int | float | bool | list | tuple | dict | None:
        value = None
        try:
            value = self.root[name]
        except KeyError as ex:
            raise DisplayableError(
                error_level=ErrorLevel.WARNING,
                raw_msg="Kan bestaande standaardinstelling niet ophalen!",
                detail_msg=f"JSON key '{name}' is onbestaand!",
                cause=ex
            )
        return value


    def store_defaults(self) -> None:
        try:
            with open(self.filepath, "wt") as json_file:
                json.dump(self.root, json_file, indent=4)
        except Exception as ex:
            raise DisplayableError(
                error_level=ErrorLevel.WARNING,
                raw_msg="Kan nieuwe standaardinstellingen niet opslaan!",
                cause=ex
            )


    def load_defaults(self) -> None:
        try:
            with open(self.filepath, "rt") as json_file:
                self.root = json.load(json_file)
        except Exception as ex:
            raise DisplayableError(
                error_level=ErrorLevel.WARNING,
                raw_msg="Kan bestaande standaardinstellingen niet ophalen!",
                cause=ex
            )
