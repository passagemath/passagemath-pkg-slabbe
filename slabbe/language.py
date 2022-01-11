# -*- coding: utf-8 -*-
r"""
Regular languages

EXAMPLES:

Language over all finite words on an alphabet::

    sage: from slabbe.language import Language
    sage: Language(alphabet=['a', 'b'])
    Language of finite words over alphabet ['a', 'b']

Finite language::

    sage: from slabbe.language import FiniteLanguage
    sage: S = ['a', 'ab', 'aab', 'aaab']
    sage: FiniteLanguage(alphabet=['a', 'b'], words=S)
    Finite language of cardinality 4 over alphabet ['a', 'b']

Regular language::

    sage: from slabbe.language import RegularLanguage
    sage: alphabet = ['a', 'b']
    sage: trans = [(0, 1, 'a'), (1, 2, 'b'), (2, 3, 'b'), (3, 4, 'a')]
    sage: automaton = Automaton(trans, initial_states=[0], final_states=[4])
    sage: RegularLanguage(alphabet, automaton)
    Regular language over ['a', 'b']
    defined by: Automaton with 5 states

Predefined languages::

    sage: from slabbe.language import languages
    sage: languages.ARP()
    Regular language over [1, 2, 3, 123, 132, 213, 231, 312, 321]
    defined by: Automaton with 7 states

AUTHORS:

 - Sébastien Labbé, initial clean and full doctested version, October 2015
"""
#*****************************************************************************
#       Copyright (C) 2015 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from __future__ import absolute_import, print_function
import itertools
from sage.combinat.words.words import Words
from sage.combinat.finite_state_machine import Automaton

class Language(object):
    r"""
    Language of finite words

    INPUT:

    - ``alphabet`` -- iterable of letters

    EXAMPLES::

        sage: from slabbe.language import Language
        sage: Language(alphabet=['a', 'b'])
        Language of finite words over alphabet ['a', 'b']
    """
    def __init__(self, alphabet):
        r"""
        EXAMPLES::

            sage: from slabbe.language import Language
            sage: Language(alphabet=['a', 'b'])
            Language of finite words over alphabet ['a', 'b']
        """
        self._alphabet = sorted(alphabet)

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe.language import Language
            sage: Language(alphabet=['a'])
            Language of finite words over alphabet ['a']
        """
        s = "Language of finite words over alphabet {}"
        return s.format(self._alphabet)

    def words_of_length_iterator(self, length):
        r"""
        Return an iterator over words of given length.

        INPUT:

        - ``length`` -- integer

        EXAMPLES::

            sage: from slabbe.language import Language
            sage: F = Language(alphabet=['a', 'b'])
            sage: it = F.words_of_length_iterator(2)
            sage: list(it)
            [word: aa, word: ab, word: ba, word: bb]
        """
        W = Words(self._alphabet)
        return W.iterate_by_length(length)

    def complexity(self, length):
        r"""
        Returns the number of words of given length.

        .. NOTE::

            This method is defined from :func:`~words_of_length_iterator`.

        INPUT:

        - ``length`` -- integer

        EXAMPLES::

            sage: from slabbe.language import Language
            sage: F = Language(alphabet=['a', 'b'])
            sage: [F.complexity(n) for n in range(5)]
            [1, 2, 4, 8, 16]
        """
        return sum(1 for _ in self.words_of_length_iterator(length))
class FiniteLanguage(Language):
    r"""
    Finite language

    INPUT:

    - ``alphabet`` -- iterable of letters
    - ``words`` -- finite iterable of words

    EXAMPLES::

        sage: from slabbe.language import FiniteLanguage
        sage: L = ['a', 'aa', 'aaa']
        sage: FiniteLanguage(alphabet=['a'], words=L)
        Finite language of cardinality 3 over alphabet ['a']
    """
    def __init__(self, alphabet, words):
        r"""
        EXAMPLES::

            sage: from slabbe.language import FiniteLanguage
            sage: L = ['a', 'aa', 'aaa']
            sage: F = FiniteLanguage(alphabet=['a'], words=L)
        """
        Language.__init__(self, alphabet)
        self._words = words
    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe.language import FiniteLanguage
            sage: L = ['a', 'ab', 'aab', 'aaab']
            sage: FiniteLanguage(alphabet=['a', 'b'], words=L)
            Finite language of cardinality 4 over alphabet ['a', 'b']
        """
        s = "Finite language of cardinality {} over alphabet {}"
        return s.format(len(self._words), self._alphabet)

    def automaton(self):
        r"""
        Return the automaton recognizing this finite language.

        EXAMPLES::

            sage: from slabbe.language import FiniteLanguage
            sage: L = ['a', 'aa', 'aaa']
            sage: F = FiniteLanguage(alphabet=['a'], words=L)
            sage: F.automaton()
            Automaton with 7 states
        """
        transitions = []
        final_states = []
        end = 1
        for w in self._words:
            start = 0
            for a in w:
                transitions.append((start, end, a))
                start, end = end, end+1
            final_states.append(start)
        return Automaton(transitions, initial_states=[0], final_states=final_states)

    def minimal_automaton(self):
        r"""
        Return the minimal automaton recognizing this finite language.

        .. NOTE:: 
        
            One of the state is not final. You may want to remove it...

        EXAMPLES::

            sage: from slabbe.language import FiniteLanguage
            sage: L = ['a', 'aa', 'aaa']
            sage: F = FiniteLanguage(alphabet=['a'], words=L)
            sage: F.minimal_automaton()
            Automaton with 5 states
        """
        return self.automaton().minimization().relabeled()

    def number_of_states(self):
        r"""
        EXAMPLES::

            sage: from slabbe.language import FiniteLanguage
            sage: L = ['a', 'aa', 'aaa']
            sage: F = FiniteLanguage(alphabet=['a'], words=L)
            sage: F.number_of_states()
            5
        """
        return len(self.minimal_automaton().states())

