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


def main():
    values = check_output(['asterisk', '-rx', 'database show'])
    values = string.split(values, '\n')
    extensions = {}
    for k in values:
        line = string.split(k, ":")
        if 'cidname' in line[0]:
            ext  = string.split(line[0], "/")[2]
            extensions[ext] = line[1]

    expmod = 1
    key = 1

    for ext in extensions:
        modstr = "expmod" + str(expmod) + " key" + str(key)
        print modstr + " type: blf"
        print modstr + " label: " + extensions[ext]
        print modstr + " value: " + ext
        key += 1
        if key > 60:
           expmod += 1
           key = 1
           if expmod > 3:
              exit()



if __name__ == "__main__":
    main()
