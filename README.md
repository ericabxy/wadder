# Wadder

a python script for working with WAD and related binary file formats.

## Background

WAD is a portable data archive format. It was created for Doom-engine 
games to store game-data separately from the executable.

## Usage

Passing a filename as the command-line parameter results in a printout 
of the WAD header information along with a short message about whether 
the parser thinks this is a valid WAD. The rest of the functionality 
depends on apporopriate tags passed as command-line parameters. A 
filename must always be the last parameter on the command-line.

<pre>
--data=&lt;Name>

        Print a single data point for an entry in the directory 
        indicated by "--index=". "Name" can be any string, but Wadder 
        only stores data named "filepos", "size", or "name" as that is 
        how a WAD is formatted. This may be made more flexible in the 
        future.

--end=&lt;number>

        Set the last entry to index when using "--list-range".

--entry=&lt;index>

        Print out the metadata for a single entry in the directory.

--find=&lt;name>

        Find and print any matching lump names. Will also match any lump 
        names that begin with "name" and will save each found lump if 
        the "--save" flag is set.

--index=&lt;number>

        Set the number of the directory entry that will be looked up. 
        This is also the first entry to be printed when using 
        "--list-range" and will be the last entry unless "--end=" is set 
        after this flag.

--length

        Print the length of the directory.

--list

        Print out the entire directory with each entry on a new line and 
        " " used as a separator between metadata. If the "--indexed" 
        flag is set, prepend each entry with its index in the directory.

--list-range

        Print out a slice of the directory starting with the entry set 
        by "--index=" or and ending with the entry set by "--end=".

--save

        Used with "--list-range" and "--find" to save each lump listed 
        as a binary file with the ".lmp" extension.

--save=&lt;number>

        Save the lump defined in the directory at "number" as a binary 
        file with its name from the directory and a ".lmp" extension. 

</pre>

## Details

WAD files have a 12-byte header, the first 4 bytes of which are "Magic 
Bytes" which identify the file as an "IWAD" or a "PWAD". Presumably, any 
four-letter word ending in "WAD" could be used to identify a WAD file if 
more WAD-like formats are created.

The rest of the header specifies the number of "lumps" (essentially 
files) in the WAD and the location of the lump directory. The directory 
likewise specifies the location, size, and name of every lump in the 
WAD. These features of the format make it very easy and fast to parse 
out all of the information contained in a WAD.

## About the ".lmp" Extension

The filename extension ".lmp" identifies a file formatted in exactly the 
same way as it would exist inside a WAD. It is usually seen in the names 
of text files that are to be inserted directly into a WAD, like the 
"dehacked.lmp" file that signals the engine's internal DeHackEd 
utilities. Wadder extracts lumps from a WAD in the exact state they are 
found without converting or reformatting them, so the ".lmp" extension 
is used to name the file.

## Issues

Wadder doesn't preform many checks on the file supplied or the 
command-line arguments. If your command-line argument is malformed, 
Python may raise an error and exit. Wadder does check if the Magic Byte 
"?WAD" is present in the header, but it will parse a file anyway if you 
tell it to.
