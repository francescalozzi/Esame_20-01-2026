import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):

        self._page = page
        self._page.title = "Programmazione Avanzata - Primo Appello - iTunes"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None

        # Alert
        self.alert = AlertManager(page)

        self.txtNumAlbumMin = None
        self.ddArtist = None
        self.btnArtistsConnected = None
        self.txtMaxConnections = None
        self.txtMinDuration = None
        self.btnSearchArtists = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Gestione Artisti e Generi", color="blue", size=24)
        self._page.controls.append(self._title)

        #row1
        self.txtNumAlbumMin = ft.TextField( label="Numero album minimo", width=250)
        self._btnCreateGraph = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.handle_create_graph )
        row1 = ft.Row([self.txtNumAlbumMin, self._btnCreateGraph],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        #row2
        self.ddArtist = ft.Dropdown(label="Artista", width = 250, disabled=True)
        self.btnArtistsConnected = ft.ElevatedButton(text="Artisti collegati", width = 150, disabled=True, on_click=self._controller.handle_connected_artists )
        row2 = ft.Row([self.ddArtist, self.btnArtistsConnected],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        #row3
        self.txtMaxArtists = ft.TextField( label="Numero massimo artisti", width=300, disabled=True)
        self.txtMinDuration = ft.TextField( label="Durata minima (minuti)", width=250, disabled=True)
        self.btnSearchArtists = ft.ElevatedButton(text="Cerca cammino da artista", disabled=True, on_click = self._controller.handle_search_path)
        row3 = ft.Row([self.txtMinDuration, self.txtMaxArtists, self.btnSearchArtists],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # txt_result
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.open(dlg)
        self._page.update()

    def update_page(self):
        self._page.update()