# FA_TOOL

Command line tool in python. It operates on fa/fasta etc. files. version: 0.0.1

fatool.py [-h] -f FAFILE  {cut,extractNames,extractContigs,remContigs}

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE	file to be cut usualy *.fa

fatool commands:
  {cut,extractNames,extractContigs,remContigs} each has own params, for more details use: command -h
  
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
  -o OUTPUT, --output	output file; if --multifile is set output directory
  --log LOG             log file if not supplied stdout
  --multifile           if this flag is set each contig will be saved inseparate file

  
extractNames:
  
  usage: fatool.py extractNames [-h] [-o OUTPUT] [--log LOG]

  optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output 	output file if not supplied stdout
  --log LOG             log file if not supplied stdout
  
  remContigs:
  
usage: facuter4.py remContigs [-h] --list LIST -o OUTPUT [--log LOG]

  optional arguments:
  -h, --help            show this help message and exit
  --list LIST           file containing list of contigs one contig per line
  -o OUTPUT, --output 	output file if not supplied stdout
  --log LOG             log file if not supplied stdout
  