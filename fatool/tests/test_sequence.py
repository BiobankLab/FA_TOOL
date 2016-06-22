import unittest
import sys
from fatool import Sequence
from string import maketrans



class TestSequence(unittest.TestCase):
    def setUp(self):
        pass

    def test_setUpSequence(self):
        c = Sequence('>name', 'ACTGactg')
        self.assertTrue( isinstance(c, Sequence) )
        self.assertEqual(c.name, 'name')
        self.assertEqual(c.seq, 'ACTGactg')

    def test_contig_str(self):
        c = Sequence('>name', 'ACTGactg') 
        self.assertEqual(str(c), '>name\nACTGactg\n')

    def test_validate_name_string(self):
        c = Sequence('>name', 'ACTGactg')
        self.assertEqual(c.validate_name_string('>name'), 1)
        
        
    def test_generic_validation(self):
        self.assertEqual(Sequence.generic_validate('ACTGactg', '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 1)
        self.assertEqual(Sequence.generic_validate('ACTGactgee', '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 0)
        seq = '   1 ACTGactgAC aaatttccca ACTGactgaa aaatttccca\n   41 ACTGactgAA aaatttccca ACTGactgtt aaatttccca\n   81 ACTGactgGG aaatttccca ACTGactgcc aaatt'
        self.assertEqual(Sequence.generic_validate(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 1)
        # not allowed symbol e
        seq = '   1 ACTGactgAC aaatttccca ACTGactgee aaatttccca\n   41 ACTGactgAA aaatttccca ACTGactgtt aaatttccca\n   81 ACTGactgGG aaatttccca ACTGactgcc aaatt'
        self.assertEqual(Sequence.generic_validate(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 0)
        # not allowed symbol e + len <
        seq = '   1 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   51 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   81 ACTGactgee aaatttccca ACTGactgee aaatt'
        self.assertEqual(Sequence.generic_validate(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 0)
        
        # not allowed symbol e + len >
        seq = '   1 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   31 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   81 ACTGactgee aaatttccca ACTGactgee aaatt'
        self.assertEqual(Sequence.generic_validate(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 0)
        
        # len >
        seq = '   1 ACTGactgTT aaatttcc ACTGactgAa aaatttccca\n   31 ACTGactgcT aaatttccca ACTGactgCT aaatttccca\n   81 ACTGactgAg aaatttccca ACTGactggg aaatt'
        self.assertEqual(Sequence.generic_validate(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 0)
        
        # len <
        seq = '   1 ACTGactgTT aaatttcc ACTGactgAa aaatttccca\n   51 ACTGactgcT aaatttccca ACTGactgCT aaatttccca\n   81 ACTGactgAg aaatttccca ACTGactggg aaatt'
        self.assertEqual(Sequence.generic_validate(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 0)
        
        # last len >
        seq = '   1 ACTGactgTT aaatttcc ACTGactgAa aaatttccca\n   51 ACTGactgcT aaatttccca ACTGactgCT aaatttccca\n   81 ACTGactgAg aaatttccca ACTGactggg aaattaaattaaatt'
        self.assertEqual(Sequence.generic_validate(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 0)
        
        # last bad symbol
        seq = '   1 ACTGactgTT aaatttcc ACTGactgAa aaatttccca\n   41 ACTGactgcT aaatttccca ACTGactgCT aaatttccca\n   81 ACTGactgAg aaatttccca ACTGactggg aaatte'
        self.assertEqual(Sequence.generic_validate(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), 0)
    

    def test_detailed_validate_generic(self):
        self.assertEqual(Sequence.detailed_validate_generic('ACTGactg', '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), [])
        seq = '   1 ACTGactgAC aaatttccca ACTGactgaa aaatttccca\n   41 ACTGactgAA aaatttccca ACTGactgtt aaatttccca\n   81 ACTGactgGG aaatttccca ACTGactgcc aaatt'
        self.assertEqual(Sequence.detailed_validate_generic(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), [])
        seq = '   1 ACTGactgAC aaatttccca ACTGactgee aaatttccca\n   41 ACTGactgAA aaatttccca ACTGactgtt aaatttccca\n   81 ACTGactgGG aaatttccca ACTGactgcc aaatt'
        self.assertEqual(Sequence.detailed_validate_generic(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), ['line 1: block 3 contains illegal chars'])
        seq = '   1 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   51 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   81 ACTGactgee aaatttccca ACTGactgee aaatt'
        message = [
            'line 1: bad line length', 
            'line 1: block 1 contains illegal chars', 
            'line 1: block 3 contains illegal chars', 
            'line 2: bad line length',
            'line 2: block 1 contains illegal chars', 
            'line 2: block 3 contains illegal chars',
            'line 3: block 1 contains illegal chars', 
            'line 3: block 3 contains illegal chars',
        ]
        self.assertEqual(Sequence.detailed_validate_generic(seq, '[^ACGNTUBDHKMRSVWY\-\nacgntubdhkmrsvwy]'), message)
        
    #def test_translate2protein_in_range_generic(self):
    
    def translate2protein_generic(self):
        tdict = {
            'GCA':'A','GCC':'A','GCG':'A','GCT':'A', 'TGC':'C','TGT':'C', 'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
            'TTC':'F', 'TTT':'F', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 'CAC':'H', 'CAT':'H', 'ATA':'I', 'ATC':'I', 'ATT':'I',
            'AAA':'K', 'AAG':'K', 'TTA':'L', 'TTG':'L', 'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'ATG':'M', 'AAC':'N', 'AAT':'N',
            'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 'CAA':'Q', 'CAG':'Q', 'AGA':'R', 'AGG':'R', 'CGA':'R', 'CGC':'R', 'CGG':'R', 
            'CGT':'R', 'AGC':'S', 'AGT':'S', 'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
            'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'TGG':'W', 'TAC':'Y', 'TAT':'Y', 'TAG': '*', 'TGA':'*', 'TAA':'*'
        }
        
        test = 'ATGGAATCGGCTTTTAATACTGCAGGGGCGTTAAGTTGGCATGAACTCACAACCAATAATACCGAAGAGGCCATGCGCTTCTATGCTGAGATTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGGGATCAGCATTGGCGGAATTACCGACAGTTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGGATCAAGTGGCTATCAGTGCTAAAAAACTCGGCGGTGACATTCTGTTTGGCCCTGAAGACATTCCAGAGGTGGGCCGTTTTTGTTGGATAAAAGACCCACAGGGCGCCATTATTGCGGCCATTAGCTATTTAAAACGTTGATGTAA'
        
        f1 = ('','MESAFNTAGALSWHELTTNNTEEAMRFYAEIFGWHFKTVKMPHGHYHIIENEGISIGGITDSLIPTLPSHWTGYITVNDVDQVAISAKKLGGDILFGPEDIPEVGRFCWIKDPQGAIIAAISYLKR*C','AA')
        f2 = ('A','WNRLLILQGR*VGMNSQPIIPKRPCASMLRFLAGTLKPSKCPTVTITLLKTRGSALAELPTV*SPPFPHIGLAILPLTMWIKWLSVLKNSAVTFCLALKTFQRWAVFVG*KTHRAPLLRPLAI*NVDV','A')
        f3 = ('AT','GIGF*YCRGVKLA*THNQ*YRRGHALLC*DFWLAL*NRQNAPRSLSHY*KRGDQHWRNYRQFNPHPSLTLDWLYYR*RCGSSGYQC*KTRR*HSVWP*RHSRGGPFLLDKRPTGRHYCGH*LFKTLM*','')
        
        self.assertEqual([f1,f2,f3], Sequence.translate2protein_generic(test, tdict))
        
        
    def test_translate2protein(self):
        pass
    
    def test_validate_seq(self):
        c = Sequence('>name', 'ACTGactg')
        self.assertEqual(c.validate_seq(), 1)
        c = Sequence('>name', 'ACTGactgee')
        self.assertEqual(c.validate_seq(), 0)
        c = Sequence('>name', '   1 ACTGactgAC aaatttccca ACTGactgaa aaatttccca\n   41 ACTGactgAA aaatttccca ACTGactgtt aaatttccca\n   81 ACTGactgGG aaatttccca ACTGactgcc aaatt')
        self.assertEqual(c.validate_seq(), 1)
        
        # not allowed symbol e
        c = Sequence('>name', '   1 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   41 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   81 ACTGactgee aaatttccca ACTGactgee aaatt')
        self.assertEqual(c.validate_seq(), 0)
        
        # not allowed symbol e + len <
        c = Sequence('>name', '   1 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   51 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   81 ACTGactgee aaatttccca ACTGactgee aaatt')
        self.assertEqual(c.validate_seq(), 0)
        
        # not allowed symbol e + len >
        c = Sequence('>name', '   1 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   31 ACTGactgee aaatttccca ACTGactgee aaatttccca\n   81 ACTGactgee aaatttccca ACTGactgee aaatt')
        self.assertEqual(c.validate_seq(), 0)
        
        # len >
        c = Sequence('>name', '   1 ACTGactgTT aaatttcc ACTGactgAa aaatttccca\n   31 ACTGactgcT aaatttccca ACTGactgCT aaatttccca\n   81 ACTGactgAg aaatttccca ACTGactggg aaatt')
        self.assertEqual(c.validate_seq(), 0)
        
        # len <
        c = Sequence('>name', '   1 ACTGactgTT aaatttcc ACTGactgAa aaatttccca\n   51 ACTGactgcT aaatttccca ACTGactgCT aaatttccca\n   81 ACTGactgAg aaatttccca ACTGactggg aaatt')
        self.assertEqual(c.validate_seq(), 0)
        
        # last len >
        c = Sequence('>name', '   1 ACTGactgTT aaatttcc ACTGactgAa aaatttccca\n   51 ACTGactgcT aaatttccca ACTGactgCT aaatttccca\n   81 ACTGactgAg aaatttccca ACTGactggg aaattaaattaaatt')
        self.assertEqual(c.validate_seq(), 0)
        
        # last bad symbol
        c = Sequence('>name', '   1 ACTGactgTT aaatttcc ACTGactgAa aaatttccca\n   41 ACTGactgcT aaatttccca ACTGactgCT aaatttccca\n   81 ACTGactgAg aaatttccca ACTGactggg aaatte')
        self.assertEqual(c.validate_seq(), 0)
    
    def test_cmp(self):
        c = Sequence('>name', '   1 ACTG')
        o = Sequence('>name2', '   1 ACTG')
        self.assertTrue(c.seq == o.seq)
        
    def test_cut(self):
        c = Sequence('>name', '   1 ACTG')
        c.normalize()
        cl = [Sequence('>name_frag_1:1', 'A'),Sequence('>name_frag_2:2', 'C'),Sequence('>name_frag_3:3', 'T'),Sequence('>name_frag_4:4', 'G')]
        rcl = c.cut(1,1)
        self.assertEqual(str(cl[0]), str(rcl[0]))
        self.assertEqual(str(cl[1]), str(rcl[1]))
        #self.assertEqual(cl[0], rcl[0])
        #self.assertEqual(cl, rcl)
    
    def test_revers(self):
        c = Sequence('>name', '   1 ACTG')
        r = Sequence('>rev_name', 'CAGT')
        self.assertEqual(str(r), str(c.reverse()))
        
    def test_normalise(self):
        c = Sequence('>name', '   1 ACTG')
        self.assertEqual('>name\n   1 ACTG\n', str(c) )
        c.normalize()
        self.assertEqual('>name\nACTG\n', str(c) )
    
    def test_statistics(self):
        c = Sequence('>name', '   1 ACTG')
        #r = {'A':1, 'C':1, 'T':1, 'G':1, 'N':0 'L':9}
        self.assertEqual({'A':1, 'C':1, 'T':1, 'G':1, 'N':0, 'L':4}, c.statistics())
        c = Sequence('>name', '   1 ACTG NNNNNNNN')
        self.assertEqual({'A':1, 'C':1, 'T':1, 'G':1, 'N':8, 'L':12}, c.statistics())
        c = Sequence('>name', '   1 ACTG NNNNNNNN\naaanan')
        self.assertEqual({'A':5, 'C':1, 'T':1, 'G':1, 'N':10, 'L':18}, c.statistics())
    
    def test_find_primers(self):
        test = 'ATGGAATCGGCTTTTAATACTGCAGGGGCGTTAAGTTGGCATGAACTCACAACCAATAATACCGAAGAGGCCATGCGC'
        c = Sequence('>test', test)
        self.assertEqual(['GGAATCGGCTTTTAATACTGCAGGGG'],c.find_primers('GGAA', 'GGGG', 'FF'))
        
        self.assertEqual(['AATCGGCT','AATACT','AAGTTGGCATGAACT','AACT','AACGCCCCT'],c.find_primers('AA', 'CT', 'ff'))
    
    def test_find_aprox_motif(self):
        test = 'ATGGAATCGGCTTTTAATACTGCAGGGGCGTTAAGTTGGCATGAACTCACAACCAATAATACCGAAGAGGCCATGCGC'
        c = Sequence('>test', test)
        #print c.find_aprox_motif('TGGAATCGGCT',1)
        self.assertEqual(['TGGAATCGGCT'], c.find_aprox_motif('TGGAATCGGCT',1))
        self.assertEqual(['TGGAATCGGCT'], c.find_aprox_motif('TAGAATCGGCT', 1))
        self.assertEqual([], c.find_aprox_motif('TAGAATCGGCT', 0))
        self.assertEqual(['TGGAATCGGCT'], c.find_aprox_motif('TGGAATCGGCT',0))
        
        
    def test_find_primers(self):
        test = 'ATGGAATCGGCTTTTAATACTGCAGGGGCGTTAAGTTGGCATGAACTCACAACCAATAATACCGAAGAGGCCATGCGCTTCTATGCTGAGATTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGGGATCAGCATTGGCGGAATTACCGACAGTTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGGATCAAGTGGCTATCAGTGCTAAAAAACTCGGCGGTGACATTCTGTTTGGCCCTGAAGACATTCCAGAGGTGGGCCGTTTTTGTTGGATAAAAGACCCACAGGGCGCCATTATTGCGGCCATTAGCTATTTAAAACGTTGATGTAA'
        c = Sequence('>test', test)
        t_TTT_GGG_FF = [
            'TTTTAATACTGCAGGG',
            'TTTAATACTGCAGGG',
            'TTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGGATCAAGTGGCTATCAGTGCTAAAAAACTCGGCGGTGACATTCTGTTTGGCCCTGAAGACATTCCAGAGGTGGG',
            'TTTGGCCCTGAAGACATTCCAGAGGTGGG',
            'TTTTTGTTGGATAAAAGACCCACAGGG',
            'TTTTGTTGGATAAAAGACCCACAGGG',
            'TTTGTTGGATAAAAGACCCACAGGG',
            'TTTTAAATAGCTAATGGCCGCAATAATGGCGCCCTGTGGG',
            'TTTAAATAGCTAATGGCCGCAATAATGGCGCCCTGTGGG',
            'TTTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTCAATAATGTGATAGTGACCGTGGG',
            'TTTCAATAATGTGATAGTGACCGTGGG'
        ]
        
        t_TTT_CCC_FR = [
            'TTTTAATACTGCAGGG',
            'TTTAATACTGCAGGG',
            'TTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGGATCAAGTGGCTATCAGTGCTAAAAAACTCGGCGGTGACATTCTGTTTGGCCCTGAAGACATTCCAGAGGTGGG',
            'TTTGGCCCTGAAGACATTCCAGAGGTGGG',
            'TTTTTGTTGGATAAAAGACCCACAGGG',
            'TTTTGTTGGATAAAAGACCCACAGGG',
            'TTTGTTGGATAAAAGACCCACAGGG',
            'TTTTAAATAGCTAATGGCCGCAATAATGGCGCCCTGTGGG',
            'TTTAAATAGCTAATGGCCGCAATAATGGCGCCCTGTGGG',
            'TTTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTCAATAATGTGATAGTGACCGTGGG',
            'TTTCAATAATGTGATAGTGACCGTGGG'
        ]
        
        self.assertEqual(t_TTT_GGG_FF,  c.find_primers('TTT', 'GGG', 'FF', 0,10000))
        self.assertEqual(t_TTT_CCC_FR,  c.find_primers('TTT', 'CCC', 'FR', 0,10000))
        
    def test_find_aprox_primers(self):
        test = 'ATGGAATCGGCTTTTAATACTGCAGGGGCGTTAAGTTGGCATGAACTCACAACCAATAATACCGAAGAGGCCATGCGCTTCTATGCTGAGATTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGGGATCAGCATTGGCGGAATTACCGACAGTTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGGATCAAGTGGCTATCAGTGCTAAAAAACTCGGCGGTGACATTCTGTTTGGCCCTGAAGACATTCCAGAGGTGGGCCGTTTTTGTTGGATAAAAGACCCACAGGGCGCCATTATTGCGGCCATTAGCTATTTAAAACGTTGATGTAA'
        c = Sequence('>test', test)
        
        t_TTT_GGG_FF = [
            'TTTTAATACTGCAGGG',
            'TTTAATACTGCAGGG',
            'TTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGGATCAAGTGGCTATCAGTGCTAAAAAACTCGGCGGTGACATTCTGTTTGGCCCTGAAGACATTCCAGAGGTGGG',
            'TTTGGCCCTGAAGACATTCCAGAGGTGGG',
            'TTTTTGTTGGATAAAAGACCCACAGGG',
            'TTTTGTTGGATAAAAGACCCACAGGG',
            'TTTGTTGGATAAAAGACCCACAGGG',
            'TTTTAAATAGCTAATGGCCGCAATAATGGCGCCCTGTGGG',
            'TTTAAATAGCTAATGGCCGCAATAATGGCGCCCTGTGGG',
            'TTTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTCAATAATGTGATAGTGACCGTGGG',
            'TTTCAATAATGTGATAGTGACCGTGGG'
        ]
        
        t_TTT_CCC_FR = [
            'TTTTAATACTGCAGGG',
            'TTTAATACTGCAGGG',
            'TTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGGG',
            'TTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGGATCAAGTGGCTATCAGTGCTAAAAAACTCGGCGGTGACATTCTGTTTGGCCCTGAAGACATTCCAGAGGTGGG',
            'TTTGGCCCTGAAGACATTCCAGAGGTGGG',
            'TTTTTGTTGGATAAAAGACCCACAGGG',
            'TTTTGTTGGATAAAAGACCCACAGGG',
            'TTTGTTGGATAAAAGACCCACAGGG',
            'TTTTAAATAGCTAATGGCCGCAATAATGGCGCCCTGTGGG',
            'TTTAAATAGCTAATGGCCGCAATAATGGCGCCCTGTGGG',
            'TTTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGGG',
            'TTTTCAATAATGTGATAGTGACCGTGGG',
            'TTTCAATAATGTGATAGTGACCGTGGG'
        ]
        
        self.assertEqual(t_TTT_GGG_FF,  c.find_aprox_primers('TTT', 'GGG', 'FF', 0,0,10000))
        self.assertEqual(t_TTT_CCC_FR,  c.find_aprox_primers('TTT', 'CCC', 'FR', 0,0,10000))
        
        t_TTTT_GGGG_FF = [
            'CTTTTAATACTGCAGGG',
            'TTTTAATACTGCAGGG',
            'TTTAATACTGCAGGG',
            'TTCTATGCTGAGATTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'ATTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'CTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTATTGAAAACGAGG',
            'TATTGAAAACGAGG',
            'GTTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGG',
            'TTTAATCCCCACCCTTCCCTCACATTGGACTGGCTATATTACCGTTAACGATGTGG',
            'TATTACCGTTAACGATGTGG',
            'TTCTGTTTGGCCCTGAAGACATTCCAGAGG',
            'TGTTTGGCCCTGAAGACATTCCAGAGG',
            'GTTTGGCCCTGAAGACATTCCAGAGG',
            'TTTGGCCCTGAAGACATTCCAGAGG',
            'GTTTTTGTTGGATAAAAGACCCACAGGG',
            'TTTTTGTTGGATAAAAGACCCACAGGG',
            'TTTTGTTGGATAAAAGACCCACAGGG',
            'TTTGTTGGATAAAAGACCCACAGGG',
            'TTGTTGGATAAAAGACCCACAGGG',
            'TGTTGGATAAAAGACCCACAGGG',
            'TTATTGCGG',
            'TATTGCGG',
            'GTTTTAAATAGCTAATGGCCGCAATAATGGCG',
            'TTTTAAATAGCTAATGGCCGCAATAATGGCG',
            'TTTAAATAGCTAATGGCCGCAATAATGGCG',
            'TCTTTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'CTTTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TTATCCAACAAAAACGGCCCACCTCTGGAATGTCTTCAGGG',
            'TCTTCAGGG',
            'GTTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'GTTTTCAATAATGTGATAGTGACCGTGG',
            'TTTTCAATAATGTGATAGTGACCGTGG',
            'TTTCAATAATGTGATAGTGACCGTGG',
        ]
        
        
        
        self.assertEqual(t_TTTT_GGGG_FF,  c.find_aprox_primers('TTTT', 'GGGG', 'FF', 1,0,10000))
        self.assertEqual(t_TTTT_GGGG_FF,  c.find_aprox_primers('TTTT', 'CCCC', 'FR', 1,0,10000))
        self.assertEqual(c.find_aprox_primers('TTTT', 'CCCC', 'fr', 1,0,10000),  c.find_aprox_primers('TTTT', 'CCCC', 'FR', 1,0,10000))
        self.assertEqual(c.find_aprox_primers('TTTT', 'CCCC', 'Fr', 1,0,10000),  c.find_aprox_primers('TTTT', 'CCCC', 'FR', 1,0,10000))
        self.assertEqual(c.find_aprox_primers('TTTT', 'CCCC', 'fR', 1,0,10000),  c.find_aprox_primers('TTTT', 'CCCC', 'FR', 1,0,10000))
        
        t_TTTT_GGGG_FF_60 = [
            'TTCTATGCTGAGATTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'ATTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'GTTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
        ]
        
        self.assertEqual(t_TTTT_GGGG_FF_60,  c.find_aprox_primers('TTTT', 'CCCC', 'FR', 1,60,10000))
        
        t_TTTT_GGGG_FF_60_65 = [
            'TTTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTGGCTGGCACTTTAAAACCGTCAAAATGCCCCACGGTCACTATCACATTATTGAAAACGAGG',
            'TTTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
            'TTTAGCACTGATAGCCACTTGATCCACATCGTTAACGGTAATATAGCCAGTCCAATGTGAGG',
        ]
        
        for r in c.find_aprox_primers('TTTT', 'GGGG', 'FF', 1,60,65):
            print r
        
        self.assertEqual(t_TTTT_GGGG_FF_60_65,  c.find_aprox_primers('TTTT', 'CCCC', 'FR', 1,60,65))
        
        
    
if __name__ == "__main__":
    unittest.main()