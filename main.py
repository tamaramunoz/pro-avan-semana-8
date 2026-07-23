import tkinter as tk
from db_config import DB_CONFIG
from database import DatabaseManager
from gui import AgenciaEspacialApp

if __name__ == "__main__":
    # inicializar gestor de datos y la interfaz
    db_manager = DatabaseManager(DB_CONFIG)
    root = tk.Tk()
    app = AgenciaEspacialApp(root, db_manager)
    root.mainloop()
