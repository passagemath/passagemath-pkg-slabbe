r"""
Hypercubic billiard subshifts

The construction of a billiard word in this module is made by lifting a
certain set of projected sturmian sequences.

EXAMPLES:

The Fibonacci word::

    sage: from slabbe import HypercubicBilliardSubshift
    sage: s = HypercubicBilliardSubshift((golden_ratio,1))
    sage: s.characteristic_word()
    word: 0100101001001010010100100101001001010010...
    sage: words.FibonacciWord()
    word: 0100101001001010010100100101001001010010...

A 3-dimensional example::

    sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi))
    sage: s.characteristic_word()
    word: 2212021220122120221202122102212021220212...
    sage: L = s.language(6, prefix_length=10000)
    sage: len(L)
    43
    sage: v = [sqrt(p) for p in primes_first_n(7)]
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

::

    sage: v = [sqrt(p) for p in primes_first_n(4)]
    sage: s = HypercubicBilliardSubshift(v)
    sage: L = s.language(4, prefix_length=18000)
    sage: len(L)
    73
    sage: v = [sqrt(p) for p in primes_first_n(5)]
    sage: t = HypercubicBilliardSubshift(v)
    sage: K = t.language(3, prefix_length=10000)
    sage: len(K)
    73
    sage: L
    {word: 0123, word: 1330, word: 3031, word: 1332, word: 3032, word: 2303,
     word: 2301, word: 2302, word: 2310, word: 3120, word: 0213, word: 0132, 
     word: 0133, word: 1023, word: 3123, word: 3203, word: 2313, word: 3201, 
     word: 2312, word: 1032, word: 2320, word: 1033, word: 3130, word: 3132, 
     word: 3213, word: 2323, word: 3210, word: 2321, word: 2013, word: 0231,
     word: 2330, word: 2331, word: 0233, word: 0232, word: 0313, word: 0312,
     word: 1203, word: 3301, word: 3302, word: 2332, word: 0321, word: 3310,
     word: 0323, word: 3312, word: 3232, word: 3230, word: 3231, word: 2103,
     word: 2031, word: 2032, word: 2033, word: 1303, word: 0332, word: 0331,
     word: 1302, word: 3320, word: 3321, word: 1230, word: 1231, word: 1232,
     word: 1233, word: 3012, word: 3013, word: 3021, word: 3102, word: 2132,
     word: 3103, word: 1321, word: 1323, word: 1320, word: 3023, word: 2133,
     word: 2130}
    sage: K
    {word: 012, word: 013, word: 014, word: 410, word: 412, word: 413, word: 414, 
     word: 102, word: 103, word: 104, word: 021, word: 024, word: 023, word: 341, 
     word: 343, word: 344, word: 342, word: 424, word: 423, word: 340, word: 421, 
     word: 031, word: 032, word: 034, word: 431, word: 430, word: 432, word: 434, 
     word: 120, word: 201, word: 041, word: 123, word: 124, word: 440, word: 441, 
     word: 442, word: 044, word: 042, word: 043, word: 203, word: 204, word: 443, 
     word: 210, word: 130, word: 132, word: 213, word: 134, word: 214, word: 301, 
     word: 140, word: 302, word: 142, word: 143, word: 144, word: 304, word: 310, 
     word: 230, word: 312, word: 231, word: 314, word: 234, word: 401, word: 402, 
     word: 403, word: 404, word: 320, word: 321, word: 324, word: 244, word: 243, 
     word: 240, word: 241, word: 420}

The following illustrates that we may need to go very far to get all factors::

    sage: s = HypercubicBilliardSubshift((sqrt(3),sqrt(2),sqrt(5)))
    sage: L = s.language(6, prefix_length=1000000)     # not tested
    WARNING: Factor complexity is p(6)=43, but only 41 factors found in
    the prefix of length 1000000

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

    def abelian_complexity(self, n):
        r"""
        Return the number abelian factors of length ``n`` of the hypercubic
        billiard word

        INPUT:

        - ``n`` -- integer

        OUTPUT:

            integer

        EXAMPLES::

            sage: from slabbe import HypercubicBilliardSubshift
            sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi))
            sage: [s.abelian_complexity(i) for i in range(10)]
            [1, 3, 4, 4, 4, 4, 4, 4, 4, 4]

        Indeed we compute 4 abelian vectors of factors of length 10::

            sage: L = s.language(6, prefix_length=10000)
            sage: set(tuple(w.abelian_vector()) for w in L)
            {(0, 2, 4), (1, 1, 4), (1, 2, 3), (2, 1, 3)}
            sage: from collections import Counter
            sage: Counter(tuple(w.abelian_vector()) for w in L)
            Counter({(1, 2, 3): 18,
                     (1, 1, 4): 18,
                     (2, 1, 3): 4,
                     (0, 2, 4): 3})

        ::

            sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi,sqrt(3)))
            sage: [s.abelian_complexity(i) for i in range(10)]
            [1, 4, 7, 8, 8, 8, 8, 8, 8, 8]

        """
        from sage.functions.other import factorial, binomial
        d = self.dimension()
        return sum([binomial(d-1,k) for k in range(0, min(d-1,n)+1)])

    def print_factor_complexity_by_abelian(self, n, prefix_length=10000):
        r"""
        Compare the formula with the actual number of abelian classes

        INPUT:

        - ``n`` -- integer

        EXAMPLES:

        Even with Fibonacci word, it does not work well::

            sage: from slabbe import HypercubicBilliardSubshift
            sage: s = HypercubicBilliardSubshift((golden_ratio,1))
            sage: s.print_factor_complexity_by_abelian(3)
            Factor Complexity:
               p(3) = 4
                    = 1*1*1 + 1*3*1
                    = 1*1 + 3*1
            Counting each abelian factor:
              abelian vector   number of factors
            ├────────────────┼───────────────────┤
              (1, 2)           1
              (2, 1)           3
            sage: s.print_factor_complexity_by_abelian(4)
            Factor Complexity:
               p(4) = 5
                    = 1*1*1 + 1*4*1
                    = 1*1 + 4*1
            Counting each abelian factor:
              abelian vector   number of factors
            ├────────────────┼───────────────────┤
              (3, 1)           2
              (2, 2)           3

        In 3 dimensions::

            sage: s = HypercubicBilliardSubshift((1,sqrt(2),pi))

        It may seem that something makes sense between the number of
        factors with given abelian vector and the complexity formula::

            sage: s.print_factor_complexity_by_abelian(2)
            Factor Complexity:
               p(2) = 7
                    = 1*1*1 + 1*2*2 + 2*1*1
                    = 1*1 + 2*2 + 2*1
            Counting each abelian factor:
              abelian vector   number of factors
            ├────────────────┼───────────────────┤
              (0, 0, 2)        1
              (1, 0, 1)        2
              (1, 1, 0)        2
              (0, 1, 1)        2

        ::

            sage: s.print_factor_complexity_by_abelian(3)
            Factor Complexity:
               p(3) = 13
                    = 1*1*1 + 1*3*2 + 2*3*1
                    = 1*1 + 3*2 + 6*1
            Counting each abelian factor:
              abelian vector   number of factors
            ├────────────────┼───────────────────┤
              (0, 0, 3)        1
              (0, 1, 2)        3
              (1, 0, 2)        3
              (1, 1, 1)        6

        ::

            sage: s.print_factor_complexity_by_abelian(4)
            Factor Complexity:
               p(4) = 21
                    = 1*1*1 + 1*4*2 + 2*6*1
                    = 1*1 + 4*2 + 12*1
            Counting each abelian factor:
              abelian vector   number of factors
            ├────────────────┼───────────────────┤
              (0, 2, 2)        1
              (1, 0, 3)        4
              (0, 1, 3)        4
              (1, 1, 2)        12

        But everything breaks down when looking at factors of length 5 or
        more::

            sage: s.print_factor_complexity_by_abelian(5)
            Factor Complexity:
               p(5) = 31
                    = 1*1*1 + 1*5*2 + 2*10*1
                    = 1*1 + 5*2 + 20*1
            Counting each abelian factor:
              abelian vector   number of factors
            ├────────────────┼───────────────────┤
              (0, 2, 3)        3
              (0, 1, 4)        3
              (1, 2, 2)        5
              (1, 1, 3)        20

        ::

            sage: s.print_factor_complexity_by_abelian(6)
            Factor Complexity:
               p(6) = 43
                    = 1*1*1 + 1*6*2 + 2*15*1
                    = 1*1 + 6*2 + 30*1
            Counting each abelian factor:
              abelian vector   number of factors
            ├────────────────┼───────────────────┤
              (0, 2, 4)        3
              (2, 1, 3)        4
              (1, 2, 3)        18
              (1, 1, 4)        18

        ::

            sage: s.print_factor_complexity_by_abelian(7)
            Factor Complexity:
               p(7) = 57
                    = 1*1*1 + 1*7*2 + 2*21*1
                    = 1*1 + 7*2 + 42*1
            Counting each abelian factor:
              abelian vector   number of factors
            ├────────────────┼───────────────────┤
              (2, 2, 3)        7
              (2, 1, 4)        9
              (1, 1, 5)        10
              (1, 2, 4)        31

        ::

            sage: v = [sqrt(p) for p in primes_first_n(7)]
            sage: s = HypercubicBilliardSubshift(v)
            sage: s.print_factor_complexity_by_abelian(2)
            Factor Complexity:
               p(2) = 43
                    = 1*1*1 + 1*2*6 + 2*1*15
                    = 1*1 + 2*6 + 2*15
            Counting each abelian factor:
              abelian vector          number of factors
            ├───────────────────────┼───────────────────┤
              (0, 0, 0, 0, 0, 0, 2)   1
              (1, 0, 1, 0, 0, 0, 0)   2
              (0, 1, 1, 0, 0, 0, 0)   2
              (0, 0, 1, 1, 0, 0, 0)   2
              (0, 0, 1, 0, 1, 0, 0)   2
              (0, 0, 1, 0, 0, 1, 0)   2
              (0, 0, 1, 0, 0, 0, 1)   2
              (1, 0, 0, 0, 0, 0, 1)   2
              (0, 1, 0, 0, 0, 0, 1)   2
              (0, 0, 0, 1, 0, 0, 1)   2
              (0, 0, 0, 0, 1, 0, 1)   2
              (0, 0, 0, 0, 0, 1, 1)   2
              (1, 0, 0, 1, 0, 0, 0)   2
              (0, 1, 0, 1, 0, 0, 0)   2
              (0, 0, 0, 1, 1, 0, 0)   2
              (0, 0, 0, 1, 0, 1, 0)   2
              (1, 1, 0, 0, 0, 0, 0)   2
              (1, 0, 0, 0, 1, 0, 0)   2
              (1, 0, 0, 0, 0, 1, 0)   2
              (0, 1, 0, 0, 1, 0, 0)   2
              (0, 0, 0, 0, 1, 1, 0)   2
              (0, 1, 0, 0, 0, 1, 0)   2

        ::

            sage: v = [sqrt(p) for p in primes_first_n(8)]
            sage: s = HypercubicBilliardSubshift(v)
            sage: s.print_factor_complexity_by_abelian(2)
            Factor Complexity:
               p(2) = 57
                    = 1*1*1 + 1*2*7 + 2*1*21
                    = 1*1 + 2*7 + 2*21
            Counting each abelian factor:
              abelian vector             number of factors
            ├──────────────────────────┼───────────────────┤
              (0, 0, 0, 0, 0, 0, 0, 2)   1
              (1, 0, 1, 0, 0, 0, 0, 0)   2
              (0, 1, 1, 0, 0, 0, 0, 0)   2
              (0, 0, 1, 1, 0, 0, 0, 0)   2
              (0, 0, 1, 0, 1, 0, 0, 0)   2
              (0, 0, 1, 0, 0, 1, 0, 0)   2
              (0, 0, 1, 0, 0, 0, 1, 0)   2
              (0, 0, 1, 0, 0, 0, 0, 1)   2
              (1, 0, 0, 0, 0, 0, 1, 0)   2
              (0, 0, 0, 0, 1, 0, 1, 0)   2
              (0, 1, 0, 0, 0, 0, 1, 0)   2
              (0, 0, 0, 0, 0, 0, 1, 1)   2
              (0, 0, 0, 1, 0, 0, 1, 0)   2
              (0, 0, 0, 0, 0, 1, 1, 0)   2
              (1, 0, 0, 1, 0, 0, 0, 0)   2
              (0, 1, 0, 1, 0, 0, 0, 0)   2
              (0, 0, 0, 1, 1, 0, 0, 0)   2
              (0, 0, 0, 1, 0, 1, 0, 0)   2
              (0, 0, 0, 1, 0, 0, 0, 1)   2
              (1, 0, 0, 0, 0, 0, 0, 1)   2
              (0, 1, 0, 0, 0, 0, 0, 1)   2
              (0, 0, 0, 0, 1, 0, 0, 1)   2
              (0, 0, 0, 0, 0, 1, 0, 1)   2
              (1, 1, 0, 0, 0, 0, 0, 0)   2
              (1, 0, 0, 0, 1, 0, 0, 0)   2
              (1, 0, 0, 0, 0, 1, 0, 0)   2
              (0, 0, 0, 0, 1, 1, 0, 0)   2
              (0, 1, 0, 0, 1, 0, 0, 0)   2
              (0, 1, 0, 0, 0, 1, 0, 0)   2

        """
        from sage.functions.other import factorial, binomial
        from sage.misc.table import table

        d = self.dimension()

        print("Factor Complexity:\n   p({}) = {}".format(n,self.complexity(n)))
        S = ["{}*{}*{}".format(factorial(k), binomial(n,k), binomial(d-1,k))
             for k in range(0, min(d-1,n)+1)]
        print("        =", ' + '.join(S))
        S = ["{}*{}".format(factorial(k)*binomial(n,k), binomial(d-1,k))
             for k in range(0, min(d-1,n)+1)]
        print("        =", ' + '.join(S))

        print("Counting each abelian factor:")
        L = self.language(n, prefix_length)
        c = Counter(tuple(w.abelian_vector()) for w in L)
        rows = sorted(c.items(), key=lambda row:row[1])
        header_row=["abelian vector", "number of factors"]
        print(table(rows=rows, header_row=header_row))

def check_open_question(d, n, prefix_length=10000):
    r"""
    INPUT:

    - ``d`` -- integer, dimension of billiard table
    - ``n`` -- integer, length of words
    - ``prefix_length`` -- integer (default:10000)

    EXAMPLES::

        sage: from slabbe.billiard_nD import check_open_question
        sage: check_open_question(5, 5, prefix_length=180000)   # long time
        WARNING: Factor complexity is p(5)=501, but only 496 factors found in the prefix of length 180000
        Factor Complexity:
           p(5) = 501
                = 1*1*1 + 1*5*4 + 2*10*6 + 6*10*4 + 24*5*1
                = 1*1 + 5*4 + 20*6 + 60*4 + 120*1
        Counting each abelian factor:
        WARNING: Factor complexity is p(5)=501, but only 496 factors found in the prefix of length 180000
          abelian vector    number of factors
        ├─────────────────┼───────────────────┤
          (0, 0, 2, 2, 1)   3
          (0, 2, 1, 1, 1)   6
          (0, 0, 2, 1, 2)   7
          (0, 1, 2, 1, 1)   10
          (1, 0, 2, 1, 1)   10
          (0, 1, 0, 2, 2)   15
          (0, 0, 1, 2, 2)   15
          (1, 0, 0, 2, 2)   15
          (1, 1, 0, 2, 1)   20
          (0, 1, 1, 2, 1)   20
          (1, 0, 1, 2, 1)   20
          (1, 1, 1, 0, 2)   55
          (1, 1, 0, 1, 2)   60
          (1, 0, 1, 1, 2)   60
          (0, 1, 1, 1, 2)   60
          (1, 1, 1, 1, 1)   120
        Factor Complexity:
           p(4) = 501
                = 1*1*1 + 1*4*5 + 2*6*10 + 6*4*10 + 24*1*5
                = 1*1 + 4*5 + 12*10 + 24*10 + 24*5
        Counting each abelian factor:
        WARNING: Factor complexity is p(4)=501, but only 476 factors found in the prefix of length 180000
          abelian vector       number of factors
        ├────────────────────┼───────────────────┤
          (0, 0, 0, 2, 1, 1)   2
          (0, 0, 0, 0, 2, 2)   3
          (1, 0, 0, 0, 2, 1)   4
          (0, 1, 0, 0, 2, 1)   4
          (0, 0, 0, 1, 2, 1)   4
          (0, 0, 1, 0, 2, 1)   4
          (1, 1, 0, 0, 0, 2)   6
          (1, 0, 1, 0, 0, 2)   7
          (0, 1, 0, 1, 0, 2)   8
          (0, 0, 1, 1, 0, 2)   8
          (0, 1, 1, 0, 0, 2)   9
          (1, 0, 0, 1, 0, 2)   9
          (1, 0, 0, 0, 1, 2)   12
          (0, 1, 0, 0, 1, 2)   12
          (0, 0, 1, 0, 1, 2)   12
          (0, 0, 0, 1, 1, 2)   12
          (1, 1, 1, 1, 0, 0)   24
          (1, 1, 1, 0, 1, 0)   24
          (1, 1, 1, 0, 0, 1)   24
          (1, 1, 0, 1, 0, 1)   24
          (1, 1, 0, 1, 1, 0)   24
          (1, 1, 0, 0, 1, 1)   24
          (1, 0, 1, 0, 1, 1)   24
          (1, 0, 0, 1, 1, 1)   24
          (0, 1, 0, 1, 1, 1)   24
          (0, 1, 1, 0, 1, 1)   24
          (1, 0, 1, 1, 0, 1)   24
          (1, 0, 1, 1, 1, 0)   24
          (0, 1, 1, 1, 1, 0)   24
          (0, 1, 1, 1, 0, 1)   24
          (0, 0, 1, 1, 1, 1)   24

    """
    from sage.arith.misc import primes_first_n
    try:
        from sage.misc.functional import sqrt
    except ImportError:
        from sage.functions.other import sqrt

    v = [sqrt(p) for p in primes_first_n(d)]
    s = HypercubicBilliardSubshift(v)
    L = s.language(n, prefix_length=prefix_length)
    s.print_factor_complexity_by_abelian(n, prefix_length=prefix_length)

    v2 = [sqrt(p) for p in primes_first_n(n+1)]
    s2 = HypercubicBilliardSubshift(v2)
    L2 = s.language(d-1, prefix_length=prefix_length)
    s2.print_factor_complexity_by_abelian(d-1, prefix_length=prefix_length)

