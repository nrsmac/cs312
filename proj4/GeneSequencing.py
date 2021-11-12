#!/usr/bin/python3

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import numpy as np
import math
import time
import random

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1


class GeneSequencing:

    def __init__(self):
        pass

    # This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment

    def align(self, seq1, seq2, banded, align_length):
        self.banded = banded
        self.MaxCharactersToAlign = align_length

        s1, s2 = seq1, seq2
        if len(seq1) > align_length:
            s1 = seq1[:align_length]
        if len(seq2) > align_length:
            s2 = seq2[:align_length]

        if banded:
            table, backpointer_table, score = self.getBandedTable(s1, s2)
        else:
            table, backpointer_table, score = self.getUnbandedTable(s1, s2)

        if banded:
            alignment1, alignment2 = self.extractFromBandedTable(table, backpointer_table, s1, s2)
        else:
            alignment1, alignment2 = self.extractFromUnbandedTable(table, backpointer_table, s1, s2)

        ###################################################################################################
        # your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
        # score = random.random() * 100;
        # alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
        #     len(seq1), align_length, ',BANDED' if banded else '')
        # alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
        #     len(seq2), align_length, ',BANDED' if banded else '')
        ###################################################################################################

        return {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}

    def getUnbandedTable(self, seq1, seq2):
        score = 0

        n = len(seq1)
        m = len(seq2)
        T = [[math.inf for j in range((m) + 1)] for i in range(n + 1)]  # O(nm)
        P = [[math.inf for j in range((m) + 1)] for i in range(n + 1)]  # O(nm)

        for i in range(0, n + 1):  # O(n)
            T[i][0] = i * INDEL
            P[i][0] = 'up'

        for j in range(0, m + 1): # O(m)
            T[0][j] = j * INDEL
            P[0][j] = 'left'

        # Doin the dirty work
        for i in range(1, n + 1):   # O(nm)
            for j in range(1, m + 1):
                left = T[i][j - 1] + INDEL
                up = T[i - 1][j] + INDEL
                diag = T[i - 1][j - 1]

                if left <= up and left <= diag:
                    T[i][j] = left
                    P[i][j] = 'left'
                elif up <= diag:
                    T[i][j] = up
                    P[i][j] = 'up'
                else:
                    if seq1[i - 1] == seq2[j - 1]:
                        diag += MATCH
                        T[i][j] = diag
                        P[i][j] = 'diag'
                    else:
                        diag += SUB
                        T[i][j] = diag
                        P[i][j] = 'diag'

        score = T[n][m]
        return T, P, score

    def getBandedTable(self, seq1, seq2):

        score = 0

        k = 7
        d = (k - 1) / 2

        n = len(seq1)

        T = [[math.inf for j in range(k)] for i in range(n)]
        P = [[math.inf for j in range(k)] for i in range(n)]

        for j in range(3, k):    # O(k)
            T[0][j] = (j - 3) * INDEL
            P[0][j] = 'left'

        # populate initial j values
        j_start = 3
        for i in range(4):
            T[i][j_start] = i * INDEL
            j_start -= 1


        # Middle
        j_start = 3
        ended_at = (0, 0)
        counter = 3
        for i in range(1, n - 2):
            for j in range(j_start, k):  # O(nk)

                # Calc left
                if j > 0:
                    left = T[i][j - 1] + INDEL
                else:
                    left = math.inf

                # Calc diag
                if j < k - 1:
                    diag = T[i - 1][j + 1] + INDEL
                else:
                    diag = math.inf

                # Calc up based on matching chars
                up = T[i - 1][j]
                if seq1[j - counter] == seq2[i - 1]:
                    up += MATCH
                else:
                    up += SUB

                if left <= diag and left <= up:
                    T[i][j] = left
                    P[i][j] = 'left'
                elif diag <= up:
                    T[i][j] = diag
                    P[i][j] = 'diag'
                else:
                    T[i][j] = up
                    P[i][j] = 'up'

            counter -= 1
            if counter < 0:
                j_start = 0
            else:
                j_start = counter
            ended_at = (i, j)

        # DO the bottom! start at i+1, j+1
        stop = k - 1
        for i in range(ended_at[0] + 1, n):
            for j in range(0, stop):   # O(nk)
                # Calc left
                if j != 0:
                    left = T[i][j - 1] + INDEL
                else:
                    left = math.inf

                # Calc diag
                if j < k - 1:
                    diag = T[i - 1][j + 1] + INDEL
                else:
                    diag = math.inf

                # Calc up based on matching chars
                up = T[i - 1][j]
                if seq1[j - counter] == seq2[i - 1]:
                    up += MATCH
                else:
                    up += SUB

                if left <= diag and left <= up:
                    T[i][j] = left
                    P[i][j] = 'left'
                elif diag <= up:
                    T[i][j] = diag
                    P[i][j] = 'diag'
                else:
                    T[i][j] = up
                    P[i][j] = 'up'
            score = T[i][j]
            stop -= 1
            counter -= 1

        return T, P, score

    def extractFromUnbandedTable(self, T, P, seq1, seq2):
        i, j = len(seq1), len(seq2)
        seq1 = [char for char in seq1]  # Reverse lists for easy poppin
        seq2 = [char for char in seq2]

        seq1_out = ""
        seq2_out = ""

        while i > 0 and j > 0:  # O(max(n, m))
            pointer = P[i][j]

            if pointer == 'diag':
                seq1_out = seq1.pop() + seq1_out
                seq2_out = seq2.pop() + seq2_out
                i -= 1
                j -= 1
            elif pointer == 'left':
                seq1_out = '-' + seq1_out  # TODO verify this
                seq2_out = seq2.pop() + seq2_out
                j -= 1

            elif pointer == 'up':
                seq1_out = seq1.pop() + seq1_out
                seq2_out = '-' + seq2_out  # TODO verify this
                i -= 1

        return seq1_out, seq2_out

    def extractFromBandedTable(self, T, P, s2, s1):
        i, j = len(T)-1, len(T[0])-3
        seq1 = [char for char in s1]  # Reverse lists for easy poppin
        seq2 = [char for char in s2]

        seq1_out = ""
        seq2_out = ""

        while i > 0 and j > 0:   # O(max(n, k))
            pointer = P[i][j]

            if pointer == 'up':
                seq1_out = seq1.pop() + seq1_out
                seq2_out = seq2.pop() + seq2_out
                i -= 1

            elif pointer == 'left':
                seq1_out = '-' + seq1_out
                seq2_out = seq2.pop() + seq2_out
                j -= 1

            elif pointer == 'diag':
                seq1_out = seq1.pop() + seq1_out
                seq2_out = '-' + seq2_out
                i -= 1
                j -= 1

        return seq1_out + seq1_out[7:], seq2_out+ seq2_out[7:]
