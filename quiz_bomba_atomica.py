import pygame
import sys
import time
import random
import json

pygame.init()

# Configurações de Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo da Bomba Nuclear")

# Carregar as imagens de fundo
background_image = pygame.image.load('assets/fundo_informacoes.jpg')
menu_background = pygame.image.load('assets/imagem_fundo1.jpg')  # Substitua pelo nome do arquivo da imagem do menu
game_background = pygame.image.load('assets/imagem_fundo2.jpg')  # Substitua pelo nome do arquivo da imagem do jogo
difficulty_background = pygame.image.load('assets/fundo_dificuldade.jpg')  # Novo fundo para a tela de dificuldade

# Redimensiona as imagens para cobrir toda a tela
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
difficulty_background = pygame.transform.scale(difficulty_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Música e sons
menu_music = "assets/musica1.mp3"
game_easy_music = "assets/facil.mp3"
game_hard_music = "assets/dificil.mp3"
correct_sound = pygame.mixer.Sound("assets/certo.mp3")
wrong_sound = pygame.mixer.Sound("assets/errado.mp3")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonte 
font = pygame.font.SysFont("Comic Sans MS", 30)  # Tamanho 30
title_font = pygame.font.SysFont("Comic Sans MS", 40)  # Tamanho 40

# Definir uma margem extra
OPTIONS_Y_OFFSET = 50  

# Função para tocar música
current_music = None  

def play_music(file, loop=True):
    global current_music
    if current_music != file: 
        pygame.mixer.music.stop()  # Para a música atual
        pygame.mixer.music.load(file) 
        pygame.mixer.music.play(-1 if loop else 0)  
        current_music = file  # Atualiza a música atual


# Função para desenhar o botão
def draw_button(text, x, y, w, h, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Verifica se o clique está dentro da área do botão
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, (100, 100, 255), (x, y, w, h))  # Quando o mouse está sobre o botão
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))  # Quando o mouse não está sobre o botão

    # Renderiza o texto dentro do botão
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)

# Função de ação quando pressionado o botão "Começar"
def start_game():
    choose_difficulty()


