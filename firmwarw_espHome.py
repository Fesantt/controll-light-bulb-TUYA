import requests
import tkinter as tk
from tkinter import colorchooser
import warnings

warnings.filterwarnings("ignore")


ipLamp = "192.168.1.4" # IP do dispositivo

# Endereços dos endpoints
endereco_base = f"http://{ipLamp}/light/light/turn_on"
endereco_desligar = f"http://{ipLamp}/light/light/turn_off"

def ligar():
    try:
        response = requests.get(f"{endereco_base}?brightness=1000")
        if response.ok:
            status_label.config(text="Status: Lâmpada ligada", fg="#00ff99")
        else:
            status_label.config(text="Erro ao ligar a lâmpada", fg="red")
    except Exception as e:
        status_label.config(text=f"Erro: {e}", fg="red")

def desligar():
    try:
        response = requests.get(endereco_desligar)
        if response.ok:
            status_label.config(text="Status: Lâmpada desligada", fg="#ff3333")
        else:
            status_label.config(text="Erro ao desligar a lâmpada", fg="red")
    except Exception as e:
        status_label.config(text=f"Erro: {e}", fg="red")

def escolher_cor():
    try:
        cor_rgb, _ = colorchooser.askcolor(title="Escolha uma cor")
        if cor_rgb:
            r, g, b = map(int, cor_rgb)
            response = requests.get(f"{endereco_base}?brightness=1000&r={r}&g={g}&b={b}")
            if response.ok:
                status_label.config(text=f"Cor definida para RGB({r}, {g}, {b})", fg="white")
            else:
                status_label.config(text="Erro ao definir cor", fg="red")
    except Exception as e:
        status_label.config(text=f"Erro ao definir cor: {e}", fg="red")


def ajustar_brilho(valor):
    try:
        valor = int(valor)
        
        min_brilho = 1
        max_brilho = 255
        
        brilho = int((valor / 100) * (max_brilho - min_brilho) + min_brilho)
        
        if min_brilho <= brilho <= max_brilho:
            response = requests.post(f"{endereco_base}?brightness={brilho}")
            
            if response.ok:
                status_label.config(text=f"Brilho definido para {valor}%", fg="orange")
            else:
                status_label.config(text="Erro ao definir brilho", fg="red")
        else:
            status_label.config(text="Erro: O brilho deve estar entre 1 e 255", fg="red")
    
    except Exception as e:
        status_label.config(text=f"Erro ao definir brilho: {e}", fg="red")

def ajustar_temperatura(valor):
    try:
        valor = int(valor)
        
        min_temp = 153.8
        max_temp = 370.4
        
        temperatura = int((valor / 100) * (max_temp - min_temp) + min_temp)
        
        response = requests.get(f"{endereco_base}?&color_temp={temperatura}")
        
        if response.ok:
            status_label.config(text=f"Temperatura de cor definida para {valor}%", fg="purple")
        else:
            status_label.config(text="Erro ao definir temperatura de cor", fg="red")
    
    except Exception as e:
        status_label.config(text=f"Erro ao definir temperatura de cor: {e}", fg="red")

def iniciar_arrasto(event):
    janela.x_start = event.x
    janela.y_start = event.y

def arrastar(event):
    x = janela.winfo_x() + (event.x - janela.x_start)
    y = janela.winfo_y() + (event.y - janela.y_start)
    janela.geometry(f"+{x}+{y}")

# Configuração da interface Tkinter
janela = tk.Tk()
janela.title("Lâmpada Santt")
janela.geometry("300x420+100+100")
janela.configure(bg="#2c2f33")
janela.overrideredirect(True)

title_bar = tk.Frame(janela, bg="#202225", relief="flat", height=30)
title_bar.pack(fill="x")
title_label = tk.Label(title_bar, text="Lâmpada Santt", fg="white", bg="#202225", font=("Arial", 10, "bold"))
title_label.pack(side="left", padx=10)

def fechar():
    janela.destroy()

close_button = tk.Button(title_bar, text="✕", font=("Arial", 12), fg="white", bg="#ff3333", command=fechar,
                         relief="flat", bd=0, activebackground="#ff5e5e", cursor="hand2")
close_button.pack(side="right", padx=10)

button_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#5865f2",
    "fg": "white",
    "relief": "flat",
    "width": 20,
    "height": 1,
    "bd": 0,
    "activebackground": "#4752c4",
    "highlightthickness": 0,
    "cursor": "hand2"
}

status_style = {
    "font": ("Arial", 10),
    "fg": "#dcdfe4",
    "bg": "#2c2f33"
}

ligar_btn = tk.Button(janela, text="Ligar", command=ligar, **button_style)
ligar_btn.pack(pady=10)

desligar_btn = tk.Button(janela, text="Desligar", command=desligar, **button_style)
desligar_btn.config(bg="#ff3333", activebackground="#ff5e5e")
desligar_btn.pack(pady=10)

cor_btn = tk.Button(janela, text="Escolher Cor", command=escolher_cor, **button_style)
cor_btn.config(bg="#42a5f5", activebackground="#64b5f6")
cor_btn.pack(pady=10)

brilho_label = tk.Label(janela, text="Ajustar Brilho (0 a 100)", **status_style)
brilho_label.pack(pady=(20, 5))

brilho_scale = tk.Scale(janela, from_=0, to=100, orient="horizontal", length=300, command=ajustar_brilho,
                        fg="white", bg="#2c2f33", troughcolor="#5865f2", sliderrelief="flat", highlightbackground="#2c2f33",
                        activebackground="#5865f2", sliderlength=20, bd=0)
brilho_scale.set(100)
brilho_scale.pack(pady=5)

temp_label = tk.Label(janela, text="Temperatura de Cor (0 a 100)", **status_style)
temp_label.pack(pady=(20, 5))

temp_scale = tk.Scale(janela, from_=0, to=100, orient="horizontal", length=300, command=ajustar_temperatura,
                      fg="white", bg="#2c2f33", troughcolor="#ffb74d", sliderrelief="flat", highlightbackground="#2c2f33",
                      activebackground="#ffb74d", sliderlength=20, bd=0)
temp_scale.set(50)
temp_scale.pack(pady=5)

status_label = tk.Label(janela, text="Status: Aguardando comando", **status_style)
status_label.pack(pady=20)

title_bar.bind("<Button-1>", iniciar_arrasto)
title_bar.bind("<B1-Motion>", arrastar)

janela.mainloop()
