# This is the miUML metamodel example expressed in miUML text

# If we can express this beast in text, we can probably express any miUML model
# though, at this point, it consists only of a class model

domain
    miUML Metamodel / MIUML / modeled

subsystem
    Class / CLASS / 1-50

classes
    Attribute / ATTR
        Name / I
        Class -> Class.Name / R20
        Domain -> Class.Domain / R20 # No target name, so use same name: Class.Domain

    Attribute in Derivation / ATTR_IN_DERIV
        Source attribute -> Attribute.Name / I / R26c
        Source class -> Attribute.Class / I / R26c
        Target attribute -> Derived Attribute.Name / I / R26
        Target class -> Derived Attribute.Class / I / R26
        Domain -> Attribute.Domain, Derived Attribute.Domain / I / R26

    Class / C
        Name / I
        Cnum : Nominal / I3
        Alias : Short name / I4
        Domain -> Subsystem Element.Domain / I234 / R14
        Element -> Subsystem Element.Number / I2 / R14

    Derived Attribute / DATTR
        Name -> Native Attribute.Name / I / R25
        Class -> Native Attribute.Class / I / R25
        Domain -> Native Attribute.Domain / I / R25
        Formula : Description

    Identifier / ID
        Number : Nominal / I
        Class -> Class.Name / I / R27
        Domain -> Class.Domain / I / R27

    Identifier Attribute / ID_ATTR
        Identifier -> Identifier.Number / I / R22
        Attribute -> Attribute.Name / I / R22
        Class -> Identifier.Class, Attribute.Class / I / R22
        Domain -> Identifier.Domain, Attribute.Domain / I / R22

    Independent Attribute / IND_ATTR
        Name -> Native Attribute.Name / I / R25
        Class -> Native Attribute.Class / I / R25
        Domain -> Native Attribute.Domain / I / R25

    Modeled Identifier / MID
        Number -> Identifier.Number / I / R30
        Class -> Identifier.Class / I / R30
        Domain -> Identifier.Domain / I / R30

    Native Attribute / NAT_ATTR
        Name -> Attribute.Name / I / R21
        Class -> Attribute.Class / I / R21
        Domain -> Attribute.Domain / I / R21
        Type -> Type::Constrained Type.Name / R24

    Non Specialized Class / NON_SPEC
        Name -> Class.Name / I / R23
        Domain -> Class.Domain / I / R23

    Referential Attribute / REF_ATTR
        Name -> Attribute.Name / I / R21
        Class -> Attribute.Class / I / R21
        Domain -> Attribute.Domain / I / R21
        \ Type

    Referential Role / REF_ROLE
        Reference type -> Formalization::Reference.Type / R31 / I
        From class -> Formalization::Reference.From class, Referential Attribute / R31 / I
        To class -> Formalization::Reference.To class, / R31 / I
        Rnum ->Formalization::Reference.Rnum / R31 / I
        Domain ->Formalization::Reference.Domain, Referential Attribute.Domain / R31 / I
        From attribute -> Referential Attribute.Name / R31 / I

        To identifier -> Identifier Attribute.Identifier / R32
        To attribute -> Identifier Attribute.Attribute / R32c
        To class -> Identifier Attribute.Class / R32c / I
        Domain ->Identifier Attribute.Domain / R32 / I


relationships
    R20 / Attribute / characterizes > Class
    Class / is characterized by >> Attribute

    R21 / Attribute <
        Native Attribute | Referential Attribute

    R22 / Identifier / requires >> Attribute
    Attribute / is required in >>0 Identifier
        ^ Identifier Attribute

    R23 / Class <
        Non Specialized Class | Relationship::Specialized Class

    R24 / Type::Constrained Type / defines range of values assignable to >>0 Native Attribute
    Native Attribute / may assume values defined by > Type::Constrained Type

    R25 / Native Attribute <
        Derived Attribute | Independent Attribute

    R26 / Derived Attribute / is derived from >> Attribute
    Attribute / contributes to the value of >>0 Derived Attribute
        ^ Attribute in Derivation

    R27 / Identifier / uniquely distinguishes instances of > Class
    Class / has instances uniquely distinguished by >> Identifier

    R30 / Identifier <
        Modeled Identifier | RR Identifier::Required Referential Identifier

    R31 / Formalization::Referential Attribute / consists of >> Referential Attribute
    Referential Attribute / is part of >> Reference

    R32 / Referential Role / references value of > Identifier Attribute
    Identifier Attribute / value is referenced by >>0 Referential Role
