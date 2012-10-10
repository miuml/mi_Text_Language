#! /usr/bin/env python

"""
Class: Current Statement

The Current Statement is the line in an miUML Text Script that matches a legal
Expression currently being processed.  Only one of these ever exists at a time
during the processing of an miUML Text Script.

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
from mi_API_Parser import API_Constructor_Call, API_Type
from mi_Parameter import Context_Parameter
from mi_DB_Command import DB_Command
from mi_Expression import Expression

class Current_Statement:
    """
    The Current Statement is the line in an miUML Text Script that matches a legal
    Expression currently being processed.  Only one of these ever exists at a time
    during the processing of an miUML Text Script.

    It initializes itself from a line of text, matches itself to an Expression and,
    if found, applies a corresponding regex to extract most or all of the data
    contained.  In complex cases, further parsing may be required.

    """
    def __init__( self, text, current_section, extraction_obj ):
        """
        State: Creating

        Creates a new Statement by linking to an Expression
        and extracting the Data Item values

        """
        self.R13_Extraction = extraction_obj
        self.section = current_section
        self.text = text
        self.parse()


    def parse( self ):
        """
        States: Parsing and Validation, Invalid Statement

        Find the Expression that matches this Statement's text and
        pass the extracted data, long with the original text to a function
        that will build all or part of an API command.

        """
        # Each section defines one or more expressions
        # An expresion is recognized by one or more patterns
        for expr in Expression[self.section]:
            for pattern in expr['patterns']:
                r = pattern.match( self.text )
                if r:
                    expr_name = expr['name']
                    call_name = expr['call']
                    extract_func = expr.get('extract') # Exists only for some exprs
                    extracted_params = self.convert_params( call_name, r.groupdict() )
                    self.update_context( call_name, extracted_params )
                    if extract_func:
                        extracted_params = eval( extract_func )
                    # tfuncs[ Expression[self.section]['name'] ]( r.groupdict(), self.text )
                    if call_name:
                        self.update_DB_Command( call_name, extracted_params )
                    return

        # State: Invalid Statement
        # Fell through without finding a matching expression
        raise mi_Parse_Error(
                'Statement has no matching expression',
                self.extraction.name, self.extraction.current_line, self.text
            )

    def convert_params( self, call_name, pdict ):
        """
        Convert each parameter to a python base type compatible with the target
        application data type.

        """
        typed_params = {}
        for p, v in pdict.items():
            app_type = API_Constructor_Call[call_name]['parameters'][p]['type']
            typed_params[p] = API_Type[app_type](v)
        return typed_params


    def update_DB_Command( self, call_name, extracted_params ):
        """
        """
        my_db_script = self.R13_Extraction.R9_DB_Population_Script
        last_command = my_db_script.last_command()
        if last_command:
            last_command.add_supplied_params( extracted_params )
        else:
            self.R13_Extraction
            my_db_script.add_command( call_name, extracted_params )

    def update_context( self, call_name, params ):
        """
        Update any Context Parameters if any Focus Parameter names are found
        in the extracted parameter set.

        """
        pspecs = API_Constructor_Call[call_name]['parameters']
        focus_params = [ fp for fp in pspecs if 'scope' in pspecs[fp] ]
        for fp in focus_params:
            Context_Parameter[ pspecs[fp]['scope'] ] = params[fp]

tfuncs = {
    'new_domain' : None,
    'new_subsystem' : None,
    'new_class' : None,
    'new_attr' : extract_attr,
    'new_gen' : None,
    'new_bin_rel' : None
}


if __name__ == '__main__':
    print( "{}: Must be called from another function.".format(__name__) )
