import fitz  # PyMuPDF
import os
import glob

def convert_pdf_to_image(pdf_path: str, pdf_filename: str, zoom_factor: float):
    """
    Convert all pages of a given PDF into high-resolution images using PyMuPDF.

    Args:
        pdf_path (str): Directory containing the PDF
        pdf_filename (str): PDF file name (e.g., 'paper123.pdf')
        zoom_factor (float): Zoom level for rendering (1.0 = 72dpi, 2.0 = 144dpi, etc.)

    Returns:
        List[fitz.Pixmap]: List of rendered images (one per page), or None on error
    """
    images = []

    try:
        # Clear previous MuPDF warning buffer
        fitz.TOOLS.mupdf_warnings()  

        # Open PDF document
        pdf_file = os.path.join(pdf_path, pdf_filename)
        doc = fitz.open(pdf_file)

        # Check for any MuPDF warnings (e.g., corrupted file)
        warnings = fitz.TOOLS.mupdf_warnings()
        if warnings:
            print(f"Warning(s) when opening {pdf_filename}:\n{warnings}")
            raise RuntimeError("MuPDF raised warnings when loading the document.")

        # Define zoom factor for resolution scaling
        zoom_matrix = fitz.Matrix(zoom_factor, zoom_factor)

        # Convert each page to image (Pixmap)
        for page_num, page in enumerate(doc):
            pix = page.get_pixmap(matrix=zoom_matrix)
            images.append(pix)

        print(f"[✓] PDF '{pdf_filename}' converted successfully with {len(images)} pages.")
        return images

    except Exception as e:
        print(f"[✗] Error when processing PDF '{pdf_filename}': {e}")
        return None




