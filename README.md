# Wadder

a collection of Python scripts for working with WAD and related binary 
file formats

## Background

WAD is a portable data archive format. It is used Doom-engine games to 
store game-data separately from the executable.

## Requirements

Wadder uses standard Python libraries.

## Usage: wadder.py

- <code>python3 wadder.py "filename"</code>
- <code>python3 wadder.py "parameters" "filename"</code>

If given a filename, this script will determine if the file has a valid 
WAD header and print the header information. The last parameter on the 
command line is taken as the filename. Other capabilities of this script 
are accessed via additional command-line parameters.

- examples:
  + <code>python3 wadder.py --list Valiant.wad</code>
  + <code>python3 wadder.py --index=100 --end=120 --list freedm.wad</code>
  + <code>python3 wadder.py --indexed --find=VILE freedoom2.wad</code>
  + <code>python3 wadder.py --find=PLAYPAL --save aaliens.wad</code>

The script can list the metadata for every entry in the WAD directory, 
or limit the list to a range indicated by "--index=" and "--end=". It 
can also find entries by name with "--find=" and it will save the lump 
data for every entry listed/found as a ".lmp" file if you pass the 
"--save" flag. For more information and features, access the help text 
using the following flag.

- <code>python3 wadder.py --help</code>

## Usage: paller.py

- <code>python3 paller.py "filename"</code>
- <code>python3 paller.py --index=13 --save-lump "filename"</code>
- <code>python3 paller.py --index=9 --save-hexmap "filename"</code>
- <code>python3 paller.py --index=0 --save-pixmap "filename"</code>

This script works with the 24bpp binary palette PLAYPAL format. It's 
designed to take a PLAYPAL lump file and split it into its 14 component 
256-color maps. It can save these as smaller binary lumps, hex values in 
a text file, or render them as 256-color pixmaps.

## Usage: patter.py

- <code>python3 patter.py "filename"</code>
- <code>python3 patter.py --save-pixmap "filename"</code>
- <code>python3 patter.py --colormap=PLAYPAL0.lmp --save-pixmap "filename"</code>

This script works with lump files formatted in DOOM "picture format". It 
can render the binary data as a 256-color pixmap with a transparency 
mask. If you do not supply it with a PLAYPAL colormap data lump it will 
render the image with 256 gray shades instead of the intended colors.

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

Lumps that are extracted from the WAD and saved as ".lmp" files can be 
worked on using the other scripts in this collection.

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
can be programmed to access a longer header if indicated. Wadder can be 
programmed to collect more metadata from the directory and retrieve it 
with extended metadata names.
