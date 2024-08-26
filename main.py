from prettytable import PrettyTable, ALL
from colorama import init
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time
from xml.etree import ElementTree as ET
from ListaCircular import ListaCircular
from xml.dom import minidom
from Nodo import Nodo

# Inicializar colorama
init(autoreset=True)

class Menu:
    def __init__(self):
        self.console = Console()
        self.archivo_contenido = None
        self.lista_matrices = ListaCircular()  # Inicializa la lista circular para almacenar matrices

    def mostrar_titulo(self):
        ascii_titulo = pyfiglet.figlet_format("PROYECT", font="slant")
        panel = Panel(
            renderable=f"[magenta bold]{ascii_titulo}[/magenta bold]",
            title="✨ Menu Principal ✨",
            title_align="center",
            border_style="cyan",
            padding=(0, 1),
            expand=False
        )
        self.console.print(panel)
        time.sleep(1)

    def mostrar_menu(self):
        table = Table(title="🎯 SELECCIONA UNA OPCIÓN 🎯", title_justify="center", border_style="cyan")
        table.add_column("📌 Opción", style="yellow", justify="center")
        table.add_column("Descripción", style="yellow", justify="left")
        table.add_row("[cyan]1[/cyan]", "[white]🌟 Opción 1: Cargar archivo[/white]")
        table.add_row("[cyan]2[/cyan]", "[white]🌟 Opción 2: Procesar archivo[/white]")
        table.add_row("[cyan]3[/cyan]", "[white]🌟 Opción 3: Escribir archivo salida[/white]")
        table.add_row("[cyan]4[/cyan]", "[white]🌟 Opción 4: Mostrar datos del estudiante[/white]")
        table.add_row("[cyan]5[/cyan]", "[white]🌟 Opción 5: Generar gráfica[/white]")
        table.add_row("[red]6[/red]", "[white]❌ Salir del programa[/white]")
        self.console.print(table)

    def ejecutar_opcion(self, opcion):
        if opcion == 1:
            ruta = input("Ingresar la ruta del archivo: ")
            self.cargar_archivo(ruta)
        elif opcion == 2:
            self.procesar_archivo()  # Procesar el archivo y manejar la lista circular
        elif opcion == 3:
            self.escribir_archivo_salida()  # Escribir archivo de salida
        elif opcion == 4:
            self.mostrar_datos_estudiante()  # Mostrar datos del estudiante
        elif opcion == 5:
            self.console.print("✨ Has seleccionado la Opción 5: Generando gráfica...")
        elif opcion == 6:
            self.console.print("[red]❌ Saliendo del programa... ¡Hasta luego![/red]")
        else:
            self.console.print("[green]⚠️ Opción no válida. Por favor, selecciona una opción del 1 al 6.[/green]")

    def cargar_archivo(self, ruta):
        try:
            with open(ruta, 'r') as archivo:
                self.archivo_contenido = archivo.read()
            self.console.print("[green]Archivo cargado exitosamente.[/green]")
        except FileNotFoundError:
            self.console.print("[red]Archivo no encontrado. Por favor, verifica la ruta.[/red]")

    def procesar_archivo(self):
        if self.archivo_contenido is None:
            self.console.print("[red]No se ha cargado ningún archivo. Por favor, carga un archivo primero.[/red]")
            return

        self.console.print("[yellow]Procesando el archivo XML...[/yellow]")

        # Parsear el contenido XML
        try:
            root = ET.fromstring(self.archivo_contenido)
        except ET.ParseError:
            self.console.print("[red]Error al procesar el archivo XML. Asegúrate de que el archivo sea válido.[/red]")
            return

        # Extraer las matrices del XML
        for matriz_element in root.findall('matriz'):
            nombre = matriz_element.get('nombre')
            n = int(matriz_element.get('n'))
            m = int(matriz_element.get('m'))
            datos = {}

            # Extraer los valores de la matriz
            for dato_element in matriz_element.findall('dato'):
                x = int(dato_element.get('x'))
                y = int(dato_element.get('y'))
                valor = int(dato_element.text)
                datos[(x, y)] = valor

            # Agregar la matriz a la lista circular
            self.lista_matrices.agregar(nombre, n, m, datos)
            self.console.print(f"[green]Matriz '{nombre}' añadida a la lista circular.[/green]")

        # Procesar cada matriz en la lista circular
        actual = self.lista_matrices.primero
        while True:
            self.console.print(f"[cyan]Procesando la matriz '{actual.nombre}'...[/cyan]")
            
            # Identificar el tamaño de la matriz
            self.console.print(f"[magenta]Tamaño de la matriz: {actual.n}x{actual.m}[/magenta]")
        
            # Calcular la matriz binaria
            self.console.print("[yellow]Calculando la matriz binaria...[/yellow]")
            matriz_binaria = {}
            for (x, y), valor in actual.datos.items():
                matriz_binaria[(x, y)] = 1 if valor != 0 else 0
            
            # Mostrar matriz original y matriz binaria
            self.console.print(f"[blue]Matriz Original y Matriz Binaria de '{actual.nombre}':[/blue]")
            for i in range(1, actual.n + 1):
                fila_original = [str(actual.datos.get((i, j), 0)) for j in range(1, actual.m + 1)]
                fila_binaria = [str(matriz_binaria.get((i, j), 0)) for j in range(1, actual.m + 1)]
                self.console.print(" | ".join(fila_original) + "    ||    " + " | ".join(fila_binaria))
            self.console.print()  # Línea en blanco al final de las matrices
            
            # Realizar suma de tuplas
            self.console.print("[yellow]Realizando la suma de las coordenadas de las tuplas...[/yellow]")
            suma_tuplas = sum(x + y for (x, y) in actual.datos.keys())
            self.console.print(f"[green]La suma de las coordenadas de las tuplas en '{actual.nombre}' es: {suma_tuplas}[/green]")
            
            # Avanzar al siguiente nodo
            actual = actual.siguiente
            if actual == self.lista_matrices.primero:
                break

    def mostrar_datos_estudiante(self):
        # Define los datos del estudiante
        nombre = "Josue David Velasquez Ixchop"
        carnet = "202307705"
        curso = "Introduccion a la Programacion y Computacion 2"
        carrera = "Ingenieria en Ciencias y Sistemas"
        semestre = "4to Semestre"
        
        # Crear un panel con los datos del estudiante
        panel = Panel(
            f"[bold yellow]Nombre:[/bold yellow] [white]{nombre}[/white]\n"
            f"[bold yellow]Carnet:[/bold yellow] [white]{carnet}[/white]\n"
            f"[bold yellow]Curso:[/bold yellow] [white]{curso}[/white]\n"
            f"[bold yellow]Carrera:[/bold yellow] [white]{carrera}[/white]\n"
            f"[bold yellow]Semestre:[/bold yellow] [white]{semestre}[/white]",
            title="📚 Datos del Estudiante 📚",
            title_align="center",
            border_style="cyan",
            padding=(1, 2),
            expand=False
        )
        
        self.console.print(panel)

    def escribir_archivo_salida(self):
        if self.lista_matrices.primero is None:
            self.console.print("[red]No hay matrices procesadas para escribir en el archivo de salida.[/red]")
            return

        # Crear el elemento raíz del XML
        root = ET.Element("matrices")

        # Recorrer la lista de matrices procesadas
        actual = self.lista_matrices.primero
        while True:
            matriz_element = ET.SubElement(root, "matriz", nombre=f"{actual.nombre}_Salida", n=str(actual.n), m=str(actual.m), g="3")

            # Agregar los datos de la matriz
            for (x, y), valor in actual.datos.items():
                dato_element = ET.SubElement(matriz_element, "dato", x=str(x), y=str(y))
                dato_element.text = str(valor)

            # Agregar las frecuencias
            frecuencias = {1: 2, 2: 2, 4: 1}  # Ejemplo de frecuencias, ajustar según sea necesario
            for g, freq in frecuencias.items():
                frecuencia_element = ET.SubElement(matriz_element, "frecuencia", g=str(g))
                frecuencia_element.text = str(freq)

            # Avanzar al siguiente nodo
            actual = actual.siguiente
            if actual == self.lista_matrices.primero:
                break

        # Convertir el árbol XML a una cadena y "prettify" el XML
        xml_str = ET.tostring(root, encoding="utf-8")
        parsed_xml = minidom.parseString(xml_str)
        pretty_xml_as_string = parsed_xml.toprettyxml(indent="  ")

        # Escribir el XML formateado en el archivo
        with open("archivo_salida.xml", "w", encoding="utf-8") as archivo_salida:
            archivo_salida.write(pretty_xml_as_string)

        self.console.print("[green]Archivo de salida escrito exitosamente como 'archivo_salida.xml'.[/green]")

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
