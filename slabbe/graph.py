# -*- coding: utf-8 -*-
r"""
Functions on graphs

.. TODO::

    - Make the doctests more simple
"""
#*****************************************************************************
#       Copyright (C) 2016-2017 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from __future__ import absolute_import, print_function
from collections import Counter, defaultdict
import itertools
from sage.graphs.digraph import DiGraph
from sage.graphs.graph import Graph
from sage.misc.cachefunc import cached_function

def projection_graph(G, proj_fn, filename=None, verbose=False):
    r"""
    Return the image of a graph under a function on vertices.

    INPUT:

    - ``G`` -- graph
    - ``proj_fn`` -- function
    - ``filename`` -- integer (default:``None``), save the graph to this pdf
      filename if filename is not None
    - ``verbose`` -- bool (default:``False``), print a table of data about the
      projection

    EXAMPLES::

        sage: from slabbe.graph import projection_graph
        sage: g = graphs.PetersenGraph()
        sage: g.vertices(sort=True)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        sage: f = lambda i: i % 5
        sage: projection_graph(g, f)
        Looped multi-digraph on 5 vertices

    With verbose information::

        sage: projection_graph(g, lambda i:i%4, verbose=True)
          Number of vertices   Projected vertices
        ├────────────────────┼────────────────────┤
          2                    3
          2                    2
          3                    1
          3                    0
        Looped multi-digraph on 4 vertices
    """
    edges = set((proj_fn(A),proj_fn(B)) for A,B,_ in G.edges(sort=False))
    G_proj = DiGraph(edges, format='list_of_edges', loops=True, multiedges=True)
    if verbose:
        d = dict(Counter(proj_fn(s) for s in G.vertices(sort=False)))
        rows = [(value, key) for key,value in d.items()]
        rows.sort(reverse=True,key=lambda row:row[1])
        header_row = ['Number of vertices', 'Projected vertices']
        from sage.misc.table import table
        print(table(rows=rows, header_row=header_row))
    if filename:
        from slabbe import TikzPicture
        print(TikzPicture.from_graph(G_proj, prog='dot').pdf(filename))
    return G_proj

def digraph_move_label_to_edge(G, label_function=None, loops=True,
        multiedges=False):
    r"""
    Return a digraph with labels moved from the arrival vertices to
    corresponding edges.

    INPUT:

    - ``G`` -- graph, whose vertices are tuples of the form (vertex, label)
    - ``label_function`` -- function or None, a function to apply to each label
    - ``loops`` -- bool (default: True)
    - ``multiedges`` -- bool (default: False)

    EXAMPLES::

        sage: G = DiGraph()
        sage: G.add_edges([((i, None), ((i+1)%10, 'plusone')) for i in range(10)])
        sage: G.add_edges([((i, None), ((i+2)%10, 'plustwo')) for i in range(10)])
        sage: G
        Digraph on 30 vertices
        sage: from slabbe.graph import digraph_move_label_to_edge
        sage: digraph_move_label_to_edge(G)
        Looped digraph on 10 vertices

    Using a function to modify the labels::

        sage: f = lambda label:"A"+label
        sage: GG = digraph_move_label_to_edge(G, label_function=f)
        sage: GG
        Looped digraph on 10 vertices
        sage: GG.edges(sort=True)[0]
        (0, 1, 'Aplusone')
    """
    if label_function:
        edges = [(u,v,label_function(label)) for ((u,_), (v,label), _) in G.edges(sort=False)]
    else:
        edges = [(u,v,label) for ((u,_), (v,label), _) in G.edges(sort=False)]
    return DiGraph(edges, format='list_of_edges', loops=loops,
            multiedges=multiedges)

def induced_subgraph(G, filter):
    r"""
    Return the induced subdigraph of a digraph keeping only vertices that are
    map to ``True`` by the filter.

    INPUT:

    - ``G`` -- graph
    - ``filter`` -- function, a function from vertices to boolean

    EXAMPLES::

        sage: from slabbe.graph import induced_subgraph
        sage: G = DiGraph()
        sage: G.add_edges([((i, ''), ((i+1)%10, 'plusone')) for i in range(10)])
        sage: G.add_edges([((i, ''), ((i+2)%10, 'plustwo')) for i in range(10)])
        sage: GG = induced_subgraph(G, lambda v: v[0]%2 == 0)
        sage: G
        Digraph on 30 vertices
        sage: GG
        Digraph on 15 vertices
        sage: GG.edges(sort=True)[0]
        ((0, ''), (2, 'plustwo'), None)

    .. TODO::

        simplify the edges aaaaa*aaa*aaa* to a* only
    """
    GG = G.copy()
    loops = dict((u, label) for (u,v,label) in GG.loop_edges())
    for v in GG.vertices(sort=False):
        if filter(v):
            continue
        incoming = [(x,y,l) for (x,y,l) in GG.incoming_edges(v) if x != y]
        outgoing = [(x,y,l) for (x,y,l) in GG.outgoing_edges(v) if x != y]
        GG.delete_vertex(v)
        if v in loops:
            it = itertools.product(outgoing, [(loops[v][0]*10,)], incoming) 
        else:
            it = itertools.product(outgoing, [tuple()], incoming) 
        for c,b,a in it:
            _,y,labelout = c
            x,_,labelin = a
            GG.add_edge(x,y, labelout + b + labelin)
    return GG

