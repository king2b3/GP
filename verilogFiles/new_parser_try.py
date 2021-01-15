import os
import sys

from hdlConvertorAst.language import Language
from hdlConvertor import HdlConvertor

from hdlConvertorAst.to.verilog.verilog2005 import ToVerilog2005

from hdlConvertorAst.to.common import ToHdlCommon
import json

#TEST_DIR = os.path.join("..", "tests", "verilog")  # uncomment for song in these directories
#filenames = [os.path.join(TEST_DIR, "dff_async_reset.v"), ]

filenames = "ff.v" 
include_dirs = []
c = HdlConvertor()
# note that there is also Language.VERILOG_2005, Language.SYSTEM_VERILOG_2017 and others
d = c.parse(filenames, Language.VERILOG, include_dirs, hierarchyOnly=True, debug=True)

for o in d.objs:
    print(o)

''' Right now we are trying to find a clean way to look at the code, this seems to do it, but 
      we might be shit out of luck with these compilers working the wya we though.
    We might have to suck up and code these ASTs by hand for now. 
'''