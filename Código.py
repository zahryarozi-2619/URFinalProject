import tkinter as tk
from tkinter import filedialog, font

class App:
    def __init__(self, width=500, height=500, name="window"):
        self.path_name = ""      # Nombre de la ruta en donde está el archivo .csv
        self.grid = []             # aquí se guardará el tablero,cuadricula
        self.cell_labels = []      # etiquetas del tablero

        # Creación de la ventana 
        self.window = tk.Tk()      # para la ventana
        self.window.title("Proyecto")   #nombre de la ventana
        self.window.geometry(f"{width}x{height}")  # dimensiones
        self.window.configure(bg='white')  #interfaz visual de la ventana
        self.casillaiteraciones = tk.StringVar()
        self.title_font = font.Font(family='Verdana', size=16, weight='bold')  #solo deja fuentes del sistema :(
        
        self.SetContent()  # llama al método para colocar el contenido

        
        self.window.mainloop()  #  bucle principal de la ventana

    def SetContent(self):
        title_frame = tk.Frame(bg='black')  #un titulo
        title_frame.pack(pady=(0, 10))
        tk.Label(title_frame, 
                 text="  EL  JUEGO  DE  LA  VIDA  ", 
                 font=self.title_font,
                 fg='black',
                 bg='white').pack()

        self.fileButton = tk.Button(master=self.window,          # luego el BOTON para abrir el archivo   
                                    text="seleccione un archivo", 
                                    height=2, 
                                    width=20,
                                    fg='black',
                                    bg='cyan',
                                    command=self.getFile,
                                    font=('Verdana', 10, 'bold'))
        self.fileButton.pack(pady=10)

        # Frame para contener el tablero
        self.grid_frame = tk.Frame(master=self.window)
        self.grid_frame.pack(pady=10)
        # Entrada para número de iteraciones
        entry_frame = tk.Frame(self.window, bg='white')
        entry_frame.pack()
        tk.Label(entry_frame, text="¿Cuántas iteraciones quiere ejecutar?:", bg='white').pack(side='left')
        self.entradadeiteraciones = tk.Entry(entry_frame, textvariable=self.casillaiteraciones, width=5)
        self.entradadeiteraciones .pack(side='left', padx=5)

        # Botón para iniciar iteraciones
        self.botoniteraciones = tk.Button(self.window,
                                        text="Ejecutar",
                                        command=self.iteraciones,
                                        bg='purple',
                                        font=('Verdana', 10, 'bold'))
        self.botoniteraciones.pack(pady=5)

        self.grid_frame = tk.Frame(master=self.window)
        self.grid_frame.pack(pady=10)
        
    def iteraciones(self):
        try:
            entrydeiteraciones = int(self.casillaiteraciones.get())
        except ValueError:
            print("Estas iteraciones no son validas")
            return

        for _ in range(entrydeiteraciones):
            self.grid = self.proximageneracion()
        self.displayGrid()
        
    def getFile(self):
        # Abre el explorador de archivos y guarda el nombre del archivo
        archivo = filedialog.askopenfile(mode='r', filetypes=[("CSV files", "*.csv")])  # Solo archivos CSV
        if archivo:
            self.path_name = archivo.name
            self.loadGrid()  # Llama a la función para cargar el archivo CSV
            self.displayGrid()  # Muestra el tablero automáticamente
    def proximageneracion(self):
        filas, columnas = len(self.grid), len(self.grid[0])
        cuadriculanew = [[0 for _ in range(columnas)] for _ in range(filas)]

        for i in range(filas):
            for j in range(columnas):
                vecinosvivos = self.contarvecinos(i, j)
                if self.grid[i][j] == 1:
                    cuadriculanew[i][j] = 1 if vecinosvivos in [2, 3] else 0
                else:
                    cuadriculanew[i][j] = 1 if vecinosvivos == 3 else 0
        return cuadriculanew
    def contarvecinos(self, x, y):
        contador = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i == x and j == y) or i < 0 or j < 0 or i >= len(self.grid) or j >= len(self.grid[0]):
                    continue
                if self.grid[i][j] == 1:
                    contador += 1
        return contador
    def loadGrid(self): 
        # Cargar archivo CSV manualmente, sin usar 'csv.reader'
        with open(self.path_name, 'r') as archivo:
            self.grid = []  # Creamos una lista vacía para el tablero
            for line in archivo:
                # Eliminar saltos de línea y dividir por coma
                fila = line.strip().split(',')
                # Convertimos cada celda a un valor entero (1 o 0)
                self.grid.append([int(cell) for cell in fila])
        print("El tablero se cargó correctamente") 

    def displayGrid(self): 
        # elimina cualquier contenido anterior del grid_frame
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # muestra cada celda como una etiqueta
        for i, fila in enumerate(self.grid):    #Recorre la matriz y crea cuadros blancos/negros según los valores
            for j, celda in enumerate(fila):
                color = "white" if celda == 1 else "black"
                label = tk.Label(self.grid_frame, width=4, height=2, bg=color, relief="solid", borderwidth=0) #el tk.Label hace una etiqueta para representar la célula
                label.grid(row=i, column=j, padx=1, pady=1) #espacio entre celdas

# Ejecutar la app con dimensiones deseadas
app = App(width=750, height=500)
