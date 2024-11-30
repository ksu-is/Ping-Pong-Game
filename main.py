import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Paddle movement
class Paddle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 6

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if down and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Ball and Physics
class Ball:
    def __init__(self, x, y, radius, color):
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.color = color
        self.radius = radius
        self.x_speed = 5
        self.y_speed = 5

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def bounce(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.y_speed = -self.y_speed

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)

# Main menu
def main_menu():
    while True:
        screen.fill(BLACK)
        
        title_text = font.render("Pong Game", True, BLUE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        instructions_text = small_font.render(
            "Select players/difficulty level with keys to start.", True, WHITE)
        screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 - 80))
        
        control_text = small_font.render(
            "1 Player Mode: WASD | 2 Player Mode: WASD + Arrow Keys", True, WHITE)
        screen.blit(control_text, (WIDTH // 2 - control_text.get_width() // 2, HEIGHT // 2 - 40))
        
        player_choice_text = small_font.render("1 Player (Press 1) / 2 Player (Press 2)", True, WHITE)
        screen.blit(player_choice_text, (WIDTH // 2 - player_choice_text.get_width() // 2, HEIGHT // 2 + 20))
        
        difficulty_text = small_font.render("Easy (Press E) / Hard (Press H)", True, WHITE)
        screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, HEIGHT // 2 + 60))

        quit_text = small_font.render("Press Escape to Quit", True, WHITE)
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 1.5))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"  # Start the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_1:
                    return "1p"  # 1-player mode
                if event.key == pygame.K_2:
                    return "2p"  # 2-player mode
                if event.key == pygame.K_e:
                    return "easy"  # Easy difficulty
                if event.key == pygame.K_h:
                    return "hard"  # Hard difficulty

# 2-player mode
def game_loop_2p():
    paddle_width, paddle_height = 15, 100
    ball_radius = 10
    
    # Create paddles and ball
    left_paddle = Paddle(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height, WHITE)
    right_paddle = Paddle(WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height, WHITE)
    ball = Ball(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius, WHITE)
    
    left_score = 0
    right_score = 0

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        left_paddle.move(keys[pygame.K_w], keys[pygame.K_s])
        right_paddle.move(keys[pygame.K_UP], keys[pygame.K_DOWN])

        # Ball movement and collision
        ball.move()
        ball.bounce()

        if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
            ball.x_speed = -ball.x_speed

        # Score
        if ball.rect.left <= 0:
            right_score += 1
            ball.rect.center = (WIDTH // 2, HEIGHT // 2)
            ball.x_speed = -ball.x_speed
        if ball.rect.right >= WIDTH:
            left_score += 1
            ball.rect.center = (WIDTH // 2, HEIGHT // 2)
            ball.x_speed = -ball.x_speed

        # Draw paddles, ball, and score
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()

        score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        # Quit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return  

        pygame.display.update()

        clock.tick(60)

# 1-player mode
def game_loop_1p(difficulty):
    paddle_width, paddle_height = 15, 100
    ball_radius = 10
    
    # Create paddles and ball
    left_paddle = Paddle(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height, WHITE)
    right_paddle = Paddle(WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height, WHITE)
    ball = Ball(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius, WHITE)
    
    left_score = 0
    right_score = 0

    # Set speed based on difficulty
    if difficulty == "easy":
        ai_speed = 3  # Slow AI
    elif difficulty == "hard":
        ai_speed = 8  # Fast AI
    else:
        ai_speed = 5  # Default speed (medium)

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement (player controls left paddle only)
        keys = pygame.key.get_pressed()
        left_paddle.move(keys[pygame.K_w], keys[pygame.K_s])

        # AI movement (right paddle follows the ball)
        if right_paddle.rect.centery < ball.rect.centery:
            right_paddle.rect.y += ai_speed
        elif right_paddle.rect.centery > ball.rect.centery:
            right_paddle.rect.y -= ai_speed

        # Ball movement and collision
        ball.move()
        ball.bounce()

        # Ball collision with paddles
        if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
            ball.x_speed = -ball.x_speed

        # Scoring
        if ball.rect.left <= 0:
            right_score += 1
            ball.rect.center = (WIDTH // 2, HEIGHT // 2)
            ball.x_speed = -ball.x_speed
        if ball.rect.right >= WIDTH:
            left_score += 1
            ball.rect.center = (WIDTH // 2, HEIGHT // 2)
            ball.x_speed = -ball.x_speed

        # Draw paddles, ball, and score
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()

        score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        # Quit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return  

        pygame.display.update()

        clock.tick(60)

# Main program execution
def main():
    while True:
        choice = main_menu()  # Show the main menu
        if choice == "1p":
            difficulty = main_menu()  # Ask for difficulty
            if difficulty == "easy":
                game_loop_1p("easy")  # Start the game in 1-player mode with easy difficulty
            elif difficulty == "hard":
                game_loop_1p("hard")  # Start the game in 1-player mode with hard difficulty
        elif choice == "2p":
            game_loop_2p()  # Start the game in 2-player mode

if __name__ == "__main__":
    main()
