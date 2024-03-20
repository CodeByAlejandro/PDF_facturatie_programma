from os import getcwd
import sys
from pathlib import Path
from typing import Union, Literal, List
from PyPDF2 import PdfWriter, PdfReader, Transformation
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


class GraphicalInterface():


    # Set global UI padding configuration
    HOR_PD = 20
    VERT_PD = 10


    def __init__(self, resource_path: Path) -> None:
        # Create main window
        self.root = tk.Tk()
        self.root.title("PDF Facturatieprogramma")

        # Create frame to hold main grid UI elements
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Create InterfaceController object to implement event listeners
        self.controller = InterfaceController()
        
        # Create stamp PDF selector row
        self._create_stamp_PDF_row()

        # Create result directory selector row
        self._create_result_directory_row()

        # Create label and entry for suffix input
        self._create_suffix_input_row()

        # Create file listbox
        self._create_file_listbox()

        # Create frame with subgrid with file buttons
        self._create_file_buttons(resource_path)

        # Create status label
        self.status_label = tk.Label(self.main_frame, text="")
        self.status_label.grid(
            row=4,
            columnspan=2,
            pady=GraphicalInterface.VERT_PD
        )

        # Create author label
        self.author_label = tk.Label(
            self.main_frame,
            text="Auteur: Alejandro De Groote"
        )
        self.author_label.grid(row=6, column=0, sticky=tk.W)


    def _create_stamp_PDF_row(self) -> None:
        # Create stamp PDF selector label
        self.stamp_label = tk.Label(
            self.main_frame,
            text="Selecteer stempel PDF om bovenop andere PDF's te plaatsen:"
        )
        # Put label in main grid
        self.stamp_label.grid(
            row=0,
            column=0,
            sticky=tk.W,
            padx=(0, GraphicalInterface.HOR_PD),
            pady=GraphicalInterface.VERT_PD
        )
        # Create event listener
        def handle_click_stamp_pdf():
            self.controller.select_stamp_pdf(self.stamp_label)
        # Create stamp PDF selector button
        self.select_stamp_button = tk.Button(
            self.main_frame,
            text="Selecteer PDF met enkele stempelpagina",
            command=handle_click_stamp_pdf
        )
        # Put button in main grid
        self.select_stamp_button.grid(
            row=0,
            column=1,
            sticky=tk.W,
            pady=GraphicalInterface.VERT_PD
        )


    def _create_result_directory_row(self) -> None:
        # Create result directory selector label
        self.result_directory_label = tk.Label(
            self.main_frame,
            text="Selecteer map om PDF's op te slaan:"
        )
        # Put label in main grid
        self.result_directory_label.grid(
            row=1,
            column=0,
            sticky=tk.W,
            padx=(0, GraphicalInterface.HOR_PD),
            pady=(0, GraphicalInterface.VERT_PD)
        )
        # Create event listener
        def handle_click_result_directory():
            self.controller.select_result_directory(
                self.result_directory_label
            )
        # Create result directory selector button
        self.select_result_directory_button = tk.Button(
            self.main_frame,
            text="Selecteer resultaat map",
            command=handle_click_result_directory
        )
        # Put button in main grid
        self.select_result_directory_button.grid(
            row=1,
            column=1,
            sticky=tk.W+tk.E,
            pady=(0, GraphicalInterface.VERT_PD)
        )


    def _create_suffix_input_row(self) -> None:
        # Create label for suffix input
        self.suffix_label = tk.Label(
            self.main_frame,
            text="Voer de suffix voor de resulterende PDF's in:"
        )
        # Put label in main grid
        self.suffix_label.grid(
            row=2,
            column=0,
            sticky=tk.W,
            padx=(0, GraphicalInterface.HOR_PD),
            pady=(0, GraphicalInterface.VERT_PD)
        )
        # Set a default value for the filename suffix field
        default_suffix = "_aangepast"
        # Create entry for suffix input
        self.suffix_entry = tk.Entry(self.main_frame, width=30)
        self.suffix_entry.insert(0, default_suffix) # Pre-populate the entry with the default value
        self.suffix_entry.grid(
            row=2,
            column=1,
            sticky=tk.W+tk.E,
            pady=(0, GraphicalInterface.VERT_PD)
        )


    def _create_file_listbox(self) -> None:
        # Create file listbox
        self.file_listbox = tk.Listbox(
            self.main_frame,
            selectmode=tk.MULTIPLE,
            width=50,
            height=10
        )
        # Put file listbox in main grid
        self.file_listbox.grid(
            row=3,
            column=0,
            sticky=tk.W,
            padx=(0, GraphicalInterface.HOR_PD),
            pady=GraphicalInterface.VERT_PD
        )


    def _create_file_buttons(self, resource_path: Path) -> None:
        # Create frame to hold subgrid with file buttons
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid(
            row=3,
            column=1,
            sticky=tk.W+tk.E,
            pady=GraphicalInterface.VERT_PD
        )

        # Create PDF selection file button
        self._create_PDF_selection_file_btn()

        # Create info file button
        self._create_info_file_btn(resource_path)

        # Create clear files button
        self._create_clear_files_btn()

        # Create process files button
        self._create_process_files_btn()


    def _create_PDF_selection_file_btn(self) -> None:
        # Create event listener
        def handle_click_select_files():
            self.controller.select_files(self.file_listbox)
        # Create PDF selection button
        self.select_button = tk.Button(
            self.buttons_frame,
            text="Selecteer bestanden",
            command=handle_click_select_files
        )
        # Put button in button subgrid
        self.select_button.grid(
            row=0,
            column=0,
            sticky=tk.W+tk.E+tk.N+tk.S,
            pady=(0, GraphicalInterface.VERT_PD)
        )


    def _create_info_file_btn(self, resource_path: Path) -> None:
        # Set image path
        resized_image_path = resource_path / Path("images/info_logo_resized.png")

        # Open and resize info image using PIL (for devel stage of project)
        image_path = resource_path / Path("images/info_logo.png")
        image = Image.open(image_path)
        image.thumbnail((25, 25))
        image.save(resized_image_path)

        # Convert the resized image to a format compatible with Tkinter
        info_logo_image = tk.PhotoImage(file=resized_image_path)

        # Create info file button
        self.select_info_button = tk.Button(
            self.buttons_frame,
            image=info_logo_image,
            command=self.controller.show_info_select_files
        )
        # Put button in button subgrid
        self.select_info_button.grid(
            row=0,
            column=1,
            sticky=tk.W+tk.E+tk.N+tk.S,
            pady=(0, GraphicalInterface.VERT_PD)
        )


    def _create_clear_files_btn(self) -> None:
        # Create event listener
        def handle_click_clear_files():
            self.controller.clear_files(self.file_listbox)
        # Create clear files button
        self.clear_button = tk.Button(
            self.buttons_frame,
            text="Wis bestandenlijst",
            command=handle_click_clear_files
        )
        # Put button in button subgrid
        self.clear_button.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E)


    def _create_process_files_btn(self) -> None:
        # Create event listener
        def handle_click_process_files():
            self.controller.process_files(
                self.file_listbox,
                self.suffix_entry,
                self.status_label
            )
        # Create process files button
        self.process_button = tk.Button(
            self.buttons_frame,
            text="Verwerk bestanden",
            command=handle_click_process_files
        )
        # Put button in button subgrid
        self.process_button.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky=tk.W+tk.E,
            pady=(GraphicalInterface.VERT_PD, 0)
        )


    def start(self) -> None:
        self.root.mainloop()


