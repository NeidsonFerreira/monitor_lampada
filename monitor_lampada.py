import tkinter as tk
from tkinter import colorchooser
from colorsys import rgb_to_hsv, hsv_to_rgb

class LampControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Lâmpada")

        self.lamp_status = tk.BooleanVar(value=False)
        self.lamp_intensity = tk.DoubleVar(value=0.5)  # Agora, usaremos valores entre 0 e 1
        self.lamp_color = tk.StringVar(value="#FFFF00")  # Cor padrão amarela

        # Configuração do canvas para desenhar a lâmpada
        self.canvas = tk.Canvas(root, width=100, height=150)
        self.canvas.pack(pady=10)

        # Rótulo para exibir o status da lâmpada
        self.status_label = tk.Label(root, text="Status: Desligada", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        # Configuração dos botões
        self.create_button("Acender", self.turn_on)
        self.create_button("Apagar", self.turn_off)
        self.create_button("+ Intensidade", self.increase_intensity)
        self.create_button("- Intensidade", self.decrease_intensity)

        # Botão para escolher cor
        self.color_button = tk.Button(root, text="Escolher Cor", command=self.choose_color)
        self.color_button.pack(pady=10)

        # Botão OK para aplicar a nova cor
        self.ok_button = tk.Button(root, text="OK", command=self.apply_color)
        self.ok_button.pack(pady=10)

        # Inicializa a lâmpada
        self.update_lamp()

    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command)
        button.pack(pady=5)

    def update_lamp(self):
        # Remove objetos antigos do canvas
        self.canvas.delete("all")

        # Converte a cor para o formato RGB
        rgb_color = self.hex_to_rgb(self.lamp_color.get())

        # Ajusta a intensidade da cor
        adjusted_rgb = self.adjust_color_intensity(rgb_color, self.lamp_intensity.get())

        # Converte de volta para o formato hexadecimal
        adjusted_hex_color = self.rgb_to_hex(adjusted_rgb)

        # Desenha a lâmpada como uma elipse preenchida
        lamp_color = adjusted_hex_color if self.lamp_status.get() else "gray"
        self.canvas.create_oval(10, 10, 90, 90, fill=lamp_color, outline="black")

        # Atualiza o rótulo de status
        status_text = "Status: Ligada" if self.lamp_status.get() else "Status: Desligada"
        self.status_label.config(text=status_text)

    def turn_on(self):
        self.lamp_status.set(True)
        self.update_lamp()

    def turn_off(self):
        self.lamp_status.set(False)
        self.update_lamp()

    def increase_intensity(self):
        intensity = self.lamp_intensity.get()
        if intensity < 1.0:
            self.lamp_intensity.set(intensity + 0.1)
            self.update_lamp()

    def decrease_intensity(self):
        intensity = self.lamp_intensity.get()
        if intensity > 0.1:
            self.lamp_intensity.set(intensity - 0.1)
            self.update_lamp()

    def choose_color(self):
        color = colorchooser.askcolor(title="Escolher Cor")[1]
        if color:
            self.lamp_color.set(color)

    def apply_color(self):
        self.update_lamp()

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb_color):
        return "#{:02x}{:02x}{:02x}".format(*rgb_color)

    def adjust_color_intensity(self, rgb_color, intensity):
        h, s, v = rgb_to_hsv(rgb_color[0]/255.0, rgb_color[1]/255.0, rgb_color[2]/255.0)
        v = min(1.0, v * intensity)  # Ajusta o valor (brilho)
        r, g, b = hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

# Criação da instância do Tkinter
root = tk.Tk()
root.geometry("400x600")

# Criação da instância do aplicativo
app = LampControlApp(root)

# Inicia o loop principal do Tkinter
root.mainloop()