def merge_multiedges(G, label_function=tuple):
    r"""
    Return the (di)graph where multiedges are merged into one.

    INPUT:

    - ``G`` -- graph
    - ``label_function`` -- function (default:``tuple``), a function to
      apply to each list of labels

    OUTPUT:

        (looped) (di)graph

    EXAMPLES:

    A digraph::

        sage: from slabbe.graph import merge_multiedges
        sage: G = DiGraph(multiedges=True)
        sage: G.add_edge(0,1,'one')
        sage: G.add_edge(0,1,'two')
        sage: G.add_edge(0,1,'alpha')
        sage: GG = merge_multiedges(G)
        sage: GG
        Digraph on 2 vertices
        sage: GG.edges(sort=True)
        [(0, 1, ('alpha', 'one', 'two'))]

    A graph::

        sage: G = Graph(multiedges=True)
        sage: G.add_edge(0,1,'one')
        sage: G.add_edge(0,1,'two')
        sage: G.add_edge(0,1,'alpha')
        sage: GG = merge_multiedges(G)
        sage: GG
        Graph on 2 vertices
        sage: GG.edges(sort=True)
        [(0, 1, ('alpha', 'one', 'two'))]

    Using ``label_function``::

        sage: fn = lambda L: LatexExpr(','.join(map(str, L)))
        sage: GG = merge_multiedges(G, label_function=fn)
        sage: GG.edges(sort=True)
        [(0, 1, alpha,one,two)]

    """
    d = defaultdict(list)
    for (u,v,label) in G.edges(sort=True):
        d[(u,v)].append(label)

    edges = [(u,v,label_function(label_list)) for (u,v),label_list in d.items()]

    loops = G.has_loops()
    if G.is_directed():
        return DiGraph(edges, format='list_of_edges', loops=loops)
    else:
        return Graph(edges, format='list_of_edges', loops=loops)

def clean_sources_and_sinks(G):
    r"""
    Return a copy of the graph where every vertices of the graph that have
    in or out degree 0 is removed (recursively).

    EXAMPLES::

        sage: from slabbe.graph import clean_sources_and_sinks
        sage: L = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,3)]
        sage: G = DiGraph(L,format='list_of_edges')
        sage: H = clean_sources_and_sinks(G)
        sage: H
        Digraph on 3 vertices
        sage: H.vertices(sort=True)
        [3, 4, 5]

    ::

        sage: L = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,3),(1,0)]
        sage: G = DiGraph(L, format='list_of_edges')
        sage: H = clean_sources_and_sinks(G)
        sage: H
        Digraph on 6 vertices
        sage: H.vertices(sort=True)
        [0, 1, 2, 3, 4, 5]

    """
    H = G.copy()
    done = False
    while not done:
        done = True
        for v in H.vertices(sort=False):
            if H.in_degree(v) == 0 or H.out_degree(v) == 0:
                done = False
                H.delete_vertex(v)
    return H

def get_funnel(G):
    r"""
    Return an edge (u,v) such that u and v are distinct, G.out_degree(u) is
    1 and G.in_degree(v) is 1. Return ``None`` if no such funnel is found.

    INPUT:

    - ``G`` -- digraph

    EXAMPLES::

        sage: from slabbe.graph import get_funnel
        sage: G = DiGraph([(str(a),str(a+1)) for a in range(5)], format='list_of_edges')
        sage: get_funnel(G)
        ('0', '1')
    """
    for (u,v,_) in G.edges(sort=True): 
        if (u != v and G.in_degree(v) == 1 and G.out_degree(u) == 1):
            return (u,v)
    else:
        return None

def reduce_funnel_edges(G, merge_function):
    r"""
    Reduce a graph by merging all funnel edge.

    We say that an edge (u,v) is a "funnel" edge if u is not v
    and the out degree of u and the in degree of v are both equal to 1.

    INPUT:

    - ``G`` -- digraph
    - ``merge_function`` -- function taking two vertices as input and
      returning a new vertex

    EXAMPLES::

        sage: from slabbe.graph import reduce_funnel_edges
        sage: G = DiGraph([(str(a),str(a+1)) for a in range(5)], format='list_of_edges')
        sage: merge_function = lambda a,b:a+b
        sage: GG = reduce_funnel_edges(G, merge_function)
        sage: GG.vertices(sort=True)
        ['012345']

    ::

        sage: G = DiGraph([(str(a),str((a+1)%5)) for a in range(5)], format='list_of_edges')
        sage: merge_function = lambda a,b:a+b
        sage: GG = reduce_funnel_edges(G, merge_function)
        sage: GG.vertices(sort=True)
        ['01234']

    The following result does not seem right::

        sage: w = words.FibonacciWord()[:100]
        sage: G = w.rauzy_graph(11)
        sage: merge_function = lambda a,b:a+b[-1:]
        sage: GG = reduce_funnel_edges(G, merge_function)
        sage: GG.vertices(sort=True)
        [word: 01001010010, word: 100101001001, word: 100101001011]

    """
    from copy import copy
    GG = copy(G)
    GG.allow_loops(True)
    #GG.allow_multiple_edges(True)

    funnel = get_funnel(GG)
    while funnel:
        (u,v) = funnel
        u_v = merge_function(u, v)
        GG.add_vertex(u_v)
        for s in GG.neighbors_out(v):
            GG.add_edge(u_v, s)
        for s in GG.neighbors_in(u):
            GG.add_edge(s, u_v)
        GG.delete_vertex(u)
        GG.delete_vertex(v)
        funnel = get_funnel(GG)
    return GG

