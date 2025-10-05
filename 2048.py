import random
import os
import msvcrt as ms 
import time

# THIS CODE USES MSVCRT WHICH IS WINDOWS ONLY, MEANING THIS ONLY RUNS ON WINDOWS AND NOT LINUX BASED SYSTEMS

# Initialize board at start or restart
def init_board():
    board = [[0] * 4 for _ in range(4)]

    # Spawn 2 tiles 
    spawn_tile(board)
    spawn_tile(board)

    return board

# Generate tile on random empty space
def spawn_tile(board):
    empty_tiles = [(row, col) for row in range(4) for col in range(4) if board[row][col] == 0]

    # Generate tile only if there exists an empty tile
    if empty_tiles:
        row, col = random.choice(empty_tiles)

        # 90% chance to generate a 2, 10% chance to generate a 4
        board[row][col] = 2 if random.random() < 0.9 else 4
    
    return
    
# Print out visual board
def display_board(board, score):
    # Clear terminal screen
    os.system("cls") 

    # Display score and instructions
    print(f"SCORE: {score} | (W)Up (S)Down (A)Left (D)Right (R)Reset (Q)Quit")
    
    # DIsplay board
    print("-" * 25)
    for row in board:
        print("|", end="")
        for val in row:
            if val == 0:
                print("{:^5}".format(" "), end="|")
            else:
                print("{:^5}".format(val), end="|")
        print("\n" + "-" * 25)
    
    return

# Handle player input 
def get_player_input():
    valid_inputs = [b'w', b'a', b's', b'd', b'r', b'q']
    while True:
        i = ms.getch()
        if i in valid_inputs:
            return i

# Move tiles based on input given
def move_board(board, direction):
    score_gain = 0
    new_board = board

    # Rotate board based on direction so move_left can be used
    for _ in range(direction):
        new_board = rotate(new_board)

    # Move tiles
    new_board, score_gain = move_left(new_board)

    # Rotate board back to normal
    for _ in range(4 - direction):
        new_board = rotate(new_board)

    return new_board, score_gain

# Only have 1 directional movement to avoid repeated, redundant code for each individual direction
def move_left(board):
    score_gain = 0
    new_board = []

    # Iterate thru and move each row
    for row in board:
        compressed = shift(row)
        merged, gained = merge(compressed)
        compressed = shift(merged)
        new_board.append(compressed) # Call shift again to remove gaps during merge
        score_gain += gained
    return new_board, score_gain

# Shift all non zero numbers to the left
def shift(row):
    new_row = [num for num in row if num != 0]
    new_row += [0] * (4 - len(new_row))
    return new_row

# Merge any adjacent equal numbers into one another and get score
def merge(row):
    score_gain = 0
    for i in range(4 - 1):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            score_gain += row[i]
            row[i+1] = 0
    return row, score_gain


# Rotate board 90 deg clockwise. Supporting function that allows every direction to be able use move_left
def rotate(board):
    return [list(row) for row in zip(*board[::-1])]

# End game if no more moves exist for player
def game_over(board):
    # Check each individual tile
    for row in range(4):
        for col in range(4):
            # Check if tile is empty
            if board[row][col] == 0:
                return False
            # Check if horiziontal merge possible
            if col < 3 and board[row][col] == board[row][col + 1]:
                return False
            # Check if vertical merge possible
            if row < 3 and board[row][col] == board[row +1][col]:
                return False
    
    return True


def main():
    start = True # flag for starting game

    # Print initial start up screen, allow user to provide a seed for debug mode
    while True:
        os.system("cls") 
        print("2048! (W)Play (S)Seed Mode (Q) Quit")
        i = get_player_input()

        if i == (b'w'):
            print('Starting the game!')
            break

        if i == (b's'):
            seed = input("Input seed: ")
            try:
                random.seed(seed)
                print("Using Seed:", seed)
                time.sleep(1)
            except ValueError:
                print("Invalid seed, using random seed.")

        if i ==(b'q'):
            start = False
            print("Quitting Game...")
            break


    # Initialize board and score
    score = 0
    board = init_board()

    # Loop game unless player restarts, quits, or has a game over
    while True and start:
        display_board(board, score)

        # Check if board has no more moves
        if game_over(board):
            print("Game Over!!")
            break
        
        # Take valid player input
        i = get_player_input()
        
        # Restart game
        if i == b'r':
            print("Restarting Game...")
            time.sleep(1)
            new_board = init_board()
            score = 0
            gained = 0

        # Quit game
        if i == b'q':
            print("Quitting Game...")
            time.sleep(1)
            break
            
        # Handle movement
        directions = {b'w' : 3, b'a' : 0, b's' : 1, b'd' : 2} # key/number equivalent to num of 90 deg clockwise rotations
        if i in directions:
            new_board, gained = move_board(board, directions[i])

        # If valid movement, handle new game state and add score and new tile
        if new_board != board:
            board = new_board
            score += gained

            # Add new tile if not restarting game
            if i != b'r':
                spawn_tile(board)


        


if __name__ == "__main__":
    main()