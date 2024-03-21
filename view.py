from pathlib import Path
import tkinter as tk
from exceptions import DisplayableError
# from PIL import Image


class GraphicalInterface():


    # Set global UI padding configuration
    HOR_PD = 20
    VERT_PD = 10


    def __init__(self, resource_path: Path) -> None:
        self.resource_path = resource_path

        # Create main window
        self.root = tk.Tk()
        self.root.title("PDF Facturatieprogramma")

        # Create frame to hold main grid UI elements
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Create stamp PDF selector row
        self._create_stamp_PDF_row()

        # Create result directory selector row
        self._create_result_directory_row()

        # Create label and entry for suffix input
        self._create_suffix_input_row()

        # Create file listbox
        self._create_file_listbox()

        # Create frame with subgrid with file buttons
        self._create_file_buttons()

        # Create status label
        self.status_label = tk.Label(self.main_frame, text="")
        self.status_label.grid(
            row=4,
            columnspan=2,
            pady=GraphicalInterface.VERT_PD
        )

        # Create warning/error message label
        self.error_label = tk.Label(self.main_frame, text="")

        # Create warning/error detail message label
        self.error_detail_label = tk.Label(self.main_frame, text="")

        # Create author label
        self.author_label = tk.Label(
            self.main_frame,
            text="Auteur: Alejandro De Groote"
        )
        self.author_label.grid(row=8, column=0, sticky=tk.W)


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
            try:
                self.controller.select_stamp_pdf(self.stamp_label)
            except DisplayableError as disp_ex:
                self._handle_displayable_error(disp_ex)
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


    def _create_file_buttons(self) -> None:
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
        self._create_info_file_btn()

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


    def _create_info_file_btn(self) -> None:
        # Set image path
        resized_image_path = \
            self.resource_path / Path("images/info_logo_resized.png")

        # Open and resize info image using PIL (for devel stage of project)
        # image_path = self.resource_path / Path("images/info_logo.png")
        # image = Image.open(image_path)
        # image.thumbnail((25, 25))
        # image.save(resized_image_path)

        # Convert the resized image to a format compatible with Tkinter
        self.info_logo_image = tk.PhotoImage(file=resized_image_path)

        # Create event listener
        def handle_click_show_info_select_files():
            self.controller.show_info_select_files
        # Create info file button
        self.select_info_button = tk.Button(
            self.buttons_frame,
            image=self.info_logo_image,
            command=handle_click_show_info_select_files
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


    def _handle_displayable_error(self, disp_ex: DisplayableError) -> None:
            self.error_label.config(text=str(disp_ex))
            self.error_label.grid(
                row=5,
                columnspan=2,
                pady=GraphicalInterface.VERT_PD
            )
            if disp_ex.detail_msg is not None:
                self.error_detail_label.config(text=disp_ex.detail_msg)
                self.error_detail_label.grid(
                    row=6,
                    columnspan=2,
                    pady=GraphicalInterface.VERT_PD
                )


    def start(self) -> None:
        # Create InterfaceController object to implement event listeners
        from controller import InterfaceController
        self.controller = InterfaceController(self)
        # Start GUI
        self.root.mainloop()
