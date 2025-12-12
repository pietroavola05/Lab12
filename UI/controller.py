import flet as ft
import networkx as nx
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model._grafo.number_of_nodes()} nodi, {self._model._grafo.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            self._soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if self._soglia < min_p or self._soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(self._soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {self._soglia}: {minori}, Archi > {self._soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""

    def handle_percorso_minimo(self, e):
        """Callback per il pulsante 'Percorso Minimo'."""

        if not self._model._grafo or nx.number_of_nodes(self._model._grafo) == 0:
            self._view.show_alert("Prima crea il grafico.")
            return

        if self._soglia is None:
            self._view.show_alert("Inserisci e calcola prima una soglia valida (pulsante 'Conta Archi').")
            return

        costo_minimo, percorso_minimo = self._model.ricerca_cammino_minimo(self._soglia)
        self._view.lista_visualizzazione_3.controls.clear()

        if percorso_minimo:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"Cammino minimo:"))

            for i in range(len(percorso_minimo) - 1):
                rifugio1 = percorso_minimo[i]
                rifugio2 = percorso_minimo[i + 1]

                peso = self._model._grafo.get_edge_data(rifugio1, rifugio2)['weight']

                testo_arco = f"[{rifugio1.id}] {rifugio1.nome} --> [{rifugio2.id}] {rifugio2.nome} [peso: {peso:.2f}]"
                self._view.lista_visualizzazione_3.controls.append(ft.Text(testo_arco))

            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"\nCosto Totale: {costo_minimo:.2f}"))

        else:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text("Nessun cammino valido (almeno 2 archi, peso > soglia) trovato."))

        self._view.page.update()