def get_left_special_vertex(G):
    r"""
    Return a vertex v such that v is left special but not bispecial, that is,
    ``G.in_degree(v)>1`` but ``G.out_degree(v)<=1``.

    Return ``None`` if no such vertex is found.

    INPUT:

    - ``G`` -- digraph

    OUTPUT:

    a vertex or ``None`` if no such vertex is found.

    EXAMPLES::

        sage: from slabbe.graph import get_left_special_vertex
        sage: G = DiGraph([(5,6), (6,7), (6,8)], format='list_of_edges')
        sage: get_left_special_vertex(G) is None
        True
        sage: G = DiGraph([(6,5), (7,6), (8,6)], format='list_of_edges')
        sage: get_left_special_vertex(G)
        6

    If there is a bispecial, but no left special it returns ``None``::

        sage: G = DiGraph([(2,3),(3,4),(4,2),(2,5),(5,6),(6,2)], format='list_of_edges')
        sage: get_left_special_vertex(G) is None
        True

    """
    for v in G.vertices(sort=True):
        if G.in_degree(v) > 1 and G.out_degree(v) <= 1:
            return v
    else:
        return None

def get_right_special_vertex(G):
    r"""
    Return a vertex v such that v is right special but not bispecial, that is,
    ``G.in_degree(v)<=1`` but ``G.out_degree(v)>1``.

    Return ``None`` if no such vertex is found.

    INPUT:

    - ``G`` -- digraph

    OUTPUT:

    a vertex or ``None`` if no such vertex is found.

    EXAMPLES::

        sage: from slabbe.graph import get_right_special_vertex
        sage: G = DiGraph([(5,6), (6,7), (6,8)], format='list_of_edges')
        sage: get_right_special_vertex(G)
        6
        sage: G = DiGraph([(6,5), (7,6), (8,6)], format='list_of_edges')
        sage: get_right_special_vertex(G) is None
        True

    """
    for v in G.vertices(sort=True):
        if G.in_degree(v) <= 1 and G.out_degree(v) > 1:
            return v
    else:
        return None

def get_bispecial_vertex(G):
    r"""
    Return a vertex v such that v is bispecial, that is,
    ``G.in_degree(v)>1`` but ``G.out_degree(v)>1``.

    Return ``None`` if no such vertex is found.

    INPUT:

    - ``G`` -- digraph

    OUTPUT:

    a vertex or ``None`` if no such vertex is found.

    EXAMPLES::

        sage: from slabbe.graph import get_bispecial_vertex
        sage: G = DiGraph([(4,6), (5,6), (6,7), (6,8)], format='list_of_edges')
        sage: get_bispecial_vertex(G)
        6
        sage: G = DiGraph([(6,5), (7,6), (8,6)], format='list_of_edges')
        sage: get_bispecial_vertex(G) is None
        True

    """
    for v in G.vertices(sort=True):
        if G.in_degree(v) > 1 and G.out_degree(v) > 1:
            return v
    else:
        return None

def bispecial_vertices(G):
    r"""
    Return the list of vertices v such that v is bispecial, that is,
    ``G.in_degree(v)>1`` but ``G.out_degree(v)>1``.

    INPUT:

    - ``G`` -- digraph

    EXAMPLES::

        sage: from slabbe.graph import bispecial_vertices
        sage: G = DiGraph([(4,6), (5,6), (6,7), (6,8)], format='list_of_edges')
        sage: bispecial_vertices(G)
        [6]
        sage: G = DiGraph([(6,5), (7,6), (8,6)], format='list_of_edges')
        sage: bispecial_vertices(G)
        []

    """
    return [v for v in G.vertices(sort=False) if G.in_degree(v) > 1 and G.out_degree(v) > 1]

