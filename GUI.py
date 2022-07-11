
# GUI.py
from gettext import find
import pygame
import time
pygame.font.init()
redlineList = []

class Grid:
    board = [
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 7, 5, 1, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 2, 4, 0, 6, 0, 0, 0, 5],
        [0, 1, 9, 3, 0, 0, 0, 1, 2],
        [2, 2, 0, 0, 2, 7, 4, 0, 0],
        [0, 4, 3, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
        return self.model

    def place(self, row, col, val):

        self.cubes[row][col].set(val)
        self.update_model()
        # row, col = self.selected
        # if self.cubes[row][col].value == 0:
        #     self.cubes[row][col].set(val)
        #     self.update_model()

        #     if valid(self.model, val, (row,col)) and solve(self.model):
        #         return True
        #     else:
        #         self.cubes[row][col].set(0)
        #         self.cubes[row][col].set_temp(0)
        #         self.update_model()
        #         return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (200, 200, 200), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (200, 200, 200), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("arial", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+20, y+7))
        #elif not(self.value == 0):
        elif (self.value > 0):
            text = fnt.render(str(self.value), 1, (65, 146, 75))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (46,139,192), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((44,44,44))
    # Draw time *defunct*
    #fnt = pygame.font.SysFont("arial", 36)
    #text = fnt.render("Time: " + format_time(time), 1, (200,200,200))
    #win.blit(text, (376, 568))

    # Draw Strikes *defunct*
    #text = fnt.render("X " * strikes, 1, (255, 0, 0))
    #win.blit(text, (20, 560))

    # Draw Lines
    #red_line_draw(win, 0, 30, 550, 30)

    # Draw Buttons
    # Solve One button
    mouse = pygame.mouse.get_pos()
    if 40 <= mouse[0] <= 140 and 575 <= mouse[1] <= 605:
        pygame.draw.rect(win,(150,150,150),[40,575,100,30])          
    else:
        pygame.draw.rect(win,(111,111,111),[40,575,100,30])
    fnt = pygame.font.SysFont("arial", 20)
    text = fnt.render("Solve One", 1, (200,200,200))
    win.blit(text, (50, 577))
    # Solve All button
    if 220 <= mouse[0] <= 320 and 575 <= mouse[1] <= 605:
        pygame.draw.rect(win,(150,150,150),[220,575,100,30])          
    else:
        pygame.draw.rect(win,(111,111,111),[220,575,100,30])
    fnt = pygame.font.SysFont("arial", 20)
    text = fnt.render("Solve All", 1, (200,200,200))
    win.blit(text, (237, 577))
    # Quit button
    if 400 <= mouse[0] <= 500 and 575 <= mouse[1] <= 605:
        pygame.draw.rect(win,(150,150,150),[400,575,100,30])          
    else:
        pygame.draw.rect(win,(111,111,111),[400,575,100,30])
    fnt = pygame.font.SysFont("arial", 20)
    text = fnt.render("Quit", 1, (200,200,200))
    win.blit(text, (433, 577))
    # Draw grid and board
    board.draw(win)

def red_line_draw(win, startX, finishX, startY, finishY):
    pygame.draw.line(win, (255,0,0), (startX, startY), (finishX, finishY), 3)

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None

def reset_board(board, model):
    for i in range(len(model)):
        for j in range(len(model[0])):
            if model[i][j] == -1:
                board.place(i, j, 0)
    return None

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False

def valid(bo, num, pos):
    # Check row
    print(pos)
    for i in range(len(bo[0])):
        #print(bo[pos[0]][i], num, pos)
        if bo[pos[0]][i] == num and pos[1] != i:
            if i > pos[0]:
                print(i, pos[0])
                xstart = (i * 60 + 30)
                xfinish = 0               
                ystart = (pos[0]*60) + 30
                yfinish = (pos[0]*60) + 30                
                redlineList.append([xstart, xfinish, ystart, yfinish])                
            if i < pos[0]:
                print(i, pos[0])
                xstart = (i * 60 + 30)
                xfinish = 540               
                ystart = (pos[0]*60) + 30
                yfinish = (pos[0]*60) + 30
                redlineList.append([xstart, xfinish, ystart, yfinish])
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            if i > pos[1]:
                xstart = (pos[1]*60) + 30
                xfinish = (pos[1]*60) + 30           
                ystart = (i * 60 + 30)
                yfinish = 0
                redlineList.append([xstart, xfinish, ystart, yfinish])
            if i < pos[1]:
                xstart = (pos[1]*60) + 30
                xfinish = (pos[1]*60) + 30       
                ystart = (i * 60 + 30)
                yfinish = 540
                redlineList.append([xstart, xfinish, ystart, yfinish])
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                print('yo')
                return False

    return True

def drawText(win, row, col, temp):
    fnt = pygame.font.SysFont("arial", 40)


    text = fnt.render(str(temp), 1, (0, 255, 255))
    win.blit(text, (col*60 + (30 - text.get_width()/2), row*60 + (30 - text.get_height()/2)))

def drawRedlineList(win):
    print(redlineList)

    for i in range(len(redlineList)):
        red_line_draw(win, redlineList[i][0], redlineList[i][1], redlineList[i][2], redlineList[i][3])

#def solve_button():
        #[7, 8, 0, 4, 0, 0, 0, 2, 0],
# 123    [6, 0, 0, 0, 7, 5, 0, 0, 9],
        #[0, 0, 0, 6, 0, 1, 0, 7, 8],
        #[0, 0, 7, 0, 4, 0, 2, 6, 0],
# 456    [0, 0, 1, 0, 5, 0, 9, 3, 0],
        #[9, 0, 4, 0, 6, 0, 0, 0, 5],
        #[0, 7, 0, 3, 0, 0, 0, 1, 2],
# 789    [1, 2, 0, 0, 0, 7, 4, 0, 0],
        #[0, 4, 9, 2, 0, 6, 0, 0, 7]
def solve_one(board, model, win, empty, all):
    
    row, col = empty
    flag = True
    #box 1
    print(empty)
    if row <= 2 and col <= 2:
        for k in range(1,10):
            if valid(model, k, empty):
                if flag:
                    for i in range(0,3):
                        for j in range (0,3):
                            print(model[i][j], 'i',i, 'j',j, 'k:',k)
                            if (i,j) != empty:
                                if model[i][j] == 0 or model[i][j] == -1:
                                    if valid(model, k, (i, j)):
                                        flag = False
                                        print(k)
                if flag == True: 
                    drawRedlineList(win)
                    redlineList.clear()
                    reset_board(board, model)
                    return k
                if flag == False:
                    redlineList.clear()
                    flag = True        
        return -1

    #box 2

    if row <= 2 and col >=3 and col <= 5:
        for k in range(1,10):
            if valid(model, k, empty):
                if flag:
                    for i in range(0,3):
                        for j in range (3,6):
                            print(model[i][j], 'i',i, 'j',j, 'k:',k)
                            if (i,j) != empty:
                                if model[i][j] == 0 or model[i][j] == -1:
                                    if valid(model, k, (i, j)):
                                        flag = False
                                        print(k)
                if flag == True: 
                    drawRedlineList(win)
                    redlineList.clear()
                    reset_board(board, model)
                    return k
                if flag == False:
                    redlineList.clear()
                    flag = True        
        return -1
    #box 3
    if row <= 2 and col >= 6:
        for k in range(1,10):
            if valid(model, k, empty):
                if flag:
                    for i in range(0,3):
                        for j in range (6,9):
                            print(model[i][j], 'i',i, 'j',j, 'k:',k)
                            if (i,j) != empty:
                                if model[i][j] == 0 or model[i][j] == -1:
                                    if valid(model, k, (i, j)):
                                        flag = False
                                        print(k)
                if flag == True: 
                    drawRedlineList(win)
                    redlineList.clear()
                    reset_board(board, model)
                    return k
                if flag == False:
                    redlineList.clear()
                    flag = True        
        return -1
    #box 4
    #if row >=4 & row <= 6 & col < 3:

    #box 5
    #if row >=4 & row <= 6 & col >=4 & col <= 6:

    #box 6
    #if row >=4 & row <= 6 & col > 6:

    #box 7
    #if row > 6  & col < 3:

    #box 8
    #if row > 6 & col >=4 & col <= 6:

    #box 9
    #if row > 6 & col > 6:

def main():
    win = pygame.display.set_mode((540,650))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clicked = board.click(mouse)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                if 40 <= mouse[0] <= 140 and 575 <= mouse[1] <= 605:
                    #red_line_draw(win, 0, 30, 540, 30)
                    empty = find_empty(board.update_model())
                    temp = solve_one(board, board.update_model(), win, empty, False)
                    print(temp)

                    row, col = empty
                        #print(row, col)
                        #print(temp)
                        #board.selected = row, col
                        #print(board.selected)
                    if temp > 0:
                        drawText(win, row, col, temp)
                        board.place(row, col, temp)
                        print(board.update_model())
                        pygame.display.update()
                        time.sleep(2)
                    else:
                        board.place(row, col, temp)
                        print(board.update_model())
                        pygame.display.update()
                if 220 <= mouse[0] <= 320 and 575 <= mouse[1] <= 605:
                    pygame.quit()
                if 400 <= mouse[0] <= 500 and 575 <= mouse[1] <= 605:
                    pygame.quit()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False

            

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()