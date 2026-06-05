import tkinter as tk
from tkinter import ttk, messagebox
from backend.usuarios import inserir_usuario
from backend.categorias import inserir_categoria_produto, inserir_categoria_financeira

class CadastrosView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()
        
    def _build_ui(self):
        lbl_titulo = ttk.Label(self, text="Cadastros Básicos", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=10)
        
        # Frame Novo Usuário
        f_usr = ttk.LabelFrame(self, text=" Novo Usuário ", padding=10)
        f_usr.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(f_usr, text="Nome:").pack(side="left")
        self.u_nome = ttk.Entry(f_usr, width=15)
        self.u_nome.pack(side="left", padx=5)
        
        ttk.Label(f_usr, text="Login:").pack(side="left")
        self.u_login = ttk.Entry(f_usr, width=15)
        self.u_login.pack(side="left", padx=5)
        
        ttk.Label(f_usr, text="Senha:").pack(side="left")
        self.u_senha = ttk.Entry(f_usr, width=15, show="*")
        self.u_senha.pack(side="left", padx=5)
        
        ttk.Label(f_usr, text="Função:").pack(side="left")
        self.u_role = ttk.Combobox(f_usr, values=["admin", "caixa", "gerente"], state="readonly", width=10)
        self.u_role.pack(side="left", padx=5)
        
        ttk.Button(f_usr, text="Criar Usuário", command=self.criar_usuario).pack(side="left", padx=10)
        
        # Frame Categoria Produto
        f_cp = ttk.LabelFrame(self, text=" Nova Categoria de Produto ", padding=10)
        f_cp.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(f_cp, text="Nome da Categoria:").pack(side="left")
        self.cp_nome = ttk.Entry(f_cp, width=30)
        self.cp_nome.pack(side="left", padx=5)
        
        ttk.Button(f_cp, text="Criar", command=self.criar_cat_produto).pack(side="left", padx=10)
        
        # Frame Categoria Financeira
        f_cf = ttk.LabelFrame(self, text=" Nova Categoria Financeira ", padding=10)
        f_cf.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(f_cf, text="Nome da Categoria:").pack(side="left")
        self.cf_nome = ttk.Entry(f_cf, width=30)
        self.cf_nome.pack(side="left", padx=5)
        
        ttk.Label(f_cf, text="Tipo (ENTRADA/SAIDA):").pack(side="left")
        self.cf_tipo = ttk.Combobox(f_cf, values=["ENTRADA", "SAIDA"], state="readonly", width=10)
        self.cf_tipo.pack(side="left", padx=5)
        
        ttk.Button(f_cf, text="Criar", command=self.criar_cat_financeira).pack(side="left", padx=10)
        
    def criar_usuario(self):
        nome = self.u_nome.get().strip()
        login = self.u_login.get().strip()
        senha = self.u_senha.get().strip()
        role = self.u_role.get().strip()
        if not nome or not login or not senha or not role:
            messagebox.showwarning("Aviso", "Preencha tudo.")
            return
        try:
            inserir_usuario(nome, login, senha, role)
            messagebox.showinfo("Sucesso", "Usuário criado!")
            self.u_nome.delete(0, tk.END)
            self.u_login.delete(0, tk.END)
            self.u_senha.delete(0, tk.END)
            self.u_role.set("")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha:\n{e}")
            
    def criar_cat_produto(self):
        nome = self.cp_nome.get().strip()
        if not nome: return
        try:
            inserir_categoria_produto(nome)
            messagebox.showinfo("Sucesso", "Categoria criada!")
            self.cp_nome.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha:\n{e}")
            
    def criar_cat_financeira(self):
        nome = self.cf_nome.get().strip()
        tipo = self.cf_tipo.get().strip()
        if not nome or not tipo: return
        try:
            inserir_categoria_financeira(nome, tipo)
            messagebox.showinfo("Sucesso", "Categoria criada!")
            self.cf_nome.delete(0, tk.END)
            self.cf_tipo.set("")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha:\n{e}")
