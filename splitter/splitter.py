"""Split a single text into smaller parts.

Counts words by counting spaces. Optionally, the script will attempt to preserve
sentence boundaries.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import logging
import math
import os
import re
import string

logger = logging.getLogger('splitter')


def _tokenize(s):
    return re.split(r'\s+', s)


def _split(filename, n_words, preserve_sentences):
    """Split a long text into chunks of approximately `n_words` words."""
    with open(filename, 'r') as input:
        words = _tokenize(input.read())
    chunks = []
    current_chunk_words = []
    current_chunk_word_count = 0
    for word in words:
        current_chunk_words.append(word)
        if word not in string.whitespace:
            current_chunk_word_count += 1
        if current_chunk_word_count == n_words:
            chunk = ' '.join(current_chunk_words)
            chunks.append(chunk)
            # start over for the next chunk
            current_chunk_words = []
            current_chunk_word_count = 0
    final_chunk = ' '.join(current_chunk_words)
    chunks.append(final_chunk)
    return chunks


def splitter(filename, output_dir, n_words, preserve_sentences):
    """Splits text and writes parts to files."""
    filename_base, filename_ext = os.path.splitext(os.path.basename(filename))
    chunks = _split(filename, n_words, preserve_sentences)

    # we want a suffix that identifies the chunk, such as "02" for the 2nd
    # chunk. Python has a couple of standard ways of doing this that should
    # be familiar from other programming languages. For example,
    # "{:04d}".format(2) => "0002"
    n_pad_digits = int(math.log10(len(chunks))) + 1
    chunk_filename_template = "{{}}_split{{:0{}d}}{{}}".format(n_pad_digits)
    for i, chunk in enumerate(chunks):
        chunk_filename = chunk_filename_template.format(filename_base, i, filename_ext)
        with open(os.path.join(output_dir, chunk_filename), 'w') as f:
            f.write(chunk)
    logging.info("Split {} into {} files. Saved to {}".format(filename, len(chunks), output_dir))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split text into parts.')
    parser.add_argument('n_words', type=int, help='Each part has this many words')
    parser.add_argument('input_filename', type=str, help='Input text filename')
    parser.add_argument('output_dir', type=str, help='Output directory')
    parser.add_argument('--preserve-sentences', type=bool, default=False,
                        store_true=True, help='Try to preserve sentences')
    args = parser.parse_args()
    filename = args.input_filename
    output_dir = args.output_dir
    n_words = args.n_words
    preserve_sentences = args.preserve_sentences

    splitter(filename, output_dir, n_words, preserve_sentences)
