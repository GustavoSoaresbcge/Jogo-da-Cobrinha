import pygame
from random import randint
# Criação do banco de dados com as tabelas
import sqlite3

conexao = sqlite3.connect('ranking.db')
cursor = conexao.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS ranking(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nickname TEXT NOT NULL UNIQUE,
pontos INTEGER NOT NULL)
''')

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
def tela_inicial(tela, largura, altura, fonte, cursor):
    nickname = ""
    digitando = True

    while digitando:
        tela.fill(preto)

        # Texto fixo
        mensagem("Digite seu nome:", branco, largura // 2 - 200, altura // 2 - 70)
        mensagem_intermitente("Confirme com Enter", largura // 2 + 50, altura // 2 + 40)
        mensagem("Máx. 10 caracteres!", branco, largura // 2 - 200, altura // 2 + 40, True)

        # Retângulo de entrada
        pygame.draw.rect(tela, branco, (largura // 2 - 200, altura // 2 - 20, 400, 50), 2)

        # Mostrar texto digitado
        mensagem(nickname, branco, largura // 2 - 190, altura // 2 - 10)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    nickname = nickname.strip()
                    if nickname == "":
                        # Buscar apelidos Anônimo já existentes
                        cursor.execute("SELECT nickname FROM ranking WHERE nickname LIKE 'Anônimo___'")
                        anonimos = cursor.fetchall()

                        numeros = []
                        for (apelido,) in anonimos:
                            try:
                                numero = int(apelido.replace("Anônimo", ""))
                                numeros.append(numero)
                            except ValueError:
                                continue

                        proximo = 1
                        while proximo in numeros:
                            proximo += 1

                        nickname = f"Anônimo{proximo:03}"

                    elif len(nickname) > 10:
                        nickname = ""
                        continue

                    digitando = False

                elif event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]

                elif len(nickname) < 20:
                    nickname += event.unicode

    return nickname


def adicionar(name, point):
    cursor.execute("""
    INSERT INTO ranking (nickname, pontos)
    VALUES (?, ?)""", (name, point))
    conexao.commit()

    # O rowid age para desempacotar as tuplas recebidas no fetchall
    cursor.execute("SELECT rowid, pontos FROM ranking ORDER BY pontos DESC")
    dados_ordenados = cursor.fetchall()
    if len(dados_ordenados) > 10: # Pega os IDs que estão além do top 10
        excedentes = dados_ordenados[10:]
        for (rowid, _) in excedentes: # _ age para suprir o pontos que foi passado com o rowid
            cursor.execute("DELETE FROM ranking WHERE rowid = ?", (rowid,))
        conexao.commit()
    # pprint.pprint(dados_ordenados)


def deletar_tudo():
    cursor.execute("DELETE FROM ranking")
    conexao.commit()


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


def mensagem_intermitente(texto, x=largura//2 - 80, y=altura - 40):
    tempo = pygame.time.get_ticks()
    if (tempo // 500) % 2 == 0:
        mensagem(texto, branco, x, y, pequena=True)


# Jogo principal
def main():
    recorde = 0
    jogando = True
    # Iniciar com a tela inicial
    nickname = tela_inicial(tela, largura, altura, fonte, cursor)

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
            cursor.execute("SELECT pontos FROM ranking WHERE nickname=?", (nickname,))
            existe = cursor.fetchone()
            # Se não existir vai retornar Null e adicionar normal
            if existe:
                # Se já existe, e o novo ponto for maior, atualiza
                if pontuacao > existe[0]:
                    cursor.execute("UPDATE ranking SET pontos=?"
                                   " WHERE nickname=?", (pontuacao, nickname))
                    conexao.commit()
            else:
                # Adiciona pontuação no banco de dados se conseguir entrar no ranking ou se tiver menos de 10 itens
                cursor.execute("SELECT nickname, pontos FROM ranking ORDER BY pontos DESC")
                dados_ordenados = cursor.fetchall()
                if len(dados_ordenados) < 10 or (len(dados_ordenados) > 0 and pontuacao > dados_ordenados[-1][1]):
                    adicionar(nickname, pontuacao)
                    conexao.commit()

        # Fim de jogo (aguardar reinício)
        aguardar_reinicio = True
        while aguardar_reinicio and jogando:
            tela.fill(preto)
            mensagem(f'Pontuação: {pontuacao}', branco, largura // 2 - 150, altura // 2 - 60)
            mensagem(f'Recorde pessoal: {recorde}', branco, largura // 2 - 150, altura // 2 - 20)
            mensagem('Aperte r para visualizar o Ranking', branco, largura // 2 - 150, altura // 2 + 20, pequena=True)
            mensagem_intermitente('Ande para começar')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jogando = False
                    aguardar_reinicio = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        aguardar_reinicio = False

                    # Mostrar Ranking do banco de dados apertando r pra visualizar e sair
                    elif event.key == pygame.K_r:
                        show_ranking = True
                        while show_ranking:
                            for evento in pygame.event.get():
                                if evento.type == pygame.QUIT:
                                    jogando = False
                                    aguardar_reinicio = False
                                    show_ranking = False
                                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                                    show_ranking = False

                            cursor.execute("SELECT nickname, pontos FROM ranking ORDER BY pontos DESC")
                            em_ordem = cursor.fetchall()
                            tela.fill(preto)
                            # Exibir cada linha do ranking
                            for i in range(len(em_ordem)):
                                texto = f"{i + 1}º {em_ordem[i][0]}{em_ordem[i][1]} pts"
                                pontinhos = '.' * (30 - len(texto.strip()))
                                new_texto = f"{i + 1}º {em_ordem[i][0]}{pontinhos}{em_ordem[i][1]} pts"
                                # Cada linha desce 40 pixels pra não sobrepor
                                mensagem(new_texto, branco, largura // 2 - 200, 80 + i * 40)

                            mensagem_intermitente('Pressione r para voltar')
                            pygame.display.update()

    cursor.close()
    conexao.close()
    pygame.quit()
    quit()


# Inicia o jogo
main()


