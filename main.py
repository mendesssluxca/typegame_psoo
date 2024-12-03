import pygame
import random
import sys
import sqlite3

# Inicializar o Pygame
pygame.init()

# Definir cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Dimensões da tela
WIDTH, HEIGHT = 500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Digitação Rápida")

# Fonte
font = pygame.font.Font(None, 36)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("ranking.db")
cursor = conn.cursor()

# Criar tabela de ranking, se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS ranking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    pontuacao INTEGER NOT NULL
)
""")
conn.commit()

# Palavras por fase
words_phase_1 = [
    "apple", "banana", "cat", "dog", "elephant", "fish", "guitar", "house", "ice", "jungle",
    "book", "cloud", "river", "snake", "train", "pencil", "flower", "plane", "chair", "bread"
]

words_phase_2 = words_phase_1 + [
    "kiwi", "lemon", "mouse", "night", "ocean", "parrot", "queen", "rose", "sun", "tree",
    "table", "castle", "garden", "forest", "bridge", "candle", "mirror", "basket", "shadow", "mountain"
]

words_phase_3 = words_phase_2 + [
    "universe", "vaccine", "water", "xylophone", "yellow", "zebra",
    "galaxy", "engine", "compass", "rainbow", "diamond", "volcano", "satellite", "emerald", "hurricane", "pyramid"
]

# Carregar ícone de coração
heart_image = pygame.image.load("assets/heart.png")  # Certifique-se de ter o arquivo "heart.png"
heart_image = pygame.transform.scale(heart_image, (40, 40))

# Variável global para pausa
is_paused = False

# Função para salvar pontuação no banco de dados
def save_score(name, score):
    cursor.execute("INSERT INTO ranking (nome, pontuacao) VALUES (?, ?)", (name, score))
    conn.commit()

# Função para desenhar a tela inicial
def draw_start_screen():
    screen.fill(WHITE)
    #titulo
    title_text = font.render("Jogo de Digitação Rápida", True, BLUE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    #botoes
    start_text = font.render("Clique para Iniciar o Jogo", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 50))

    ranking_text = font.render("Clique para Ver o Ranking", True, BLACK)
    screen.blit(ranking_text, (WIDTH // 2 - ranking_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

# Função para desenhar o ranking
def draw_ranking():
    screen.fill(WHITE)
    ranking_title = font.render("Ranking", True, BLUE)
    screen.blit(ranking_title, (WIDTH // 2 - ranking_title.get_width() // 2, 50))

    cursor.execute("SELECT nome, pontuacao FROM ranking ORDER BY pontuacao DESC LIMIT 5")
    players = cursor.fetchall()

    y_offset = 150
    for idx, (name, score) in enumerate(players):
        ranking_text = font.render(f"{idx + 1}. {name} - {score} pontos", True, BLACK)
        screen.blit(ranking_text, (50, y_offset))
        y_offset += 40

    back_text = font.render("Pressione ESC para voltar", True, RED)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 100))

    pygame.display.flip()

# Função para desenhar corações
def draw_hearts(hearts_left):
    # Apenas desenha os corações quando houver vidas restantes
    if hearts_left > 0:
        for i in range(hearts_left):
            screen.blit(heart_image, (10 + i * 50, 50))  # Posição do coração


# Função para desenhar a tela do jogo
def draw_screen(words, score, phase, user_input):
    screen.fill(WHITE)

    #fase atual
    phase_text = font.render(f"Fase: {phase}", True, BLACK)
    screen.blit(phase_text, (10, 10))

    #pontuação
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 200, 10))

    #palavras na tela
    for word in words:
        word_surface = font.render(word["text"], True, BLACK)
        screen.blit(word_surface, (word["x"], word["y"]))

    #entrada do jogador
    input_surface = font.render(f"Digite: {user_input}", True, RED)
    screen.blit(input_surface, (WIDTH // 2 - 100, HEIGHT - 50))

    
# Função para desenhar a tela de Game Over
def draw_game_over():
    screen.fill(WHITE)
    over_text = font.render("GAME OVER", True, RED)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 3))

    instruction_text = font.render("Pressione ESC para voltar ao menu", True, BLACK)
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

# Função para desenhar a tela de entrada do nome do usuário
def draw_username_screen(username):
    screen.fill(WHITE)
    prompt_text = font.render("Digite seu nome de usuário:", True, BLUE)
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 4))

    username_text = font.render(username, True, BLACK)
    screen.blit(username_text, (WIDTH // 2 - username_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

# Loop principal do jogo
def game_loop(username):
    global is_paused
    score = 0
    phase = 1
    words = []
    user_input = ""
    word_speed = 0.2
    word_interval = 2000
    last_word_time = pygame.time.get_ticks()
    hearts_left = 3

    while True:
        current_time = pygame.time.get_ticks()
        word_list = words_phase_1 if phase == 1 else words_phase_2 if phase == 2 else words_phase_3

        # Pausar o jogo
        if is_paused:
            pause_text = font.render("Jogo Pausado - Pressione '1' para continuar", True, RED)
            screen.fill(WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    is_paused = not is_paused
            continue

        if current_time - last_word_time > word_interval:
            new_word = {"text": random.choice(word_list), "x": random.randint(50, WIDTH - 150), "y": -50}
            words.append(new_word)
            last_word_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    save_score(username, score)
                    return
                elif event.key == pygame.K_1:
                    is_paused = not is_paused
                else:
                    user_input += event.unicode

        # Verificar automaticamente se a palavra foi digitada corretamente
        for word in words[:]:  # Itera sobre uma cópia para evitar problemas ao remover elementos
            if user_input.lower() == word["text"].lower():
                words.remove(word)
                score += 10
                user_input = ""  # Limpa o input do jogador
                break

        for word in words:
            word["y"] += word_speed
            if word["y"] > HEIGHT:
                words.remove(word)
                hearts_left -= 1
                if hearts_left == 0:
                    draw_game_over()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                save_score(username, score)
                                return

        # Lógica de fases e pontuação
        if score >= 50 and phase == 1:
            phase = 2
            word_speed = 0.4
            word_interval = 1500  # Intervalo mais rápido
        elif score >= 100 and phase == 2:
            phase = 3
            word_speed = 0.7
            word_interval = 1200  # Intervalo ainda mais rápido
        elif score >= 500 and phase == 3:
            # Exibir mensagem de vitória
            screen.fill(WHITE)
            victory_text = font.render("Parabéns! Você venceu!", True, BLUE)
            screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 3))
            instruction_text = font.render("Pressione ESC para voltar ao menu", True, BLACK)
            screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()

            # Aguardar entrada do jogador para encerrar
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        save_score(username, score)
                        return

        # Atualize a tela em uma única função
        screen.fill(WHITE)
        draw_screen(words, score, phase, user_input)  # Inclua elementos principais
        draw_hearts(hearts_left)  # Adicione os corações na tela
        pygame.display.flip()  # Atualize a tela apenas uma vez


# Função principal
def main():
    global is_paused
    clock = pygame.time.Clock()
    running = True
    username = ""
    state = "username" # Pode ser "username", "start", "game", "ranking"

  # Loop do jogo
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

# Tela de entrada de nome de usuário
            if state == "username":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username != "":
                        state = "start"
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                draw_username_screen(username)

            elif state == "start":
                # Tela inicial
                draw_start_screen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if HEIGHT // 2 - 50 <= mouse_y <= HEIGHT // 2 + 50:
                        state = "game"
                    elif HEIGHT // 2 + 50 <= mouse_y <= HEIGHT // 2 + 150:
                        state = "ranking"

            elif state == "ranking":
                draw_ranking()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "start"

            elif state == "game":
                game_loop(username)
                state = "start"

        clock.tick(60)

if __name__ == "__main__":
    main()
