from pathlib import Path
from typing import Protocol, Iterable, Literal
from exceptions import DisplayableError


class UserInterface(Protocol):

    def bind_controller(self, resource_path: Path) -> None: ...

    def start(self, resource_path: Path) -> None: ...

    def update_stamp_pdf(self, text: str) -> None: ...

    def update_result_directory(self, text: str) -> None: ...

    def update_filename_suffix(self, text: str) -> None: ...

    def get_filename_suffix(self) -> str: ...

    def update_files_to_process(self, file_path: str) -> None: ...

    def clear_files_to_process(self) -> None: ...

    def update_status_label(self, text: str) -> None: ...

    def show_info(self, info_title: str, info_text: str) -> None: ...

    def show_warning(self, warning_title: str, warning_text: str) -> None: ...

    def select_file(
        self,
        filetypes: Iterable[tuple[str, str | list[str] | tuple[str, ...]]] | None = ...
    ) -> str: ...

    def select_files(
        self,
        filetypes: Iterable[tuple[str, str | list[str] | tuple[str, ...]]] | None = ...
    ) -> (tuple[str, ...] | Literal['']): ...

    def select_directory(self) -> str: ...

    def handle_error(self, disp_ex: DisplayableError) -> None: ...
