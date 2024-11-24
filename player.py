from constants import TILE_SIZE, OFFSET_Y

class Player:
    def __init__(self, x, y, images):
        self.grid_x = x
        self.grid_y = y
        self.images = images
        self.current_frame = 0
        self.animation_speed = 5
        self.animation_counter = 0
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False

    def move(self, dx, dy, maze):
        if self.moving:
            return
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if 0 <= new_x < len(maze.grid[0]) and 0 <= new_y < len(maze.grid):
            if maze.grid[new_y][new_x] != 1:
                self.grid_x = new_x
                self.grid_y = new_y
                self.target_x = new_x * TILE_SIZE
                self.target_y = new_y * TILE_SIZE
                self.moving = True

    def update(self):
        speed = 4  # Smooth movement speed
        if self.moving:
            if self.pixel_x < self.target_x:
                self.pixel_x = min(self.pixel_x + speed, self.target_x)
            elif self.pixel_x > self.target_x:
                self.pixel_x = max(self.pixel_x - speed, self.target_x)

            if self.pixel_y < self.target_y:
                self.pixel_y = min(self.pixel_y + speed, self.target_y)
            elif self.pixel_y > self.target_y:
                self.pixel_y = max(self.pixel_y - speed, self.target_y)

            if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
                self.moving = False


    def reset(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False

    def draw(self, screen):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.animation_counter = 0
        image = self.images[self.current_frame]
        screen.blit(image, (self.pixel_x, self.pixel_y + OFFSET_Y))
