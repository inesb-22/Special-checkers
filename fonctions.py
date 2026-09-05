# board drawing

def draw_board(square_size):
    fill(117,62,35)
    stroke(107,52,25)
    rect(square_size, square_size, width - (2*square_size), height - (2*square_size))
    fill(235,221,205)
    for horizontal in range(int(square_size + square_size/2), int(width - square_size/2), int(square_size*5)):
        for vertical in range(int(square_size + square_size/2), int(height - square_size/2), int(square_size*5)):
            square(horizontal + square_size*2, vertical + square_size*2, square_size*2.5)
            square(horizontal - square_size/2, vertical - square_size/2, square_size*2.5)


# display pieces and queens

def display_board(square_size, game_board):
    for row in range(8):
        for col in range(8):
            pos_x = square_size*2 + square_size/4 + col*square_size*2.5
            pos_y = square_size*2 + square_size/4 + row*square_size*2.5
            stroke(91,50,36)
            
            value = game_board[row][col]

            # 1 = computer simple piece (beige)
            if value == 1:
                fill(235,221,205)
                circle(pos_x, pos_y, 50)
                
            # 2 = player simple piece (brown)
            elif value == 2:
                fill(91,50,36)
                circle(pos_x, pos_y, 50)
                
            # 3 = computer queen (beige with gold center)
            elif value == 3:
                fill(235,221,205)
                circle(pos_x, pos_y, 50)
                fill(255,215,0)
                circle(pos_x, pos_y, 24)
                
            # 4 = player queen (brown with gold center)
            elif value == 4:
                fill(91,50,36)
                circle(pos_x, pos_y, 50)
                fill(255,215,0)
                circle(pos_x, pos_y, 24)


def move_computer(game_board, difficulty):

    valid_moves = []

    # search for all valid moves
    for row in range(8):
        for col in range(8):
            piece = game_board[row][col]
            
            # computer pieces (1 = simple, 3 = queen)
            if piece == 1 or piece == 3:
                
                # simple piece only moves down, queen moves in 4 directions
                if piece == 1:
                    directions = [(1,-1), (1,1)]
                else:
                    directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
                
                for move_row, move_col in directions:
                    new_row = row + move_row
                    new_col = col + move_col
                    
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        
                        # free square
                        if game_board[new_row][new_col] == 0:
                            valid_moves.append((row, col, new_row, new_col, None, None))
                            
                        # opponent piece (2 or 4)
                        elif game_board[new_row][new_col] in [2,4]:
                            jump_row = new_row + move_row
                            jump_col = new_col + move_col
                            
                            if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                                if game_board[jump_row][jump_col] == 0:
                                    valid_moves.append((row, col, jump_row, jump_col, new_row, new_col))

    if len(valid_moves) == 0:
        print("Computer is blocked.")
        return

    # obligation to capture if possible
    jump_moves = [move for move in valid_moves if move[4] is not None]
    if len(jump_moves) > 0:
        valid_moves = jump_moves

    # difficulty logic
    play_smart = False
    
    if difficulty == "easy":
        play_smart = False
    elif difficulty == "medium":
        if random(100) < 50:
            play_smart = True
        else:
            play_smart = False
    elif difficulty == "hard":
        play_smart = True

    if not play_smart: 
        choice = valid_moves[int(random(len(valid_moves)))]
    else: 
        best_move = valid_moves[0]
        best_distance = 1000

        for move in valid_moves:
            distance = 1000
            for piece_row in range(8):
                for piece_col in range(8):
                    if game_board[piece_row][piece_col] in [2,4]:
                        d = abs(piece_row - move[2]) + abs(piece_col - move[3])
                        if d < distance:
                            distance = d
            
            if distance < best_distance:
                best_distance = distance
                best_move = move

        choice = best_move

    # movement execution
    start_row, start_col, end_row, end_col, captured_row, captured_col = choice
    moved_piece = game_board[start_row][start_col]
    
    game_board[start_row][start_col] = 0
    
    # computer queen promotion at row 7 (the bottom)
    if moved_piece == 1 and end_row == 7:
        game_board[end_row][end_col] = 3
        print("Computer got a Queen!")
    else:
        game_board[end_row][end_col] = moved_piece
    
    if captured_row is not None:
        game_board[captured_row][captured_col] = 0
        print("Computer captured your piece!")
    else:
        print("Computer moved.")


# count player and computer pieces

def count_pieces(game_board):
    player_pieces = 0
    computer_pieces = 0
    for row in range(8):
        for col in range(8):
            if game_board[row][col] in [1,3]:
                computer_pieces += 1
            elif game_board[row][col] in [2,4]:
                player_pieces += 1
    return player_pieces, computer_pieces


# check win conditions

def check_winner(game_board):
    player_pieces, computer_pieces = count_pieces(game_board)
    if player_pieces == 0:
        return "computer"
    if computer_pieces == 0:
        return "player"
    return None


def draw_rps():
    stroke(0)
    strokeWeight(1)

    # rock
    fill(80,80,80)
    stroke(0)
    ellipse(115,15,22,16)
    
    fill(40)
    noStroke()
    circle(111,13,2)        # left eye
    circle(119,13,2)        # right eye
    
    # smile
    stroke(40)
    noFill()
    arc(115,16,8,5,0,PI)

    # paper
    stroke(0)
    fill(245,245,220)
    rect(245,6,14,18)
    
    stroke(150,160,130)
    line(248,11,256,11)    # lines
    line(248,15,256,15)
    line(248,19,256,19)

    # scissors
    stroke(120)
    strokeWeight(1)
    line(400,20,410,7)     # blades
    line(410,20,400,7)   
    
    stroke(220,120,80)
    strokeWeight(2)
    noFill()
    circle(399,22,5)        # handles
    circle(411,22,5)       
    
    strokeWeight(1)         # reset stroke weight for the rest of the game
