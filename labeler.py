from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject
import decimal

A4_WIDTH_MM = 210.0
A4_HEIGHT_MM = 297.0

A4_PAGE = (A4_WIDTH_MM, A4_HEIGHT_MM)

LABEL_MEDIA_WIDTH = 106
LABEL_MEDIA_HEIGHT = 36

LABEL_MEDIA_PAGE = (LABEL_MEDIA_WIDTH, LABEL_MEDIA_HEIGHT)


def mm2pts(mm_value):
    return mm_value*2.83465


def read_all_label_pages(label_files):
    label_pages = []

    for lf in label_files:
        reader = PdfFileReader(lf)
        for i in range(reader.numPages):
            label_pages.append(reader.getPage(i))
    return label_pages


def convert_label_files(label_files_name, output_file_name, print_size=A4_PAGE, label_media_size=LABEL_MEDIA_PAGE):
    l_files = [open(f, 'rb') for f in label_files_name]

    print_width, print_height = print_size
    label_width, label_height = label_media_size

    l_pages = read_all_label_pages(l_files)
    total_num_labels = len(l_pages)
    label_per_page = int(print_height / label_height)
    writer = PdfFileWriter()

    scalex = decimal.Decimal(mm2pts(label_width)) / l_pages[0].mediaBox.getWidth()
    scaley = decimal.Decimal(mm2pts(label_height)) / l_pages[0].mediaBox.getHeight()
    pw = decimal.Decimal(mm2pts(print_width))             # Page Width
    ph = decimal.Decimal(mm2pts(print_height))            # Page Height
    lw = decimal.Decimal(mm2pts(label_width))     # Label Width
    lh = decimal.Decimal(mm2pts(label_height))    # Label Height

    page_buffer = None
    i = 0
    for label in l_pages:
        if page_buffer is None:
            page_buffer = PageObject.createBlankPage(None, pw, ph)

        x = (pw - lw)/2
        y = ph - ((i+1) * lh)

        page_buffer.mergeTransformedPage(label, (scalex,0,0,scaley,x,y))
        i=i+1
        if i >= label_per_page:
            i = 0
            writer.addPage(page_buffer)
            page_buffer = None

    if page_buffer is not None:
        writer.addPage(page_buffer)

    with open(output_file_name, 'wb') as f:
        writer.write(f)

    for f in l_files:
        f.close()


if __name__ == '__main__':
    labels = ['label.pdf']
    convert_label_files(labels, 'out1.pdf')


