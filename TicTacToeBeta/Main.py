__author__ = 'Pedro'

from Node import *
from Util import *
from random import randrange
from time import sleep
import subprocess as sp
from os import system, name


def heuristic_list():
    print("HEURISTICS LIST:")
    print("1 - (D1) This heuristic uses Max-Min only. In case of a tie it chooses the first node that was generated "
          "when creating the tree.")
    print("2 - (D2) This heuristic uses Max-Min only. In case of a tie uses most wins as tie breaker when choosing  "
          "between two equal paths.")
    print("3 - (D3) This heuristic uses Max-Min only. In case of a tie use closest win as tie breaker when choosing "
          "between two equal paths.")
    print("4 - (D4) This heuristic uses Max-Min only. In case of a tie chooses the path with the most wins in your next"
          " two turns as tie breaker. In the case the game is so advanced that this search is not possible it will "
          "use X as the tie breaker")
    print("5 - (S1) Select the next move based on this priority sequence: \n  1) Win by placing three in a row "
          "\n  2) Block an opponent's win move \n  3) Random mark")
    print("6 - (S1.5) Select the next move based on this priority sequence: \n  1) Win by placing three in a row \n  2) "
          "Block an opponent's win move \n  6) Mark center \n  8) Mark empty corner \n  9) Mark empty side")
    print("7 - (S2) Select the next move based on this priority sequence: \n  1) Win by placing three in a row \n  2) "
          "Block an opponent's win move \n  4) Create a fork \n  6) Mark center \n  8) Mark empty corner \n  9) Mark "
          "empty side")
    print("8 - (S3) Select the next move based on this priority sequence: \n  1) Win by placing three in a row \n  2) "
          "Block an opponent's win move \n  4) Create a fork \n  5) Block fork from an opponent \n  6) "
          "Mark center \n  7) Mark opposite corner from an opponent's mark \n  8) Mark empty corner \n  9) Mark empty "
          "side")


def flip_board(node):
    new = [x * (-1) for x in node.board]
    return new


def game(num):
    if num == 1:
        print("COMPUTER BATTLE!!!")
        heuristic_list()
        cpu1 = int(input("\nWhich heuristic should CPU1 use?"))
        cpu2 = int(input("\nWhich heuristic should CPU2 use?"))

        again = True
        while again:
            print("CPU1 is 'O' and CPU2 is 'X'.")
            initial = -1 + 2 * randrange(0, 2)
            #initial = 1
            if initial == 1:
                print("CPU2 starts this time")
                tree2 = Node(0, [0, 0, 0, 0, 0, 0, 0, 0, 0], 1)
                tree2.create_children()
                tree2.heuristic()
                current2 = tree2
                current2 = decide_move(current2, cpu2)

                tree1 = Node(0, flip_board(current2), 1)
                tree1.create_children()
                tree1.heuristic()
                current1 = tree1
                print(current1)
                turn = -1
            else:
                print("CPU1 starts this time")
                tree1 = Node(0, [0, 0, 0, 0, 0, 0, 0, 0, 0], 1)
                tree1.create_children()
                tree1.heuristic()
                current1 = tree1
                current1 = decide_move(current1, cpu1)
                #temp_board = flip_board(current1)
                tree2 = Node(0, flip_board(current1), 1)
                tree2.create_children()
                tree2.heuristic()
                current2 = tree2
                print(current1)
                #print(current2)
                turn = 1
            input("\nPress anything to continue...")
            while current1.game_result is None:
                if turn == 1:
                    print("CPU2 Turn!")
                    current2 = decide_move(current2, cpu2)
                    for child in current1.children:
                            if child.action[0] == current2.action[0]:
                                current1 = child
                else:
                    print("CPU1 Turn!")
                    current1 = decide_move(current1, cpu1)
                    for child in current2.children:
                            if child.action[0] == current1.action[0]:
                                current2 = child
                turn = -turn
                print(current1)
                input("\nPress anything to continue...")
            if current1.game_result == -1:
                print("CPU2 won!!!")
            elif current1.game_result == 1:
                print("CPU1 won!!!")
            else:
                print("Tied Game!!!")

            std = input("Want to play again?(y or n): ")
            if std == 'n':
                again = False
    elif num == 2:
        heuristic_list()
        heuristic = int(input("Choose the computer heuristic: "))
        print("I'm 'O' and you are 'X'. Good Luck!")
        wait = input("PRESS ENTER TO START THE GAME!!!")
        again = True
        while again:
            #initial = -1 + 2 * randrange(0, 2)
            initial = 1
            if initial == 1:
                print("You get to start this time")
                print_empty_board()
                allowed = False
                while not allowed:
                    pos = int(input("Enter the Position: "))
                    if pos < 1 or pos > 9:
                        print("Invalid Position!")
                    else:
                        allowed = True

                temp_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                temp_board[pos - 1] = initial
                tree = Node(0, temp_board, 1)
                print(tree)
                tree.board
                me = initial

            else:
                print("I'll start this time")
                tree = Node(0, [0, 0, 0, 0, 0, 0, 0, 0, 0], 1)
                me = -initial  # either max or min player(1 or -1)

            tree.create_children()
            tree.heuristic()
            current1 = tree
            #sleep(2)
            #print(current)

            while current1.game_result is None:
                if current1.turn == me:
                    print("My Turn!")
                    if current1.depth != 0:
                        sleep(2)
                    current1 = decide_move(current1, heuristic)
                else:
                    print("Your Turn!")
                    allowed = False
                    while not allowed:
                        pos = int(input("Enter the Position: ")) - 1
                        if pos < 0 or pos > 9:
                            print("Invalid Position!")
                        for child in current1.children:
                            if child.action[0] == pos:
                                allowed = True
                                current1 = child
                        if not allowed:
                            print("Position already used!Try again.")
                print(current1)
            if current1.game_result == 1:
                print("I won!! AI Rules!!! Sorry for that...")
            elif current1.game_result == -1:
                print("Congratulations, you beat me! I need to study more...")
            else:
                print("Tied Game!!!")

            std = input("Want to play again?(y or n): ")
            if std == 'n':
                again = False

# main
if __name__ == '__main__':
    print("TIC-TAC-TOE")
    print("That's how it works: \nEvery number(from 1 to 9) represents a position on the board.")
    print("To play in that position press the respective number.\nHere's a sample board so you can make sure you're"
          " playing in the right spot")
    print("\n 1  | 2 | 3 \n ___ ___ ___\n 4  | 5 | 6 \n ___ ___ ___\n 7  | 8 | 9 \n\n")
    print("\nReady to start?")
    wait = int(input("\nPress 1 for CPU vs CPU or 2 for Human vs CPU: "))
    game(wait)