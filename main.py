import pygame
import random  # Import random module
import os
from maze import Maze
from player import Player
from shadow import Shadow
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, GREEN, OFFSET_Y


def load_images_from_folder(folder):
    """Helper function to load and scale images from a folder."""
    images = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".png"):
            image = pygame.image.load(os.path.join(folder, filename))
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            images.append(image)
    return images

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("You Are Your Own Enemy")

    # Load assets
    background = pygame.image.load("assets/background.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    tile_images = load_images_from_folder("assets/tile")
    player1_run_images = load_images_from_folder("assets/player1run")
    player2_run_images = load_images_from_folder("assets/player2run")
    key_frames = load_images_from_folder("assets/key")

    # Initialize maze, players, shadow, and logs
    maze = Maze('levels.txt', tile_images)
    player_a = Player(1, 1, player1_run_images)  # Knight (Player A)
    player_b = Player(len(maze.grid[0]) - 2, len(maze.grid) - 2, player2_run_images)  # Ninja (Player B)
    shadow = Shadow(len(maze.grid[0]) // 2, len(maze.grid) // 2)

    players = [player_a, player_b]
    normal_player = player_a  # Player currently moving normally
    opposite_player = player_b  # Player currently moving oppositely
    score = 0
    logs = []
    collectibles_remaining = 0
    clock = pygame.time.Clock()

    # Key animation variables
    key_frame_index = 0
    key_animation_speed = 5
    key_animation_counter = 0

    # Random control switching variables
    next_control_switch_time = pygame.time.get_ticks() + random.randint(1000, 5000)  # Random interval (1-5 seconds)

    def reset_collectibles():
        """Count the number of collectibles in the current level."""
        nonlocal collectibles_remaining
        collectibles_remaining = sum(row.count(3) for row in maze.grid)

    reset_collectibles()

    running = True
    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle random control switch
        current_time = pygame.time.get_ticks()
        if current_time >= next_control_switch_time:
            normal_player, opposite_player = opposite_player, normal_player  # Swap roles
            next_control_switch_time = current_time + random.randint(1000, 5000)  # Set next random switch time
            logs.append("Control switched between players.")

        # Handle input for both players using Arrow Keys
        keys = pygame.key.get_pressed()

        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        elif keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1

        # Apply movement logic
        normal_player.move(dx, dy, maze)  # Normal direction
        opposite_player.move(-dx, -dy, maze)  # Opposite direction

        # Update all players
        for player in players:
            player.update()

        # Shadow movement and collision detection
        shadow.move(player_a, player_b, maze)
        if shadow.check_collision(player_a, player_b):
            logs.append("Shadow caught a player! Resetting level...")
            player_a.reset(1, 1)
            player_b.reset(len(maze.grid[0]) - 2, len(maze.grid) - 2)
            shadow.reset(len(maze.grid[0]) // 2, len(maze.grid) // 2)
            score -= 10

        # Check if players collect collectibles
        for player in players:
            if maze.grid[player.grid_y][player.grid_x] == 3:
                logs.append(f"Player {players.index(player) + 1} collected a key!")
                maze.grid[player.grid_y][player.grid_x] = 0
                collectibles_remaining -= 1
                score += 5

        # Check if players reach the goal
        for player in players[:]:
            if maze.grid[player.grid_y][player.grid_x] == 2 and collectibles_remaining == 0:
                logs.append(f"Player {players.index(player) + 1} reached the goal!")
                players.remove(player)
                score += 1

        # Check win condition
        if not players:
            if maze.current_level_index + 1 < len(maze.levels):
                maze.load_level(maze.current_level_index + 1)
                player_a.reset(1, 1)
                player_b.reset(len(maze.grid[0]) - 2, len(maze.grid) - 2)
                players = [player_a, player_b]
                shadow.reset(len(maze.grid[0]) // 2, len(maze.grid) // 2)
                reset_collectibles()
                shadow.decrease_move_interval(100)
                logs.append("Level Complete!")
            else:
                logs.append(f"Game Over! Final Score: {score}")
                running = False

        # Animate the key
        key_animation_counter += 1
        if key_animation_counter >= key_animation_speed:
            key_frame_index = (key_frame_index + 1) % len(key_frames)
            key_animation_counter = 0

        # Draw maze, players, and shadow
        maze.draw(screen)
        shadow.draw(screen)
        for player in players:
            player.draw(screen)

        # Draw animated keys
        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                if cell == 3:
                    screen.blit(key_frames[key_frame_index], (x * TILE_SIZE, y * TILE_SIZE + OFFSET_Y))

        # Display score and logs
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, GREEN)
        level_text = font.render(f"Level: {maze.current_level_index + 1}", True, GREEN)  # Display level
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))  # Position level text below the score

        log_font = pygame.font.Font(None, 24)
        log_box_x = SCREEN_WIDTH - 300 - 10
        log_box_y = 10
        pygame.draw.rect(screen, (0, 0, 0), (log_box_x, log_box_y, 300, 120), 0)

        for i, log in enumerate(logs[-5:]):
            log_text = log_font.render(log, True, (255, 255, 255))
            screen.blit(log_text, (log_box_x + 10, log_box_y + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()




