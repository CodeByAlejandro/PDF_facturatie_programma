from enum import Enum, auto


class ErrorLevel(Enum):
    WARNING = auto()
    ERROR = auto()


class DisplayableError(Exception):


    def __init__(
        self,
        error_level: ErrorLevel,
        raw_msg: str,
        detail_msg: str | None = None,
        cause: Exception | None = None
    ) -> None:
        self.error_level = error_level
        self.raw_msg = raw_msg
        self.detail_msg = detail_msg
        self.cause = cause


    def __str__(self) -> str:
        if self.error_level is ErrorLevel.WARNING:
            return "Waarschuwing: " + self.raw_msg
        elif self.error_level is ErrorLevel.ERROR:
            return "Fout: " + self.raw_msg
        else:
            return self.raw_msg
