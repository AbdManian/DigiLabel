import argparse
import pagesizes
from labelmerger import do_label_merge


def create_user_args():
    parser = argparse.ArgumentParser(
        description='Scale and merge multi-page label pdf files into single A4 PDF')

    parser.add_argument(
        '--output',
        '-o',
        dest='outputfile',
        help='Output pdf file',
        required=True)

    parser.add_argument(
        '--PrintWidth',
        metavar='SizeMM',
        help='Print page width (default=A4)',
        type=int,
        default=210)
    parser.add_argument(
        '--PrintHeight',
        metavar='SizeMM',
        help='Print page height (default=A4)',
        type=int,
        default=297)
    parser.add_argument('--PrintBottomMargin', metavar='SizeMM',
                        help='Bottom print margin', type=int, default=0)
    parser.add_argument('--PrintTopMargin', metavar='SizeMM',
                        help='Top print margin', type=int, default=0)
    parser.add_argument(
        '--LabelPageHeight',
        metavar='SizeMM',
        help='Height of label media paper',
        type=int,
        default=36)
    parser.add_argument(
        '--LabelPageWidth',
        metavar='SizeMM',
        help='Width of label media paper',
        type=int,
        default=107)
    parser.add_argument(
        '--LabelPageLeftMargin',
        metavar='SizeMM',
        help='Left margin for printable area in media paper',
        type=int,
        default=3)
    parser.add_argument(
        '--LabelPageBottomMargin',
        metavar='SizeMM',
        help='Bottom margin for printable area in media paper',
        type=int,
        default=0)
    parser.add_argument(
        '--LabelPageRightMargin',
        metavar='SizeMM',
        help='Right margin for printable area in media paper',
        type=int,
        default=1)
    parser.add_argument(
        '--LabelPageTopMargin',
        metavar='SizeMM',
        help='Top margin for printable area in media paper',
        type=int,
        default=2)

    parser.add_argument(
        'labels',
        action='store',
        nargs='+',
        help='Input label files')

    return parser.parse_args()


def build_label_print_size(args):
    label_margins = pagesizes.PrintMargins(
        args.LabelPageTopMargin,
        args.LabelPageRightMargin,
        args.LabelPageBottomMargin,
        args.LabelPageLeftMargin)

    label_page = pagesizes.PageSize(
        args.LabelPageHeight,
        args.LabelPageWidth,
        label_margins)

    print_margins = pagesizes.PrintMargins(
        args.PrintTopMargin,
        0,
        args.PrintBottomMargin,
        0
    )

    print_page = pagesizes.PageSize(
        args.PrintHeight,
        args.PrintWidth,
        print_margins)

    return pagesizes.LabelPrintSize(print_page, label_page)


def main():
    user_args = create_user_args()
    page_sizes = build_label_print_size(user_args)
    do_label_merge(user_args.outputfile, user_args.labels, page_sizes)


if __name__ == '__main__':
    main()
