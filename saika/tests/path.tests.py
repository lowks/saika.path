# -*- encoding: utf-8 -*-

__author__ = 'Mohanson'

import unittest
import os

import saika.path
import saika.path.utils


class PathTestSuit(unittest.TestCase):
    def test_1_define_path(self):
        define_path = saika.path.define_path()
        print('define_path', define_path)
        self.assertEqual(define_path, saika.path.relpath('../path'))

    def test_2_caller_path(self):
        caller_path = saika.path.caller_path()
        print('caller_path', caller_path)
        self.assertEqual(caller_path, os.path.normcase(os.path.abspath(os.path.dirname(__file__))))

    def test_3_relpath(self):
        relpath1 = saika.path.relpath('./')
        self.assertEqual(relpath1, os.path.normcase(os.path.abspath(os.path.dirname(__file__))))
        relpath2 = saika.path.relpath('../')
        self.assertEqual(relpath2, os.path.normcase(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))))
        relpath3 = saika.path.relpath('./1.txt')
        self.assertEqual(relpath3, os.path.normcase(os.path.join(os.path.abspath(os.path.dirname(__file__)), '1.txt')))
        relpath4 = saika.path.relpath('../1.txt')
        self.assertEqual(relpath4, os.path.normcase(
            os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '1.txt')))
        relpath5 = saika.path.relpath('../1/1.txt')
        self.assertEqual(relpath5, os.path.normcase(
            os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '1', '1.txt')))
        relpath6 = saika.path.relpath('./', r'c:/')
        self.assertEqual(relpath6, os.path.normcase(r'c:/'))
        relpath7 = saika.path.relpath('./1.txt', r'c:/test/')
        self.assertEqual(relpath7, os.path.normcase(r'c:/test/1.txt'))

    def test_4_assert_path(self):
        self.assertTrue(saika.path.utils.globbing('1.txt', '*.txt'))
        self.assertTrue(saika.path.utils.globbing('1.txt', '1.*'))
        self.assertTrue(saika.path.utils.globbing('1.txt', '*.*'))
        self.assertTrue(saika.path.utils.globbing('1.txt', '1.txt'))
        self.assertTrue(saika.path.utils.globbing('1.txt.1', '1.*.1'))
        self.assertTrue(saika.path.utils.globbing('1.txt.1', '*.txt.*'))
        self.assertTrue(saika.path.utils.globbing('1.txt.1', '1*'))
        self.assertTrue(saika.path.utils.globbing('1.txt.1', '?.txt.*'))

        self.assertFalse(saika.path.utils.globbing('1.txt', '*.js'))
        self.assertFalse(saika.path.utils.globbing('1.txt', '1.1'))

    def test_5_folder(self):
        folder = saika.path.folder(saika.path.relpath('./'))
        for i in folder.allfiles('*.py'):
            print(i.basename)


if __name__ == '__main__':
    unittest.main()