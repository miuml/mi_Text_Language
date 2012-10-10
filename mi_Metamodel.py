#! /usr/bin/env python

"""
Complicated miUML population expressions require metamodel specific
parsing and intermediate structures before an API Call can be constructed.

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
from mi_DB_Population_Script import DB_Population_Script


# Diagnostic
import pdb # debug

# Constants

# This name should stand out in case it does not get deleted
# after the entire DB Pop script has completed, as it should
INITIAL_DUMMY_ID_ATTR_NAME = '__POP_Dummy_ID'


# Regex

# Global

Context_Parameter = {'domain':'DMV', 'class':'Car' } # For testing only

Identifiers = { 'domain':None, 'classes':{} }
Ref_Attrs = []


def new_class_ids( class_data ):
    """
    A new class has been created.  Start a new id record for it.

    """
    Identifiers['domain'] = Context_Parameter['domain']
    ids = Identifiers['classes'][ Context_Parameter['class'] ] = []

def parse_id( attr_data ):
    """
    For each attribute that participates in one or more identifier attributes, save
    its info so we can add it to each of its id's in the add id commands phase.

    """
    ids = Identifiers['classes'][ Context_Parameter['class'] ]
    max_id_num = len(ids) # The current max id number

    # Parse out the id numbers in which this attribute participates
    if attr_data['id'] == 'I':
        id_numbers = [1]
    else:
        id_numbers = sorted( [int(i) for i in set(attr_data['id'][1:])] ) # Duplicates removed

    highest_id_num = id_numbers[-1]
    assert highest_id_num > 0, "Highest id number is less than 1"

    if highest_id_num > max_id_num:
        # We need to create an empty set for each new higher id number
        missing_ids = highest_id_num - max_id_num
        ids += [ set() for _ in range(missing_ids) ]
        # Now we can safely index with ids[id_num-1] for each newly requested id number
    # Otherwise, there is an adequate number of lists in ids
    # If ids is empty, it will always pick up at least one new empty list since the
    # minimum possible highest_id_num is 1

    attr_name = attr_data['name']
    for i in id_numbers:
        ids[i-1].add( attr_name ) # its a set, so no duplicates


def add_id_commands():
    """
    Adds a list of id edit commands to the DB Population Script so that
    each attribute in a class can be added to each identifier in which
    it will participate.  For each class, at the end of 'add to id' list
    of commands, there will be one 'remove from id' command to get rid of
    the dummy initial id which must be created for a new class.

    """
    pdb.set_trace()
    for class_name, class_ids in Identifiers['classes'].items():
        params = {}
        params['class'] = class_name
        for i, this_id in enumerate(class_ids):
            params['id_num'] = i+1
            for this_attr in this_id:
                params['attr'] = this_attr
                DB_Population_Script.add_command( 'add_attr_to_id', params )
        params['id_num'] = 1
        params['attr'] = INITIAL_DUMMY_ID_ATTR_NAME
        DB_Population_Script.add_command( 'remove_attr_from_id', params )


if __name__ == '__main__':
    new_class_ids( {'name':'Car', 'alias':'CAR' } )
    parse_id( { 'name':'State', 'id':"I13" } )
    parse_id( { 'name':'Title', 'id':"I" } )
    parse_id( { 'name':'VIN', 'id':"I2" } )
    parse_id( { 'name':'License Number', 'id':"I3" } )
    parse_id( { 'name':'Manufacturer', 'id':"I2" } )
    add_id_commands()




