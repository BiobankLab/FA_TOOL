# -*- coding: utf-8 -*-


import re
import math
from fatool import Sequence
import logging

class Fa(object):
    def __init__(self, contigs_list, name):
        logger = logging.getLogger(__name__)
        
        logger.debug('creating Fa object')
        self.name = name
        self.contigs = []
        self.contigs_idx = {}
        for r in contigs_list:
            if not isinstance(r, Sequence):
                logger.error('Supplied param is not Sequence object')
                raise TypeError('Wrong param supplied Sequence was expected')
            if not r.name in self.contigs_idx:
                if len(self.contigs) > 0:
                    logger.debug('appending contig: '+r.name)
                    self.contigs.append(r)
                else:
                    logger.debug('adding first contig: '+r.name)
                    self.contigs = [r]

                self.contigs_idx[r.name] = len(self.contigs) - 1
            else:
                logger.error('Sequence name: '+r.name+' already exists in file')
                raise NameError('Sequence name already exists: '+r.name)
            
            
    @staticmethod
    def load_from_file(file):
        if isinstance(file, str):
            with open(file, 'r') as f:
                contigs = Fa.load_content(f.read())
                name = file
        else:
            name = file.name
            with file as f:
                contigs = Fa.load_content(f.read() )
                
                
        return Fa(contigs, name)
            
    @staticmethod       
    def load_content(content):
        #print content
        nc = content.split('>')
        contigs_list = []
        for r in nc[1:]:
            contigs_list.append(Sequence('>'+r.split('\n', 1)[0], re.sub('^>.*\n', '', '>'+r.rstrip())))
        return contigs_list

    def write(self, fafile):
        if isinstance(fafile, str):
            with open(fafile, 'w') as f:
                f.write(str(self))
        else:
            with fafile as f:
                f.write(str(self))

    def write_multiple_files(self, dir):
        dir = dir.rstrip('/')
        dir = dir.rstrip('\\')
        if len(dir) > 0:
            dir = dir+'/'
        for r in self.contigs:
            with open(dir+r.name+'.fa', 'w') as w:
                w.write(str(r))

    def add_contigs(self, contig_list, owrite=0):
        for r in contig_list:
            self.add_contig(r, owrite)


    def add_contig(self, contig, owrite = 0):
        if not isinstance(contig, Sequence):
            raise TypeError('Wrong param supplied contig was expected')
        if contig.name in self.contigs_idx:
            if owrite == 1:
                #rem old item and add new name
                del self.contigs[self.contigs_idx[contig.name]]
                self.contigs.append(contig)
                for a, r in enumerate(self.contigs):
                    #print 'cnt '+str(r)
                    self.contigs_idx[r.name] = a
        else:
            self.contigs.append(contig)
            self.contigs_idx[contig.name] = len(self.contigs) - 1

    def show_names(self):
        return sorted(self.contigs_idx, key=self.contigs_idx.get)
        
    
    def extract(self, contigs_name_list):
        new_contig_list = []
        for r in contigs_name_list:
            if r in self.contigs_idx:
                new_contig_list.append(self.contigs[self.contigs_idx[r]])
        return Fa(new_contig_list, 'extr_'+self.name)

    def remove(self, contigs_name_list):
        new_contig_list = []
        for r in self.contigs:
            if not r.name in contigs_name_list:
                new_contig_list.append(r)
        return Fa(new_contig_list, 'rem_'+self.name)

    def validate(self):
        '''
        '''

    def nl_statistics(self, g, percent):
        '''
        Counts statistics of N50, L50, N75 etc.
        g array containing sorted contigs by length, from biggest to lowest
        '''
        ncount = -1 # index & number of contigs with +1
        nsum = 0
        stop = math.floor(self.stats['L']*(percent/100.00))
        while nsum < stop:
            ncount += 1
            nsum += g[ncount]
            
        self.stats['N'+str(percent)] = g[ncount]
        self.stats['L'+str(percent)] = ncount + 1

    def bp_stats(self, length):
        self.stats['totalc'] += 1
        if length > 50000:
            self.stats['nbp50000'] += 1  # number of contigs with length
            self.stats['lbp50000'] += length  # total length of contigs with min. len
        elif length > 25000:
            self.stats['nbp25000'] += 1
            self.stats['lbp25000'] += length
        elif length > 10000:
            self.stats['nbp10000'] += 1
            self.stats['lbp10000'] += length
        elif length > 5000:
            self.stats['nbp5000'] += 1
            self.stats['lbp5000'] += length
        elif length > 1000:
            self.stats['nbp1000'] += 1
            self.stats['lbp1000'] += length
        
    def statistics(self):
        self.stats = {
            'A': 0, 'C': 0, 'T': 0, 'G': 0, 'N': 0, 'L': 0,
            'nbp1000': 0, 'nbp5000': 0, 'nbp10000': 0, 'nbp25000': 0, 'nbp50000': 0,
            'lbp1000': 0, 'lbp5000': 0, 'lbp10000': 0, 'lbp25000': 0, 'lbp50000': 0,
            'totalc':0
        }
        nstat_list = []
        bp_stats = []
        for r in self.contigs:
            temp = r.statistics()
            self.stats['A'] += temp['A']
            self.stats['C'] += temp['C']
            self.stats['T'] += temp['T']
            self.stats['G'] += temp['G']
            self.stats['N'] += temp['N']
            self.stats['L'] += temp['L']
            nstat_list.append(temp['L'])
            self.bp_stats(temp['L'])

        self.stats['longest'] = max(nstat_list)
        nstat_list.sort()
        nstat_list.reverse()

        self.nl_statistics(nstat_list, 50)
        self.nl_statistics(nstat_list, 75)
        self.nl_statistics(nstat_list, 90)
        
        #print self.stats
        
        return self.stats

    def sort(self, mono):
        contig_list = []
        temp = {}  # dict to store name:len(contig)
        for r in self.contigs:
            temp[r.name] = len(r)

        if mono == -1:
            for r in sorted(temp, key=temp.get)[::-1]:
                contig_list.append(self.contigs[self.contigs_idx[r]])
        else:
            for r in sorted(temp, key=temp.get):
                contig_list.append(self.contigs[self.contigs_idx[r]])

        return Fa(contig_list, 'sorted_'+self.name)
    
    def reverse():
        cl = []
        for r in self.contigs:
            cl.append(r.reverse)
        return Fa(cl, 'rev_'+self.name)
    
    def join(self, fa_list, owrite = 0):
        for fa in fa_list:
            if not isinstance(fa, Fa):
                raise TypeError('Wrong param supplied Fa was expected')
            self.add_contigs(fa.contigs, owrite)
            
    def count_contigs(self):
        return len(self.contigs)

    def __str__(self):
        return_string = ''
        for r in self.contigs:
            return_string += str(r)
        return return_string
