from pathlib import Path
from threading import Thread
from protocols import ApplicationInterface
from model import Defaults
from core import PDFProcessor
from exceptions import DisplayableError


class InterfaceController():


    def __init__(self, ui: ApplicationInterface, resource_path: Path) -> None:
        self.stamp_pdf: Path | None = None
        self.result_directory: Path | None = None
        self.ui = ui
        self.defaults = Defaults(resource_path)
        try:
            self.defaults.load_defaults()
        except DisplayableError as disp_ex:
            self.ui.handle_error(disp_ex)
        else:
            stamp_pdf_path = self.defaults.get_property("stamp_pdf_path")
            if isinstance(stamp_pdf_path, str) and stamp_pdf_path != "":
                self.ui.update_stamp_pdf(text=stamp_pdf_path)
                self.stamp_pdf = Path(stamp_pdf_path)
            result_directory_path = \
                self.defaults.get_property("result_directory_path")
            if isinstance(result_directory_path, str) \
            and result_directory_path != "":
                self.ui.update_result_directory(text=result_directory_path)
                self.result_directory = Path(result_directory_path)
            filename_suffix = self.defaults.get_property("filename_suffix")
            if isinstance(filename_suffix, str) and filename_suffix != "":
                self.ui.update_filename_suffix(text=filename_suffix)
        self.PDFProcessor = PDFProcessor()


    def select_stamp_pdf(self) -> None:
        stamp_pdf_path = self.ui.select_file(filetypes=[("PDF files", "*.pdf")])
        if stamp_pdf_path:
            self.ui.update_stamp_pdf(text=stamp_pdf_path)
            self.stamp_pdf = Path(stamp_pdf_path)
            self.defaults.add_property(
                "stamp_pdf_path",
                stamp_pdf_path
            )
        else:
            default = self.defaults.get_property("stamp_pdf_path")
            if isinstance(default, str):
                self.ui.update_stamp_pdf(text=default)
            else:
                self.ui.update_stamp_pdf(text="Geen stempel PDF geselecteerd!")


    def select_result_directory(self) -> None:
        result_directory_path = self.ui.select_directory()
        if result_directory_path:
            self.ui.update_result_directory(text=result_directory_path)
            self.result_directory = Path(result_directory_path)
            self.defaults.add_property(
                "result_directory_path",
                result_directory_path
            )
        else:
            default = self.defaults.get_property("result_directory_path")
            if isinstance(default, str):
                self.ui.update_result_directory(text=default)
            else:
                self.ui.update_result_directory(text="Geen map geselecteerd!")


    def select_files(self) -> None:
        file_paths = self.ui.select_files(filetypes=[("PDF files", "*.pdf")])
        for file_path in file_paths:
            self.ui.update_files_to_process(file_path)


    def show_info_select_files(self) -> None:
        self.ui.show_info(
            "Tip: Meervoudige selectie",
            "U kunt meerdere PDF's selecteren door de CTRL-toets " + \
            "ingedrukt te houden tijdens het selecteren. Houd de " + \
            "SHIFT-toets ingedrukt om een van-tot bereik te selecteren " + \
            "met 2 linkermuiskliks."
        )


    def clear_files(self) -> None:
        self.ui.clear_files_to_process()


    def process_files(self) -> None:
        # Check if stamp PDF is selected
        if self.stamp_pdf is None:
            self.ui.show_warning(
                "Geen stempel PDF geselecteerd",
                "Selecteer alstublieft een PDF met enkele stempelpagina om door te gaan."
            )
            return

        # Check if result directory is selected
        if self.result_directory is None:
            self.ui.show_warning(
                "Geen map geselecteerd",
                "Selecteer alstublieft een map om de resulterende PDF's op te slaan."
            )
            return

        # Get PDF files to stamp
        files_to_process = self.ui.get_files_to_process()

        # Check if no PDF files to stamp have been selected
        total_files = len(files_to_process)
        if total_files == 0:
            self.ui.show_warning(
                "Geen bestanden geselecteerd",
                "Selecteer alstublieft PDF-bestanden om te verwerken."
            )
            return

        # Get the suffix entered by the user
        filename_suffix = self.ui.get_filename_suffix()
        # Set the retrieved suffix as the new default value
        self.defaults.add_property("filename_suffix", filename_suffix)

        # Start new thread to process PDF files
        def thread_function(self):
            self._process_files_core(
                files_to_process,
                filename_suffix
            )
        processing_thread = Thread(
            target=thread_function,
            args=(self,)
        )
        processing_thread.start()


    def _process_files_core(
        self,
        files_to_process: list[str],
        filename_suffix: str
    ) -> None:
        # Show status message while processing
        self.ui.update_status_label(text="Bezig met verwerken...")

        # Set number of PDF files to process
        total_files = len(files_to_process)

        # Satisfy static analysis tools in IDE
        if self.result_directory is not None and self.stamp_pdf is not None:
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
                    self.ui.handle_error(disp_ex)

                # Update status message
                self.ui.update_status_label(
                    text=f"Bezig met verwerken van {index}/{total_files} bestanden..."
                )

        # Update status message
        self.ui.update_status_label(text="Verwerking voltooid!")

        # Store new defaults
        try:
            self.defaults.store_defaults()
        except DisplayableError as disp_ex:
            self.ui.handle_error(disp_ex)
