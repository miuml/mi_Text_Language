#! /usr/bin/env python

"""
Class: DB Population Script

A sequence of DB Commands that will be executed to populate an miUML metamodel
schema.

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
from mi_DB_Command import DB_Command



class DB_Population_Script:
    """
    A sequence of DB Commands that will be executed to populate an miUML metamodel
    schema.

    """
    def __init__( self ):
        self.R11_DB_Command = []

    def last_command( self ):
        """
        Returns the DB Command object at the end of the pop script

        """
        return None if not self.Rll_DB_Command else self.R11_DB_Command[-1]

    def ev_add_command( self, call_name, extracted_params ):
        """
        Event: Add a new command to the end of this pop script

        """
        self.Rll_DB_Command.append( DB_Command( self, call_name, extracted_params ) )

    def execute( self ):
        """
        Connect to the database and run the script.  Rolls back if any command
        fails.

        """
        # Connect to DB
        
        # Create savepoint

        # Loop through commands
        # Rolling back if problem

        # Close DB connection









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
