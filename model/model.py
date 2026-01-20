import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self._id_map= {}

        self._best_path = []
        self._best_weight = 0

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        return DAO.get_artists_with_min_albums(min_albums)

    def build_graph(self,n_alb:int):
        self._graph.clear()

        vertici = DAO.get_artists_with_min_albums(n_alb)
        for a in vertici:
            self._id_map[a.id] = a

        self._graph.add_nodes_from(vertici)

        edges = DAO.get_edges_common_genres(n_alb)

        for id1,id2,w in edges:
            a1 = self._id_map[id1]
            a2 = self._id_map[id2]
            self._graph.add_edge(a1,a2, weight=w)


        return self._graph.number_of_nodes(), self._graph.number_of_edges()


    def get_graph_artist(self):
        return list(self._graph.nodes())

    def get_artists_by_id(self, id):
        return self._id_map.get(id)


    def get_componente_connessa(self,a1):
        risultato = []

        for vicino in self._graph.neighbors(a1):
            w = self._graph[a1][vicino]['weight']
            risultato.append((vicino,w))

        risultato = sorted(risultato, key=lambda x: int(x[0]))
        return risultato


    def search_path(self,start_artist, dmin_minutes, n_art):
        self._best_path = []
        self._best_weight = 0

        dmin = int(dmin_minutes * 60 * 1000)

        #considero solo gli artisti che hanno alemno una track lunga >= dmin
        id_corretti = DAO.get_artists_with_track_min_duration(dmin)

        #prendo solo i nod presenti nel grafo
        nodi_concessi = {a for a in self._graph.nodes if a.id in id_corretti}

        #start deve essere ammesso

        if start_artist not in nodi_concessi:
            return [], 0

        self._ricorsione(current = start_artist, path = [start_artist], weight = 0,
                         nodi_concessi = nodi_concessi, lunghezza_arrivo = n_art)

        return self._best_path, self._best_weight


    def _ricorsione(self, current, path, weight,nodi_concessi, lunghezza_arrivo):
        #se si è raggiunta la lunghezza richiesta

        if len(path) == lunghezza_arrivo:
            if weight > self._best_weight:
                self._best_weight = weight
                self._best_path = list(path)


        for vicino in self._graph.neighbors(current):
            if vicino in nodi_concessi and vicino not in path:
                w = self._graph[current][vicino]['weight']
                self._ricorsione(current = vicino,
                                 path = path + [vicino],
                                 weight = weight + w,
                                 nodi_concessi = nodi_concessi,
                                 lunghezza_arrivo = lunghezza_arrivo)


