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
from mi_Parameter import Context_Parameter
from mi_Expression import SUBSYS_REF
from mi_API_Parser import API_Type


# Diagnostic
import pdb # debug

# Constants

# This name should stand out in case it does not get deleted
# after the entire DB Pop script has completed, as it should
INITIAL_DUMMY_ID_ATTR_NAME = '__POP_Dummy_ID'


# { rnum:[{ from_class, from_attr, to_class, to_attr, const }, ...] }

class Metamodel_Parser:
    """
    Takes the lightly parsed data from the script processor and further parses
    it and buffers forward references and dependencies so that DB Commands can
    be corectly created.

    """
    def __init__( self, db_pop_script ):
        """
        Parsing is done on a domain by domain basis at this point.  So each
        time a new domain is encountered, we clear all the buffers.

        """
        self.db_pop_script = db_pop_script # Bridge to script domain
        self.new_domain()

    def parse( self, method_name, parsed_expr ):
        """
        Given a lightly parsed expression, invoke a corresponding method
        to parse that data a bit deeper and buffer any forward
        references or dependencies.

        """
        # Verify that the member function is defined on this class
        if method_name not in self.__class__.__dict__.keys():
            print(">> Parse: bad method_name")
            pdb.set_trace()
            raise mi_Error( "No parse function for expression: " + method_name )

        # Invoke it, passing along the parsed expression data
        eval( 'self.' + method_name )( parsed_expr )
        # These expression functions are defined below
        print(">> Expr:" + method_name + " meta-parsed")
        #pdb.set_trace()



    # >>> Begin expression parsing functions

    def new_domain( self, domain_data=None ):
        """
        Clears all buffers for a new domain.

        """
        # These are buffered up in the context of the current domain
        self.subsystems = set() # All subsystems in current domain that have been parsed
        self.subsys_dependencies = {} # Classes in these have been processed
        self.identifiers = {}
        self.references = {}

    def new_bridge( self, bridge_data ):
        """
        """
        pass

    def new_subsystem( self, subsys_data ):
        """
        Adds name to list of processed subsystems

        """
        self.subsystems.add( subsys_data['name'] )

    def new_class( self, class_data ):
        """
        A new class has been created.  Start a new id record for it.

        """
        ids = self.identifiers[ Context_Parameter['class'] ] = []

    def new_ind_attr( self, attr_data ):
        """
        If an identifier string is specified, parse it.  Convert the data type to
        the correct API variable name and reject if type is unknown.

        """
        # Create any required identifier attributes
        if attr_data['id']:
            self.parse_id( attr_data )

        # Fill in / convert / validate the type name
        attr_type = attr_data['type']
        if not attr_type:
            # Assume it is the same as the attribute name
            attr_type = attr_data['name']
        # Change it to a variable name style with lower case and underscores
        attr_type = attr_type.replace(" ", "_").lower()
        if attr_type not in API_Type:
            raise mi_Error("Unknown data type specified: " + attr_type )

        # Change the extracted value to the correct type name
        attr_data['type'] = attr_type



    def new_ref_attr( self, attr_data ):
        """
        According to the miUML metatmodel, a Referential Attribute participates in
        one or more References.  A Relationship is formalized by one or more
        References.

        This meanst that a new referential attribute parsed here may participate in
        multiple References.  Each of these References must be added to the references
        dictionary structured as shown:

        references -> { rnum: <reference>, ... }
        <reference> -> [
            'from_attr':from_attr, 'to_attr':to_attr,
            'from_class':from_class, 'to_class':to_class, constrained:<boolean>
            ]

        This data will be used during the relationship construction phase after all
        new class and new ind attr commands are added to the DB Pop Script.

        The incoming reference dictionary has the following keys:
            'from_attr', 'to_attrs', 'id', 'rnum', 'constrained'

        Most of these values are fully parsed by the extracting regex, but 'to_attrs'
        may contain multiple to attributes, so these must be parsed out to yield possibly
        many references, one for each destination attribute.

        Finally, we request an identifier attribute if id membership is specified as
        a referential attribute can participate in an identifier just like an independent
        attribute.
        
        """
        # Save for quick access in to_attr loop
        rnum = attr_data['rnum']
        constrained = attr_data['constrained']
        from_attr = attr_data['from_attr']
        id_member = attr_data['id']
        from_class = Context_Parameter['class']
        this_subsys = Context_Parameter['subsys']
        this_domain = Context_Parameter['domain']

        # Create a new attr_data set for this relationship
        if rnum not in self.references:
            self.references[rnum] = []

        # Parse to_attrs
        to_attrs = attr_data['to_attrs'].split(", ")
        for to_attr in to_attrs:
            ref_rec = {
                    'from_attr':from_attr,
                    'subsystem':this_subsys,
                    'from_class':from_class,
                    'constrained':constrained
                }
            if SUBSYS_REF in to_attr:
                to_subsys, to_attr = to_attr.split( SUBSYS_REF )
                if this_subsys not in self.subsys_dependencies:
                    self.subsys_dependencies[this_subsys] = set( )
                self.subsys_dependencies[this_subsys].add( to_subsys )
            try:
                ref_rec['to_class'], ref_rec['to_attr'] = to_attr.split( '.' )
            except ValueError:
                raise mi_Error( "Bad to attr reference in referential attribute: " + to_attr )
            self.references[rnum].append( ref_rec )

        # If ref attr participates in one or more ids, parse id data
        if attr_data['id']:
            attr_data = {'name':attr_data['from_attr'], 'id':attr_data['id']}
            self.parse_id( attr_data )

    # <<< End of parse expression functions

    def parse_id( self, attr_data ):
        """
        For each attribute that participates in one or more identifier attributes, save
        its info so we can add it to each of its id's in the add id commands phase.

        """
        print(">> Parsing ID for: " + attr_data['id'] )
        #pdb.set_trace()
        ids = self.identifiers[ Context_Parameter['class'] ]
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

        print(">> ID Created")
        #pdb.set_trace()

    def add_id_commands( self ):
        """
        Adds a list of id edit commands to the DB Population Script so that
        each attribute in a class can be added to each identifier in which
        it will participate.  For each class, at the end of 'add to id' list
        of commands, there will be one 'remove from id' command to get rid of
        the dummy initial id which must be created for a new class.

        """
        for class_name, class_ids in self.identifiers.items():
            params = {}
            Context_Parameter['class'] = class_name
            for i, this_id in enumerate( class_ids ):
                params['id_num'] = i+1
                for this_attr in this_id:
                    params['attr'] = this_attr
                    self.db_pop_script.add_command( 'add_attr_to_id', params )
            params['id_num'] = 1
            params['attr'] = INITIAL_DUMMY_ID_ATTR_NAME
            self.db_pop_script.add_command( 'remove_attr_from_id', params )


if __name__ == '__main__':
    from mi_DB_Population_Script import DB_Population_Script
    parser = Metamodel_Parser( DB_Population_Script() )

    # Test new_ref_attr
    Context_Parameter['class'] = "Native Attribute"
    Context_Parameter['domain'] = "miUML Metamodel"
    parser.new_class( {'name':'Native Attribute', 'alias':'NATTR' } )
    Context_Parameter['subsys'] = "Class"
    parser.new_ref_attr( {
        'from_attr':"Type",
        'to_attrs':"Type::Constrained Type.Name",
        'id':"I13", 
        'rnum':"24",
        'constrained':False
        } )

#    Context_Parameter['domain'] = 'DMV'
#    Context_Parameter['class'] = 'Car'
#
#    parser.new_class( {'name':'Car', 'alias':'CAR' } )
#    parser.new_ind_attr( { 'name':'State', 'id':"I13" } )
#    parser.new_ind_attr( { 'name':'Title', 'id':"I" } )
#    parser.new_ind_attr( { 'name':'VIN', 'id':"I2" } )
#    parser.new_ind_attr( { 'name':'License Number', 'id':"I3" } )
#    parser.new_ind_attr( { 'name':'Manufacturer', 'id':"I2" } )
#    parser.add_id_commands()




