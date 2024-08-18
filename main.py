from prettytable import PrettyTable, ALL
from colorama import init
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time

# Inicializar colorama
init(autoreset=True)

class Menu:
    def __init__(self):
        self.console = Console()
        self.archivo_contenido = None

    def mostrar_titulo(self):
        # Crear un título con pyfiglet
        ascii_titulo = pyfiglet.figlet_format("PROYECT", font="slant")  # Cambia "slant" por la fuente que prefieras
        
        # Crear un panel con Rich
        panel = Panel(
            renderable=f"[magenta bold]{ascii_titulo}[/magenta bold]",  # El contenido del panel
            title="✨ Menu Principal ✨", 
            title_align="center",
            border_style="cyan",
            padding=(0, 1),
            expand=False
        )
        self.console.print(panel)
        time.sleep(1)

    def mostrar_menu(self):
        # Crear tabla con Rich
        table = Table(title="🎯 SELECCIONA UNA OPCIÓN 🎯", title_justify="center", border_style="cyan")
        
        table.add_column("📌 Opción", style="yellow", justify="center")
        table.add_column("Descripción", style="yellow", justify="left")
        
        # Añadir filas al menú con colores y emojis
        table.add_row("[cyan]1[/cyan]", "[lightwhite]🌟 Opción 1: Cargar archivo[/lightwhite]")
        table.add_row("[cyan]2[/cyan]", "[lightwhite]🌟 Opción 2: Procesar archivo[/lightwhite]")
        table.add_row("[cyan]3[/cyan]", "[lightwhite]🌟 Opción 3: Escribir archivo salida[/lightwhite]")
        table.add_row("[cyan]4[/cyan]", "[lightwhite]🌟 Opción 4: Mostrar datos del estudiante[/lightwhite]")
        table.add_row("[cyan]5[/cyan]", "[lightwhite]🌟 Opción 5: Generar gráfica[/lightwhite]")
        table.add_row("[red]6[/red]", "[lightwhite]❌ Salir del programa[/lightwhite]")

        # Mostrar el menú
        self.console.print(table)

    def ejecutar_opcion(self, opcion):
        if opcion == 1:
            ruta = input("Ingresar la ruta del archivo: ")
            self.cargar_archivo(ruta)
        else:
            opciones = {
                2: "✨ Has seleccionado la Opción 2: Procesando archivo...",
                3: "✨ Has seleccionado la Opción 3: Escribiendo archivo de salida...",
                4: "✨ Has seleccionado la Opción 4: Mostrando datos del estudiante...",
                5: "✨ Has seleccionado la Opción 5: Generando gráfica...",
                6: "[red]❌ Saliendo del programa... ¡Hasta luego![/red]"
            }
            self.console.print(opciones.get(opcion, "[green]⚠️ Opción no válida. Por favor, selecciona una opción del 1 al 6.[/green]"))

    def cargar_archivo(self, ruta):
        try:
            with open(ruta, 'r') as archivo:
                self.archivo_contenido = archivo.read()
            self.console.print("[green]Archivo cargado exitosamente.[/green]")
        except FileNotFoundError:
            self.console.print("[red]Archivo no encontrado. Por favor, verifica la ruta.[/red]")

    def iniciar(self):
        self.mostrar_titulo()
        while True:
            self.mostrar_menu()
            try:
                opcion = int(input("Selecciona una opción: "))
                self.ejecutar_opcion(opcion)
                if opcion == 6:
                    break
            except ValueError:
                self.console.print("[red]⚠️ Entrada no válida. Por favor, introduce un número.[/red]")

if __name__ == "__main__":
    menu = Menu()
    menu.iniciar()