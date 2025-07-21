import tkinter as WidgetMaker
import random
import os
import sys

# Verifica se o script está sendo executado como um executável (por exemplo, criado com PyInstaller)
if getattr(sys, 'frozen', False):
    # Executando como .exe
    base_path = sys._MEIPASS
else:
    # Executando como script normal
    base_path = os.path.abspath(".")

caminho_imagem_personagem = os.path.join(base_path, "design", "personagem.png")

class UmbraIdle:
    def __init__(self, janela_widget):
        self.janela_widget = janela_widget
        
    def configuracao_inicial(self):
        # Instruções iniciais
        self.janela_widget.overrideredirect(True)  # Remove a barra de título
        self.janela_widget.attributes('-topmost', True)  # Mantém no topo
        self.janela_widget.wm_attributes('-transparentcolor', 'white')  # Define qual cor é a transparente

        # Posição inicial 
        # x é a posição horizontal e y é a posição vertical
        # A posição 0,0 é o canto superior esquerdo da tela
        # Os valores negativos são para cima e para a esquerda
        # Os valores positivos são para baixo e para a direita
        self.x = 100
        self.y = 600

        # Frame para o personagem
        self.frame_personagem = WidgetMaker.Frame(janela_widget, bg='white')
        self.frame_personagem.pack(expand=True, fill='both')

        # Carrega a imagem do personagem 
        try:
            self.imagem_personagem = WidgetMaker.PhotoImage(file=caminho_imagem_personagem)
            self.personagem = WidgetMaker.Label(self.frame_personagem, image=self.imagem_personagem, bg='white')
        except:
            self.personagem = WidgetMaker.Label(self.frame_personagem, text="(^-^)", bg='white', font=('Arial', 24))

        self.personagem.pack(expand=True)

        # Balão de mensagem (inicialmente invisível)
        self.balao_mensagem = WidgetMaker.Label(
            janela_widget, text="", bg='light yellow', fg='black',
            relief='solid', borderwidth=1, wraplength=150, font=('Arial', 16)
        )

        # Configura a janela
        self.janela_widget.geometry(f"200x200+{self.x}+{self.y}")
        self.janela_widget.config(bg='white')

        # Permite mover o personagem
        self.personagem.bind("<Button-1>", self.inicio_movimentacao_widget)
        self.personagem.bind("<B1-Motion>", self.durante_movimentacao_widget)
        self.personagem.bind("<ButtonRelease-1>", self.parando_movimentacao_widget)

        self.em_movimentacao = False
        
        # Permite fechar o app com Ctrl+W
        self.janela_widget.bind('<Control-w>', lambda event: self.janela_widget.destroy())

    def inicio_movimentacao_widget(self, event):
        self.em_movimentacao = True
        self.offset_x = event.x
        self.offset_y = event.y

    def durante_movimentacao_widget(self, event):
        if self.em_movimentacao:
            x = self.janela_widget.winfo_x() + event.x - self.offset_x
            y = self.janela_widget.winfo_y() + event.y - self.offset_y
            self.janela_widget.geometry(f"+{x}+{y}")

    def parando_movimentacao_widget(self, event):
        self.em_movimentacao = False

    def selecao_da_frase_motivacional(self):
        self.mensagens_motivacao = [
            "Muito bom! Continue assim!",
            "Você está indo bem!",
            "Um passo de cada vez!",
            "Foco no objetivo!",
            "Você consegue!",
            "Ótimo progresso!"
        ]
        return random.choice(self.mensagens_motivacao)

    def mostrar_mensagem(self):
        mensagem = self.selecao_da_frase_motivacional()
        self.balao_mensagem.config(text=mensagem)
        self.balao_mensagem.place_forget()

        # Atualiza o layout para garantir que o tamanho do balão está correto
        self.janela_widget.update_idletasks()

        char_x = self.frame_personagem.winfo_x()
        char_y = self.frame_personagem.winfo_y()
        char_width = self.frame_personagem.winfo_width()
        msg_width = self.balao_mensagem.winfo_reqwidth()

        x = char_x + (char_width // 2) - (msg_width // 2)
        y = char_y + 10

        self.balao_mensagem.place(x=x, y=y)
        self.balao_mensagem.lift()
        self.balao_mensagem.after(10000, self.balao_mensagem.place_forget)

    def mostrar_mensagem_loop(self):
        self.mostrar_mensagem()
        self.janela_widget.after(10000, self.mostrar_mensagem_loop)

if __name__ == "__main__":
    janela_widget = WidgetMaker.Tk()
    janela_widget.geometry("100x100")
    umbra_inicializada = UmbraIdle(janela_widget)
    
    # Configuração inicial da janela e do personagem
    umbra_inicializada.configuracao_inicial()

    # Iniciando o loop de mensagens
    janela_widget.after(5000, umbra_inicializada.mostrar_mensagem_loop)
    
    janela_widget.mainloop()