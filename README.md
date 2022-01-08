# Wadder

A python script for working with WAD and related binary file formats.

## Background

WAD is a portable data archive format. It was created for Doom-engine 
games to store game-data separately from the executable.

## Usage

Passing a filename as the command-line parameter results in a printout 
of the WAD header information along with a short message about whether 
the parser thinks this is a valid WAD. The rest of the functionality 
depends on apporopriate tags passed as command-line parameters. A 
filename must always be the last parameter on the command-line.

--entry "index"

        Print out the metadata for a single entry in the directory.

--filepos "index"
--name "index"
--size "index"

        Print a single data point for an entry in the directory.

--find="name"

        Find and print any matching lump names. Will also match any lump 
        names that begin with "name"

--length

        Print the length of the directory.

--list
--indexed-list

        Print out the entire directory with each entry on a new line and 
        " " used as a separator between each part of the entry's 
        metadata. The "indexed" version prints the lump number before 
        the metadata.

--list="begin" "end"

        Print out the part of the directory between entries "begin" and 
        "end" inclusive. Otherwise behaves as "--list"

--save "index"

        save the lump as a binary file named with its name from the 
        directory and a ".binary" extension

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

## Issues

Wadder doesn't preform many checks on the file supplied or the 
command-line arguments. If your command-line argument is malformed, 
Python may raise an error and exit. Wadder does check if the Magic Byte 
"?WAD" is present in the header, but it will parse a file anyway if you 
tell it to.
