from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from view import GraphicalInterface
from model import Defaults
from core import PDFProcessor
from exceptions import DisplayableError


class InterfaceController():


    def __init__(self, gui: GraphicalInterface) -> None:
        self.stamp_pdf: Path | None = None
        self.result_directory: Path | None = None
        self.gui = gui
        self.defaults = Defaults(self.gui.resource_path)
        try:
            self.defaults.load_defaults()
        except DisplayableError as disp_ex:
            self.gui._handle_displayable_error(disp_ex)
        self.PDFProcessor = PDFProcessor()


    def select_stamp_pdf(self, stamp_label: tk.Label) -> None:
        stamp_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if stamp_pdf_path:
            stamp_label.config(text=stamp_pdf_path)
            self.stamp_pdf = Path(stamp_pdf_path)
            self.defaults.add_property(
                "stamp_pdf_path",
                stamp_pdf_path
            )
        else:
            default = self.defaults.get_property("stamp_pdf_path")
            if isinstance(default, str):
                stamp_label.config(text=default)
            else:
                stamp_label.config(text="Geen stempel PDF geselecteerd!")


    def select_result_directory(self, result_directory_label: tk.Label) -> None:
        result_directory_path = filedialog.askdirectory()
        if result_directory_path:
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
            try:
                self.PDFProcessor.stamp_pdf_pages(
                    content_pdf,
                    self.stamp_pdf,
                    result_pdf,
                    'ALL'
                )
            except DisplayableError as disp_ex:
                disp_ex.raw_msg = \
                    "Kan één of meerdere gestempelde PDF's niet opslaan!"
                self.gui._handle_displayable_error(disp_ex)

            # Update status message
            status_label.config(
                text=f"Bezig met verwerken van {index}/{total_files} bestanden..."
            )

        # Update status message
        status_label.config(text="Verwerking voltooid!")

        # Store new defaults
        try:
            self.defaults.store_defaults()
        except DisplayableError as disp_ex:
            self.gui._handle_displayable_error(disp_ex)
