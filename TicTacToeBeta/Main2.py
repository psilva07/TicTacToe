__author__ = 'Pedro'

from Node import *
from random import randrange
from os import system

def flip_board(node):
    new = [x * (-1) for x in node.board]
    return new

def game(cpu1, cpu2, interactions):
    scores = {"-1s": [0, 0, 0, 0], "-1ns": [0, 0, 0, 0], "1s": [0, 0, 0, 0], "1ns": [0, 0, 0, 0],}
    for runs in range(interactions):
        print("%i.." % (runs + 1))
        initial = -1 + 2 * randrange(0, 2)
        #initial = 0
        if initial == 1:
            #print("CPU2 starts this time")
            key = "-1s"
            antkey = "1ns"
            scores[key][0] += 1
            scores[antkey][0] += 1

            tree2 = Node(0, [0, 0, 0, 0, 0, 0, 0, 0, 0], 1)
            tree2.create_children()
            tree2.heuristic()
            current2 = tree2
            current2 = decide_move(current2, cpu2)

            tree1 = Node(0, flip_board(current2), 1)
            tree1.create_children()
            tree1.heuristic()
            current1 = tree1
            #print(current1)
            turn = -1
        else:
            #print("CPU1 starts this time")
            key = "1s"
            antkey = "-1ns"
            scores[key][0] += 1
            scores[antkey][0] += 1

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
            #print(current1)
            turn = 1

        while current1.game_result is None:
            if turn == 1:
                #print("CPU2 Turn!")
                current2 = decide_move(current2, cpu2)
                for child in current1.children:
                        if child.action[0] == current2.action[0]:
                            current1 = child
            else:
                #print("CPU1 Turn!")
                current1 = decide_move(current1, cpu1)
                for child in current2.children:
                        if child.action[0] == current1.action[0]:
                            current2 = child
            turn = -turn
        if current1.game_result == -1:
            if key == "-1s":
                scores[key][1] += 1
                scores[antkey][2] += 1
            else:
                scores[antkey][1] += 1
                scores[key][2] += 1
        elif current1.game_result == 1:
            if key == "1s":
                scores[key][1] += 1
                scores[antkey][2] += 1
            else:
                scores[antkey][1] += 1
                scores[key][2] += 1
        else:
            scores[key][3] += 1
            scores[antkey][3] += 1
    return scores


# main
if __name__ == '__main__':
    print("TIC-TAC-TOE")
    print("COMPUTER BATTLE!!!")
    heuristics_list = [1,2,3,4,5,6,7,8]
    for heuristic_1 in heuristics_list:
        for heuristic_2 in heuristics_list:
            if heuristic_1 == 5 or heuristic_2 == 5:
                final = game(heuristic_1, heuristic_2, 10)
            else:
                final = game(heuristic_1, heuristic_2, 5)
            print("\n%i VS %i" %(heuristic_1,heuristic_2))
            print("Heuristic1 %i started: %i times, %i wins, %i losses, %i draws" %(heuristic_1, final["1s"][0], final["1s"][1], final["1s"][2], final["1s"][3]))
            print("Heuristic1 %i didn't started: %i times, %i wins, %i losses, %i draws" %(heuristic_1, final["1ns"][0], final["1ns"][1], final["1ns"][2], final["1ns"][3]))
            print("\nHeuristic2 %i started: %i times, %i wins, %i losses, %i draws" %(heuristic_2, final["-1s"][0], final["-1s"][1], final["-1s"][2], final["-1s"][3]))
            print("Heuristic2 %i didn't started: %i times, %i wins, %i losses, %i draws\n" %(heuristic_2, final["-1ns"][0], final["-1ns"][1], final["-1ns"][2], final["-1ns"][3]))
            #system('say "Tic Tac Toe"')
        heuristics_list.remove(heuristic_1)