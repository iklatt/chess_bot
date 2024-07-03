import tkinter as tk
from PIL import Image, ImageTk
import chess

class ChessPiece:
    def __init__(self, fenChar, xPos, yPos, image, canvasObject):
        self.x = xPos
        self.y = yPos
        self.image = image
        self.fen = fenChar
        self.piece = canvasObject
    
    def move(self, newX, newY):
        self.x = newX
        self.y = newY
    
    def promote(self, newFenChar, newImage, newCanvasObject):
        self.fen = newFenChar
        self.image = newImage
        self.piece = newCanvasObject

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
        self.game = chess.Board()

        self.initialize_pieces()
        self.from_fen()
        
        self.selected_piece = False

        # Bindings for drag and drop
        self.canvas.bind("<ButtonPress-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)
    

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
    

    def initialize_pieces(self):
        fen_pieces = "KQRRBBNNPPPPPPPPkqrrbbnnpppppppp"
        xPos = 0
        yPos = 0
        for fen_char in fen_pieces:
            file = "piece_images\\" + self.fen_to_image_dictionary[fen_char]
            image = ImageTk.PhotoImage( Image.open(file).convert('RGBA').resize((100, 100)) )
            piece = ChessPiece(fen_char, xPos, yPos, image, self.canvas.create_image(xPos, yPos, image=image))
            self.pieces_list.append(piece)


    def from_fen(self):
        pieces = self.pieces_list.copy()
        fen = self.game.fen()
        row = 0
        col = 0
        for chr in fen:
            if chr == "/":
                row += 1
                col = 0
            elif chr == " ":
                break
            elif chr.isdigit():
                col += int(chr)
            else:
                for piece in pieces:
                    if piece.fen == chr:
                        self.canvas.moveto(piece.piece, col * 100, row * 100)
                        piece.move(col * 100, row * 100)
                        pieces.remove(piece)
                        col += 1
                        break
        print(fen)
        for i in range(len(pieces)):
            print("Removing:", pieces[i].fen)
            self.pieces_list.remove(pieces[i])


    def is_legal_pawn_promotion(self, uci_move):
        possible_promotions = ['q', 'r', 'n', 'b']
        black_is_promoting = self.selected_piece.fen == 'P' and uci_move[1] == '7' and uci_move[3] == '8'
        white_is_promoting = self.selected_piece.fen == 'p' and uci_move[1] == '2' and uci_move[3] == '1'
        if black_is_promoting or white_is_promoting:
            for promo in possible_promotions:
                if chess.Move.from_uci(uci_move + promo) in self.game.legal_moves:
                    return True
        return False

    #TODO: Get user input via buttons that appear on the screen
    def get_user_input(self):
        possible_input = ['q', 'r', 'b', 'n']
        user_input = ""
        while user_input not in possible_input:
            user_input = input("What do you want to promote to?")
        return user_input


    def promote_pawn(self, uci_move, xPos, yPos):
        x = xPos // 100 * 100
        y = yPos // 100 * 100
        promotion_char = self.get_user_input()
        uci_move += promotion_char
        self.game.push_uci(uci_move)
        if self.selected_piece.fen.isupper():
            promotion_char = promotion_char.upper()
        file = "piece_images\\" + self.fen_to_image_dictionary[promotion_char]
        image = ImageTk.PhotoImage( Image.open(file).convert('RGBA').resize((100, 100)) )
        new_piece = self.canvas.create_image(x, y, image=image)
        self.selected_piece.promote(promotion_char, image, new_piece)
        self.selected_piece.x = x
        self.selected_piece.y = y
        self.from_fen()


    def make_move(self, xPos, yPos):
        if xPos < 0 or xPos >= 800 or yPos < 0 or yPos >= 800:
            return False
        start_x = self.selected_piece.x
        start_y = self.selected_piece.y
        if start_x // 100 == xPos // 100 and start_y // 100 == yPos // 100:
            return False
        uci_move = self.convert_board_location(start_x, start_y, False) + self.convert_board_location(xPos, yPos, False)
        if chess.Move.from_uci(uci_move) in self.game.legal_moves:
            self.game.push_uci(uci_move)
            self.from_fen()
            return True
        # See if the move is a pawn promotion:
        if self.is_legal_pawn_promotion(uci_move):
            #Promote
            self.promote_pawn(uci_move, xPos, yPos)
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
    def on_drop(self, event):
        if self.selected_piece:
            x = event.x // 100 * 100
            y = event.y // 100 * 100
            #check that the move is legal, if it is make that move on self.game:
            if not self.make_move(x, y):
                self.canvas.moveto(self.selected_piece.piece, self.selected_piece.x, self.selected_piece.y)
            self.selected_piece = False

if __name__ == "__main__":
    window = tk.Tk()
    chess_board = ChessBoard(window)
    window.mainloop()