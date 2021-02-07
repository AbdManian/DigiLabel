import labeler
import argparse


parser = argparse.ArgumentParser(description=
                                 'Scale and merge multi-page label pdf files into single A4 PDF')

parser.add_argument('--output', '-o', dest='outputfile', help='Output pdf file', required=True)

parser.add_argument('--PrintWidth', metavar='SizeMM',
                    help='Print page width (default=A4)', type=int, default=210)
parser.add_argument('--PrintHeight', metavar='SizeMM',
                    help='Print page height (default=A4)', type=int, default=297)
parser.add_argument('--PrintBottomMargin', metavar='SizeMM',
                    help='Bottom print margin', type=int, default=0)
parser.add_argument('--PrintTopMargin', metavar='SizeMM',
                    help='Top print margin', type=int, default=0)
parser.add_argument('--LabelPageHeight', metavar='SizeMM',
                    help='Height of label media paper', type=int, default=36)
parser.add_argument('--LabelPageWidth', metavar='SizeMM',
                    help='Width of label media paper', type=int, default=107)
parser.add_argument('--LabelPageLeftMargin', metavar='SizeMM',
                    help='Left margin for printable area in media paper', type=int, default=3)
parser.add_argument('--LabelPageBottomMargin', metavar='SizeMM',
                    help='Bottom margin for printable area in media paper', type=int, default=0)
parser.add_argument('--LabelPageRightMargin', metavar='SizeMM',
                    help='Right margin for printable area in media paper', type=int, default=1)
parser.add_argument('--LabelPageTopMargin', metavar='SizeMM',
                    help='Top margin for printable area in media paper', type=int, default=2)

parser.add_argument('labels', action='store', nargs='+', help='Input label files')

args = parser.parse_args()

print(args)
exit(0)
labeler.convert_label_files(args.labels, args.outputfile)
