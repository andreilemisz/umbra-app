import tkinter as WidgetMaker
import random
import os
import sys
from huggingface_hub import InferenceClient

# Verifica se o script está sendo executado como um executável (por exemplo, criado com PyInstaller)
if getattr(sys, 'frozen', False):
    # Executando como .exe
    base_path = sys._MEIPASS
else:
    # Executando como script normal
    base_path = os.path.abspath(".")

caminho_imagem_personagem = os.path.join(base_path, "design", "personagem.png")

api_key_path = os.path.join(base_path, "api_key.txt")
with open(api_key_path, "r") as f:
    api_key = f.read().strip()

client = InferenceClient(
    provider="featherless-ai",
    api_key=api_key,
)

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
        self.x = 110
        self.y = 500

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
        
        # Permite acionar função com Ctrl+F
        self.janela_widget.bind('<Control-f>', self.iniciar_chatbot)

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

    def iniciar_chatbot(self, event=None):
        # Eu coloquei para o chatbot abrir abaixo do widget principal
        # Depois eu posso transformar isso para colocar no centro da tela
        # Também não sei se gostei muito da ideia de ser uma caixa de texto
        # modelo tradicional, depois eu posso ver de fazer algo mais moderno
        # ou estilizado, mas por enquanto vou deixar assim para não atrasar o projeto
        
        # Calcula a posição atual do widget principal na tela
        self.janela_widget.update_idletasks()  # Garante que as posições estejam atualizadas
        x_atual = self.janela_widget.winfo_rootx()
        y_atual = self.janela_widget.winfo_rooty()
        altura_janela = self.janela_widget.winfo_height()

        # Cria uma nova janela (Toplevel) abaixo do widget principal
        chatbot_window = WidgetMaker.Toplevel(self.janela_widget)
        chatbot_window.title("Chatbot Umbra")
        # Posiciona a janela do chatbot logo abaixo do widget principal
        chatbot_window.geometry(f"200x120+{x_atual}+{y_atual + altura_janela + 10}")
        chatbot_window.resizable(False, False)

        # Label de instrução
        label = WidgetMaker.Label(chatbot_window, text="Digite sua mensagem para a Umbra:")
        label.pack(pady=(10, 0))

        # Campo de entrada de texto
        entry = WidgetMaker.Entry(chatbot_window, width=25)
        entry.pack(pady=5)

        # Label para mostrar a resposta
        resposta_label = WidgetMaker.Label(chatbot_window, text="", wraplength=180, justify="left")
        resposta_label.pack(pady=(5, 5))

        def enviar_mensagem():
            mensagem = entry.get()
            if mensagem.strip():
                completion = self.gerar_resposta(mensagem)
                resposta = completion.choices[0].message.content
                resposta_label.config(text=resposta)
                entry.delete(0, WidgetMaker.END)

        botao = WidgetMaker.Button(chatbot_window, text="Enviar", command=enviar_mensagem)
        botao.pack(pady=(0, 10))

        entry.focus_set()

    def gerar_resposta(self, mensagem_usuario):
        return client.chat.completions.create(
            model="PocketDoc/Dans-PersonalityEngine-V1.3.0-24b",
            temperature=0.1,
            max_tokens=50,
            messages=[
                {
                    "role": "system",
                    "content": "Você é uma fada chamada Umbra, que tem uma personalidade sábia, calma, e um pouco enigmática. Tente dar respostas curtas, mas com um tom incentivador e motivador. Use emojis para expressar emoções, mas não exagere. O nome da pessoa que você está conversando com é Andrei, um programador. ",
                },
                {
                    "role": "user",
                    "content": mensagem_usuario
                }
            ],
        )

if __name__ == "__main__":
    janela_widget = WidgetMaker.Tk()
    janela_widget.geometry("100x100")
    umbra_inicializada = UmbraIdle(janela_widget)
    
    # Configuração inicial da janela e do personagem
    umbra_inicializada.configuracao_inicial()

    # Iniciando o loop de mensagens
    janela_widget.after(5000, umbra_inicializada.mostrar_mensagem_loop)
    
    janela_widget.mainloop()