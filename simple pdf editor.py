from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from tkinter import Tk, filedialog
import time

def add_to_pdf(input_path, output_path, text, image_path, text_position=(100, 700), image_position=(100, 500), image_size=(200, 100)):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    x_text, y_text = text_position
    can.setFont("Times New Roman", 15)
    can.drawString(x_text, y_text, text)

    x_img, y_img = image_position
    img_w, img_h = image_size
    can.drawImage(image_path, x_img, y_img, img_w, img_h)

    can.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    overlay_page = overlay_pdf.page[0]

    for page in reader.pages:
        page.merge_page(overlay_page)
        writer.add_page(page)

    with open(output_path, "wb") as op:
        writer.write(op)

    print("PDF edited successfully at {output_path}")


def main():
    input_path = input("Enter the path of the pdf")

    output_path = input("Enter the desired location for the pdf to be saved")

    text = input("add text")

    root = Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    
    time.sleep(0.5)
    img_path = filedialog.askopenfilename(title="select an image to add", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    root.update()

    if not img_path:
        print("no img selected")

        return
    
    add_to_pdf(input_path, output_path, text, img_path)



if __name__ == "__main__":
    main()