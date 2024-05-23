# -*- coding: utf-8 -*-
r"""
q-analog of Markoff numbers

EXAMPLES::

    sage: from slabbe.q_markoff import mu, mu_q, mu_12, mu_q_12
    sage: W = FiniteWords([0,1])
    sage: u = W([0,1,1,0,0,0,1,1,0])
    sage: mu(u)
    [100385  58807]
    [ 58807  34450]
    sage: mu_12(u)
    58807
    sage: mu_q_12(u)
    q^24 + 8*q^23 + 36*q^22 + 119*q^21 + 313*q^20 + 692*q^19 + 1325*q^18 + 2243*q^17 + 3405*q^16 + 4680*q^15 + 5861*q^14 + 6717*q^13 + 7061*q^12 + 6812*q^11 + 6026*q^10 + 4874*q^9 + 3587*q^8 + 2385*q^7 + 1417*q^6 + 741*q^5 + 333*q^4 + 125*q^3 + 37*q^2 + 8*q + 1

::

    sage: from slabbe.q_markoff import L,R,A,B
    sage: L,R,A,B
    (
    [1 0]  [1 1]  [2 1]  [5 2]
    [1 1], [0 1], [1 1], [2 1]
    )
    sage: from slabbe.q_markoff import Lq,Rq,Aq,Bq
    sage: Lq,Rq,Aq,Bq
    (
    [q 0]  [q 1]  [q^2 + q       1]
    [q 1], [0 1], [      q       1],
    <BLANKLINE>
    [q^4 + q^3 + 2*q^2 + q                 q + 1]
    [              q^2 + q                     1]
    )

"""
#*****************************************************************************
#       Copyright (C) 2024 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
import itertools, collections

from sage.matrix.constructor import matrix
from sage.matrix.special import identity_matrix
from sage.rings.integer_ring import ZZ
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.misc.misc_c import prod

L = matrix(2, (1,0,1,1))
R = matrix(2, (1,1,0,1))
A = matrix(2, (2,1,1,1))
B = matrix(2, (5,2,2,1))

K1 = PolynomialRing(ZZ, 'q', order='neglex')
q = K1.gen()

Lq = matrix(2, (q,0,q,1))
Rq = matrix(2, (q,1,0,1))
Aq = matrix(2, (q+q**2,1,q,1))
Bq = matrix(2, (q+2*q**2+q**3+q**4,1+q,q+q**2,1))

AqBq_dict = {'a':Aq, 'b':Bq}

def mu(w):
    r"""
    INPUT:

    - ``w`` -- binary word

    EXAMPLES::

        sage: from slabbe.q_markoff import mu
        sage: W = FiniteWords('ab')
        sage: W
        Finite words over {'a', 'b'}
        sage: mu(W('aa'))
        [5 3]
        [3 2]
        sage: mu(W('a'))
        [2 1]
        [1 1]
        sage: mu(W('abb'))
        [70 29]
        [41 17]

    """
    if hasattr(w, 'parent') and hasattr(w.parent(),'alphabet'):
        alphabet = w.parent().alphabet()
    else:
        alphabet = sorted(set(w))
    a,b = alphabet
    AB_dict = {a:A, b:B}
    I = identity_matrix(2)
    return prod((AB_dict[a] for a in w), I)

def mu_q(w):
    r"""
    INPUT:

    - ``w`` -- binary word

    EXAMPLES:

        sage: from slabbe.q_markoff import mu_q
        sage: W = FiniteWords('ab')
        sage: mu_q(W(''))
        [1 0]
        [0 1]
        sage: mu_q(W('a'))
        [q^2 + q       1]
        [      q       1]
        sage: mu_q(W('b'))
        [q^4 + q^3 + 2*q^2 + q                 q + 1]
        [              q^2 + q                     1]
        sage: mu_q(W('ab'))
        [q^6 + 2*q^5 + 3*q^4 + 3*q^3 + 2*q^2 + q                     q^3 + 2*q^2 + q + 1]
        [          q^5 + q^4 + 2*q^3 + 2*q^2 + q q^2 + q + 1]

    """
    if hasattr(w, 'parent') and hasattr(w.parent(),'alphabet'):
        alphabet = w.parent().alphabet()
    else:
        alphabet = sorted(set(w))
    a,b = alphabet
    AB_dict = {a:Aq, b:Bq}
    I = identity_matrix(2)
    return prod((AB_dict[a] for a in w), I)

def mu_12(w):
    r"""
    Return the entry at position (1,2) in the matrix mu(w)

    .. NOTE:: Returns a Markoff number is when w is Christoffel

    INPUT:

    - ``w`` -- binary word

    OUTPUT:

    integer

    EXAMPLES::

        sage: from slabbe.q_markoff import mu_12
        sage: W = FiniteWords('ab')
        sage: mu_12(W('a'))
        1
        sage: mu_12(W('b'))
        2
        sage: mu_12(W('ab'))
        5

    The smallest non injective example::

        sage: u = W('abaabb')
        sage: v = W('aabbab')
        sage: mu_12(u)
        1130
        sage: mu_12(v)
        1130

    But become injective if we extend by one letter::

        sage: u = W('abaabb')
        sage: v = W('aabbab')
        sage: a = W('a')
        sage: b = W('b')
        sage: mu_12(u+a)
        3857
        sage: mu_12(v+a)
        3827
        sage: mu_12(u+b)
        6584
        sage: mu_12(v+b)
        6524
        sage: mu_12(a+u)
        2923
        sage: mu_12(a+v)
        2953
        sage: mu_12(b+u)
        6976
        sage: mu_12(b+v)
        7036

    """
    return mu(w)[0,1]

def mu_q_12(w):
    r"""
    Return the entry at position (1,2) in the matrix mu(w)

    INPUT:

    - ``w`` -- binary word

    OUTPUT:

    polynomial in q

    EXAMPLES::

        sage: from slabbe.q_markoff import mu_q_12
        sage: W = FiniteWords('ab')
        sage: mu_q_12(W(''))
        0
        sage: mu_q_12(W('a'))
        1
        sage: mu_q_12(W('b'))
        q + 1
        sage: mu_q_12(W('ab'))
        q^3 + 2*q^2 + q + 1

    """
    return mu_q(w)[0,1]

