# RBI Baseball 3 - ROM Modifier
# Brahm Neufeld
# December 2013
# This file generates patch files that will turn the original RBI 3 ROM into the modified 2013 version.

import time
import binascii
from Values import *


# function to compare two strings, print the positions
# and values of any DIFFERENCES
def character_compare(a,b):
    output = ""
    for i in range(len(a)):
        if a[i] != b[i]:
            # print to the console
            # print(i, b[i])
            # print to the file
            output += str(i) + "\t" + str(b[i]) + "\n"
    return output


# function to create a patchfile
# to update:
# # right now the 1990 ROM and patch file are defined as globals.
# # in the future the 1990 ROM will be a user-updated file, but the patchfile will live on the server.
# # remember, when the user uploads a 1990 ROM, the server should destroy it when it's done.
def create_patchfile(original_1990_rom, modified_2013_rom):
    with open(original_1990_rom, "rb") as rom_1990:
        data_1990 = rom_1990.read()
        data_1990 = str(binascii.hexlify(data_1990))

    with open(modified_2013_rom, "rb") as rom_2013:
        data_2013 = rom_2013.read()
        data_2013 = str(binascii.hexlify(data_2013))

    with open(time.strftime("%Y-%m-%d_%H-%M-%S") + ".pch", "w+") as f:
        f.write(character_compare(data_1990, data_2013))
        f.close()


# take a patch file and use it to recreate the 2005/2013 ROM using the 1990 ROM as a base.
# the program will have to take the PATCHED 1990 file then apply any user-initiated changes to it...
# then serve the all-changed-up file back to the user.
# to do:
# # the user will have to upload the 1990 file to the server... it can't live on the server.
def modify_1990_file(original_1990_rom, patchfile_filename, new_file_filename):
    # ok let's go to town on this ROM patch file thingamajig
    with open(original_1990_rom, "rb") as rom_1990:
        # use hexlify to read in the rom file as the hex characters
        data_1990 = binascii.hexlify(rom_1990.read())
        # put each character of the 1990 ROM in a list - easiest way to work with strings
        data_1990 = list(str(data_1990))
        with open(patchfile_filename, "r") as patch_file:
            # read in the patch file as an array of lines, 1st value is offset and 2nd value is the value to patch in.
            patch_array = patch_file.readlines()
            # remove the tab and newline characters from my nice purdy strings... yeah that's real nice mmmmhmmmmmmm
            patch_array = [x.replace("\t", " ").replace("\n", "") for x in patch_array]
            # now we need to do something to some elements in the data_1990 array - the ones to patch up to 2013.
            # so for each value in patch_array, look up the data_1990 hex string position and replace the data
            i = 0
            for x in patch_array:
                # each patch_array element is a string that looks like this: "1234 A" ("character_offset  value_to_replace")
                # so we have to split them into a little array
                split = patch_array[i].split()
                # the first split string (array position 0) is actually an integer position so we have to
                # turn it into an int, look up the position, and assign the second split string (array pos 1)
                # which is the hexadecimal replacement data to be patched into the 1990 ROM
                data_1990[int(split[0])] = split[1]
                # increment i. Good 'ole i. Here boy... we're going out to the farm. It'll all be over soon.
                i+=1
        # ok, remember that list we made out of the 1990 ROM characters? Let's get that back in a big ass string.
        data_1990 = "".join(data_1990)
        # praise be to carlos satanas if this can actually write to a new binary .nes file!
        # i learned it from youuuuuuuu: http://tinyurl.com/odeh844
        with open(new_file_filename, "wb") as f:
            # holy SHIT this was a hard one to crack. Have to remove the prefix b' and take off the last ' character
            # or else will end up with the "odd-length string" error.
            data_1990 = data_1990.rstrip("'").lstrip("b'")
            # write dat file
            f.write(binascii.unhexlify(data_1990))

def write_to_web_logfile(message):
    """
    Simple logging tool for use on the website
    Opens a logfile (permissions must be manually set for it on webserver) and writes a message to it.
    LOGFILE MUST EXIST ON SERVER WITH PERMISSIONS SET.
    """
    with open(ROOT_DIRECTORY + "rbi.log", "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S") + " - " + message+"\n")
        f.close()

def main():
    # Uncomment create_patchfile() whenever we need to create a new "base" patch file from the hacking and cracking
    # that BN is doing with the original ROM file. The patchfile can then be applied to every modified ROM to set up
    # proper 2013 teams, menu layouts, etc.
    # create_patchfile()

    # Uncomment modify_1990_file() whenever we want to apply the base patch to a newly uploaded 1990 ROM file.
    # modify_1990_file()
    do="nothing"

if __name__ == "__main__":
    main()
