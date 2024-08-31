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
        ascii_titulo = pyfiglet.figlet_format("PROYECTO-1", font="slant")
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

        if root.tag != 'matrices':
            self.console.print("[red]Error: El archivo XML debe comenzar con la etiqueta 'matrices'.[/red]")
            return

        nombres_matrices = set()

        for matriz_element in root.findall('matriz'):
            nombre = matriz_element.get('nombre')
            if nombre in nombres_matrices:
                self.console.print(f"[red]Error: La matriz con nombre '{nombre}' ya existe. Los nombres de matrices deben ser únicos.[/red]")
                continue  # Continua con la siguiente matriz
            
            nombres_matrices.add(nombre)

            try:
                n = int(matriz_element.get('n'))
                m = int(matriz_element.get('m'))
            except (TypeError, ValueError):
                self.console.print(f"[red]Error: Los atributos 'n' y 'm' de la matriz '{nombre}' deben ser enteros válidos.[/red]")
                continue  # Continua con la siguiente matriz

            datos = Mapa()

            for dato_element in matriz_element.findall('dato'):
                try:
                    x = int(dato_element.get('x'))
                    y = int(dato_element.get('y'))
                    valor = int(dato_element.text)
                except (TypeError, ValueError):
                    self.console.print(f"[red]Error: Los atributos 'x', 'y' y el valor de los datos de la matriz '{nombre}' deben ser enteros válidos.[/red]")
                    continue  # Continua con la siguiente matriz

                if not (1 <= x <= n):
                    self.console.print(f"[red]Error: El valor 'x'={x} en la matriz '{nombre}' excede el límite de filas 'n'={n} o es menor que 1.[/red]")
                    continue  # Continua con la siguiente matriz

                if not (1 <= y <= m):
                    self.console.print(f"[red]Error: El valor 'y'={y} en la matriz '{nombre}' excede el límite de columnas 'm'={m} o es menor que 1.[/red]")
                    continue  # Continua con la siguiente matriz

                datos.agregar(Par(x, y), valor)

            self.lista_matrices.agregar(nombre, n, m, datos)
            self.console.print(f"[green]Matriz '{nombre}' añadida a la lista circular.[/green]")

            self.console.print("[yellow]Calculando la matriz binaria...[/yellow]")
            datos_binarios = self.convertir_a_binario(datos)
            nombre_binario = f"{nombre}_Binario"
            self.lista_matrices.agregar(nombre_binario, n, m, datos_binarios)

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
        enlace_documentacion = "https://github.com/DavidVelasquez77/IPC2_Proyecto1_202307705.git"
        
        # Crear un panel con los datos del estudiante
        panel = Panel(
            f"[bold yellow]Nombre:[/bold yellow] [white]{nombre}[/white]\n"
            f"[bold yellow]Carnet:[/bold yellow] [white]{carnet}[/white]\n"
            f"[bold yellow]Curso:[/bold yellow] [white]{curso}[/white]\n"
            f"[bold yellow]Carrera:[/bold yellow] [white]{carrera}[/white]\n"
            f"[bold yellow]Semestre:[/bold yellow] [white]{semestre}[/white]\n"
            f"[bold yellow]Documentación:[/bold yellow] [white]{enlace_documentacion}[/white]",
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
                # Obtener la matriz original
                matriz_original = self.lista_matrices.buscar(actual.nombre.replace('_Binario', ''))

                if matriz_original is None:
                    actual = actual.siguiente
                    if actual == self.lista_matrices.primero:
                        break
                    continue

                patrones = Mapa()

                for i in range(1, actual.n + 1):
                    patron = Lista()
                    for j in range(1, actual.m + 1):
                        valor = actual.obtener_dato(i, j)
                        patron.agregar(Par(j, valor))

                    patron_existente = False
                    for k in range(1, patrones.tamano() + 1):
                        clave = Par(k, None)
                        patron_info = patrones.obtener(clave)
                        if patron_info is not None and self.comparar_patrones(patron_info.obtener(0), patron):
                            filas_grupo = patron_info.obtener(1)
                            filas_grupo.agregar(i)
                            patron_existente = True
                            break

                    if not patron_existente:
                        filas_grupo = Lista()
                        filas_grupo.agregar(i)
                        nuevo_patron = Lista()
                        nuevo_patron.agregar(patron)
                        nuevo_patron.agregar(filas_grupo)
                        patrones.agregar(Par(patrones.tamano() + 1, None), nuevo_patron)

                # Construcción de la matriz reducida
                matriz_reducida = Mapa()
                for k in range(1, patrones.tamano() + 1):
                    clave = Par(k, None)
                    patron_info = patrones.obtener(clave)
                    if patron_info is not None:
                        filas_grupo = patron_info.obtener(1)
                        fila_datos = Lista()
                        for j in range(1, actual.m + 1):
                            suma = 0
                            for idx in range(1, filas_grupo.tamano() + 1):
                                fila = filas_grupo.obtener(idx - 1)
                                suma += matriz_original.obtener_dato(fila, j)
                            fila_datos.agregar(suma)
                        matriz_reducida.agregar(clave, fila_datos)

                # Crear el elemento de la matriz
                matriz_element = ET.SubElement(
                    root,
                    "matriz",
                    nombre=f"{matriz_original.nombre}_Salida",
                    n=str(matriz_reducida.tamano()),
                    m=str(actual.m),
                    g=str(patrones.tamano())
                )

                # Agregar datos de la matriz reducida
                for i in range(1, matriz_reducida.tamano() + 1):
                    fila_datos = matriz_reducida.obtener(Par(i, None))
                    for j in range(1, fila_datos.tamano() + 1):
                        valor = fila_datos.obtener(j - 1)
                        dato_element = ET.SubElement(matriz_element, "dato", x=str(i), y=str(j))
                        dato_element.text = str(valor)

                # Agregar frecuencias de patrones
                for k in range(1, patrones.tamano() + 1):
                    patron_info = patrones.obtener(Par(k, None))
                    if patron_info is not None:
                        filas_grupo = patron_info.obtener(1)
                        frecuencia = filas_grupo.tamano()
                        frecuencia_element = ET.SubElement(matriz_element, "frecuencia", g=str(k))
                        frecuencia_element.text = str(frecuencia)

                self.console.print(f"[yellow]Patrón {k}: Frecuencia {frecuencia}[/yellow]")

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

        while nodo_datos is not None:
            clave_valor_nodo = nodo_datos.valor  # Obtén el objeto NodoMapa
            par = clave_valor_nodo.clave  # Accede a la clave (un objeto Par)
            if par.x > max_x:
                max_x = par.x
            if par.y > max_y:
                max_y = par.y
            nodo_datos = nodo_datos.siguiente

        # Rellenar la tabla con los datos de la matriz sin usar add_row
        i = 1
        while i <= max_x:
            fila = ""
            j = 1
            while j <= max_y:
                valor = datos.obtener(Par(i, j), 0)
                fila += f" {valor} "  # Concatenar los valores de la fila sin indicadores de filas o columnas
                j += 1
            self.console.print(fila)
            i += 1



    def generar_grafica(self):
        if self.lista_matrices.primero is None:
            self.console.print("[red]No hay matrices para generar gráficas.[/red]") 
            return

        matriz = self.lista_matrices.primero

        # Crear el grafo para la matriz original
        matriz_actual = matriz

        # Crear el grafo
        dot = graphviz.Digraph(comment=f'Matriz {matriz_actual.nombre}', format='png')

        # Ajustar el tamaño del lienzo y el espacio entre nodos
        dot.attr(dpi='100', size="10,10", ranksep='0.5', nodesep='0.5')

        # Nodo central con el título "Matrices"
        dot.node('matrices', 'Matrices', shape='ellipse')

        # Nodo con el nombre del ejemplo
        dot.node('ejemplo', matriz_actual.nombre, shape='ellipse')
        dot.edge('matrices', 'ejemplo')

        # Nodos con valores n y m
        dot.node('n', f'n= {matriz_actual.n}', shape='ellipse', style='bold', color='blue', penwidth='2')
        dot.node('m', f'm= {matriz_actual.m}', shape='ellipse', style='bold', color='blue', penwidth='2')
        dot.edge('ejemplo', 'n')
        dot.edge('ejemplo', 'm')

        # Crear nodos para cada columna y conectar con el nodo de la matriz
        for j in range(1, matriz_actual.m + 1):
            dot.node(f'col{j}', f'Columna {j}', shape='ellipse')
            dot.edge('ejemplo', f'col{j}')

        # Añadir nodos para los valores de la matriz
        for j in range(1, matriz_actual.m + 1):
            prev_node = f'col{j}'
            for i in range(1, matriz_actual.n + 1):
                valor = matriz_actual.datos.obtener(Par(i, j), 0)
                node_name = f'{i},{j}'
                dot.node(node_name, str(valor), shape='ellipse')
                dot.edge(prev_node, node_name)
                prev_node = node_name

        # Renderizar el grafo
        dot.render(f'{matriz_actual.nombre}_original_grafica.gv', format='png', cleanup=True)
        self.console.print(f"[green]Gráfica '{matriz_actual.nombre}_original_grafica.png' generada exitosamente.[/green]")




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
