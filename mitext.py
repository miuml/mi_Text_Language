#! /usr/bin/env python

"""
mitext command

Takes a text miUML model file from the command line, reads it and populates the
local miUML metamodel database.  The entire file is first scanned for syntax errors.
If any are found, the database will not be touched.  Assuming success, each model
element will be created until a metamodel error is encountered, at which point
processing ends and no further elements are created.

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
import os
from sys import argv, stdin

# Go to real code file directory, in case invoked by symbolic link
# so we can find required relative parent/sibling directories
# We must do this before importing anything local that uses relative paths

# The directory where the editor is launched is not necessarily the same
# as the source code directory, particularly if a symbolic link is used.
# We'll need it to get the correct path names of any command files specified
# as arguments.
launch_dir = os.getcwd()

# Local modules and resource directories are easiest to find if we ensure
# that the current directory is the source code directory.
# So we go there immediately.  Realpath is used in case we are launched with
# a symbolic link.
os.chdir( os.path.dirname( os.path.realpath(__file__) ) )

# Local
from mi_DB_Population_Script import DB_Population_Script
from mi_API_Parser import API_Parser
from mi_Extraction import Extraction

# Diagnostic
import pdb

if __name__ != '__main__':
    print( os.path.basename(__file__) +
        " must be executed from the command line and not imported."
    )
    exit(1)

# For now we will process a single file only, make sure one is specified
if len( argv ) != 2:
    print( "Usage: mi miuml_text_file" )
    exit(1)

# Verify that the file exists before connecting to the db

tfile_abs_path = os.path.join( launch_dir, argv[1] )
if not os.path.isfile( tfile_abs_path ):
    print( "Could not open: " + tfile_abs_path )
    # We'll test again for an open error when we start processing it
    exit(1)


# Load the metamodel constructor API
API_Parser()

# Create singleton classes
db_pop_script_obj = DB_Population_Script( )

# Begin the extraction
Extraction( tfile_abs_path, db_pop_script_obj )
