# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# STUDENT OATH:
# -------------
#
# "I declare that the attached project is wholly my own work in accordance
# with Seneca Academic Policy. No part of this project has been copied
# manually or electronically from any other source (including web sites) or
# distributed to other students."
#
# Name   Adnan Azad  Student ID  021244157

# reference used: primer for prg550 assignment #1

import copy
import random
import string

def main():
    """
    + Calls playBattleship()
    """
    playBattleship()


def playBattleship():
    """
    playBattleship
    + Calls all other functions below and will be the only function that is
      called from the main script.
    """
    # Game end if: missiles run out or all boats sunk
    # all basic data creation
    total_missile = 50
    missiles_away = 00
    current_score=00
    hit_or_miss = 'none'
    coord_record=[]
    coord_type='none'
    cols = random.randint(10, 35) # x-axis
    rows = random.randint(10, 35) # y-axis
    colString = "  " + string.digits[1:] + string.ascii_uppercase[:cols-9]
    rowString = string.digits[1:] + string.ascii_uppercase[:rows-9]
    # 2D array generation rows x cols
    water_board = [['~' for i in range(cols)] for j in range(rows)]
    char_value_dict={'A':10,'B':11,'C':12,'D':13,'E':14,'F':15,'G':16,'H':17,
                    'I':18,'J':19,'K':20,'L':21,'M':22,'N':23,'O':24,'P':25,
                    'Q':26,'R':27,'S':28,'T':29,'U':30,'V':31,'W':32,'X':33,
                    'Y':34,'Z':35,}
        
    # create game board with ships and everything
    ship_board, water_board = initGame(missiles_away,total_missile,
                                       current_score,hit_or_miss, coord_record,
                                       water_board,rows,cols,rowString,colString)
    
    # while missiles havent run out or score hasn't reached 160
    while (total_missile!=0 or current_score != 160):
        u_coord = input("Enter Target Coordinates--> ").upper() # user coordinates
        move_validity,coord_type = checkMove(ship_board,coord_record,coord_type,u_coord,rowString,
                                             colString,char_value_dict)
    
        # keep asking user for input until input is valid
        while move_validity == -1: # while invalid
            print ("Invalid Coordinate! Try again")
            u_coord = input("Enter Target Coordinates--> ").upper() # recollect input
            move_validity,coord_type = checkMove(ship_board,coord_record,coord_type,u_coord,rowString,
                                                 colString,char_value_dict)
        # if valid move
        if move_validity != -1:
            internal_u_coord,coord_type = checkMove(ship_board,coord_record,coord_type,u_coord,
                                                    rowString,colString,
                                                    char_value_dict)
            # call updateData and collect game information
            (hit_or_miss, coord_record,
             missiles_away,current_score,
             total_missile) = updateData(missiles_away,total_missile,
                          current_score,coord_type,internal_u_coord,u_coord,
                          ship_board,water_board,rows,cols,rowString,colString,
                          hit_or_miss,char_value_dict)
            # re-draw gameboard
            drawGame(missiles_away,total_missile,current_score,hit_or_miss,
                 coord_record,water_board,rows,cols,rowString,colString)
    if (current_score == 160): #won the game
        print("CONGRATULATIONS! You've Won!")
    elif (missiles_away==50): # lost the war, used up all missiles
        print("Sorry! You've Lost the war!")
        drawGame(missiles_away,total_missile,current_score,hit_or_miss,
             coord_record,ship_board,rows,cols,rowString,colString)
        
def validMove(board,coord_record,u_coord,rowString,colString,char_value_dict):
    # less than 2 characters entered
    if (len(u_coord)<=1):
        return -1
    row_index = u_coord[1]
    col_index = u_coord[0]
    delta = 0
    # Check if coord is within bounds
    # invalid coordinates
    if col_index not in colString: # col out of bounds
        return -1
    elif row_index not in rowString: # row out of bounds
        return -1
    elif (len(u_coord)>2): # more than 2 characters entered
        return -1
    elif coord_record != []:
        if str(u_coord)in coord_record[0]: # if previous move
            return -1
    elif board[int(row_index)-1][int(col_index)-1] == "X": # if already fired here
        return -1
            
    return delta
    
