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
            self.console.print(f"[debug] Convirtiendo ({clave.x},{clave.y}) valor {valor} a binario: {valor_binario}")
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
                matriz_original = self.lista_matrices.buscar(actual.nombre.replace('_Binario', ''))

                if matriz_original is None:
                    actual = actual.siguiente
                    if actual == self.lista_matrices.primero:
                        break
                    continue

                patrones = Mapa()
                grupos = Mapa()
                g_mapping = Mapa()

                for i in range(1, actual.n + 1):
                    patron = Lista()
                    for j in range(1, actual.m + 1):
                        patron.agregar(actual.obtener_dato(i, j))
                    
                    patron_existente = False
                    for k in range(1, patrones.tamano() + 1):
                        patron_actual = patrones.obtener(Par(k, None))
                        if patron_actual and self.comparar_patrones(patron_actual.obtener(0), patron):
                            patron_actual.obtener(1).agregar(i)
                            patron_existente = True
                            break
                    
                    if not patron_existente:
                        nuevo_grupo = Lista()
                        nuevo_grupo.agregar(i)
                        nuevo_patron = Lista()
                        nuevo_patron.agregar(patron)
                        nuevo_patron.agregar(nuevo_grupo)
                        patrones.agregar(Par(patrones.tamano() + 1, None), nuevo_patron)

                # Usamos un Mapa para representar la matriz reducida
                matriz_reducida = Mapa()
                n_reducida = patrones.tamano()
                m_reducida = actual.m

                for k in range(1, patrones.tamano() + 1):
                    patron_info = patrones.obtener(Par(k, None))
                    if patron_info:
                        filas_grupo = patron_info.obtener(1)
                        for j in range(1, actual.m + 1):
                            suma = 0
                            for idx in range(filas_grupo.tamano()):
                                fila = filas_grupo.obtener(idx)
                                suma += matriz_original.obtener_dato(fila, j)
                            matriz_reducida.agregar(Par(k, j), suma)
                        
                        g_mapping.agregar(Par(k, None), filas_grupo.obtener(0))
                        grupos.agregar(Par(k, None), filas_grupo)

                # Crear el elemento de la matriz para el archivo XML
                matriz_element = ET.SubElement(
                    root,
                    "matriz",
                    nombre=f"{matriz_original.nombre}_Salida",
                    n=str(n_reducida),
                    m=str(m_reducida),
                    g=str(patrones.tamano())
                )

                # Agregar datos de la matriz reducida
                for i in range(1, n_reducida + 1):
                    for j in range(1, m_reducida + 1):
                        valor = matriz_reducida.obtener(Par(i, j))
                        if valor is not None:
                            dato_element = ET.SubElement(matriz_element, "dato", x=str(i), y=str(j))
                            dato_element.text = str(valor)
                            self.console.print(f"[debug] Matriz '{matriz_original.nombre}_Salida': ({i},{j}) = {valor}")

                # Agregar frecuencias y g de patrones
                for k in range(1, grupos.tamano() + 1):
                    filas_grupo = grupos.obtener(Par(k, None))
                    if filas_grupo:
                        frecuencia = filas_grupo.tamano()
                        g_valor = g_mapping.obtener(Par(k, None))
                        frecuencia_element = ET.SubElement(matriz_element, "frecuencia", g=str(g_valor))
                        frecuencia_element.text = str(frecuencia)
                        self.console.print(f"[debug] Grupo {k}: g={g_valor}, Frecuencia {frecuencia}")

                # Agregar la nueva matriz reducida a la lista_matrices
                nombre_matriz_reducida = f"{matriz_original.nombre}_Salida"
                self.lista_matrices.agregar(nombre_matriz_reducida, n_reducida, m_reducida, matriz_reducida)
                self.console.print(f"[green]Matriz reducida '{nombre_matriz_reducida}' añadida a la lista circular.[/green]")

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
        
        for i in range(patron1.tamano()):
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
            
    def crear_grafo(self, matriz, sufijo):
        dot = graphviz.Digraph(comment=f'Matriz {matriz.nombre}', format='png')
        dot.attr(dpi='100', size="10,10", ranksep='0.5', nodesep='0.5')
    
        dot.node('matrices', 'Matrices', shape='ellipse')
        dot.node('ejemplo', matriz.nombre, shape='ellipse')
        dot.edge('matrices', 'ejemplo')
    
        dot.node('n', f'n= {matriz.n}', shape='ellipse', style='bold', color='blue', penwidth='2')
        dot.node('m', f'm= {matriz.m}', shape='ellipse', style='bold', color='blue', penwidth='2')
        dot.edge('ejemplo', 'n')
        dot.edge('ejemplo', 'm')
    
        for j in range(1, matriz.m + 1):
            dot.node(f'col{j}', f'Columna {j}', shape='ellipse')
            dot.edge('ejemplo', f'col{j}')
    
        for j in range(1, matriz.m + 1):
            prev_node = f'col{j}'
            for i in range(1, matriz.n + 1):
                valor = matriz.obtener_dato(i, j)
                self.console.print(f"[debug] Obteniendo valor en ({i},{j}): {valor}")  # Depuración
                node_name = f'{i},{j}'
                dot.node(node_name, str(valor), shape='ellipse')
                dot.edge(prev_node, node_name)
                prev_node = node_name
    
        dot.render(f'{matriz.nombre}_{sufijo}_grafica.gv', format='png', cleanup=True)
        self.console.print(f"[green]Gráfica '{matriz.nombre}_{sufijo}_grafica.png' generada exitosamente.[/green]")
    
    def generar_grafica(self):
        if self.lista_matrices.primero is None:
            self.console.print("[red]No hay matrices para generar gráficas.[/red]")
            return

        # Imprimir todas las matrices de salida disponibles en la lista
        self.console.print("[blue]Matrices de salida disponibles y su contenido:[/blue]")
        current = self.lista_matrices.primero
        has_matrices_salida = False

        while True:
            if current.nombre.endswith('_Salida'):
                self.console.print(f"[yellow]Matriz '{current.nombre}':[/yellow]")
                for i in range(1, current.n + 1):
                    fila = ""
                    for j in range(1, current.m + 1):
                        valor = current.obtener_dato(i, j)
                        fila += f" {valor} "  # Concatenar los valores de la fila
                    self.console.print(fila)
                self.console.print()  # Nueva línea para separar matrices
                has_matrices_salida = True
            current = current.siguiente
            if current == self.lista_matrices.primero:
                break

        if not has_matrices_salida:
            self.console.print("[yellow]No hay matrices de salida disponibles para mostrar.[/yellow]")

        nombre_matriz = input("Ingresa el nombre de la matriz para generar la gráfica: ")
        matriz_original = self.lista_matrices.buscar(nombre_matriz)

        if matriz_original is None:
            self.console.print(f"[red]No se encontró una matriz con el nombre '{nombre_matriz}'.[/red]")
            return

        # Buscar la matriz de salida correspondiente
        nombre_matriz_Salida = f"{nombre_matriz}_Salida"
        matriz_Salida = self.lista_matrices.buscar(nombre_matriz_Salida)

        if matriz_Salida is None:
            self.console.print(f"[yellow]No se encontró una matriz de salida '{nombre_matriz_Salida}'. Solo se generará la gráfica de la matriz original.[/yellow]")

        # Imprimir datos para verificar
        self.console.print(f"[debug] Datos de la matriz original '{nombre_matriz}':")
        for i in range(1, matriz_original.n + 1):
            fila = ""
            for j in range(1, matriz_original.m + 1):
                valor = matriz_original.obtener_dato(i, j)
                fila += f" {valor} "
            self.console.print(fila)

        # Generar gráfica para la matriz original
        self.crear_grafo(matriz_original, "original")

        # Imprimir datos de la matriz de salida para verificar
        if matriz_Salida:
            self.console.print(f"[debug] Matriz de salida cargada: {matriz_Salida.nombre}")
            for i in range(1, matriz_Salida.n + 1):
                fila = ""
                for j in range(1, matriz_Salida.m + 1):
                    valor = matriz_Salida.obtener_dato(i, j)
                    fila += f" {valor} "
                self.console.print(f"[debug] Fila {i}: {fila}")
            
            # Generar gráfica para la matriz de salida
            self.crear_grafo(matriz_Salida, "salida")
        else:
            self.console.print(f"[yellow]No se generó gráfica de salida porque no se encontró la matriz '{nombre_matriz_Salida}'.[/yellow]")

        self.console.print("[blue]Proceso de generación de gráficas completado.[/blue]")



        # Agregar esta sección para depuración
        self.console.print("[blue]Matrices en la lista:[/blue]")
        current = self.lista_matrices.primero
        while current:
            self.console.print(f"- {current.nombre}")
            current = current.siguiente
            if current == self.lista_matrices.primero:
                break

                
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
