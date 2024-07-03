import socket
#عشان يبعت ويستقبل 
import threading 
#دي بتتعامل مع ال ماتركس
import numpy as np
import sys
import math
import pygame 
#-----------------------------------------------------------------------------------------
host='127.0.0.1'
port=2177
conn,addr=None,None  # Initialize conn and addr variables
blue=(0,0,255)
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
yellow=(255,255,0)
pink=(255,200,200)
babyblue=(137,207,240)
navyblue=(0,0,128)
row_count=6
column_count=7
gameover=False
turn=True
flag=0
#-----------------------------------------------------------------------------------------
##create socket
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port))
##i need only 1 client to connect to server 
sock.listen(1)
#-----------------------------------------------------------------------------------------
##creating a thread 
def create_thread(targett):
    thread=threading.Thread(target=targett)
    #a type of thread that runs in the background and does not prevent the program from exiting if there are no non-daemon threads running
    thread.daemon=True
    thread.start()
#-----------------------------------------------------------------------------------------
def receiveData():
    global flag
    global gameover
    global turn
    while True:
        data ,addr=conn.recvfrom(1024)
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
                    label=myFont.render("Game Over, Player 2 won:)",1,navyblue)
                    screen.blit(label,(40,10))
                    gameover=True
        pygame.display.update()
        if dataa[2]=='yourturn':
            turn=True
            print("server turn="+str(turn))
#-----------------------------------------------------------------------------------------
##دي كل ال بتعمله ان هي بتطبع ان في ثريد اتكريت و بتعمل اكسيبت لل كلينت ال عمل كونيكتوبتستدعي لناس كلها باخر جمله 
def waiting4connection():
    print("thread created")
    global conn,addr
    conn,addr=sock.accept()
    print("client is connected")
    receiveData()
#-----------------------------------------------------------------------------------------
create_thread(waiting4connection)
#-----------------------------------------------------------------------------------------
##create board function 
def createboard():
    ## make a matrix 6*7
    board=np.zeros((6,7))
    return board
#-----------------------------------------------------------------------------------------
## piece has 3 values 0--> the place is empty , 1--> player1 & 2--> player2 
def dropPiece(board,row,column,piece):
    board[row][column]=piece
#-----------------------------------------------------------------------------------------
## we must make sure that the location chose must have the value =0 
def isValidLocation(board,column):
    ## row_column-1 becouse i have a row to write if player 1 win or not
    return board[row_count-1][column]==0
#-----------------------------------------------------------------------------------------
def nextOpenRow(board ,column):
    for row in range (row_count):
        if board[row][column] == 0:
            return row
#-----------------------------------------------------------------------------------------
## print the matrix in reverse to check the matrix in correct manner
def printBoard(board):
    print(np.flip(board,0))
#-----------------------------------------------------------------------------------------
def GameOver (board):
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
#-----------------------------------------------------------------------------------------
##check if there is 4 locations for win 
def winning_move(board,piece):
    ## check horizontal location 
    ## -3 as the column =7 
    for c in range(column_count-3):
        for r in range(row_count):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True
    
    ## check vertical location 
    for c in range(column_count):
        for r in range(row_count-3):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True
    
    # check positively sloped diagonal 
    for c in range(column_count-3):
        for r in range(row_count-3):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True

    ## check negatively sloped diagonal        
    for c in range(column_count-3):
        for r in range(3,row_count):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True
#-----------------------------------------------------------------------------------------
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
                pygame.draw.circle (screen,babyblue , (int(c*SQUARE_SIZE +SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle (screen,navyblue , (int(c*SQUARE_SIZE +SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
    pygame.display.update()

#-----------------------------------------------------------------------------------------

board=createboard()
pygame.init()
SQUARE_SIZE=100
width=column_count*SQUARE_SIZE
height=(row_count+1)*SQUARE_SIZE
size=(width,height)
## -5 is the space between each square and another 
RADIUS=int(SQUARE_SIZE/2 - 5)
screen=pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()
pygame.display.set_caption("Connect 4 - Server")
myFont=pygame.font.SysFont("algerian",40)

#-----------------------------------------------------------------------------------------

while not gameover:
    ## check if the user press on x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        
        ## postion of the mouse 
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,white,(0,0,width,SQUARE_SIZE))
            ## to get the mouse postition 
            posx=event.pos[0]
            if turn==True:
                pygame.draw.circle(screen, babyblue, (posx, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

 
        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,white,(0,0,width,SQUARE_SIZE))
        
            #handle all events happen in game 
         
            if turn==True:
                ## position where the user enter 
                posX=event.pos[0]
                ##chatGPT :O
                column=int(math.floor(posX/SQUARE_SIZE))
                

                if isValidLocation(board,column):
                    row= nextOpenRow(board,column)
                    dropPiece(board,row,column,1)
                    flag+=1

                    send_data='{}-{}-{}'.format(str(row),str(column),'yourturn').encode()
                    ############################################
                    #دا الي انا حطيته في كود السيرفر علشان اشغله امبارح
                    # المشكلة كانت انك بتحاولي تلعبي وتتكي على الكورة واصلا مفيش كونكت بين السيرفر والكلاينت
                    #فانا بقوله لو مفيش كونكت
                    if conn is not None:
                        conn.send(send_data)
                    else:
                        print("Connection not established.")

                    #conn.send(send_data)
                    ############################################
                    print(send_data)
                    turn=False
                    GameOver(board)
                    print(str(flag))
                    print(str(turn))
                    
                    if winning_move(board,1):
                        label=myFont.render("Game Over, Player 1 won :)",1 ,babyblue)
                        screen.blit(label,(40,10))
                        gameover=True
            printBoard(board)
            drawBoard(board)

#-----------------------------------------------------------------------------------------

if gameover:
    pygame.time.wait(3000)
    ## to avoid the not respose of window 
    pygame.display.quit()
    sys.exit()
 