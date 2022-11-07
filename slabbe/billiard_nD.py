r"""
Hypercubic billiard subshifts

EXAMPLES::

    sage: from slabbe import HypercubicBilliardSubshift
    sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi))
    sage: L = s.language(6, prefix_length=10000)
    sage: len(L)
    43
    sage: v = list(sqrt(p) for p in primes(start=2, stop=18))
    sage: s = HypercubicBilliardSubshift(v)
    sage: K = s.language(2, prefix_length=10000)
    sage: len(K)
    43

An open question is to find a bijection between L and K::

    sage: L
    {word: 022120, word: 120212, word: 022122, word: 212221, word: 212220,
     word: 212021, word: 212022, word: 222102, word: 220122, word: 022210,
     word: 120221, word: 022212, word: 122201, word: 122120, word: 012212,
     word: 201221, word: 201222, word: 220212, word: 221022, word: 221220,
     word: 012220, word: 102212, word: 122210, word: 122212, word: 122012,
     word: 012221, word: 210221, word: 210222, word: 212201, word: 212202,
     word: 202122, word: 222120, word: 021220, word: 102221, word: 122021,
     word: 122102, word: 021222, word: 021221, word: 212212, word: 212210,
     word: 202212, word: 222012, word: 221202}
    sage: K
    {word: 20, word: 21, word: 23, word: 24, word: 25, word: 26, word: 60,
     word: 61, word: 63, word: 66, word: 64, word: 62, word: 65,
     word: 30, word: 31, word: 32, word: 34, word: 35, word: 36,
     word: 01, word: 02, word: 03, word: 04, word: 05, word: 06,
     word: 40, word: 42, word: 41, word: 45, word: 43, word: 46,
     word: 10, word: 12, word: 13, word: 14, word: 15, word: 16,
     word: 51, word: 50, word: 53, word: 56, word: 52, word: 54}

AUTHORS:

- Initial version, Mélodie Andrieu et Sébastien Labbé, Novembre 7, 2022

"""
#*****************************************************************************
#       Copyright (C) 2022 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
import itertools
from collections import Counter

from sage.modules.free_module_element import vector
from sage.combinat.words.word_generators import words

