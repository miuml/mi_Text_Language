#! /usr/bin/env python

"""
Modeled Classes: Context Parameter and Supplied Parameter
Implementation: Dictionaries

A Supplied Parameter is a value extracted from the Current Statement and contributed
toward the construction of a Metamodel API DB Command.  All Expressions within a
Constructor Block must be processed to create a complete set of Supplied Parameter
values.

A Context Parameter is a value extracted from a Current Statement which will be shared
among one or more Metamodel API DB Commands.  These apply only to Focus Parameters such
as 'Domain', 'Subsystem', and 'Class'.  The same 'domain' value, for example, may set
the context for multiple subsequent commands.

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

Context_Parameter = {'domain':None, 'subsys':None, 'class':None} # Focus_param:value
Supplied_Parameter = {}

def new_domain( self, data_items, statement ):
    """
    Build create domain API call.

    """
    # Set the current domain context
    context_parameters['domain'] = data_items['name']
    supplied_parameters = data_items

    # Creates a command which adds itself to the db pop script
    DB_Command( 'new_domain' )

    def new_subsystem( self, data_items, expr ):
        """
        Build create subsystem API call

        """
        self.context['subsystem'] = data_items['name']
        call_name = self.api.constructors['subsystem']['call_name']
        DB_Command( call_name, tuple(data_items.items()), context, self.db_pop_script )

    def new_class( self, data_items, expr ):
        """
        Build create class API call

        """
        self.context['class'] = { 'name' : data_items['name'] }
        call_name = self.api.constructors['class']['call_name']
        DB_Command( call_name, tuple(data_items.items()), context, self.db_pop_script )


#tfuncs = {
#    'new_domain' : pass_params,
#    'new_subsystem' : pass_params,
#    'new_class' : pass_params,
#    'new_attr' : pass_params,
#    'new_gen' : pass_params,
#    'new_bin_rel' : pass_params
#}


if __name__ == '__main__':
    import os
    from sys import argv, stdin

    # For now we will process a single file only, make sure one is specified
    if len( argv ) != 1:
        print( "Specify an miUML text file to process." )
        exit(1)

    # Verify that the file exists before connecting to the db
    if not os.path.isfile(argv[1]):
        print( "Could not open the file." )
        # We'll test again for an open error when we start processing it
        exit(1)

    # Connect to the metamodel db
    db = miuml_db()

    # Process the miuml text file
    the_SFile = miUML_Text_File( "Resources/api_def.mi" )
    pprint( the_SFile.sections )
