NAME
====
fatool

DESCRIPTION
===========

Tool for analyze and manipulate fasta files

VERSION
=======

0.2.1

LICENSE
=======
APACHE 2.0  Specified in LICENSE.md file

INTRODUCTION
============

Command line tool in python 2.7. It operates on fa/fasta/etc. files. version: 0.1.0


PREREQUISITES
=============
PYTHON 2.7

COMMAND LINE
============

usage: cmdfatool.py [-h] [-v]
                    {cut,extractNames,extractContigs,remContigs,join,split,reverse,validate,stats}

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         display version number and exit

fatool commands:
  {cut,extractNames,extractContigs,remContigs,join,split,reverse,validate,stats} each has own params, for more details use: command -h
  
    cut                 split supplied sequence into smaller parts, according to given params
    extractNames        extracting contigs names only
    extractContigs      extracting contigs specified in file (output in new file)
    remContigs          removing contigs specified in file (output in new file)
    join                joining two or more files, yet not verifing duplicates
    split               each cotig saved into separate file
    reverse             reverse all sequences in file
    validate            validates fa file
    stats               show statistics of fa file

    
    cut:
    
usage: cmdfatool.py cut [-h] -f FAFILE -r RANGE [-o OUTPUT] [-s STEP]
                        [--log LOG] [--operator OPERATOR]

optional arguments:
  -h, --help                    show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -r RANGE, --range RANGE       cutted sequence length
  -o OUTPUT, --output OUTPUT    output file default: output.fa
  -s STEP, --step STEP          step length default: 1
  --log LOG                     log file if not supplied stdout
  --operator OPERATOR           user who have fired script it will be noted in log
  
  
    extractNames:
  
usage: cmdfatool.py extractNames [-h] -f FAFILE [-o OUTPUT] [--log LOG]
                                 [--operator OPERATOR]

optional arguments:
  -h, --help                    show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -o OUTPUT, --output OUTPUT    output file if not supplied stdout
  --log LOG             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log
 
 
    extractContigs:
 
usage: cmdfatool.py extractContigs [-h] -f FAFILE --list LIST -o OUTPUT
                                   [--log LOG] [--operator OPERATOR]
                                   [--multifile]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  --list LIST           file containing list of contigs one contig per line
  -o OUTPUT, --output OUTPUT    output file; if --multifile is set output directory
  --log LOG             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log
  --multifile           if this flag is set each contig will be saved in
                        separate file
    
    
    remContigs
                        
usage: cmdfatool.py remContigs [-h] -f FAFILE --list LIST -o OUTPUT
                               [--log LOG] [--operator OPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  --list LIST           file containing list of contigs one contig per line
  -o OUTPUT, --output OUTPUT    output file if not supplied stdout
  --log LOG             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log
  
  
    join
    
usage: cmdfatool.py join [-h] -f FAFILE -o OUTPUT
                         [--files [FILES [FILES ...]]] [--overwrite]
                         [--log LOG] [--operator OPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -o OUTPUT, --output OUTPUT    output file if not supplied stdout
  --files [FILES [FILES ...]]   files to be joined
  --overwrite           if set owerwrites contigs with same name
  --log LOG             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log
  
  
  split

usage: cmdfatool.py split [-h] -f FAFILE -d OUTPUTDIR [--log LOG]
                          [--operator OPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -d OUTPUTDIR, --outputDir OUTPUTDIR   output directory where splited contigs will be saved
  --log LOG             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log
  
  
  reverse
  
usage: cmdfatool.py reverse [-h] -f FAFILE -o OUTPUT [--log LOG]
                            [--operator OPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -o OUTPUT, --output OUTPUT    output file; if --multifile is set output directory
  --log LOG             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log  
  
  
  validate
  
usage: cmdfatool.py validate [-h] -f FAFILE -t TYPE [--details]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE
                        file to be cut usualy *.fa
  -t TYPE, --type TYPE  type of sequence 0 - general, 1 DNA, 2 - amino
  --details             set if you want to see detaild validation info
  
  
  stats
  
usage: cmdfatool.py stats [-h] -f FAFILE [--log LOG]
                          [--operator [OPERATOR [OPERATOR ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to show statistics usualy *.fa
  --log LOG             log file if not supplied stdout
  --operator [OPERATOR [OPERATOR ...]]  user who have fired script it will be noted in log
