import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is the size N array/seq of integers representing the best sequence.
    """

    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    y = []
    T = np.empty((L,N), object)
    emission_scores_transpose = np.transpose(emission_scores)
    score = -np.inf
    index = 0
    for j in xrange(N):
        for i in xrange(L):
            temp_max = -np.inf
            temp_max_index = 0
            if j == 0:
                T[i][j] = [start_scores[i] + emission_scores_transpose[i][j],-1]
            else:
                for k in xrange(L):
                    temp_del = T[k][j-1][0] + trans_scores[k][i]
                    if temp_del > temp_max:
                        temp_max = temp_del
                        temp_max_index = k

                T[i][j] = [temp_max + emission_scores_transpose[i][j], temp_max_index]

            if j == N-1:
                T[i][j][0] += end_scores[i]


    for i in xrange(L):
        if T[i][N-1][0] > score:
            score = T[i][N-1][0]
            index = i
    y.insert(0,index) ## index of the tag of last word
    j = N-1

    ## using backpointers to find tag indexes of previous words
    while j > 0:
        y.insert(0,T[index][j][1])
        index = T[index][j][1]
        j -= 1
    return (score, y)
