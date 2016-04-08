NAME
====
fatool

VERSION
=======

0.1.0

LICENSE
=======

INTRODUCTION
============

Command line tool in python 2.7. It operates on fa/fasta/etc. files. version: 0.1.0


PREREQUISITES
=============
PYTHON 2.7

COMMAND LINE
============

usage: fatool.py [-h] -f FAFILE [--operator OPERATOR] [--log LOG]
                 {cut,extractNames,extractContigs,remContigs,join,split} ...

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile   file to be cut usualy *.fa
  --operator OPERATOR   user who have fired script it will be noted in log
  --log LOG             log file if not supplied stdout

facutter commands:
  {cut,extractNames,extractContigs,remContigs,join,split} each has own params
  
    cut                 split supplied sequence into smaller parts, according to given params
    extractNames        extracting contigs names only
    extractContigs      extracting contigs specified in file (output in new file)
    join                joining two or more files, yet not verifing duplicates
    remContigs          removing contigs specified in file (output in new file)
    split               each cotig saved into separate file
  
cut:
  
  usage: fatool.py cut [-h] -r RANGE [-o OUTPUT] [-s STEP] [--log LOG]

  optional arguments:
  -h, --help            show this help message and exit
  -r RANGE, --range RANGE	cutted sequence length
  -o OUTPUT, --output OUTPUT	output file default: output.fa
  -s STEP, --step STEP  step length default: 1
  --log LOG             log file if not supplied stdout
  
extractContigs:
  
  usage: fatool.py extractContigs [-h] --list LIST -o OUTPUT [--log LOG] [--multifile]

  optional arguments:
  -h, --help            show this help message and exit
  --list LIST           file containing list of contigs one contig per line
  -o OUTPUT, --output	  output file; if --multifile is set output directory
  --log LOG             log file if not supplied stdout
  --multifile           if this flag is set each contig will be saved inseparate file

  
extractNames:
  
  usage: fatool.py extractNames [-h] [-o OUTPUT] [--log LOG]

  optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output 	output file if not supplied stdout
  --log LOG             log file if not supplied stdout

join:

  usage: fatool.py join [-h] -o OUTPUT [--files [FILES [FILES ...]]]

  optional arguments:
  -h, --help                  show this help message and exit
  -o OUTPUT, --output OUTPUT  output file
  --files [FILES [FILES ...]] files to be joined
 
remContigs:
  
  usage: fatool.py remContigs [-h] --list LIST -o OUTPUT [--log LOG]

  optional arguments:
  -h, --help            show this help message and exit
  --list LIST           file containing list of contigs one contig per line
  -o OUTPUT, --output 	output file if not supplied stdout
  --log LOG             log file if not supplied stdout

split:

  usage: fatool.py split [-h] -d OUTPUTDIR

  optional arguments:
  -h, --help                show this help message and exit
  -d OUTPUTDIR, --outputDir output directory where splited contigs will be saved