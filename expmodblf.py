#!/usr/bin/env python
# This is a script to read the asterisk user table and create a blf setup for the aastra expansion modules.
#
# MIT License
#
# Copyright (c) 2017 Scott Price
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from subprocess import check_output
import string
import sys
import os

expmod = 1
key = 1


def blfString(ext, name):
    global key, expmod
    modstr = "expmod" + str(expmod) + " key" + str(key)
    outstr = ""
    outstr = outstr + modstr + " type: blf/xfer" + os.linesep
    outstr = outstr + modstr + " label: " + str(name) + os.linesep
    outstr = outstr + modstr + " value: " + str(ext) + os.linesep
    outstr = outstr + os.linesep
    return outstr


def incKey():
    global key, expmod
    key += 1
    if key > 60:
        expmod += 1
        key = 1
        if expmod > 3:
            exit()


def parking():
    outstr = ""
    values = check_output(['asterisk', '-rx', 'parking show'])
    values = string.split(values, '\n')
    extensions = {}
    conferences = {}
    conf = 1
    start = None
    end = None
    for k in values:
        line = string.split(k, ":")
        if 'Spaces' in line[0]:
            space = string.split(line[1], "-")
            start = int(space[0])
            end   = int(space[1])
    if start is not None:
        for park in range(start, end + 1):
            outstr = outstr + blfString(park, "Park " + str(park))
            incKey()

    return outstr

def main():
    global key, expmod
    fptr  = None
    if (len(sys.argv) > 1):
        fname = str(sys.argv[1]).replace('/', '').replace('\\', '')
        if len(fname) > 0:
            fptr = open(fname, 'w')
            if os.path.isfile(fname + ".in"):
                infile = open(fname + ".in")
                fptr.write(infile.read())

    values = check_output(['asterisk', '-rx', 'database show'])
    values = string.split(values, '\n')
    extensions = {}
    conferences = {}

    for k in values:
        line = string.split(k, ":")
        if 'cidname' in line[0]:
            ext = string.split(line[0], "/")[2]
            extensions[ext] = line[1].strip()
        elif 'CONFERENCE' in line[0] and 'exten' in line[0]:
            ext = line[1].strip()
            conferences[ext] = "Conf " + str(ext)

    outstr = parking()

    for ext in sorted(conferences.iterkeys()):
        outstr = outstr + blfString(ext, conferences[ext])
        incKey()

    for ext in sorted(extensions.iterkeys()):
        outstr = outstr + blfString(ext, extensions[ext])
        incKey()

    if fptr is None:
        print outstr
    else:
        fptr.write(outstr)

if __name__ == "__main__":
    main()
