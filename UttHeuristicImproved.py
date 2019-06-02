import pygame
import math
import random
import copy


# Used to draw the grid on the screen

def draw_grid(screen):
    linecolor = (255, 255, 255)

    linewidth = 2

    for i in range(10):
        pygame.draw.line(screen, linecolor,

                         (20 + (screen.get_width() - 40) / 9 * i, 20),

                         (20 + (screen.get_width() - 40) / 9 * i,

                          (screen.get_height() - 20)), linewidth)

        pygame.draw.line(screen, linecolor,

                         (20, 20 + (screen.get_height() - 40) / 9 * i),

                         ((screen.get_width() - 20),

                          (20 + (screen.get_height() - 40) / 9 * i)), linewidth)

    linecolor = (255, 0, 0)

    linewidth = 6

    for i in range(0, 10, 3):
        pygame.draw.line(screen, linecolor,

                         (20 + (screen.get_width() - 40) / 9 * i, 20),

                         (20 + (screen.get_width() - 40) / 9 * i,

                          (screen.get_height() - 20)), linewidth)

        pygame.draw.line(screen, linecolor,

                         (20, 20 + (screen.get_height() - 40) / 9 * i),

                         ((screen.get_width() - 20),

                          (20 + (screen.get_height() - 40) / 9 * i)), linewidth)


# given the move and a list of each spots state return the move list

def move_list(pmove, spots):
    possible_moves = []

    sect = int(pmove[0] % 3 + (pmove[1] % 3) * 3)

    for i in range(9):

        if spots[sect][i] == 0:
            x = int(i % 3 + (sect % 3) * 3)

            y = int(math.floor(sect / 3) * 3 + i / 3)

            possible_moves.append([x, y])

    if len(possible_moves) == 0:

        for i in range(9):

            for j in range(9):

                if spots[i][j] == 0:
                    x = int(j % 3 + (i % 3) * 3)

                    y = int(math.floor(i / 3) * 3 + j / 3)

                    possible_moves.append([x, y])

    return possible_moves


# given a tictactoe grid return true if the player has got a win

def check_win(section, player):
    if (((player == section[0]) and

         (section[0] == section[1]) and (section[0] == section[2])) or

            ((player == section[3]) and

             (section[3] == section[4]) and (section[3] == section[5])) or

            ((player == section[6]) and

             (section[6] == section[7]) and (section[6] == section[8])) or

            ((player == section[0]) and

             (section[0] == section[3]) and (section[0] == section[6])) or

            ((player == section[1]) and

             (section[1] == section[4]) and (section[1] == section[7])) or

            ((player == section[2]) and

             (section[2] == section[5]) and (section[2] == section[8])) or

            ((player == section[0]) and

             (section[0] == section[4]) and (section[0] == section[8])) or

            ((player == section[6]) and

             (section[6] == section[4]) and (section[6] == section[2]))):
        return True

    return False


# given the move and a list of each spots check if the move caused a section to

# win

def check_win_sect(section, spots, total_sections, player): #updates total_sections, and checks if entire game has been won
    if (check_win(spots[section], player)):

        for i in range(9):
            spots[section][i] = player

        total_sections[section] = player

        if check_win(total_sections, player):
            print("player {:d} Wins".format(player))

            return True

    return False


# draws the x's and o's that were placed

def draw_x_o(screen, spots):
    player_x = pygame.transform.scale(pygame.image.load("X.png").convert(),

                                      (int((screen.get_width() - 40) / 12), int((screen.get_height() - 40) / 12)))

    player_o = pygame.transform.scale(pygame.image.load("O.png").convert(),

                                      (int((screen.get_width() - 40) / 12), int((screen.get_height() - 40) / 12)))

    for i in range(9):

        for j in range(9):

            x = int(j % 3 + (i % 3) * 3)

            y = int(math.floor(i / 3) * 3 + j / 3)

            if spots[i][j] == 1:
                screen.blit(player_x, [30 + (screen.get_width() - 40) / 9 * x,

                                       30 + (screen.get_height() - 40) / 9 * y])

            if spots[i][j] == 2:
                screen.blit(player_o, [30 + (screen.get_width() - 40) / 9 * x,

                                       30 + (screen.get_height() - 40) / 9 * y])


