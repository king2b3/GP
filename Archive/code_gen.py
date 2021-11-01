''' Structural verilog code generator. Takes AST as list of strings,
      and generates structural verilog code. 

    Will probably be moved into other file

    Simple code gen, will do variable declerations, but output should be reviewed
      by the user.
    Created on: 2-1-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
'''

import operations as op
import csv

class createCode(object):
    ''' Structure to create structural verilog code in a text file

        self.ins : list of input as strings
        self.ast : list of nodes 
        self.file_str : string to be written to the file.
          String will have proper escape chacaters
    '''

    def __init__(self, ins, ast, filename='output.txt') -> None:
        self.ins = ins
        self.ast = ast
        self.body_str = ""
        self.temp_ast = None
        self.gate_counter = {
            'and': 0,
            'or': 0,
            'nand': 0,
            'nor': 0,
            'xor': 0,
            'not': 0
        }
        self.gate_fix = {
            'and': 'AND',
            'or': 'OR',
            'nand': 'NAND',
            'nor': 'NOR',
            'xor': 'XOR',
            'not': 'NOT'
        }

    def writeFile(self) -> None:
        ''' Writes structural file
            
            1. Module with input/output names
            2. input, output, wire
            3. Structural level verilog
            4. endmodule
        '''
        pass
    # create input blocks
    def prepAST(self):
        ''' Maps the AST to inputs and node names to a dictionary
              which will contain the 
        '''
        currentAST = self.ast.copy()
        while len(currentAST) > 1:
            currentAST = tempAST
            temp_len = len(currentAST)
            for node in range(temp_len):
                if op.checkBinaryGate(currentAST[node]):
                    # guesses that the next two nodes in the AST list are the node's children
                    children = currentAST[node+1:node+3]
                    try:
                        # if children are not gates
                        if type(children[0]) in self.ins and type(children[1]) in self.ins:
                            # splits small tree from AST
                            tempStart = currentAST[:node+1]
                            tempEnd = currentAST[node+3:]
                            # preforms logical operation on children

                            self.body_str += tempAST[node] + ' '
                            self.body_str += self.gate_fix[tempAST[node]] + '_' + str(self.gate_counter[tempAST[node]]) + ' '
                            self.body_str += '(' + self.gate_fix[tempAST[node] + '_' + str(self.gate_counter[tempAST[node]]) + ', '\
                                    str(childten[0]) + ', ' + str(childten[0]) +');\n'              
                            # combines logical result of the tree with old AST
                            tempAST = tempStart  + tempEnd
                            tempAST[node] = self.gate_fix[tempAST[node] + '_' + str(self.gate_counter[tempAST[node]])                    
                            self.gate_counter[tempAST[node]] += 1  
                            break
                    except:
                        # error check
                        sys.exit()

                elif op.checkSoloGate(currentAST[node]):
                    child = currentAST[node+1]
                    # if child is not a gate
                    if type(child) == bool:
                        tempStart = currentAST[:node+1]
                        tempEnd = currentAST[node+2:]
                        # preforms logical operation
                        self.body_str += tempAST[node] + ' '
                        self.body_str += self.gate_fix[tempAST[node]] + '_' + str(self.gate_counter[tempAST[node]]) + ' '
                        self.body_str += '(' + self.gate_fix[tempAST[node] + '_' + str(self.gate_counter[tempAST[node]]) + ', '\
                                str(child) +');\n'                          
                        # combines logical result of the tree with old AST
                        tempAST = tempStart  + tempEnd
                        tempAST[node] = self.gate_fix[tempAST[node] + '_' + str(self.gate_counter[tempAST[node]])
                        self.gate_counter[tempAST[node]] += 1
                        break

                '''
                elif op.checkStatementGate(currentAST[node]):
                    children = currentAST[node+1:node+3]
                    if type(children[1]) == bool:
                        tempStart = currentAST[:node+1]
                        tempEnd = currentAST[node+3:]
                        # preforms statement operation
                        tempResult = returnGate(currentAST[node],children)
                        # combines logical result with AST
                        tempAST = tempStart  + tempEnd
                        tempAST[node] = tempResult
                        break
                '''
        self.body_str += 'endmodule'