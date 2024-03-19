from pathlib import Path
from typing import Union, Literal, List
from PyPDF2 import PdfWriter, PdfReader, Transformation
import tkinter as tk
from tkinter import filedialog, messagebox
# from PIL import Image


def stamp_pdf_pages(
    content_pdf: Path,
    stamp_pdf: Path,
    pdf_result: Path,
    page_indices: Union[Literal["ALL"], List[int]] = "ALL",
):
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


def select_stamp_pdf():
    stamp_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if stamp_pdf_path:
        stamp_label.config(text=stamp_pdf_path)
        global stamp_pdf
        stamp_pdf = Path(stamp_pdf_path)
    else:
        stamp_label.config(text="Geen stempel PDF geselecteerd!")


def select_result_directory():
    result_directory_path = filedialog.askdirectory()
    if result_directory_path:
        result_directory_label.config(text=result_directory_path)
        global result_directory
        result_directory = Path(result_directory_path)
    else:
        result_directory_label.config(text="Geen directory geselecteerd!")


def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    for file_path in file_paths:
        file_listbox.insert(tk.END, file_path)


def show_help_select_files():
    messagebox.showinfo(
        "Tip: Meervoudige selectie",
        "U kunt meerdere PDF's selecteren door de SHIFT-toets " + \
        "ingedrukt te houden tijdens het selecteren"
    )


def clear_files():
    file_listbox.delete(0, tk.END)


def process_files():
    # Check if stamp PDF is selected
    if stamp_pdf is None:
        messagebox.showwarning(
            "Geen stempel PDF geselecteerd",
            "Selecteer alstublieft een PDF met enkele stempelpagina om door te gaan."
        )
        return

    # Check if result directory is selected
    if result_directory is None:
        messagebox.showwarning(
            "Geen directory geselecteerd",
            "Selecteer alstublieft een directory om de resulterende PDF's op te slaan."
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
        result_pdf = result_directory / result_pdf_file
        stamp_pdf_pages(content_pdf, stamp_pdf, result_pdf, 'ALL')

        # Update status message
        status_label.config(
            text=f"Bezig met verwerken van {index}/{total_files} bestanden..."
        )

    # Update status message
    status_label.config(text="Verwerking voltooid!")


if __name__ == "__main__":
    # Set gobal variables
    stamp_pdf = None
    result_directory = None

    # Set global UI padding configuration
    HOR_PD = 20
    VERT_PD = 10

    # Create main window
    root = tk.Tk()
    root.title("PDF Facturatieprogramma")

    # Create frame to hold main grid UI elements
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    # Create stamp PDF selector
    stamp_label = tk.Label(
        main_frame,
        text="Selecteer stempel PDF om bovenop andere PDF's te plaatsen:"
    )
    stamp_label.grid(
        row=0, column=0, sticky=tk.W, padx=(0, HOR_PD), pady=VERT_PD
    )
    select_stamp_button = tk.Button(
        main_frame,
        text="Selecteer PDF met enkele stempelpagina",
        command=select_stamp_pdf
    )
    select_stamp_button.grid(row=0, column=1, sticky=tk.W, pady=VERT_PD)

    # Create result directory selector
    result_directory_label = tk.Label(
        main_frame,
        text="Selecteer directory om PDF's op te slaan:"
    )
    result_directory_label.grid(
        row=1, column=0, sticky=tk.W, padx=(0, HOR_PD), pady=(0, VERT_PD)
    )
    select_result_directory_button = tk.Button(
        main_frame,
        text="Selecteer resultaat directory",
        command=select_result_directory
    )
    select_result_directory_button.grid(
        row=1, column=1, sticky=tk.W+tk.E, pady=(0, VERT_PD)
    )

    # Create label and entry for suffix input
    suffix_label = tk.Label(
        main_frame,
        text="Voer de suffix voor de resulterende PDF's in:"
    )
    suffix_label.grid(
        row=2, column=0, sticky=tk.W, padx=(0, HOR_PD), pady=(0, VERT_PD)
    )
    # Set a default value for the filename suffix field
    default_suffix = "_aangepast"
    suffix_entry = tk.Entry(main_frame, width=30)
    suffix_entry.insert(0, default_suffix) # Pre-populate the entry with the default value
    suffix_entry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=(0, VERT_PD))

    # Create file listbox
    file_listbox = tk.Listbox(
        main_frame, selectmode=tk.MULTIPLE, width=50, height=10
    )
    file_listbox.grid(
        row=3, column=0, sticky=tk.W, padx=(0, HOR_PD), pady=VERT_PD
    )

    # Create frame to hold subgrid with file selection buttons
    buttons_frame = tk.Frame(main_frame)
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid(row=3, column=1, sticky=tk.W+tk.E, pady=VERT_PD)

    # Create file selection buttons
    select_button = tk.Button(
        buttons_frame,
        text="Selecteer bestanden",
        command=select_files
    )
    select_button.grid(
        row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, pady=(0, VERT_PD)
    )

    # Open and resize the image using PIL
    # image = Image.open("images/info_logo.png")
    # resized_image = image.thumbnail((25, 25))
    # image.save("info_logo_resized.png")

    # Convert the resized image to a format compatible with Tkinter
    info_logo_image = tk.PhotoImage(file="images/info_logo_resized.png")
    select_help_button = tk.Button(
        buttons_frame,
        image=info_logo_image,
        command=show_help_select_files
    )
    select_help_button.grid(
        row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S, pady=(0, VERT_PD)
    )
    clear_button = tk.Button(
        buttons_frame,
        text="Wis bestandenlijst",
        command=clear_files
    )
    clear_button.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E)
    process_button = tk.Button(
        buttons_frame,
        text="Verwerk bestanden",
        command=process_files
    )
    process_button.grid(
        row=2, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(VERT_PD, 0)
    )

    # Create status label
    status_label = tk.Label(main_frame, text="")
    status_label.grid(row=4, columnspan=2, pady=VERT_PD)

    # Create author label
    author_label = tk.Label(main_frame, text="Auteur: Alejandro De Groote")
    author_label.grid(row=6, column=0, sticky=tk.W)

    root.mainloop()
