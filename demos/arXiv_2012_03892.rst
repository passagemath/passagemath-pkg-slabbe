==========================================================================
Three characterizations of a self-similar aperiodic 2-dimensional subshift
==========================================================================

:author: Sébastien Labbé, Nov 18, 2020

This file countains a copy of the SageMath code present in the chapter.

.. default-role:: math
.. .. |Xcal| mathmacro:: \mathcal{X}

Section 1.4: Wang shifts
------------------------

First we define the set `\Ucal` of Wang tiles in SageMath

::

    sage: from slabbe import WangTileSet
    sage: tiles = ["FOJO", "FOHL", "JMFP", "DMFK", "HPJP", "HPHN", "HKFP", "HKDP", 
    ....:          "BOIO", "GLEO", "GLCL", "ALIO", "EPGP", "EPIP", "IPGK", "IPIK",
    ....:          "IKBM", "IKAK", "CNIP"]
    sage: U = WangTileSet([tuple(tile) for tile in tiles])

We desubstitute `\Ucal` with the set `\{0, 1, 2, 3, 4, 5, 6, 7\}` :math:`\alpha`
of markers in the direction `\be_2`:

.. link

::

    sage: U.find_markers(i=2,radius=2,solver="dancing_links")
    [[0, 1, 2, 3, 4, 5, 6, 7]]
    sage: M = [0, 1, 2, 3, 4, 5, 6, 7]
    sage: V,alpha0 = U.find_substitution(M, i=2, radius=2, solver="dancing_links")

We obtain `\alpha_0:\Omega_\Vcal\to\Omega_\Ucal` given as a rule of the form
`\alpha_0:&\Zrange{20}\to\Zrange{18}^{*^2}`

We desubstitute `\Vcal` with the set `\{0, 1, 2, 8, 9, 10, 11\}`
of markers in the direction `\be_1`:

.. link

::

    sage: V.find_markers(i=1,radius=1,solver="dancing_links")
    [[0, 1, 2, 8, 9, 10, 11],
    [3, 5, 13, 14, 17, 20],
    [4, 6, 7, 12, 15, 16, 18, 19]]
    sage: M = [0, 1, 2, 8, 9, 10, 11]
    sage: W,alpha1 = V.find_substitution(M, i=1, radius=1, solver="dancing_links")

We obtain `\alpha_1:\Omega_\Wcal\to\Omega_\Vcal` given as a rule of the form
`\alpha_1:&\Zrange{18}\to\Zrange{20}^{*^2}`

It turns out that `\Ucal` and `\Wcal` are equivalent

.. link

::

    sage: W.is_equivalent(U)
    True

The bijection \texttt{vert} between the vertical colors,
the bijection \texttt{horiz} between the horizontal colors
and bijection `\alpha_2` from `\Ucal` to `\Wcal` is computed as follows

.. link

::

    sage: _,vert,horiz,alpha2 = U.is_equivalent(W, certificate=True)
    sage: vert
    {'A': 'IJ',
     'B': 'IH',
     'C': 'BF',
     'D': 'G',
     'E': 'AF',
     'F': 'I',
     'G': 'ID',
     'H': 'B',
     'I': 'GF',
     'J': 'A'}
    sage: horiz
    {'K': 'PO', 'L': 'M', 'M': 'PL', 'N': 'MO', 'O': 'K', 'P': 'KO'}

We obtain the morphism `\alpha_2:\Omega_\Ucal\to\Omega_\Wcal` given as a rule of the form
`\alpha_2:&\Zrange{18}\to\Zrange{18}^{*^2}`

We may check that `\alpha_0\circ\alpha_1\circ\alpha_2=\phi`

.. link

