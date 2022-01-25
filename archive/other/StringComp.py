#   Bayley King
#   Python 3.7.3 
#   String Comp for fitness function

from HereBoy import HereBoy

class StringComp (HereBoy):
    def __init__(self):
        self.ops = ['or','and','not']
        self.diffCount = 0


    def compare(self,tree1,tree2):
        tree1,tree2 = self.structure(tree1,tree2)
        return self.nodes(tree1,tree2)
    
    
    def structure(self,tree1,tree2):
        elemCount = max(len(tree1),len(tree2))
        if len(tree1) < len(tree2):
            treeLen = True
        elif len(tree1) > len(tree2):
            treeLen = False

        
        for elem in range(elemCount):
            try:
                if tree1[elem] in self.ops and tree2[elem] not in self.ops:
                    self.removeSubTree(tree1,elem)
                    self.diffCount += 1
                elif tree1[elem] not in self.ops and tree2[elem] in self.ops:
                    self.addSubTree(tree1,elem,tree2(elem))
                    self.diffCount += 1
                else:
                    pass
            except:
                if treeLen:
                    while treeLen:
                        if len(tree1) == len(tree2):
                            break
                        tree1.insert(-1,None)
                        self.diffCount +=1
                else:
                    while not treeLen:
                        if len(tree1) == len(tree2):
                            break
                        tree1.pop(-1)
                        self.diffCount +=1
        return tree1,tree2


    def nodes(self,tree1,tree2):
        for elem in range(len(tree1)):
            if tree1[elem] != tree2[elem]:
                tree1[elem] = tree2[elem]
                self.diffCount +=1
        return tree1,tree2
            
    
    def removeSubTree(self,tree,elem,extraCount=2,num=0,stillTree=True):
        t1 = tree[:elem]
        t2 = tree[elem:]

        while stillTree:
            num += 1
            children = t2[num:num+2]
            if children[0] in self.ops and children[1] in self.ops:
                extraCount += 2
            elif children[0] in self.ops:
                extraCount += 1
            elif children[1] in self.ops:
                extraCount += 1
            else:
                stillTree = False

        t2 = t2[num+extraCount:]
        t2.insert(0,None)

        tree = t1+t2
        return tree

    def addSubTree(self,tree,elem,op):
        t1 = tree[:elem]
        t2 = tree[elem:]
        return t1+[op,None,None]+t2



    # Random selection?
    # first node in tree?
    # does it matter to look at the children in the tree?
    # insert node with blanks?
    # Weight all modifications the same?
    # for now, no mapping, simple padding




def main():

    newTree2 = ['or','in1','and','in1','or','in1','in2']
    #newTree1 = ['or','in1','and','in1','or','in1','in2']
    newTree1 = ['or','in1','in2']
    if len(newTree1) > len(newTree2):
        tree2 = tuple(newTree1)
        tree1 = newTree2
    elif len(newTree1) < len(newTree2):
        tree2 = tuple(newTree2)
        tree1 = newTree1
    else:
        tree2 = tuple(newTree1)
        tree1 = newTree2

    testComp = stringComp(tree1,tree2)

    testComp.structure()
    print(testComp.diffCount)
    print(testComp.tree1,'\n',testComp.tree2)

    testComp.nodes()
    print(testComp.diffCount)
    print(testComp.tree1,'\n',testComp.tree2)

if __name__ == "__main__":
    main()