def reduce_left_special_vertices(G, merge_function):
    r"""
    Merge all left special vertices with its in-neighbor(s) ``u`` using
    ``merge_function(u,v)`` to create the new vertex.

    INPUT:

    - ``G`` -- digraph
    - ``merge_function`` -- function taking two vertices as input and
      returning a new vertex

    OUTPUT:

    a digraph

    EXAMPLES::

        sage: from slabbe.graph import reduce_left_special_vertices
        sage: edges = [(0,1),(1,2),(2,3),(3,4),(4,0),(2,5),(5,6),(6,7),(7,0)]
        sage: edges = [(str(u),str(v)) for (u,v) in edges]
        sage: G = DiGraph(edges, format='list_of_edges')
        sage: merge_function = lambda u,v:u+v
        sage: GG = reduce_left_special_vertices(G, merge_function)
        sage: sorted((a,b) for (a,b,_) in GG.edges(sort=False))
        [('2', '3'),
         ('2', '5'),
         ('3', '401'),
         ('401', '2'),
         ('5', '6'),
         ('6', '701'),
         ('701', '2')]

    It is idempotent::

        sage: GGG = reduce_left_special_vertices(GG, merge_function)
        sage: GGG == GG
        True

    """
    from copy import copy
    GG = copy(G)
    GG.allow_loops(True)
    #GG.allow_multiple_edges(True)

    v = get_left_special_vertex(GG)
    while v is not None:
        for u in GG.neighbors_in(v):
            u_v = merge_function(u, v)
            GG.add_edges((s, u_v) for s in GG.neighbors_in(u))
            if GG.out_degree(u) == 1:
                GG.delete_vertex(u)
            GG.add_edges((u_v, t) for t in GG.neighbors_out(v))
        GG.delete_vertex(v)
        v = get_left_special_vertex(GG)
    return GG

def reduce_right_special_vertices(G, merge_function):
    r"""
    Merge all right special vertices with its in-neighbor(s) ``u`` using
    ``merge_function(u,v)`` to create the new vertex.

    INPUT:

    - ``G`` -- digraph
    - ``merge_function`` -- function taking two vertices as input and
      returning a new vertex

    OUTPUT:

    a digraph

    EXAMPLES::

        sage: from slabbe.graph import reduce_right_special_vertices
        sage: edges = [(0,1),(1,2),(2,3),(3,4),(4,0),(2,5),(5,6),(6,7),(7,0)]
        sage: edges = [(str(u),str(v)) for (u,v) in edges]
        sage: G = DiGraph(edges, format='list_of_edges')
        sage: merge_function = lambda u,v:u+v
        sage: GG = reduce_right_special_vertices(G, merge_function)
        sage: sorted((a,b) for (a,b,_) in GG.edges(sort=False))
        [('0', '123'),
         ('0', '125'),
         ('123', '4'),
         ('125', '6'),
         ('4', '0'),
         ('6', '7'),
         ('7', '0')]

    It is idempotent::

        sage: GGG = reduce_right_special_vertices(GG, merge_function)
        sage: GGG == GG
        True

    """
    from copy import copy
    GG = copy(G)
    GG.allow_loops(True)
    #GG.allow_multiple_edges(True)

    v = get_right_special_vertex(GG)
    while v is not None:
        for w in GG.neighbors_out(v):
            v_w = merge_function(v, w)
            GG.add_edges((v_w, s) for s in GG.neighbors_out(w))
            if GG.in_degree(w) == 1:
                GG.delete_vertex(w)
            GG.add_edges((t, v_w) for t in GG.neighbors_in(v))
        GG.delete_vertex(v)
        v = get_right_special_vertex(GG)
    return GG

def reduce_bispecial_vertices(G, merge_function, filter=None):
    r"""
    Merge all bispecial vertices with its in-neighbor(s) ``u`` using
    ``merge_function(u,v)`` to create the new vertex. Only edges such that
    ``filter(u,v)`` is True are kept.

    INPUT:

    - ``G`` -- digraph
    - ``merge_function`` -- function taking two vertices as input and
      returning a new vertex
    - ``filter`` -- function from pair of vertices to boolean (default:``None``),
      Only creates edges ``(u,v)`` such that ``filter(u,v) is True`` are kept.
      If ``None``, then ``filter = lambda a,b:True`` is used.

    OUTPUT:

    a digraph

    EXAMPLES::

        sage: from slabbe.graph import reduce_left_special_vertices
        sage: from slabbe.graph import reduce_bispecial_vertices
        sage: edges = [(0,1),(1,2),(2,3),(3,4),(4,0),(2,5),(5,6),(6,7),(7,0)]
        sage: edges = [(str(u),str(v)) for (u,v) in edges]
        sage: G = DiGraph(edges, format='list_of_edges')
        sage: merge_function = lambda u,v:u+v
        sage: GG = reduce_left_special_vertices(G, merge_function)
        sage: GGG = reduce_bispecial_vertices(GG, merge_function)
        sage: sorted((a,b) for (a,b,_) in GGG.edges(sort=False))
        [('3', '4012'),
         ('4012', '3'),
         ('4012', '5'),
         ('5', '6'),
         ('6', '7012'),
         ('7012', '3'),
         ('7012', '5')]

    It is idempotent::

        sage: GGGG = reduce_bispecial_vertices(GGG, merge_function)
        sage: GGGG == GGG
        True

    """
    from copy import copy
    GG = copy(G)
    GG.allow_loops(True)
    #GG.allow_multiple_edges(True)

    if filter is None:
        filter = lambda a,b:True

    GG_bispecials = bispecial_vertices(GG)
    for v in GG_bispecials:
        if v not in GG:
            # v was deleted earlier in the process
            continue
        for u in GG.neighbors_in(v):
            u_v = merge_function(u, v)
            GG.add_edges((s, u_v) for s in GG.neighbors_in(u))
            if GG.out_degree(u) == 1:
                GG.delete_vertex(u)
            GG.add_edges((u_v, t) for t in GG.neighbors_out(v) if filter(u_v,t))
        GG.delete_vertex(v)
    return GG

