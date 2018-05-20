import math
import sys

import numpy as np

# (starting coordinate, direction)
N = ([(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)], (-1, 0))
E = ([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)], (0, 1))
NE = ([(3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3)], (-1, 1))
SE = ([(5, 3), (5, 4), (5, 5), (5, 6), (4, 6), (3, 6)], (-1, -1))

scores = [[3, 4, 5, 7, 5, 4, 3],
          [4, 6, 8, 10, 8, 6, 4],
          [5, 8, 11, 13, 11, 8, 5],
          [5, 8, 11, 13, 11, 8, 5],
          [4, 6, 8, 10, 8, 6, 4],
          [3, 4, 5, 7, 5, 4, 3]]

infinity = float('inf')


class AIPlayer:

    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.lines = self.create_lines(self)
        self.ab_count = 0

    @staticmethod
    def switch_player(player):
        if player == 1:
            return 2
        else:
            return 1

    @staticmethod
    def generate_moves(board, player):
        boards = []
        transposed_board = list(map(list, zip(*board)))
        for c1, col in enumerate(transposed_board):
            temp_board = transposed_board[:]
            try:
                pos = next(i for i, v in zip(range(len(col) - 1, -1, -1), reversed(col)) if v == 0)
                new_col = col[:]
                new_col[pos] = player
                temp_board[c1] = new_col
                boards.append(list(map(list, zip(*temp_board))))
            except StopIteration:
                continue
        return np.array(boards)

    @staticmethod
    def create_lines(self):
        lines = []
        for x in N[0]:
            lines.append(((self.create_line(x[0], x[1], N[1][0], N[1][1])), (N[1][0], N[1][1])))
        for x in E[0]:
            lines.append(((self.create_line(x[0], x[1], E[1][0], E[1][1])), (E[1][0], E[1][1])))
        for x in NE[0]:
            lines.append(((self.create_line(x[0], x[1], NE[1][0], NE[1][1])), (NE[1][0], NE[1][1])))
        for x in SE[0]:
            lines.append(((self.create_line(x[0], x[1], SE[1][0], SE[1][1])), (SE[1][0], SE[1][1])))
        return lines

    @staticmethod
    def create_line(x, y, d1, d2):
        line = []
        while 0 <= x <= 5 and 0 <= y <= 6:
            line.append((x, y))
            x += d1
            y += d2
        return line

    @staticmethod
    def check_empty(line, board):
        for pos in line:
            if board[pos[0]][pos[1]] != 0:
                return False
        return True

    @staticmethod
    def get_move(current_board, best_board):
        transposed_current_board = list(map(list, zip(*current_board)))
        transposed_best_board = list(map(list, zip(*best_board)))
        for (count, col) in enumerate(transposed_current_board):
            if not np.array_equal(col, transposed_best_board[count]):
                return count

    def get_alpha_beta_move(self, board):
        depth = 4
        alpha, beta, best_value = -infinity, infinity, -infinity
        turns = self.generate_moves(board, self.player_number)
        best_turn = turns[0]
        for (count, node) in enumerate(turns):
            current_value = self.alphabeta(node, depth - 1, depth, alpha, beta, self.switch_player(self.player_number))
            self.ab_count += 1
            if current_value > best_value:
                best_value = current_value
                best_turn = node
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return self.get_move(board, best_turn)

    def alphabeta(self, node, depth, level, alpha, beta, player):
        if depth == 0 and level % 2 == 0:
            return self.evaluation_function(node, level, player)
        elif depth == 0 and level % 2 != 0:
            return self.evaluation_function(node, level, self.switch_player(player))
        elif self.check_win(node) > 0:
            if self.check_win(node) == self.player_number:
                return 100000
            else:
                return -100000
        if player == self.player_number:
            best_value = -infinity
            for child in self.generate_moves(node, player):
                self.ab_count += 1
                best_value = max(best_value,
                                 self.alphabeta(child, depth - 1, level, alpha, beta, self.switch_player(player)))
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = infinity
            for child in self.generate_moves(node, player):
                self.ab_count += 1
                best_value = min(best_value,
                                 self.alphabeta(child, depth - 1, level, alpha, beta, self.switch_player(player)))
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    def get_expectimax_move(self, board):
        depth = 4
        alpha, beta, best_value = -infinity, infinity, -infinity
        turns = self.generate_moves(board, self.player_number)
        best_turn = turns[0]
        for (count, node) in enumerate(turns):
            current_value = self.expectimax(node, depth - 1, 1, self.switch_player(self.player_number), True, alpha,
                                            beta)
            if current_value > best_value:
                best_value = current_value
                best_turn = node
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return self.get_move(board, best_turn)

    """
    
    """

    def expectimax(self, node, depth, level, player, chance_node, alpha, beta):
        if depth == 0 and level % 2 == 0:
            return self.evaluation_function(node, level, player)
        elif depth == 0 and level % 2 != 0:
            return self.evaluation_function(node, level, self.switch_player(player))
        # elif self.check_win(node) > 0:
        #     return self.evaluation_function(node, level, player)
        elif chance_node:
            alpha = 0
            children = self.generate_moves(node, player)
            for child in children:
                alpha += ((1 / len(child)) * self.expectimax(child, depth - 1, level + 1, self.switch_player(player),
                                                             False, alpha, beta))
            return alpha
        else:
            best_value = -infinity
            for child in self.generate_moves(node, player):
                best_value = max(best_value,
                                 self.expectimax(child, depth - 1, level + 1, self.switch_player(player), True, alpha,
                                                 beta))
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value

    def evaluation_function(self, board, level, player):
        return self.score_board(board, level, player)  # - self.score_board(board, level, self.switch_player(player))

    def score_board(self, board, level, player):
        score = 0
        for (line, direction) in self.lines:
            if not self.check_empty(line, board):
                score += self.score_line(line, direction, board, player)
        return score

    def score_line(self, line, direction, board, player):
        line_score = 0
        for start in range(0, len(line) - 3):
            partial_line = line[start:start + 4]
            if not self.check_empty(partial_line, board):
                line_score += self.score_partial_line(partial_line, direction, board, player)
        return line_score

    # TODO check if have two openings
    def score_partial_line(self, partial_line, direction, board, player):
        partial_line_score = 0
        square_scores = 0
        for (x, y) in partial_line:
            if board[x][y] == player:
                square_scores += scores[x][y]
                partial_line_score += 1
            elif board[x][y] == self.switch_player(player):
                return 0
        return self.generate_score(partial_line_score, partial_line, direction, board)  # + square_scores

    def generate_score(self, score, partial_line, direction, board):
        if score == 0:
            return 10 - (self.distance(partial_line, direction, board))
        elif score >= 4:
            return (score * 100) - (self.distance(partial_line, direction, board))
        elif score == 3:
            return (score * 50) - (self.distance(partial_line, direction, board))
        else:
            return (score * 10) - (self.distance(partial_line, direction, board))

    @staticmethod
    def check_openings(line):
        pass

    @staticmethod
    def distance(partial_line, direction, board):
        distance = 0
        if direction == (0, 1):  # If its a vertical line
            return np.count_nonzero(partial_line)
        for (x, y) in partial_line:
            while x <= 5 and board[x][y] != 0:
                x += 1
                distance += 1
        return distance

    def check_win(self, board):
        one, two = 0, 0
        for (line, (d1, d2)) in self.lines:
            for (x, y) in line:
                if board[x][y] == 1:
                    one += 1
                    two = 0
                elif board[x][y] == 2:
                    one = 0
                    two += 1
                else:
                    one, two = 0, 0
                if one >= 4:
                    return 1
                elif two >= 4:
                    return 2
        return 0


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def flipBit(self, board, p, x, y):
        """
        Flip the bit at the x/y location.
        """
        board.BITBOARDS[p] |= (1 << (x * 7 + y))

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move