class HypercubicBilliardSubshift:
    def __init__(self, v):
        r"""
        INPUT:

        - ``v`` -- d-dimensional speed vector

        EXAMPLES::

            sage: from slabbe import HypercubicBilliardSubshift
            sage: v = (1, sqrt(2), pi)
            sage: s = HypercubicBilliardSubshift(v)
        """
        self._v = v

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import HypercubicBilliardSubshift
            sage: v = (1, sqrt(2), pi)
            sage: s = HypercubicBilliardSubshift(v)
            sage: s
            Hypercubic billiard of speed vector (1, sqrt(2), pi)
        """
        return "Hypercubic billiard of speed vector {}".format(self._v)

    def dimension(self):
        r"""
        Return the ambient dimension of the billiard table.

        EXAMPLES::

            sage: from slabbe import HypercubicBilliardSubshift
            sage: v = (1, sqrt(2), pi)
            sage: s = HypercubicBilliardSubshift(v)
            sage: s.dimension()
            3

        """
        return len(self._v)

    def characteristic_word(self, verbose=False):
        r"""
        Return the characteristic billiard word with given speed vector

        INPUT:

        - ``verbose`` -- boolean

        OUTPUT:

        infinite word over alphabet {0,1,...,d-1}

        EXAMPLES::

            sage: from slabbe import HypercubicBilliardSubshift
            sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi))
            sage: s.characteristic_word()
            word: 2212021220122120221202122102212021220212...

        ... compared to::

            sage: from slabbe import BilliardCube
            sage: b = BilliardCube((1,sqrt(2), pi))
            sage: b.to_word(alphabet=[0,1,2])
            word: 2120212202122102212021220122210221202122...

        ::

            sage: v = (100+1/pi,1+1/pi^2,49+1/sqrt(2),pi)
            sage: s = HypercubicBilliardSubshift(v)
            sage: s.characteristic_word()
            word: 0020020020020020020020020020020020020020...

        TESTS::

            sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi))
            sage: s.characteristic_word(verbose=True)
            (1.00000000000000, 1.41421356237310, 3.14159265358979)
            (0, 1) 1010110101101010110101101010110101101011...
            (0, 2) 2220222022202220222022202220222202220222...
            (1, 2) 2212212212212221221221221221222122122122...
            word: 2212021220122120221202122102212021220212...

        AUTHORS:

        - Mélodie Andrieu et Sébastien Labbé, Novembre 7, 2022

        """
        from sage.combinat.words.words import InfiniteWords

        dim = len(self._v)
        speed_ratio = {(i,j): self._v[j]/(self._v[i]+self._v[j]) for (i,j) in
                itertools.combinations(range(dim), 2)}

        d = {}
        for (i,j),slope in speed_ratio.items():
            alphabet = [i, j]
            w = words.CharacteristicSturmianWord(slope, alphabet) 
            d[(i,j)] = w

        if verbose:
            print(vector(self._v).n())
            for ij,w in d.items():
                print(ij,w)

        def _the_iterator(letters, iterators):
            while True:
                c = Counter(letters)
                max_value = max(c.values())
                argmax, = [key for key in c if c[key] == max_value]

                yield argmax

                for i,letter in enumerate(letters):
                    if letter == argmax:
                        letters[i] = next(iterators[i])

        iterators = [iter(w) for w in d.values()]
        letters = [next(it) for it in iterators]

        W = InfiniteWords(alphabet=list(range(dim)))
        return W(_the_iterator(letters, iterators))

    def language(self, n, prefix_length=1000):
        r"""
        Return the language of the hypercubic billiard word

        INPUT:

        - ``n`` -- integer
        - ``prefix_length`` -- integer (default: 1000),

        OUTPUT:

        list of words

        EXAMPLES::

            sage: from slabbe import HypercubicBilliardSubshift
            sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi))

        Two factors of length 6 appear far away in the characteristic word::

            sage: s.language(6, prefix_length=10000) - s.language(6)
            WARNING: Factor complexity is p(6)=43, but only 41 factors
            found in the prefix of length 1000
            {word: 012220, word: 022210}

        Same for factors of length 15::

            sage: s.characteristic_word()[8252:8292]
            word: 1202122012212022120212210221220212210221
            sage: s.language(15, prefix_length=8292) - s.language(15, prefix_length=8280)
            WARNING: Factor complexity is p(15)=241, but only 236 factors
            found in the prefix of length 8280
            {word: 022122021221022, 
             word: 210221220212210, 
             word: 102212202122102, 
             word: 221022122021221, 
             word: 221220212210221}

        """
        w = self.characteristic_word()

        prefix = w[:prefix_length]
        F = prefix.factor_set(n)

        # check that the complexity matches the formula
        p_n = self.complexity(n)
        if len(F) != p_n:
            print ("WARNING: Factor complexity is p({})={},"
                " but only {} factors found in the prefix of"
                " length {}".format(n, p_n, len(F), prefix_length))

        return F

    def complexity(self, n):
        r"""
        Return the number factors of length ``n`` of the hypercubic
        billiard word

        INPUT:

        - ``n`` -- integer

        OUTPUT:

        integer

        EXAMPLES::

            sage: from slabbe import HypercubicBilliardSubshift
            sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi))
            sage: [s.complexity(i) for i in range(10)]
            [1, 3, 7, 13, 21, 31, 43, 57, 73, 91]

        It matches the formula `n^2+n+1` in dimension 3::

            sage: [n^2+n+1 for n in range(10)]
            [1, 3, 7, 13, 21, 31, 43, 57, 73, 91]

        ::

            sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi,sqrt(3)))
            sage: [s.complexity(i) for i in range(10)]
            [1, 4, 13, 34, 73, 136, 229, 358, 529, 748]

        """
        from sage.functions.other import factorial, binomial

        d = self.dimension()
        return sum([factorial(k)*binomial(n,k)*binomial(d-1,k) 
                   for k in range(0, min(d-1,n)+1)])

