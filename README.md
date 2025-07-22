# umbra-app
Aplicativo para desktop de uma assistente virtual para lembretes de tarefas e motivação extra durante o dia

## milestone 1 - concluído!
- Executável .exe que lançe o aplicativo
- Personagem 100x100 na tela que pode ser movido
- Frases prontas que são escolhidas aleatoriamente em intervalos determinados de tempo
- Código refatorado

Obs: para criar o executável o código a rodar é:
pyinstaller --onefile --windowed --icon=design\personagem_ico.ico --add-data "design/personagem.png;design" --name umbra-app main.py --clean

## milestone 2
a desenvolver próximos passos

!! > atualizar o requirements.txt com novas bibliotecas
!! > chave da api está em documento separado, lembrar disso ao criar executável