class RegularLanguage(Language):
    r"""
    Regular language

    INPUT:

    - ``alphabet`` -- iterable of letters
    - ``automaton`` -- finite state automaton

    EXAMPLES::

        sage: from slabbe.language import RegularLanguage
        sage: alphabet = ['a', 'b']
        sage: trans = [(0, 1, 'a'), (1, 2, 'b'), (2, 3, 'b'), (3, 4, 'a')]
        sage: automaton = Automaton(trans, initial_states=[0], final_states=[4])
        sage: RegularLanguage(alphabet, automaton)
        Regular language over ['a', 'b']
        defined by: Automaton with 5 states
    """
    def __init__(self, alphabet, automaton):
        r"""
        EXAMPLES::

            sage: from slabbe.language import RegularLanguage
            sage: alphabet = ['a', 'b']
            sage: trans = [(0, 1, 'a'), (1, 2, 'b'), (2, 3, 'b'), (3, 4, 'a')]
            sage: automaton = Automaton(trans, initial_states=[0], final_states=[4])
            sage: R = RegularLanguage(alphabet, automaton)
        """
        Language.__init__(self, alphabet)
        self._automaton = automaton


    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe.language import RegularLanguage
            sage: alphabet = ['a', 'b']
            sage: trans = [(0, 1, 'a'), (1, 2, 'b'), (2, 3, 'b'), (3, 4, 'a')]
            sage: automaton = Automaton(trans, initial_states=[0], final_states=[4])
            sage: RegularLanguage(alphabet, automaton)
            Regular language over ['a', 'b']
            defined by: Automaton with 5 states
        """
        s = "Regular language over {}\ndefined by: {}"
        return s.format(self._alphabet, self._automaton)

    def words_of_length_iterator(self, length):
        r"""
        Return an iterator over words of given length.

        INPUT:

        - ``length`` -- integer

        EXAMPLES::

            sage: from slabbe.language import RegularLanguage
            sage: alphabet = ['a', 'b']
            sage: trans = [(0, 1, 'a'), (1, 2, 'b'), (2, 3, 'b'), (3, 4, 'a')]
            sage: automaton = Automaton(trans, initial_states=[0], final_states=[4])
            sage: R = RegularLanguage(alphabet, automaton)
            sage: [list(R.words_of_length_iterator(i)) for i in range(6)]
            [[], [], [], [], [word: abba], []]
        """
        it = super(RegularLanguage, self).words_of_length_iterator(length)
        return [a for a in it if self._automaton(a)]

class SturmianLanguage(Language):
    def __init__(self, alphabet):
        r"""
        INPUT:

        - ``alphabet`` -- list of size 2

        EXAMPLES::

            sage: from slabbe.language import SturmianLanguage
            sage: S = SturmianLanguage(['a', 'b'])
            sage: [S.complexity(n) for n in range(5)]
            [1, 2, 4, 8, 14]

        The number of factors of length n is well-known (http://oeis.org/A005598)::

            sage: [len(set(S.words_of_length_iterator(i))) for i in range(15)] # not tested
            [1, 2, 4, 8, 14, 24, 36, 54, 76, 104, 136, 178, 224, 282, 346]
            sage: oeis.find_by_subsequence(_)                                  # not tested
            0: A005598: a(n) = 1 + Sum_{i=1..n} (n-i+1)*phi(i).

        """
        self._alphabet = list(alphabet)
        self._parent = Words(self._alphabet)
        if not len(self._alphabet) == 2:
            raise ValueError('alphabet(={}) must be of size 2'.format(self._alphabet))

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe.language import SturmianLanguage
            sage: SturmianLanguage(alphabet=['a', 'b'])
            Language of all Sturmian factors over alphabet ['a', 'b']
        """
        s = "Language of all Sturmian factors over alphabet {}"
        return s.format(self._alphabet)

    def unit_square_parameter_partition(self, length):
        r"""
        Return the partition of the unit square where each polygonal atom
        represents the set of parameter associated to a factor of length n.

        See Chapter 2 from this book:

        Filiot, Emmanuel, Anna Frid, Franck Hétroy-Wheeler, Kolja Knauer,
        Arnaud Labourel, Jean-Luc Mari, Pierre-Alain Reynier, et Gérard
        Subsol. Informatique Mathématique Une photographie en 2019.
        https://www.gdr-im.fr/im-photographie/

        EXAMPLES::

            sage: from slabbe.language import SturmianLanguage
            sage: S = SturmianLanguage('ab')
            sage: S.unit_square_parameter_partition(5)
            Polyhedron partition of 24 atoms with 24 letters

        We check that the sizes are ok::

            sage: [len(S.unit_square_parameter_partition(i)) for i in range(10)] # long time (2s)
            [1, 2, 4, 8, 14, 24, 36, 54, 76, 104]
            sage: oeis.find_by_subsequence(_)                   # not tested
            0: A005598: a(n) = 1 + Sum_{i=1..n} (n-i+1)*phi(i).

        TESTS::

            sage: [len(S.unit_square_parameter_partition(i)) for i in range(15)] # not tested
            [1, 2, 4, 8, 14, 24, 36, 54, 76, 104, 136, 178, 224, 282, 346]

        """
        from slabbe import PolyhedronPartition
        from sage.geometry.polyhedron.library import polytopes
        # square = polytopes.hypercube(2, intervals='zero_one') # broken in sage 9.0
        square = polytopes.hypercube(2, intervals=[[0,1]]*2)
        P = PolyhedronPartition([square])
        for i in range(1, length+1):
            for j in range(1, i+1):
                P = P.refine_by_hyperplane([j,-i,-1])
        return P

    def factor(self, slope, intercept, length):
        r"""

        EXAMPLES::

            sage: from slabbe.language import SturmianLanguage
            sage: S = SturmianLanguage('ab')
            sage: S.factor(1/3, 0, 5)
            word: aabaa
            sage: S.factor(1/3, 4/5, 5)
            word: baaba

        """
        from sage.functions.other import floor
        L = [floor((n+1)*slope + intercept) - floor(n*slope + intercept)
                for n in range(length)]
        L = [self._alphabet[a] for a in L]
        return self._parent(L)

    def words_of_length_iterator(self, length):
        r"""
        Return an iterator over words of given length.

        INPUT:

        - ``length`` -- integer

        EXAMPLES::

            sage: from slabbe.language import SturmianLanguage
            sage: S = SturmianLanguage('ab')
            sage: sorted(S.words_of_length_iterator(0))
            [word: ]
            sage: sorted(S.words_of_length_iterator(1))
            [word: a, word: b]
            sage: sorted(S.words_of_length_iterator(2))
            [word: aa, word: ab, word: ba, word: bb]
            sage: sorted(S.words_of_length_iterator(3))
            [word: aaa,
             word: aab,
             word: aba,
             word: abb,
             word: baa,
             word: bab,
             word: bba,
             word: bbb]
            sage: sorted(S.words_of_length_iterator(4))
            [word: aaaa,
             word: aaab,
             word: aaba,
             word: abaa,
             word: abab,
             word: abba,
             word: abbb,
             word: baaa,
             word: baab,
             word: baba,
             word: babb,
             word: bbab,
             word: bbba,
             word: bbbb]

        ::

            sage: [len(set(S.words_of_length_iterator(i))) for i in range(10)] # long time
            [1, 2, 4, 8, 14, 24, 36, 54, 76, 104]

        """
        P = self.unit_square_parameter_partition(length)
        for atom in P.atoms():
            slope,intercept = atom.center()
            w = self.factor(slope, intercept, length)
            yield w

#####################
# Language generators
#####################
class LanguageGenerator(object):
    def ARP(self):
        r"""
        Return the Arnoux-Rauzy-Poincaré regular language.

            sage: from slabbe.language import languages
            sage: L = languages.ARP()
            sage: L
            Regular language over [1, 2, 3, 123, 132, 213, 231, 312, 321]
            defined by: Automaton with 7 states
            sage: [L.complexity(n) for n in range(4)]
            [1, 9, 57, 345]
        """
        alphabet = [1, 2, 3, 123, 132, 213, 231, 312, 321]
        automaton = self._ARP_automaton()
        return RegularLanguage(alphabet, automaton)

    def _ARP_automaton(self):
        r"""
        Return the automaton for the ARP language.

        EXAMPLES::

            sage: from slabbe.language import languages
            sage: A = languages._ARP_automaton()
            sage: A
            Automaton with 7 states

        TESTS::

            sage: A.process([1, 312, 1, 213])
            (True, 'H213')
            sage: A([1, 312, 1, 213])
            True
        """
        def H(i,j,k):
            return 'H{}{}{}'.format(i,j,k)
        def P(i,j,k):
            return int('{}{}{}'.format(i,j,k))
        def A(k):
            return int('{}'.format(k))
        D = 'Delta'
        states = [H(*p) for p in itertools.permutations((1,2,3))] + [D]
        autom = Automaton(initial_states=[D], final_states=states)
        for p in itertools.permutations((1,2,3)):
            i,j,k = p
            v = H(*p)
            autom.add_transition(v, H(k,i,j), P(k,i,j))
            autom.add_transition(v, H(j,k,i), P(j,k,i))
            autom.add_transition(v, H(k,j,i), P(k,j,i))
            autom.add_transition(v, D, A(i))
            autom.add_transition(v, v, A(j))
            autom.add_transition(D, v, P(i,j,k))
        for k in [1,2,3]:
            autom.add_transition(D, D, A(k))
        return autom

    def Brun(self):
        r"""
        Return the Brun regular language.

        EXAMPLES::

            sage: from slabbe.language import languages
            sage: L = languages.Brun()
            sage: L
            Regular language over [123, 132, 213, 231, 312, 321]
            defined by: Automaton with 6 states
            sage: [L.complexity(n) for n in range(4)]
            [1, 6, 18, 54]
            sage: list(L.words_of_length_iterator(2))
            [word: 123,123,
             word: 123,132,
             word: 123,312,
             word: 132,123,
             word: 132,132,
             word: 132,213,
             word: 213,213,
             word: 213,231,
             word: 213,321,
             word: 231,123,
             word: 231,213,
             word: 231,231,
             word: 312,231,
             word: 312,312,
             word: 312,321,
             word: 321,132,
             word: 321,312,
             word: 321,321]
        """
        alphabet = [123, 132, 213, 231, 312, 321]
        automaton = self._Brun_automaton()
        return RegularLanguage(alphabet, automaton)

    def _Brun_automaton(self):
        r"""
        Return the automaton for the Brun language.

        EXAMPLES::

            sage: from slabbe.language import languages
            sage: A = languages._Brun_automaton()
            sage: A
            Automaton with 6 states

        TESTS::

            sage: A([123, 123, 132, 213])
            True
            sage: A([123, 123, 132, 213, 123])
            False
        """
        def B(i,j,k):
            return int('{}{}{}'.format(i,j,k))
        states = [B(*p) for p in itertools.permutations((1,2,3))]
        autom = Automaton(initial_states=states, final_states=states)
        for p in itertools.permutations((1,2,3)):
            i,j,k = p
            autom.add_transition(B(*p), B(i,j,k), B(i,j,k))
            autom.add_transition(B(*p), B(i,k,j), B(i,k,j))
            autom.add_transition(B(*p), B(k,i,j), B(k,i,j))
        return autom

    def Selmer(self):
        r"""
        Return the Selmer regular language.

        EXAMPLES::

            sage: from slabbe.language import languages
            sage: L = languages.Selmer()
            sage: L
            Regular language over [123, 132, 213, 231, 312, 321]
            defined by: Automaton with 6 states
            sage: [L.complexity(n) for n in range(4)]
            [1, 6, 12, 24]
            sage: list(L.words_of_length_iterator(2))
            [word: 123,132,
             word: 123,312,
             word: 132,123,
             word: 132,213,
             word: 213,231,
             word: 213,321,
             word: 231,123,
             word: 231,213,
             word: 312,231,
             word: 312,321,
             word: 321,132,
             word: 321,312]
        """
        alphabet = [123, 132, 213, 231, 312, 321]
        automaton = self._Selmer_automaton()
        return RegularLanguage(alphabet, automaton)

    def _Selmer_automaton(self):
        r"""
        Return the automaton for the Selmer language.

        EXAMPLES::

            sage: from slabbe.language import languages
            sage: A = languages._Selmer_automaton()
            sage: A
            Automaton with 6 states

        TESTS::

            sage: A([123, 132, 213])
            True
            sage: A([123, 132, 213, 123])
            False
        """
        def S(i,j,k):
            return int('{}{}{}'.format(i,j,k))
        states = [S(*p) for p in itertools.permutations((1,2,3))]
        autom = Automaton(initial_states=states, final_states=states)
        for p in itertools.permutations((1,2,3)):
            i,j,k = p
            autom.add_transition(S(*p), S(i,k,j), S(i,k,j))
            autom.add_transition(S(*p), S(k,i,j), S(k,i,j))
        return autom

    def Cassaigne(self):
        r"""
        Return the Cassaigne regular language over the alphabet
        [11, 22, 122, 211, 121, 212].

        EXAMPLES::

            sage: from slabbe.language import languages
            sage: L = languages.Cassaigne()
            sage: L
            Regular language over [11, 22, 121, 122, 211, 212]
            defined by: Automaton with 1 state
            sage: [L.complexity(n) for n in range(4)]
            [1, 6, 36, 216]
        """
        alphabet = [11, 22, 122, 211, 121, 212]
        automaton = self._Cassaigne_automaton()
        return RegularLanguage(alphabet, automaton)

    def _Cassaigne_automaton(self):
        r"""
        Return the automaton for the Cassaigne language over the alphabet
        [11, 22, 122, 211, 121, 212].

        EXAMPLES::

            sage: from slabbe.language import languages
            sage: A = languages._Cassaigne_automaton()
            sage: A
            Automaton with 1 state
        """
        q = 0
        states = [q]
        autom = Automaton(initial_states=states, final_states=states)
        alphabet = [11, 22, 122, 211, 121, 212]
        for i in alphabet:
            autom.add_transition(q, q, i)
        return autom

languages = LanguageGenerator()
