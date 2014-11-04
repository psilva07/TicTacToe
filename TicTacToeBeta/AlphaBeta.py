__author__ = 'Pedro'

#from sys import maxsize


#TreeBuilder
class Node(object):
    def __init__(self, depth, board, parent, action, state):
        """
        Constructor for a node
        :param depth: Depth of the current node being inserted in the tree. Should start with 0.
        :param board: Board configuration at the present node.
        :param parent: Parent of current node. If node is the root this should be None.
        :param action: Tuple of two values representing the action performed from the last node to the current one.
        The first value is the position played and the second is the value played, either -1 or 1.
        :param state: Heuristic value associated with the node
        """
        self.depth = depth
        self.board = board
        self.children = []
        self.parent = parent
        self.state = state
        self.action = action

    def create_children(self):
        if self.depth < 8:
            for n in range(0,len(self.board)):
                if check_win(self) is False and self.board[n] == 0:
                    boardTemp = self.board.copy()
                    boardTemp[n] = move(self.depth)
                    new = Node(self.depth+1, boardTemp, self, (n, move(self.depth)), None)
                    self.children.append(new)
            for k in self.children:
                k.create_children()


#Game
#Game always starts with human, improve that later
def move(depth):
    """
    Function used to decide who is played next based on the depth. Bases on the fact the human begins the game and uses O.
     Needs improvement.
    :param depth: Depth of current board. Next movement will increase the deapth
    :return: Returns 1 to play X or 1 to play 0
    """
    if depth == 0 or depth % 2 == 0:
        return 1
    else:
        return -1


def check_win(node):
    """
    Given a node check if we have a board that consists in a victory. A victory happens when tree X's or O's are played
    in a row, column or diagonal.
    :param node: Receives a node to have its board checked.
    :return: Returns True if the board characterizes a victory and False otherwise.
    """
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


#util - Functions that help manage and visualize the tree
def print_board(node):
    """
    Prints a node's board in the terminal
    :param node: The node that will have the board printed.
    """
    temp = string_node(node.board)
    #print("%s %s" %(temp[4], temp[4]))
    print("\n %s  | %s | %s \n ___ ___ ___\n %s  | %s | %s \n ___ ___ ___\n %s  | %s | %s \n\n"
          % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8]))


def string_node(board):
    """
    Function used by print_board to translate the board from "-1,0,1" to "O,' ',X".
    :param board: Board that will be translated.
    :return: returns a list corresponding to the translated board
    """
    temp = []
    for i in range(0,len(board)):
        if board[i] == 0:
            temp.append(" ")
        elif board[i] == -1:
            temp.append("O")
        else:
            temp.append("X")
    return temp


def run_over_tree(tree):
    print("%d" %tree.depth)
    print_board(tree)
    for obj in tree.children:
        run_over_tree(obj)


def run_over_tree(tree, depth): #Given a tree and a depth only print boards on that depth

    if tree.depth == depth:
        print("%d" %tree.depth)
        print_board(tree)
    for obj in tree.children:
        run_over_tree(obj, depth)

def run_over_terminals(tree):
    if not tree.children:
        print("%d" %tree.depth)
        print_board(tree)
    else:
        for obj in tree.children:
            run_over_terminals(obj)

def run_over_terminals(tree, depth):
    if not tree.children and tree.depth == depth:
        print("%d" %tree.depth)
        print_board(tree)
    else:
        for obj in tree.children:
            run_over_terminals(obj, depth)

def tree_size(tree): #that's not a reliable function yet
    count = 1
    if not tree:
        return 0
    else:
        for child in tree.children:
            count += tree_size(child)
        return count


#main
if __name__ == '__main__':
    tree = Node(0, [0, 0, 0, 0, 0, 0, -1, 0, 0], None, None, None)
    tree.create_children()
    #print ("Children: %d" %len(tree.children))
    #run_over_tree(tree)
    run_over_tree(tree, 1)
    #run_over_terminals(tree,5)
    #print(tree_size(tree))