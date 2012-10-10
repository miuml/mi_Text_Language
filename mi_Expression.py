#! /usr/bin/env python

"""
Class: Expression

The grammar of an miUML Text Script breaks down into a series of Statements,
Constructor Blocks and legal Expressions that actually specify the construction
of some Metamodel component.  Here we define the grammar of all Expressions.

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

# API
API_PATH = "../Resources/api_build_def.mi"
CMD_PREFIX = "UI_"

# Keywords and special characters
LIST_DELIM = '/' # List delimiter
REF_SYMBOL = '->' # Reference symbol
TYPE_SYMBOL = ':' # Data type designator

# Regex pattern building blocks
SPACE = r'\s*' # Stretch of whitespace
NAME = r'\w[\w\s]*\w' # Spaces must be rtrimmed on extraction
TO_NAME = r'\w[\w\s:.,]*' # Target of attribute reference
LIST = SPACE + LIST_DELIM + SPACE
REF = SPACE + REF_SYMBOL + SPACE
TYPE = SPACE + TYPE_SYMBOL + SPACE
SUPER = r'<'
SUB = r'|'
ASSOC = r'^'

# _RS designates a regex string (uncompiled)
name_RS = r'(?P<name>' + NAME + ')'
alias_RS = r'(?P<alias>' + NAME + ')' # Domain, Subsystem, Class alias
domain_type_RS = r'(?P<type>(modeled|realized))?'
range_RS = r'(?P<floor>\d+)-(?P<ceiling>\d+)' # Range of values, ex: 1-100
opt_cnum_RS = '(' + LIST + r'(?P<cnum>\d+)' + ')?' # optional <num>

#mult_RS = r'(?P<mult>>>?0?)'
#from_class_RS = r'(?P<from_class>' + NAME + ')'
#to_class_RS = r'(?P<to_class>' + TO_NAME + ')'
#phrase_RS = r'(?P<phrase>' + NAME + ')'
#to_name_RS = r'(?P<to_name>' + NAME + ')' # Referenced attribute

# Full pattern names for readability
name_alias_domain_type_RS = LIST.join( [name_RS, alias_RS, domain_type_RS] )
name_alias_range_RS = LIST.join( [name_RS, alias_RS, range_RS] )
name_alias_opt_cnum_RS = LIST.join( [name_RS, alias_RS] ) + opt_cnum_RS


#persp_RS = from_class_RS + LIST + phrase_RS + mult_RS + to_class_RS
#superclass_RS = name_RS + SPACE + SUPER
#subclasses_RS = NAME + SUB + r'.*'
#assoc_class_RS = ASSOC + SPACE + name_RS
#name_alias_RS = LIST.join( [name_RS, alias_RS] )

# Attribute expression
opt_id_RS = '(' + LIST + r'(?P<id>I[2-9]*)' + ')?'# identifier tags: I[, I2, ... ]
opt_derived_RS = r'((?P<derived>\\)\s*)?'
opt_type_RS = '(' + TYPE + r'(?P<type>' + NAME + '))?'
opt_deriv_attr_opt_type_opt_id_RS =  opt_derived_RS + name_RS + opt_type_RS + opt_id_RS

# Referential attribute expression
from_attr_RS = r'(?P<from_attr>' + NAME + ')'
to_attrs_RS = r'\s*->\s*(?P<to_attrs>\w[\w.:,\s]*\w)'
rnum_opt_c_RS = LIST + r'R(?P<rnum>\d+)(?P<constrained>c)?' # R<num>
from_attr_to_attrs_opt_id_rnum_opt_c_RS = from_attr_RS + to_attrs_RS + opt_id_RS + rnum_opt_c_RS

# { section:<expressions>, ... }
# expressions -> ( ( name:expr_name, <patterns>, call:api_call_name ), ... )
# patterns -> ( <re>, ... )

# A section defines one or more legal statemeents
# each of which is defined by a regex
Expression = { # Expression modeled class implemented as dict
    'domain':(
        {
            'name':'new_domain',
            'patterns':( re.compile( name_alias_domain_type_RS ), ),
            'call':'new_domain'
        },
    ),
#    'bridges':(
#        {
#            'name':'new_bridge',
#            'patterns':( re.compile( client_service_RS ), ),
#            'call':'new_bridge'
#        },
#    ),
    'subsystem':(
        {
            'name':'new_subystem',
            'patterns':( re.compile( name_alias_range_RS ), ),
            'call':'new_subsystem'
        },
    ),
    'classes':(
        {
            'name':'new_class',
            'patterns':( re.compile( name_alias_opt_cnum_RS ), ),
            'call':'new_class'
            'extract':'new_class_ids'
        },
    ),
    'attributes':(
        {
            'name':'new_ind_attr',
            'patterns':(
                re.compile( attr_opt_type_opt_id_RS ), ),
            'call':'new_ind_attr',
            'extract': 'parse_ids'
        },
        {
            'name':'new_ref_attr',
            'patterns':(
                re.compile( ref_opt_id_rnum_RS ), ),
            'call': None, # No API call, data saved for later command
            'extract': 'save_refs'
        }
    ),
#    'relationships':(
#        {
#            'name':'active_persp',
#            'patterns':( re.compile( rnum_persp_RS ), ),
#            'call':'new_bin_rel'
#        },
#        {
#            'name':'passive_persp',
#            'patterns':( re.compile( persp_RS ), ),
#            'call':'new_bin_rel'
#        },
#        {
#            'name':'assoc_class',
#            'patterns':( re.compile( assoc_class_RS ), ),
#            'call':'new_bin_rel'
#        },
#        {
#            'name':'superclass',
#            'patterns':( re.compile( superclass_RS ), ),
#            'call':'new_gen'
#        },
#        {
#            'name':'subclass',
#            'patterns':( re.compile( subclass_RS ), ),
#            'call':'new_gen'
#        }
#    )
}


if __name__ == '__main__':
    from pprint import pprint
    print()
    pprint( Expression )
    print()
    