def vertices_in_a_cycle(G, verbose=False):
    r"""
    Return the set of vertices belonging to a cycle.

    INPUT:

    - ``G`` -- digraph
    - ``verbose`` -- bool (default:``False``)

    OUTPUT:

    list or set of vertices

    EXAMPLES::

        sage: from slabbe.graph import vertices_in_a_cycle
        sage: G = DiGraph()
        sage: G.add_vertex(0)
        sage: vertices_in_a_cycle(G)
        []
        sage: vertices_in_a_cycle(G, verbose=True)
        ignoring vertex 0 because it has no loop
        []

    ::

        sage: G = DiGraph(loops=True)
        sage: G.add_edge(0, 0)
        sage: vertices_in_a_cycle(G)
        [0]

    ::

        sage: D = DiGraph({0:[1, 3], 1:[2], 2:[0,3], 4:[5, 6], 5:[6]})
        sage: D.strongly_connected_components()
        [[3], [0, 1, 2], [6], [5], [4]]
        sage: vertices_in_a_cycle(D)
        [0, 1, 2]

    """
    V = []
    for c in G.strongly_connected_components():
        if len(c) > 1:
            V.extend(c)
        elif len(c) == 1:
            v, = c
            if G.has_edge(v,v):
                V.append(v)
            else:
                if verbose:
                    print("ignoring vertex {} because "
                          "it has no loop".format(v))
        else:
            continue
    return V

@cached_function
def digraphs_with_n_edges(n_edges, connected=None):
    r"""
    Return the list of directed multigraphs with loops with n
    edges with no sink nor sources up to graph isomorphisms.

    This is an initial naive straight-forward implementation.
    Something more clever needs to be done to handle 6 edges or more.

    INPUT:

    - ``n_edges`` -- integer
    - ``connected`` -- bool (defaut: ``None``), if ``True``, returns only
      those that are connected.

    EXAMPLES::

        sage: from slabbe.graph import digraphs_with_n_edges
        sage: digraphs_with_n_edges(1)
        [Looped multi-digraph on 1 vertex]
        sage: digraphs_with_n_edges(2)
        [Looped multi-digraph on 1 vertex,
         Looped multi-digraph on 2 vertices,
         Looped multi-digraph on 2 vertices]
        sage: digraphs_with_n_edges(3)
        [Looped multi-digraph on 1 vertex,
         Looped multi-digraph on 2 vertices,
         Looped multi-digraph on 2 vertices,
         Looped multi-digraph on 2 vertices,
         Looped multi-digraph on 3 vertices,
         Looped multi-digraph on 3 vertices,
         Looped multi-digraph on 2 vertices,
         Looped multi-digraph on 3 vertices]

    ::

        sage: [g.edges(labels=False) for g in digraphs_with_n_edges(3)]
        [[(0, 0), (0, 0), (0, 0)],
         [(0, 0), (0, 0), (1, 1)],
         [(0, 0), (0, 1), (1, 0)],
         [(0, 0), (0, 1), (1, 1)],
         [(0, 0), (1, 1), (2, 2)],
         [(0, 0), (1, 2), (2, 1)],
         [(0, 1), (0, 1), (1, 0)],
         [(0, 1), (1, 2), (2, 0)]]

    ::

        sage: len(digraphs_with_n_edges(4)) # long time (10s)
        29
        sage: len(digraphs_with_n_edges(5)) # not tested (1h)
        110
        sage: len(digraphs_with_n_edges(6)) # not tested (6d 18h 48min 21s)
        509

    .. NOTE::

        List [1,3,8,29,110,509] does not exist in OEIS but is almost related to
        https://oeis.org/A350907 "Number of unlabeled initially connected
        digraphs with n arcs."

    Those that are connected::

        sage: [len(digraphs_with_n_edges(i, connected=True)) for i in range(1,6)] # not tested (<1h)
        [1, 2, 5, 18, 71]
        sage: [len(digraphs_with_n_edges(i, connected=True)) for i in range(1,7)] # not tested (<7days)
        [1, 2, 5, 18, 71, 344]

    .. TODO::

        Do something more clever using nauty graph generator
        ``for g in digraphs(nvertices, size=n, copy=True)`` and use
        ``IntegerVectorsModPermutationGroup`` to generate admissible
        multiplicities for edges and loops, using the automorphism group of
        the graph::

            sage: I = IntegerVectorsModPermutationGroup(PermutationGroup([[(1,2,3)]]), sum=6)
            sage: I.cardinality()
            10
            sage: I.list()
            [[6, 0, 0], [5, 1, 0], [5, 0, 1], [4, 2, 0], [4, 1, 1],
             [4, 0, 2], [3, 3, 0], [3, 2, 1], [3, 1, 2], [2, 2, 2]]

        Also one may use `integer_lists_mod_perm_group` in the Vincent package
        `adm_cycles` which is better than the one in Sage. See:
        https://gitlab.com/modulispaces/admcycles/-/blob/master/admcycles/integer_list.py?ref_type=heads

    """
    from sage.graphs.digraph import DiGraph

    def has_sink(G):
        return any(d== 0 for d in G.out_degree_iterator())
    def has_source(G):
        return any(d== 0 for d in G.in_degree_iterator())

    L = []

    nvertices = 2 * n_edges
    V = list(range(nvertices))
    VV = list(itertools.product(V, repeat=2))
    for edges in itertools.combinations_with_replacement(VV, n_edges):
        g = DiGraph(edges, format='list_of_edges', loops=True, multiedges=True)
        if has_sink(g) or has_source(g):
            continue
        if any(g.is_isomorphic(h) for h in L):
            continue

        if connected is None or g.is_connected() == connected:
            L.append(g)

    return L

