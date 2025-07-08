r"""

"""
import itertools

class ColoredPointSet:
    def __init__(self, data, dimension):
        r"""
        INPUT:

        - ``data`` -- dictionary of label to list of points
        - ``dimension`` -- integer
        """
        self._data = data
        self._dimension = dimension

    def alphabet(self):
        return self._data.keys()

    def xy_min(self):
        return [min(min(v[i] for v in V) for V in self._data.values()) 
                for i in range(self._dimension)]

    def xy_max(self):
        return [max(max(v[i] for v in V) for V in self._data.values()) 
                for i in range(self._dimension)]

    def plot(self, legend=False):
        A = self.alphabet()
        color_dict = dict(zip(A, rainbow(len(A))))

        G = Graphics()
        for a in sorted(A):
            legend_label = a if legend else None
            G += points(self._data[a], color=color_dict[a], legend_label=legend_label)
        return G

    def plot_as_graphics_array(self, ncols=8):
        A = self.alphabet()
        color_dict = dict(zip(A, rainbow(len(A))))

        xmin,ymin = self.xy_min()
        xmax,ymax = self.xy_max()

        L = []
        for a in sorted(A):
            G = points(self._data[a], color=color_dict[a], legend_label=a, 
                    xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
            L.append(G)
        return graphics_array(L, ncols=ncols)

    def graph_dict(self, epsilon=None, sample_size=30):
        if epsilon is None:
            epsilon = ZZ(20).inverse()
        d = {}
        for (k,V) in self._data.items():
            sample_V = sample(V, sample_size)
            print(k, len(V), len(sample_V))
            near = [(x,y) for (x,y) in itertools.combinations(sample_V, 2) if
                    (vector(y)-vector(x)).norm(oo) < epsilon]
            d[k] = Graph(near, format='list_of_edges')
        return d

    def polyhedron_dict(self, epsilon=None, sample_size=30):
        graph_dict = self.graph_dict(epsilon=epsilon, sample_size=sample_size)
        d = {}
        for (k,G) in graph_dict.items():
            d[k] = [Polyhedron(c) for c in G.connected_components()]
        return d

    def plot_trying_avoiding_overlap(self, ncols=8, epsilon=None, sample_size=40):
        A = self.alphabet()
        polyhedron_dict = self.polyhedron_dict(epsilon=epsilon,
                sample_size=sample_size)
        rows = []
        for (a,b) in itertools.combinations(A, 2):
            Pa = polyhedron_dict[a]
            Pb = polyhedron_dict[b]
            if any(pa.intersection(pb).volume()>0 for pa in Pa for pb in Pb):
                row = [0] * len(A)
                row[a] = 1
                row[b] = -1
                rows.append(row)
        M = matrix(rows)
        return M
