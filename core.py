from pathlib import Path
from typing import Union, Literal, List
from PyPDF2 import PdfWriter, PdfReader, Transformation
import json


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
            raise KeyError("Defaults: JSON property should be str type!")
        valid_value_types = (str, int, float, bool, list, tuple, dict, None)
        if type(value) not in valid_value_types:
            raise ValueError(
                "Defaults: JSON value should be a valid JSON type!"
            )
        self.root[name] = value


    def get_property(
        self,
        name: str
    ) -> str | int | float | bool | list | tuple | dict | None:
        value = None
        try:
            value = self.root[name]
        except KeyError:
            pass
        return value


    def store_defaults(self) -> None:
        try:
            with open(self.filepath, "wt") as json_file:
                json.dump(self.root, json_file, indent=4)
        except Exception:
            pass
            # print error to GUI


    def load_defaults(self) -> None:
        try:
            with open(self.filepath, "rt") as json_file:
                self.root = json.load(json_file)
        except Exception:
            pass
            # print error to GUI


class PDFProcessor():


    def stamp_pdf_pages(
        self,
        content_pdf: Path,
        stamp_pdf: Path,
        pdf_result: Path,
        page_indices: Union[Literal["ALL"], List[int]] = "ALL",
    ) -> None:
        # Get single stamp PDF page
        reader = PdfReader(stamp_pdf)
        stamp_page = reader.pages[0]

        # Create PDF writer to write fully stampted PDFs
        # (= all pages have been stamped)
        writer = PdfWriter()

        # Create PDF reader to read the selected content PDF pages
        reader = PdfReader(content_pdf)

        # Get indices of selected content PDF pages
        if page_indices == "ALL":
            page_indices = list(range(0, len(reader.pages)))

        # Loop all content PDF pages at selected indices
        for index in page_indices:
            # Get content PDF page at current index
            content_page = reader.pages[index]

            # Get content PDF page size
            # (4 coordinates mediabox with bottom left at 0,0)
            content_mb = content_page.mediabox

            # Get stamp PDF page size
            # (4 coordinates mediabox with bottom left at 0,0)
            stamp_mb = stamp_page.mediabox

            # Calculate x axis ratio between content PDF page and stamp PDF page
            content_x = content_mb.right
            stamp_x = stamp_mb.right
            x_axis_ratio = float(content_x / stamp_x)

            # Calculate y axis ratio between content PDF page and stamp PDF page
            content_y = content_mb.top
            stamp_y = stamp_mb.top
            y_axis_ratio = float(content_y / stamp_y)

            # Scale stamp PDF page contents to size of content PDF page
            op = Transformation().scale(sx=x_axis_ratio, sy=y_axis_ratio)
            stamp_page.add_transformation(op)

            # Merge stamp PDF page into content PDF page
            # = write stamp PDF after content PDF page (meaning overwrite)
            content_page.merge_page(stamp_page)

            # Add stamped PDF page to PdfWriter-object
            writer.add_page(content_page)

        # Write the fully stamped content PDF as result PDF file
        with open(pdf_result, "wb") as fp:
            writer.write(fp)
