import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
from datetime import datetime
from qbittorrent_port_updater import (
    load_env, save_env, get_forwarded_port, 
    set_qbittorrent_port, get_current_qbittorrent_port
)
import threading
import time

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.update()

    def flush(self):
        pass

class PortCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("qBittorrent Port Checker")
        self.root.geometry("800x600")
        
        # Variáveis
        self.running = False
        self.credentials = load_env() or ('http://localhost:8080', 'admin', 'adminadmin')
        self.host_var = tk.StringVar(value=self.credentials[0])
        self.username_var = tk.StringVar(value=self.credentials[1])
        self.password_var = tk.StringVar(value=self.credentials[2])

        self.create_widgets()
        
    def create_widgets(self):
        # Frame de configurações
        config_frame = ttk.LabelFrame(self.root, text="Configurações", padding=10)
        config_frame.pack(fill=tk.X, padx=5, pady=5)

        # Host
        ttk.Label(config_frame, text="Host:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(config_frame, textvariable=self.host_var, width=40).grid(row=0, column=1, padx=5, pady=2)

        # Username
        ttk.Label(config_frame, text="Usuário:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(config_frame, textvariable=self.username_var).grid(row=1, column=1, padx=5, pady=2)

        # Password
        ttk.Label(config_frame, text="Senha:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(config_frame, textvariable=self.password_var, show="*").grid(row=2, column=1, padx=5, pady=2)

        # Botões
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(button_frame, text="Iniciar", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Parar", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Salvar Configurações", command=self.save_settings).pack(side=tk.LEFT, padx=5)

        # Area de Log
        log_frame = ttk.LabelFrame(self.root, text="Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=20)
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # Redirecionar stdout para o log
        sys.stdout = RedirectText(self.log_area)

    def save_settings(self):
        host = self.host_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        save_env(host, username, password)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Configurações salvas com sucesso!")

    def start_monitoring(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Iniciar thread de monitoramento
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Monitoramento parado.")

    def monitor_loop(self):
        while self.running:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Verificando porta...")
            
            # Obter a porta encaminhada
            port = get_forwarded_port()
            if port:
                current_qb_port = get_current_qbittorrent_port(
                    self.host_var.get(),
                    self.username_var.get(),
                    self.password_var.get()
                )
                
                if current_qb_port is None:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Falha ao obter porta atual do qBittorrent.")
                elif current_qb_port != port:
                    if set_qbittorrent_port(port, self.host_var.get(), self.username_var.get(), self.password_var.get()):
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Porta do qBittorrent atualizada de {current_qb_port} para {port}")
                    else:
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Falha ao atualizar porta do qBittorrent.")
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Porta já está correta: {port}")
            
            time.sleep(45)

if __name__ == "__main__":
    root = tk.Tk()
    app = PortCheckerGUI(root)
    root.mainloop()