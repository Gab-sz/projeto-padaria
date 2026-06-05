import tkinter as tk
from tkinter import ttk
from frontend.views.login import LoginView
from frontend.views.menu import MenuView

class AppController(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Padaria - ERP & PDV")
        self.geometry("1024x768")
        self.minsize(800, 600)
        
        # Tema padrão do ttk
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'
        
        # Variável de sessão
        self.usuario_logado = None
        
        # Container principal
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        # Dicionário de frames instanciados
        self.frames = {}
        
        # Inicializa as views principais que controlam a estrutura (Login e Menu)
        for F in (LoginView, MenuView):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.show_frame(LoginView)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

    def realizar_login(self, dados_usuario):
        self.usuario_logado = dados_usuario
        self.show_frame(MenuView)
        
    def realizar_logout(self):
        self.usuario_logado = None
        self.show_frame(LoginView)
