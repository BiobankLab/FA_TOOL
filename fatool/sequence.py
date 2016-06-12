# -*- coding: utf-8 -*-

from string import maketrans
from collections import Counter
import fuzzy
import re


class Sequence(object):
    def __init__(self, name, seq):
        if Sequence.validate_name_string(name):
            self.name = name.lstrip('>')
        else:
            raise NameError('Sequence name have to start with ">"') 
        self.seq = seq
        #self.quality = quality

    # def is_valid(self):

    # def validate_name(self):
        
        
    @staticmethod
    def validate_name_string(nstr):
        if re.search('^>', nstr):
            return 1

    def validate_seq(self):
        '''
        validates general seqence not specified for DNA or others.
        '''
        # pattern to find not allowed chars.
        pattern = re.compile('[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]')
        if pattern.search(self.seq):
            if re.search('(\d+)', self.seq):
                seq_array = self.seq.split('\n')
                new_array = []  # array to store new sequence
                for r in seq_array:
                    r = r.lstrip()  # removing ' ' from beginings and ends
                    nr = r.split(' ')  # split to array to catch all blocks aaaaaaaaaa aaaaaaaaaa
                    new_array.append(nr)
                
                end_of_seq_array = len(seq_array)
                # if min. two lines calculate expected line length
                if end_of_seq_array > 1:
                    line_length = int(new_array[1][0])-int(new_array[0][0])

                # validate ecah block (between " ") of sequence ()
                i = 0
                while i < end_of_seq_array:
                    if not re.search('(\d+)', new_array[i][0]):
                        return 7  # line doesn't starts with digit
                    if not (len(new_array[i])-1)*10 == line_length and i != (end_of_seq_array-1):
                        return 0 # bad line length
                    for a, r in enumerate(new_array[i][1:]):  # skip first elem which is digit
                        if len(r) != 10:  # block not eq 10
                            if len(r) < 10:  # if less it can be ok if last elem of last line
                                if(i == end_of_seq_array - 1):
                                    if a != len(new_array[i]) - 2:  # if last -2 because enumerate is from first elem not 0 elem.
                                        return 0  # not last elem of last line
                                else:
                                    return 0  # not last line
                            else:
                                return 0  # block not eq 10
                        if pattern.search(r):
                            return 0
                    i += 1
            else:
                return 0  # digit is not first char
            # return pattern.search(self.seq) but nan error code returned before
            return 1
        return 1  # valid
    
    @staticmethod
    def generic_validate(seq, domain):
        # pattern created from passed domain (domain contains chars that are not allowed)
        pattern = re.compile(domain) #'[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'
        # if sequence contains illegal chars
        if pattern.search(seq):
            # if digits it can be ok if format like (60 xxxxxxxxxx xxx...)
            if re.search('(\d+)', seq):
                # to check that we have to transform array
                seq_array = seq.split('\n')
                new_array = []  # array to store new sequence as array of arrays
                for r in seq_array:
                    r = r.lstrip()  # removing ' ' from beginings and ends
                    nr = r.split(' ')  # split to array to catch all blocks aaaaaaaaaa aaaaaaaaaa
                    new_array.append(nr)
                
                end_of_seq_array = len(seq_array)
                # if min. two lines calculate expected line length
                if end_of_seq_array > 1:
                    line_length = int(new_array[1][0])-int(new_array[0][0])

                # validate ecah block (between " " [space]) of given sequence
                i = 0
                while i < end_of_seq_array:
                    if not re.search('(\d+)', new_array[i][0]):
                        return 7  # line doesn't starts with digit
                    if not (len(new_array[i])-1)*10 == line_length and i != (end_of_seq_array-1):
                        return 0 # bad line length
                    for a, r in enumerate(new_array[i][1:]):  # skip first elem which is digit
                        if len(r) != 10:  # block not eq 10
                            if len(r) < 10:  # if less it can be ok if last elem of last line
                                if(i == end_of_seq_array - 1):
                                    if a != len(new_array[i]) - 2:  # if last -2 because enumerate is from first elem not 0 elem.
                                        return 0  # not last elem of last line
                                else:
                                    return 0  # not last line
                            else:
                                return 0  # block not eq 10
                        if pattern.search(r):
                            return 0
                    i += 1
            else:
                return 0  # digit is not first char
            # return pattern.search(seq) but nan error code returned before
            return 1
        return 1  # valid
    
    # def validate_dna_seq(self):

    # def validate_other_seq(self):
    
    @staticmethod
    def detailed_validate_generic(seq, domain):
        not_valid = 0
        missmatches = {}
        # pattern created from passed domain (domain contains chars that are not allowed)
        pattern = re.compile(domain)
        # find not allowed chars in sequence
        m = pattern.finditer(seq)
        log_info = []
        # if not allowed chars found
        if m:
            # it may be 60 xxxxxxxxxx xxx.... format
            if re.search('(\d+)', seq):
                seq_array = seq.split('\n')
                new_array = []  # array to store new sequence after cleaning and transformation
                for r in seq_array:
                    r = r.lstrip()  # removing ' ' from beginings and ends
                    nr = r.split(' ')  # split to array to catch all blocks aaaaaaaaaa aaaaaaaaaa
                    new_array.append(nr)
                end_of_seq_array = len(seq_array)
                # if min. two lines calculate expected line length
                if end_of_seq_array > 1:
                    line_length = int(new_array[1][0])-int(new_array[0][0])

                # validate ecah block (between " " [space]) of given sequence
                i = 0
                while i < end_of_seq_array:
                    # digit on begining of line was not found - error
                    if not re.search('(\d+)', new_array[i][0]):
                        log_info.append('line '+str(i+1)+": line doesn't starts with digit")  # line doesn't starts with digit
                    # check if line length = expected line length last line can be shorter
                    if not (len(new_array[i])-1)*10 == line_length and i != (end_of_seq_array-1):
                        #return 0 # bad line length
                        log_info.append('line '+str(i+1)+': bad line length')
                    #chcek all blocks if are eq 10 (last can be shorter)
                    for a, r in enumerate(new_array[i][1:]):  # skip first elem which is digit
                        if len(r) != 10:  # block not eq 10
                            if len(r) < 10:  # if less it can be ok if last elem of last line
                                if(i == end_of_seq_array - 1):
                                    if a != len(new_array[i]) - 2:  # if last -2 because enumerate is from first elem not 0 elem.
                                        log_info.append('line '+str(i+1)+': block '+str(a+1)+' contains les then 10 chars')  # not last elem of last line
                                else:
                                    log_info.append('line '+str(i+1)+': block '+str(a+1)+' contains les then 10 chars') # not last line
                            else:
                                log_info.append('line '+str(i+1)+': block '+str(a+1)+' contains more then 10 chars')  # block gt 10
                        # if block contains illegal chars now after transtrmation it should contain only legal chars.
                        if pattern.search(r):
                            log_info.append('line '+str(i+1)+': block '+str(a+1)+' contains illegal chars')
                    i += 1
            else:
            # in this case it is not seq like "10 xxxxx xxxxx"
                for mitem in m:
                    log_info.append('Position:\t'+str(mitem.start())+'\tvalue:\t'+str(mitem.group()))
        # none of not allowed chars were found sequence OK
        return log_info
    # def detailed_validate_dna_seq(self):

    # def detailed_validate_other_seq(self):

    def cut(self, length, step):
        '''
        cutting contig into smaller parts accordigly to supplied params
        length of contig (number of chars)
        step offset between current and next start
        '''
        self.normalize()
        i = 0
        contig_end = len(self.seq)  # last position of contig
        contig_list = []  # contig list returning by function
        while i+length <= contig_end:
            contig_list.append(Sequence('>'+self.name+'_frag_'+str(i + 1)+':'+str(i + length), str(self.seq[i:i+length])))
            i = i+step
        return contig_list

    def reverse(self):
        '''
        creates reversed sequence
        '''
        self.normalize()
        nr = re.sub('\n', '', self.seq)
        rev = nr[::-1]
        rev = rev.translate(maketrans('ACTGactg', 'TGACtgac'))
        # creating 80 chars lines
        #rev = re.sub("(.{80})", '\\1\n', rev, 0)
        return Sequence('>rev_'+self.name, rev)


    def normalize(self):
        self.seq = re.sub(' ', '', self.seq)
        self.seq = re.sub('^\d', '', self.seq, re.M)
        self.seq = re.sub('\n', '', self.seq)

    def statistics(self):
        '''
        returns simple statistics for contig
        '''
        self.normalize()
        r = {}
        c = Counter(self.seq)
        r['A'] = c['A']+c['a']
        r['C'] = c['C']+c['c']
        r['G'] = c['G']+c['g']
        r['T'] = c['T']+c['t']
        r['N'] = c['N']+c['n']
        r['L'] = len(self.seq)
        return r
    
    #def getRange(self, start, stop):
    #    return self.seq[start:stop]
    
    def translate_dna2rna(self):
        nc = self.seq.translate(maketrans('ACTGactg', 'UGACugac'))
        return Sequence('>rna_'+self.name, nc)
        
    def translate_rna2dna(self):
        nc = self.seq.translate(maketrans('UGACugac', 'ACTGactg'))
        return Sequence('>dna_'+self.name, nc)
    
    # ctrl f1 frame 1 forward, r1 frame 1 revers, fall torward all frames, rall reverse all frames, all in this way?
    # supply dict of translation or its constant?
    @staticmethod
    def translate2protein_in_range_generic(seq, start, stop, tdict):
        p = ''
        p_stop = ''
        # search results in distribution to frames
        frame1 = []
        frame2 = []
        frame3 = []
        
        # creating pattern to find start codons
        for r in start:
            p +=  r+'|'
        p = '('+p.rstrip('|')+')'
        
        # creating pattern to find stop codons
        for r in stop:
            p_stop +=  r+'|'
        p_stop = '('+p.rstrip('|')+')'
        
        # match for start contigs
        m = re.finditer(p, seq)
        
        # there will be stored latest string position for each frame
        frame_iterator[0,0,0]
        
        stop_pos = len(seq) # where to stop searching if no stopcodon found
        
        # using each found start codon
        for r in m:     
            # if start is lower then last used position skip it.
            if frame_iterator[r.start()%3] <= r.start():
                # set i for start position of current start contig
                i = r.start()
                ret = ''
                while i+3 <= stop:
                    ret += Sequence.translate(seq[i:i+3], tdict)
                    if re.match(p_stop, seq[i:i+3]):
                        i = i+3
                        break
                    else:
                        i = i+3
                
                frame_iterator[r.start()%3] = i
                if r.start()%3 == 0:
                    frame1.append((ret,r.start(),i,str(r.start()/3+1),str(i-r.start())))
                elif r.start()%3 == 1:
                    frame2.append((ret,r.start(),i,str(r.start()/3+1),str(i-r.start())))
                elif r.start()%3 == 2:
                    frame3.append((ret,r.start(),i,str(r.start()/3+1),str(i-r.start())))
                    
        return [frame1, frame2, frame3]
        
    @staticmethod
    def translate2protein_generic(seq, tdict):
        # +5 to secure all frames
        f1 = ''
        f2 = ''
        f3 = ''
        while i+5 < len(seq):
            f1 += Sequence.translate(seq[i:i+3], tdict)
            f2 += Sequence.translate(seq[i+1:i+4], tdict)
            f3 += Sequence.translate(seq[i+2:i+5], tdict)
            
        return [('',f1,seq[-2:]),(seq[0:1],f2,seq[-1:]),(seq[0:2],f2,)]
    
    def translate2protein(self, tdict):
        tdict = {
            'GCA':'A','GCC':'A','GCG':'A','GCT':'A', 'TGC':'C','TGT':'C', 'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
            'TTC':'F', 'TTT':'F', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 'CAC':'H', 'CAT':'H', 'ATA':'I', 'ATC':'I', 'ATT':'I',
            'AAA':'K', 'AAG':'K', 'TTA':'L', 'TTG':'L', 'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'ATG':'M', 'AAC':'N', 'AAT':'N',
            'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 'CAA':'Q', 'CAG':'Q', 'AGA':'R', 'AGG':'R', 'CGA':'R', 'CGC':'R', 'CGG':'R', 
            'CGT':'R', 'AGC':'S', 'AGT':'S', 'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
            'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'TGG':'W', 'TAC':'Y', 'TAT':'Y', 'TAG': '*', 'TGA':'*', 'TAA':'*'
        }
        f = Sequence.translate2protein_generic(self.seq, tdict)
        r = Sequence.translate2protein_generic(self.reverse().seq, tdict)
        return {'fwd':f, 'rev':r}
    
    @staticmethod
    def translate(contig, tdict):
        if codon in tdict:
            return tdict[codon]
        else:
            return '|'+codon+'|'

    def find_aprox_motif(self, motif, missmatch_level):
        self.normalize()
        return fuzzy.find_all_motifs(motif, self.seq, missmatch_level, hs_start_pos = 0)
        
    def find_aprox_primers(self, start, stop, missmatch_level = 0, len_min = 50, len_max = 10000):
        #start 5'->3'
        # add missmatch_level condition if 50%>
        rev = stop[::-1]
        new_stop = rev.translate(maketrans('ACTGactg', 'TGACtgac'))
        r_list = []
        self.normalize()
        #print '\nAfter normailzation'
        #print self.seq
        
        res = fuzzy.find_all_motifs_in_aprox_range(start, stop, self.seq, missmatch_level, 0, len_min, len_max)
        if res:
            r_list.extend(res)
        
        rev = start[::-1]
        new_start = rev.translate(maketrans('ACTGactg', 'TGACtgac'))
        #print 'new_seq in sequence\n'
        #print new_seq.seq
        res = fuzzy.find_all_motifs_in_aprox_range(new_start, stop, self.seq, missmatch_level, 0, len_min, len_max)
        if res:
            r_list.extend(res)
        print 'Sequence.find_aprox_primers',
        for s in r_list:
            print s+'\n'
        return r_list
        
    def __str__(self):
        '''
        creates nicely outputed string
        '''
        return '>'+self.name+'\n'+re.sub("(.{80})", '\\1\n', self.seq, 0)+'\n'


    def __len__(self):
        return len(self.seq)

    def __cmp__(self, other):
        if self.seq == other.seq:
            return 0
        
    def __eq__(self, other):
        return self.seq == other.seq