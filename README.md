# Attestation Minjec

This project generates QR codes and integrates them into PDF files. It uses Python with the `qrcode`, `PyPDF2`, and `reportlab` libraries.

## Features

- Generate QR codes from a dictionary of URLs and save them as image files.
- Automatically save QR code images in a "qr-codes" directory.
- Insert generated QR codes into specified pages of existing PDF files.
- Position QR codes at specified coordinates on PDF pages.
- Provide customizable options for QR code generation and PDF manipulation.

## Requirements

- Python 3.x
- `qrcode` library
- `PyPDF2` library
- `reportlab` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/qfjkl/attestation-minjec.git
    ```

2. Change to the project directory:

    ```bash
    cd attestation-minjec
    ```

3. Install the required libraries:

    ```bash
    pip install qrcode[pil] PyPDF2 reportlab
    ```

## Usage

1. Create a dictionary with filenames and URLs to generate QR codes.

    ```python
    data = {
        "example1.png": "http://example.com/1",
        "example2.png": "http://example.com/2",
    }
    ```

2. Call the `generate_qr_code` function to generate QR codes and insert them into PDF files.

    ```python
    generate_qr_code(data)
    ```

## Functions

### `generate_qr_code`

Generates QR codes from the provided data and saves them as image files. Also adds the QR codes to specified PDF files.

**Args:**
- `data` (dict): A dictionary where the keys are filenames for the QR code images and the values are URLs to encode in the QR codes.
- `position` (tuple): The (x, y) position to place the QR code on the PDF page. Default is `(100, 100)`.

### `add_qr_to_pdf`

Adds a QR code image to a specified page in an existing PDF file.

**Args:**
- `input_pdf` (str): The filename of the existing PDF file.
- `output_pdf` (str): The filename for the output PDF with the QR code added.
- `qr_code_file` (str): The filename of the QR code image to add.
- `page_number` (int): The page number to add the QR code to (1-based index).
- `position` (tuple): The (x, y) position to place the QR code on the page.