class InterfaceController():


    def __init__(self) -> None:
        self.stamp_pdf: Path | None = None
        self.result_directory: Path | None = None
        self.PDFProcessor = PDFProcessor()


    def select_stamp_pdf(self, stamp_label: tk.Label) -> None:
        stamp_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if stamp_pdf_path is not None:
            stamp_label.config(text=stamp_pdf_path)
            self.stamp_pdf = Path(stamp_pdf_path)
        else:
            stamp_label.config(text="Geen stempel PDF geselecteerd!")


    def select_result_directory(self, result_directory_label: tk.Label) -> None:
        result_directory_path = filedialog.askdirectory()
        if result_directory_path is not None:
            result_directory_label.config(text=result_directory_path)
            self.result_directory = Path(result_directory_path)
        else:
            result_directory_label.config(text="Geen map geselecteerd!")


    def select_files(self, file_listbox: tk.Listbox) -> None:
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file_path in file_paths:
            file_listbox.insert(tk.END, file_path)


    def show_info_select_files(self) -> None:
        messagebox.showinfo(
            "Tip: Meervoudige selectie",
            "U kunt meerdere PDF's selecteren door de CTRL-toets " + \
            "ingedrukt te houden tijdens het selecteren (op sommige " + \
            "grafische omgevingen kan dit de SHIFT-toets zijn)"
        )


    def clear_files(self, file_listbox: tk.Listbox) -> None:
        file_listbox.delete(0, tk.END)


    def process_files(
            self,
            file_listbox: tk.Listbox,
            suffix_entry: tk.Entry,
            status_label: tk.Label
    ) -> None:
        # Check if stamp PDF is selected
        if self.stamp_pdf is None:
            messagebox.showwarning(
                "Geen stempel PDF geselecteerd",
                "Selecteer alstublieft een PDF met enkele stempelpagina om door te gaan."
            )
            return

        # Check if result directory is selected
        if self.result_directory is None:
            messagebox.showwarning(
                "Geen map geselecteerd",
                "Selecteer alstublieft een map om de resulterende PDF's op te slaan."
            )
            return

        # Get PDF files to stamp
        files_to_process = file_listbox.get(0, tk.END)

        # Check if no PDF files to stamp have been selected
        total_files = len(files_to_process)
        if total_files == 0:
            messagebox.showwarning(
                "Geen bestanden geselecteerd",
                "Selecteer alstublieft PDF-bestanden om te verwerken."
            )
            return

        # Get the suffix entered by the user
        filename_suffix = suffix_entry.get()

        # Show status message while processing
        status_label.config(text="Bezig met verwerken...")

        # Stamp all selected PDFs
        for index, file_path in enumerate(files_to_process, start=1):
            content_pdf = Path(file_path)
            result_pdf_file = Path(content_pdf.stem + f"{filename_suffix}.pdf")
            result_pdf = self.result_directory / result_pdf_file
            self.PDFProcessor.stamp_pdf_pages(
                content_pdf,
                self.stamp_pdf,
                result_pdf,
                'ALL'
            )

            # Update status message
            status_label.config(
                text=f"Bezig met verwerken van {index}/{total_files} bestanden..."
            )

        # Update status message
        status_label.config(text="Verwerking voltooid!")


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


if __name__ == "__main__":
    resource_path = Path(getattr(sys, "_MEIPASS", getcwd()))
    gui = GraphicalInterface(resource_path)
    gui.start()
