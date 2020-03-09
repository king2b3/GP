### Assumptions

1. Every node either has 1 or 2 children
    1. every function has a pre-defined size
    2. EX/ no 3 input gate(s)
2. There are no sharing of nodes in the AST
    1. Each node is the sole child of another node
    2. EX/ The output of a gate cannot feed into two seperate gates
3. Each output has its own seperate AST
    1. Future implementation of other trees, just need to find some other examples on how they managed multiple output circuits
### Steps
1. Take AST input as a list
2. init tree with first value
    1. Value = Function(node)
    2. Init two blank children
    3. Remove first node from AST list
4. If First Value == Not
    1. Init child1 as a node, child2 = None
    2. Children on node = None
    3. Goto End
3. for node in AST
    1. If node == And, Or
        1. Init Child as a new Node, layer += 1
        2. Init two blank children
    2. If node == Not
        1. Child 1 