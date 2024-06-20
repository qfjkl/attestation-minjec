import qrcode
import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def add_qr_to_pdf(input_pdf, output_pdf, qr_code_file, page_number, position):
    """Adds a QR code image to a specified page in an existing PDF file.
    
    Args:
        input_pdf (str): The filename of the existing PDF file.
        output_pdf (str): The filename for the output PDF with the QR code added.
        qr_code_file (str): The filename of the QR code image to add.
        page_number (int): The page number to add the QR code to (1-based index).
        position (tuple): The (x, y) position to place the QR code on the page.
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawImage(os.path.join(os.getcwd(), "qr-codes", qr_code_file), *position, width=100, height=100)  # Adjust the size as needed
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open(os.path.join(os.getcwd(), "Attestations", input_pdf), "rb"))
    output = PdfWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        if i == page_number - 1:  # Page numbers are 0-based in PyPDF2
            page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    with open(os.path.join(os.getcwd(), "Attestations", output_pdf), "wb") as outputStream:
        output.write(outputStream)


def generate_qr_code_and_add_to_pdf(data, position):
    """Generates QR codes from the provided data and saves them as image files.
    Also adds the QR codes to specified PDF files.
    
    Args:
        data (dict): A dictionary where the keys are filenames for the QR code images and the values are URLs to encode in the QR codes.
        position (tuple): The (x, y) position to place the QR code on the PDF page.
    """
    # Create a directory for QR codes if it doesn't exist
    if not os.path.exists("qr-codes"):
        os.makedirs("qr-codes")

    for file_name, url in data.items():
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(os.path.join(os.getcwd(), "qr-codes", file_name))
        
        # Add QR code to PDF
        pdf_filename = f"attestation {file_name.split('.')[0].upper()}.pdf"
        output_pdf_filename = f"{file_name.split('.')[0].upper()}.pdf"
        qr_code_file_name = file_name
        add_qr_to_pdf(pdf_filename, output_pdf_filename, qr_code_file_name, 1, position)


def get_pdf_page_size(pdf_file, page_number):
    """Gets the size of the specified page in the PDF file.
    
    Args:
        pdf_file (str): The filename of the PDF file.
        page_number (int): The page number to inspect (1-based index).
    
    Returns:
        tuple: The width and height of the specified page.
    """
    doc = fitz.open(os.path.join(os.getcwd(), "Attestations", pdf_file))
    page = doc.load_page(page_number - 1)  # 0-based index
    rect = page.rect
    return rect.width, rect.height


def inches_to_pixels(inches, ppi=96):
    """Converts inches to pixels based on the given PPI (pixels per inch).
    
    Args:
        inches (float): The size in inches.
        ppi (int, optional): Pixels per inch. Default is 96 for screen resolution.
        
    Returns:
        float: The size in pixels.
    """
    return inches * ppi

def pixels_to_inches(pixels, ppi=96):
    """Converts pixels to inches based on the given PPI (pixels per inch).
    
    Args:
        pixels (float): The size in pixels.
        ppi (int, optional): Pixels per inch. Default is 96 for screen resolution. For print, the standard is often 300 PPI.
        
    Returns:
        float: The size in inches.
    """
    return pixels / ppi


# Main part of the script
if __name__ == "__main__":
    pdf_size = get_pdf_page_size("attestation BAKARI.pdf", 1)
    # print(pdf_size)

    width_distance = 17995.531 # px
    height_distance =  866 # px
    
    position = (pixels_to_inches(width_distance), pixels_to_inches(height_distance))
    
    data = {
        "Bakari.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/BAKARI.pdf",
        "Beyeck.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/BEYECK.pdf",
        "Dobe.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/DOBE.pdf",
        "Essama.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/ESSAMA.pdf",
        "Etoundi.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/ETOUNDI.pdf",
        "Mbarga.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/MBARGA.pdf",
        "Mbele.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/MBELE.pdf",
        "Mbida.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/MBIDA.pdf",
        "Ndeh.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/NDEH.pdf",
        "Ngon.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/NGON.pdf",
        "Taka.png": "https://github.com/qfjkl/attestation-minjec/blob/main/Attestations/TAKA.pdf"
    }

    generate_qr_code_and_add_to_pdf(data, position)