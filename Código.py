import tkinter as tk
from tkinter import filedialog, font, messagebox

class App:
    def __init__(self, width=500, height=500, name="window"):
        self.path_name = ""      # Nombre de la ruta en donde está el archivo .csv
        self.grid = []             # aquí se guardará el tablero,cuadricula
        self.cell_labels = []      # etiquetas del tablero

        # Creación de la ventana 
        self.window = tk.Tk()      # para la ventana
        self.window.title("Proyecto")   #nombre de la ventana
        self.window.geometry(f"{width}x{height}")  # dimensiones
        self.window.configure(bg='black')  #interfaz visual de la ventana
        self.casillaiteraciones = tk.StringVar()
        self.title_font = font.Font(family='Verdana', size=30, weight='bold')  #solo deja fuentes del sistema :(
        
        self.SetContent()  # llama al método para colocar el contenido

        
        self.window.mainloop()  #  bucle principal de la ventana

    def SetContent(self):
        title_frame = tk.Frame(bg='black')  #un titulo
        title_frame.pack(pady=(0, 10))
        tk.Label(title_frame, 
                 text=" -  👾 EL  JUEGO  DE  LA  VIDA 👾  -  ", 
                 font=self.title_font,
                 fg='white',
                 bg='black').pack()

        self.fileButton = tk.Button(master=self.window,          # luego el BOTON para abrir el archivo   
                                    text="📂- Seleccione un archivo -🗃", 
                                    height=2, 
                                    width=30,
                                    fg='white',
                                    bg='black',
                                    command=self.getFile,
                                    font=('Verdana', 10, 'bold'))
        self.fileButton.pack(pady=10)
        self.save_button = tk.Button( #boton guardar tablero
            self.window,
            text="🔽 Descargar tablero 🔽",
            command=self.guardar_tablero,  # Función que definiremos
            bg='black',
            fg='white',
            font=('Verdana', 10)
        )
        self.save_button.pack(pady=10)
        # Frame para contener el tablero
        self.grid_frame = tk.Frame(master=self.window)
        self.grid_frame.pack(pady=10)
        # Entrada para número de iteraciones
        entry_frame = tk.Frame(self.window,bg="white")
        entry_frame.pack()
        tk.Label(entry_frame, text=" 🔁 ¿Cuántas iteraciones quiere ejecutar? 🔁 :", bg='white').pack(side='left')
        self.entradadeiteraciones = tk.Entry(entry_frame, textvariable=self.casillaiteraciones, width=5)
        self.entradadeiteraciones .pack(side='left', padx=5)

        # Botón para iniciar iteraciones
        self.botoniteraciones = tk.Button(self.window,
                                        text="Ejecutar",
                                        command=self.iteraciones, #command=self.iteraciones llama al método iteraciones() al presionar el botón
                                        bg='purple',
                                        font=('Verdana', 10, 'bold'))
        self.botoniteraciones.pack(pady=5)

        self.grid_frame = tk.Frame(master=self.window)
        self.grid_frame.pack(pady=10)
        
    def loadGrid(self): 
            # Cargar archivo CSV manualmente, sin usar 'csv.reader'
            with open(self.path_name, 'r') as archivo:
                self.grid = []  # Creamos una lista vacía para el tablero
                for line in archivo:
                    # Eliminar saltos de línea y dividir por coma
                    fila = line.strip().split(',')
                    # Convertimos cada celda a un valor entero (1 o 0)
                    self.grid.append([int(cell) for cell in fila])
             # validar dimensiones mínimas (9x9)
            if len(self.grid) < 9:
                tk.messagebox.showerror("Error", "El archivo debe tener al menos 9 filas y 9 columnas.")
                self.grid = []  # Borra el tablero para que no se use
                return
            print("El tablero se cargó correctamente") 

    def guardar_tablero(self):
        
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Guardar tablero como CSV"
        )

        if ruta_archivo:
            try:
                with open(ruta_archivo, 'w') as archivof: #abre el archivo en modo escritura
                    for fila in self.grid:
                        linea = ','.join(map(str, fila)) + '\n'
                        archivof.write(linea)
