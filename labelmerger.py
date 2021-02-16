from pagesizes import LabelPrintSize
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject


def read_all_label_pages(label_files):
    label_pages = []

    for lf in label_files:
        reader = PdfFileReader(lf)
        for i in range(reader.numPages):
            label_pages.append(reader.getPage(i))
    return label_pages


def open_label_files(label_file_names):
    l_files = [open(x, 'rb') for x in label_file_names]
    label_pages = read_all_label_pages(l_files)
    return l_files, label_pages


def label_merger(label_pages, print_size: LabelPrintSize):
    labels_per_page = print_size.get_num_labels_in_page()
    print_page_height, print_page_width = print_size.get_print_decimal_pts_height_width()
    label_page_height, label_page_width = print_size.get_label_decimal_pts_height_width()

    page_horizontal_print_area = print_size.get_print_decimal_pts_horizontal_print_area()
    label_vertical_print_area = print_size.get_label_decimal_pts_vertial_print_area()
    label_horizontal_print_area = print_size.get_label_decimal_pts_horizontal_print_area()

    pp_margin_top, pp_margin_right, pp_margin_bottom, pp_margin_left = print_size.get_print_margins()

    x_offset = ((page_horizontal_print_area -
                 label_page_width) / 2) + pp_margin_left
    y_offset = pp_margin_top

    writer = PdfFileWriter()

    page_buffer = None
    cnt = 0
    for label in label_pages:
        if page_buffer is None:
            page_buffer = PageObject.createBlankPage(
                None, print_page_width, print_page_height)
        scale_x = label_horizontal_print_area / label.mediaBox.getWidth()
        scale_y = label_vertical_print_area / label.mediaBox.getHeight()

        x = x_offset
        y = print_page_height - ((cnt + 1) * label_page_height - y_offset)

        page_buffer.mergeTransformedPage(label, (scale_x, 0, 0, scale_y, x, y))
        cnt += 1

        if cnt >= labels_per_page:
            cnt = 0
            writer.addPage(page_buffer)
            page_buffer = None

    if page_buffer is not None:
        writer.addPage(page_buffer)

    return writer


def do_label_merge(output_file, label_file_names, print_sizes):
    l_files, label_pages = open_label_files(label_file_names)

    writer = label_merger(label_pages, print_sizes)

    with open(output_file, 'wb') as f:
        writer.write(f)

    for f in l_files:
        f.close()
