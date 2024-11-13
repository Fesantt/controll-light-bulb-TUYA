import tinytuya
import tkinter as tk
from tkinter import colorchooser
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

device_id = "SEU_DEVICE_ID" #  ID DO DISPOSITIVO
local_key = "SUA_LOCAL_KEY" # LOCAL KEY PARA AUTENTICAÇÃO NO DISPOSITIVO
device_ip = "192.168.1.3" # IP DO SEU DISPOSITIVO
version = 3.3

device = tinytuya.BulbDevice(device_id, device_ip, local_key)
device.set_version(version)

def ligar():
    try:
        device.turn_on()
        status_label.config(text="Status: Lâmpada ligada", fg="green")
    except Exception as e:
        status_label.config(text=f"Erro: {e}", fg="red")

def desligar():
    try:
        device.turn_off()
        status_label.config(text="Status: Lâmpada desligada", fg="red")
    except Exception as e:
        status_label.config(text=f"Erro: {e}", fg="red")

def escolher_cor():
    try:
        cor_rgb, cor_hex = colorchooser.askcolor(title="Escolha uma cor")
        if cor_rgb:
            r, g, b = map(int, cor_rgb)
            device.set_colour(r, g, b)
            status_label.config(text=f"Cor definida para RGB({r}, {g}, {b})", fg="blue")
    except Exception as e:
        status_label.config(text=f"Erro ao definir cor: {e}", fg="red")

def ajustar_brilho(valor):
    try:
        valor = int(valor)
        if 0 <= valor <= 100:
            brilho = int((valor / 100) * (1000 - 25) + 25)
            device.set_brightness(brilho)
            status_label.config(text=f"Brilho definido para {valor}%", fg="orange")
        else:
            status_label.config(text="Erro: Valor de brilho fora do intervalo (0-100)", fg="red")
    except Exception as e:
        status_label.config(text=f"Erro ao definir brilho: {e}", fg="red")

def ajustar_temperatura(valor):
    try:
        valor = int(valor)
        if 0 <= valor <= 1000:
            temperatura = int((valor / 100) * (1000 - 25) + 25)
            device.set_colourtemp(temperatura)
            status_label.config(text=f"Temperatura de cor definida para {valor}%", fg="purple")
        else:
            status_label.config(text="Erro: Valor de temperatura fora do intervalo (0-100)", fg="red")
    except Exception as e:
        status_label.config(text=f"Erro ao definir temperatura de cor: {e}", fg="red")


def criar_icone_bandeja():
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 64, 64), fill=(0, 255, 0))

    def abrir_janela(icon, item):
        janela.deiconify()

    def sair(icon, item):
        icon.stop()
        janela.quit()

    icon = pystray.Icon("controle_lampada", image, "Controle da Lâmpada", menu=pystray.Menu(
        item('Abrir', abrir_janela),
        item('Sair', sair)
    ))

    icon.run()

janela = tk.Tk()
janela.title("Lampada Santt")
janela.geometry("350x460")
janela.configure(bg="#2d2d2d")

button_style = {"font": ("Arial", 12, "bold"), "bg": "#4caf50", "fg": "white", "relief": "raised", "width": 15}
status_style = {"font": ("Arial", 10), "fg": "white", "bg": "#2d2d2d"}

ligar_btn = tk.Button(janela, text="Ligar", command=ligar, **button_style)
ligar_btn.pack(pady=10)

desligar_btn = tk.Button(janela, text="Desligar", command=desligar, **button_style)
desligar_btn.config(bg="#f44336")
desligar_btn.pack(pady=10)

cor_btn = tk.Button(janela, text="Escolher Cor", command=escolher_cor, **button_style)
cor_btn.config(bg="#2196f3")
cor_btn.pack(pady=10)

brilho_label = tk.Label(janela, text="Ajustar Brilho (0 a 100)", **status_style)
brilho_label.pack(pady=(20, 5))

brilho_scale = tk.Scale(janela, from_=0, to=100, orient="horizontal", length=250, command=ajustar_brilho,
                        fg="white", bg="#2d2d2d", troughcolor="#555", sliderrelief="flat", highlightbackground="#2d2d2d")
brilho_scale.set(100)
brilho_scale.pack(pady=5)

temp_label = tk.Label(janela, text="Temperatura de Cor (0 a 255)", **status_style)
temp_label.pack(pady=(20, 5))

temp_scale = tk.Scale(janela, from_=0, to=255, orient="horizontal", length=250, command=ajustar_temperatura,
                      fg="white", bg="#2d2d2d", troughcolor="#555", sliderrelief="flat", highlightbackground="#2d2d2d")
temp_scale.set(100)  
temp_scale.pack(pady=5)

# Status
status_label = tk.Label(janela, text="Status: Aguardando comando", **status_style)
status_label.pack(pady=20)

janela.withdraw()

import threading
threading.Thread(target=criar_icone_bandeja, daemon=True).start()

janela.mainloop()
