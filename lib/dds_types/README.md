# How to create a new type
First use srpkg tool to create a new type package and give it a descriptive name. They should be in CamelCase.

Then write an IDL file and run the script to auto generate the includes. They almost write like C/C++ structs. You cannot use primitive types as IDL types. Instead, they have to be encapuslated within one of the supported complex types. Usually, this is almost always a struct. So just use a struct.

If you want to use a primitive as a type, there are premade types for you in standard_types. They are structs which contain a single variable of that type.

Click [here](https://community.rti.com/static/documentation/connext-dds/current/doc/manuals/connext_dds_professional/users_manual/users_manual/Translations_for_IDL_Types.htm#Table_DataTypesinIDL_C++PSM) to find what types are supported which you can include inside your struct.