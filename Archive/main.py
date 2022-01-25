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
#filenames = ["verilogFiles/test.v", ]
filenames = ["verilogFiles/uart.v", ]

include_dirs = []
c = HdlConvertor()
d = c.parse(filenames, Language.VERILOG, include_dirs, hierarchyOnly=False, debug=True)
#tv = ToVerilog(sys.stdout)
#tv.print_context(d)

#print(d.objs[1].objs)
#print(d.objs[1].objs[0].name)
#print(d.objs[1].objs[0])
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
print(dir(d.objs[1].objs[0].body.body[0]))
print(d.objs[1].objs[0].body.body[0].if_true.src)
print(d.objs[1].objs[0].body.body[0].if_false.src)
print(dir(d.objs[1].objs[0].body.body[0].elifs))
print(d.objs[1].objs[0].body.body[0].cond)
print(d.objs[1].objs[0].body.body[0].in_prepoc)
print(d.objs[1].objs[0].body.body[0].labels)
'''


#g = d.objs[1].objs[0]

#tv = ToVerilog(d)
#tv = HdlContext(d)

#print(tv)

#tv.print_context(d)



#print('##########')


'''
for o in d.objs:
    print(o)
    print('##########')
    for i in o.objs:
        print('here',i)
'''
