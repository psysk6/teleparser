#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Telegram cache4 db parser.
# Part of the project: tblob.py tdb.py logger.py
#
# Version History
# - 20200807: added support for version 6.3.0
# - 20200803: changed sqlite3 opening to 'bytes', fixed tdb.py on ver 4.9.0
# - 20200731: fixed wrong object ID for page_block_subtitle
# - 20200622: fixed wrong object 0x83e5de54 (message_empty_struct)
# - 20200617: added support for 5.15.0
# - 20200418: change eol terminators, added requirements file
# - 20200407: [tblob] fixed a bug, [tdb] added a couple of checks base on
#             version 4.8.11, added small script to test/debug single blobs
# - 20200406: first public release (5.5.0, 5.6.2)
# - 20190729: first private release
#
# Released under MIT License
#
# Copyright (c) 2019 Francesco "dfirfpi" Picasso, Reality Net System Solutions
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Telegram cache4 db parser, script entry point."""

# pylint: disable= C0103,C0116

import sqlite3
import tblob
import tdb

VERSION = "20200807"


def process(infilename, outdirectory):

    db_connection = None
    db_uri = "file:" + infilename + "?mode=ro"

    tparse = tblob.tblob()

    with sqlite3.connect(db_uri, uri=True) as db_connection:
        db_connection.text_factory = bytes
        db_connection.row_factory = sqlite3.Row
        db_cursor = db_connection.cursor()

        teledb = tdb.tdb(outdirectory, tparse, db_cursor)
        teledb.parse()

    teledb.save_parsed_tables()
    teledb.create_timeline()  # TODO: address crash in this method
