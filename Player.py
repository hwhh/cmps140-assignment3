import tree
from BasePlayer import BasePlayer


class AI(BasePlayer):
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        BasePlayer.__init__(self, "CPU", True)

    @staticmethod
    def evaluate3(opp_board, my_board):
        """
        Returns the number of possible 3 in a rows in bitboard format.
        Running time: O(1)
        http://www.gamedev.net/topic/596955-trying-bit-boards-for-connect-4/
        """
        inverse_board = ~(my_board | opp_board)
        r_shift7_my_board = my_board >> 7
        l_shift7_my_board = my_board << 7
        r_shift14_my_board = my_board >> 14
        l_shit14_my_board = my_board << 14
        r_shift16_my_board = my_board >> 16
        l_shift16_my_board = my_board << 16
        r_shift8_my_board = my_board >> 8
        l_shift8_my_board = my_board << 8
        r_shift6_my_board = my_board >> 6
        l_shift6_my_board = my_board << 6
        r_shift12_my_board = my_board >> 12
        l_shift12_my_board = my_board << 12

        # check _XXX and XXX_ horizontal
        result = inverse_board & r_shift7_my_board & r_shift14_my_board \
                 & (my_board >> 21)

        result |= inverse_board & r_shift7_my_board & r_shift14_my_board \
                  & l_shift7_my_board

        result |= inverse_board & r_shift7_my_board & l_shift7_my_board \
                  & l_shit14_my_board

        result |= inverse_board & l_shift7_my_board & l_shit14_my_board \
                  & (my_board << 21)

        # check XXX_ diagonal /
        result |= inverse_board & r_shift8_my_board & r_shift16_my_board \
                  & (my_board >> 24)

        result |= inverse_board & r_shift8_my_board & r_shift16_my_board \
                  & l_shift8_my_board

        result |= inverse_board & r_shift8_my_board & l_shift8_my_board \
                  & l_shift16_my_board

        result |= inverse_board & l_shift8_my_board & l_shift16_my_board \
                  & (my_board << 24)

        # check _XXX diagonal \
        result |= inverse_board & r_shift6_my_board & r_shift12_my_board \
                  & (my_board >> 18)

        result |= inverse_board & r_shift6_my_board & r_shift12_my_board \
                  & l_shift6_my_board

        result |= inverse_board & r_shift6_my_board & l_shift6_my_board \
                  & l_shift12_my_board

        result |= inverse_board & l_shift6_my_board & l_shift12_my_board \
                  & (my_board << 18)

        # check for _XXX vertical
        result |= inverse_board & (my_board << 1) & (my_board << 2) \
                  & (my_board << 3)

        return result

    @staticmethod
    def evaluate2(opp_board, my_board):
        """
        Returns the number of possible 2 in a rows in bitboard format.
        Running time: O(1)
        """
        inverse_board = ~(my_board | opp_board)
        r_shift7_my_board = my_board >> 7
        r_shift14_my_board = my_board >> 14
        l_shift7_my_board = my_board << 7
        l_shift14_my_board = my_board << 14
        r_shift8_my_board = my_board >> 8
        l_shift8_my_board = my_board << 8
        l_shift16_my_board = my_board << 16
        r_shift16_my_board = my_board >> 16
        r_shift6_my_board = my_board >> 6
        l_shift6_my_board = my_board << 6
        r_shift12_my_board = my_board >> 12
        l_shift12_my_board = my_board << 12

        # check for _XX
        result = inverse_board & r_shift7_my_board & r_shift14_my_board
        result |= inverse_board & r_shift7_my_board & r_shift14_my_board
        result |= inverse_board & r_shift7_my_board & l_shift7_my_board

        # check for XX_
        result |= inverse_board & l_shift7_my_board & l_shift14_my_board

        # check for XX / diagonal
        result |= inverse_board & l_shift8_my_board & l_shift16_my_board

        result |= inverse_board & r_shift8_my_board & r_shift16_my_board
        result |= inverse_board & r_shift8_my_board & r_shift16_my_board
        result |= inverse_board & r_shift8_my_board & l_shift8_my_board

        # check for XX \ diagonal
        result |= inverse_board & r_shift6_my_board & r_shift12_my_board
        result |= inverse_board & r_shift6_my_board & r_shift12_my_board
        result |= inverse_board & r_shift6_my_board & l_shift6_my_board
        result |= inverse_board & l_shift6_my_board & l_shift12_my_board

        # check for _XX vertical
        result |= inverse_board & (my_board << 1) & (my_board << 2) \
                  & (my_board << 2)

        return result

    @staticmethod
    def evaluate1(opp_board, my_board):
        """
        Returns the number of possible 1 in a rows in bitboard format.
        Running time: O(1)
        Diagonals are skipped since they are worthless.
        """
        inverse_board = ~(my_board | opp_board)
        # check for _X
        result = inverse_board & (my_board >> 7)

        # check for X_
        result |= inverse_board & (my_board << 7)

        # check for _X vertical
        result |= inverse_board & (my_board << 1)

        return result

    @staticmethod
    def bitboard_bits(i):
        """"
        Returns the number of bits in a bitboard (7x6).
        Running time: O(1)
        Help from: http://stackoverflow.com/q/9829578/1524592
        """
        i = i & 0xFDFBF7EFDFBF  # magic number to mask to only legal bitboard
        # positions (bits 0-5, 7-12, 14-19, 21-26, 28-33, 35-40, 42-47)
        i = (i & 0x5555555555555555) + ((i & 0xAAAAAAAAAAAAAAAA) >> 1)
        i = (i & 0x3333333333333333) + ((i & 0xCCCCCCCCCCCCCCCC) >> 2)
        i = (i & 0x0F0F0F0F0F0F0F0F) + ((i & 0xF0F0F0F0F0F0F0F0) >> 4)
        i = (i & 0x00FF00FF00FF00FF) + ((i & 0xFF00FF00FF00FF00) >> 8)
        i = (i & 0x0000FFFF0000FFFF) + ((i & 0xFFFF0000FFFF0000) >> 16)
        i = (i & 0x00000000FFFFFFFF) + ((i & 0xFFFFFFFF00000000) >> 32)

        return i

    def evalCost(self, b, opp_board, my_board, b_my_turn):
        """
        Returns cost of each board configuration.
        winning is a winning move
        blocking is a blocking move
        Running time: O(7n)
        """
        win_reward = 9999999
        opp_cost3_row = 1000
        my_cost3_row = 3000
        opp_cost2_row = 500
        my_cost2_row = 500
        opp_cost1_row = 100
        my_cost1_row = 100

        if self.hasWon(opp_board):
            return -win_reward
        elif self.hasWon(my_board):
            return win_reward

        get3_win = self.evaluate3(opp_board, my_board)
        winning3 = self.bitboard_bits(get3_win) * my_cost3_row

        get3_block = self.evaluate3(my_board, opp_board)
        blocking3 = self.bitboard_bits(get3_block) * -opp_cost3_row

        get2_win = self.evaluate2(opp_board, my_board)
        winning2 = self.bitboard_bits(get2_win) * my_cost2_row

        get2_block = self.evaluate2(my_board, opp_board)
        blocking2 = self.bitboard_bits(get2_block) * -opp_cost2_row

        get1_win = self.evaluate1(opp_board, my_board)
        winning1 = self.bitboard_bits(get1_win) * my_cost1_row

        get1_block = self.evaluate1(my_board, opp_board)
        blocking1 = self.bitboard_bits(get1_block) * -opp_cost1_row

        return winning3 + blocking3 + winning2 + blocking2 \
               + winning1 + blocking1

    def search(self, board, use_alphabeta=True):
        """
        Construct the minimax tree, and get the best move based off the root.
        You have two options to build the tree:
            if use_alphabeta is True:
                alpha beta will be used to construct the tree
            otherwise:
                raw minimax will be used to construct the tree (it may be
            required to lower the maxDepth because it will be slower).
        """
        my_board = board.BITBOARDS[board.current_turn]
        opp_board = board.BITBOARDS[(not board.current_turn)]
        max_depth = 5

        g = tree.graph(my_board, opp_board, max_depth)  # minimax graph

        if use_alphabeta:
            g.alphabeta(board, self, g.root, max_depth,
                        float('-inf'), float('inf'))
        else:
            g.construct_tree(board, self, g.root, my_board, opp_board, 1)

        return g.getMove()

    def forced_moves(self, board):
        """
        If placing a token can win immediately, return that column.
        Otherwise, if you can block your opponent immediately, return
        one of those column(s).
        """

        my_board = board.BITBOARDS[board.current_turn]
        opp_board = board.BITBOARDS[(not board.current_turn)]
        possible_bits = self.get_legal_locations(my_board | opp_board)

        forced_cols = []  # cols needed to block your opponent if you cannot win
        for colbitTuple in possible_bits:
            temp_my_board = self.setNthBit(my_board, colbitTuple[1])
            temp_opp_board = self.setNthBit(opp_board, colbitTuple[1])

            if self.hasWon(temp_my_board):
                return colbitTuple[0]
            elif self.hasWon(temp_opp_board):
                forced_cols.append(colbitTuple[0])

        if forced_cols:
            return forced_cols[0]
        return -1

    def play(self, board):
        """
        Returns the column to place the piece in.
        """
        forced_column = self.forced_moves(board)  # if there is a forced move
        if forced_column > -1:
            return forced_column  # play it

        x = self.search(board)  # otherwise, search the tree
        return x

    def hasWon(self, bitboard):
        # taken from http://stackoverflow.com/q/7033165/1524592
        y = bitboard & (bitboard >> 6)
        if (y & (y >> 2 * 6)):  # check \ diagonal
            return True
        y = bitboard & (bitboard >> 7)
        if (y & (y >> 2 * 7)):  # check horizontal
            return True
        y = bitboard & (bitboard >> 8)
        if (y & (y >> 2 * 8)):  # check / diagonal
            return True
        y = bitboard & (bitboard >> 1)
        if (y & (y >> 2)):  # check vertical
            return True
        return False
