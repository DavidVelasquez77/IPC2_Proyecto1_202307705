from prettytable import PrettyTable, ALL
from colorama import init
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time
from xml.etree import ElementTree as ET
from xml.dom import minidom
from Nodo import Nodo
from ListaCircular import ListaCircular

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

            # Agregar la matriz original a la lista circular
            self.lista_matrices.agregar(nombre, n, m, datos)
            self.console.print(f"[green]Matriz '{nombre}' añadida a la lista circular.[/green]")

            # Crear la matriz reducida basada en los valores de la matriz original
            datos_reducidos = {}
            for i in range(1, n + 1, 2):  # Agrupando de dos en dos filas
                nuevo_x = (i + 1) // 2  # Nuevo índice de fila en la matriz reducida
                for j in range(1, m + 1):
                    valor1 = datos.get((i, j), 0)
                    valor2 = datos.get((i + 1, j), 0) if i + 1 <= n else 0
                    datos_reducidos[(nuevo_x, j)] = valor1 + valor2

            nombre_reducido = f"{nombre}_Salida"
            self.lista_matrices.agregar(nombre_reducido, (n + 1) // 2, m, datos_reducidos)
            self.console.print(f"[green]Matriz reducida '{nombre_reducido}' generada y añadida a la lista circular.[/green]")

        # Mostrar todas las matrices (opcional)
        self.lista_matrices.mostrar_todas()

    def escribir_archivo_salida(self):
        if self.lista_matrices.primero is None:
            self.console.print("[red]No hay matrices procesadas para escribir en el archivo de salida.[/red]")
            return

        root = ET.Element("matrices")

        actual = self.lista_matrices.primero
        while True:
            if actual.nombre.endswith('_Binaria'):  # Procesar solo la matriz binaria
                nombre_salida = actual.nombre.replace('_Binaria', '_Salida')
                matriz_reducida = {}  # Almacenará la matriz reducida
                frecuencias = {}  # Almacenará las frecuencias

                # Reducir la matriz agrupando filas de dos en dos y sumando los valores
                for i in range(1, actual.n, 2):  # Saltar de dos en dos
                    for j in range(1, actual.m + 1):
                        valor_1 = actual.obtener_dato(i, j)
                        valor_2 = actual.obtener_dato(i + 1, j) if i + 1 <= actual.n else 0
                        nuevo_valor = valor_1 + valor_2

                        nuevo_x = (i + 1) // 2  # Nuevo índice de fila
                        matriz_reducida[(nuevo_x, j)] = nuevo_valor

                        # Contar la frecuencia de cada valor
                        if nuevo_valor not in frecuencias:
                            frecuencias[nuevo_valor] = 0
                        frecuencias[nuevo_valor] += 1

                # Crear la etiqueta de la matriz en el XML
                matriz_element = ET.SubElement(root, "matriz", nombre=nombre_salida, n="3", m=str(actual.m), g=str(len(frecuencias)))

                # Agregar los datos de la matriz reducida al XML
                for (x, y), valor in matriz_reducida.items():
                    dato_element = ET.SubElement(matriz_element, "dato", x=str(x), y=str(y))
                    dato_element.text = str(valor)

                # Agregar las frecuencias al XML
                for valor, frecuencia in frecuencias.items():
                    frecuencia_element = ET.SubElement(matriz_element, "frecuencia", g=str(valor))
                    frecuencia_element.text = str(frecuencia)

            actual = actual.siguiente
            if actual == self.lista_matrices.primero:
                break

        # Convertir el árbol XML en una cadena con formato bonito
        xml_str = ET.tostring(root, encoding="utf-8")
        pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

        # Escribir el XML a un archivo
        with open("archivo_salida.xml", "w", encoding="utf-8") as archivo_salida:
            archivo_salida.write(pretty_xml_str)

        self.console.print("[green]Archivo de salida escrito exitosamente como 'archivo_salida.xml'.[/green]")

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

    root = ET.Element("matrices")

    actual = self.lista_matrices.primero
    while True:
        if actual.nombre.endswith('_Binaria'):  # Procesar solo la matriz binaria
            nombre_salida = actual.nombre.replace('_Binaria', '_Salida')
            matriz_reducida = {}  # Almacenará la matriz reducida
            frecuencias = {}  # Almacenará las frecuencias

            # Reducir la matriz agrupando filas de dos en dos y sumando los valores
            for i in range(1, actual.n, 2):  # Saltar de dos en dos
                for j in range(1, actual.m + 1):
                    valor_1 = actual.obtener_dato(i, j)
                    valor_2 = actual.obtener_dato(i + 1, j) if i + 1 <= actual.n else 0
                    nuevo_valor = valor_1 + valor_2

                    nuevo_x = (i + 1) // 2  # Nuevo índice de fila
                    matriz_reducida[(nuevo_x, j)] = nuevo_valor

                    # Contar la frecuencia de cada valor
                    if nuevo_valor not in frecuencias:
                        frecuencias[nuevo_valor] = 0
                    frecuencias[nuevo_valor] += 1

            # Crear la etiqueta de la matriz en el XML
            matriz_element = ET.SubElement(root, "matriz", nombre=nombre_salida, n="3", m=str(actual.m), g=str(len(frecuencias)))

            # Agregar los datos de la matriz reducida al XML
            for (x, y), valor in matriz_reducida.items():
                dato_element = ET.SubElement(matriz_element, "dato", x=str(x), y=str(y))
                dato_element.text = str(valor)

            # Agregar las frecuencias al XML
            for valor, frecuencia in frecuencias.items():
                frecuencia_element = ET.SubElement(matriz_element, "frecuencia", g=str(valor))
                frecuencia_element.text = str(frecuencia)

        actual = actual.siguiente
        if actual == self.lista_matrices.primero:
            break

    # Convertir el árbol XML en una cadena con formato bonito
    xml_str = ET.tostring(root, encoding="utf-8")
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

    # Escribir el XML a un archivo
    with open("archivo_salida.xml", "w", encoding="utf-8") as archivo_salida:
        archivo_salida.write(pretty_xml_str)

    self.console.print("[green]Archivo de salida escrito exitosamente como 'archivo_salida.xml'.[/green]")




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