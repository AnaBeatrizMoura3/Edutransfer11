import pygame
import sys
import math
import random


pygame.init()

# Configurações da Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulador de Lançamento de Bomba")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Carregar imagens
plane_img = pygame.image.load("assets/aviao.png")  # Substitua com o caminho correto da imagem do avião
plane_img = pygame.transform.scale(plane_img, (100, 40))

bomb_img = pygame.image.load("assets/bomba.jpg")  # Substitua com o caminho correto da imagem da bomba
bomb_img = pygame.transform.scale(bomb_img, (20, 20))

background_img = pygame.image.load("assets/imagem_fundo1.jpg")  # Substitua com o caminho do fundo desejado
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Carregar fundo personalizado para a tela de informações
info_background_img = pygame.image.load("assets/imagem_fundo2.jpg")
info_background_img = pygame.transform.scale(info_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Carregar sons
plane_sound = pygame.mixer.Sound("assets/aviao.mp3")  # Som do avião
explosion_sound = pygame.mixer.Sound("assets/explosao.mp3")  # Som da explosão
background_music = "assets/musica1.mp3"  # Música de fundo da tela de informações

# Constantes de Física
g = 9.81  # Aceleração da gravidade (m/s²)

# Função para calcular o tempo de voo e o alcance horizontal
def calculate_time_and_range(vx, y0):
    t_total = math.sqrt(2 * y0 / g)  # Tempo até atingir o solo
    alcance = vx * t_total  # Alcance horizontal
    return t_total, alcance

# Função para calcular a trajetória parabólica
def calculate_trajectory(vx, y0, scale, release_x):
    t = 0
    dt = 0.05
    trajectory = []
    x = release_x
    y = y0
    vy = 0  # Velocidade inicial vertical é 0 (movimento horizontal no início)

    while y > 0:
        # Atualiza a posição horizontal (movimento uniforme)
        x += vx * dt
        # Atualiza a posição vertical (movimento acelerado devido à gravidade)
        vy += g * dt
        y -= vy * dt  # A posição vertical é alterada pela velocidade vertical

        trajectory.append((x * scale, SCREEN_HEIGHT - y * scale))  # Armazena a posição da trajetória
        t += dt

    return trajectory

# Função para desenhar o avião e a bomba
def draw_airplane_and_bomb(plane_x, plane_y, bomb_x, bomb_y, bomb_released):
    screen.blit(plane_img, (plane_x, plane_y))
    if not bomb_released:
        # A bomba está junto ao avião antes de ser solta
        bomb_x = plane_x + plane_img.get_width() // 2
        bomb_y = plane_y + plane_img.get_height()
    screen.blit(bomb_img, (bomb_x - bomb_img.get_width() // 2, bomb_y))

# Função para desenhar a explosão
def draw_explosion(x, y):
    for _ in range(100):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        pygame.draw.circle(screen, random.choice([pygame.Color('red'), pygame.Color('yellow')]), (int(x + vx * 10), int(y + vy * 10)), 3)

# Função para a tela inicial
def show_start_screen():
    font = pygame.font.SysFont("Arial", 24)
    screen.blit(info_background_img, (0, 0))

    title_text = font.render("Simulador de Lançamento de Bomba", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    instructions_text = [
        "Bem-vindo ao simulador de lançamento de bomba!",
        "Use as caixas de entrada para definir a velocidade inicial e a altura.",
        "Pressione 'Enter' para iniciar o lançamento.",
        "O avião vai se mover para frente e soltar a bomba.",
        "A trajetória da bomba será calculada com base nas fórmulas apresentadas.",
        "Fórmula do alcance: alcance = v_x * t_total",
        "Fórmula do tempo total: t_total = sqrt(2 * altura / g)"
    ]
    info_rect = pygame.Rect(50, 150, SCREEN_WIDTH - 100, 250)
    pygame.draw.rect(screen, GRAY, info_rect)

    for i, line in enumerate(instructions_text):
        text = font.render(line, True, BLACK)
        screen.blit(text, (50, 150 + i * 30))
    
    start_text_rect = pygame.Rect(220, 480, 360, 60)
    pygame.draw.rect(screen, GRAY, start_text_rect)

    start_text = font.render("Pressione qualquer tecla para começar", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT - 100))

    pygame.display.flip()

    # Reproduzir música de fundo enquanto na tela de informações
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1, 0.0)  # Reproduzir em loop

    # Esperar o usuário pressionar uma tecla para iniciar
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_input = False
                pygame.mixer.music.stop()  # Parar a música de fundo ao iniciar o simulador
                break

# Função do simulador
def simulator():
    user_text_vx = ""
    user_text_y0 = ""
    active_vx = False
    active_y0 = False
    font = pygame.font.SysFont("Arial", 24)
    plane_x = 50
    plane_y = 250  # Posição ajustada para mais acima
    bomb_released = False
    bomb_x = 0
    bomb_y = 0
    trajectory = []
    plane_moving = False
    alcance = 0
    t_total = 0  # Variável para armazenar o tempo total
    scale = 1  # Escala para ajustar a altura no display
    error_message = ""

    while True:
        screen.blit(background_img, (0, 0))  # Desenha o fundo

        # Exibe o texto explicativo
        text_vx = font.render("Velocidade inicial horizontal (m/s):", True, BLACK)
        screen.blit(text_vx, (50, 50))

        text_y0 = font.render("Altura inicial (m):", True, BLACK)
        screen.blit(text_y0, (50, 150))

        # Caixa de entrada para velocidade inicial
        input_box_vx = pygame.Rect(50, 100, 200, 50)
        pygame.draw.rect(screen, BLACK, input_box_vx, 2)

        # Caixa de entrada para altura inicial
        input_box_y0 = pygame.Rect(50, 200, 200, 50)
        pygame.draw.rect(screen, BLACK, input_box_y0, 2)

        # Exibir o alcance e o tempo total (se calculados)
        if bomb_released:
            alcance_rect = pygame.Rect(50, 300, 200, 60)
            pygame.draw.rect(screen, GRAY, alcance_rect)
            alcance_text = font.render(f"Alcance: {alcance:.2f} m", True, BLACK)
            screen.blit(alcance_text, (50, 300))

            # Exibir a fórmula para calcular o alcance
        formula_rect = pygame.Rect(50, 350, 250, 60)
        pygame.draw.rect(screen, GRAY, formula_rect)
        formula_text = font.render("Fórmula do alcance:", True, BLACK)
        screen.blit(formula_text, (50, 350))

        formula_content = font.render("alcance = v_x * t_total", True, BLACK)
        screen.blit(formula_content, (50, 380))

        # Exibir a fórmula para calcular t_total
        t_total_formula_rect = pygame.Rect(50, 420, 250, 60)
        pygame.draw.rect(screen, GRAY, t_total_formula_rect)

        t_total_formula_text = font.render("Fórmula do tempo total:", True, BLACK)
        screen.blit(t_total_formula_text, (50, 420))

        t_total_formula_content = font.render("t_total = sqrt(2 * altura / g)", True, BLACK)
        screen.blit(t_total_formula_content, (50, 450))
        t_total_rect = pygame.Rect(50, 480, 250, 60)
            
        pygame.draw.rect(screen, GRAY, t_total_rect)
        t_total_text = font.render(f"Tempo total: {t_total:.2f} s", True, BLACK)
        screen.blit(t_total_text, (50, 500))
        
        # Exibir mensagem de erro
        if error_message:
            error_surface = font.render(error_message, True, RED)
            screen.blit(error_surface, (50, 400))

        # Processamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_vx.collidepoint(event.pos):
                    active_vx = True
                    active_y0 = False
                elif input_box_y0.collidepoint(event.pos):
                    active_y0 = True
                    active_vx = False
                else:
                    active_vx = active_y0 = False
            
            if event.type == pygame.KEYDOWN:
                if active_vx:
                    if event.key == pygame.K_RETURN:
                        continue
                    elif event.key == pygame.K_BACKSPACE:
                        user_text_vx = user_text_vx[:-1]
                    else:
                        user_text_vx += event.unicode
                elif active_y0:
                    if event.key == pygame.K_RETURN:
                        try:
                            vx = float(user_text_vx)
                            y0 = float(user_text_y0)
                            if vx <= 0 or y0 <= 0:
                                error_message = "Velocidade e altura devem ser maiores que 0!"
                                continue

                            # Remove mensagem de erro e escala
                            error_message = ""
                            scale = SCREEN_HEIGHT / (y0 * 1.5)  # Ajusta a escala para o tamanho da tela

                            # Calcula a trajetória, alcance e tempo total
                            bomb_x = plane_x + 40
                            bomb_y = SCREEN_HEIGHT - y0 * scale
                            t_total, alcance = calculate_time_and_range(vx, y0)
                            trajectory = calculate_trajectory(vx, y0, scale, plane_x + 50)
                            bomb_released = True
                            plane_moving = True
                            plane_sound.play()  # Tocar o som do avião assim que o avião começa a se mover
                        except ValueError:
                            error_message = "Insira valores numéricos válidos!"
                    elif event.key == pygame.K_BACKSPACE:
                        user_text_y0 = user_text_y0[:-1]
                    else:
                        user_text_y0 += event.unicode

        # Exibir os textos que o utilizador está a digitar
        txt_surface_vx = font.render(user_text_vx, True, BLACK)
        screen.blit(txt_surface_vx, (input_box_vx.x + 5, input_box_vx.y + 5))

        txt_surface_y0 = font.render(user_text_y0, True, BLACK)
        screen.blit(txt_surface_y0, (input_box_y0.x + 5, input_box_y0.y + 5))

        # Atualiza a posição do avião com base na velocidade
        if plane_moving:
            plane_speed = vx / 10  # Ajuste a velocidade do avião proporcional à velocidade de lançamento da bomba
            plane_x += plane_speed  # O avião se move com base na velocidade ajustada
            if bomb_released and trajectory:
                bomb_x, bomb_y = trajectory.pop(0)  # A bomba segue a trajetória

            elif bomb_released and not trajectory:
                draw_explosion(bomb_x, SCREEN_HEIGHT - 10)
                explosion_sound.play()  # Tocar o som da explosão
                plane_sound.stop()  # Parar o som do avião quando a bomba atinge o solo
                pygame.display.flip()
                pygame.time.wait(1000)
                bomb_released = False
                plane_moving = False  # Para o avião
                plane_x = 50  # Reinicia o avião na posição inicial

        draw_airplane_and_bomb(plane_x, plane_y, bomb_x, bomb_y, bomb_released)

        # Desenha a trajetória até o ponto atual
        if trajectory:
            for point in trajectory:
                pygame.draw.circle(screen, (0, 255, 0), (int(point[0]), int(point[1])), 3)

        pygame.display.flip()

# Iniciar o simulador
show_start_screen()
simulator()
