NAME
====
fatool


VERSION
=======

0.3.1

LICENSE
=======
APACHE 2.0  Specified in LICENSE.md file

INTRODUCTION
============

Package and Command line tool in python 2.7. It operates on fa/fasta/etc. files. version: 0.2.1. To install package use setup.py install.


PREREQUISITES
=============
PYTHON 2.7

USAGE
=====



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
                        [--report REPORT] [--operator OPERATOR]

optional arguments:
  -h, --help                    show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -r RANGE, --range RANGE       cutted sequence length
  -o OUTPUT, --output OUTPUT    output file default: output.fa
  -s STEP, --step STEP          step length default: 1
  --report REPORT               log file if not supplied stdout
  --operator OPERATOR           user who have fired script it will be noted in log
  
  
    extractNames
  
usage: cmdfatool.py extractNames [-h] -f FAFILE [-o OUTPUT] [--report REPORT]
                                 [--operator OPERATOR]

optional arguments:
  -h, --help                    show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -o OUTPUT, --output OUTPUT    output file if not supplied stdout
  --report REPORT               log file if not supplied stdout
  --operator OPERATOR           user who have fired script it will be noted in log
 
 
    extractContigs
 
usage: cmdfatool.py extractContigs [-h] -f FAFILE --list LIST -o OUTPUT
                                   [--report REPORT] [--operator OPERATOR]
                                   [--multifile]

optional arguments:
  -h, --help                    show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  --list LIST                   file containing list of contigs one contig per line
  -o OUTPUT, --output OUTPUT    output file; if --multifile is set output directory
  --report REPORT               log file if not supplied stdout
  --operator OPERATOR           user who have fired script it will be noted in log
  --multifile                   if this flag is set each contig will be saved in
                                separate file
    
    
    remContigs
                        
usage: cmdfatool.py remContigs [-h] -f FAFILE --list LIST -o OUTPUT
                               [--report REPORT] [--operator OPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  --list LIST           file containing list of contigs one contig per line
  -o OUTPUT, --output OUTPUT    output file if not supplied stdout
  --report REPORT             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log
  
  
    join
    
usage: cmdfatool.py join [-h] -f FAFILE -o OUTPUT
                         [--files [FILES [FILES ...]]] [--overwrite]
                         [--report REPORT] [--operator OPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -o OUTPUT, --output OUTPUT    output file if not supplied stdout
  --files [FILES [FILES ...]]   files to be joined
  --overwrite           if set owerwrites contigs with same name
  --report REPORT             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log
  
  
    split

usage: cmdfatool.py split [-h] -f FAFILE -d OUTPUTDIR [--report REPORT]
                          [--operator OPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -d OUTPUTDIR, --outputDir OUTPUTDIR   output directory where splited contigs will be saved
  --report REPORT             log file if not supplied stdout
  --operator OPERATOR   user who have fired script it will be noted in log
  
  
    reverse
  
usage: cmdfatool.py reverse [-h] -f FAFILE -o OUTPUT [--report REPORT]
                            [--operator OPERATOR]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to be cut usualy *.fa
  -o OUTPUT, --output OUTPUT    output file; if --multifile is set output directory
  --report REPORT             log file if not supplied stdout
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
  
usage: cmdfatool.py stats [-h] -f FAFILE [--report REPORT]
                          [--operator [OPERATOR [OPERATOR ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE    file to show statistics usualy *.fa
  --report REPORT             log file if not supplied stdout
  --operator [OPERATOR [OPERATOR ...]]  user who have fired script it will be noted in log

    findPrimer

usage: cmdfatool.py findPrimer [-h] -f FAFILE --start START --stop STOP --mode
                               {FF,FR} [--minlen MINLEN] [--maxlen MAXLEN]
                               [--mml MML] [--report REPORT]
                               [--operator [OPERATOR [OPERATOR ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -f FAFILE, --fafile FAFILE  
                        file to show statistics usualy *.fa
  --start START         first sequence to be found
  --stop STOP           last sequence to be found
  --mode {FF,FR}        FF (start - forward orientated, stop - forward orientated) or FR (start - forward orientated, stop - reverse orientated)
  --minlen MINLEN       minimum length (detfault 50bp)
  --maxlen MAXLEN       max length (detfault 1000bp)
  --mml MML             mismatch level number of allowed missmatches in primers (detfault 0)
  --report REPORT       report results into file if not supplied stdout
  --operator [OPERATOR [OPERATOR ...]]
                        user who have fired script it will be noted in report

                        
  cutNameMarker:


usage: cmdfatool.py cutNameMarker [-h] -f FAFILE -m MARKER -l LENGTH
                                  --keepMarker KEEPMARKER [-o OUTPUT]

optional arguments:
  -h, --help                  show this help message and exit
  -f FAFILE, --fafile FAFILE  file to show statistics usualy *.fa
  -m MARKER, --marker MARKER  marker that indicates start of cut
  -l LENGTH, --length LENGTH  length of cut
  --keepMarker KEEPMARKER     weather to keep marker or not default 1 (Yes)
  -o OUTPUT, --output OUTPUT  output file default: output.fa
