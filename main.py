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
from utils import NodoLista
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
            self.console.print("[yellow]Realizando suma de patrones...[/yellow]")

            # Mostrar las matrices
            self.mostrar_matriz(nombre, datos)
            self.mostrar_matriz(nombre_binario, datos_binarios)
            self.console.print("[green]Matriz binaria generada.[/green]")


   
    def convertir_a_binario(self, mapa):
        datos_binarios = Mapa()
        nodo_actual = mapa.items().inicio

        while nodo_actual:
            clave = nodo_actual.valor.clave  # Accede al objeto `Par` que es la clave
            valor = nodo_actual.valor.valor  # Accede al valor asociado
            valor_binario = 1 if valor > 0 else 0  # Convertir el valor a binario (1 o 0)
            datos_binarios.agregar(clave, valor_binario)  # Agregar al nuevo Mapa de datos binarios
            nodo_actual = nodo_actual.siguiente

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

                for i in range(1, actual.n + 1):
                    patron = Lista()
                    for j in range(1, actual.m + 1):
                        valor = actual.obtener_dato(i, j)
                        patron.agregar(Par(j, valor))

                    patron_existente = False
                    for k in range(1, patrones.tamano() + 1):
                        clave = Par(k, None)  # Usa Par como clave
                        patron_info = patrones.obtener(clave)
                        if patron_info is not None and patron_info.tamano() >= 2:
                            filas_grupo = patron_info.obtener(1)
                            if filas_grupo is not None and filas_grupo.tamano() >= 1:
                                if self.comparar_patrones(patron_info.obtener(0), patron):
                                    filas_grupo.agregar(i)
                                    patron_existente = True
                                    break

                    if not patron_existente:
                        filas_grupo = Lista()
                        filas_grupo.agregar(i)
                        nuevo_patron = Lista()
                        nuevo_patron.agregar(patron)
                        nuevo_patron.agregar(filas_grupo)
                        patrones.agregar(Par(patrones.tamano(), None), nuevo_patron)  # Usa Par como clave

                matriz_reducida = Mapa()
                for k in range(1, patrones.tamano() + 1):
                    clave = Par(k, None)  # Usa Par como clave
                    patron_info = patrones.obtener(clave)
                    if patron_info is not None:
                        filas_grupo = patron_info.obtener(1)
                        fila_datos = Lista()
                        for j in range(1, actual.m + 1):
                            suma = 0
                            for idx in range(1, filas_grupo.tamano() + 1):
                                fila = filas_grupo.obtener(idx - 1)  # Ajustado índice
                                suma += matriz_original.obtener_dato(fila, j)
                            fila_datos.agregar(suma)
                        matriz_reducida.agregar(Par(k - 1, None), fila_datos)  # Usa Par como clave

                matriz_element = ET.SubElement(
                    root,
                    "matriz",
                    nombre=f"{matriz_original.nombre}_Salida",
                    n=str(matriz_reducida.tamano()),
                    m=str(actual.m),
                    g=str(patrones.tamano())
                )

                for i in range(1, matriz_reducida.tamano() + 1):
                    fila_datos = matriz_reducida.obtener(Par(i - 1, None))  # Usa Par como clave
                    for j in range(1, fila_datos.tamano() + 1):
                        valor = fila_datos.obtener(j - 1)  # Ajustado índice
                        dato_element = ET.SubElement(matriz_element, "dato", x=str(i), y=str(j))
                        dato_element.text = str(valor)

                for k in range(1, patrones.tamano() + 1):
                    patron_info = patrones.obtener(Par(k, None))  # Usa Par como clave
                    if patron_info is not None:
                        filas_grupo = patron_info.obtener(1)
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
        
        tamano1 = patron1.tamano()
        tamano2 = patron2.tamano()
        
        if tamano1 != tamano2:
            return False
        
        for i in range(tamano1):
            if patron1.obtener(i) != patron2.obtener(i):
                return False
        
        return True


    def mostrar_matriz(self, nombre, datos):
        self.console.print(f"[yellow]Matriz '{nombre}':[/yellow]")

        if datos.tamano() == 0:
            self.console.print("[red]No hay datos para mostrar en la matriz.[/red]")
            return

        # Determinar las dimensiones de la matriz
        max_x = 0
        max_y = 0
        nodo_datos = datos.items().inicio

        while nodo_datos:
            clave_valor_nodo = nodo_datos.valor  # Obtén el objeto NodoMapa
            par = clave_valor_nodo.clave  # Accede a la clave (un objeto Par)
            valor = clave_valor_nodo.valor  # Accede al valor asociado
            if par.x > max_x:
                max_x = par.x
            if par.y > max_y:
                max_y = par.y
            nodo_datos = nodo_datos.siguiente

        self.console.print(f"Dimensiones: {max_x}x{max_y}")

        # Crear la tabla para mostrar los datos
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Fila", style="cyan", justify="center")

        # Agregar columnas para la tabla
        j = 1
        while j <= max_y:
            table.add_column(str(j), style="cyan", justify="center")
            j += 1

        # Rellenar la tabla con los datos de la matriz
        i = 1
        while i <= max_x:
            row_datos = []
            j = 1
            while j <= max_y:
                valor = datos.obtener(Par(i, j), 0)
                row_datos.append(str(valor))
                j += 1

            table.add_row(str(i), *row_datos)
            i += 1

        self.console.print(table)

    def generar_grafica(self):
        # Obtener la matriz original y la matriz binaria
        matriz = self.lista_matrices.primero
        matriz_binaria = self.lista_matrices.buscar(f'{matriz.nombre}_Binario')

        # Crear el grafo para la matriz original
        dot = graphviz.Digraph(comment=f'Matriz {matriz.nombre}')
        nodo_datos = matriz.datos.items().inicio

        while nodo_datos:
            # Extraer la clave y el valor desde el nodo de la lista
            clave_valor = nodo_datos.valor
            par = clave_valor.clave
            valor = clave_valor.valor
            dot.node(f'{par.x},{par.y}', f'{valor}')
            if par.x < matriz.n:
                dot.edge(f'{par.x},{par.y}', f'{par.x+1},{par.y}')
            if par.y < matriz.m:
                dot.edge(f'{par.x},{par.y}', f'{par.x},{par.y+1}')
            nodo_datos = nodo_datos.siguiente

        # Renderizar el grafo de la matriz original
        dot.render(f'{matriz.nombre}.gv', format='png', cleanup=True)

        # Crear el grafo para la matriz binaria
        dot_binario = graphviz.Digraph(comment=f'Matriz {matriz_binaria.nombre}')
        nodo_datos_binario = matriz_binaria.datos.items().inicio

        while nodo_datos_binario:
            # Extraer la clave y el valor desde el nodo de la lista
            clave_valor_binario = nodo_datos_binario.valor
            par_binario = clave_valor_binario.clave
            valor_binario = clave_valor_binario.valor
            dot_binario.node(f'{par_binario.x},{par_binario.y}', f'{valor_binario}')
            if par_binario.x < matriz_binaria.n:
                dot_binario.edge(f'{par_binario.x},{par_binario.y}', f'{par_binario.x+1},{par_binario.y}')
            if par_binario.y < matriz_binaria.m:
                dot_binario.edge(f'{par_binario.x},{par_binario.y}', f'{par_binario.x},{par_binario.y+1}')
            nodo_datos_binario = nodo_datos_binario.siguiente

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
