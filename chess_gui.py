import tkinter as tk
from PIL import Image, ImageTk
import chess

class ChessPiece:
    def __init__(self, fenChar, xPos, yPos, image):
        self.x = xPos
        self.y = yPos
        self.image = image
        self.fen = fenChar
    
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
        self.image_references = {}
        self.piece_location_dictionary = {}
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
        self.selected_piece_original_position = None

        # Bindings for drag and drop
        self.canvas.bind("<ButtonPress-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

    def set_piece(self, fen_piece, xPos, yPos):
        file = "piece_images\\" + self.fen_to_image_dictionary[fen_piece]
        img = ImageTk.PhotoImage( Image.open(file).convert('RGBA').resize((100, 100)) )
        self.image_references[(xPos // 100, yPos // 100)] = img
        self.piece_location_dictionary[(xPos // 100, yPos // 100)] = self.canvas.create_image(xPos, yPos, image=img)

    #TODO: Need to reset image_references every time this is called.
    def set_up_from_FEN(self, fen):
        self.image_references = {}
        self.piece_location_dictionary = {}
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
        start_x, start_y = self.selected_piece_original_position
        start_x *= 100
        start_y *= 100
        # Only update the chess board when the piece moves to a different location:
        if start_x != xPos or start_y != yPos:
            uci_move = self.convert_board_location(start_x, start_y, False) + self.convert_board_location(xPos, yPos, False)
            self.game.push_uci(uci_move)
            x = xPos // 100
            y = yPos // 100
            if (x, y) in self.piece_location_dictionary:
                self.piece_location_dictionary.pop((x, y))
            self.piece_location_dictionary[(x, y)] = self.selected_piece
            self.piece_location_dictionary.pop((start_x // 100, start_y // 100))
        self.canvas.moveto(self.selected_piece, xPos, yPos)

    def is_illegal_move(self, xPos, yPos):
        # Check if the move is in bounds
        if xPos < 0 or xPos >= 800 or yPos < 0 or yPos >= 800:
            return True
        # Check if the move is legal:
        start_x, start_y = self.selected_piece_original_position
        start_x *= 100
        start_y *= 100
        if start_x == xPos and start_y == yPos:
            return True
        uci_move = self.convert_board_location(start_x, start_y, False) + self.convert_board_location(xPos, yPos, False)
        if chess.Move.from_uci(uci_move) in self.game.legal_moves:
            return False
        return True

    def on_start(self, event):
        clicked_square = (event.x // 100, event.y // 100)
        if clicked_square in self.piece_location_dictionary:
            self.selected_piece = self.piece_location_dictionary[clicked_square]
            self.selected_piece_original_position = clicked_square

    def move(self, event):
        if self.selected_piece:
            self.canvas.moveto(self.selected_piece, event.x - 50, event.y - 50)

    # This function ensures the piece is centered on the square that it was dropped onto.
    #TODO: Need these squares to be valid, ie can't be out of bounds nor can it be an illegal move.
    #      If an illegal move is made, return the piece to its original location
    def on_drop(self, event):
        if self.selected_piece:
            x = (event.x // 100) * 100
            y = (event.y // 100) * 100
            #check that the move is legal:
            if self.is_illegal_move(x, y):
                x,y = self.selected_piece_original_position
                x *= 100
                y *= 100
            self.make_move(x, y)
            self.selected_piece = False
            self.selected_piece_original_position = None


if __name__ == "__main__":
    window = tk.Tk()
    chess_board = ChessBoard(window)
    window.mainloop()