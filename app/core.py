from pathlib import Path
from typing import Union, Literal
from PyPDF2 import PdfWriter, PdfReader, Transformation, PageObject
from exceptions import ErrorLevel, DisplayableError


class PDFProcessor():


    def stamp_pdf_pages(
        self,
        content_pdf: Path,
        stamp_pdf: Path,
        result_pdf: Path,
        page_indices: Union[Literal["ALL"], list[int]] = "ALL",
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

            # Create deep copy of original stamp PDF page
            stamp_page_copy = PageObject.create_blank_page(
                width=stamp_page.mediabox.width,
                height=stamp_page.mediabox.height
            )
            stamp_page_copy.merge_page(stamp_page)

            # Scale copy of stamp PDF page's contents to size of content PDF page
            op = Transformation().scale(sx=x_axis_ratio, sy=y_axis_ratio)
            stamp_page_copy.add_transformation(op)

            # Merge scaled copy of stamp PDF page into content PDF page
            # = write scaled copy of stamp PDF after content PDF page
            # (meaning overwrite)
            content_page.merge_page(stamp_page_copy)

            # Add stamped PDF page to PdfWriter-object
            writer.add_page(content_page)

        # Write the fully stamped content PDF as result PDF file
        try:
            with open(result_pdf, "wb") as fp:
                writer.write(fp)
        except Exception as ex:
            raise DisplayableError(
                error_level=ErrorLevel.ERROR,
                raw_msg="Kan gestempelde PDF niet opslaan!",
                cause=ex
            )