def heuristic_function(currentMove, spots, player, total_sections):
    # currentMove is current move being considered.  ex: [7,4] where 7 is column(across) and 4 is row(down)
    # spots is the board's current state ex: 9 of [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # player is current player
    # total_sections is entire board [0, 0, 0,
    #                                 0, 1, 0
    #                                 0, 0, 0] single array.

    heuristic_val = 0
    # foundWin = False

    xTemp = int(currentMove[0] / 3 + math.floor(currentMove[1] / 3) * 3)
    yTemp = int(currentMove[0] % 3 + (currentMove[1] % 3) * 3)
    spotsTemp = copy.deepcopy(spots)
    totalSectionsTemp = copy.deepcopy(total_sections)
    spotsTemp[xTemp][yTemp] = player
    if (check_win_sect(xTemp, spotsTemp, totalSectionsTemp, player)):
        x = int(currentMove[0] / 3 + math.floor(currentMove[1] / 3) * 3)
        y = int(currentMove[0] % 3 + (currentMove[1] % 3) * 3)
        # spots[x][y] = player
        # foundWin = True
        heuristic_val = 10000000
    elif(check_win(spotsTemp[xTemp], player)): #Leads to a win on a small board
        heuristic_val = checkTwoInARowBig(total_sections, xTemp, player) # checks if this leads to two boards in a row
    else:
        heuristic_temp = checkTwoInARowBig(spots[xTemp], yTemp, player)
        if(heuristic_temp == 300):
            heuristic_val = 10
            heuristic_val += (getHeuristicValNoOptimalMove(currentMove) / 10) #move results in multiple possible wins.  Corner and center moves are
                                                                              #favored every slightly over top/side moves. This breaks ties between
                                                                              #multiple optimal moves
        elif(heuristic_temp != 25):
            heuristic_val = 8
            heuristic_val += (getHeuristicValNoOptimalMove(currentMove) / 10)
        else: #No move gets them closer to a win.  Then corner is best, then center, then top/bottom/left/right
            heuristic_val = getHeuristicValNoOptimalMove(currentMove)

    return heuristic_val

def checkTwoInARowBig(total_sections, winningBoard, player):
    #winningBoard is xTemp from heuristic_function
    heuristic_value = 0
    numberOfInARows = 0
    inLine = getSpotsInLine(winningBoard)
    for inLineSpot in inLine:
        if(total_sections[inLineSpot] == player): #if other inline spot is owned by player
            if(isNotImpeded(winningBoard, inLineSpot, total_sections)): #if spot aka winningBoard and other owned inline spot are not blocked by the other player
                numberOfInARows += 1
    if(numberOfInARows == 2): #move results in two moves in a row
        heuristic_value = 300
    elif(numberOfInARows == 0): #move results in no moves in a row
        heuristic_value = 25
    else: #move results in one move in a row.
        heuristic_value = numberOfInARows * 100
    return heuristic_value

#checks if two possible in-a-row moves on a board are already impeded by the other player
def isNotImpeded(spot1, spot2, total_sections):
    notImpeded = True
    emptyBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    emptyBoard[spot1] = 3 # 3 here is an arbitrary number.  Used to not be confused with player 1 or 2
    emptyBoard[spot2] = 3
    movesToCheck = [0, 1, 2, 3, 4, 5, 6, 7, 8] # check all the spots not including spot1 and spot2 to see if it would result
                                               # in a win if the board were entirely empty.  We can then check if this spot is
                                               # actually occupied or not
    movesToCheck.remove(spot1)
    movesToCheck.remove(spot2)
    for move in movesToCheck:
        emptyBoard[move] = 3
        if(check_win(emptyBoard, 3)):
            spot3 = move
            emptyBoard[move] = 0
            break
        emptyBoard[move] = 0
    #spot3 is now the spot to check for being occupied or not
    if(total_sections[spot3] != 0):
        notImpeded = False

    return notImpeded

