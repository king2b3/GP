#   Bayley King
#   Python 3.7.1
#   Levenshtein Distance Calculator
#   Code modified from https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/

import numpy as np

def levenshtein(
    seq1, seq2, 
    scale=True
):
    ''' Levenshtein Distance Calculation

        Creates a matrix sized to the two sequences
        Returns: (based off of scale bool)
            Distance in nums of changes needed
                or
            nums of changes needed / min of length of sequence 1 and 2 
    '''
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    if scale:
        return ((matrix[size_x - 1, size_y - 1])/min(size_x-1,size_y-1))
    else:
        return (matrix[size_x - 1, size_y - 1])




def main():
    newTree2 = ['nand', 'nand', 'I1', 'nand', 'Sel', 'I1', 'or', 'nand', 'Sel', 'Sel', 'nand', 'or', 'Sel', 'I1', 'and', 'I0', 'I0']
    newTree1 = ['nand', 'nand', 'I0', 'Sel', 'nand', 'I1', 'nand', 'Sel', 'Sel']

    print(levenshtein(newTree1,newTree2))



if __name__ == "__main__":
    main()