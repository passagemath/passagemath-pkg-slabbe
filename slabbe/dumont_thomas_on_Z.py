# -*- coding: utf-8 -*-
r"""
Dumont-Thomas Numeration system on Z

.. TODO::

    The code is currently broken, this is a work in progress.

EXAMPLES::

    sage: m = WordMorphism('a->abc,b->baba,c->ca')
    sage: w = m.fixed_point('a')

"""
#*****************************************************************************
#       Copyright (C) 2023 Sebastien Labbe <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.combinat.words.morphism import WordMorphism
from sage.combinat.words.words import FiniteWords
from sage.modules.free_module_element import vector


class PeriodicPoint():
    def __init__(self, morphism, p, seed):
        self._morphism = morphism
        self._seed = seed
        self._p = p

    def quo_rem(self, n):
        if n == 0 or n == -1:
            raise ValueError()
        elif n >= 1:
            pass
        elif n <= -2:
            pass
        else:
            assert False


    def representation(self, n):
        r"""
        EXAMPLES::

            sage: from slabbe.dumont_thomas_on_Z import PeriodicPoint
            sage: m = WordMorphism('a->ab,b->a')
            sage: u = PeriodicPoint(m, 2, ('b','a'))
            sage: [u.representation(i) for i in range(10)]
            [[0],
             [0, 0, 1],
             [0, 1, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 1],
             [0, 1, 0, 0, 0],
             [0, 1, 0, 0, 1],
             [0, 1, 0, 1, 0],
             [0, 0, 1, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 1]]
            sage: u.representation(-3)
            [1, 0, 0, 1, 0]

        """
        if n == 0 :
            return [0]
        elif n == -1:
            return [1]
        elif n >= 1:
            b,a = self._seed
            letter = a
            t = tail(self._morphism, letter, n)
            tail_length_mod_p = len(t) % self._p
            if tail_length_mod_p:
                return [0] + [0]*(self._p-tail_length_mod_p) + t
            else:
                return [0] + t
        elif n <= -2:
            b,a = self._seed
            letter = b
            t = tail(self._morphism, letter, n)
            tail_length_mod_p = len(t) % self._p
            if tail_length_mod_p:
                return [1] + [0]*(self._p-tail_length_mod_p) + t
            else:
                return [1] + t
        else:
            assert False


    def table(self, start, stop, step=1):
        r"""
        EXAMPLES::

            sage: from slabbe.dumont_thomas_on_Z import PeriodicPoint
            sage: m = WordMorphism('a->ab,b->a')
            sage: u = PeriodicPoint(m, 2, ('b','a'))
            sage: u.table(10,-10,-1)
              10   [0, 0, 1, 0, 0, 1, 0]
              9    [0, 0, 1, 0, 0, 0, 1]
              8    [0, 0, 1, 0, 0, 0, 0]
              7    [0, 1, 0, 1, 0]
              6    [0, 1, 0, 0, 1]
              5    [0, 1, 0, 0, 0]
              4    [0, 0, 1, 0, 1]
              3    [0, 0, 1, 0, 0]
              2    [0, 1, 0]
              1    [0, 0, 1]
              0    [0]
              -1   [1]
              -2   [1, 0, 1]
              -3   [1, 0, 0, 1, 0]
              -4   [1, 0, 1, 0, 1]
              -5   [1, 0, 1, 0, 0]
              -6   [1, 0, 0, 1, 0, 1, 0]
              -7   [1, 0, 0, 1, 0, 0, 1]
              -8   [1, 0, 0, 1, 0, 0, 0]
              -9   [1, 0, 1, 0, 1, 0, 1]

        ::

             sage: m = WordMorphism('a->ab,b->ba')
             sage: u = PeriodicPoint(m, 2, ('a','a'))
             sage: u.table(10,-10,-1)   # known bug

        """
        from sage.misc.table import table

        rows = []
        for n in range(start, stop, step):
            rep = self.representation(n)
            row = [n, rep]
            rows.append(row)
        return table(rows)


def tail(morphism, letter, n):
    r"""
    Return the representation of n in based on the prefix of length n 
    in the image of ``morphism^p(letter)`` for some p.

    EXAMPLES::

        sage: from slabbe.dumont_thomas_on_Z import tail
        sage: m = WordMorphism('a->abc,b->baba,c->ca')
        sage: [tail(m, 'a', i) for i in range(10)]
        [[], [1], [2], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [1, 0, 0]]
        sage: [tail(m, 'a', i) for i in range(-10,0)]    # known bug
        [[1, 2, 2], [0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [0], [1], []]

    ::

        sage: m = WordMorphism('a->ab,b->a')
        sage: tail(m, 'b', -3)
        [0, 1, 0]
        sage: tail(m, 'b', -4)
        [0, 1, 0, 1]

    """
    alphabet = morphism.domain().alphabet()

    letters_to_int =  {a:i for (i,a) in enumerate(alphabet)}
    position = letters_to_int[letter]
    M = morphism.incidence_matrix()
    vMk = vector([1]*len(alphabet))
    length_of_images = []
    while ((n>=0 and vMk[position] <= n) or 
           (n <0 and vMk[position] < -n)):
        length_of_images.append(vMk)
        vMk_next = vMk*M
        if n>=0 and vMk[position] == vMk_next[position]:
            raise IndexError('index (={}) out of range, the fixed point is finite and has length {}'.format(n,vMk[position]))
        vMk = vMk_next
    k = len(length_of_images)
    #if k > p:
    #    raise ValueError('n(={}) must be smaller than the '
    #            'length of word (={})'.format(n, sum(length_of_images[-2])))
    letter_k = letter
    if n >= 0:
        n_k = n
    else:
        n_k = n + (vMk*M)[position]
        #print((vMk*M)[position])
        #print(n, n_k)
    #if pad_with_zeroes:
    #    path = [0]*(p-k)
    #else:
    #    path = []
    path = []
    while k > 0:
        m_letter_k = morphism(letter_k)
        S = 0
        j = 0
        while S <= n_k:
            a = m_letter_k[j]
            i = letters_to_int[a]
            pile_length = length_of_images[k-1][i]
            S += pile_length
            j += 1
        path.append(j-1)
        n_k -= S - pile_length
        letter_k = a
        k -= 1
    return path

