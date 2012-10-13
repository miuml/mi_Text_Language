#! /usr/bin/env python

"""
Creation of the API_Parser class loads and parses the API constructors and types.

An API constructor is just an API call which creates something (as opposed
to an edit or delete call).

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
import sys
import os

# Local
MODULE_DIR = os.path.abspath( "../Modules" )
if MODULE_DIR not in sys.path:
    sys.path.append( MODULE_DIR )
from mi_Error import *
from mi_Structured_File_2 import Structured_File

# Diagnostic
import pdb # debug

# Constants
API_PATH = os.path.abspath( "Resources/constructor_api_def.mi" )
CALL_PREFIX = "UI_"
TYPE_SECTION = "type"
CONSTRUCTION = "constructor"

# Regex
# <metaclass>[ / <callname>]
metaclass_record_RE = re.compile( r'(?P<metaclass>\w+)(\s*/\s*(?P<call_name>\w+))?' )

# Global
tfunc = { 'string':str, 'integer':int, 'float':float, 'bool':bool }

API_Constructor_Call = {}
API_Type = {}

class API_Parser:
    """
    Constructor API - The API constructor calls

    """
    def __init__( self ):

        # Import command and type sections
        self.api_data = Structured_File( API_PATH )
        self.current_api_call = None

        # Parse the command records
        self.build_types()
        self.build_constructors()

    def build_types( self ):
        """
        Parse each line of text formatted like this:
        
        <app_type><_TYPE_DELIM><ui_type>

        To create dictionary with this structure:

        { <app_type> : <ui_func> }

        Where the ui_func is a Python function corresponding to
        the specified ui_type to make it possible to cast from
        a string to the ui_type compatible with the app_type
        when building an API command.

        """
        for n, line in enumerate( self.api_data.sections[TYPE_SECTION] ):
            app_type, ui_type = line.split()

            # Check for any errors in the type data
            if ui_type not in tfunc:
                raise mi_Parse_Error( "Unknown ui type", API_PATH, n, line )
            if not app_type:
                raise mi_Parse_Error( "App type unspecified", API_PATH, n, line )
            if app_type in API_Type:
                raise mi_Parse_Error( "App type duplicate", API_PATH, n, line )

            # All good, add it to our metamodel types
            API_Type[app_type] = tfunc[ui_type]

    def build_constructors( self ):
        """
        Parse each line of text formatted like this:

        <metamodel_class> [ / api_call_name ]

        or this:

        <parameter>[...],

        where <parameter> is either of these:

        param_name:app_type
        [ param_name:app_type ]

        to create a dictionary with this structure:

        metamodel_class:{ 'call_name': call_name, 'parameters':<parameters> }
        <parameters> -> parameters:{ 'multiple':boolean, 'optional':boolean, 'type':app_type }

        The presence of the ... symbol sets the multiple key while [ ] sets the optional key

        """
        # There are only two kinds of constructor records:
        # metaclass and parameter list
        #
        # Every parameter line has at least one parameter, and a parameter
        # must always use the : symbol to declare its type
        # So we can sort sort the two record types based on whether or not
        # this symbol is found in the line.
        #
        for n, line in enumerate( self.api_data.sections[CONSTRUCTION] ):
            if ":" in line: # It's a list of parameters
                self.parse_params( line, n )
            else: # It's the name of a metaclass
                self.parse_metaclass( line, n )

    def parse_params( self, line, n ):
        """
        Parse a line of comma separated parameters with the format:

        <param_name>[-><focus_param>]:<app_type>[...]

        where [] indicates an optional item and ... is an literal symbol

        all of which may or may not be bracketed by [ ] to indicate that
        the param is optional

        See the source file comments for more details on the grammar

        """
        line = line.rstrip(",") # remove any superfluous trailing comma
        for precord in line.split(","):
            optional = False # API provides a default value for parameter
            multiple = False # Multiple values may be specified for parameter
            focus_param = None
            param_name, param_type = precord.split( ":" )

            # Is this an optional parameter?
            if '[' in param_name:
                optional = True

            param_name = param_name.lstrip(" [")
            param_type = param_type.rstrip(" ]")

            # Check for scope setting
            if "->" in param_name:
                param_name, focus_param = param_name.split("->")

            if param_type.endswith('...'):
                multiple = True
                param_type = param_type.rstrip(".")

            # Check for parse errors
            if not param_name:
                raise mi_Parse_Error( "Parameter name missing", API_PATH, n, line )
            if not param_type:
                raise mi_Parse_Error( "Parameter type missing", API_PATH, n, line )
            if not self.current_api_call:
                raise mi_Parse_Error( "Parameter with no metaclass", API_PATH, n, line )
            if param_name in API_Constructor_Call[self.current_api_call]['parameters']:
                raise mi_Parse_Error( "Duplicate parameter", API_PATH, n, line )
            if param_type not in API_Type:
                raise mi_Parse_Error( "Parameter with unknown type", API_PATH, n, line )

            # All good, add the parameter to the metaclass
            prec = {'type':param_type, 'optional':optional, 'multiple':multiple}
            if focus_param:
                prec['scope'] = focus_param # Relevant for only a handful of calls
            API_Constructor_Call[self.current_api_call]['parameters'][param_name] = prec


    def parse_metaclass( self, line, n ):
        """
        Parses a metaclass record of the form:

        <metaclass>[ / <call_name>]

        """
        r = metaclass_record_RE.match( line )
        if not r:
            raise mi_Parse_Error( "Bad metaclass record", API_PATH, n, line )
        metaclass = r.groupdict()['metaclass']
        call_name = r.groupdict()['call_name']

        if not metaclass:
            raise mi_Parse_Error( "Metaclass missing ", API_PATH, n, line )
        if not call_name:
            call_name = 'new_' + metaclass
        if metaclass in API_Constructor_Call:
            raise mi_Parse_Error( "Metaclass duplicate", API_PATH, n, line )

        API_Constructor_Call[call_name] = { 'metaclass':metaclass, 'parameters': {} }
        self.current_api_call = call_name


if __name__ == '__main__':
    from pprint import pprint as pp
    API_Parser()
    print( "API Types")
    print( )
    pp( API_Type )
    print( "API Constructor Calls")
    pp( API_Constructor_Call )
    print( )

