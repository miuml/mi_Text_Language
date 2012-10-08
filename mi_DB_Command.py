#! /usr/bin/env python

"""
Class: DB Command

A Metamodel API DB Command

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
from mi_Parameter import Context_Parameter
from mi_API_Parser import API_Constructor_Call

# Symbols
CMD_PREFIX = "UI_"
PARAM_PREFIX = "p_"
PARAM_ASSIGN = ":="
PARAM_PLACE = "%s"


class DB_Command:
    """
    The eleements of a PostgreSQL stored procedure call that can be
    invoked using the psycopg2 driver.  Requires a commands string with
    placeholders for values in a separate list.

    """
    def __init__( self, call_name, extracted_params ):
        """
        Constructs itself from the supplied call name and param-value pairs.

        """
        # State: Creating
        self.call_name = call_name # ex: new_class
        self.api_param_specs = API_Constructor_Call[self.call_name]['parameters']
        self.required_pnames = { pname for pname in self.api_param_specs if
                not self.api_param_specs[pname]['optional'] }

        self.cmd = None # String will be built after all required params are supplied
        self.pvals = []

        self.supplied_params = {} # The next two methods fill these in
        self.fill_in_context() # Only need to do this once per DB Command
        self.add_supplied_params( extracted_params )

    def fill_in_context( self ):
        """
        State: Filling in Context

        For any Context Parameter that has a value, which is required by this
        DB Command, fill in the correspoinding Supplied Parameter by copying the
        Context Parameter value.

        For example, if the Context Parameter 'domain' is set to 'Air Traffic Control'
        and this DB Command requries a value for 'domain', add a Supplied Parameter
        named 'domian' with the 'Air Traffic Control' value.

        """
        # All context key-values where value is not None
        context_settings = { c for c,v in Context_Parameter.items() if v }

        # Take the intersection of the context settings and expected parameters
        # and set those values
        for c in ( context_settings & self.api_param_specs.keys() ):
            self.supplied_params[c] = Context_Parameter[c]


    def add_supplied_params( self, extracted_params ):
        """
        Add the latest batch of extracted parameters to this DB Command's
        supplied parameters.  If all the required parameters are available,
        complete the command string.

        """
        # State: Packaging Parameter Values

        # Add the newly extracted parameters to our supplied params
        for p, v in extracted_params.items():
            self.supplied_params[p] = v

        # If the required pnames minus the supplied pnames is empty, then
        # we have a value for each 
        if not ( self.required_pnames - self.supplied_params.keys() ):
            # Event: all params suppled -> self
            self.complete_command()


    def complete_command( self ):
        """
        Generates an SQL command string from the call name and supplied parameter values.

        ex: UI_new_class( p_name:=%s, p_alias:=%s, p_cnum:=%s )

        """
        pdb.set_trace()
        # State: Completed

        # Start with the api call name and an open parenthesis
        self.cmd = CMD_PREFIX + self.call_name + "( " # Partial

        # Now create a parameter string and a parameter list, both with the
        # same ordering.
        pstrings = []
        for p, v in self.supplied_params.items():
            # Construct the string, ex: p_ + name + := + %s
            pstrings.append( PARAM_PREFIX + p + PARAM_ASSIGN + PARAM_PLACE )
            self.pvals.append( v ) # Append the value to be assigned
        self.cmd += ", ".join( pstrings ) + " )" # Add params and closing parenthesis

        # State: Completed / ( final state with procedure finished )


    def __repr__( self ):
        return "{}:: {}, {}, {}, {}, {}".format(
                self.__class__.__name__,
                self.call_name,
                self.api_param_specs,
                self.required_pnames,
                self.cmd,
                self.pvals
            )

    def __str__( self ):
        return ("Class: DB Command\n"
        "call_name: {}\n" 
        "supplied_params: {}\n" 
        "required_params: {}\n"
        "cmd: {}\npvals: {}\n".format(
                self.call_name,
                self.supplied_params,
                self.required_pnames,
                self.cmd,
                self.pvals
            )
        )

if __name__ == '__main__':
    from mi_API_Parser import API_Parser
    API_Parser()
    Context_Parameter['domain'] = 'ATC'
    Context_Parameter['subsys'] = 'Main'
    test_cmd = DB_Command( "new_class", {
            "name":"Aircraft",
            "alias":"AIR",
            "cnum":53
        }
    )
    print()
    print( test_cmd )
