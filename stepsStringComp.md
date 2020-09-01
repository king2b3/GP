# String Comp Steps

#### General Overview
1. Definitions 
    1. Left to Right
    2. Add, Del, and Sub only commands
    3. Tree1 is modded tree (list), Tree2 is original tree (tuple)
2. Count how many sub trees exist
    1. Use add / sub based off of this
3. Build same structure
    1. Direct Subs count as change
    2. Count NULL to val subs as change? 
        1. Count change in structure? 
        2. Count both

#### For Loop structure

Structure Check:
treeLen = max(len(Tree1,Tree2))
for elemCount in range(treeLen)
    is Tree1(elemCount) Op or Input?

        if Op AND Tree2(elemCount) is Input
            Remove sub tree and create blank node
            counter++

        elif Op AND Tree2(elemCount) is Op
            Pass

        elif Input AND Tree2(elemCount) is Input
            Pass

        elif Input AND Tree2(elemCount) is Op
            Insert Blank Op into Tree1
            counter++

compare string length
    if same
        continue
    else
        GoTo StructureCheck

for elemCount in range(treeLen)
    if Tree1(elemCount) == Tree2(elemCount)
        pass
    elif Tree1(elemCount) != Tree2(elemCount)
        counter++

#### Remove Tree

split tree along elem
extraCount = 0
for num in range(len(a2))
    for i in range(1,3):
        if a2[num+i] in Ops

split a2 along extraCount

tree1 = a1+a2