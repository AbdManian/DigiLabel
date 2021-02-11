from decimal import Decimal


def mm2pts(mm_value):
    return mm_value * 2.83465


def decimal_pts(mm_value):
    return Decimal(mm2pts(mm_value))


class PrintMargins:
    def __init__(self, top, right, bottom, left):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def get_horizontal_margins(self):
        return self.left + self.right

    def get_vertical_margins(self):
        return self.top + self.bottom

    def __repr__(self):
        return f"Margins: {self.top} {self.right} {self.bottom} {self.left}"

    def get_decimal_pts(self):
        return decimal_pts(self.top), decimal_pts(self.right), decimal_pts(self.bottom), decimal_pts(self.left)


class PageSize:
    def __init__(self, height, width, print_margins: PrintMargins = None):
        self.height = height
        self.width = width
        self.margins = print_margins
        if self.margins is None:
            self.margins = PrintMargins(0, 0, 0, 0)

    def get_vertical_print_area(self):
        return self.height - self.margins.get_vertical_margins()

    def get_horizontal_print_area(self):
        return self.width - self.margins.get_horizontal_margins()

    def validate_size(self):
        return self.get_vertical_print_area() > 0 and self.get_horizontal_print_area() > 0

    def __repr__(self):
        return f"Page: {self.height}x{self.width} |{self.margins}|"

    def get_decimal_pts_height_width(self):
        return decimal_pts(self.height), decimal_pts(self.width)

    def get_decimal_pts_margins(self):
        return self.margins.get_decimal_pts()


class LabelPrintSize:
    def __init__(self, page: PageSize, label: PageSize):
        self.page = page
        self.label = label

    def get_num_labels_in_page(self):
        return int(self.page.get_vertical_print_area() / self.label.height)

    def validate_size(self):
        return (self.page.validate_size() and
                self.label.validate_size() and
                self.get_num_labels_in_page() > 0)

    def __repr__(self):
        return f"LabelPrintSize: Page=|{self.page}| Label=|{self.label}| " \
               f"valid={self.validate_size()} num_labels={self.get_num_labels_in_page()}"

    def get_print_decimal_pts_height_width(self):
        return self.page.get_decimal_pts_height_width()

    def get_label_decimal_pts_height_width(self):
        return self.label.get_decimal_pts_height_width()

    def get_print_margins(self):
        return self.page.get_decimal_pts_margins()

    def get_label_margins(self):
        return self.label.get_decimal_pts_margins()

    def get_print_decimal_pts_horizontal_print_area(self):
        return decimal_pts(self.page.get_horizontal_print_area())

    def get_label_decimal_pts_vertial_print_area(self):
        return decimal_pts(self.label.get_vertical_print_area())

    def get_label_decimal_pts_horizontal_print_area(self):
        return decimal_pts(self.label.get_horizontal_print_area())


if __name__ == '__main__':
    margins = PrintMargins(1, 2, 3, 4)
    label_page = PageSize(12, 10, margins)
    print_page = PageSize(80, 15, PrintMargins(10, 0, 3, 0))
    dut = LabelPrintSize(print_page, label_page)
    print(dut.validate_size(), dut.get_num_labels_in_page(), print_page.get_vertical_print_area())



