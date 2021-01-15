# DigiLabel
Convert multi-page label files into single pdf file

## motivation
Originally designed for printing DigiKala label files with ordinary laserjet printers!

## Requirements
You need python3 and PyPDF2 package. Use pip for installing the dependency

    pip install -r requirements.txt
    
## How to use
Call `main.py` 
  python main.py -o output_file.pdf label1.pdf 
  
Command line:

    usage: main.py [-h] --output OUTPUTFILE labels [labels ...]

    Scale and merge multi-page label pdf files into single A4 PDF

    positional arguments:
      labels                Input label files

    optional arguments:
      -h, --help            show this help message and exit
      --output OUTPUTFILE, -o OUTPUTFILE
                            Output pdf file
