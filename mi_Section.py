#! /usr/bin/env python

"""
Modeled Classes: Section, Section Sequence

An miUML Text Script is organized into a series of Sections.  The legal ordering
of Sections is determined, for miUML Text Scripts, by the loose miUML metamodel
taxonomy and a strategy for making text scripts easy to read and create.

Every text script must begin with a domain section since that is the highest level
of the miUML taxonomy.  For ease of specification, the 'domain' section is singular
which means that it begins the specification of a single domain.  The 'classes'
section, on the other hand has a multiple plurality (as suggested by the plural noun
name) since it can specify the construction of multiple classes.

From any given section it is possible to predict a set of legal following
domains.  For example, a domain section must be followed by either a types or
subsystems section.  It is an error for a domain section to be followed by
a classes section since the classes could not be associated with any subsystem.

The Legal Sequence association class / relationship captures this information.

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

# Global

# Complete set of legal section names, indented to show relative context
# Each seciton has a name corresponding to a miUML metaclass and either
# None indicating singular or a plural suffix indicating multiple objects
# are created in that section.
Section = {
    ('model', None ), # Not plural (one object of that type created)
        ('domain', None ),
            ( 'type', 's' ), # plural (multiple objects of that type created)
            ( 'subsystem', None ),
                ( 'class', 'es' ),
                ( 'relationship', 's' ),
                ( 'lifecycle', 's' ),
            ( 'loop', 's' ),
            ( 'lineage', 's' ),
        ( 'bridge', 's' )
    }

# Section grammar has been hand-parsed so that
# given a current section, we can determine which sections may
# appear next, taking into metamodel hierarchy, and whether or not a term
# is optional.
#
# Grammar for section headers:
#
# model -> { domain }, [<bridges>]
# domain -> [<types>], { subsystem }, [<cloops>], [<lineages>]
# subsystem -> [classes], [<relationships>], [<lifecycles>]
#
# Key: -> = 'is composed of', {} = 'one or more', [] = 'optional', <> = 'atomic'
#
Section_Order = {
    # <term> : <terms that may appear next> 
    'model':{ 'domain' }, # ex: if current_section is 'model', next must be 'domain'
    'domain':{ 'types', 'subsystem' },
    'types':{ 'subsystem' },
    'subsystem':{ 'classes', 'domain', 'bridges' },
    'classes':{
        'relationships', 'lifecycles', 'cloops', 'lineages', 'subsystem', 'domain', 'bridges'
    },
    'relationships':{
        'lifecycles', 'cloops', 'lineages', 'subsystem', 'domain', 'bridges'
    },
    'lifecycles':{
        'cloops', 'lineages', 'subsystem', 'domain', 'bridges'
    },
    'bridges':{ 'domain' },
    'cloops':{ 'lineages', 'subsystem', 'domain', 'bridges' },
    'lineages':{ 'subsystem', 'domain', 'bridges' }
}

# Constants

# Regex
section_RE = re.compile( r'^\s*(?P<name>\w+)\s*$' )

if __name__ == '__main__':
    from pprint import pprint
    print( "Section Names:\n" )
    pprint( Section )
    print( "\nSection Order:\n" )
    pprint( Section_Order )
    print()
