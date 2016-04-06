# -*- coding: utf-8 -*-

import sys
import argparse
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)

    subparsers = parser.add_subparsers(title='facutter commands', help='each has own params, for more details use: command -h')

    sub_cut = subparsers.add_parser('cut')
    sub_cut.add_argument('-r', '--range', help='cutted sequence length', type=int, required=True)
    sub_cut.add_argument('-o', '--output', help='output file default: output.fa', type=argparse.FileType('w'), default='output.fa')
    sub_cut.add_argument('-s', '--step', help='step length default: 1', type=int, default=1)
    sub_cut.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_cut.set_defaults(func=cut_fa)

    sub_en = subparsers.add_parser('extractNames')
    sub_en.add_argument('-o', '--output', help='output file if not supplied stdout', type=argparse.FileType('w'))
    # sub_en.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_en.set_defaults(func=extract_names)

    sub_ec = subparsers.add_parser('extractContigs')
    sub_ec.add_argument('--list', help='file containing list of contigs one contig per line', type=argparse.FileType('r'), required=True)
    sub_ec.add_argument('-o', '--output', help='output file; if --multifile is set output directory', type=str, required=True)
    # sub_ec.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_ec.add_argument('--multifile', help='if this flag is set each contig will be saved in separate file', action='store_true')
    sub_ec.set_defaults(func=extract_contigs)

    sub_rc = subparsers.add_parser('remContigs')
    sub_rc.add_argument('--list', help='file containing list of contigs one contig per line', type=argparse.FileType('r'), required=True)
    sub_rc.add_argument('-o', '--output', help='output file if not supplied stdout', type=str, required=True)
    # sub_rc.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))
    sub_rc.set_defaults(func=remove_contigs)

    parser.add_argument('--operator', help='user who have fired script it will be noted in log', type=str)
    parser.add_argument('--log', help='log file if not supplied stdout', type=argparse.FileType('w'))

    args = parser.parse_args()
    args.func(args)


def make_log(content, lfile):
    with lfile as f:
        f.write(content)


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
        # N = step*8000

        while i + split_range <= coe:
            # while curent position + length of frag is less or equal postion of the last char in file.
            o.write('> frag ' + str(i + 1) + ' : ' + str(i + split_range) + '\n' + str(fa[i:i + split_range]) + '\n')
            i = i + step
            # print dot every N split to show that script does not heng.
            # if(i%N == 0): sys.stdout.write('.')


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


def extract_contigs(args):
    # default all extracted contigs in one file
    # with flag multifile save each contig to separate file
    fafile = args.fafile
    elist = args.list
    log = args.log

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
                lcounter = lcounter + 1
                # check if list item is with '>' important to create pattern.
                if re.match('^>', r.strip()):
                    pattern = '('+re.escape(r.strip())+'\n[A-Za-z\n]*)>'
                else:
                    pattern = '(> '+re.escape(r.strip())+'\n[A-Za-z\n]*|>'+r.strip()+'\n[A-Za-z\n]*)>'

                m = re.search(pattern, content)

                if m:
                    excounter = excounter + 1
                    opt = re.sub('[>\*\\\?\<\/]', '', r.strip())
                    with open(output+'/'+opt+'.fa', 'w') as o:
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
                if re.match('^>', r.strip()):
                    pattern = '('+re.escape(r.strip())+'\n[A-Za-z\n]*)>'
                else:
                    pattern = '(> '+re.escape(r.strip())+'\n[A-Za-z\n]*|>'+r.strip()+'\n[A-Za-z\n]*)>'

                m = re.search(pattern, content)

                if m:
                    excounter = excounter + 1
                    o.write(m.group(1))
                else:
                    # log_content = log_content + 'contig not found: ' + r
                    log_not_found = 'contig not found: ' + r

        if(log):
            log_content = '\nfatools\nlist items:\t'+str(lcounter)+'\nextracted contigs:\t'+str(excounter)+'\n'
            if log_not_found:
                log_content = log_content + '\nContigs not found:\n============================================\n'+log_not_found
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
            # check if list item is with '>' important to create pattern.
            if re.match('^>', r.strip()):
                pattern = '('+re.escape(r.strip())+'\n[A-Za-z\n]*)>'
            else:
                pattern = '(> '+re.escape(r.strip())+'\n[A-Za-z\n]*|>'+r.strip()+'\n[A-Za-z\n]*)>'

            if re.match(pattern, content):
                rem_counter = rem_counter + 1
            content = re.sub(pattern, '>', content)
        o.write(content)
    if(log):
        make_log('fatool - remContigs:\n list items:\t'+str(lcounter)+'\ncontings rmoved:\t'+str(rem_counter), log)
    else:
        print 'list items:\t'+str(lcounter)+'\ncontings rmoved:\t'+str(rem_counter)


def split_contigs(args):
    return 1


def statistics(args):
    return 1


if __name__ == '__main__':
    exit(main())
