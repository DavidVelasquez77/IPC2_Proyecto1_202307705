#Importaciones
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
#para los colores en la consola
init(autoreset=True)

class Menu:
    def __init__(self):
        self.console = Console()
        self.archivo_contenido = None
        self.lista_matrices = ListaCircular()  
    
    def mostrar_titulo(self):
            # Genera el título "PROYECTO-1" en formato ASCII usando la fuente "slant"
            ascii_titulo = pyfiglet.figlet_format("PROYECTO-1", font="slant")
            
            # Crea un panel con el título ASCII, un título decorativo, y estilo de borde
            panel = Panel(
                renderable=f"[magenta bold]{ascii_titulo}[/magenta bold]",  # Contenido del panel en negrita magenta
                title="✨ Menu Principal ✨",  # Título del panel
                title_align="center",  # Alineación del título al centro
                border_style="cyan",  # Estilo del borde en color cian
                padding=(0, 1),  # Espaciado interno del panel
                expand=False  # No expandir el panel para llenar el espacio disponible
            )
            
            # Imprime el panel en la consola
            self.console.print(panel)
            
            # Pausa la ejecución por 1 segundo
            time.sleep(1)
            
    def mostrar_menu(self):
            # Crea una tabla con un título centrado y un estilo de borde cian
            table = Table(title="🎯 SELECCIONA UNA OPCIÓN 🎯", title_justify="center", border_style="cyan")
            
            # Agrega una columna para las opciones con estilo amarillo y justificación centrada
            table.add_column("📌 Opción", style="yellow", justify="center")
            
            # Agrega una columna para las descripciones con estilo amarillo y justificación a la izquierda
            table.add_column("Descripción", style="yellow", justify="left")
            
            # Agrega filas a la tabla con las opciones y sus descripciones
            table.add_row("[cyan]1[/cyan]", "[white]🌟 Opción 1: Cargar archivo[/white]")
            table.add_row("[cyan]2[/cyan]", "[white]🌟 Opción 2: Procesar archivo[/white]")
            table.add_row("[cyan]3[/cyan]", "[white]🌟 Opción 3: Escribir archivo salida[/white]")
            table.add_row("[cyan]4[/cyan]", "[white]🌟 Opción 4: Mostrar datos del estudiante[/white]")
            table.add_row("[cyan]5[/cyan]", "[white]🌟 Opción 5: Generar gráfica[/white]")
            table.add_row("[red]6[/red]", "[white]❌ Salir del programa[/white]")
            
            # Imprime la tabla en la consola
            self.console.print(table)
            
    def ejecutar_opcion(self, opcion):
            # Verifica si la opción seleccionada es 1
            if opcion == 1:
                # Imprime un mensaje indicando que se ha seleccionado la opción 1
                self.console.print("✨ Has seleccionado la Opción 1: Cargando el archivo...")
                # Solicita al usuario que ingrese la ruta del archivo
                ruta = input("Ingresar la ruta del archivo: ")
                # Llama al método cargar_archivo con la ruta proporcionada
                self.cargar_archivo(ruta)
            
            # Verifica si la opción seleccionada es 2
            elif opcion == 2:
                # Imprime un mensaje indicando que se ha seleccionado la opción 2
                self.console.print("✨ Has seleccionado la Opción 2: Procesando el archivo...")
                # Llama al método procesar_archivo
                self.procesar_archivo()  
            
            # Verifica si la opción seleccionada es 3
            elif opcion == 3:
                # Imprime un mensaje indicando que se ha seleccionado la opción 3
                self.console.print("✨ Has seleccionado la Opción 3: Escribiendo el archivo de salida...")
                # Llama al método escribir_archivo_salida
                self.escribir_archivo_salida()  
            
            # Verifica si la opción seleccionada es 4
            elif opcion == 4:
                # Imprime un mensaje indicando que se ha seleccionado la opción 4
                self.console.print("✨ Has seleccionado la Opción 4: Mostrando datos del estudiante...")            
                # Llama al método mostrar_datos_estudiante
                self.mostrar_datos_estudiante()  
            
            # Verifica si la opción seleccionada es 5
            elif opcion == 5:
                # Imprime un mensaje indicando que se ha seleccionado la opción 5
                self.console.print("✨ Has seleccionado la Opción 5: Generando gráfica...")
                # Llama al método generar_grafica
                self.generar_grafica()  
            
            # Verifica si la opción seleccionada es 6
            elif opcion == 6:
                # Imprime un mensaje indicando que se ha seleccionado la opción 6 y se está saliendo del programa
                self.console.print("[red]❌ Saliendo del programa... ¡Hasta luego![/red]")
            
            # Si la opción no es válida
            else:
                # Imprime un mensaje indicando que la opción no es válida
                self.console.print("[green]⚠️ Opción no válida. Por favor, selecciona una opción del 1 al 6.[/green]")
                
    def cargar_archivo(self, ruta):
            try:
                # Intenta abrir el archivo en modo lectura
                with open(ruta, 'r') as archivo:
                    # Lee el contenido del archivo y lo almacena en self.archivo_contenido
                    self.archivo_contenido = archivo.read()
                # Imprime un mensaje indicando que el archivo se cargó exitosamente
                self.console.print("[green]Archivo cargado exitosamente.[/green]")
            except FileNotFoundError:
                # Si ocurre un error de archivo no encontrado, imprime un mensaje de error
                self.console.print("[red]Archivo no encontrado. Por favor, verifica la ruta.[/red]")
    
    def procesar_archivo(self):
            # Verifica si no se ha cargado ningún archivo
            if self.archivo_contenido is None:
                self.console.print("[red]No se ha cargado ningún archivo. Por favor, carga un archivo primero.[/red]")
                return
            
            # Imprime un mensaje indicando que se está procesando el archivo XML
            self.console.print("[yellow]Procesando el archivo XML...[/yellow]")
            
            try:
                # Intenta parsear el contenido del archivo como XML
                root = ET.fromstring(self.archivo_contenido)
            except ET.ParseError:
                # Si ocurre un error de parseo, imprime un mensaje de error
                self.console.print("[red]Error al procesar el archivo XML. Asegúrate de que el archivo sea válido.[/red]")
                return
            
            # Verifica que la etiqueta raíz del XML sea 'matrices'
            if root.tag != 'matrices':
                self.console.print("[red]Error: El archivo XML debe comenzar con la etiqueta 'matrices'.[/red]")
                return
            
            # Conjunto para almacenar los nombres de matrices y verificar unicidad
            nombres_matrices = set()
            
            # Itera sobre cada elemento 'matriz' en el XML
            for matriz_element in root.findall('matriz'):
                nombre = matriz_element.get('nombre')
                
                # Verifica si el nombre de la matriz ya existe
                if nombre in nombres_matrices:
                    self.console.print(f"[red]Error: La matriz con nombre '{nombre}' ya existe. Los nombres de matrices deben ser únicos.[/red]")
                    continue  
                
                # Agrega el nombre de la matriz al conjunto
                nombres_matrices.add(nombre)
                
                try:
                    # Intenta convertir los atributos 'n' y 'm' a enteros
                    n = int(matriz_element.get('n'))
                    m = int(matriz_element.get('m'))
                except (TypeError, ValueError):
                    self.console.print(f"[red]Error: Los atributos 'n' y 'm' de la matriz '{nombre}' deben ser enteros válidos.[/red]")
                    continue  
                
                # Mapa para almacenar los datos de la matriz
                datos = Mapa()
                
                # Itera sobre cada elemento 'dato' en la matriz
                for dato_element in matriz_element.findall('dato'):
                    try:
                        # Intenta convertir los atributos 'x', 'y' y el valor del dato a enteros
                        x = int(dato_element.get('x'))
                        y = int(dato_element.get('y'))
                        valor = int(dato_element.text)
                    except (TypeError, ValueError):
                        self.console.print(f"[red]Error: Los atributos 'x', 'y' y el valor de los datos de la matriz '{nombre}' deben ser enteros válidos.[/red]")
                        continue  
                    
                    # Verifica que 'x' esté dentro del rango válido
                    if not (1 <= x <= n):
                        self.console.print(f"[red]Error: El valor 'x'={x} en la matriz '{nombre}' excede el límite de filas 'n'={n} o es menor que 1.[/red]")
                        continue  
                    
                    # Verifica que 'y' esté dentro del rango válido
                    if not (1 <= y <= m):
                        self.console.print(f"[red]Error: El valor 'y'={y} en la matriz '{nombre}' excede el límite de columnas 'm'={m} o es menor que 1.[/red]")
                        continue  
                    
                    # Agrega el dato al mapa de datos
                    datos.agregar(Par(x, y), valor)
                
                # Agrega la matriz a la lista de matrices
                self.lista_matrices.agregar(nombre, n, m, datos)
                self.console.print(f"[green]Matriz '{nombre}' añadida a la lista circular.[/green]")
                
                # Calcula la matriz binaria
                self.console.print("[yellow]Calculando la matriz binaria...[/yellow]")
                datos_binarios = self.convertir_a_binario(datos)
                nombre_binario = f"{nombre}_Binario"
                self.lista_matrices.agregar(nombre_binario, n, m, datos_binarios)
                
                # Muestra las matrices
                self.mostrar_matriz(nombre, datos)
                self.mostrar_matriz(nombre_binario, datos_binarios)
                self.console.print("[green]Matriz binaria generada.[/green]")
    
    def convertir_a_binario(self, mapa):
            # Crea un nuevo mapa para almacenar los datos binarios
            datos_binarios = Mapa()
            
            # Obtiene el nodo inicial de los elementos del mapa
            nodo_actual = mapa.items().inicio
            
            # Itera sobre cada nodo en el mapa
            while nodo_actual:
                # Obtiene la clave del nodo actual
                clave = nodo_actual.valor.clave  
                
                # Obtiene el valor del nodo actual
                valor = nodo_actual.valor.valor  
                
                # Convierte el valor a binario (1 si es mayor que 0, de lo contrario 0)
                valor_binario = 1 if valor > 0 else 0  
                
                # Agrega la clave y el valor binario al nuevo mapa
                datos_binarios.agregar(clave, valor_binario)  
                
                # Avanza al siguiente nodo
                nodo_actual = nodo_actual.siguiente
            
            # Retorna el mapa con los datos binarios
            return datos_binarios
    
    def mostrar_datos_estudiante(self):
            # Define los datos del estudiante
            nombre = "Josue David Velasquez Ixchop"
            carnet = "202307705"
            curso = "Introduccion a la Programacion y Computacion 2"
            carrera = "Ingenieria en Ciencias y Sistemas"
            semestre = "4to Semestre"
            enlace_documentacion = "https://github.com/DavidVelasquez77/IPC2_Proyecto1_202307705.git"
            
            # Crea un panel con los datos del estudiante
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
            
            # Imprime el panel en la consola
            self.console.print(panel)
            
    def escribir_archivo_salida(self):
            # Verifica si no hay matrices procesadas para escribir en el archivo de salida
            if self.lista_matrices.primero is None:
                self.console.print("[red]No hay matrices procesadas para escribir en el archivo de salida.[/red]")
                return
            
            # Crea el elemento raíz del XML
            root = ET.Element("matrices")
            actual = self.lista_matrices.primero
            
            # Itera sobre la lista de matrices
            while True:
                # Verifica si el nombre de la matriz actual termina en '_Binario'
                if actual.nombre.endswith('_Binario'):
                    # Busca la matriz original correspondiente
                    matriz_original = self.lista_matrices.buscar(actual.nombre.replace('_Binario', ''))
                    
                    # Si no se encuentra la matriz original, continúa con la siguiente
                    if matriz_original is None:
                        actual = actual.siguiente
                        if actual == self.lista_matrices.primero:
                            break
                        continue
                    
                    # Inicializa los mapas para patrones, grupos y mapeo de g
                    patrones = Mapa()
                    grupos = Mapa()
                    g_mapping = Mapa()
                    
                    # Itera sobre las filas de la matriz actual
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
                    
                    # Crea el mapa para la matriz reducida
                    matriz_reducida = Mapa()
                    n_reducida = patrones.tamano()
                    m_reducida = actual.m
                    
                    # Calcula los valores de la matriz reducida
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
                    
                    # Crea el elemento de la matriz en el XML
                    matriz_element = ET.SubElement(
                        root,
                        "matriz",
                        nombre=f"{matriz_original.nombre}_Salida",
                        n=str(n_reducida),
                        m=str(m_reducida),
                        g=str(patrones.tamano())
                    )
                    
                    # Agrega los datos de la matriz reducida al XML
                    for i in range(1, n_reducida + 1):
                        for j in range(1, m_reducida + 1):
                            valor = matriz_reducida.obtener(Par(i, j))
                            if valor is not None:
                                dato_element = ET.SubElement(matriz_element, "dato", x=str(i), y=str(j))
                                dato_element.text = str(valor)
                    
                    # Agrega las frecuencias y valores de g de los patrones al XML
                    for k in range(1, grupos.tamano() + 1):
                        filas_grupo = grupos.obtener(Par(k, None))
                        if filas_grupo:
                            frecuencia = filas_grupo.tamano()
                            g_valor = g_mapping.obtener(Par(k, None))
                            frecuencia_element = ET.SubElement(matriz_element, "frecuencia", g=str(g_valor))
                            frecuencia_element.text = str(frecuencia)
                    
                    # Agrega la matriz reducida a la lista de matrices
                    nombre_matriz_reducida = f"{matriz_original.nombre}_Salida"
                    self.lista_matrices.agregar(nombre_matriz_reducida, n_reducida, m_reducida, matriz_reducida)
                    self.console.print(f"[green]Matriz reducida '{nombre_matriz_reducida}' añadida a la lista circular.[/green]")
                
                # Avanza al siguiente nodo en la lista de matrices
                actual = actual.siguiente
                if actual == self.lista_matrices.primero:
                    break
            
            # Convierte el árbol XML a una cadena con formato bonito
            xml_str = ET.tostring(root, encoding="utf-8")
            pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")
            
            # Escribe la cadena XML en un archivo
            with open("archivo_salida.xml", "w", encoding="utf-8") as archivo_salida:
                archivo_salida.write(pretty_xml_str)
            
            # Imprime un mensaje indicando que el archivo de salida se escribió exitosamente
            self.console.print("[green]Archivo de salida escrito exitosamente como 'archivo_salida.xml'.[/green]")    
            
    def comparar_patrones(self, patron1, patron2):
            # Verifica si alguno de los patrones es None
            if patron1 is None or patron2 is None:
                return False
            
            # Verifica si los tamaños de los patrones son diferentes
            if patron1.tamano() != patron2.tamano():
                return False
            
            # Compara los elementos de los patrones uno por uno
            for i in range(patron1.tamano()):
                if patron1.obtener(i) != patron2.obtener(i):
                    return False
            
            # Si todos los elementos son iguales, retorna True
            return True
    
    def mostrar_matriz(self, nombre, datos):
            # Imprime el nombre de la matriz en color amarillo
            self.console.print(f"[yellow]Matriz '{nombre}':[/yellow]")
            
            # Verifica si la matriz no tiene datos
            if datos.tamano() == 0:
                self.console.print("[red]No hay datos para mostrar en la matriz.[/red]")
                return
            
            # Inicializa las variables para encontrar los máximos valores de x e y
            max_x = 0
            max_y = 0
            
            # Obtiene el nodo inicial de los datos
            nodo_datos = datos.items().inicio
            
            # Itera sobre los nodos para encontrar los máximos valores de x e y
            while nodo_datos is not None:
                clave_valor_nodo = nodo_datos.valor  # Obtiene el valor del nodo actual
                par = clave_valor_nodo.clave  # Obtiene la clave (Par) del nodo actual
                
                # Actualiza el máximo valor de x si es necesario
                if par.x > max_x:
                    max_x = par.x
                
                # Actualiza el máximo valor de y si es necesario
                if par.y > max_y:
                    max_y = par.y
                
                # Avanza al siguiente nodo
                nodo_datos = nodo_datos.siguiente
            
            # Itera sobre las filas de la matriz
            i = 1
            while i <= max_x:
                fila = ""  # Inicializa la cadena para la fila actual
                j = 1
                
                # Itera sobre las columnas de la matriz
                while j <= max_y:
                    # Obtiene el valor de la posición (i, j) en la matriz, o 0 si no existe
                    valor = datos.obtener(Par(i, j), 0)
                    
                    # Agrega el valor a la cadena de la fila
                    fila += f" {valor} "  
                    j += 1
                
                # Imprime la fila actual
                self.console.print(fila)
                i += 1            
                
    def crear_grafo(self, matriz, sufijo):
            # Crea un nuevo objeto Digraph de graphviz con un comentario y formato PNG
            dot = graphviz.Digraph(comment=f'Matriz {matriz.nombre}', format='png')
            
            # Establece atributos generales del grafo
            dot.attr(dpi='100', size="10,10", ranksep='0.5', nodesep='0.5')
            
            # Crea nodos y aristas para la estructura básica del grafo
            dot.node('matrices', 'Matrices', shape='ellipse')
            dot.node('ejemplo', matriz.nombre, shape='ellipse')
            dot.edge('matrices', 'ejemplo')
            
            # Crea nodos para los atributos 'n' y 'm' de la matriz
            dot.node('n', f'n= {matriz.n}', shape='ellipse', style='bold', color='blue', penwidth='2')
            dot.node('m', f'm= {matriz.m}', shape='ellipse', style='bold', color='blue', penwidth='2')
            dot.edge('ejemplo', 'n')
            dot.edge('ejemplo', 'm')
            
            # Crea nodos y aristas para cada columna de la matriz
            for j in range(1, matriz.m + 1):
                dot.node(f'col{j}', f'Columna {j}', shape='ellipse')
                dot.edge('ejemplo', f'col{j}')
            
            # Crea nodos y aristas para cada valor en la matriz
            for j in range(1, matriz.m + 1):
                prev_node = f'col{j}'
                for i in range(1, matriz.n + 1):
                    valor = matriz.obtener_dato(i, j)
                    node_name = f'{i},{j}'
                    dot.node(node_name, str(valor), shape='ellipse')
                    dot.edge(prev_node, node_name)
                    prev_node = node_name
            
            # Renderiza el grafo a un archivo PNG y limpia los archivos intermedios
            dot.render(f'{matriz.nombre}_{sufijo}_grafica.gv', format='png', cleanup=True)
            
            # Imprime un mensaje indicando que la gráfica se generó exitosamente
            self.console.print(f"[green]Gráfica '{matriz.nombre}_{sufijo}_grafica.png' generada exitosamente.[/green]")   
            
    def generar_grafica(self):
            # Verifica si no hay matrices en la lista
            if self.lista_matrices.primero is None:
                self.console.print("[red]No hay matrices para generar gráficas.[/red]")
                return
            
            # Imprime un mensaje indicando que se mostrarán las matrices de salida disponibles
            self.console.print("[blue]Matrices de salida disponibles y su contenido:[/blue]")
            
            current = self.lista_matrices.primero
            has_matrices_salida = False
            
            # Itera sobre la lista de matrices
            while True:
                # Verifica si el nombre de la matriz actual termina en '_Salida'
                if current.nombre.endswith('_Salida'):
                    self.console.print(f"[yellow]Matriz '{current.nombre}':[/yellow]")
                    
                    # Imprime el contenido de la matriz
                    for i in range(1, current.n + 1):
                        fila = ""
                        for j in range(1, current.m + 1):
                            valor = current.obtener_dato(i, j)
                            fila += f" {valor} "  
                        self.console.print(fila)
                    self.console.print()  
                    has_matrices_salida = True
                
                # Avanza al siguiente nodo en la lista de matrices
                current = current.siguiente
                if current == self.lista_matrices.primero:
                    break
            
            # Verifica si no hay matrices de salida disponibles
            if not has_matrices_salida:
                self.console.print("[yellow]No hay matrices de salida disponibles para mostrar.[/yellow]")
            
            # Solicita al usuario que ingrese el nombre de la matriz para generar la gráfica
            nombre_matriz = input("Ingresa el nombre de la matriz para generar la gráfica: ")
            matriz_original = self.lista_matrices.buscar(nombre_matriz)
            
            # Verifica si la matriz original no se encontró
            if matriz_original is None:
                self.console.print(f"[red]No se encontró una matriz con el nombre '{nombre_matriz}'.[/red]")
                return
            
            # Busca la matriz de salida correspondiente
            nombre_matriz_Salida = f"{nombre_matriz}_Salida"
            matriz_Salida = self.lista_matrices.buscar(nombre_matriz_Salida)
            
            # Verifica si la matriz de salida no se encontró
            if matriz_Salida is None:
                self.console.print(f"[yellow]No se encontró una matriz de salida '{nombre_matriz_Salida}'. Solo se generará la gráfica de la matriz original.[/yellow]")
            
            # Imprime los datos de la matriz original
            self.console.print(f"[debug] Datos de la matriz original '{nombre_matriz}':")
            for i in range(1, matriz_original.n + 1):
                fila = ""
                for j in range(1, matriz_original.m + 1):
                    valor = matriz_original.obtener_dato(i, j)
                    fila += f" {valor} "
                self.console.print(fila)
            
            # Genera la gráfica de la matriz original
            self.crear_grafo(matriz_original, "original")
            
            # Si la matriz de salida existe, imprime sus datos y genera su gráfica
            if matriz_Salida:
                self.console.print(f"[debug] Matriz de salida cargada: {matriz_Salida.nombre}")
                for i in range(1, matriz_Salida.n + 1):
                    fila = ""
                    for j in range(1, matriz_Salida.m + 1):
                        valor = matriz_Salida.obtener_dato(i, j)
                        fila += f" {valor} "
                    self.console.print(f"[debug] Fila {i}: {fila}")
                
                self.crear_grafo(matriz_Salida, "salida")
            else:
                self.console.print(f"[yellow]No se generó gráfica de salida porque no se encontró la matriz '{nombre_matriz_Salida}'.[/yellow]")
            
            # Imprime un mensaje indicando que el proceso de generación de gráficas se completó
            self.console.print("[blue]Proceso de generación de gráficas completado.[/blue]")
            
if __name__ == "__main__":
    # Crea una instancia del menú
    menu = Menu()
    
    # Muestra el título del menú
    menu.mostrar_titulo()
    
    # Bucle principal del menú
    while True:
        # Muestra las opciones del menú
        menu.mostrar_menu()
        try:
            # Solicita al usuario que seleccione una opción
            opcion = int(input("Selecciona una opción: "))
            
            # Ejecuta la opción seleccionada
            menu.ejecutar_opcion(opcion)
            
            # Si la opción es 6, sale del bucle y termina el programa
            if opcion == 6:
                break
        except ValueError:
            # Maneja el error si el usuario ingresa un valor no válido
            print("[red]⚠️ Por favor, ingresa un número válido.[/red]")