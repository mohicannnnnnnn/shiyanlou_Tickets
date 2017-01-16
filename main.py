# coding: utf-8

"""get ticket from terminal
Usage:
    Ticket [-hgdtkz] <src_city> <dest_city> <date>
Options:
    -h help
    -g gaotie
    -d dongche
    -t tekuai
    -k kongtiao
    -z zhida
Example:
    Ticket -g luoyang xian 2017-2-5
"""

import getopt
import sys

try:
    opt, arg = getopt.getopt(sys.argv[1:], "hgdtkz")
    print opt, arg
except getopt.GetoptError:
    print "Please check your arguments"