def minimal_perfect_matching(vertices, cost=None, solver=None, verbose=False):
    r"""
    Return a perfect matching of points minimizing the sum of the cost of all pairs.

    INPUT:

    - ``vertices`` -- list of vertices
    - ``cost`` -- function (vertices x vertices -> R) or ``None``. If
      ``None``, it computes the Euclidean distance between points.
    - ``solver`` -- string (default:``None``), name of a MILP solver,
      default is ``default_mip_solver()``
    - ``verbose`` -- bool (default:``False``)

    OUTPUT:

    list of pairs of vertices

    EXAMPLES::

        sage: from slabbe.graph import minimal_perfect_matching
        sage: minimal_perfect_matching([(0,0), (10,0), (0,1), (10,1)])
        [((0, 0), (0, 1)), ((10, 0), (10, 1))]

    """
    if cost is None:
        from sage.modules.free_module_element import vector
        cost = lambda u,v: (vector(v)-vector(u)).norm().n()

    edges = list(itertools.combinations(vertices, 2))
    cost_dict = {(u,v):cost(u,v) for (u,v) in edges}

    from sage.numerical.mip import MixedIntegerLinearProgram
    p = MixedIntegerLinearProgram(solver=solver)
    matching = p.new_variable(binary=True)
    p.set_objective(-p.sum(cost_dict[e]*matching[e] for e in edges))
    for v in vertices:
        p.add_constraint(p.sum(matching[(x,y)] for (x,y) in edges if y == v) 
                        +p.sum(matching[(x,y)] for (x,y) in edges if x == v) == 1)
    if verbose:
        p.show()

    p.solve()
    matching = p.get_values(matching, convert=bool, tolerance=1e-3)
    return sorted(e for (e, b) in matching.items() if b)

def eulerian_paths(G):
    r"""
    Return a sequence of paths covering all edges of the graph exactly
    once.

    INPUT:

    - ``G`` -- undirected graph

    ALGORITHM:

    Euler's Theorem says that (https://en.wikipedia.org/wiki/Eulerian_path):

        A connected graph has an Euler cycle if and only if every vertex has
        even degree.

    Therefore, we may construct a partition of the edges of any graph into
    a union of k paths where k is equal to the number of odd degree
    vertices divided by 2. The idea is to add an additional dummy vertex
    and link every odd degree vertex to it and solve for the Eulerian
    circuit in that even degree graph.

    EXAMPLES:

    The following graph has two vertices of odd degree. Thus, it
    has no Eulerian circuit, but it has an Eulerian path::

        sage: G = Graph([(0,1), (1,2), (0,3), (3,2), (0,4), (4,2)])
        sage: G
        Graph on 5 vertices
        sage: G.degree()
        [3, 2, 3, 2, 2]
        sage: G.eulerian_circuit()
        False
        sage: G.eulerian_circuit(path=True)
        [(2, 4, None),
         (4, 0, None),
         (0, 3, None),
         (3, 2, None),
         (2, 1, None),
         (1, 0, None)]
        sage: from slabbe.graph import eulerian_paths
        sage: eulerian_paths(G)
        [[2, 4, 0, 3, 2, 1, 0]]

    The following has four odd degree vertices. Thus, it has
    no Eulerian circuit nor Eulerian paths. But we can cover all the edges
    with two paths::

        sage: G = Graph([(0,1), (1,2), (0,3), (3,2), (0,4), (4,2), (1,4)])
        sage: G.eulerian_circuit()
        False
        sage: G.eulerian_circuit(path=True)
        False
        sage: eulerian_paths(G)
        [[1, 0], [4, 2, 3, 0, 4, 1, 2]]

    Works if G is already Eulerian::

        sage: G = Graph([(0,1), (1,2), (2,3), (3,4), (4,0)])
        sage: eulerian_paths(G)
        [[0, 4, 3, 2, 1, 0]]

    """
    if G.is_eulerian():
        edge_seq,vertex_seq = G.eulerian_circuit(labels=False, return_vertices=True)
        return [vertex_seq]

    G_copy = G.copy()
    odd_degree_vertices = [v for (v,d) in G_copy.degree_iterator(labels=True) if d % 2 == 1]

    # construct a dummy vertex which is not already a vertex of the graph
    dummy_vertex = -1
    while dummy_vertex in G_copy:
        dummy_vertex = (dummy_vertex,)
    assert dummy_vertex not in G_copy

    G_copy.add_edges((v,dummy_vertex) for v in odd_degree_vertices)
    assert G_copy.is_eulerian(), "this graph should be Eulerian, i.e., degree sequence should be all even: {}".format(G_copy.degree())

    edge_sequence,L = G_copy.eulerian_circuit(labels=False, return_vertices=True)

    assert L[0] == L[-1]
    del L[0]

    # find the first position of the dummy vertex in the circuit
    first_dummy = 0
    while L[first_dummy] != dummy_vertex:
        first_dummy += 1
    assert L[first_dummy] == dummy_vertex

    # rotate the circuit
    L = L[first_dummy:] + L[:first_dummy]
    L.append(L[0])

    starts = [i for (i,v) in enumerate(L) if v == dummy_vertex]
    assert starts[0] == 0
    
    paths = [L[starts[i]:starts[i+1]] for i in range(len(starts)-1)]
    return [path[1:] for path in paths]

