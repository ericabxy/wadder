# Wadder

a collection of Python scripts for working with WAD and related binary 
file formats

## Background

WAD is a portable data archive format. It is used Doom-engine games to 
store game-data separately from the executable.

## Requirements

Wadder uses standard Python libraries.

## Usage

The main script is "wadder.py". Below is some quick-and-dirty 
documentation that will eventually be included as command-line "help" 
output.

Passing a filename as the sole command-line parameter results in a 
printout of the file's WAD header information along with a short message 
about whether the parser thinks it is a valid WAD. More specific 
features are accessed via additional command-line parameters. A filename 
must always be the last parameter on the command-line.

The "directory" is a list of every lump in the WAD with associated 
metadata. An "entry" contains all metadata for a lump in the directory. 
An "index" is the number of an entry in the directory. Use the 
command-line paramaters as described below to control what Wadder does 
with the directory, the metadata, and the lump data.

<pre>

--data=filepos
--data=size
--data=name

        Add the specified key to the list of metadata to print for each 
        entry. By default for each entry Wadder will print all three 
        metadata, so normally this is not needed. However it can be used 
        to re-add to the list of metadata if it was removed with 
        "--data-only=".

--data-only=filepos
--data-only=size
--data-only=name

        Clear the list of metadata to print for each entry, and replace 
        it with only the key specified. If more metadata is needed, use 
        "--data=" to add more to the list.

--end=N

        Set the last entry to index (inclusive) when using "--list". 
        Defaults to the last entry in the directory.

--entry=N

        Print all metadata for a single entry in the directory at index 
        N.

--find=string

        Find and print the entry for any lumps which have a name 
        starting with "string". Also save each matching lump if the 
        "--save" flag is set.

--header-identification
--header-numlumps
--header-infotableofs

        Print the requested header information.

--index=N

        Set the first entry to index when using "--list". Defaults to 
        the first entry [0].

--indexed

        Prepend each entry listed by printing its index before the 
        metadata.

--length

        Print the length of the directory.

--list

        Print each entry in the directory starting with "--index=" and 
        ending with "--end=". Each entry is printed on a new line with a 
        " " separator between each metadata. If the "--indexed" flag is 
        set, prepend each entry with its index in the directory. If the 
        "--save" flag is set, save each entry listed as a raw lump file.

--save

        Save the lump data from each entry listed as a binary file with 
        the ".lmp" extension.

--save=N

        Save the lump data from the entry specified by N as a binary 
        file with the ".lmp" extension.

</pre>

## Details

WAD files have a 12-byte header, the first 4 bytes of which are "Magic 
Bytes" which identify the file as an "IWAD" or a "PWAD". Presumably, any 
four-letter word ending in "WAD" could be used to identify a WAD file if 
more WAD-like formats are created.

The rest of the header specifies the number of "lumps" (essentially 
files) in the WAD and the location of the lump directory. The directory 
likewise specifies the location, size, and name of every lump in the 
WAD. These features of the format make it easy to parse all the 
information contained in a WAD.

## About the ".lmp" Extension

The filename extension ".lmp" identifies a file formatted in exactly the 
same way as it would exist inside a WAD, such as the Doom picture 
format. It is usually seen in the names of text files that are to be 
inserted directly into a WAD, like the "dehacked.lmp" file that signals 
the engine's internal DeHackEd features. Wadder extracts lumps from a 
WAD in the exact state they are found without converting or reformatting 
them, so the ".lmp" extension is used to name each extracted file for 
clarity.

## Issues

Wadder doesn't preform many checks on the file supplied or the 
command-line arguments. If your command-line argument is malformed, 
Python may raise an error and exit. Wadder does check if the Magic Byte 
"?WAD" is present in the header, but it may parse a file anyway if you 
tell it to.

## Future Considerations

If new WAD formats are created in the future, Wadder can accomodate 
them. Wadder recognizes anything with "?WAD" on the first 4 bytes and 
can be programmed to access a longer header if present. Wadder can be 
programmed to collect more metadata from the directory and retrieve it 
with extended metadata names.