#Return the spots that are can be combined with spot to make a winning combination
def getSpotsInLine(spot):
    if(spot == 0):
        inLine = [1, 2, 3, 4, 6, 8]
    elif(spot == 1):
        inLine = [0, 2, 4, 7]
    elif(spot == 2):
        inLine = [0, 1, 4, 5, 6, 8]
    elif(spot == 3):
        inLine = [0, 4, 5, 6]
    elif(spot == 4):
        inLine = [0, 1, 2, 3, 5, 6, 7, 8]
    elif(spot == 5):
        inLine = [2, 3, 4, 8]
    elif(spot == 6):
        inLine = [0, 2, 3, 4, 7, 8]
    elif(spot == 7):
        inLine = [1, 4, 6, 8]
    else:
        inLine = [0, 2, 4, 5, 6, 7]
    return inLine

def getHeuristicValNoOptimalMove(currentMove):
    row = currentMove[1]
    col = currentMove[0]
    if(row == 0 or row == 2 or row == 3 or row == 5 or row == 6 or row == 8): #a top or bottom row on individual board
        topOrBottomRow = True
    else:
        topOrBottomRow = False
    if (col == 0 or col == 2 or col == 3 or col == 5 or col == 6 or col == 8):  # a top or bottom col on individual board
        topOrBottomCol = True
    else:
        topOrBottomCol = False
    if(topOrBottomRow and topOrBottomCol):
        return 5 #is a corner move
    elif((not topOrBottomRow) and (not topOrBottomCol)):
        return 3 #is a center move
    else:
        return 1 #is a top/bottom/left/right move