def minimal_eulerian_paths(G, cost=None):
    r"""
    Return a sequence of paths covering all edges of the graph exactly
    once and minimizing the distance between the end and start of the next
    path.

    INPUT:

    - ``G`` -- undirected graph
    - ``cost`` -- function (vertices x vertices -> R) or ``None``. If
      ``None``, it computes the Euclidean distance between points.

    ALGORITHM:

    Euler's Theorem says that (https://en.wikipedia.org/wiki/Eulerian_path):

        A connected graph has an Euler cycle if and only if every vertex has
        even degree.

    We add edges between vertices of odd degree (a matching of minimal
    Euclidean distance). We compute a Euler cycle. We decompose the cycle.

    EXAMPLES:

    The following graph has two vertices of odd degree. Thus, it
    has no Eulerian circuit, but it has an Eulerian path::

        sage: G = Graph([(0,1), (1,2), (0,3), (3,2), (0,4), (4,2)])
        sage: G
        Graph on 5 vertices
        sage: G.degree()
        [3, 2, 3, 2, 2]
        sage: G.eulerian_circuit()
        False
        sage: G.eulerian_circuit(path=True)
        [(2, 4, None),
         (4, 0, None),
         (0, 3, None),
         (3, 2, None),
         (2, 1, None),
         (1, 0, None)]
        sage: from slabbe.graph import minimal_eulerian_paths
        sage: cost = lambda u,v : abs(v-u)
        sage: minimal_eulerian_paths(G, cost)
        [[(2, 1), (1, 0), (0, 4), (4, 2), (2, 3), (3, 0)]]

    The following has four odd degree vertices. Thus, it has
    no Eulerian circuit nor Eulerian paths. But we can cover all the edges
    with two paths::

        sage: G = Graph([(0,1), (1,2), (0,3), (3,2), (0,4), (4,2), (1,4)])
        sage: G.eulerian_circuit()
        False
        sage: G.eulerian_circuit(path=True)
        False
        sage: cost = lambda u,v : abs(v-u)
        sage: minimal_eulerian_paths(G, cost)       # known bug
        [[(4, 2), (2, 3), (3, 0), (0, 4), (4, 1), (1, 2)], [(1, 0)]]

    TODO:

    - the matchings should not be part of the edges of the graph!!

    """
    G_copy = G.copy()
    odd_degree_vertices = [v for (v,d) in G_copy.degree_iterator(labels=True) if d % 2 == 1]

    assert len(odd_degree_vertices) % 2 == 0, "there should be an even # of odd degree vertices"
    # we add the edges of a minimal perfect matching between odd degree
    # vertices
    matching = minimal_perfect_matching(odd_degree_vertices, cost=cost)
    #print(matching)

    # ignore edges of the matching which are already in the graph
    matching_to_add = [(a,b) for (a,b) in matching if not G_copy.has_edge(a,b)]

    G_copy.add_edges(matching_to_add)

    assert G_copy.is_eulerian(), "this graph should be Eulerian, i.e., degree sequence should be all even: {}".format(G_copy.degree())

    L = G_copy.eulerian_circuit(labels=False)

    paths = []
    path = []
    for edge in L:
        if edge in matching_to_add or (edge[1], edge[0]) in matching_to_add:
            paths.append(path)
            path = []
        else:
            path.append(edge)
    else:
        # insert the last path found at the beginning of the first
        paths[0][0:0] = path

    return paths


