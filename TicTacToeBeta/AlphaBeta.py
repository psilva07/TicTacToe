__author__ = 'Pedro and Julian'

from sys import maxsize

#TreeBuilder
class Node(object):
    def __init__(self, depth, board):
        self.depth = depth
        self.board = board
        self.children = []
        """include:
        # parent - parent node
          state - heuristic value associated with the node
          action - what took you here. Tuple of two values (position, move - either -1 or 1)"""


def createChildren(node):
    #print("Depth %d" %self.depth)
    #printBoard(self)
    if node.depth < 8:
        for n in range(0,len(node.board)):
            if checkWin(node) is False and node.board[n] == 0:
                boardTemp = node.board.copy()
                boardTemp[n] = move(node.depth)
                #print(boardTemp)
                new = Node(node.depth+1, boardTemp)
                node.children.append(new)
        for k in node.children:
            createChildren(k)

#Game


#Game always starts with human, improve that later
def move(depth):
    if depth == 0 or depth % 2 == 0:
        return 1
    else:
        return -1

def checkWin(node):
    if(((node.board[0] == node.board[1] and node.board[1] == node.board[2]) or
       (node.board[0] == node.board[3] and node.board[3] == node.board[6])) and
       (node.board[0] == -1 or node.board[0] == 1)):

        #print ("Game Over!!! Player %d won!" %node.board[0])
        return True

    elif(((node.board[6] == node.board[7] and node.board[7] == node.board[8]) or
         (node.board[2] == node.board[5] and node.board[5] == node.board[8])) and
         (node.board[8] == -1 or node.board[8] == 1)):

        #print ("Game Over!!! Player %d won!" %node.board[8])
        return True

    elif(((node.board[3] == node.board[4] and node.board[4] == node.board[5]) or
         (node.board[1] == node.board[4] and node.board[4] == node.board[7]) or
         (node.board[0] == node.board[4] and node.board[4] == node.board[8]) or
         (node.board[2] == node.board[4] and node.board[4] == node.board[6])) and
         (node.board[4] == -1 or node.board[4] == 1)):

        #print ("Game Over!!! Player %d won!" %node.board[4])
        return True

    else:
        return False

def printBoard(tree):
    temp = stringTree(tree.board)
    #print("%s %s" %(temp[4], temp[4]))
    print("\n %s  | %s | %s \n ___ ___ ___\n %s  | %s | %s \n ___ ___ ___\n %s  | %s | %s \n\n" % (temp[0], temp[1], temp[2],
                                                                                                   temp[3], temp[4], temp[5],
                                                                                                   temp[6], temp[7], temp[8]))

def stringTree(tree):
    temp = []
    for i in range(0,9):
        if tree[i] == 0:
            temp.append(" ")
        elif tree[i] == -1:
            temp.append("O")
        elif tree[i] == 1:
            temp.append("X")
    return temp

def runOverTree(tree):
    print("%d" %tree.depth)
    printBoard(tree)
    for obj in tree.children:
        runOverTree(obj)

def runOverTree(tree, depth): #Given a tree and a depth only print boards on that depth

    if tree.depth == depth:
        print("%d" %tree.depth)
        printBoard(tree)
    for obj in tree.children:
        runOverTree(obj, depth)

def runOverTerminals(tree):
    if not tree.children:
        print("%d" %tree.depth)
        printBoard(tree)
    else:
        for obj in tree.children:
            runOverTerminals(obj)

def runOverTerminals(tree, depth):
    if not tree.children and tree.depth == depth:
        print("%d" %tree.depth)
        printBoard(tree)
    else:
        for obj in tree.children:
            runOverTerminals(obj, depth)

def treeSize(tree): #that's not a reliable function yet
    count = 1
    if not tree:
        return 0
    else:
        for child in tree.children:
            count += treeSize(child)
        return count



if __name__ == '__main__':
    tree = Node(0, [0, 0, 0, 0, 0, 0, -1, 0, 0])
    createChildren(tree)
    #print ("Children: %d" %len(tree.children))
    #runOverTree(tree)
    #runOverTree(tree, 2)
    #runOverTerminals(tree,5)
    #print(treeSize(tree))