::

    sage: from slabbe import Substitution2d
    sage: Phi = Substitution2d({0: [[17]], 1: [[16]], 2: [[15], [11]],
    ....: 3: [[13], [9]], 4: [[17], [8]], 5: [[16], [8]], 6: [[15], [8]],
    ....: 7: [[14], [8]], 8: [[14, 6]], 9: [[17, 3]], 10: [[16, 3]],
    ....: 11: [[14, 2]], 12: [[15, 7], [11, 1]], 13: [[14, 6], [11, 1]],
    ....: 14: [[13, 7], [9, 1]], 15: [[12, 6], [9, 1]], 16: [[18, 5], [10, 1]],
    ....: 17: [[13, 4], [9, 1]], 18: [[14, 2], [8, 0]]})
    sage: alpha0 * alpha1 * alpha2 == Phi
    True

We conclude that

.. MATH::

    \Omega_\Ucal
        =\overline{\alpha_0(\Omega_\Vcal)}^\sigma
        =\overline{\alpha_0\alpha_1(\Omega_\Wcal)}^\sigma
        =\overline{\alpha_0\alpha_1\alpha_2(\Omega_\Ucal)}^\sigma
        =\overline{\phi(\Omega_\Ucal)}^\sigma.

In the proof, we used Knuth's dancing links algorithm \cite{knuth_dancing_2000}
because it is faster at this particular task than the MILP solver Gurobi
\cite{gurobi} or the SAT solvers Glucose \cite{doi:10.1142/S0218213018400018}
as we can see below:

.. link

::

    sage: U.find_markers(i=2,radius=2,solver="dancing_links") # long time (3s)
    [[0, 1, 2, 3, 4, 5, 6, 7]]
    sage: U.find_markers(i=2,radius=2,solver="gurobi") # long time (13s) # optional gurobi
    [[0, 1, 2, 3, 4, 5, 6, 7]]
    sage: U.find_markers(i=2,radius=2,solver="glucose") # long time (2min 10s) # optional glucose # not tested
    [[0, 1, 2, 3, 4, 5, 6, 7]]

Note that for other tasks like finding a valid tiling an `n\times n` square
with Wang tiles, the Glucose SAT solver \cite{doi:10.1142/S0218213018400018}
based on MiniSAT \cite{minisat} is faster \cite{labbe_comparison_2018} than
Knuth's dancing links algorithm or MILP solvers.

Section 1.5: Coding of toral `\Z^2`-rotations
---------------------------------------------

First, one may import the necessary functions and define the golden mean
\texttt{phi} as an element of a number field defined by a quadratic
polynomial which is more efficient when doing arithmetic operations and
comparisons

.. link

::

    sage: from slabbe import PolyhedronExchangeTransformation as PET
    sage: from slabbe.arXiv_1903_06137 import self_similar_19_atoms_partition
    sage: z = polygen(QQ, 'z')
    sage: K.<phi> = NumberField(z**2-z-1, 'phi', embedding=RR(1.6))

The proof uses Proposition~\ref{prop:orbit-preimage} two times to induce both
the vertical and horizontal actions, starting with the vertical action.
We begin with the lattice `\Gamma_0=\Z^2`, the partition `\Pcal_\Ucal`, the
coding map `\sccode_0:\R^2/\Gamma_0\to\A_0`, the alphabet `\A_0=\Zrange{18}`
and `\Z^2`-action `R_\Ucal` defined on `\torus^2` as shown below

.. link

:: 

    sage: Gamma0 = matrix.column([(1,0), (0,1)])
    sage: PU = self_similar_19_atoms_partition()
    sage: RUe1 = PET.toral_translation(Gamma0, vector((phi^-2,0)))
    sage: RUe2 = PET.toral_translation(Gamma0, vector((0,phi^-2)))

From Proposition~\ref{prop:orbit-preimage}, then `\Xcal_{\Pcal_\Ucal,R_\Ucal}=
\overline{\beta_0(\Xcal_{\Pcal_1,R_1})}^\sigma`. The partition `\Pcal_1`, the
action `R_1` and substitution `\beta_0` are given below with alphabet
`\A_1=\Zrange{20}`

.. link