def checkMove(board,coord_record,coord_type,u_coord,rowString,colString,char_value_dict):
    """
    checkMove
    + Validates the player's coordinate input (you must accept player's input as a
      string only) and 
    + sends back the numeric index that the coordinate 
      corresponds to or 
      + the value -1 if the coordinate entered is invalid.
      For example, if 'coord' is "11", checkMove would return 0 
      (first column of first row), "12"->1, "13"->2, etc.
    - finding the difference provides the accurate row selected (delta)
      to select col, do delta = delta+delta. is row_index > col_index
      if col_index > row_index then delta = delta-delta
      if col_index == row_index then
    """
    row_index = u_coord[1]
    col_index = u_coord[0]
    delta = 0
    
    # Check if coord is within bounds
    # invalid coordinates
    delta = validMove(board,coord_record,u_coord,rowString,colString,char_value_dict)
    if delta == -1:
        pass
    # valid coordinates
    else:
        if col_index.isalpha(): # check to see if first char is letter
            if row_index.isalpha(): # check to see if second char is letter
                # Case: CHAR,CHAR
                coord_type = "cc"
                # greater value - lower value to find difference
                if (char_value_dict.get(col_index)>char_value_dict.get(row_index)):
                    delta = char_value_dict.get(col_index)-char_value_dict.get(row_index)
                elif (char_value_dict.get(row_index)>=char_value_dict.get(col_index)):
                    delta = char_value_dict.get(row_index)-char_value_dict.get(col_index)
            elif row_index.isnumeric(): # check to see if second char is num
                # Case: CHAR,NUM
                coord_type = "cn"
                delta = char_value_dict.get(col_index)-int(row_index)
        elif col_index.isnumeric(): # check to see if first char is num
            if row_index.isalpha(): # check to see if second char is letter
                # Case: NUM/col,CHAR/row
                coord_type = "nc"
                # find difference between the two values
                delta = char_value_dict.get(row_index)-int(col_index)
            elif row_index.isnumeric(): # check to see if second char is num
                # Case: NUM,NUM
                coord_type = "nn"
                # find difference between the two values
                if int(row_index)>int(col_index):   
                    delta = int(row_index)-int(col_index)
                elif col_index>=row_index: 
                    delta = int(col_index)-int(row_index)
    return delta,coord_type
      
def drawGame(missiles_away,total_missile,current_score,hit_or_miss,
             coord_record,board,rows,cols,rowString,colString):
    """
    drawGame
    + Draws the game board by displaying all of the characters
      (including the leading and trailing '|' character) on the screen
      (properly labeled 1 to (up to) Z for rows and columns, and the game title
      "Python Battleship..." at the top (see below for a sample run of the game).
    + This function is called to "redraw" the screen for each valid coordinate 
      the player enters.
    """
    #print("rows: ", rows, " cols: ", cols)
    """
    using the string module character set constants to generate the top and
    left side labels
    """
    # printing actual water board
    print("  \nPython Battleship...")
    print(colString)
    for i in range(rows) :
        print(rowString[i] + "|", end="")
        for j in range(cols):
            print(str(board[i][j]),end="")
        print("|")
    # print scorings and such
    print("Missiles Away:",str(missiles_away),"  Missiles Left:",str(total_missile))
    print("Current Score:",str(current_score),end="   ")
    if coord_record==[]:
        print("Last Move: ")
    else:
        print("Last Move: ", str(hit_or_miss)," on ", str(coord_record[0]))
    return board

