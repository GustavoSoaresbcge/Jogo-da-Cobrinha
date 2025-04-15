import pygame
from random import randint

# Inicializa o Pygame
pygame.init()

# Cores gerais
preto = (0, 0, 0)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
dourado = (255, 215, 0)
branco = (255, 255, 255)

# Tamanho da tela e blocos
largura = 800
altura = 600
bloco = 20

# Fonte
fonte = pygame.font.SysFont('Arial', 35)
fonte_pequena = pygame.font.SysFont('Arial', 20)

# Tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobrinha')

# Relógio
clock = pygame.time.Clock()
speed = 15


# Funções
def mensagem(msg, cor, x, y, pequena=False):
    if pequena:
        texto = fonte_pequena.render(msg, True, cor)
        # Omitindo pequena == True:
    else:
        texto = fonte.render(msg, True, cor)
    tela.blit(texto, [x, y])
    # Transformou o Str numa superfície (imagem) pronta pro Pygame exibir e
    # o Block Transfer (Blit) coloca uma superície sobre a outra


def desenha_cobra(lista):
    for BLOCO in lista:
        pygame.draw.rect(tela, verde, [BLOCO[0], BLOCO[1], bloco, bloco])


def gerar_maca():
    x = randint(0, (largura - bloco) // bloco) * bloco
    y = randint(2, (altura - bloco) // bloco) * bloco
    return [x, y]


def cor_apple():
    if randint(1, 100) <= 30: # 30% de chance
        type_apple = 'dourada'
    else:
        type_apple = 'comum'
    return type_apple


def mensagem_intermitente(texto):
    tempo = pygame.time.get_ticks()
    if (tempo // 500) % 2 == 0:
        mensagem(texto, branco, largura//2 - 80, altura - 40, pequena=True)


# Jogo principal
def jogo():
    recorde = 0
    jogando = True

    while jogando:
        game_over = False
        start = False

        x = largura // 2
        y = altura // 2
        x_mudar = 0
        y_mudar = 0

        cobra = []
        tamanho = 1
        pontuacao = 0

        maca = gerar_maca()
        type_apple = cor_apple()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    jogando = False
                elif event.type == pygame.KEYDOWN:
                    if not start:
                        if event.key == pygame.K_LEFT:
                            x_mudar = -bloco
                            y_mudar = 0
                            start = True
                        elif event.key == pygame.K_RIGHT:
                            x_mudar = bloco
                            y_mudar = 0
                            start = True
                        elif event.key == pygame.K_UP:
                            y_mudar = -bloco
                            x_mudar = 0
                            start = True
                        elif event.key == pygame.K_DOWN:
                            y_mudar = bloco
                            x_mudar = 0
                            start = True
                    else:
                        if event.key == pygame.K_LEFT and x_mudar == 0:
                            x_mudar = -bloco
                            y_mudar = 0
                        elif event.key == pygame.K_RIGHT and x_mudar == 0:
                            x_mudar = bloco
                            y_mudar = 0
                        elif event.key == pygame.K_UP and y_mudar == 0:
                            y_mudar = -bloco
                            x_mudar = 0
                        elif event.key == pygame.K_DOWN and y_mudar == 0:
                            y_mudar = bloco
                            x_mudar = 0

            if not start:
                tela.fill(preto)
                if type_apple == 'dourada':
                    cor_maca = dourado
                else:
                    cor_maca = vermelho
                pygame.draw.rect(tela, cor_maca, [maca[0], maca[1], bloco, bloco])
                pygame.draw.rect(tela, verde, [x, y, bloco, bloco])
                mensagem_intermitente('Ande para começar')
                pygame.display.update()
                continue

            x += x_mudar
            y += y_mudar

            # Checa colisão com as paredes
            if x < 0 or x >= largura or y < 0 or y >= altura:
                game_over = True

            tela.fill(preto)

            # Maçã
            if type_apple == 'dourada':
                cor_maca = dourado
            else:
                cor_maca = vermelho
            pygame.draw.rect(tela, cor_maca, [maca[0], maca[1], bloco, bloco])

            # Cobra
            cabeca = [x, y]
            cobra.append(cabeca)
            if len(cobra) > tamanho:
                del cobra[0]

            # Checando colisão com o corpo
            if cabeca in cobra[:-1]:
                game_over = True

            desenha_cobra(cobra)
            pygame.display.update()

            # Pegou maçã
            if x == maca[0] and y == maca[1]:
                if type_apple == 'dourada':
                    pontuacao += 2
                    tamanho += 2
                else:
                    pontuacao += 1
                    tamanho += 1

                maca = gerar_maca()
                type_apple = cor_apple()

            clock.tick(speed)

        # Atualiza recorde
        if pontuacao > recorde:
            recorde = pontuacao

        # Fim de jogo (aguardar reinício)
        aguardar_reinicio = True
        while aguardar_reinicio and jogando:
            tela.fill(preto)
            mensagem(f'Pontuação: {pontuacao}', branco, largura // 2 - 150, altura // 2 - 60)
            mensagem(f'Recorde pessoal: {recorde}', branco, largura // 2 - 150, altura // 2 - 20)
            mensagem_intermitente('Ande para começar')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jogando = False
                    aguardar_reinicio = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        aguardar_reinicio = False
    pygame.quit()
    quit()


# Inicia o jogo
jogo()


