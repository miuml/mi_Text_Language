# This is the ATC example expressed in miUML text

# section makers are never indented, and everything else must be indented
# this avoids keyword collisions in model element names
# all other indentation is optional, but this file suggest a good style to use

domain # Marks a new section, sections must be in the correct sequence (domain, subsys, etc)
    Air Traffic Control / ATC # / is better than comma, easier to read and easy to type
    # above ordering expected after domain keyword is <name> / <alias>
    # / is a general purpose seperator for 'also named', 'described by'

types  # 
    Experience Level : Posint # : means 'based on' or 'using'
    Employee ID : Nominal

loops  # Empty section is okay
# lineages - sections must be in order, but may be entirely omitted if there is no content

subsystem # Now we have the modeled content organized within subsystems
    Air Field Management / AF # The ordering <name> / <alias> is expected here

classes
    Air Traffic Controller / ATC / 1 # Class number is optional
        ID : Employee ID / I # Use the colon just like on the class diagram
        Name # If no type is specified, look for one with a matching name
        Rating : Experience Level # Space
        Station -> Duty Station.Number / R3

    Duty Station / DS
        Number : Nominal / I
        Location : Name
        Capacity : Posint

    Shift Specification / SHIFT_SPEC
        Name / I
        Min break : Duration
        Max shift : Duration

    Off Duty Controller / OFF
        ID -> ATC.ID / I / R1
        Last shift ended : Date

    On Duty Controller / ON
        ID -> ATC.ID / I / R1
        Time logged in : Date

relationships
    R1 # name
    Air Traffic Controller < # superclass
        On Duty Controller | Off Duty Controller # subclasses
        # The pipe character tells us that this is a list of subclasses

    R2
    # multiplicity is >, >>, >0 or >>0 for 1, 1..*, 0..1 and 0..*, respectively
    On Duty Controller / is directing traffic within >>0 Control Zone # active phrase on top
    Control Zone has traffic directed by 1 On Duty Controller

    R3
    On Duty Controller / is logged into > Duty Station
    Duty Station / is being used by >0 On Duty Controller

lifecycles

states

events

transitions

non-transitions

# assigners

# actions