::

    sage: y_ineq = [phi^-1, 0, -1] # y <= phi^-1 (see Polyhedron? for syntax)
    sage: P1,beta0 = RUe2.induced_partition(y_ineq, PU, substitution_type='column')
    sage: R1e1,_ = RUe1.induced_transformation(y_ineq)
    sage: R1e2,_ = RUe2.induced_transformation(y_ineq)

From Proposition~\ref{prop:orbit-preimage}, then `\Xcal_{\Pcal_1,R_1}=
\overline{\beta_1(\Xcal_{\Pcal_2,R_2})}^\sigma`.  The partition `\Pcal_2`, the
action `R_2` and substitution `\beta_1` are given below with alphabet
`\A_2=\Zrange{18}`

.. link

::

    sage: x_ineq = [phi^-1, -1, 0] # x <= phi^-1 (see Polyhedron? for syntax)
    sage: P2,beta1 = R1e1.induced_partition(x_ineq, P1, substitution_type='row')
    sage: R2e1,_ = R1e1.induced_transformation(x_ineq)
    sage: R2e2,_ = R1e2.induced_transformation(x_ineq)

We define `\Pcal_2'=h(\Pcal_2)`, `\sccode_2'=\sccode_2\circ h^{-1}`,
`(R'_2)^\bn=h\circ (R_2)^\bn\circ h^{-1}` as shown below

.. link

::

    sage: P2_scaled = (-phi*P2).translate((1,1))

We observe that the scaled partition `\Pcal_2'` is the same as `\Pcal_\Ucal` up
to a permutation `\beta_2` of the indices of the atoms in such a way that
`\beta_2\circ\sccode_0=\sccode_2'`.  The partition `\Pcal_\Ucal`, the action
`R_\Ucal` and substitution `\beta_2:\A_2\to\A_0` are given below

.. link

::

    sage: assert P2_scaled.is_equal_up_to_relabeling(PU)
    sage: beta2 = Substitution2d.from_permutation(PU.keys_permutation(P2_scaled))

Thus `\Xcal_{\Pcal_2,R_2} =\beta_2\left(\Xcal_{\Pcal_\Ucal,R_\Ucal}\right)`.
We may check that `\beta_0\circ\beta_1\circ\beta_2=\phi`

.. link

::

    sage: from slabbe import Substitution2d
    sage: Phi = Substitution2d({0: [[17]], 1: [[16]], 2: [[15], [11]],
    ....: 3: [[13], [9]], 4: [[17], [8]], 5: [[16], [8]], 6: [[15], [8]],
    ....: 7: [[14], [8]], 8: [[14, 6]], 9: [[17, 3]], 10: [[16, 3]],
    ....: 11: [[14, 2]], 12: [[15, 7], [11, 1]], 13: [[14, 6], [11, 1]],
    ....: 14: [[13, 7], [9, 1]], 15: [[12, 6], [9, 1]], 16: [[18, 5], [10, 1]],
    ....: 17: [[13, 4], [9, 1]], 18: [[14, 2], [8, 0]]})
    sage: beta0 * beta1 * beta2 == Phi
    True

We conclude that

.. MATH::

    \begin{align*}
        \Xcal_{\Pcal_\Ucal,R_\Ucal}
        &= \overline{\beta_0(\Xcal_{\Pcal_1,R_1})}^\sigma
        = \overline{\beta_0\beta_1(\Xcal_{\Pcal_2,R_2})}^\sigma
        = \overline{\beta_0\beta_1\beta_2\left(\Xcal_{\Pcal_\Ucal,R_\Ucal}\right)}^\sigma
        = \overline{\phi\left(\Xcal_{\Pcal_\Ucal,R_\Ucal}\right)}^\sigma.
    \end{align*}

Using SageMath, verify that the equalities `\beta_0=\alpha_0`,
`\beta_1=\alpha_1` and `\beta_2=\alpha_2` hold

.. link

::

    sage: beta0 == alpha0
    True
    sage: beta1 == alpha1
    True
    sage: beta2 == alpha2
    True

