__author__ = 'Pedro'

from queue import Queue
from random import choice
#from copy import deepcopy
# from sys import maxsize
# TreeBuilder

tree_depth=0
class Node(object):

    def __init__(self, depth, board, turn, parent=None, action=None, state=None):
        """
        Constructor for a node
        :param depth: Depth of the current node being inserted in the tree. Should start with 0.
        :param board: Board configuration at the present node.
        :param turn: Defines who is currently playing, "O" or "X", -1 or 1 respectively.
        :param parent: Parent of current node. If node is the root this should be None.
        :param action: Tuple of two values representing the action performed from the last node to the current one.
        The first value is the position played and the second is the value played, either -1 or 1.
        :param state: Heuristic value associated with the node.
        """
        self.depth = depth
        self.board = board
        self.turn = turn
        self.parent = parent
        self.state = state
        self.action = action
        self.children = []
        self.value = self.game_result = self.check_win()

    def create_children(self):
        if 0 in self.board:
            for n in range(len(self.board)):
                if self.game_result is None and self.board[n] == 0:
                    board_temp = self.board.copy()
                    board_temp[n] = -self.turn
                    new = Node(self.depth + 1, board_temp, -self.turn, self, (n, -self.turn), None)
                    self.children.append(new)
                    global tree_depth
                    if self.depth + 1 > tree_depth:
                        tree_depth = self.depth + 1

            for k in self.children:
                k.create_children()

    def __repr__(self):
        """
        Overwrite the __repr__ to give a representation for a node's board.
        """
        temp = self.__string_node()
        #print("%s %s" %(temp[4], temp[4]))
        return ("\n %s  | %s | %s \n ___ ___ ___\n %s  | %s | %s \n ___ ___ ___\n %s  | %s | %s \n\n"
                % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8]))

    def __string_node(self):
        """
        Private method used by __ref__() to translate the board from "-1,0,1" to "O,' ',X" respectively .
        :return: returns a list corresponding to the translated board
        """
        temp = []
        for i in range(0, len(self.board)):
            if self.board[i] == 0:
                temp.append(" ")
            elif self.board[i] == -1:
                temp.append("O")
            else:
                temp.append("X")
        return temp

    def check_win(self):
        """
        Given a node check if we have a board that consists in a victory or draw. A victory happens when tree X's or O's are played
        in a row, column or diagonal. A draw happens if the board is full (depth 8) and no one won.
        :return: Returns 1 if circle wins, 0 if it's a draw or -1 if X wins.
        """
        if(((self.board[0] == self.board[1] and self.board[1] == self.board[2]) or
           (self.board[0] == self.board[3] and self.board[3] == self.board[6])) and
           (self.board[0] == -1 or self.board[0] == 1)):
            return -self.board[0]

        elif(((self.board[6] == self.board[7] and self.board[7] == self.board[8]) or
             (self.board[2] == self.board[5] and self.board[5] == self.board[8])) and
             (self.board[8] == -1 or self.board[8] == 1)):
            return -self.board[8]

        elif(((self.board[3] == self.board[4] and self.board[4] == self.board[5]) or
             (self.board[1] == self.board[4] and self.board[4] == self.board[7]) or
             (self.board[0] == self.board[4] and self.board[4] == self.board[8]) or
             (self.board[2] == self.board[4] and self.board[4] == self.board[6])) and
             (self.board[4] == -1 or self.board[4] == 1)):
            return -self.board[4]

        elif 0 not in self.board:
            return 0

        else:
            return None

    def heuristic(self):
            for i in reversed(range(tree_depth)):
                self.heuristic_prop(i)

    def heuristic_prop(self, depth):
        if self.depth == depth and self.children:
            self.value = self.get_value()
        else:
            for obj in self.children:
                obj.heuristic_prop(depth)

    def get_value(self):
        values = []
        for child in self.children:
            values.append(child.value)
        #print(values)
        if self.turn == 1:
            return max(values)
        else:
            return min(values)


