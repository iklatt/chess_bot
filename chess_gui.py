import tkinter as tk
from PIL import Image, ImageTk
import chess

class ChessPiece:
    def __init__(self, fenChar, xPos, yPos, image, canvas_object):
        self.x = xPos
        self.y = yPos
        self.image = image
        self.fen = fenChar
        self.piece = canvas_object
    
    def move(self, newX, newY):
        self.x = newX
        self.y = newY

class ChessBoard:
    def __init__(self, window):
        self.window = window
        self.window.geometry("850x850")
        self.window.configure(background="gray")
        
        self.canvas = tk.Canvas(window, highlightbackground= "black", width=800, height=800)
        self.canvas.pack(pady=1)

        # Create the squares of the board:
        for row in range(8):
            for column in range(8):
                if (row + column) % 2 == 0:
                    color="#F0D9B5"
                else:
                    color="#B58863"
                self.canvas.create_rectangle(row * 100 + 1, column * 100 + 1, (row + 1) * 100 + 1, (column + 1) * 100 + 1, 
                                        fill=color)
        
        # Set up the pieces:
        self.pieces_list = []
        self.fen_to_image_dictionary = {
            "K": "white_king.png",
            "Q": "white_queen.png",
            "R": "white_rook.png",
            "B": "white_bishop.png",
            "N": "white_knight.png",
            "P": "white_pawn.png",
            "k": "black_king.png",
            "q": "black_queen.png",
            "r": "black_rook.png",
            "b": "black_bishop.png",
            "n": "black_knight.png",
            "p": "black_pawn.png"
        }
        starting_position_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.set_up_from_FEN(starting_position_fen)
        self.game = chess.Board()

        self.selected_piece = False

        # Bindings for drag and drop
        self.canvas.bind("<ButtonPress-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

    def set_piece(self, fen_piece, xPos, yPos):
        file = "piece_images\\" + self.fen_to_image_dictionary[fen_piece]
        image = ImageTk.PhotoImage( Image.open(file).convert('RGBA').resize((100, 100)) )
        piece = ChessPiece(fen_piece, xPos, yPos, image, self.canvas.create_image(xPos, yPos, image=image))
        self.pieces_list.append(piece)

    def set_up_from_FEN(self, fen):
        self.pieces_list = []
        row = 0
        col = 0
        for char in fen:
            if char == "/":
                row += 1
                col = 0
            elif char == " ":
                break
            elif char.isdigit():
                col += int(char)
            else:
                self.set_piece(char, col * 100 + 50, row * 100  + 50)
                col += 1

    # Convert coordinates to chess notation for that square:
    def convert_board_location(self, xPos, yPos, boardIsFlipped):
        x = xPos // 100
        y = yPos // 100
        if boardIsFlipped:
            x = 7 - x
            y += 1
        else:
            y = 8 - y
        return chr(97 + x) + str(y)
    
    def make_move(self, xPos, yPos):
        start_x = self.selected_piece.x
        start_y = self.selected_piece.y
        column = xPos // 100
        row = yPos // 100
        # Only update the chess board when the piece moves to a different location:
        if start_x // 100 != column or start_y // 100 != row:
            uci_move = self.convert_board_location(start_x, start_y, False) + self.convert_board_location(xPos, yPos, False)
            self.game.push_uci(uci_move)
            # If there is another piece at this location, delete it:
            for piece in self.pieces_list:
                if (column, row) == (piece.x // 100, piece.y // 100):
                    self.pieces_list.remove(piece)
            self.selected_piece.move(column * 100, row * 100)
        self.canvas.moveto(self.selected_piece.piece, column * 100, row * 100)

    def is_illegal_move(self, xPos, yPos):
        # Check if the move is in bounds
        if xPos < 0 or xPos >= 800 or yPos < 0 or yPos >= 800:
            return True
        # Check if the move is legal:
        start_x = self.selected_piece.x
        start_y = self.selected_piece.y
        if start_x // 100 == xPos // 100 and start_y // 100 == yPos // 100:
            return True
        uci_move = self.convert_board_location(start_x, start_y, False) + self.convert_board_location(xPos, yPos, False)
        if chess.Move.from_uci(uci_move) in self.game.legal_moves:
            return False
        return True

    def on_start(self, event):
        clicked_square = (event.x // 100, event.y // 100)
        for piece in self.pieces_list:
            if clicked_square == (piece.x // 100, piece.y // 100):
                self.selected_piece = piece

    def move(self, event):
        if self.selected_piece:
            self.canvas.moveto(self.selected_piece.piece, event.x - 50, event.y - 50)

    # This function ensures the piece is centered on the square that it was dropped onto.
    #TODO: Need these squares to be valid, ie can't be out of bounds nor can it be an illegal move.
    #      If an illegal move is made, return the piece to its original location
    def on_drop(self, event):
        if self.selected_piece:
            x = event.x
            y = event.y
            #check that the move is legal:
            if self.is_illegal_move(x, y):
                x = self.selected_piece.x
                y = self.selected_piece.y
            self.make_move(x, y)
            self.selected_piece = False

if __name__ == "__main__":
    window = tk.Tk()
    chess_board = ChessBoard(window)
    window.mainloop()