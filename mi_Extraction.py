#! /usr/bin/env python

"""
Extraction

Extracts data from an miUML Text Script and creates a DB Population Script

"""
# --
# Copyright 2012, Model Integration, LLC
# Developer: Leon Starr / leon_starr@modelint.com

# This file is part of the miUML metamodel library.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.  The license text should be viewable at
# http://www.gnu.org/licenses/
# --
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# System
import re
import os
import sys

# Diagnostic
import pdb # debug

# Local
MODULE_DIR = os.path.abspath( "../Modules" )
if MODULE_DIR not in sys.path:
    sys.path.append( MODULE_DIR )
from mi_Error import *
from mi_Section import *
from mi_Current_Statement import Current_Statement

# Global


# Constants
COMMENT_CHAR = '#'

class Extraction:
    """
    A DB Population Script is extracted from an miUML Text Script during
    an Extraction.  So this is an association class on a 1:1 association.

    """
    def __init__( self, text_file_path, db_pop_script_obj ):
        """
        """
        # miUML Text Script file path
        self.fname = text_file_path
        self.ts_file = None  # Open file descriptor

        # Model navigation shorcuts
        self.R9_DB_Population_Script = db_pop_script_obj

        # Initial position in miUML Text Script
        self.current_section = 'model'
        self.line_no = 0
        self.context = {}

        # Metamodel specific
        #self.ref_attrs = {}
        #self.identifiers = {}

        # Process each line of the text script
        self.open_text_script()
        self.process_lines()

    
    def open_text_script( self ):
        """
        State: Opening Text Script

        """
        try:
            self.ts_file = open( self.fname )
        except:
            # Transition to Invalid File terminal state
            raise mi_File_Error( "Cannot open", self.fname )


    def process_lines( self ):
        """
        State: Processing Line
        
        Opens an miUML Text Script and processes each line.  A non-comment,
        non-whitespace line will either be a section header or an expression
        pattern.

        A section sets context while an expression pattern yields a new Statement
        Statement which parses itself according to the pattern.

        """
        for n, line in enumerate( self.ts_file, 1 ):
            line = self.strip_comment( line )
            # left indent whitespace is preserved
            if line:
                self.line_no = n
                section_match = section_RE.match( line )
                if section_match:
                    # If the section name is valid, set it as the current section
                    self.update_section( section_match.groupdict()['name'] )
                else:
                    # Create a Statement which will parse the content
                    # any whitespace indent is removed
                    pdb.set_trace()
                    Current_Statement( line.strip(), self.current_section, self )

    def update_section( self, section_name ):
        """
        State: Updating Current Section

        Verifies that the new section fits in the current context.
        If so, it becomes the new current context.

        """
        # This expression constructs a metamodel element
        if section_name not in Section:
            raise mi_Parse_Error( "Unrecognized section",
                    self.fname, self.line_no, section_name  )
            if section_name not in section_order[self.current_section]:
                # State: Bad Section
                raise mi_Parse_Error( "Section in wrong context",
                        self.fname, self.line_no, section_name )

        self.current_section = section_name


    def strip_comment( self, line ):
        """
        Strips any or all comment portion from the line and/or any whitespace.

        """
        # Empty line
        if not line:
            return None

        # Comment type 1: Entire line is a comment, return nothing
        if line.startswith( COMMENT_CHAR ):
            return None

        # Comment type 2: Remove trailing comment
        return line.split( COMMENT_CHAR )[0].rstrip()

        # Content, but no comment, preserve indent and strip trailing whitespace/newline
        return line.rstrip()




# Not sure where these should go
#    def add_ref_attr( self, data_items ):
#        """
#        { R26: { 'from': 'Source attribute', 'to':'Name', 'constrained':True } }
#        """
#        rnum = data_items.pop('rnum')
#        self.ref_attrs[rnum] = data_items
#
#    def add_non_primary_id( self ):
#        """
#        """
#        self.np_ids['class'] = 
#
