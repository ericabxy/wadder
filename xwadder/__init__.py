"""
Wadder - modules for handling the WAD file format.

Using some of the extensive documentation found at The Doom Wiki[1],
Wadder provides functions and classes designed to interpret and extract
binary data from files in WAD format. Generic modules can find and
extract the lumps from a WAD, while more specialized modules can parse
the binary data contained in generalized lumps. Game-specific modules
can interpret the data from specialized lumps.

MODULES

WAD (currently called Wads) - read the header and lump directory of a
WAD file and save individual lumps as binary files.

Doom - interpret lumps specifically formatted for the Doom engine and
various source ports (BOOM, MBF).

FOOTER

According to the Doom Bible, WAD is an acronym for "Where's All the
Data?". Alternatively, Wadder considers "Wad of Aggregate Data" to be
an appropriate backronym.

1: https://doomwiki.org/
"""
