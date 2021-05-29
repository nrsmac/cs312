#!/usr/bin/python3

# from PyQt5.QtCore import QLineF, QPointF


import math
import time
import numpy as np

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

TOP = 0
DIAG = 1
LEFT = 2


class GeneSequencing:

    def __init__(self):
        pass

    # This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
    # handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment
    def align(self, sequences, table, banded, align_length):
        self.banded = banded
        self.MaxCharactersToAlign = align_length
        results = []

        for i in range(len(sequences)):
            jresults = []
            for j in range(len(sequences)):
                if j < i:
                    s = {}
                else:
                    # your code should replace these three statements and populate the three variables: score,
                    # alignment1 and alignment2

                    result = None
                    if not banded:
                        result = self.get_not_banded(sequences[i][:align_length],
                                                                sequences[j][:align_length])
                        score = result[0]
                        alignment1 = result[1]
                        alignment2 = result[2]
                    else:
                        banded_result = self.get_banded(sequences[i][:align_length], sequences[j][:align_length])

                    score = i + j
                    alignment1 = alignment1 + '  DEBUG:(seq{}, {} chars,align_len={}{})'.format(i + 1,
                                                                                           len(sequences[i]),
                                                                                           align_length,
                                                                                           ',BANDED' if banded else '')
                    alignment2 = alignment2 + '  DEBUG:(seq{}, {} chars,align_len={}{})'.format(j + 1,
                                                                                           len(sequences[j]),
                                                                                           align_length,
                                                                                           ',BANDED' if banded else '')
                    ###################################################################################################
                    s = {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}
                    table.item(i, j).setText('{}'.format(int(score) if score != math.inf else score))
                    table.repaint()
                jresults.append(s)
            results.append(jresults)
        return results

    def get_not_banded(self, sequence1, sequence2):

        # matrix = np.ones((len(sequence1) + 1, len(sequence2) + 1)) * np.inf
        # back_pointer_matrix = np.ones((len(sequence1) + 1, len(sequence2) + 1)) * np.inf

        matrix = [[math.inf for x in range(len(sequence2)+1)]for y in range(len(sequence1)+1)]
        back_pointer_matrix = [[math.inf for x in range(len(sequence2)+1)]for y in range(len(sequence1)+1)]


        # initialize matrix stuff
        for i in range(len(sequence1) + 1):
            matrix[i][0] = i
            back_pointer_matrix[i][0] = TOP

        for j in range(len(sequence2) + 1):
            matrix[0][j] = j
            back_pointer_matrix[0][j] = LEFT

        back_pointer_matrix[0][0] = -1

        for i in range(1, len(sequence1)+1):
            for j in range(1, len(sequence2)+1):
                #  find out what the top is, what diag is, and what left is
                #  compare them all to get the shortest while accounting for INDEL, sub and match
                #  get a value that goes into the
                #  update back matrices accordingly -> back_pointer_matrix[i][j]
                if i == 1 and j ==1 :
                    matrix[i][j] = 1
                    back_pointer_matrix[i][j] = DIAG
                else:
                    if sequence1[i-1] == sequence2[j-1]:
                        diff = 0
                    else:
                        diff = 1

                    corners = [matrix[i-1][j] + 1, matrix[i - 1][j - 1]+diff, 1 + matrix[i][j-1]]##top, diag, left
                    E = min(corners)

                    matrix[i][j] = E
                    back_pointer_matrix[i][j] = corners.index(E)  #either TOP, DIAG, LEFT

        not_banded_path = self.get_path(back_pointer_matrix, sequence1, sequence2)

        return matrix[1][1], not_banded_path[0], not_banded_path[1]

    def get_path(self, back_pointer_matrix, sequence1, sequence2):

        alignment1 = ""
        alignment2 = ""
        i, j = len(sequence1), len(sequence2)  # our back pointer matrix can only go backwards
        while i != 0 or j != 0:
            if back_pointer_matrix[i][j] == TOP:
                # do the zero stuff, it came from top
                sequence1_char = sequence1[i-1]
                alignment1 = sequence1_char + alignment1  # add it to the front of alignment one
                alignment2 = "-" + alignment2  # add it to the front of alignment 2
                i -= 1

            elif back_pointer_matrix[i][j] == DIAG:
                # came from diagonal
                sequence1_char = sequence1[i - 1]
                sequence2_char = sequence2[j - 1]
                alignment1 = sequence1_char + alignment1  # add it to the front of alignment 1
                alignment2 = sequence2_char + alignment2  # add it to the front of alignment 2
                i -= 1
                j -= 1

            elif back_pointer_matrix[i][j] == LEFT:
                sequence2_char = sequence2[j-1]
                alignment1 = "-" + alignment1  # add it to the front of alignment 1
                alignment2 = sequence2_char + alignment2  # add it to the front of alignment 2
                j -= 1
            else:
                raise ValueError("Invalid pointer {} in array at ({},{})".format(back_pointer_matrix[i][j], i, j))

        return [alignment1, alignment2]

    def get_banded(self, sequence1, sequence2, d):
        matrix = [[math.inf for x in range(len(sequence2) + 1)] for y in range(len(sequence1) + 1)]
        back_pointer_matrix = [[math.inf for x in range(len(sequence2) + 1)] for y in range(len(sequence1) + 1)]

        # initialize matrix stuff
        for i in range(len(sequence1) + 1):
            matrix[i][0] = i
            back_pointer_matrix[i][0] = TOP

        for j in range(len(sequence2) + 1):
            matrix[0][j] = j
            back_pointer_matrix[0][j] = LEFT

        back_pointer_matrix[0][0] = -1

        last = None
        same_as_last = False
        d_counter = 0

        for i in range(1, len(sequence1) + 1):
            for j in range(1, len(sequence2) + 1):
                #  find out what the top is, what diag is, and what left is
                #  compare them all to get the shortest while accounting for INDEL, sub and match
                #  get a value that goes into the
                #  update back matrices accordingly -> back_pointer_matrix[i][j]
                if i == 1 and j == 1:
                    matrix[i][j] = 1
                    back_pointer_matrix[i][j] = DIAG
                else:
                    if sequence1[i - 1] == sequence2[j - 1]:
                        diff = 0
                    else:
                        diff = 1

                    corners = [matrix[i - 1][j] + 1, matrix[i - 1][j - 1] + diff,
                               1 + matrix[i][j - 1]]  ##top, diag, left
                    E = min(corners)

                    matrix[i][j] = E
                    back_pointer_matrix[i][j] = corners.index(E)  # either TOP, DIAG, LEFT
