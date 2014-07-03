# -*- coding: utf-8 -*-

"""
test_splitter
----------------------------------

Tests for `splitter` module.
"""
import os
import tempfile

from splitter import splitter

from splitter.tests import base


class TestSplitter(base.TestCase):

    test_filename = os.path.join(os.path.dirname(__file__), 'text-french.txt')

    def test_split_simple(self):
        filename = self.test_filename
        n_words = 1000
        preserve_sentences = False
        chunks = splitter._split(filename, n_words, preserve_sentences)
        self.assertEqual(len(chunks), 16)

    def test_splitter_simple(self):
        filename = self.test_filename
        output_dir = tempfile.mkdtemp()
        n_words = 1000
        preserve_sentences = False
        splitter.splitter(filename, output_dir, n_words, preserve_sentences)
        self.assertEqual(len(os.listdir(output_dir)), 16)
