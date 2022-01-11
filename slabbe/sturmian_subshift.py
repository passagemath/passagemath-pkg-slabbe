# -*- coding: utf-8 -*-
r"""
Sturmian subshift

This modules contains few methods to enumerate of language of factors of
length n within a Sturmian subshift.

EXAMPLES::

    sage: from slabbe import SturmianSubshift
    sage: s = SturmianSubshift(.35355)
    sage: s
    Sturmian subshift of slope 0.353550000000000
    sage: s.characteristic_word()
    word: abaabaabaabaababaabaabaabaabaababaabaaba...
    sage: sorted(s.language(4))
    [word: aaba, word: abaa, word: abab, word: baab, word: baba]
    sage: s.random_factor(4)               # random
    word: baba
    sage: s.random_factor(4)               # random
    word: abaa
    sage: s.lexicographically_minimal_factor(10)
    word: aabaabaaba
    sage: s.lexicographically_maximal_factor(10)
    word: babaabaaba

Providing other type of inputs works including the continued fraction
expansion of a real number::

    sage: slope = continued_fraction(([0,1,2,3], [3,4,5]))
    sage: S = SturmianSubshift(slope); S
    Sturmian subshift of slope [0; 1, 2, 3, (3, 4, 5)*]
    sage: slope.n()
    0.697174148591765
    sage: sorted(S.language(5))
    [word: abbab, word: abbba, word: babba, word: babbb, word: bbabb, word: bbbab]

Providing a rational number as input also works and its language still has
complexity n+1 because we consider the language of the two sided
characteristic sequence::

    sage: S = SturmianSubshift(1/3); S
    Sturmian subshift of slope 1/3
    sage: S.characteristic_word()
    word: aabaabaabaabaabaabaabaabaabaabaabaabaaba...
    sage: sorted(S.language(3))
    [word: aaa, word: aab, word: aba, word: baa]
    sage: sorted(S.language(4))
    [word: aaab, word: aaba, word: abaa, word: baaa, word: baab]

AUTHORS:

    - S. Labbé, initial version, 2021

"""
#*****************************************************************************
#       Copyright (C) 2021-2022 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

class SturmianSubshift:
    def __init__(self, slope):
        r"""
        INPUT:

        - ``slope`` -- real number in the interval [0,1]

        EXAMPLES::

            sage: from slabbe import SturmianSubshift
            sage: s = SturmianSubshift(.35355)
        """
        self._slope = slope

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import SturmianSubshift
            sage: SturmianSubshift(.35355)
            Sturmian subshift of slope 0.353550000000000
        """
        return "Sturmian subshift of slope {}".format(self._slope)

    def characteristic_word(self):
        r"""
        Return the characteristic Sturmian word of given slope

        EXAMPLES::

            sage: from slabbe import SturmianSubshift
            sage: s = SturmianSubshift(.35355)
            sage: s.characteristic_word()
            word: abaabaabaabaababaabaabaabaabaababaabaaba...

        Rational slope::

            sage: s = SturmianSubshift(1/4)
            sage: s.characteristic_word()
            word: aaabaaabaaabaaabaaabaaabaaabaaabaaabaaab...
        """
        from sage.combinat.words.word_generators import words
        from sage.rings.rational_field import QQ
        from sage.rings.infinity import Infinity
        w = words.CharacteristicSturmianWord(self._slope, 'ab')
        #return w
        if self._slope in QQ:
            return w**Infinity
        else:
            return w

    def language(self, n):
        r"""
        Return the set of factors of size n in that sturmian word of
        rational or irrational slope.

        EXAMPLES::

            sage: from slabbe import SturmianSubshift
            sage: s = SturmianSubshift(.35355)
            sage: sorted(s.language(5))
            [word: aabaa, word: aabab, word: abaab, word: ababa, word: baaba, word: babaa]
            sage: len(_)
            6

        ::

            sage: s = SturmianSubshift(1/golden_ratio^2)
            sage: sorted(s.language(0))
            [word: ]
            sage: sorted(s.language(1))
            [word: a, word: b]
            sage: sorted(s.language(2))
            [word: aa, word: ab, word: ba]

        Rational slope::

            sage: s = SturmianSubshift(1/4)
            sage: sorted(s.language(10))
            [word: aaaabaaaba, word: aaabaaaaba, word: aaabaaabaa, word: aabaaaabaa, 
             word: aabaaabaaa, word: abaaaabaaa, word: abaaabaaaa, word: abaaabaaab,
             word: baaaabaaab, word: baaabaaaab, word: baaabaaaba]
            sage: len(_)
            11

        """
        w = self.characteristic_word()
        if n == 0:
            hamiltonian = w[:1]
        elif n > 0:
            prefix = w[:n-1]
            ab = prefix.parent()(['a', 'b'])
            hamiltonian = prefix.reversal() * ab * prefix
        else:
            raise ValueError('n(={}) should be >=0'.format(n))
        F = hamiltonian.factor_set(n)
        assert len(F) == n + 1
        return F

    def random_factor(self, n):
        r"""
        EXAMPLES::

            sage: from slabbe import SturmianSubshift
            sage: s = SturmianSubshift(.35355)
            sage: s.random_factor(5) # random
            word: babaa
            sage: s.random_factor(5) # random
            word: aabab

        """
        from sage.misc.prandom import choice
        F = self.language(n)
        return choice(list(F))

    def lexicographically_minimal_factor(self, n, check=False):
        r"""
        EXAMPLES::

            sage: from slabbe import SturmianSubshift
            sage: s = SturmianSubshift(.35355)
            sage: s.lexicographically_minimal_factor(10)
            word: aabaabaaba
            sage: s.lexicographically_minimal_factor(10, check=True)
            word: aabaabaaba
            sage: s.lexicographically_minimal_factor(100, check=True)
            word: aabaabaabaabaababaabaabaabaabaababaabaab...

        """
        w = self.characteristic_word()
        prefix = w[:n-1]
        a = prefix.parent()(['a'])
        a_prefix = a*prefix
        if check:
            F = sorted(self.language(n))
            factor_min = F[0]
            assert factor_min == a_prefix
        return a_prefix

    def lexicographically_maximal_factor(self, n, check=False):
        r"""
        EXAMPLES::

            sage: from slabbe import SturmianSubshift
            sage: s = SturmianSubshift(.35355)
            sage: s.lexicographically_maximal_factor(10)
            word: babaabaaba
            sage: s.lexicographically_maximal_factor(10, check=True)
            word: babaabaaba
            sage: s.lexicographically_maximal_factor(100, check=True)
            word: babaabaabaabaababaabaabaabaabaababaabaab...

        """
        w = self.characteristic_word()
        prefix = w[:n-1]
        b = prefix.parent()(['b'])
        b_prefix = b*prefix
        if check:
            F = sorted(self.language(n))
            factor_max = F[-1]
            assert factor_max == b_prefix
        return b_prefix

