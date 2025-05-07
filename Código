import csv
import tkinter as tk
from tkinter import filedialog

class App:
    def __init__(self, width=500, height=500, name="window"):
        self.path_name = ""        # Ruta del archivo CSV
        self.grid = []              # Aquí se guardará el tablero
        self.cell_labels = []       # Para almacenar las etiquetas del tablero

        # Crear la ventana principal
        self.window = tk.Tk()
        self.window.title(name)
        self.window.geometry(f"{width}x{height}")

        self.SetContent()          # Llama al método para colocar los botones
        self.window.mainloop()    # Inicia el bucle principal de la ventana

    def SetContent(self):
        # Botón para abrir el archivo CSV
        self.fileButton = tk.Button(master=self.window, text="Elige un archivo CSV", height=2, width=15, command=self.getFile)
        self.fileButton.pack(pady=10)

        # Frame para contener el tablero
        self.grid_frame = tk.Frame(master=self.window)
        self.grid_frame.pack(pady=10)

    def getFile(self):
        # Abre el explorador de archivos y guarda el nombre del archivo
        archivo = filedialog.askopenfile(mode='r', filetypes=[("CSV files", "*.csv")])
        if archivo:
            self.path_name = archivo.name
            self.loadGrid()  # Llama a la función para cargar el archivo CSV
            self.displayGrid()  # Muestra el tablero automáticamente

    def loadGrid(self):
        # Carga el CSV en una lista de listas (matriz)
        with open(self.path_name, newline='') as f:
            lector = csv.reader(f)
            self.grid = []
            for fila in lector:
                # Convertimos los valores de texto a enteros
                self.grid.append([int(celda) for celda in fila])
        print("Tablero cargado correctamente.")

    def displayGrid(self):
        # Elimina cualquier contenido anterior del grid_frame
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Muestra cada celda como una etiqueta en la interfaz
        for i, fila in enumerate(self.grid):
            for j, celda in enumerate(fila):
                color = "white" if celda == 1 else "black"
                label = tk.Label(self.grid_frame, width=4, height=2, bg=color, relief="solid", borderwidth=0)
                label.grid(row=i, column=j, padx=1, pady=1)

# Ejecutar la app con dimensiones deseadas
app = App(width=750, height=500)
