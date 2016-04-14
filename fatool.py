# -*- coding: utf-8 -*-

import sys
import argparse
import re
import datetime
from string import maketrans


def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)

    subparsers = parser.add_subparsers(title='facutter commands', help='each has own params, for more details use: command -h')

    sub_cut = subparsers.add_parser('cut', help='split supplied sequence into smaller parts, according to given params')
    sub_cut.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_cut.add_argument('-r', '--range', help='cutted sequence length', type=int, required=True)
    sub_cut.add_argument('-o', '--output', help='output file default: output.fa', type=argparse.FileType('w'), default='output.fa')
    sub_cut.add_argument('-s', '--step', help='step length default: 1', type=int, default=1)
    sub_cut.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_cut.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    sub_cut.set_defaults(func=cut_fa)

    sub_en = subparsers.add_parser('extractNames', help='extracting contigs names only')
    sub_en.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_en.add_argument('-o', '--output', help='output file if not supplied stdout', type=argparse.FileType('w'))
    sub_en.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_en.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    sub_en.set_defaults(func=extract_names)

    sub_ec = subparsers.add_parser('extractContigs', help='extracting contigs specified in file (output in new file)')
    sub_ec.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_ec.add_argument('--list', help='file containing list of contigs one contig per line', type=argparse.FileType('r'), required=True)
    sub_ec.add_argument('-o', '--output', help='output file; if --multifile is set output directory', type=str, required=True)
    sub_ec.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_ec.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    sub_ec.add_argument('--multifile', help='if this flag is set each contig will be saved in separate file', action='store_true')
    sub_ec.set_defaults(func=extract_contigs)

    sub_rc = subparsers.add_parser('remContigs', help='removing contigs specified in file (output in new file)')
    sub_rc.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_rc.add_argument('--list', help='file containing list of contigs one contig per line', type=argparse.FileType('r'), required=True)
    sub_rc.add_argument('-o', '--output', help='output file if not supplied stdout', type=str, required=True)
    sub_rc.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_rc.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    sub_rc.set_defaults(func=remove_contigs)
    
    sub_jc = subparsers.add_parser('join', help='joining two or more files, yet not verifing duplicates')
    sub_jc.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_jc.add_argument('-o', '--output', help='output file if not supplied stdout', type=argparse.FileType('w'), required=True)
    sub_jc.add_argument('--files', help='files to be joined', nargs='*', type=argparse.FileType('r'))
    sub_jc.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_jc.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    sub_jc.set_defaults(func=join)
    
    sub_sc = subparsers.add_parser('split', help='each cotig saved into separate file')
    sub_sc.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_sc.add_argument('-d', '--outputDir', help='output directory where splited contigs will be saved', type=str, required=True)
    sub_sc.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_sc.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    sub_sc.set_defaults(func=split_contigs)
    
    sub_r = subparsers.add_parser('reverse', help='reverse all sequences in file')
    sub_r.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_r.add_argument('-o', '--output', help='output file; if --multifile is set output directory', type=argparse.FileType('w'), required=True)
    sub_r.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_r.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    sub_r.set_defaults(func=reverse)
    
    sub_v  = subparsers.add_parser('validate', help='validates fa file')
    sub_v.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_v.add_argument('-t', '--type', help='type of sequence 0 - general, 1 DNA, 2 - amino', type=int, required=True)
    sub_v.add_argument('--detailed', help='set if you want to see detaild validation info', action='store_true')
    sub_v.set_defaults(func=validate)
    
    #parser.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    #parser.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))

    args = parser.parse_args()
    args.func(args)


def make_log(content, lfile):
    with lfile as f:
        f.write(content)


# function prepares pattern for contig search
def make_pattern(r):
    if re.match('^>', r.strip()):
        pattern = '('+re.escape(r.strip())+'\n[A-Za-z\n]*)[\Z>]?'
    else:
        pattern = '(> '+re.escape(r.strip())+'\n[A-Za-z\n]*|>'+r.strip()+'\n[A-Za-z\n]*)[\Z>]?'
    return pattern


def cut_fa(args):

    fafile = args.fafile
    output = args.output
    split_range = args.range
    step = args.step

    print 'step used: '+str(step)

    fa = ''  # sequence grabed from file and ceared
    with fafile as f:
        # load sequence from file remove first line and all white chars
        for r in f.readlines()[1:]:
            fa = fa+r.replace("\r", "").replace("\n", "")

    with output as o:
        coe = len(fa)  # end of fa position
        i = 0

        while i + split_range <= coe:
            # while curent position + length of frag is less or equal postion of the last char in file.
            o.write('> frag ' + str(i + 1) + ' : ' + str(i + split_range) + '\n' + str(fa[i:i + split_range]) + '\n')
            i = i + step


def extract_names(args):
    fafile = args.fafile
    output = args.output
    # sequence title line begining
    pat = re.compile('^>')
    if output is None:
        print 'no output defined results will be print on stdout\n'
        with fafile as f:
            for r in f.readlines():
                if pat.match(r):
                    print r
    else:
        # proceed fafile and save title lines in output file
        with fafile as f, output as o:
            for r in f.readlines():
                if pat.match(r):
                    o.write(r)

def make_file_name(r, suffix):
    if len(suffix) > 0:
        name = re.sub('[>\*\\\?\<\/]', '', r.strip())
        return name+'.'+suffix
    else:
        return re.sub('[>\*\\\?\<\/]', '', r.strip())


