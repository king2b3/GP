#   Bayley King
#   Python 3.6.8
#   Main program for gen alogrithms


import sys
from hdlConvertor.language import Language
from hdlConvertor.toVerilog import ToVerilog
from hdlConvertor.hdlAst._structural import HdlContext
from hdlConvertor import HdlConvertor
import pickle
from ctypes import *

p1 = "verilogFiles"

#filenames = ["verilogFiles/addsub.v", ]
#filenames = ["verilogFiles/2-1mux.v", ]
filenames = ["verilogFiles/test.v", ]
#filenames = ["verilogFiles/uart.v", ]

include_dirs = []
c = HdlConvertor()

filenames = filenames[0]
d = c.verilog_pp(filenames, Language.VERILOG)

print(d)
#for i in d:
#    print(i)
'''
a = []
for x in range(len(d.objs[1].objs)):
    print(d.objs[1].objs[x])
    #print(dir(d.objs[1].objs[x]))
    if 'body' in dir(d.objs[1].objs[x]):
        a.append(d.objs[1].objs[x].body)
    elif 'src' in dir(d.objs[1].objs[x]):
        a.append(d.objs[1].objs[x].src)
print(a,'\n')


for i in a:
    print(i.if_false,'\n')


#print(dir(d.objs[1].objs[0]))
#print(d.objs[1].objs[0].src)
'''