#map(str, fila): Convierte cada elemento de la fila (números 0 o 1) a strings
#','.join(...): Une los elementos con comas formato .csv
#+ '\n': Agrega un salto de línea al final de cada fila
                messagebox.showinfo("Éxito", "Tablero guardado correctamente. ✔")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

        
    def iteraciones(self):
        try: #Contiene el código que podría lanzar una excepción (error).
            entrydeiteraciones = int(self.casillaiteraciones.get()) #convierte la entrada de iteraciones del usuario a entero
        except ValueError:#error de valor, se ejecuta solo si ocurre
            print("Estas iteraciones no son validas")
            return

        for _ in range(entrydeiteraciones): # ejecuta proximageneracion() según el número de iteraciones
            self.grid = self.proximageneracion()
        self.displayGrid() #actualiza el tablero
        
    def getFile(self):
        # Abre el explorador de archivos y guarda el nombre del archivo
        archivo = filedialog.askopenfile(mode='r', filetypes=[("CSV files", "*.csv")])  # Solo archivos CSV
        if archivo:
            self.path_name = archivo.name
            self.loadGrid()  # Llama a la función para cargar el archivo CSV
            self.displayGrid()  # Muestra el tablero automáticamente
            
    def proximageneracion(self):
        filas, columnas = len(self.grid), len(self.grid[0])#se define cuales son las filas y las columnas
        #el self.grid es la matriz (lista de listas) que representa el tablero actual/len(self.grid) devuelve el número de filas (sub-listas en la lista principal)/len(self.grid[0]) devuelve los elementos en la primera fila que serian las columnas
        cuadriculanew = [[0 for _ in range(columnas)] for _ in range(filas)]#una cuadricula nueva, una nueva matriz con todos los valores en 0
        #[0 for _ in range(columnas)] crea una fila con columnas cero
        #for _ in range(filas) repite la creación de filas filas veces
        for i in range(filas): #itera sobre cada fila
            for j in range(columnas):#ppor cada fila itera sobre cada columna esto apra aacceder a cada célula del tablero
                vecinosvivos = self.contarvecinos(i, j) #método contarvecinos(i, j) para obtener el número de células vivas alrededor de la posición (i, j)
                if self.grid[i][j] == 1: #si esta viva
                    cuadriculanew[i][j] = 1 if vecinosvivos in [2, 3] else 0# célula viva (1)sobrevive con 2 o 3 vecinos vivos
                else:#si esta muerta
                    cuadriculanew[i][j] = 1 if vecinosvivos == 3 else 0 #Célula muerta (0) revive con exactamente 3 vecinos vivos
                    
        return cuadriculanew
    def contarvecinos(self, x, y):
        contador = 0 #lleva la cuenta de vecinos vivos
        for i in range(x - 1, x + 2):
#range(x - 1, x + 2) genera valores desde x-1 hasta x+1 (3 filas: arriba, la misma, abajo)
#Igual para j (3 columnas: izquierda, misma, derecha)
# esto para revisar las 8 células adyacentes más la célula central (x, y) que luego no se debe tener en cuenta pues no es su propia vecina
            for j in range(y - 1, y + 2):
                if (i == x and j == y) or i < 0 or j < 0 or i >= len(self.grid) or j >= len(self.grid[0]):
                    #(i == x and j == y) revisa si es la celula central 
                    # i < 0 or j < 0 evita cualquier indice negativo que están fuera de los límites válidos del tablero (para las celulas en los bordes del tablero)
                    #i >= len(self.grid) o j >= len(self.grid[0])evita índices fuera del borde inferior/derecho
                    continue #Ignora células que: son la célula central que estamos evaluando,estan fuera de los límites del tablero.
                if self.grid[i][j] == 1:
                    contador += 1# si la célula en (i, j) está viva (1), incrementa el contador
        return contador

    def displayGrid(self): 
        # elimina cualquier contenido anterior del grid_frame
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # muestra cada celda como una etiqueta
        for i, fila in enumerate(self.grid):    #Recorre la matriz y crea cuadros blancos/negros según los valores
            for j, celda in enumerate(fila):
                color = "white" if celda == 1 else "#340524"
                label = tk.Label(self.grid_frame, width=4, height=2, bg=color, relief="solid", borderwidth=0) #el tk.Label hace una etiqueta para representar la célula
                label.grid(row=i, column=j, padx=1, pady=1) #espacio entre celdas

# Ejecutar la app con dimensiones deseadas
app = App(width=750, height=500)