def extract_contigs(args):
    # default all extracted contigs in one file
    # with flag multifile save each contig to separate file
    fafile = args.fafile
    elist = args.list
    log = args.log
    log_content = '\nfatools extractContigs\tstarted:\t'+str(datetime.datetime.now())+'\t'

    # counters: extracted contigs and list items
    excounter = lcounter = 0
    log_not_found = ''

    print 'extracting contigs'
    # output to multi files
    if(args.multifile):
        output = args.output
        with elist as cntgs, fafile as f:
            content = f.read()
            for r in cntgs:
                #print r
                lcounter = lcounter + 1
                # check if list item is with '>' important to create pattern.
                
                m = re.search(make_pattern(r), content)

                if m:
                    excounter = excounter + 1
                    with open(output+'/'+make_file_name(r,'fa'), 'w') as o:
                        o.write(m.group(1))
                else:
                    # log_content = log_content + 'contig not found: ' + r
                    log_not_found = 'contig not found: ' + r
    # output to single file
    else:
        output = args.output
        with elist as cntgs, fafile as f, open(output, 'w') as o:
            content = f.read()
            for r in cntgs:
                lcounter = lcounter + 1
                # check if list item is with '>' important to create pattern.

                m = re.search(make_pattern(r), content)

                if m:
                    excounter = excounter + 1
                    o.write(m.group(1))
                else:
                    # log_content = log_content + 'contig not found: ' + r
                    log_not_found = 'contig not found: ' + r

        if(log):
            log_content = log_content + 'stoped:\t'+str(datetime.datetime.now())+'\n'
            if args.operator:
                log_content = log_content + 'operator:\t'+args.operator+'\n'
            log_content = log_content + '='*15+'\nlist items:\t'+str(lcounter)+'\nextracted contigs:\t'+str(excounter)+'\n'
            if log_not_found:
                log_content = log_content + '\nContigs not found:\n'+'='*15+'\n'+log_not_found
            make_log(log_content, log)
        else:
            print 'list items: '+str(lcounter)+'; extracted contigs: '+str(excounter)
            if log_not_found:
                '\nContigs not found:\n============================================\n'+log_not_found


def remove_contigs(args):
    fafile = args.fafile
    rlist = args.list
    output = args.output
    log = args.log
    # counters for listitems and removed contigs
    lcounter = rem_counter = 0
    with elist as cntgs, fafile as f, open(output, 'w') as o:
        content = f.read()
        for r in cntgs:
            lcounter = lcounter + 1

            if re.match(make_pattern, content):
                rem_counter = rem_counter + 1
            content = re.sub(make_pattern, '>', content)
        #rstrip removes last > left after removing last contig
        o.write(content.rstrip('>'))
    if(log):
        make_log('fatool - remContigs:\n list items:\t'+str(lcounter)+'\ncontings rmoved:\t'+str(rem_counter), log)
    else:
        print 'list items:\t'+str(lcounter)+'\ncontings rmoved:\t'+str(rem_counter)

def join(args):
    with args.fafile as f:
        content = f.read()
        for r in args.files:
            with r as j:
                content = content.rstrip() + '\n' + r.read()
        with args.output as o:
            o.write(content)
        
    


def split_contigs(args):
    with args.fafile as f:
        content = f.read()
        nc = content.split('>')
        for r in nc[1:]:
            #print ofile
            with open(args.outputDir+'/'+make_file_name(r.split('\n', 1)[0],'fa'), 'w') as o:
                o.write('>'+r)
            
        

def statistics(args):
    return 1


def validate(args):
    pattern = re.compile('[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]')
    #dna
    #amino
    not_valid = 0
    missmatches = {}
    with args.fafile as f:
        content = f.read()
        if not re.search('^>', content):
            print 'Invalid fa file no ">" at begining'
            exit(0)

        nc = content.split('>')
        nv_list = {}
        m = None
        log_info = ''
        # detailed flag show more info
        if(args.detailed):
            for r in nc[1:]:
                # removing first line of sequence it contains name of contig
                nr = re.sub('^>.*\n','','>'+r)
                m = pattern.finditer(nr)
                if m:
                    not_valid = 1
                    for i in m:
                        log_info += 'Contig:\t'+r.split('\n', 1)[0]+'\tposition:\t'+str(i.start())+'\tvalue:\t'+str(i.group())+'\n'
                    #nv_list = 
                    #break
        else:
            for r in nc[1:]:
                nr = re.sub('^>.*\n','','>'+r)
                if pattern.search(nr):
                    not_valid = 1
                    break
    if not_valid == 0:
        print 'File is valid fa file'
    else:
        print 'Invalid fa file'
        if log_info:
            print log_info

def reverse(args):
    with args.fafile as f, args.output as o:
        content = f.read()
        nc = content.split('>')
        for r in nc[1:]:#need to change
            nr = re.sub('^>.*\n','','>'+r)
            # removing new lines to output with 80 chars per line
            nr = re.sub('\n', '', nr)
            rev = nr[::-1]
            rev = rev.translate(maketrans('ACTGactg', 'TGACtgac'))
            rev = re.sub("(.{80})",'\\1\n', rev, 0)
            o.write('>rev_'+r.split('\n', 1)[0]+'\n'+rev)
            

if __name__ == '__main__':
    exit(main())
