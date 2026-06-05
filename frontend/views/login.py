import tkinter as tk
from tkinter import ttk, messagebox
from backend.usuarios import autenticar_usuario

class LoginView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Centralizar o frame de login usando grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        login_frame = ttk.LabelFrame(self, text=" Acesso ao Sistema ", padding=(20, 20))
        login_frame.grid(row=1, column=1)
        
        ttk.Label(login_frame, text="Login:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_login = ttk.Entry(login_frame, width=30)
        self.entry_login.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Senha:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_senha = ttk.Entry(login_frame, show="*", width=30)
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)
        
        btn_login = ttk.Button(login_frame, text="Entrar", command=self.fazer_login)
        btn_login.grid(row=2, column=0, columnspan=2, pady=15)
        
        # Bind do Enter para fazer login rapidamente
        self.entry_senha.bind("<Return>", lambda e: self.fazer_login())

    def on_show(self):
        # Limpa ao voltar para a tela de login
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_login.focus()

    def fazer_login(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not login or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
            
        try:
            usuario = autenticar_usuario(login, senha)
            if usuario:
                self.controller.realizar_login(usuario)
            else:
                messagebox.showerror("Erro", "Credenciais inválidas.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no login:\n{e}")