def has_claw_decomposition(G, certificate=False):
    r"""
    Return whether a graph has a claw decomposition.

    This is an answer to the question posted at
    https://ask.sagemath.org/question/81610/test-if-a-graph-has-a-claw-decomposition/

    INPUT:

    - ``G`` -- undirected graph
    - ``certificate`` -- boolean

    OUTPUT:

    a boolean or 2-tuple (boolean, solution) if certificate is True

    EXAMPLES::

        sage: from slabbe.graph import has_claw_decomposition
        sage: G1 = Graph( [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3),
        ....: (1, 5), (2, 3), (2, 4), (3, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 8),
        ....: (6, 10), (7, 9), (7, 11), (8, 9), (8, 10), (9, 11), (10, 11)])
        sage: has_claw_decomposition(G1)
        False
        sage: has_claw_decomposition(G1, certificate=True)
        (False, None)

    ::

        sage: G2 = Graph([(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4),
        ....:    (1, 5), (2, 4), (2, 5), (3, 5), (4, 5)])
        sage: has_claw_decomposition(G2)
        True
        sage: has_claw_decomposition(G2, certificate=True)     # random
        (True,
         [[(0, 1), (1, 2), (1, 5)],
          [(0, 3), (1, 3), (3, 5)],
          [(0, 2), (2, 4), (2, 5)],
          [(0, 4), (1, 4), (4, 5)]])

    """
    import itertools
    from sage.combinat.matrices.dancing_links import dlx_solver

    id_to_edge = [frozenset(edge) for edge in G.edges(labels=False)]
    edge_to_id = {edge:i for (i,edge) in enumerate(id_to_edge)}

    rows = []
    for u in G:
        u_neighbors = G.neighbors(u)
        for three_neighbors in itertools.combinations(u_neighbors, 3):
            L = [edge_to_id[frozenset((u,v))] for v in three_neighbors]
            L.sort()
            rows.append(L)
    d = dlx_solver(rows)

    solution = d.one_solution()
    has_solution = not solution is None

    if not certificate:
        return has_solution
    else:
        if has_solution:
            solution_vertices = [[tuple(id_to_edge[id]) for id in rows[row_number]]
                                 for row_number in solution]
            return (has_solution, solution_vertices)
        else:
            return (has_solution, solution)


def has_graph_decomposition(self, G, induced=False, certificate=False):
    r"""
    Return whether a graph has a decomposition into isometric copies of
    another graph.

    This is an answer to the question posted at
    https://ask.sagemath.org/question/81610/test-if-a-graph-has-a-claw-decomposition/

    INPUT:

    - ``self`` -- undirected graph
    - ``G`` -- undirected graph
    - ``induced`` -- boolean (default: ``False``); whether or not to
      consider only the induced copies of ``G`` in ``self``
    - ``certificate`` -- boolean

    OUTPUT:

    A boolean or 2-tuple ``(boolean, solution)`` if certificate is ``True``

    In the latter case, ``solution`` is a list of lists of edges.

    EXAMPLES::

        sage: from slabbe.graph import has_graph_decomposition
        sage: G1 = Graph( [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3),
        ....: (1, 5), (2, 3), (2, 4), (3, 5), (4, 6), (4, 7), (5, 6), (5, 7), (6, 8),
        ....: (6, 10), (7, 9), (7, 11), (8, 9), (8, 10), (9, 11), (10, 11)])
        sage: claw = graphs.ClawGraph()
        sage: has_graph_decomposition(G1, claw)
        False
        sage: has_graph_decomposition(G1, claw, certificate=True)
        (False, None)

    ::

        sage: G2 = Graph([(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4),
        ....:    (1, 5), (2, 4), (2, 5), (3, 5), (4, 5)])
        sage: has_graph_decomposition(G2, claw)
        True
        sage: has_graph_decomposition(G2, claw, certificate=True)     # random
        (True,
         [[(0, 1), (1, 2), (1, 3)],
          [(0, 2), (0, 3), (0, 4)],
          [(1, 4), (2, 4), (4, 5)],
          [(1, 5), (2, 5), (3, 5)]])

    """
    from sage.combinat.matrices.dancing_links import dlx_solver

    id_to_edge = [frozenset(edge) for edge in self.edges(labels=False)]
    edge_to_id = {edge:i for (i,edge) in enumerate(id_to_edge)}

    rows = []
    for g in self.subgraph_search_iterator(G, induced=induced, return_graphs=True):
        g_edges = g.edges(labels=False)
        L = [edge_to_id[frozenset(edge)] for edge in g_edges]
        L.sort()
        rows.append(L)
    d = dlx_solver(rows)

    solution = d.one_solution()
    has_solution = not solution is None

    if not certificate:
        return has_solution
    else:
        if has_solution:
            solution_edges = [[tuple(id_to_edge[id]) for id in rows[row_number]]
                                 for row_number in solution]
            return (has_solution, solution_edges)
        else:
            return (has_solution, solution)


