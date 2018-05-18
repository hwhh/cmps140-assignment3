class Graph:

    def __init__(self, my_board, opp_board, max_depth):
        # initiate the first/root node to be at depth 0 and pointing to itself
        root_node = Node(my_board, opp_board, 0, -1, -1)
        self.root = root_node
        self.maxDepth = max_depth  # the max depth to consider moves

    def get_move(self):
        """
        This function simply returns the column from the minimax graphs's top
        values. In the case there is more than one column equally-well rated,
        we will the one closest to the center.
        """
        best_value = self.root.value
        root_children = self.root.children
        best_columns = [c.col for c in root_children if c.value == best_value]
        if best_columns:
            if len(best_columns) > 1:
                # return the column closest to the center, if they are all equal
                return min(best_columns, key=lambda x: 3-x)
            else:
                return best_columns[0]
        raise Exception("Failed to find best value")

    def construct_tree(self, b, ai, parent_node, my_board, opp_board, depth):
        """
        Likely the most complex function, this builds the tree of possibilities
        by brute forcing through all possible configurations up to a given depth
        (maxDepth). It works by getting the legal locations of where a place can
        be placed, and setting those bits (equivalent to placing a token). Once
        the board is either won or the max depth is reached, we evaluate the
        board. When the function pops out, it creates the value of the parent
        node based on its children values (maxmizing the values if we are
        playing or minimizing if the opponent is playing). On a high level, we
        are presuming both players will play the optimal moves and we want to
        maxmize our reward and minimize the opponent's rewards. We alternate
        back and forth from maximizing and minizming the reward after the
        lowest tree values have been filled.
        tl;dr This function fills a minimax tree.
        The function runs in O(7^d) (d=maxDepth), but the true expansion is
        considerably less than this after the move # + depth >= 4, because we
        stop branches where there is a win and all seven columns are not
        necessarily available.
        """
        b_my_turn = (depth % 2 == 1)

        possible_bits = ai.get_legal_locations(my_board | opp_board)
        children_nodes = []

        for colbitTuple in possible_bits:
            won = False
            col = colbitTuple[0]

            if b_my_turn:  # it's my turn, so add to my board
                tmp_my_board = ai.setNthBit(my_board, colbitTuple[1])
                tmp_opp_board = opp_board
                won = b.has_won(tmp_my_board)
            else:  # it's the oppnent's turn, so we simulate their move
                tmp_my_board = my_board
                tmp_opp_board = ai.setNthBit(opp_board, colbitTuple[1])
                won = b.has_won(tmp_opp_board)

            my_node = Node(tmp_my_board, tmp_opp_board, depth, parent_node, col)

            # stop expanding the branch if the game is won | max depth = reached
            if won or depth == self.maxDepth:
                my_node.value = ai.evalCost(b, tmp_opp_board, tmp_my_board, b_my_turn)
            else:
                self.construct_tree(b, ai, my_node,
                                    tmp_my_board, tmp_opp_board, depth+1)
                my_node.setValueFromChildren()

            children_nodes.append(my_node)

        parent_node.children = children_nodes
        parent_node.setValueFromChildren()

    @staticmethod
    def create_node_children(ai, node):
        """
        This function will look at all the possible locations you can play
        pieces and create their respective nodes. After this list of nodes is
        created it is added to the inital's node class variable children.
        """
        b_my_turn = node.depth % 2
        possible_bits = ai.get_legal_locations(node.myBoard | node.oppBoard)
        children_nodes = []
        for colbitTuple in possible_bits:
            col = colbitTuple[0]
            if b_my_turn:
                tmp_my_board = ai.setNthBit(node.myBoard, colbitTuple[1])
                tmp_opp_board = node.oppBoard
            else:
                tmp_my_board = node.myBoard
                tmp_opp_board = ai.setNthBit(node.oppBoard, colbitTuple[1])
            child_node = Node(tmp_my_board, tmp_opp_board, node.depth+1, node, col)
            children_nodes.append(child_node)
        node.children = children_nodes

    def alphabeta(self, b, ai, node, depth, alpha, beta):
        """
        Constructs the tree using alphabeta, this is quite similar to the raw
        minimax used in the construct tree, however it is considerably faster
        because it removes branches that cannot be used. Simply put, it takes
        advantage of the minimax's attribute to maxmize and then minimize the
        nodes' values. For instance, if you have a bottom value of 5 and find
        a value of -100 at the bottom, you can ignore the entire branch because
        you know it will be minizmized before reaching the top.
        On my laptop, this equates to an increase from depth 5 to 7 for a max
        wait of ~2 seconds over non-optimized minimax.
        """
        is_turn = node.depth % 2 == 0  # if it's the AI's turn, we should maxmize
        if depth == 0 or node.depth == self.maxDepth:
            if node.value is None:
                node.value = ai.evalCost(b, node.myBoard, node.oppBoard, is_turn)
            return node.value

        self.create_node_children(ai, node)
        if is_turn:
            v = float('-inf')
            for child in node.children:
                v = max(v, self.alphabeta(b, ai, child, depth-1, alpha, beta))
                alpha = max(alpha, v)
                if node.value is None or alpha > node.value:
                    node.value = alpha
                if beta <= alpha:
                    node.value = None
                    break
            return v
        else:
            v = float('inf')
            for child in node.children:
                v = min(v, self.alphabeta(b, ai, child, depth-1, alpha, beta))
                beta = min(beta, v)
                if node.value is None or beta < node.value:
                    node.value = beta
                if beta <= alpha:
                    node.value = None
                    break
            return v


class Node:
    def __init__(self, my_board, opp_board, depth, parent_node, col, value=None):
        self.myBoard = my_board
        self.oppBoard = opp_board
        self.value = value
        self.depth = depth
        if depth == 0:  # if the node is the root
            self.parent = self  # set the parent node to itself
        else:
            self.parent = parent_node
        self.children = []
        self.col = col

    def setValueFromChildren(self):
        """
        Get the value of a node based on its children, minimizing if value if
        it's the opponent turn or maxmizing if it's before my turn.
        """
        if self.children and self.value is None:
            if self.depth % 2:
                self.value = min(c.value for c in self.children)
            else:
                self.value = max(c.value for c in self.children)
            return self.value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, node):
        return self.value == node.value

    def __lt___(self, node):
        return self.value < node.value

    def __gt__(self, node):
        return self.value > node.value