__author__ = 'Pedro'

from Node import *
from random import randrange
from os import system


def game(cpu1, cpu2, interactions):
    scores = {"-1s": [0, 0, 0, 0], "-1ns": [0, 0, 0, 0], "1s": [0, 0, 0, 0], "1ns": [0, 0, 0, 0],}
    # scores[-1] = [0,0,0,0] #who started, wins, losses, draws
    #scores[1] = [0,0,0,0]
    for runs in range(interactions):
        board_keeper = []
        print("%i.." % (runs + 1))
        #clear()
        #heuristic_list()
        #clear()
        #print("CPU1 is 'O' and CPU2 is 'X'.")
        initial = -1 + 2 * randrange(0, 2)
        if initial == 1:
            #print("CPU2 starts this time")
            key = "1s"
            antkey = "-1ns"
            scores[key][0] += 1
            scores[antkey][0] += 1
            tree2 = Node(0, [0, 0, 0, 0, 0, 0, 0, 0, 0], -initial)
            turn = -initial  # either max or min player(1 or -1)
            tree2.create_children()
            tree2.heuristic()
            current = tree2
        else:
            #print("CPU1 starts this time")
            key = "-1s"
            antkey = "1ns"
            scores[key][0] += 1
            scores[antkey][0] += 1
            #scores[-1][0] += 1
            tree1 = Node(0, [0, 0, 0, 0, 0, 0, 0, 0, 0], -initial)
            turn = initial  # either max or min player(1 or -1)
            tree1.create_children()
            tree1.heuristic()
            current = tree1
        #sleep(1)
        #print(current)
        #input("\nPress anything to continue...")

        while current.game_result is None:
            if current.turn == turn:
                #if current.depth != 0:
                #    print("CPU2 Turn!")
                #if current.depth > 2:
                #    sleep(2)
                current = decide_move(current, cpu2)
            else:
                #if current.depth != 0:
                #    print("CPU1 Turn!")
                #if current.depth > 2:
                #   sleep(2)
                current = decide_move(current, cpu1)
                #print(current)
                #input("\nPress anything to continue...")
            board_keeper.append(current)
        if current.game_result == -1:
            if key == "-1s":
                scores[key][1] += 1
                scores[antkey][2] += 1
            else:
                scores[antkey][1] += 1
                scores[key][2] += 1
        elif current.game_result == 1:
            if key == "1s":
                scores[key][1] += 1
                scores[antkey][2] += 1
                for board in board_keeper:
                    print(board)
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
    # print("\nReady to start?")
    #int(input("\nPress 1 for CPU vs CPU or 2 for Human vs CPU: "))
    heuristic_1 = 5
    heuristic_2 = 8
    #print("1 = Heuristic ", heuristic_1)
    #print("-1 = Heuristic ", heuristic_2)
    final = game(heuristic_2, heuristic_1, 40)
    print("Heuristic1 %i started: %i times, %i wins, %i losses, %i draws" %(heuristic_1, final["1s"][0], final["1s"][1], final["1s"][2], final["1s"][3]))
    print("Heuristic1 %i didn't started: %i times, %i wins, %i losses, %i draws" %(heuristic_1, final["1ns"][0], final["1ns"][1], final["1ns"][2], final["1ns"][3]))
    print("\nHeuristic2 %i started: %i times, %i wins, %i losses, %i draws" %(heuristic_2, final["-1s"][0], final["-1s"][1], final["-1s"][2], final["-1s"][3]))
    print("Heuristic2 %i didn't started: %i times, %i wins, %i losses, %i draws" %(heuristic_2, final["-1ns"][0], final["-1ns"][1], final["-1ns"][2], final["-1ns"][3]))
    system('say "Tic Tac Toe"')
    #print(final)