def main(mode):
    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Call this function so the Pygame library can initialize itself

    pygame.init()
    prev_move = [-1, -1]
    spots = [[0 for x in range(9)] for x in range(9)]
    total_sections = [0 for x in range(9)]
    open_pos = []

    for i in range(9):
        for x in range(9):
            open_pos.append([i, x])

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800, 600])
    # This sets the name of the window
    pygame.display.set_caption('Ultimate tic-tac-toe')
    clock = pygame.time.Clock()

    # Before the loop, load the sounds:
    # click_sound = pygame.mixer.Sound("01. La La Land.ogg")
    # Set positions of graphics
    # background_position = [0, 0]

    done = False
    pos = [0, 0]
    # x is 1 o is 2

    randomplayer = False
    player = 1;

    if ((mode == 2 and random.randint(0, 1) == 0) or mode == 3):
        randomplayer = True

    while not done:
        mouse_position = pygame.mouse.get_pos()
        pos[0] = math.floor((mouse_position[0] - 20) / ((screen.get_width() - 40) / 9))
        pos[1] = math.floor((mouse_position[1] - 20) / ((screen.get_height() - 40) / 9))

        if (not randomplayer):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check if the mouse click was on a valid spot
                    # if it was place players mark and check for a win
                    for i in open_pos:
                        if (pos[0] == i[0] and pos[1] == i[1]):
                            x = int(pos[0] / 3 + math.floor(pos[1] / 3) * 3)
                            y = int(pos[0] % 3 + (pos[1] % 3) * 3)
                            spots[x][y] = player
                            # check if the move caused the player to win a section
                            # if the move won the whole game done will become true
                            done = check_win_sect(x, spots, total_sections, player)
                            open_pos = move_list(pos, spots)
                            if (len(open_pos) == 0 and not done):
                                print("Tie")
                                done = True

                            if (mode == 2):
                                randomplayer = (not randomplayer)

                            player = 2 if player == 1 else 1

        else:

            if (False):
                move = random.randint(0, len(open_pos) - 1)
                pos = open_pos[move]
                x = int(pos[0] / 3 + math.floor(pos[1] / 3) * 3)
                y = int(pos[0] % 3 + (pos[1] % 3) * 3)
                spots[x][y] = player
                print(open_pos)
                print(x, y)
            else: #Intelligent agent code starts here
                #
                #foundWin = False
                #for posMove in open_pos:
                #    xTemp = int(posMove[0] / 3 + math.floor(posMove[1] / 3) * 3)
                #    yTemp = int(posMove[0] % 3 + (posMove[1] % 3) * 3)
                #    spotsTemp = copy.deepcopy(spots)
                #    spotsTemp[xTemp][yTemp] = player
                #    if(check_win_sect(xTemp, spotsTemp, total_sections, player)):
                #        x = int(posMove[0] / 3 + math.floor(posMove[1] / 3) * 3)
                #        y = int(posMove[0] % 3 + (posMove[1] % 3) * 3)
                #        spots[x][y] = player
                #        foundWin = True
                #        break

                currentPosValues = []
                random.shuffle(open_pos)
                for posMove in open_pos:
                    currentMoveHeuristic = heuristic_function(posMove, spots, player, total_sections)
                    currentPosValues.append(currentMoveHeuristic)

                currentMoveValue = max(currentPosValues) # The max value
                currentMoveIndex = currentPosValues.index(currentMoveValue) # The index of the max value
                pos = open_pos[currentMoveIndex] # The move that should be taken

                #The move is finalized.  Random move if currentMoveValue is zero, or currentMove
                if(currentMoveValue == 0):
                #check_win_sect(x, spots, total_sections, player)
                    move = random.randint(0, len(open_pos) - 1)
                    pos = open_pos[move]
                    x = int(pos[0] / 3 + math.floor(pos[1] / 3) * 3)
                    y = int(pos[0] % 3 + (pos[1] % 3) * 3)
                    spots[x][y] = player
                    print(open_pos)
                    print(x, y)
                else:
                    x = int(pos[0] / 3 + math.floor(pos[1] / 3) * 3)
                    y = int(pos[0] % 3 + (pos[1] % 3) * 3)
                    spots[x][y] = player

            # check if the move caused the player to win a section
            # if the move won the whole game done will become true
            done = check_win_sect(x, spots, total_sections, player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    done = True
            open_pos = move_list(pos, spots)
            if (len(open_pos) == 0 and not done):
                print("Tie")
                done = True

            if (mode == 2):
                randomplayer = (not randomplayer)
            for i in range(10000000):
                x = i + 1

            player = 2 if player == 1 else 1
        # fill the background color to black so that it will
        # refresh what is on the screen

        screen.fill(BLACK)
        draw_grid(screen)

        # indicate where you will be putting your move (yellow mark on screen)

        for i in open_pos:
            if (pos[0] == i[0] and pos[1] == i[1]):
                pygame.draw.rect(screen, (255, 255, 152),
                                 pygame.Rect(30 + (screen.get_width() - 40) / 9 * pos[0],
                                             30 + (screen.get_height() - 40) / 9 * pos[1],
                                             (screen.get_width() - 40) / 12, (screen.get_height() - 40) / 12))

            else:
                pygame.draw.rect(screen, (55, 55, 55),
                                 pygame.Rect(30 + (screen.get_width() - 40) / 9 * i[0],
                                             30 + (screen.get_height() - 40) / 9 * i[1],
                                             (screen.get_width() - 40) / 12, (screen.get_height() - 40) / 12))

        draw_x_o(screen, spots)

        # Copy image to screen:

        # screen.blit(player_image, [x, y])

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':

    string = 'Mode:\n Enter 1 for human vs human'

    string += '\n Enter 2 for human vs computer '

    string += '\n Enter 3 for computer vs computer \n'

    try:

        mode = int(input(string))

    except ValueError:

        print("Entered the Wrong Value please enter 1,2, or 3")

    main(mode)
