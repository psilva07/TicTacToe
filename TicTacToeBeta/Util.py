__author__ = 'Pedro'
#util - Functions that help manage and visualize the tree


def run_over_tree(node, depth=None):  #Given a tree and a depth only print boards on that depth
    if depth is None:
        print("Depth %d" % node.depth)
        print(node)
        for child in node.children:
            run_over_tree(child)
    else:
        if node.depth == depth:
            #print("%d" % node.depth)
            print(node.value)
        for obj in node.children:
            run_over_tree(obj, depth)


def run_over_terminals(node, depth=None):
    if depth is None:
        if node.game_result is not None:
            print("%d" % node.value)
            #print(node)
        else:
            for obj in node.children:
                run_over_terminals(obj)
    else:
        if not node.children and node.depth == depth:
            print("%d" % node.depth)
            print(node)
        else:
            for obj in node.children:
                run_over_terminals(obj, depth)


def tree_size(my_tree):  #that's not a reliable function yet
    count = 0
    if not my_tree:
        return count
    else:
        for child in my_tree.children:
            count += tree_size(child)
        return 1 + count

def print_empty_board():
    print("\n    |   |   \n ___ ___ ___\n    |   |   \n ___ ___ ___\n    |   |   \n\n")
