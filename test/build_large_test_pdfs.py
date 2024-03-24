from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

module_path = Path(__file__).parent

input_pdf = module_path / Path("../input/factuur.pdf")
factuur = PdfReader(input_pdf)

for nbr in range(1, 11):
    output_pdf = module_path / Path("../input/factuur_1000" + f"_{nbr}.pdf")
    with PdfWriter(str(output_pdf)) as factuur_1000:
        page = factuur.pages[0]
        for _ in range(1000):
            factuur_1000.add_page(page)
