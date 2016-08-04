# -*- coding: utf-8 -*-


import sys
import argparse
import re
import datetime
from string import maketrans
from fatool import *
from decimal import *
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    #logger.setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser()
    #parser.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    parser.add_argument('-v', '--version', help='display version number and exit', action='version', version='%(prog)s 0.3.1')
    subparsers = parser.add_subparsers(title='fatool commands', help='each has own params, for more details use: command -h')

    sub_cut = subparsers.add_parser('cut', help='split supplied sequence into smaller parts, according to given params')
    sub_cut.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_cut.add_argument('-r', '--range', help='cutted sequence length', type=int, required=True)
    sub_cut.add_argument('-o', '--output', help='output file default: output.fa', type=argparse.FileType('w'), default='output.fa')
    sub_cut.add_argument('-s', '--step', help='step length default: 1', type=int, default=1)
    sub_cut.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_cut.add_argument('--operator', help='user who have fired script it will be noted in report', type=str)
    sub_cut.set_defaults(func=cut_fa)

    sub_en = subparsers.add_parser('extractNames', help='extracting contigs names only')
    sub_en.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_en.add_argument('-o', '--output', help='output file if not supplied stdout', type=argparse.FileType('w'))
    sub_en.add_argument('--report', help='report results into  file if not supplied stdout', type=argparse.FileType('w'))
    sub_en.add_argument('--operator', help='user who have fired script it will be noted in report', type=str)
    sub_en.set_defaults(func=extract_names)

    sub_ec = subparsers.add_parser('extractContigs', help='extracting contigs specified in file (output in new file)')
    sub_ec.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_ec.add_argument('--list', help='file containing list of contigs one contig per line', type=argparse.FileType('r'), required=True)
    sub_ec.add_argument('-o', '--output', help='output file; if --multifile is set output directory', type=str, required=True)
    sub_ec.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_ec.add_argument('--operator', help='user who have fired script it will be noted in report', type=str)
    sub_ec.add_argument('--multifile', help='if this flag is set each contig will be saved in separate file', action='store_true')
    sub_ec.set_defaults(func=extract_contigs)

    sub_rc = subparsers.add_parser('remContigs', help='removing contigs specified in file (output in new file)')
    sub_rc.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_rc.add_argument('--list', help='file containing list of contigs one contig per line', type=argparse.FileType('r'), required=True)
    sub_rc.add_argument('-o', '--output', help='output file if not supplied stdout', type=str, required=True)
    sub_rc.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_rc.add_argument('--operator', help='user who have fired script it will be noted in report', type=str)
    sub_rc.set_defaults(func=remove_contigs)
    
    sub_jc = subparsers.add_parser('join', help='joining two or more files, yet not verifing duplicates')
    sub_jc.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_jc.add_argument('-o', '--output', help='output file if not supplied stdout', type=argparse.FileType('w'), required=True)
    sub_jc.add_argument('--files', help='files to be joined', nargs='*', type=argparse.FileType('r'))
    sub_jc.add_argument('--overwrite', help='if set owerwrites contigs with same name', action='store_true')
    sub_jc.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_jc.add_argument('--operator', help='user who have fired script it will be noted in report', type=str)
    sub_jc.set_defaults(func=join)
    
    sub_sc = subparsers.add_parser('split', help='each cotig saved into separate file')
    sub_sc.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_sc.add_argument('-d', '--outputDir', help='output directory where splited contigs will be saved', type=str, required=True)
    sub_sc.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_sc.add_argument('--operator', help='user who have fired script it will be noted in report', type=str)
    sub_sc.set_defaults(func=split_contigs)
    
    sub_r = subparsers.add_parser('reverse', help='reverse all sequences in file')
    sub_r.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_r.add_argument('-o', '--output', help='output file; if --multifile is set output directory', type=argparse.FileType('w'), required=True)
    sub_r.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_r.add_argument('--operator', help='user who have fired script it will be noted in report', type=str)
    sub_r.set_defaults(func=reverse)
    
    sub_v  = subparsers.add_parser('validate', help='validates fa file')
    sub_v.add_argument('-f', '--fafile', help='file to be cut usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_v.add_argument('-t', '--type', help='type of sequence 0 - general, 1 DNA, 2 - amino', type=int, required=True)
    sub_v.add_argument('--details', help='set if you want to see detaild validation info', action='store_true')
    sub_v.set_defaults(func=validate)
    
    sub_s  = subparsers.add_parser('stats', help='show statistics of fa file')
    sub_s.add_argument('-f', '--fafile', help='file to show statistics usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_s.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_s.add_argument('--operator', help='user who have fired script it will be noted in report', nargs='*', type=str)
    sub_s.set_defaults(func=statistics)
    '''
    sub_fm  = subparsers.add_parser('findMotif', help='display motifs position in contig')
    sub_fm.add_argument('-f', '--fafile', help='file to show statistics usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_fm.add_argument('--mml', help='mismatch level number of allowed missmatches in primers (detfault 0)', type=str, default=0)
    sub_fm.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_fm.add_argument('--operator', help='user who have fired script it will be noted in report', nargs='*', type=str)
    sub_fm.set_defaults(func=find_motif)
    '''
    sub_fp  = subparsers.add_parser('findPrimer', help='display list of founded primers')
    sub_fp.add_argument('-f', '--fafile', help='file to show statistics usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_fp.add_argument('--start', help='strat codon 5\'', type=str, required=True)
    sub_fp.add_argument('--stop', help='stop codon 3\'', type=str, required=True)
    sub_fp.add_argument('--mode', help='FF (start forward, stop forward) or FR (start 5\' stop 3\')', type=str, choices=['FF', 'FR'], default = 'FR', required=True)
    sub_fp.add_argument('--minlen', help='minimum length (detfault 50bp)', type=int, default=50)
    sub_fp.add_argument('--maxlen', help='max length (detfault 1000bp)', type=int, default=1000)
    sub_fp.add_argument('--mml', help='mismatch level number of allowed missmatches in primers (detfault 0)', type=int, default=0)
    sub_fp.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_fp.add_argument('--operator', help='user who have fired script it will be noted in report', nargs='*', type=str)
    sub_fp.set_defaults(func=find_primers)
    
    sub_cn = subparsers.add_parser('cutName', help='cuts name from position to given length')
    sub_cn.add_argument('-f', '--fafile', help='file to show statistics usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_cn.add_argument('--start', help='start of cut', type=int, required=True)
    sub_cn.add_argument('-l', '--length', help='length of cut', type=int, required=True)
    sub_cn.set_defaults(func=cut_name)
    
    sub_lnam = subparsers.add_parser('cutNameMarker', help='cuts name leaving defined number of chars after begining of marker')
    sub_lnam.add_argument('-f', '--fafile', help='file to show statistics usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_lnam.add_argument('-m', '--marker', help='marker that indicates start of cut', type=str, required=True)
    sub_lnam.add_argument('-l', '--length', help='length of cut', type=int, required=True)
    sub_lnam.add_argument('--keepMarker', help='weather to keep marker or not default 1 (Yes)', type=int, required=True)
    sub_lnam.add_argument('-o', '--output', help='output file default: output.fa', type=argparse.FileType('w'), default='output.fa')
    #sub_lnam.add_argument('-d', '--outputDir', help='output directory where multiple contigs will be saved', type=str)
    sub_lnam.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_lnam.add_argument('--operator', help='user who have fired script it will be noted in report', nargs='*', type=str)
    sub_lnam.set_defaults(func=cut_name_pattern)
    
    sub_trn_d2p = subparsers.add_parser('translateDNA2Proteins', help='display translation to proteins')
    sub_trn_d2p.add_argument('-f', '--fafile', help='file to show statistics usualy *.fa', type=argparse.FileType('r'), required=True)
    sub_trn_d2p.add_argument('-o', '--output', help='output file default: output.fa', type=argparse.FileType('w'), default='output.fa')
    sub_trn_d2p.add_argument('--startCodons', help='list of start codons separated by space bar', nargs='*', type=str)
    sub_trn_d2p.add_argument('--stopCodons', help='list of stop codons separated by space bar', nargs='*', type=str)
    sub_trn_d2p.add_argument(
        '--tdict', help='Which dictionary use for translation: STD - standard, VMTO - Vertebrate Mitochondrial, YMTO - Yeast Mitochondrial, BAPP - Bacterial Archaeal Plant and Plastid', 
        type=str, choices=['STD', 'VMTO', 'YMTO', 'BAPP'], default = 'STD'
    )
    sub_trn_d2p.add_argument('--nss', help='No Start Stop', action='store_true')
    sub_trn_d2p.add_argument('--report', help='report results into file if not supplied stdout', type=argparse.FileType('w'))
    sub_trn_d2p.add_argument('--operator', help='user who have fired script it will be noted in report', nargs='*', type=str)
    sub_trn_d2p.set_defaults(func=translate_dna_to_protein)

    args = parser.parse_args()
    
        
    args.func(args)
    
def resolve_operator(operator_arg_list):
    # makes prity print of opoerator
    op = ''
    for r in operator_arg_list:
        op += r+' '
    return op.rstrip()
    
def make_log_header(cmd, op):
    stats_rep = '\n-------------------------------------------------------------'
    stats_rep +='\ncmdfatool '+str(cmd)+' \n\nstarted:\t'+str(datetime.datetime.now())
    if op:
        stats_rep += '\nOperator:\t'+resolve_operator(op)
    stats_rep += '\n-------------------------------------------------------------\n'
    return stats_rep
    
    
def cut_fa(args):
    #logging.basicConfig(level=logging.ERROR)
    #logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    logger.setLevel(logging.DEBUG)
    logger.debug('debug mode started')
    logger.info('command: cut starting')
    rep = str(make_log_header('cut', args.operator))
    
    fafile = args.fafile
    output = args.output
    split_range = args.range
    step = args.step
    
    f = Fa.load_from_file(fafile)
    logger.info('file: '+fafile.name+' loaded')
    contig_list = []
    for r in f.contigs:
        contig_list += r.cut(split_range, step)
        logger.info('cutted contigs added from conting: '+r.name)
    result_fa = Fa(contig_list, 'splited')
    logger.info('trying to write file')
    result_fa.write(output)
    logger.info('file written')
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(rep)
    
    
def extract_names(args):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info('command: extractNames starting')
    rep = str(make_log_header('extractNames', args.operator))
    fafile = args.fafile
    output = args.output
    
    fa = Fa.load_from_file(fafile)
    names = fa.show_names()
    with output as o:
        for r in names:
            o.write(r+'\n')
    rep += 'Number of neames founded:\t' + str(len(names))
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(rep)

def extract_contigs(args):
    # default all extracted contigs in one file
    # with flag multifile save each contig to separate file
    
    rep = str(make_log_header('extractContigs', args.operator))
    
    fa = Fa.load_from_file(args.fafile)
    rep += 'Number of contigs in orginal file:\t'+str(len(fa.contigs))
    
    #file with contigs names one per line
    with args.list as cntgs:
       elist = [c.strip() for c in cntgs]
    result_fa = fa.extract(elist)
    if( args.multifile):
        result_fa.write_multiple_files(args.output)
    else:
        result_fa.write(args.output)
    rep += '\nContigs to remove:\t'+str(len(elist))
    rep += '\Extracted contigs:\t'+str(len(result_fa.contigs))
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(rep)
    else:
        print rep

def remove_contigs(args):
    # contigs from list are removed, others saved to file
    rep = str(make_log_header('remContigs', args.operator))
    fa = Fa.load_from_file(args.fafile)
    rep += 'Number of contigs in orginal file:\t'+str(len(fa.contigs))
    # file that contains list of contigs one per line
    with args.list as cntgs:
        rlist = [c.strip() for c in cntgs]
    rep += 'Number of contigs to remove:\t'+len(rlist)
    result_fa = fa.remove(rlist)
    rep += 'Number of contigs after remove:\t'+str(len(fa.contigs))
    rep += 'Contigs removed:\t'+str(len(fa.contigs) - len(result_fa.contigs))
    result_fa.write(args.output)
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(stats_rep)
    else:
        print stats_rep
    
    
def join(args):
    # joins contig from multiple files
    rep = str(make_log_header('join', args.operator))
    fa = Fa.load_from_file(args.fafile)
    fa_list = []
    contigs_to_add = 0
    #  list of Fa files to join.
    for r in args.files:
        if len(r) > 0:
            fa2add = Fa.load_from_file(r)
            fa_list.append(fa2add)
            contigs_to_add += fa2add.count_contigs()
    rep += '\nOrginal contigs number:\t'+Fa.count_contigs()
    rep += '\nTotal files to join with orginal file:\t'+len(args.files)
    rep += '\nTotal contigs to add:\t'+str(contigs_to_add)
    fa.join(fa_list, args.overwrite)
    rep += '\nNumber of contigs after join:\t'+str(fa.count_contigs())
    fa.write(args.output)
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(stats_rep)
    else:
        print stats_rep
    
def split_contigs(args):
    #writes each contig in single file
    rep = str(make_log_header('split', args.operator))
    fa = Fa.load_from_file(args.fafile)
    fa.write_multiple_files(args.output)
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(rep)
    else:
        print rep
    

def statistics(args):
    #  returns statistics of fa file
    stats_rep = str(make_log_header('stats', args.operator))
    fa = Fa.load_from_file(args.fafile)
    stats = fa.statistics()
    stats_rep += '\n\nNumber of N:\t'+str(stats['N'])
    stats_rep += '\nNumber of A:\t'+str(stats['A'])
    stats_rep += '\nNumber of C:\t'+str(stats['C'])
    stats_rep += '\nNumber of T:\t'+str(stats['T'])
    stats_rep += '\nNumber of G:\t'+str(stats['G'])
    getcontext().rounding = ROUND_05UP
    getcontext().prec = 4
    stats_rep += '\nGC[%] (0.5 up):\t'+str(Decimal(stats['G']+stats['C'])/stats['L']*Decimal(100.00))
    stats_rep += '\n\nTotal length:\t'+str(stats['L'])
    stats_rep += '\nTotal contigs:\t'+str(stats['totalc'])
    stats_rep += '\n\ncontigs 1000-5000bp:\t'+str(stats['nbp1000'])
    stats_rep += '\ncontigs 1000-5000bp length:\t'+str(stats['lbp1000'])
    stats_rep += '\ncontigs 5001-10000bp:\t'+str(stats['nbp5000'])
    stats_rep += '\ncontigs 5001-10000bp length:\t'+str(stats['lbp5000'])
    stats_rep += '\ncontigs 10001-25000bp:\t'+str(stats['nbp10000'])
    stats_rep += '\ncontigs 10001-25000bp length:\t'+str(stats['lbp10000'])
    stats_rep += '\ncontigs 25001-50000bp:\t'+str(stats['nbp25000'])
    stats_rep += '\ncontigs 25001-50000bp length:\t'+str(stats['lbp25000'])
    stats_rep += '\ncontigs 50001+bp:\t'+str(stats['nbp50000'])
    stats_rep += '\ncontigs 50001+bp length:\t'+str(stats['lbp50000'])
    stats_rep += '\n\ncontigs > 1000bp:\t'+str(stats['nbp1000']+stats['nbp5000']+stats['nbp10000']+stats['nbp25000']+stats['nbp50000'])
    stats_rep += '\ncontigs > 1000bp length:\t'+str(stats['lbp1000']+stats['lbp5000']+stats['lbp10000']+stats['lbp25000']+stats['nbp50000'])
    stats_rep += '\ncontigs > 5000bp:\t'+str(stats['nbp5000']+stats['nbp10000']+stats['nbp25000']+stats['nbp50000'])
    stats_rep += '\ncontigs > 5000bp length:\t'+str(stats['lbp5000']+stats['lbp10000']+stats['lbp25000']+stats['nbp50000'])
    stats_rep += '\ncontigs > 10000bp:\t'+str(stats['nbp10000']+stats['nbp25000']+stats['nbp50000'])
    stats_rep += '\ncontigs > 10000bp length:\t'+str(stats['lbp10000']+stats['lbp25000']+stats['nbp50000'])
    stats_rep += '\ncontigs > 25000bp:\t'+str(stats['nbp25000']+stats['nbp50000'])
    stats_rep += '\ncontigs > 25000bp length:\t'+str(stats['lbp25000']+stats['nbp50000'])
    stats_rep += '\ncontigs > 50000bp:\t'+str(stats['nbp50000'])
    stats_rep += '\ncontigs > 50000bp length:\t'+str(stats['nbp50000'])
    stats_rep += '\nLongest contig:\t'+str(stats['longest'])
    stats_rep += '\n\nN50:\t'+str(stats['N50'])
    stats_rep += '\nL50:\t'+str(stats['L50'])
    stats_rep += '\nN75:\t'+str(stats['N75'])
    stats_rep += '\nL75:\t'+str(stats['L75'])
    stats_rep += '\nN90:\t'+str(stats['N90'])
    stats_rep += '\nL90:\t'+str(stats['L90'])
    stats_rep += '\n\n------------------------------------------------------'
    stats_rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(stats_rep)
    else:
        print stats_rep
    

def validate(args):
    # check if fa is valid
    rep = str(make_log_header('validate', args.operator))
    fa = Fa.load_from_file(args.fafile)
    result_list = {}
    if args.details:
        for r in fa.contigs:
            result_list[r.name] = Sequence.detailed_validate_generic(r, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]')
    else:
        for r in fa.contigs:
            result_list[r.name] = Sequence.validate_generic(r, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]')
    #print result_list
    
    for r in result_list:
        rep += r +'\n'
    
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(rep)
    else:
        print rep
            

def reverse(args):
    rep = str(make_log_header('reverse', args.operator))
    fa = Fa.load_from_file(args.fafile)
    fa.reverse()
    fa.write(args.output)
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(rep)
    else:
        print rep
        

def find_motif(args):
    print 'not available yet'
    pass

def find_primers(args):
    rep = str(make_log_header('reverse', args.operator))
    fa = Fa.load_from_file(args.fafile)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug(args)
    rep = ''
    for r in fa.contigs:
        rep += '\n================\n\t\t'+r.name+'\n'
        for q in r.find_aprox_primers(args.start, args.stop, str(args.mode), int(args.mml), args.minlen, args.maxlen):
            rep += q+'\n'
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(rep)
    else:
        print rep
        
def cut_name_pattern(args):
    rep = str(make_log_header('cutNameMarker', args.operator))
    fa = Fa.load_from_file(args.fafile)
    for r in fa.contigs:
        r.leave_name_after_marker(args.marker, args.length, args.keepMarker)
    fa.write(args.output)

def print_frame_output(r_dict):
    i = 0
    otp = ''
    for f in r_dict:
        otp += 'FRAME:\t'+str(i+1)+'\n'
        otp += '\nBEFORE:\t '+f[0]
        otp += '\nTRANSLATION:\n\n'+f[1]
        otp += '\n\nAFTER:\t '+f[2]
        otp += '\n------------------------------------------------\n'
        i+=1
    return otp
    
def translate_dna_to_protein(args):
    rep = str(make_log_header('translate2protein', args.operator))
    fa = Fa.load_from_file(args.fafile)
    if args.tdict == 'STD':
        tdict = Sequence.tdict_standard
    elif args.tdict == 'VMTO':
        tdict = Sequence.tdict_vertebrate_mitochondrial
    elif args.tdict == 'YMTO':
        tdict = Sequence.tdict_yeast_mitochondrial
    elif args.tdict == '????????':
        tdict = Sequence.tdict_standard
    elif args.tdict == 'BAPP':
        tdict = Sequence.tdict_bacterial_archaeal_plant_plastid
    else:
        print 'applied dictionary is not valid!'
        exit(1)
        
    r_dict = {}
    otp = ''
    if args.nss:
        for r in fa.contigs:
            r_dict = r.translate2protein(tdict)
            otp += '\n=============================\n'+r.name+'\n=============================\n'
            otp += '\nFORWARD\n\n'
            otp += print_frame_output(r_dict['fwd'])
            otp += '\n'+'='*15+'\n'
            otp += '\nREVERS\n\n'
            otp += print_frame_output(r_dict['rev'])
        rep += otp
                
    else:
        for r in fa.contigs:
        
            r_dict = r.translate2protein_in_range(args.startCodons, args.stopCodons, tdict)
            otp += '\n=============================\n'+r.name+'\n=============================\n'
            otp += 'FORWARD\n\n'
            i = 0
            
            for f in r_dict['fwd']:
                otp += 'FRAME:\t'+str(i+1)+'\n'
                for k in f:
                    otp += '\n'+k[0]+' start: '+str(k[1])
                    otp += '\n------------------------------------------------\n'
                otp += '\n'+'='*15+'\n'
                i += 1
            otp += 'REVERS\n\n'
            i = 0
            for f in r_dict['rev']:
                otp += 'FRAME:\t'+str(i+1)+'\n'
                for k in f:
                    otp += '\n'+k[0]+' start: '+str(k[1])
                    otp += '\n------------------------------------------------\n'
                i += 1
        rep += otp
    
    fa.write(args.output)
    rep += '\n\n------------------------------------------------------'
    rep += '\nFinished:\t'+str(datetime.datetime.now())
    if args.report:
        with args.report as log_file:
            log_file.write(rep)
    else:
        print rep
    
def cut_name(args):
    pass

        
if __name__ == '__main__':
    exit(main())
    
    
    
       
        
        
