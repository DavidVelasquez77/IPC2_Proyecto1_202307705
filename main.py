from ListaCircular import ListaCircular
import xml.etree.ElementTree as ET
from xml.dom import minidom
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import pyfiglet
import time
from Nodo import Nodo
from rich import print
from colorama import init
import graphviz

# Inicializar colorama
init(autoreset=True)

# Clases personalizadas para reemplazar estructuras nativas
class Par:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Mapa:
    def __init__(self):
        self._items = []

    def agregar(self, clave, valor):
        self._items.append((clave, valor))

    def obtener(self, clave, valor_default=None):
        for k, v in self._items:
            if k == clave:
                return v
        return valor_default

    def contiene(self, clave):
        for k, v in self._items:
            if k == clave:
                return True
        return False

    def items(self):
        return self._items


class Lista:
    def __init__(self):
        self._items = []

    def agregar(self, item):
        self._items.append(item)

    def obtener(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def items(self):
        return self._items

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
            self.console.print("✨ Has seleccionado la Opción 1: Cargando el archivo...")
            ruta = input("Ingresar la ruta del archivo: ")
            self.cargar_archivo(ruta)
        elif opcion == 2:
            self.console.print("✨ Has seleccionado la Opción 2: Procesando el archivo...")
            self.procesar_archivo()  # Procesar el archivo y manejar la lista circular
        elif opcion == 3:
            self.console.print("✨ Has seleccionado la Opción 3: Escribiendo el archivo de salida...")
            self.escribir_archivo_salida()  # Escribir archivo de salida
        elif opcion == 4:
            self.console.print("✨ Has seleccionado la Opción 4: Mostrando datos del estudiante...")            
            self.mostrar_datos_estudiante()  # Mostrar datos del estudiante
        elif opcion == 5:
            self.console.print("✨ Has seleccionado la Opción 5: Generando gráfica...")
            self.generar_grafica()  # Llama a la función para generar la gráfica

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

        try:
            root = ET.fromstring(self.archivo_contenido)
        except ET.ParseError:
            self.console.print("[red]Error al procesar el archivo XML. Asegúrate de que el archivo sea válido.[/red]")
            return

        for matriz_element in root.findall('matriz'):
            nombre = matriz_element.get('nombre')
            n = int(matriz_element.get('n'))
            m = int(matriz_element.get('m'))
            datos = Mapa()

            for dato_element in matriz_element.findall('dato'):
                x = int(dato_element.get('x'))
                y = int(dato_element.get('y'))
                valor = int(dato_element.text)
                datos.agregar(Par(x, y), valor)

            self.lista_matrices.agregar(nombre, n, m, datos)
            self.console.print(f"[green]Matriz '{nombre}' añadida a la lista circular.[/green]")

            self.console.print("[yellow]Calculando la matriz binaria...[/yellow]")
            datos_binarios = self.convertir_a_binario(datos)
            nombre_binario = f"{nombre}_Binario"
            self.lista_matrices.agregar(nombre_binario, n, m, datos_binarios)
            self.console.print("[yellow]Realizando suma de tuplas...[/yellow]")

            # Mostrar las matrices
            self.mostrar_matriz(nombre, datos)
            self.mostrar_matriz(nombre_binario, datos_binarios)
            self.console.print("[green]Matriz binaria generada.[/green]")

    def convertir_a_binario(self, datos):
        datos_binarios = Mapa()
        for par, valor in datos.items():
            valor_binario = 1 if valor > 0 else 0
            datos_binarios.agregar(par, valor_binario)
        return datos_binarios
    
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
            title="[magenta]Datos del Estudiante[/magenta]",
            border_style="cyan"
        )
        
        # Mostrar el panel en la consola
        self.console.print(panel)

    def escribir_archivo_salida(self):
        if self.lista_matrices.primero is None:
            self.console.print("[red]No hay matrices procesadas para escribir en el archivo de salida.[/red]")
            return

        root = ET.Element("matrices")
        actual = self.lista_matrices.primero

        while True:
            if actual.nombre.endswith('_Binario'):
                matriz_original = self.lista_matrices.buscar(actual.nombre.replace('_Binario', ''))
                patrones = Mapa()

                for i in range(1, actual.n + 1):
                    # Construir el patrón de acceso como una tupla
                    patron = tuple(actual.obtener_dato(i, j) for j in range(1, actual.m + 1))
                    
                    if not patrones.contiene(patron):
                        patrones.agregar(patron, [i])
                    else:
                        patrones.obtener(patron).append(i)

                matriz_reducida = Mapa()
                for patron, filas in patrones.items():
                    nueva_fila = len(matriz_reducida.items()) + 1
                    matriz_reducida.agregar(nueva_fila, [0] * actual.m)
                    
                    for fila in filas:
                        for j in range(1, actual.m + 1):
                            matriz_reducida.obtener(nueva_fila)[j - 1] += matriz_original.obtener_dato(fila, j)

                # Agregar la matriz reducida al XML
                matriz_element = ET.SubElement(
                    root,
                    "matriz",
                    nombre=f"{matriz_original.nombre}_Salida",
                    n=str(len(matriz_reducida.items())),
                    m=str(actual.m),
                    g=str(len(patrones.items()))
                )

                for i, fila_datos in matriz_reducida.items():
                    for j, valor in enumerate(fila_datos, start=1):
                        dato_element = ET.SubElement(matriz_element, "dato", x=str(i), y=str(j))
                        dato_element.text = str(valor)
                
                # Agregar las frecuencias al XML
                for g, filas in patrones.items():
                    frecuencia_element = ET.SubElement(matriz_element, "frecuencia", g=str(len(filas)))
                    frecuencia_element.text = str(len(filas))      
                    
            actual = actual.siguiente
            if actual == self.lista_matrices.primero:
                break

        xml_str = ET.tostring(root, encoding="utf-8")
        pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

        with open("archivo_salida.xml", "w", encoding="utf-8") as archivo_salida:
            archivo_salida.write(pretty_xml_str)

        self.console.print("[green]Archivo de salida escrito exitosamente como 'archivo_salida.xml'.[/green]")

    def mostrar_matriz(self, nombre, datos):
        self.console.print(f"[yellow]Matriz '{nombre}':[/yellow]")
        if not datos:
            self.console.print("[red]No hay datos para mostrar en la matriz.[/red]")
            return

        # Determinar el rango de filas y columnas
        max_x = max(par.x for par, valor in datos.items())
        max_y = max(par.y for par, valor in datos.items())

        # Crear una tabla para mostrar la matriz
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Columna", style="cyan", justify="center")
        for j in range(1, max_y + 1):
            table.add_column(str(j), style="cyan", justify="center")

        for i in range(1, max_x + 1):
            row = [str(i)]
            for j in range(1, max_y + 1):
                row.append(str(datos.obtener(Par(i, j), 0)))
            table.add_row(*row)

        self.console.print(table)

    def generar_grafica(self):
        matriz = self.lista_matrices.primero
        matriz_binaria = self.lista_matrices.buscar(f'{matriz.nombre}_Binario')

        # Crear el grafo para la matriz original
        dot = graphviz.Digraph(comment=f'Matriz {matriz.nombre}')
        for par, valor in matriz.datos.items():
            dot.node(f'{par.x},{par.y}', f'{valor}')
            if par.x < matriz.n:
                dot.edge(f'{par.x},{par.y}', f'{par.x+1},{par.y}')
            if par.y < matriz.m:
                dot.edge(f'{par.x},{par.y}', f'{par.x},{par.y+1}')

        # Renderizar el grafo de la matriz original
        dot.render(f'{matriz.nombre}.gv', format='png', cleanup=True)

        # Crear el grafo para la matriz binaria
        dot_binario = graphviz.Digraph(comment=f'Matriz {matriz_binaria.nombre}')
        for par, valor in matriz_binaria.datos.items():
            dot_binario.node(f'{par.x},{par.y}', f'{valor}')
            if par.x < matriz_binaria.n:
                dot_binario.edge(f'{par.x},{par.y}', f'{par.x+1},{par.y}')
            if par.y < matriz_binaria.m:
                dot_binario.edge(f'{par.x},{par.y}', f'{par.x},{par.y+1}')

        # Renderizar el grafo de la matriz binaria
        dot_binario.render(f'{matriz_binaria.nombre}.gv', format='png', cleanup=True)

# Main loop para ejecutar el menú
if __name__ == "__main__":
    menu = Menu()
    menu.mostrar_titulo()
    
    while True:
        menu.mostrar_menu()
        try:
            opcion = int(input("Selecciona una opción: "))
            menu.ejecutar_opcion(opcion)
            if opcion == 6:
                break
        except ValueError:
            print("[red]⚠️ Por favor, ingresa un número válido.[/red]")
