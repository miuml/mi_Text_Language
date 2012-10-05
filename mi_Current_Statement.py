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

# Diagnostic
import pdb # debug

# Local
MODULE_DIR = os.path.abspath( "../Modules" )
if MODULE_DIR not in sys.path:
    sys.path.append( MODULE_DIR )
from mi_Error import *
from mi_Parameter import Context_Parameter
from mi_DB_Command import DB_Command
from mi_Expression import Expression

class Statement:
    """
    The Current Statement is the line in an miUML Text Script that matches a legal
    Expression currently being processed.  Only one of these ever exists at a time
    during the processing of an miUML Text Script.

    It initializes itself from a line of text, matches itself to an Expression and,
    if found, applies a corresponding regex to extract most or all of the data
    contained.  In complex cases, further parsing may be required.

    """
    def __init__( self, text, section, extraction_obj ):
        """
        State: Creating

        Creates a new Statement by linking to an Expression
        and extracting the Data Item values

        """
        self.R13_Extraction = extraction_obj
        self.section = section
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
                    extracted_params = r.groupdict()
                    expr_name = expr['name']
                    call_name = expr['call']
                    self.update_context( extracted_params )
                    # tfuncs[ Expression[self.section]['name'] ]( r.groupdict(), self.text )
                    self.update_DB_Command( call_name, extracted_params )
                    return

        # State: Invalid Statement
        # Fell through without finding a matching expression
        raise mi_Parse_Error(
                'Statement has no matching expression',
                self.extraction.name, self.extraction.current_line, self.text
            )

    def update_DB_Command( self, extracted_params ):
        """
        """
        last_command = self.R13_Extraction.R9_DB_Population_Script.last_command()
        if last_command:
            last_command.add_supplied_params( call_name, extracted_params )
        else:
            the_db_script.add_command( call_name, extracted_params )

    def update_context( self, params ):
        """
        Update any Context Parameters if any Focus Parameter names are found
        in the extracted parameter set.

        """
        for p, v in params.items():
            if p in Context_Parameter:
                Context_Parameter[p] = v


tfuncs = {
    'new_domain' : pass_params,
    'new_subsystem' : pass_params,
    'new_class' : pass_params,
    'new_attr' : pass_params,
    'new_gen' : pass_params,
    'new_bin_rel' : pass_params
}


if __name__ == '__main__':
    print( "{}: Must be called from another function.".format(__name__) )