# Função para exibir o menu principal
def main_menu():
    play_music(menu_music)
    while True:
        screen.blit(menu_background, (0, 0))  # Coloca o fundo do menu na tela

        # Título
        title_surface = title_font.render("Jogo da Bomba Nuclear", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Botões de Menu
        draw_button("Começar", 250, 200, 300, 60, GREEN, start_game)
        draw_button("Informações", 250, 300, 300, 60, GREEN, show_info)
        draw_button("Sair", 250, 400, 300, 60, GREEN, quit_game)

        # Atualiza a tela
        pygame.display.flip()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Começar
                    start_game()
                elif event.key == pygame.K_i:  # Informações
                    show_info()
                elif event.key == pygame.K_ESCAPE:  # Sair
                    quit_game()


# Tela de Escolha de Dificuldade
def choose_difficulty():
    play_music(menu_music)
    while True:
        screen.blit(difficulty_background, (0, 0))  # Coloca o fundo da tela de dificuldade

        # Título
        title_surface = font.render("Escolha a Dificuldade", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Texto de instrução
        instruction_text = font.render("Pressione '1' para Fácil", True, BLACK)
        instruction_text1 = font.render("Pressione '2' para Difícil", True, BLACK)
        instruction_text2 = font.render("Pressione 'Esc' para Voltar", True, BLACK)

        # Desenhando os retângulos cinzas atrás do texto
        rect_width = max(instruction_text.get_width(), instruction_text1.get_width(), instruction_text2.get_width()) + 20
        rect_height = 40

        # Retângulos atrás de cada linha de instrução
        pygame.draw.rect(screen, GRAY, (50 - 10, 200 - 5, rect_width, rect_height))  # Retângulo para o primeiro texto
        pygame.draw.rect(screen, GRAY, (50 - 10, 250 - 5, rect_width, rect_height))  # Retângulo para o segundo texto
        pygame.draw.rect(screen, GRAY, (50 - 10, 300 - 5, rect_width, rect_height))  # Retângulo para o terceiro texto

        # Desenhando o texto na tela
        screen.blit(instruction_text, (50, 200))
        screen.blit(instruction_text1, (50, 250))
        screen.blit(instruction_text2, (50, 300))

        # Atualiza a tela
        pygame.display.flip()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Modo Fácil
                    easy_mode()
                elif event.key == pygame.K_2:  # Modo Difícil
                    hard_mode()
                elif event.key == pygame.K_ESCAPE:  # Voltar
                    main_menu()

# Função de exibição da tela de informações
def show_info():
    info_screen()

# Função de tela de informações
def info_screen():
    while True:
        screen.blit(background_image, (0, 0)) # Fundo branco para informações

        # Título
        title_surface = font.render("Informações sobre o Jogo", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Descrição
        description = [
            "O objetivo do jogo é responder perguntas sobre a bomba nuclear.",
            "Cada pergunta tem um tempo limite para ser respondida.",
            "As respostas corretas dão pontos e as erradas, não."
        ]

        # Ajuste de posicionamento e fundo
        y_offset = 150
        max_line_width = SCREEN_WIDTH - 100  # Largura máxima para o texto
        explanation_lines = wrap_text("\n".join(description), max_line_width)

        # Calcula a altura do retângulo cinza
        rect_width = max([font.size(line)[0] for line in explanation_lines]) + 40
        rect_height = len(explanation_lines) * 40 + 20
        pygame.draw.rect(screen, GRAY, (50 - 10, y_offset - 5, rect_width, rect_height))  # Fundo cinza

        # Exibe o texto
        for i, line in enumerate(explanation_lines):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (50, y_offset + i * 40))

        # Texto para instruções
        instruction_text = font.render("Pressione 'Esc' para Voltar", True, BLACK)
        screen.blit(instruction_text, (50, y_offset + len(explanation_lines) * 40 + 20))

        # Atualiza a tela
        pygame.display.flip()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Voltar
                    main_menu()

# Função para encerrar o jogo
def quit_game():
    pygame.quit()
    sys.exit()

# Função para exibir o quiz
# Função para rodar o quiz com seleção aleatória de perguntas
def run_quiz(questions, mode_music):
    play_music(mode_music)  # Música do modo selecionado
    global current_question, score

    # Seleciona 5 perguntas aleatórias
    selected_questions = random.sample(questions, 5)
    current_question = 0
    score = 0

    while current_question < len(selected_questions):
        screen.blit(game_background, (0, 0))  # Coloca o fundo do jogo na tela
        start_time = time.time()

        # Pergunta atual
        question_data = selected_questions[current_question]
        question_text = question_data["question"]
        options = question_data["options"]
        correct_option = question_data["correct"]

        answered = False
        while not answered:
            # Tempo restante
            elapsed_time = time.time() - start_time
            remaining_time = max(0, time_limit - int(elapsed_time))

            # Limpa a tela
            screen.blit(game_background, (0, 0))  # Mantém o fundo do jogo

            # Define a largura máxima permitida para o texto
            max_width = SCREEN_WIDTH - 100  # 100 de margem total (50 de cada lado)

            # Quebra o texto em linhas
            question_lines = wrap_text(question_text, max_width)

            # Renderiza cada linha da pergunta
            for i, line in enumerate(question_lines):
               question_surface = font.render(line, True, BLACK)
               screen.blit(question_surface, (50, 50 + i * 40))  # Ajusta a posição vertical


            # Renderiza as opções
            for i, option in enumerate(options):
                color = GRAY
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                # Coordenadas do botão
                x, y, w, h = 100, 150 + i * 70, 600, 50
                y += OPTIONS_Y_OFFSET
                # Checa se o mouse está sobre o botão
                if x + w > mouse[0] > x and y + h > mouse[1] > y:
                    color = (0, 200, 0)
                    if click[0] == 1:
                        answered = True
                        if i == correct_option:
                            score += 1
                            correct_sound.play()
                            feedback("Certo!", GREEN, question_data["explanation"])
                        else:
                            wrong_sound.play()
                            feedback("Errado!", RED, f"Resposta correta: {options[correct_option]}. {question_data['explanation']}")
                        current_question += 1

                pygame.draw.rect(screen, color, (x, y, w, h))

                # Texto da opção
                # Quebra a opção em linhas
                option_lines = wrap_text(option, w - 20)  # Largura do botão menos margem

                # Renderiza cada linha da opção
                for j, line in enumerate(option_lines):
                   option_surface = font.render(line, True, BLACK)
                   screen.blit(option_surface, (x + 10, y + 10 + j * 30))  # Ajusta a posição vertical


            # Exibe o tempo restante em branco
            timer_surface = font.render(f"Tempo restante: {remaining_time}s", True, WHITE)
            screen.blit(timer_surface, (50, 500))  # Coloca o tempo mais embaixo na tela

            # Se o tempo acabar, avança automaticamente
            if remaining_time <= 0:
                wrong_sound.play()
                feedback("Tempo esgotado!", RED, f"Resposta correta: {options[correct_option]}. {question_data['explanation']}")
                answered = True
                current_question += 1

            # Atualiza a tela
            pygame.display.flip()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Continuar
                        answered = True
                        current_question += 1

    # Tela de finalização
    end_quiz()


# Perguntas do Modo Fácil
with open("assets/easy_questions.json", encoding="utf8") as easy_questions_json:
    easy_questions = json.loads(easy_questions_json.read())

# Perguntas do Modo Difícil
with open("assets/hard_questions.json", encoding="utf8") as hard_questions_json:
    hard_questions = json.loads(hard_questions_json.read()) 

# Variáveis globais do quiz
current_question = 0
score = 0
time_limit = 10  # Tempo em segundos para responder cada pergunta

# Função para exibir a tela final do quiz
def end_quiz():
    global score
    while True:
        screen.blit(background_image, (0, 0))  # Fundo da tela de finalização

        # Título
        title_surface = title_font.render("Quiz Finalizado!", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Pontuação final
        score_text = font.render(f"Sua pontuação: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(score_text, score_rect)

        # Botões
        draw_button("Voltar ao Menu", 250, 250, 300, 60, GREEN, main_menu)
        draw_button("Reiniciar Quiz", 250, 400, 300, 60, GREEN, restart_game)

        # Atualiza a tela
        pygame.display.flip()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()


# Função para reiniciar o quiz
def restart_game():
    global score, current_question
    score = 0
    current_question = 0
    choose_difficulty()

# Função para iniciar o Modo Fácil
def easy_mode():
    run_quiz(easy_questions,game_easy_music)

# Função para iniciar o Modo Difícil
def hard_mode():
    run_quiz(hard_questions,game_hard_music)

# Feedback para a resposta correta ou errada
def feedback(message, color, explanation):
    running = True
    max_line_width = SCREEN_WIDTH - 100  # Largura máxima do texto na tela
    explanation_lines = wrap_text(explanation, max_line_width)

    while running:
        screen.blit(game_background, (0, 0))  # Fundo para a tela de explicações

        # Desenhando o retângulo cinza atrás da mensagem e explicação
        message_width = font.size(message)[0]
        explanation_width = max([font.size(line)[0] for line in explanation_lines])
        rect_width = max(message_width, explanation_width) + 40
        rect_height = 100 + len(explanation_lines) * 40
        pygame.draw.rect(screen, GRAY, (40, 80, rect_width, rect_height))  # Retângulo cinzento no fundo

        # Mensagem de Feedback
        message_surface = font.render(message, True, color)
        screen.blit(message_surface, (50, 100))

        # Exibição da explicação
        for i, line in enumerate(explanation_lines):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (50, 150 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Continuar após a resposta
                    running = False

# Função para quebrar o texto em várias linhas
def wrap_text(text, max_width):
    """Quebra o texto em várias linhas de acordo com a largura máxima."""
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        # Verifica se adicionar a palavra atual excede o tamanho máximo
        if font.size(current_line + word)[0] > max_width:
            lines.append(current_line.strip())  # Adiciona a linha completa
            current_line = word + " "  # Começa uma nova linha
        else:
            current_line += word + " "
    
    lines.append(current_line.strip())  # Adiciona a última linha
    return lines

main_menu()