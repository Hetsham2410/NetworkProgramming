import socket
import threading
import numpy as np
import pygame
import sys
import math

# Constants
host = '127.0.0.1'
port = 2177
blue=(0,0,255)
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
yellow=(255,255,0)
pink=(255,200,200)
babyblue=(137,207,240)
navyblue=(0,0,128)
row_count = 6
column_count = 7
gameover = False
turn = False
flag = 0

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

def create_thread(targett):
    thread = threading.Thread(target=targett)
    thread.daemon = True
    thread.start()

def receiveData():
    global flag, gameover, turn
    while True:
        data = client_socket.recv(1024)
        data2=data.decode()
        dataa=data2.split('-')
        row=int(dataa[0])
        column=int(dataa[1])
        if turn == False:
            if isValidLocation(board,column):
                row=nextOpenRow(board,column)
                dropPiece(board,row,column,2)
                drawBoard(board)
                print(str(flag))
                if winning_move(board,2):
                    label=myFont.render("Game Over, Player 1 won :)",1,babyblue)
                    screen.blit(label,(40,10))
                    gameover=True
        pygame.display.update()
        if dataa[2]=='yourturn':
            turn=True
            print("server turn="+str(turn))

def isValidLocation(board, column):
    return board[row_count - 1][column] == 0

def nextOpenRow(board, column):
    for row in range(row_count):
        if board[row][column] == 0:
            return row

def dropPiece(board, row, column, piece):
    board[row][column] = piece
## print the matrix in reverse to check the matrix in correct manner
def printBoard(board):
    print(np.flip(board,0))
def drawBoard(board):
    ## this for loop to move on all elements 
    for c in range (column_count):
        for r in range (row_count):
            ## draw rectangle shape 
               ## rect(surface, color ,rect,width)
            pygame.draw.rect(screen,pink,(c*SQUARE_SIZE ,r*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE , SQUARE_SIZE))
            pygame.draw.circle(screen, white, (int (c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r* SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE /2)), RADIUS)
    for c in range (column_count):
        for r in range (row_count):
            if board[r][c]==1:
                pygame.draw.circle (screen,navyblue , (int(c*SQUARE_SIZE +SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle (screen,babyblue , (int(c*SQUARE_SIZE +SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
    pygame.display.update()

def GameOver(board):
    global gameover
    ## it counts to 42 if there is no player won 
    if flag == 42 and not winning_move(board,1) and not winning_move(board,2):
        ##print this on screen 
        label=myFont.render("Game Over, Match Tied :(",1,green)
        screen.blit(label,(40,10))
        pygame.display.update()
        ## wait 3 sec then  make gameover 
        pygame.time.wait(3000)
        gameover=True
        pygame.display.quit()
        sys.exit()

def winning_move(board, piece):
    for c in range(column_count - 3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    for c in range(column_count):
        for r in range(row_count - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    for c in range(column_count - 3):
        for r in range(row_count - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    for c in range(column_count - 3):
        for r in range(3, row_count):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
    return False

create_thread(receiveData)

board = np.zeros((row_count, column_count), dtype=int)

pygame.init()
SQUARE_SIZE = 100
width = column_count * SQUARE_SIZE
height = (row_count + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 - Client")
myFont=pygame.font.SysFont("algerian",40)
while not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, white, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn:
                pygame.draw.circle(screen, navyblue, (posx, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, white, (0, 0, width, SQUARE_SIZE))
            if turn:
                posX = event.pos[0]
                column = int(math.floor(posX / SQUARE_SIZE))

                if isValidLocation(board, column):
                    row = nextOpenRow(board, column)
                    dropPiece(board, row, column, 1)
                    drawBoard(board)
                    flag += 1

                    send_data = '{}-{}-{}'.format(row, column, 'yourturn').encode()
                    client_socket.send(send_data)
                    print(send_data)
                    turn = False
                    GameOver(board)
                    print(str(flag))
                    print(str(turn))

                    if winning_move(board, 1):
                        label=myFont.render("Game Over, Player 2 won :)",1 ,navyblue)
                        screen.blit(label,(40,10))
                        gameover = True
            printBoard(board)
            drawBoard(board)
            # pygame.display.update()



if gameover:
    pygame.time.wait(3000)
    ## to avoid the not respose of window 
    pygame.display.quit()
    sys.exit()