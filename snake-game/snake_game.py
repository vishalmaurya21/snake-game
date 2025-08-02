import curses
import random
import time

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.timeout(100)  # Refresh rate in milliseconds
    
    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    
    # Create a new window
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)
    
    # Initial snake position and direction
    snake_x = sw // 4
    snake_y = sh // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    
    # Create food
    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], curses.ACS_DIAMOND)
    
    # Initial direction (right)
    key = curses.KEY_RIGHT
    
    score = 0
    
    # Game loop
    while True:
        # Get next key
        next_key = w.getch()
        key = key if next_key == -1 else next_key
        
        # Calculate new head position
        new_head = [snake[0][0], snake[0][1]]
        
        # Update head position based on direction
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1
        
        # Add new head to snake
        snake.insert(0, new_head)
        
        # Check if snake hits the border
        if (
            new_head[0] in [0, sh - 1] or
            new_head[1] in [0, sw - 1] or
            new_head in snake[1:]
        ):
            w.clear()
            w.addstr(sh // 2, sw // 2 - 10, f"Game Over! Your score: {score}")
            w.refresh()
            time.sleep(2)
            break
        
        # Check if snake eats the food
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                new_food = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = new_food if new_food not in snake else None
            w.addch(food[0], food[1], curses.ACS_DIAMOND)
        else:
            # Remove tail if no food eaten
            tail = snake.pop()
            w.addch(tail[0], tail[1], " ")
        
        # Draw snake head
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
        
        # Display score
        w.addstr(0, 2, f"Score: {score}")
        
        # Draw border
        w.border(0)
        w.refresh()

def start_game():
    print("Welcome to Snake Game!")
    print("Use arrow keys to move the snake.")
    print("Eat the food (♦) to grow and earn points.")
    print("Don't hit the walls or yourself!")
    print("Press Enter to start...")
    input()
    curses.wrapper(main)
    # print("Thanks for playing Snake Game!")
    print("Game Over")

if __name__ == "__main__":
    try:
        start_game()
    except Exception as e:
        print(f"An error occurred: {e}")
    