def decide_move(dad, type):
    children = dad.children
    if type < 5:
        winner = dad.value
        #build ties list
        ties = []
        for guy in children:
            #print("child value %i" %(guy.value))
            #print(guy)
            if guy.value == winner:
                #print("PICK")
                ties.append(guy)
                #print(guy)
        sorted = False
        if len(ties) > 1:
            while not sorted:
                sorted = True
                for i in range(len(ties)-1):
                    if is_better(ties[i+1], ties[i], type):
                        sorted = False
                        ties[i], ties[i+1] = ties[i+1], ties[i]
        return ties[0]
    else:
        winner = -children[0].turn
        #1) Win by placing three in a row
        for child in children:
            if child.game_result == winner:
                #print("ONE")
                return child
        #2) Block an opponent's win move
        for child in children:
            for second in child.children:
                if second.game_result == -winner:
                    pos = second.action[0]
                    for block in children:
                        if block.action[0] == pos:
                            #print("TWO")
                            return block
        #3) Random mark
        if type == 5:
            return choice(children)

        #4) Create a fork
        if type == 7 or type == 8:
            wins_counter = 0
            for child in children:
                num = count_wins_next(child, -winner)
                if num > wins_counter:
                    wins_counter = num
                    my_choice = child
            if wins_counter > 1:
                #print("FORK")
                return my_choice

        #5) Block fork from an opponent
        if type == 8:
            loss_counter = 0
            for child in children:
                child.board[child.action[0]] = -child.turn
                num = count_losses_next(child)
                if num > loss_counter:
                    loss_counter = num
                    my_choice = child
                child.board[child.action[0]] = child.turn
            if loss_counter > 1:
                #print("FORK BLOCK")
                return my_choice

        #6) Mark center
        for child in children:
            if child.action[0] == 4:
                #print("CENTER")
                return child

        #7) Mark opposite corner from an opponent's mark
        if type == 8:
            if dad.board[0] == winner and dad.board[8] == 0 and dad.board[4] != -winner:
                for child in children:
                    if child.action[0] == 8:
                        #print("OPPOSITE SIDE")
                        return child
            elif dad.board[8] == winner and dad.board[0] == 0 and dad.board[4] != -winner:
                for child in children:
                    if child.action[0] == 0:
                        #print("OPPOSITE SIDE")
                        return child
            if dad.board[2] == winner and dad.board[6] == 0 and dad.board[4] != -winner:
                for child in children:
                    if child.action[0] == 6:
                        #print("OPPOSITE SIDE")
                        return child
            if dad.board[6] == winner and dad.board[2] == 0 and dad.board[4] != -winner:
                for child in children:
                    if child.action[0] == 2:
                        #print("OPPOSITE SIDE")
                        return child

        #8) Mark empty corner
        for child in children:
            act = child.action[0]
            if act in (0, 2, 8, 6):
                #print("EMPTY CORNER")
                return child

        #9) Mark empty side
        #print("EMPTY SIDE")
        return children[0]


def is_better(a, b, type):
    if type == 1:
        return False
    if type == 2:
        valueA = most_wins(a, a.turn)
        valueB = most_wins(b, b.turn)
        if valueA > valueB:
            return True
        return False
    if type == 4 and count_openings(a.board) >= 3:
        valueA = most_win_in_two_turns(a, a.turn)
        valueB = most_win_in_two_turns(b, b.turn)
        #print("Value A: %i" %(valueA))
        #print(a)
        #print("Value B: %i" %(valueB))
        #print(b)
        #input()
        if valueA > valueB:
            return True
        return False
    else: #if type == 3:
        valueA = shortest_win(a, a.turn)
        valueB = shortest_win(b, b.turn)
        if valueA < valueB:
            return True
        return False


def shortest_win(node, winner):
    q = Queue()
    checked = []
    q.put(node)
    path = 0
    while not q.empty():
        v = q.get()
        if v.game_result == winner:
            return v.depth
        elif v not in checked:
            for edge in v.children:
                if v not in checked:
                    q.put(edge)
            checked.append(v)
    return 10

def most_win_in_two_turns(node, winner):
    total = 0
    q = Queue()
    checked = []
    q.put(node)
    path = 0
    while not q.empty():
        v = q.get()
        if v.game_result == winner:
            total += 1
        if v not in checked:
            for edge in v.children:
                if v not in checked and v.depth <= (node.depth + 3):
                    q.put(edge)
            checked.append(v)
    return total


def most_wins(node, winner):
    total = 0
    q = Queue()
    checked = []
    q.put(node)
    path = 0
    while not q.empty():
        v = q.get()
        if v.game_result == winner:
            total += 1
        if v not in checked:
            for edge in v.children:
                if v not in checked:
                    q.put(edge)
            checked.append(v)
    return total


def count_wins_next(node, winner):
    count = 0
    for i in range(len(node.board)):
        if node.board[i] == 0:
            temp = node
            #temp = deepcopy(node)
            temp.board[i] = winner
            result = temp.check_win()
            if result == node.turn:
                count += 1
            node.board[i] = 0
    return count


def count_losses_next(node):
    count = 0
    for i in range(len(node.board)):
        if node.board[i] == 0:
            temp = node
            #temp = deepcopy(node)
            temp.board[i] = -node.turn
            result = temp.check_win()
            if result == -node.turn:
                count += 1
            node.board[i] = 0
    return count


def count_openings(board):
    count = 0
    for i in board:
        if i == 0:
            count += 1
    return count