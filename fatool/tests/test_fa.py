import unittest
import sys
from fatool import *
import os




class TestFa(unittest.TestCase):

    def setUp(self):
        with open('test.fa', 'w') as f: 
            f.write('>name3\nCTNACtacgatNNNNNNN\n>name4\nCTNAC\n>name5\nNNNNNACTGNNNN\n>name\nACTGactg\n>name7\nNNNACTGN\n>name8\nCTNACtacgatNNNNNNN\n>name2\nNNNNNNNNNACTGNNNN\n>name6\nCTNACtatNNN\n')
            
        with open('f2.fa', 'w') as f: 
            f.write('')
        pass

    def test_setUpFa(self):
        cl = []
        cl.append(Sequence('>name', 'ACTGactg'))
        cl.append(Sequence('>name2', 'CCCTAGACTG'))
        cl.append(Sequence('>name3', 'CTNNNNNNACtacgat'))
        f = Fa(cl, 'test-fa')
        self.assertEqual(cl, f.contigs)
        self.assertEqual('test-fa', f.name)
        self.assertEqual({'name':0, 'name2':1, 'name3':2}, f.contigs_idx)
        cl.append('something')
        with self.assertRaises(TypeError):
            Fa(cl, 'name4')
        
    def test_str(self):
        cl = []
        cl.append(Sequence('>name', 'ACTGactg'))
        cl.append(Sequence('>name2', 'CCCTAGACTG'))
        cl.append(Sequence('>name3', 'CTNNNNNNACtacgat'))
        f = Fa(cl, 'test-fa')
        self.assertEqual('>name\nACTGactg\n>name2\nCCCTAGACTG\n>name3\nCTNNNNNNACtacgat\n', str(f))
        
    def test_add_contig(self):
        cl = []
        cl.append(Sequence('>name', 'ACTGactg'))
        f = Fa(cl, 'test-fa')
        self.assertEqual(cl, f.contigs)
        f.add_contig(Sequence('>name2', 'CCCTAGACTG'))
        cl.append(Sequence('>name2', 'CCCTAGACTG'))
        self.assertEqual(cl, f.contigs)
        f.add_contig(Sequence('>name2', 'ACTGaaaaaaa') )
        self.assertEqual(cl, f.contigs)
        cl = [Sequence('>name', 'ACTGactg'), Sequence('>name2', 'ACTGaaaaaaa')]
        f.add_contig(Sequence('>name2', 'ACTGaaaaaaa'), 1)
        self.assertEqual(cl, f.contigs)
        
    def test_add_contigs(self):
        cl = [Sequence('>name', 'ACTGactg')]
        f = Fa(cl, 'test-fa')
        self.assertEqual(cl, f.contigs)
        cl.append(Sequence('>name2', 'CCCTAGACTG'))
        cl.append(Sequence('>name3', 'CTNNNNNNACtacgat'))
        f.add_contigs([Sequence('>name2', 'CCCTAGACTG'), Sequence('>name3', 'CTNNNNNNACtacgat')])
        self.assertEqual(cl, f.contigs)
        f.add_contigs([Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')])
        self.assertEqual(cl, f.contigs)
        f.add_contigs([Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')], 1)
        cl = [Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')]
        self.assertEqual(cl, f.contigs)
        #self.assertEqual(cl, f.contigs)
        
    def test_show_names(self):
        cl = [Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')]
        f = Fa(cl, 'test-fa')
        self.assertEqual(['name','name2','name3'], f.show_names())
        f.add_contig(Sequence('>name2', 'ACTGaaaaaaa'), 1)
        self.assertEqual(['name','name3','name2'], f.show_names())
        f.add_contig(Sequence('>name7', 'ACTGaaaaaaa'), 1)
        self.assertEqual(['name','name3','name2','name7'], f.show_names())
        
    def test_extract(self):
        cl = [Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')]
        f = Fa(cl, 'test-fa')
        self.assertEqual(cl, f.contigs)
        cl2 = [Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')]
        self.assertEqual(cl2, f.extract(['name2', 'name3']).contigs)
        self.assertEqual('extr_test-fa', f.extract(['name2', 'name3']).name)
        self.assertEqual(cl2, f.extract(['name2', 'name3', 'name321']).contigs)

    
    def test_remove(self):
        cl = [Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')]
        f = Fa(cl, 'test-fa')
        self.assertEqual([Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')], f.remove(['name']).contigs)
        self.assertEqual([Sequence('>name', 'ACTGactg')], f.remove(['name2','name3']).contigs)
        self.assertEqual([Sequence('>name', 'ACTGactg')], f.remove(['name2','name3','name234']).contigs)
        self.assertEqual([Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')], f.remove(['name']).contigs)
    
    def test_statistics(self):
        cl = [Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC')]
        f = Fa(cl, 'test-fa')
        stat = {
            'A': 7, 'C': 8, 'T': 7, 'G': 4, 'N': 22, 'L': 48,
            'nbp1000': 0, 'nbp5000': 0, 'nbp10000': 0, 'nbp25000': 0, 'nbp50000': 0,
            'lbp1000': 0, 'lbp5000': 0, 'lbp10000': 0, 'lbp25000': 0, 'lbp50000': 0,
            'totalc':4, 'N50':17, 'L50':2,  'N75':8, 'L75':3, 'N90':8, 'L90':3,
            'longest':18
        }

        self.assertEqual(stat, f.statistics())
        
    def test_sort(self):
        cl = [Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC')]
        f = Fa(cl, 'test-fa')
        cl = [Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name', 'ACTGactg'), Sequence('>name4', 'CTNAC')]
        #for r in f.sort(1).contigs:
        #    print r
        #for r in cl.reverse():
        #    print r
        self.assertEqual(cl, f.sort(-1).contigs)
        cl = [Sequence('>name4', 'CTNAC'), Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')]
        self.assertEqual(cl, f.sort(1).contigs)
        
    def test_join(self):
        cl = [Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC')]
        f = Fa(cl, 'test-fa')
        cl2 = [Sequence('>name', 'NNNNNNNN'), Sequence('>name5', 'NNNNNNNNNACTGNNNN'), Sequence('>name6', 'CTNACtacgatNNNNNNN')]
        f2 = Fa(cl2, 'test2-fa')
        f.join([f2])
        cl.append(Sequence('>name5', 'NNNNNNNNNACTGNNNN'))
        cl.append(Sequence('>name6', 'CTNACtacgatNNNNNNN'))
        self.assertEqual(cl, f.contigs)
        cl = [
            Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC'),
            Sequence('>name5', 'NNNNNACTGNNNN'), Sequence('>name6', 'CTNACtatNNN'), Sequence('>name7', 'NNNACTGN'), Sequence('>name8', 'CTNACtacgatNNNNNNN')
        ]
        f = Fa([Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN')], 'fa1')
        f2 = Fa([Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC')], 'fa2')
        f3 = Fa([Sequence('>name5', 'NNNNNACTGNNNN'), Sequence('>name6', 'CTNACtatNNN')], 'fa3')
        f4 = Fa([Sequence('>name7', 'NNNACTGN'), Sequence('>name8', 'CTNACtacgatNNNNNNN')], 'fa4')
        f.join([f2,f3,f4])
        self.assertEqual(cl, f.contigs)
        f = Fa([Sequence('>name', 'ACTGactg'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name3', 'CTNACtacgatNNNNNNN')], 'fa1')
        f2 = Fa([Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC'), Sequence('>name', 'AnnnnnCTGactg')], 'fa2')
        f3 = Fa([Sequence('>name5', 'NNNNNACTGNNNN'), Sequence('>name6', 'CTNACtatNNN'), Sequence('>name4', 'annaCTNAC'), Sequence('>name', 'AaaCTnnaGactg')], 'fa3')
        f4 = Fa([Sequence('>name7', 'NNNACTGN'), Sequence('>name8', 'CTNACtacgatNNNNNNN'), Sequence('>name3', 'CTNaaaACtacgatNNNNNNN'), Sequence('>name', 'AnnnCTGactg')], 'fa4')
        f.join([f2,f3,f4])
        self.assertEqual(cl, f.contigs)
        cl = [
            Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC'), Sequence('>name5', 'NNNNNACTGNNNN'), Sequence('>name', 'ACTGactg'), 
            Sequence('>name7', 'NNNACTGN'), Sequence('>name8', 'CTNACtacgatNNNNNNN'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name6', 'CTNACtatNNN')
        ]
        f = Fa([Sequence('>name', 'NNN'), Sequence('>name2', 'ACTGNNNN'), Sequence('>name3', 'NNNNNNN')], 'fa1')
        f2 = Fa([Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC')], 'fa2')
        f3 = Fa([Sequence('>name5', 'NNNNNACTGNNNN'), Sequence('>name6', 'CTNNN'), Sequence('>name', 'ACTGactg')], 'fa3')
        f4 = Fa([Sequence('>name7', 'NNNACTGN'), Sequence('>name8', 'CTNACtacgatNNNNNNN'),Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name6', 'CTNACtatNNN') ], 'fa4')
        f.join([f2,f3,f4], 1)
        
        self.assertEqual(cl, f.contigs)
    
    def test_load_from_file(self):
        cl = [
            Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC'), Sequence('>name5', 'NNNNNACTGNNNN'), Sequence('>name', 'ACTGactg'), 
            Sequence('>name7', 'NNNACTGN'), Sequence('>name8', 'CTNACtacgatNNNNNNN'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name6', 'CTNACtatNNN')
        ]
        with open('test.fa') as f:
            fob = Fa.load_from_file(f)
                
        self.assertEqual('test.fa', fob.name)
        self.assertEqual(cl, fob.contigs)
        f2 = Fa.load_from_file('test.fa')
        self.assertEqual('test.fa', f2.name)
        self.assertEqual(cl, f2.contigs)
        
            
    def test_write(self):
        cl = [
            Sequence('>name3', 'CTNACtacgatNNNNNNN'), Sequence('>name4', 'CTNAC'), Sequence('>name5', 'NNNNNACTGNNNN'), Sequence('>name', 'ACTGactg'), 
            Sequence('>name7', 'NNNACTGN'), Sequence('>name8', 'CTNACtacgatNNNNNNN'), Sequence('>name2', 'NNNNNNNNNACTGNNNN'), Sequence('>name6', 'CTNACtatNNN')
        ]
        f = Fa(cl, 'fa1')
        f.write('f2.fa')
        with open('test.fa') as f1, open('f2.fa') as f2:
            f1_content = f1.read()
            f2_content = f2.read()
            self.assertEqual(f1_content, f2_content)
        
    
    def tearDown(self):
        os.remove('f2.fa')
        os.remove('test.fa')
        pass
        
        
if __name__ == "__main__":
    unittest.main()