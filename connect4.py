import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def createBoard():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def dropPiece(board, row, column, piece):
    board[row][column] = piece

def isValidLocation(board, column):
    return board[ROW_COUNT-1][column] == 0

def getNextOpenRow(board, column):
    for r in range(ROW_COUNT):
        if board[r][column] == 0:
            return r

def printBoard(board):
    print(np.flip(board, 0))

def winningMove(board, piece):
    # Horizontal Win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    
    # Vertical Win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Positive Sloped Win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Negative Sloped Win
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def drawBoard(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

    


board = createBoard()
gameOver = False
turn = 0

pygame.init()

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
drawBoard(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            # Ask for Player 1 Input
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0,width, SQUARESIZE))
            if turn == 0:
                posx = event.pos[0]
                column = int(math.floor(posx/SQUARESIZE))
                if isValidLocation(board, column):
                    row = getNextOpenRow(board, column)
                    dropPiece(board, row, column, 1)
                    if winningMove(board, 1):
                        label = myFont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        gameOver = True
            else:
                posx = event.pos[0]
                column = int(math.floor(posx/SQUARESIZE))
                if isValidLocation(board, column):
                    row = getNextOpenRow(board, column)
                    dropPiece(board, row, column, 2)
                    if winningMove(board, 2):
                        label = myFont.render("Player 2 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        gameOver = True
            
            printBoard(board)
            drawBoard(board)
            
            turn += 1
            turn = turn % 2
            if gameOver:
                pygame.time.wait(3000)

