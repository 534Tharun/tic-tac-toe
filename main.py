import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]

    def print_board(self):
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i + 1]} | {self.board[i + 2]}")
            if i < 6:
                print("---------")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, position, player):
        self.board[position] = player

    def is_winner(self, player):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] == player:
                return True
        return False

    def is_draw(self):
        return ' ' not in self.board

class AIPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def minimax(self, state, depth, maximizing_player, alpha, beta):
        if state.is_winner(self.symbol):
            return 1
        if state.is_winner('X' if self.symbol == 'O' else 'O'):
            return -1
        if state.is_draw():
            return 0

        if maximizing_player:
            max_eval = float('-inf')
            for move in state.available_moves():
                state.make_move(move, self.symbol)
                eval = self.minimax(state, depth + 1, False, alpha, beta)
                state.make_move(move, ' ')
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in state.available_moves():
                state.make_move(move, 'X' if self.symbol == 'O' else 'O')
                eval = self.minimax(state, depth + 1, True, alpha, beta)
                state.make_move(move, ' ')
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, state):
        best_move = None
        best_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in state.available_moves():
            state.make_move(move, self.symbol)
            eval = self.minimax(state, 0, False, alpha, beta)
            state.make_move(move, ' ')
            if eval > best_eval:
                best_eval = eval
                best_move = move
        return best_move

def main():
    board = TicTacToe()
    human_player = 'X'
    ai_player = AIPlayer('O')

    while True:
        board.print_board()

        if board.available_moves():
            if human_player == 'X':
                while True:
                    try:
                        move = int(input("Enter your move (0-8): "))
                        if move in board.available_moves():
                            break
                        else:
                            print("Invalid move. Try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                move = ai_player.get_best_move(board)

            board.make_move(move, human_player if human_player == 'X' else 'O')

            if board.is_winner(human_player):
                board.print_board()
                print("You win!")
                break
            elif board.is_winner(ai_player.symbol):
                board.print_board()
                print("AI wins!")
                break
            elif board.is_draw():
                board.print_board()
                print("It's a draw!")
                break

            human_player, ai_player.symbol = ai_player.symbol, human_player
        else:
            board.print_board()
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()