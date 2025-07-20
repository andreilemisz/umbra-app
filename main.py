import tkinter as tk
from tkinter import PhotoImage
import random
import threading
import time

class IdleCharacter:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove a barra de título
        self.root.attributes('-topmost', True)  # Mantém no topo
        self.root.wm_attributes('-transparentcolor', 'white')  # Define cor transparente
        
        # Posição inicial
        self.x = 100
        self.y = 600
        
        # Frases de motivação
        self.messages = [
            "Muito bom! Continue assim!",
            "Você está indo bem!",
            "Um passo de cada vez!",
            "Foco no objetivo!",
            "Você consegue!",
            "Ótimo progresso!"
        ]
        
        # Carrega a imagem do personagem (substitua pelo seu arquivo)
        try:
            self.character_img = PhotoImage(file="character.png")
            self.character = tk.Label(root, image=self.character_img, bg='white')
        except:
            # Fallback se a imagem não carregar
            self.character = tk.Label(root, text="(^-^)", bg='white', font=('Arial', 24))
        
        self.character.pack()
        
        # Balão de mensagem (inicialmente invisível)
        self.message_label = tk.Label(root, text="", bg='light yellow', fg='black', relief='solid', borderwidth=1, wraplength=150, font=('Arial', 16))
        
        # Configura a janela
        self.root.geometry(f"200x200+{self.x}+{self.y}")
        self.root.config(bg='white')
        
        # Permove mover o personagem
        self.character.bind("<Button-1>", self.start_move)
        self.character.bind("<B1-Motion>", self.on_move)
        self.character.bind("<ButtonRelease-1>", self.stop_move)
        
        self.moving = False
        
        # Inicia o loop de mensagens
        self.show_message_loop()
    
    def start_move(self, event):
        self.moving = True
        self.offset_x = event.x
        self.offset_y = event.y
    
    def on_move(self, event):
        if self.moving:
            x = self.root.winfo_x() + event.x - self.offset_x
            y = self.root.winfo_y() + event.y - self.offset_y
            self.root.geometry(f"+{x}+{y}")
    
    def stop_move(self, event):
        self.moving = False
        
    def show_message(self):
        message = random.choice(self.messages)
        self.message_label.config(text=message)
        
        # Posiciona o balão acima do personagem
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.message_label.place(x=80, y=10)
        self.message_label.lift()
        
        # Mostra por 10 segundos
        self.message_label.after(10000, self.message_label.place_forget)
    
    def show_message_loop(self):
        self.show_message()
        # Agenda a próxima mensagem para 15 minutos (900000 ms)
        self.root.after(10000, self.show_message_loop)
        # self.root.after(900000, self.show_message_loop)

def main():
    root = tk.Tk()
    root.geometry("100x100")
    app = IdleCharacter(root)
    root.mainloop()

if __name__ == "__main__":
    main()