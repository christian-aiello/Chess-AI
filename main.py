from cmath import inf
import string, copy, random, colorama

colorama.init()


def in_board(r, c):
    return r in range(8) and c in range(8)


def algebraic(move):
    start, end = move.split(" ")
    sc, sr = start[0], int(start[1])
    ec, er = end[0], int(end[1])
    sc, ec = ord(sc) - 97, ord(ec) - 97
    sr, er = 8 - sr, 8 - er
    return ((sr, sc), (er, ec))


def to_algebraic(move):
    start, end = move[0], move[1]
    sr, sc = start[0], int(start[1])
    er, ec = end[0], int(end[1])

    sc, ec = chr(sc + 97), chr(ec + 97)
    sr, er = 8 - sr, 8 - er

    if len(move) == 2:
        return sc + str(sr) + ec + str(er)
    else:
        return sc + str(sr) + ec + str(er) + move[2]


def create_piece(char, row, col):
    color = 1

    if char in string.ascii_lowercase:
        color = 0

    if char.upper() == "P":
        return Pawn(color, row, col)
    elif char.upper() == "R":
        return Rook(color, row, col)
    elif char.upper() == "N":
        return Knight(color, row, col)
    elif char.upper() == "B":
        return Bishop(color, row, col)
    elif char.upper() == "Q":
        return Queen(color, row, col)
    elif char.upper() == "K":
        return King(color, row, col)


class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col


