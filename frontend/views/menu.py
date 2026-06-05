import tkinter as tk
from tkinter import ttk
from frontend.views.pdv import PDVView
from frontend.views.estoque import EstoqueView
from frontend.views.produtos import ProdutosView
from frontend.views.financeiro import FinanceiroView
from frontend.views.cadastros import CadastrosView

class MenuView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Layout: Sidebar (Esquerda) + Área de Conteúdo (Direita)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ttk.Frame(self, width=200, relief="raised")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        self.content_area = ttk.Frame(self)
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)
        
        self.sub_frames = {}
        for F in (PDVView, EstoqueView, ProdutosView, FinanceiroView, CadastrosView):
            frame = F(parent=self.content_area, controller=self.controller)
            self.sub_frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self._build_sidebar()
        
    def _build_sidebar(self):
        lbl_titulo = ttk.Label(self.sidebar, text="Menu Principal", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=20, padx=10)
        
        # Informações do usuário
        self.lbl_user = ttk.Label(self.sidebar, text="Usuário: --")
        self.lbl_user.pack(pady=5)
        
        btn_pdv = ttk.Button(self.sidebar, text="Frente de Caixa (PDV)", command=lambda: self.show_sub_frame(PDVView))
        btn_pdv.pack(fill="x", padx=10, pady=5)
        
        btn_estoque = ttk.Button(self.sidebar, text="Estoque", command=lambda: self.show_sub_frame(EstoqueView))
        btn_estoque.pack(fill="x", padx=10, pady=5)
        
        btn_produtos = ttk.Button(self.sidebar, text="Produtos & Fichas", command=lambda: self.show_sub_frame(ProdutosView))
        btn_produtos.pack(fill="x", padx=10, pady=5)
        
        btn_financeiro = ttk.Button(self.sidebar, text="Financeiro", command=lambda: self.show_sub_frame(FinanceiroView))
        btn_financeiro.pack(fill="x", padx=10, pady=5)
        
        btn_cadastros = ttk.Button(self.sidebar, text="Cadastros", command=lambda: self.show_sub_frame(CadastrosView))
        btn_cadastros.pack(fill="x", padx=10, pady=5)
        
        # Espaçador
        ttk.Frame(self.sidebar).pack(fill="both", expand=True)
        
        btn_logout = ttk.Button(self.sidebar, text="Sair (Logout)", command=self.controller.realizar_logout)
        btn_logout.pack(fill="x", padx=10, pady=20)
        
    def show_sub_frame(self, cont):
        frame = self.sub_frames[cont]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()
            
    def on_show(self):
        # Atualiza a label do usuário logado ao entrar no Menu
        if self.controller.usuario_logado:
            user = self.controller.usuario_logado
            role_suffix = f" ({user['funcao']})" if user.get('funcao') else ""
            self.lbl_user.config(text=f"Usuário: {user['login']}{role_suffix}")
        self.show_sub_frame(PDVView) # Default frame ao logar