def updateData(missiles_away,total_missile,current_score,coord_type,
               internal_u_coord,u_coord,ship_board,water_board,rows,cols,
               rowString,colString,hit_or_miss,char_value_dict):
    """
    updateData
    + After a player chooses a valid coordinate, this
      function updates the 'board' by placing either an 'X' (for a miss)
      or revealing a ship's character (for a hit). 
    + As well, this function updates the missile totals, previous move, and
      player's score.
    """

    coord_record=[] # used to store last known coordinate
    coord_record.append(u_coord)
    # coord = num,num
    coord_col=u_coord[0]
    coord_row=u_coord[1]

    if coord_type=='nn':
        # check if hit or miss
        if ship_board[int(coord_row)-1][int(coord_col)-1] == "~":
            ship_board[int(coord_row)-1][int(coord_col)-1]="X"
            water_board[int(coord_row)-1][int(coord_col)-1]="X"
            hit_or_miss = 'Miss!'
        else: # if hit
            hit_or_miss = 'Hit!'
            water_board[int(coord_row)-1][int(coord_col)-1]=ship_board[int(coord_row)-1][int(coord_col)-1]
            
    elif coord_type=='nc': # col num, row char
        char_value_row=char_value_dict.get(coord_row)
        # check if hit or miss
        if ship_board[char_value_row-1][int(coord_col)-1] == "~":
            ship_board[char_value_row-1][int(coord_col)-1]="X" 
            water_board[char_value_row-1][int(coord_col)-1]="X" 
            hit_or_miss = 'Miss!'
        else: # if hit
            hit_or_miss = 'Hit!'
            water_board[char_value_row-1][int(coord_col)-1]=ship_board[char_value_row-1][int(coord_col)-1]
    
    elif coord_type=='cn': # col char, row num
        char_value_col=char_value_dict.get(coord_col)
        # check if hit or miss
        if ship_board[int(coord_row)-1][char_value_col-1] == "~":
            ship_board[int(coord_row)-1][char_value_col-1]="X" 
            water_board[int(coord_row)-1][char_value_col-1]="X" 
            hit_or_miss = 'Miss!'
        else: # if hit
            hit_or_miss = 'Hit!'
            water_board[int(coord_row)-1][char_value_col-1]=ship_board[int(coord_row)-1][char_value_col-1]
    
    elif coord_type=='cc': # col char, row char
        char_value_row=char_value_dict.get(coord_row)
        char_value_col=char_value_dict.get(coord_col)
        # check if hit or miss
        if ship_board[char_value_row-1][char_value_col-1] == "~":
            ship_board[char_value_row-1][char_value_col-1]="X" 
            water_board[char_value_row-1][char_value_col-1]="X" 
            hit_or_miss = 'Miss!'
        else: # if hit
            hit_or_miss = 'Hit!'
            water_board[char_value_row-1][char_value_col-1]=ship_board[char_value_row-1][char_value_col-1]
    # if hit, increase score
    if (hit_or_miss=='Hit!'): current_score=current_score+5
    missiles_away=missiles_away+1
    total_missile=total_missile-1
    return (hit_or_miss, coord_record,
         missiles_away,current_score,
         total_missile)
      

def initGame(missiles_away,total_missile,current_score,hit_or_miss,
             coord_record,board,rows,cols,rowString,colString):
    """
    initGame
    + Initializes the entire game board and calls the "loadShips" function
      5 times (once for each ship) (see below) randomly.
    """
    # generating random numbers from 10 to 35 inclusive
    # create empty board and send to loadShips()
    water_board = drawGame(missiles_away,total_missile,current_score,hit_or_miss,
             coord_record,board,rows,cols,rowString,colString)
    
    # should run for 5 times, once for each ship, populate empty board 
    ship_board = loadShips(water_board,rows,cols) 
    
    return ship_board, water_board



def loadShips(water_board, rows, cols):
    """
    loadShips
    + Randomly places all 'ships' onto the board making sure that the ship will
      "fit" on a single row starting at a specific coordinate.
      For instance, the aircraft carrier (10 characters in length) can only
      be placed starting at a column that is 10 or more positions LEFT of the
      right game boundary (determined by the dimensions of the board).
      The reasons you may not be able to place a ship at the position randomly
      generated are:
      1. would place ship beyond column boundary, or
      2. would overlap (conflict) with an existing ship's position.
    """
    board= copy.deepcopy(water_board)
    # Ships list contains all Ships
    ships = ["[CCCCCCC=>", "[BBBBB=>", "[DDD=>", "[SS=>", "[F>"]    
    # print("rows: ", rows, " cols: ", cols)
    # use loop to print the ships into the internal board
    for item in ships :
        #print(item)
        #print("ship: ", item, " len of ship: ", len(item))

        placed = False
        while placed == False :
            (y, x) = (random.randint(0, rows - 1), random.randint(0, cols-len(item)))
            # print("x:", x, " y: ", y)
            for coord in board[y][x:]:
                if coord != '~' :
                    placed = False
                    break
                else :
                    placed = True
        # can now place ship at (y, x) (rows and cols)
        for index in range(len(item)) :
            board[y][x + index] = item[index]

    # print(board)
    return board # return ship populated board



main()