class Pawn(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.VALUE = 100

    def __repr__(self):
        if self.color:
            return "P"
        else:
            return "p"

    def get_moves(self, board):
        moves = []

        if self.color:
            captures, two_squares, one_square, starting, end = (
                [(-1, 1), (-1, -1)],
                -2,
                -1,
                6,
                0,
            )
        else:
            captures, two_squares, one_square, starting, end = (
                [(1, 1), (1, -1)],
                2,
                1,
                1,
                7,
            )

        if self.row == starting:
            er = self.row + two_squares
            ec = self.col
            if in_board(er, ec) and board.board[er][ec] == 0:
                moves.append(((self.row, self.col), (er, ec)))

        er = self.row + one_square
        ec = self.col
        if in_board(er, ec) and board.board[er][ec] == 0:
            if er == end:
                moves.append(((self.row, self.col), (er, ec), "q"))
                moves.append(((self.row, self.col), (er, ec), "r"))
                moves.append(((self.row, self.col), (er, ec), "b"))
                moves.append(((self.row, self.col), (er, ec), "n"))
            else:
                moves.append(((self.row, self.col), (er, ec)))
        else:
            moves = []

        for (r, c) in captures:
            er = self.row + r
            ec = self.col + c
            if in_board(er, ec):
                if (
                    board.board[er][ec] != 0
                    and (board.board[er][ec]).color != self.color
                ):
                    if er == end:
                        moves.append(((self.row, self.col), (er, ec), "q"))
                        moves.append(((self.row, self.col), (er, ec), "r"))
                        moves.append(((self.row, self.col), (er, ec), "b"))
                        moves.append(((self.row, self.col), (er, ec), "n"))
                    else:
                        moves.append(((self.row, self.col), (er, ec)))
                else:
                    if (er, ec) == board.en_passant:
                        moves.append(((self.row, self.col), (er, ec)))
        return moves


class Rook(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.VALUE = 479

    def __repr__(self):
        if self.color:
            return "R"
        else:
            return "r"

    def get_moves(self, board):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for (r, c) in directions:
            er = self.row
            ec = self.col
            for _ in range(8):
                er += r
                ec += c
                if in_board(er, ec):
                    if board.board[er][ec] == 0:
                        moves.append(((self.row, self.col), (er, ec)))
                    else:
                        if board.board[er][ec].color == self.color:
                            break
                        else:
                            moves.append(((self.row, self.col), (er, ec)))
                            break
                else:
                    break

        return moves


class Knight(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.VALUE = 280

    def __repr__(self):
        if self.color:
            return "N"
        else:
            return "n"

    def get_moves(self, board):
        moves = []
        directions = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]

        for (r, c) in directions:
            er = self.row + r
            ec = self.col + c
            if in_board(er, ec):
                if board.board[er][ec] == 0:
                    moves.append(((self.row, self.col), (er, ec)))
                else:
                    if board.board[er][ec].color != self.color:
                        moves.append(((self.row, self.col), (er, ec)))

        return moves


class Bishop(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.VALUE = 320

    def __repr__(self):
        if self.color:
            return "B"
        else:
            return "b"

    def get_moves(self, board):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for (r, c) in directions:
            er = self.row
            ec = self.col
            for _ in range(8):
                er += r
                ec += c
                if in_board(er, ec):
                    if board.board[er][ec] == 0:
                        moves.append(((self.row, self.col), (er, ec)))
                    else:
                        if board.board[er][ec].color == self.color:
                            break
                        else:
                            moves.append(((self.row, self.col), (er, ec)))
                            break
                else:
                    break

        return moves


class Queen(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.VALUE = 929

    def __repr__(self):
        if self.color:
            return "Q"
        else:
            return "q"

    def get_moves(self, board):
        moves = []
        directions = [
            (1, 1),
            (-1, 1),
            (-1, -1),
            (1, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        ]

        for (r, c) in directions:
            er = self.row
            ec = self.col
            for _ in range(8):
                er += r
                ec += c
                if in_board(er, ec):
                    if board.board[er][ec] == 0:
                        moves.append(((self.row, self.col), (er, ec)))
                    else:
                        if board.board[er][ec].color == self.color:
                            break
                        else:
                            moves.append(((self.row, self.col), (er, ec)))
                            break
                else:
                    break

        return moves


class King(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.VALUE = 90000

    def __repr__(self):
        if self.color:
            return "K"
        else:
            return "k"

    def get_moves(self, board):
        moves = []
        wk = board.wk
        wq = board.wq
        bk = board.bk
        bq = board.bq
        directions = [
            (1, 1),
            (-1, 1),
            (-1, -1),
            (1, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        ]

        for (r, c) in directions:
            er = self.row + r
            ec = self.col + c
            if in_board(er, ec):
                if board.board[er][ec] == 0:
                    moves.append(((self.row, self.col), (er, ec)))
                else:
                    if board.board[er][ec].color != self.color:
                        moves.append(((self.row, self.col), (er, ec)))

        if self.color and board.turn:
            if wk:
                if (board.board[7][5] == 0) and (board.board[7][6] == 0):
                    if (7, 5) not in board.get_captured(opponent=True) and (
                        7,
                        6,
                    ) not in board.get_captured(opponent=True):
                        moves.append(((self.row, self.col), (7, 6)))
            if wq:
                if (
                    (board.board[7][3] == 0)
                    and (board.board[7][2] == 0)
                    and (board.board[7][1] == 0)
                ):
                    if (7, 3) not in board.get_captured(opponent=True) and (
                        7,
                        2,
                    ) not in board.get_captured(opponent=True):
                        moves.append(((self.row, self.col), (7, 2)))
        elif not self.color and not board.turn:
            if bk:
                if (board.board[0][5] == 0) and (board.board[0][6] == 0):
                    if (0, 5) not in board.get_captured(opponent=True) and (
                        0,
                        6,
                    ) not in board.get_captured(opponent=True):
                        moves.append(((self.row, self.col), (0, 6)))
            if bq:
                if (
                    (board.board[0][3] == 0)
                    and (board.board[0][2] == 0)
                    and (board.board[0][1] == 0)
                ):
                    if (0, 3) not in board.get_captured(opponent=True) and (
                        0,
                        2,
                    ) not in board.get_captured(opponent=True):
                        moves.append(((self.row, self.col), (0, 2)))

        return moves


class Board:
    def __init__(self):
        self.turn = 1
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.wk = False
        self.wq = False
        self.bk = False
        self.bq = False
        self.half = 0
        self.full = 1
        self.en_passant = None

    def evaluate(self):
        white_evaluation = self.material(1)
        black_evaluation = self.material(0)

        if self.turn:
            perspective = 1
        elif not self.turn:
            perspective = -1

        return (white_evaluation - black_evaluation) * perspective

    def material(self, color):
        material = 0

        for row in self.board:
            for col in row:
                if col != 0 and col.color == color:
                    material += col.VALUE

        return material

    def perft(self, depth):
        total = 0
        for move in self.get_all_moves():
            board = copy.deepcopy(self)
            board.make_move(*move)
            perft = board.explore(depth - 1)
            print(f"{to_algebraic(move)}: {perft}")
            total += perft
        print(f"Total: {total}")

        return total

    def is_checkmate(self):
        if len(self.get_all_moves()) == 0:
            for row in range(8):
                for col in range(8):
                    if (
                        type(self.board[row][col]).__name__ == "King"
                        and (self.board[row][col]).color == self.turn
                    ):
                        if (row, col) not in self.get_captured(opponent=True):
                            return -1
            return 1

        if self.half == 50:
            return -1

        return 0

    def explore(self, depth):
        if depth == 0:
            return 1
        elif depth == 1:
            return len(self.get_all_moves())
        else:
            counter = 0
            for move in self.get_all_moves():
                board = copy.deepcopy(self)
                board.make_move(*move)
                counter += board.explore(depth - 1)
            return counter

    def minimax(self, depth, alpha, beta, root=False):
        if depth == 0:
            return self.evaluate()

        moves = self.get_all_moves()
        if self.is_checkmate() == 1:
            return -inf
        elif self.is_checkmate() == -1:
            return 0


        best_evaluation = -inf
        best_moves = []

        for move in moves:
            board = copy.deepcopy(self)
            board.make_move(*move)
            evaluation = -board.minimax(depth - 1, -beta, -alpha)
            if evaluation >= best_evaluation:
                if root:
                    if evaluation == best_evaluation:
                        best_moves.append(move)
                    elif evaluation > best_evaluation:
                        best_moves = []
                        best_moves.append(move)
                best_evaluation = evaluation
            alpha = max(alpha, best_evaluation)
            if alpha >= beta:
                break

        if root:
            return random.choice(best_moves)
        return best_evaluation

    def display(self):
        for i, row in enumerate(game.board):
            row = ["·" if i == 0 else i for i in row]
            space = " "
            print(colorama.Fore.WHITE + str(8 - i), end=" ")
            for i, col in enumerate(row):
                if i != 7:
                    if col == "·":
                        print(colorama.Fore.WHITE + str(col), end=" ")
                    elif col.color:
                        print(colorama.Fore.BLUE + str(col), end=" ")
                    elif not col.color:
                        print(colorama.Fore.RED + str(col), end=" ")
                else:
                    if col == "·":
                        print(colorama.Fore.WHITE + str(col))
                    elif col.color:
                        print(colorama.Fore.BLUE + str(col))
                    elif not col.color:
                        print(colorama.Fore.RED + str(col))
        print(colorama.Fore.WHITE + "  a b c d e f g h")

    def generate_board(
        self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    ):
        fen = fen.split(" ")

        pieces = fen[0]
        turn = fen[1]
        castling = fen[2]
        en_passant = fen[3]
        self.half = int(fen[4])
        self.full = int(fen[5])

        self.board = [[0 for _ in range(8)] for _ in range(8)]

        row = 0
        col = 0

        for piece in pieces:
            if piece in string.digits:
                col += int(piece)
            elif piece == "/":
                row += 1
                col = 0
            else:
                self.board[row][col] = create_piece(piece, row, col)
                col += 1

        if turn == "b":
            self.turn = 0
        else:
            self.turn = 1

        if "K" in castling:
            self.wk = True
        if "Q" in castling:
            self.wq = True
        if "k" in castling:
            self.bk = True
        if "q" in castling:
            self.bq = True
        if castling == "-":
            self.wk, self.wq, self.bk, self.bq = False, False, False, False

        if en_passant != "-":
            self.en_passant = (8 - int(en_passant[1]), ord(en_passant[0]) - 97)
        else:
            self.en_passant = None

    def make_move(self, start, end, promotion=None):
        (sr, sc) = start
        (er, ec) = end
        self.half += 1
        if not self.turn:
            self.full += 1

        if self.board[er][ec] != 0:
            self.half = 0

        if type(self.board[sr][sc]).__name__ == "Pawn":
            self.half = 0
            if (er, ec) == self.en_passant:
                if er == 2:
                    self.board[3][ec] = 0
                if er == 5:
                    self.board[4][ec] = 0

        self.en_passant = None

        if type(self.board[sr][sc]).__name__ == "Pawn":
            if abs(sr - er) == 2:
                if (self.board[sr][sc]).color:
                    self.en_passant = (sr - 1, sc)
                else:
                    self.en_passant = (sr + 1, sc)

        if type(self.board[sr][sc]).__name__ == "King":
            if (self.board[sr][sc]).color:
                if abs(sc - ec) == 2:
                    if (
                        ec == 6
                        and type(self.board[7][7]).__name__ == "Rook"
                        and (self.board[7][7]).color
                    ):
                        self.board[7][5] = self.board[7][7]
                        self.board[7][7] = 0
                        (self.board[7][5]).row = 7
                        (self.board[7][5]).col = 5
                    if (
                        ec == 2
                        and type(self.board[7][0]).__name__ == "Rook"
                        and (self.board[7][0]).color
                    ):
                        self.board[7][3] = self.board[7][0]
                        self.board[7][0] = 0
                        (self.board[7][3]).row = 7
                        (self.board[7][3]).col = 3
                self.wk, self.wq = False, False
            else:
                if abs(sc - ec) == 2 and (sr, sc):
                    if (
                        ec == 6
                        and type(self.board[0][7]).__name__ == "Rook"
                        and not (self.board[0][7]).color
                    ):
                        self.board[0][5] = self.board[0][7]
                        self.board[0][7] = 0
                        (self.board[0][5]).row = 0
                        (self.board[0][5]).col = 5
                    if (
                        ec == 2
                        and type(self.board[0][0]).__name__ == "Rook"
                        and not (self.board[0][0]).color
                    ):
                        self.board[0][3] = self.board[0][0]
                        self.board[0][0] = 0
                        (self.board[0][3]).row = 0
                        (self.board[0][3]).col = 3
                self.bk, self.bq = False, False

        if type(self.board[er][ec]).__name__ == "Rook":
            if (er, ec) == (7, 7):
                self.wk = False
            elif (er, ec) == (7, 0):
                self.wq = False
            elif (er, ec) == (0, 0):
                self.bq = False
            elif (er, ec) == (0, 7):
                self.bk = False

        if type(self.board[sr][sc]).__name__ == "Rook":
            if (sr, sc) == (7, 7):
                self.wk = False
            elif (sr, sc) == (7, 0):
                self.wq = False
            elif (sr, sc) == (0, 0):
                self.bq = False
            elif (sr, sc) == (0, 7):
                self.bk = False

        self.board[er][ec] = self.board[sr][sc]
        self.board[sr][sc] = 0
        (self.board[er][ec]).row, (self.board[er][ec]).col = er, ec

        if promotion:
            if promotion == "q":
                self.board[er][ec] = Queen((self.board[er][ec]).color, er, ec)
            if promotion == "b":
                self.board[er][ec] = Bishop((self.board[er][ec]).color, er, ec)
            if promotion == "n":
                self.board[er][ec] = Knight((self.board[er][ec]).color, er, ec)
            if promotion == "r":
                self.board[er][ec] = Rook((self.board[er][ec]).color, er, ec)

        self.turn = not int(self.turn)

    def validate_move(self, start, end, promotion=None):
        (sr, sc) = start
        (er, ec) = end

        if type(self.board[sr][sc]).__name__ == "King":
            if abs(sc - ec) == 2:
                if (sr, sc) in self.get_captured(opponent=True):
                    return False

        board_copy = copy.deepcopy(self)
        board_copy.make_move(start, end, promotion)

        for row in board_copy.board:
            for col in row:
                if col != 0:
                    if type(col).__name__ == "King" and (
                        col.color == (not board_copy.turn)
                    ):
                        if (col.row, col.col) not in board_copy.get_captured():
                            return True

        return False

    def get_all_moves(self):
        moves = []
        for row in self.board:
            for col in row:
                if col != 0 and col.color == self.turn:
                    for move in col.get_moves(self):
                        if self.validate_move(*move):
                            moves.append(move)

        return moves

    def get_captured(self, opponent=None):
        turn = self.turn
        if opponent:
            turn = not turn
        squares = []
        for row in self.board:
            for col in row:
                if col != 0 and col.color == turn:
                    if type(col).__name__ != "Pawn":
                        squares.extend([i[1] for i in col.get_moves(self)])
                    else:
                        for i in col.get_moves(self):
                            if i[0][1] != i[1][1]:
                                squares.append(i[1])

        return squares


game = Board()


def main():
    colors = {1: "White", 0: "Black"}

    game.generate_board()

    while True:
        game.display()

        mate = game.is_checkmate()
        if mate == 1:
            print(f"Checkmate! {colors[1 - game.turn]} wins!")
            break
        elif mate == -1:
            print("Draw!")
            break

        if game.turn == 1:
            move = input()
            if (
                len(move) == 5
                and move[2] == " "
                and move[1] in string.digits
                and move[4] in string.digits
                and move[0] not in string.digits
                and move[3] not in string.digits
            ):
                if (algebraic(move)[0], algebraic(move)[1]) in game.get_all_moves():
                    game.make_move(*algebraic(move))
                elif (algebraic(move)[0], algebraic(move)[1]) in [
                    i[0:2] for i in game.get_all_moves()
                ]:
                    move = algebraic(move)
                    promotion = input("Promote to (q, r, b, n)?: ")
                    move = (move[0], move[1], promotion)
                    game.make_move(*move)
                else:
                    print("Invalid!")
            else:
                print("Invalid!")
        else:
            print("AI thinking...")
            game.make_move(*game.minimax(3, -inf, inf, root=True))

    input("Press any key to exit.")


if __name__ == "__main__":
    main()
