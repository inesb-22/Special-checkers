from fonctions import draw_board, display_board, move_computer, count_pieces, check_winner, draw_rps

SQUARE_SIZE = 30

game_state = "MENU"

p_rps_choice = "rock"
c_rps_choice = "rock"

difficulty = "medium"

select_p = None
game_winner = None


# 0 = empty cell
# 1 = computer piece
# 2 = player piece
# 3 = computer queen
# 4 = player queen

game_board=[
    [1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,2,0,2,0,2,0,2],
    [2,0,2,0,2,0,2,0],
    [0,2,0,2,0,2,0,2]
]


def setup():
    size(660,660)
    textAlign(LEFT)
    textSize(16)
    println("The game has started!")


def draw():
    global game_state, difficulty, game_winner

    background(168,129,92)
    draw_board(SQUARE_SIZE)
    display_board(SQUARE_SIZE, game_board)

    fill(255) # information text
    textSize(16)

    if game_state == "MENU":
        text("--- SELECT DIFFICULTY ---", 20, 25)
        text("Press E : Easy", 20, 50)
        text("Press M : Medium", 20, 70)
        text("Press H : Hard", 20, 90)

    elif game_state == "RPS":
        text("1 = Rock          | 2 = Paper          | 3 = Scissors", 20, 20)
        draw_rps()

    elif game_state == "PLAYER_MOVE":
        text("Select a piece. A/E (Forward), Q/D (Backward - Queens)", 20, 25)

    elif game_state == "END":
        if game_winner == "player":
            fill(0,255,0)
            text("You won!", 20, 25)
        else:
            fill(255,0,0)
            text("Computer won!", 20, 25)
            
        fill(255)
        text("Press R to restart.", 20, 50)

    # score
    r_player_p, r_computer_p = count_pieces(game_board)
    p_captures = 12 - r_computer_p
    c_captures = 12 - r_player_p

    fill(255)
    textSize(14)
    text("Your captures : "+str(p_captures), 20, height-70)
    text("Computer captures : "+str(c_captures), 20, height-50)
    text("Difficulty : "+difficulty, 20, height-30)

    # stop button
    fill(180,40,40)
    rect(width-90, height-45, 70, 30)
    fill(255)
    text("STOP", width-73, height-25)


# keyboard management

def keyPressed():
    global game_state, p_rps_choice, c_rps_choice, difficulty, select_p, game_winner

    if game_state == "END":
        if key == 'r' or key == 'R':
            reset_game()
        return

    # menu screen
    if game_state == "MENU":
        if key == 'e' or key == 'E':
            difficulty = "easy"
            game_state = "RPS"
        elif key == 'm' or key == 'M':
            difficulty = "medium"
            game_state = "RPS"
        elif key == 'h' or key == 'H':
            difficulty = "hard"
            game_state = "RPS"
        return

    # rps screen
    if game_state == "RPS":
        if key == '1':
            p_rps_choice = "rock"
        elif key == '2':
            p_rps_choice = "paper"
        elif key == '3':
            p_rps_choice = "scissors"
        else:
            return

        roll = int(random(3))
        if roll == 0:
            c_rps_choice = "rock"
        elif roll == 1:
            c_rps_choice = "paper"
        else:
            c_rps_choice = "scissors"

        println("You : "+p_rps_choice)
        println("Computer : "+c_rps_choice)

        if p_rps_choice == c_rps_choice:
            println("Tie!")
            return

        # player victory
        if (p_rps_choice == "rock" and c_rps_choice == "scissors") or \
           (p_rps_choice == "paper" and c_rps_choice == "rock") or \
           (p_rps_choice == "scissors" and c_rps_choice == "paper"):

            println("You won RPS!")
            game_state = "PLAYER_MOVE"
            return

        # computer victory
        else:
            println("Computer won RPS.")
            move_computer(game_board, difficulty)
            
            winner = check_winner(game_board)
            if winner is not None:
                game_winner = winner
                game_state = "END"
            return


    # player movement
    if game_state == "PLAYER_MOVE":
        if select_p is None:
            return

        current_row = select_p[0]
        current_col = select_p[1]
        piece_type = game_board[current_row][current_col]
        
        move_row = 0
        move_col = 0

        if key == 'a' or key == 'A':     # top left
            move_row, move_col = -1, -1
        elif key == 'e' or key == 'E':   # top right
            move_row, move_col = -1, 1
        elif key == 'q' or key == 'Q':   # bottom left
            if piece_type == 2:
                println("A simple piece cannot move backward! Only a Queen can.")
                return
            move_row, move_col = 1, -1
        elif key == 'd' or key == 'D':   # bottom right
            if piece_type == 2:
                println("A simple piece cannot move backward! Only a Queen can.")
                return
            move_row, move_col = 1, 1
        else:
            return

        new_row = current_row + move_row
        new_col = current_col + move_col
        
        valid_move = False
        captured_piece = None

        if 0 <= new_row < 8 and 0 <= new_col < 8:
            
            # simple move
            if game_board[new_row][new_col] == 0:
                valid_move = True
                
            # jump over enemy piece (1 or 3)
            elif game_board[new_row][new_col] in [1,3]:
                jump_row = new_row + move_row
                jump_col = new_col + move_col
                
                if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                    if game_board[jump_row][jump_col] == 0:
                        valid_move = True
                        captured_piece = (new_row, new_col)
                        new_row = jump_row
                        new_col = jump_col

        if valid_move:
            game_board[current_row][current_col] = 0
            
            # player promotion to queen at row 0
            if piece_type == 2 and new_row == 0:
                game_board[new_row][new_col] = 4
                println("You got a Queen!")
            else:
                game_board[new_row][new_col] = piece_type
            
            if captured_piece is not None:
                game_board[captured_piece[0]][captured_piece[1]] = 0

            winner = check_winner(game_board)
            if winner is not None:
                game_winner = winner
                game_state = "END"
            else:
                game_state = "RPS"

            select_p = None


# mouse management

def mousePressed():
    global select_p, game_state

    # stop button
    if mouseX >= width-90 and mouseX <= width-20 and mouseY >= height-45 and mouseY <= height-15:
        exit()

    # selection of player piece or queen (value 2 or 4)
    if game_state == "PLAYER_MOVE":
        for row in range(8):
            for col in range(8):
                if game_board[row][col] in [2,4]:
                    pos_x = SQUARE_SIZE*2 + SQUARE_SIZE/4 + col*SQUARE_SIZE*2.5
                    pos_y = SQUARE_SIZE*2 + SQUARE_SIZE/4 + row*SQUARE_SIZE*2.5
                    
                    if dist(mouseX, mouseY, pos_x, pos_y) <= 40:
                        select_p = (row, col)
                        println("Selected piece : "+str(row)+", "+str(col))
                        return


def reset_game():
    global game_board, game_state, select_p, game_winner, p_rps_choice, c_rps_choice

    game_board=[
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,2,0,2,0,2,0,2],
        [2,0,2,0,2,0,2,0],
        [0,2,0,2,0,2,0,2]
    ]
    
    game_state = "MENU"
    select_p = None
    game_winner = None
    p_rps_choice = "rock"
    c_rps_choice = "rock"
    println("New game!")
