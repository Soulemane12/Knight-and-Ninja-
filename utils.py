def check_collision(player, maze):
    return maze.grid[player.y][player.x] == 1  # Check if the player is on a wall



def check_win(player_a, player_b, maze):
    goal_a = maze.grid[player_a.y][player_a.x] == 2
    goal_b = maze.grid[player_b.y][player_b.x] == 2
    return goal_a and goal_b
