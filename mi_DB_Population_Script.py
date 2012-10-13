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
import os
import sys

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
        Returns the last unfinished DB Command.  A DB Command is not finished until
        a cmd string has been generated.

        """
        # Empty script (no commands yet)
        if not self.R11_DB_Command:
            return None

        # If last command is unfinished, return it
        last_command = self.R11_DB_Command[-1]
        return ( last_command if not last_command.cmd else None )


    def add_command( self, call_name, extracted_params ):
        """
        Event: Add a new command to the end of this pop script

        """
        self.R11_DB_Command.append( DB_Command( call_name, extracted_params ) )

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

    print( DB_Population_Script )
