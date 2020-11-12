### Next things to consider

1. Redundant / Trojan insertion into code
   1. Keep testing with normal tests now with min use for lev
   2. Try new N num of initial mutations on original AST
2. Exhaustive testing of mutations, on every node
3. Max size of new code
4. Prepare the full test case test pattern
5. Side by side truth tables
6. Implement new crossover features


### Things to fix
1. Check structural fitness scores. System just won't converge, need to better decide if something is diverse enough.
2. Crossover function breaking
   1. ['or', 'and', 'I1', 'or', 'I1', 'I0', 'and', 'I0', 'and', 'I1', 'I0'] -> ['or', 'and', 'I1', 'or', 'I1', 'I0', 'and', 'I1', 'I0', 'I0', 'and', 'I1']

Final AST is:    ['nand', 'nand', 'I1', 'nand', 'Sel', 'I1', 'or', 'nand', 'Sel', 'Sel', 'nand', 'or', 'Sel', 'I1', 'and', 'I0', 'I0']
Original AST  :  ['nand', 'nand', 'I0', 'Sel', 'nand', 'I1', 'nand', 'Sel', 'Sel']