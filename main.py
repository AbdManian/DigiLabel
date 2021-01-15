import labeler
import argparse


parser = argparse.ArgumentParser(description=
                                 'Scale and merge multi-page label pdf files into single A4 PDF')

parser.add_argument('--output', '-o', dest='outputfile', help='Output pdf file', required=True)

parser.add_argument('labels', action='store', nargs='+', help='Input label files')

args = parser.parse_args()

labeler.convert_label_files(args.labels, args.outputfile)
