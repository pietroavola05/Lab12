import networkx as nx
from networkx.algorithms.flow import cost_of_flow

from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self._grafo = nx.Graph()  # grafico, semplice, non diretto ma pesato
        self._lista_rifugi = DAO.ReadRifugi() #sono tutti i rifugi
        # dictionary comprehension
        self._dict_rifugi = {rifugio.id: rifugio for rifugio in self._lista_rifugi}

        self._costo_minimo = float('inf')
        self._sequenza_minima = []
        self._soglia = 0.0  #poi viene inserita dall'utente

        self._connessioni = []
        self._lista_pesi = []
        self._dict_attributi = {}

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """''
        # aggiungo i nodi
        self._grafo.clear()

        self._connessioni = DAO.get_connessioni(year, self._dict_rifugi)
        self._lista_pesi = []

        #aggiungo gli archi
        for c in self._connessioni:
            peso = c.calcola_peso()
            self._lista_pesi.append(peso)
            self._grafo.add_edge(c.id_rifugio1, c.id_rifugio2, weight=peso)

        self._dict_attributi = nx.get_edge_attributes(self._grafo, "weight")


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        minimo = min(self._lista_pesi)
        massimo = max(self._lista_pesi)
        return minimo, massimo

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori = 0
        maggiori = 0

        # questa funzione mi restituisce un dizionario che:
        #chiavi (nodo1, nodo2)
        #valore asociato alla chiave (l'attributo indicato)

        if not self._dict_attributi:
            self._dict_attributi = nx.get_edge_attributes(self._grafo, "weight")
        for peso in self._dict_attributi.values():
            if peso < soglia:
                minori += 1
            else:
                maggiori += 1

        return minori, maggiori



    def ricerca_cammino_minimo(self, soglia):
        shortest_path = nx.all_pairs_shortest_path(self._grafo)
        print(shortest_path)

        #prima di ogni ricerca
        self._soglia = soglia
        self._costo_minimo = float('inf')
        self._sequenza_minima = []

        for nodo in self._grafo.nodes():
            costo_corrente = 0
            sequenza_parziale = [nodo]

            self._ricorsione(nodo, costo_corrente, sequenza_parziale)

        #return al controller
        return self._costo_minimo, self._sequenza_minima


    def _ricorsione(self, nodo_corrente, costo_corrente, sequenza_parziale):

        # se supero già un certo costo non ha senso che continui questo ramo
        if costo_corrente >= self._costo_minimo:
            return

        #aggionamento se condizioni verificate
        if len(sequenza_parziale) >= 3 and costo_corrente < self._costo_minimo:
            self._costo_minimo = costo_corrente
            self._sequenza_minima = list(sequenza_parziale)

        #ciclo
        for vicino in self._grafo.neighbors(nodo_corrente):

            #nodi già presenti nel percorso parziale
            if vicino in sequenza_parziale:
                continue
            # il peso dell'arco e appplico vincolo > soglia
            peso = self._grafo.get_edge_data(nodo_corrente, vicino)['weight']
            if peso > self._soglia:
                nuovo_costo = costo_corrente + peso

                #aggiorno sequenza e richiamo la ricorsione
                sequenza_parziale.append(vicino)
                self._ricorsione(vicino, nuovo_costo, sequenza_parziale)
                # Backtracking
                sequenza_parziale.pop()
        return



    def get_shortest_path_nx(self, soglia):
        #Calcola il percorso minimo in un sottografo  (per test e confronto).
        # questa funzione non viene richiamata formalmente dal model ma può essere usata per fare un confronto con l'altra

        #faccio un copia del grafo così possa togliere gli edges che non servono per il vincolo
        G = self._grafo.copy()

        archi_da_rimuovere = []
        for u, v, att in G.edges(data=True):
            if att['weight'] <= soglia:
                archi_da_rimuovere.append((u, v))

        G.remove_edges_from(archi_da_rimuovere)

        best_costo = float('inf')
        best_path = []

        for source in G.nodes():
            for target in G.nodes():
                if source == target:
                    continue

                try:
                    # l'algoritmo di Dijkstra
                    path = nx.dijkstra_path(G, source, target, weight='weight')
                    path_cost = nx.dijkstra_path_length(G, source, target, weight='weight')

                    # vincolo
                    if len(path) >= 3:
                        if path_cost < best_costo:
                            best_costo = path_cost
                            best_path = path

                except nx.NetworkXNoPath:
                    # è il tipo di eccezione che scaturiste da questa function di nx
                    continue

        return best_costo, best_path

