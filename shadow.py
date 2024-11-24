import pygame
from constants import TILE_SIZE, OFFSET_Y


class Shadow:
    def __init__(self, x, y, move_interval=1000):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = move_interval

    def move(self, player_a, player_b, maze):
        """Move the shadow toward the nearest player."""
        current_time = pygame.time.get_ticks()

        # Check if enough time has passed for the shadow to move
        if current_time - self.last_move_time >= self.move_interval:
            self.last_move_time = current_time

            # Determine the nearest player
            distance_a = abs(self.grid_x - player_a.grid_x) + abs(self.grid_y - player_a.grid_y)
            distance_b = abs(self.grid_x - player_b.grid_x) + abs(self.grid_y - player_b.grid_y)
            target_player = player_a if distance_a <= distance_b else player_b

            # Attempt to move toward the target player
            new_x, new_y = self.grid_x, self.grid_y
            if self.grid_x < target_player.grid_x:
                new_x += 1
            elif self.grid_x > target_player.grid_x:
                new_x -= 1
            elif self.grid_y < target_player.grid_y:
                new_y += 1
            elif self.grid_y > target_player.grid_y:
                new_y -= 1

            # Only move if the new position is not a wall
            if maze.grid[new_y][new_x] != 1:
                self.grid_x = new_x
                self.grid_y = new_y

        # Update pixel position based on the grid
        self.pixel_x = self.grid_x * TILE_SIZE
        self.pixel_y = self.grid_y * TILE_SIZE

    def check_collision(self, player_a, player_b):
        """Check if the shadow collides with any player."""
        shadow_rect = pygame.Rect(
            self.pixel_x, self.pixel_y, TILE_SIZE, TILE_SIZE
        )
        player_a_rect = pygame.Rect(
            player_a.pixel_x, player_a.pixel_y, TILE_SIZE, TILE_SIZE
        )
        player_b_rect = pygame.Rect(
            player_b.pixel_x, player_b.pixel_y, TILE_SIZE, TILE_SIZE
        )

        return shadow_rect.colliderect(player_a_rect) or shadow_rect.colliderect(player_b_rect)

    def reset(self, x, y):
        """Reset shadow to its starting position."""
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.last_move_time = pygame.time.get_ticks()

    def decrease_move_interval(self, amount):
        """Decrease the interval between moves to make the shadow faster."""
        self.move_interval = max(100, self.move_interval - amount)

    def draw(self, screen):
        """Draw the shadow on the screen."""
        pygame.draw.rect(
            screen,
            (128, 0, 128),  # Purple color for the shadow
            (self.pixel_x, self.pixel_y + OFFSET_Y, TILE_SIZE, TILE_SIZE)
        )
        # Optional debug rectangle
        pygame.draw.rect(
            screen,
            (255, 0, 0),  # Red border for debugging
            (self.pixel_x, self.pixel_y + OFFSET_Y, TILE_SIZE, TILE_SIZE),
            1
        )
