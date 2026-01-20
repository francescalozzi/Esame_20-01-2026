import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            n_alb = int(self._view.txtNumAlbumMin.value)
            if n_alb <= 0:
                raise ValueError
        except:
            self._view.create_alert('inserire un valore valido')
            return

        try:
            n_nodes, n_edges = self._model.build_graph(n_alb)
        except Exception as ex:
            self._view.create_alert('errore costruzione grafo {ex}')
            return

        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.btnSearchArtists.disabled = False


        artisti = self._model.get_graph_artist()
        artisti.sort(key = lambda a: a.id)

        self._view.ddArtist.options = [ft.dropdown.Option(key= str(a.id), text= str(a)) for a in artisti]

        self._view.ddArtist.value = None

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'Grafo creato: {n_nodes} artisit, {n_edges} archi'))
        self._view.update_page()


    def handle_connected_artists(self, e):
        if self._view.ddArtist.value is None:
            self._view.create_alert('selezionare un artista')
            return

        a1_id = int(self._view.ddArtist.value)
        a1 = self._model.get_artists_by_id(a1_id)

        if a1 is None:
            self._view.create_alert('artista non valido')
            return

        connessi = self._model.get_componente_connessa(a1)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f'artisti direttamente collegati a {a1}: '))

        if len(connessi) == 0:
            self._view.txt_result.controls.append(ft.Text(f'nessun artista collegato a questo artista {a1}'))
        else:
            for a2,w in connessi:
                self._view.txt_result.controls.append(ft.Text(f'{a2}- numero di generi in comune: {w}'))


    def handle_search_path(self, e):
        if self._view.ddArtist.value is None:
            self._view.create_alert('selezioni un artista')
            return

        try:
            start_id = int(self._view.ddArtist.value)
        except:
            self._view.create_alert('artista non valido')
            return


        start_artist = self._model.get_artists_by_id(start_id)
        if start_artist is None:
            self._view.create_alert('artista di partenza non trovato')


        try:
            d_min = float(self._view.txtMinDuration.value)
            if d_min < 0:
                raise ValueError
        except:
            self._view.create_alert('inserire una durata valida in minuti')
            return

        # n_art è il numero di nodi nel cammino

        try:
            n_art = int(self._view.txtMaxArtists.value)
            if n_art <= 0:
                raise ValueError

        except:
            self._view.create_alert('inserire un valore valido')
            return

        max_nodes = len(self._model.get_graph_artist())
        if n_art > max_nodes:
            self._view.create_alert('valore troppo grande: grandezza massima {max_nodes}')
            return

        try:
            path,w = self._model.search_path(start_artist, d_min, n_art)
        except Exception as e:
            self._view.create_alert(f'Errore nella ricerca del cammino {e}')
            return

        self._view.txt_result.controls.clear()

        if not path:
            self._view.txt_result.controls.append(ft.Text('nessun cammino valido è stato trovato'))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(f'cammino di massimo peso trovato per {start_artist}'))
        self._view.txt_result.controls.append(ft.Text(f'cammino di lunghezza {len(path)}'))
        for a in path:
            self._view.txt_result.controls.append(ft.Text(str(a)))


        self._view.txt_result.controls.append(ft.Text(f'peso massimo trovato {w}'))

        self._view.update_page()

