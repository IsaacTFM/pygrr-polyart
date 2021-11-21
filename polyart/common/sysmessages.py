"""
This module prints a random message from "messages.txt" whenever it is ran or imported, and then exits.
To be imported in Pygrr's script's "__main__" call (if it does not do anything else).

See devnote.
"""

# import used modules
from random import choice
from sys import argv
from os.path import abspath, join
from time import sleep

# if this is the origin file (not imported)
if __name__ == "__main__":
    quit()

# locate the messages.txt file
# this is required as open() will try to open a file from the origin's directory, which is of an unknown relative position to this folder
filepath = abspath(join(__file__, "..", "..", "config", "sysmessages.txt"))

# open the file in reader mode
r = open(filepath, "r")
# split the entries by line
data = r.read().split("\n")
r.close()

# choose a random message and print message
print(f"{argv[0]} says:\n'{choice(data)}'")


# delay for 1.5 seconds
sleep(1.5)
# exit / quit
quit()
