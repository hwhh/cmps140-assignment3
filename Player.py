import math
import sys

import numpy as np

# (starting coordinate, direction)
N = ([(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)], (-1, 0))
E = ([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)], (0, 1))
NE = ([(3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3)], (-1, 1))
SE = ([(5, 3), (5, 4), (5, 5), (5, 6), (4, 6), (3, 6)], (-1, -1))

scores = [[1, 2, 3, 5, 3, 2, 1],
          [2, 4, 6, 8, 6, 4, 2],
          [3, 6, 9, 10, 9, 6, 3],
          [3, 6, 9, 10, 9, 6, 3],
          [2, 4, 6, 8, 6, 4, 2],
          [1, 2, 3, 5, 3, 2, 1]]

infinity = float('inf')


class AIPlayer:

    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.lines = self.create_lines(self)

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



    def minimax(self, board):
        moves = self.generate_moves(board, self.player_number)
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            score = self.min_play(move, 1)
            if score > best_score:
                best_move = move
                best_score = score
        return self.get_move(board, best_move)

    def min_play(self, board, d):
        if self.check_win(board) or d == 0:
            return self.evaluation_function(board, 3, self.switch_player(self.player_number))
        best_score = float('inf')
        for move in self.generate_moves(board, self.switch_player(self.player_number)):
            score = self.max_play(move, d-1)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(self, board, d):
        if self.check_win(board) or d == 0:
            return self.evaluation_function(board, 3, self.player_number)
        best_score = float('-inf')
        for move in self.generate_moves(board, self.player_number):
            score = self.min_play(move, d-1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score

    def get_alpha_beta_move(self, board):
        best_move = self.rootAlphaBeta(board, 3, self.player_number)
        return self.get_move(board, best_move)

    def alphaBeta(self, board, alpha, beta, ply, player):
        if ply == 0:
            return self.evaluation_function(board, 3, player)
        move_list = self.generate_moves(board, player)
        for move in move_list:
            current_eval = -self.alphaBeta(move, -beta, -alpha, ply - 1, self.switch_player(player))
            if current_eval >= beta:
                return beta
            if current_eval > alpha:
                alpha = current_eval

        return alpha

    def rootAlphaBeta(self, board, ply, player):
        best_move = None
        max_eval = float('-infinity')
        move_list = self.generate_moves(board, player)
        alpha = float('infinity')
        for move in move_list:
            alpha = -self.alphaBeta(move, float('-infinity'), alpha, ply - 1, self.switch_player(player))
            if alpha > max_eval:
                max_eval = alpha
                best_move = move
        return best_move

    def get_alpha_beta_move(self, board):
        alpha, beta, best_value = infinity, 1000000, -1000000
        depth = 3
        best_move = None
        for move in self.generate_moves(board, self.player_number):
            current_value = self.alpha_beta(move, depth - 1, alpha, beta, self.switch_player(self.player_number))
            if current_value > best_value:
                best_value = current_value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return self.get_move(board, best_move)

    def alpha_beta(self, board, depth, alpha, beta, player):
        if depth == 0:
            if player == self.player_number:
                return self.evaluation_function(board, depth, self.switch_player(self.player_number))
            else:
                return self.evaluation_function(board, depth, player)
        elif player == self.player_number:
            v = -1000000
            for child in self.generate_moves(board, player):
                v = max(v, self.alpha_beta(child, depth - 1, alpha, beta, self.switch_player(player)))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return v
        else:
            v = 1000000
            for child in self.generate_moves(board, player):
                v = min(v, self.alpha_beta(child, depth - 1, alpha, beta, self.switch_player(player)))
                alpha = min(beta, v)
                if beta <= alpha:
                    break
            return v

    def get_expectimax_move(self, board):
        # first look at the
        return 0

    def evaluation_function(self, board, level, player):
        # if self.check_win(board, self.player_number):
        #     print(board)
        #     return -100000000
        # elif self.check_win(board, self.switch_player(self.player_number)):
        #     print(board)
        #     return 100000000
        # else:
        x = self.score_board(board, level, player)
        y = self.score_board(board, level, self.switch_player(player))
        return x-y

    def score_board(self, board, level, player):
        score = 0
        for (line, direction) in self.lines:
            if not self.check_empty(line, board):  # optimisation
                score += self.score_line(line, direction, board, player)
        return score

    def score_line(self, line, direction, board, player):
        line_score = 0
        for start in range(0, len(line) - 3):
            partial_line = line[start:start + 4]
            if not self.check_empty(partial_line, board):
                line_score += self.score_partial_line(partial_line, direction, board, player)
        return line_score

    # TODO Check the distance away in the line
    def score_partial_line(self, partial_line, direction, board, player):
        partial_line_score = 0
        square_scores = 0
        for (x, y) in partial_line:
            if board[x][y] == player:
                square_scores += 0  # scores[x][y]
                partial_line_score += 1
            elif board[x][y] == self.switch_player(player):
                return 0
        dis = self.distance(board, partial_line, direction)
        if partial_line_score == 4:
            return square_scores + (partial_line_score ** 5) - dis
        elif partial_line_score == 3:
            return square_scores + (partial_line_score ** 4) - dis
        elif partial_line_score == 2:
            return square_scores + (partial_line_score ** 3) - dis
        elif partial_line_score == 1:
            return square_scores + (partial_line_score ** 2) - dis
        else:
            return square_scores + partial_line_score - dis

    @staticmethod
    def distance(board, line, direction):
        distance = 0
        if direction[0] != 0 and direction[1] != 0:  # DIAGONAL
            for (x, y) in line:
                while board[x][y] == 0 and 0 <= x < 5:
                    distance += 1
                    x += 1
            return distance
        else:
            for (x, y) in line:
                if board[x][y] == 0:
                    distance += 1
            return distance

    @staticmethod
    def check_win(board):
        boardHeight = len(board[0])
        boardWidth = len(board)
        # check horizontal spaces
        for y in range(boardHeight):
            for x in range(boardWidth - 3):
                if board[x][y] == 1 and board[x + 1][y] == 1 and board[x + 2][y] == 1 and board[x + 3][y] == 1:
                    return 1
                elif board[x][y] == 2 and board[x + 1][y] == 2 and board[x + 2][y] == 2 and board[x + 3][y] == 2:
                    return 2
        # check vertical spaces
        for x in range(boardWidth):
            for y in range(boardHeight - 3):
                if board[x][y] == 1 and board[x][y + 1] == 1 and board[x][y + 2] == 1 and board[x][y + 3] == 1:
                    return 1
                if board[x][y] == 2 and board[x][y + 1] == 2 and board[x][y + 2] == 2 and board[x][y + 3] == 2:
                    return 2
        # check / diagonal spaces
        for x in range(boardWidth - 3):
            for y in range(3, boardHeight):
                if board[x][y] == 1 and board[x + 1][y - 1] == 1 and board[x + 2][y - 2] == 1 and board[x + 3][
                    y - 3] == 1:
                    return 1
                elif board[x][y] == 2 and board[x + 1][y - 1] == 2 and board[x + 2][y - 2] == 2 and board[x + 3][
                    y - 3] == 2:
                    return 2
        # check \ diagonal spaces
        for x in range(boardWidth - 3):
            for y in range(boardHeight - 3):
                if board[x][y] == 1 and board[x][y + 1] == 1 and board[x][y + 2] == 1 and board[x][y + 3] == 1:
                    return 1
                elif board[x][y] == 2 and board[x][y + 1] == 2 and board[x][y + 2] == 2 and board[x][y + 3] == 2:
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


"""

b1 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 2, 2, 0, 0, 0],
              [0, 0, 1, 1, 1, 0, 0]]

        b2 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0],
              [0, 0, 1, 1, 2, 0, 0]]

        # o1 = self.evaluation_function(b1, 1, 2)
        # o2 = self.evaluation_function(b2, 1, 2)

        #
        #
        #
        # return 0"""
