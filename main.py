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
from utils import Par 
from utils import Mapa
from utils import Lista
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
        for item in datos.items():  # Assuming items() returns a Lista of Par objects
            par = item  # `item` is already a Par object
            valor = datos.obtener(par)  # Get the value associated with this Par object
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
        [0]
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

                # Procesar cada fila de la matriz binaria
                for i in range(1, actual.n + 1):
                    patron = Lista()
                    for j in range(1, actual.m + 1):
                        valor = actual.obtener_dato(i, j)
                        patron.agregar(Par(j, valor))

                    # Verificar si el patrón ya existe
                    patron_existente = False
                    for k in range(1, patrones.tamano() + 1):
                        patron_guardado = patrones.obtener(Par(k, None))
                        if patron_guardado is not None and self.comparar_patrones(patron_guardado.obtener(Par(1, None)), patron):
                            filas_grupo = patron_guardado.obtener(Par(2, None))
                            filas_grupo.agregar(i)
                            patron_existente = True
                            break

                    if not patron_existente:
                        # Si el patrón no existe, crear un nuevo grupo para este patrón
                        filas_grupo = Lista()
                        filas_grupo.agregar(i)
                        nuevo_patron = Lista()
                        nuevo_patron.agregar(patron)
                        nuevo_patron.agregar(filas_grupo)
                        patrones.agregar(Par(patrones.tamano() + 1, nuevo_patron))

                matriz_reducida = Mapa()
                for k in range(1, patrones.tamano() + 1):
                    patron_info = patrones.obtener(Par(k, None))
                    if patron_info is not None:
                        filas_grupo = patron_info.obtener(Par(2, None))
                        fila_datos = Lista()
                        for j in range(1, actual.m + 1):
                            suma = 0
                            for idx in range(1, filas_grupo.tamano() + 1):
                                fila = filas_grupo.obtener(Par(idx, None))
                                suma += matriz_original.obtener_dato(fila, j)
                            fila_datos.agregar(suma)
                        matriz_reducida.agregar(Par(k, fila_datos))

                matriz_element = ET.SubElement(
                    root,
                    "matriz",
                    nombre=f"{matriz_original.nombre}_Salida",
                    n=str(matriz_reducida.tamano()),
                    m=str(actual.m),
                    g=str(patrones.tamano())
                )

                for i in range(1, matriz_reducida.tamano() + 1):
                    fila_datos = matriz_reducida.obtener(Par(i, None))
                    for j in range(1, fila_datos.tamano() + 1):
                        valor = fila_datos.obtener(Par(j, None))
                        dato_element = ET.SubElement(matriz_element, "dato", x=str(i), y=str(j))
                        dato_element.text = str(valor)

                for k in range(1, patrones.tamano() + 1):
                    patron_info = patrones.obtener(Par(k, None))
                    if patron_info is not None:
                        filas_grupo = patron_info.obtener(Par(2, None))
                        frecuencia_element = ET.SubElement(matriz_element, "frecuencia", g=str(k))
                        frecuencia_element.text = str(filas_grupo.tamano())

            actual = actual.siguiente
            if actual == self.lista_matrices.primero:
                break

        xml_str = ET.tostring(root, encoding="utf-8")
        pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

        with open("archivo_salida.xml", "w", encoding="utf-8") as archivo_salida:
            archivo_salida.write(pretty_xml_str)

        self.console.print("[green]Archivo de salida escrito exitosamente como 'archivo_salida.xml'.[/green]")


    def comparar_patrones(self, patron1, patron2):
        if patron1 is None or patron2 is None:
            return False
        if patron1.tamano() != patron2.tamano():
            return False
        for i in range(1, patron1.tamano() + 1):
            if patron1.obtener(Par(i, None)) != patron2.obtener(Par(i, None)):
                return False
        return True





    def mostrar_matriz(self, nombre, datos):
        self.console.print(f"[yellow]Matriz '{nombre}':[/yellow]")
        if datos.tamano() == 0:
            self.console.print("[red]No hay datos para mostrar en la matriz.[/red]")
            return

        max_x = max(par.x for par, valor in datos.items())
        max_y = max(par.y for par, valor in datos.items())

        self.console.print(f"Dimensiones: {max_x}x{max_y}")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Columna", style="cyan", justify="center")
        for j in range(1, max_y + 1):
            table.add_column(str(j), style="cyan", justify="center")

        for i in range(1, max_x + 1):
            row = [str(i)]
            for j in range(1, max_y + 1):
                valor = datos.obtener(Par(i, j), 0)
                self.console.print(f"Valor en {i},{j}: {valor}")
                row.append(str(valor))
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
