from tkinter import *
from PIL import Image, ImageTk

# Create and size window:
window = Tk()
window.geometry("850x850")
window.configure(background="gray")

# Label for testing:
coords_label = Label(window, text='TESTING TEXT')
coords_label.pack()

# Create canvas:
canvas = Canvas(window, highlightbackground= "black", width=800, height=800)
canvas.pack(pady=1)

# Create the squares of the board:
for row in range(8):
    for column in range(8):
        if (row + column) % 2 == 0:
            color="#F0D9B5"
        else:
            color="#B58863"
        canvas.create_rectangle(row * 100 + 1, column * 100 + 1, (row + 1) * 100 + 1, (column + 1) * 100 + 1, 
                                fill=color)

#Adding the pieces to the board:

# Dictionary to hold image references
image_references = {}
pieces = {}
piece_dictionary = {
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
def set_piece(fen_piece, xPos, yPos):
    global img
    file = "piece_images\\" + piece_dictionary[fen_piece]
    img = ImageTk.PhotoImage( Image.open(file).convert('RGBA').resize((100, 100)) )
    image_references[(xPos // 100, yPos // 100)] = img
    pieces[(xPos // 100, yPos // 100)] = canvas.create_image(xPos, yPos, image=img)

#TODO: Need to reset image_references every time this is called.
def set_up_from_FEN(fen):
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
            set_piece(char, col * 100 + 50, row * 100  + 50)
            col += 1

# Convert coordinates to chess notation for that square:
def convert_board_location(xPos, yPos, boardIsFlipped):
    x = xPos // 100
    y = yPos // 100
    if boardIsFlipped:
        x = 7 - x
        y += 1
    else:
        y = 8 - y
    return chr(97 + x) + str(y)

# Drag and Drop functionality:

# This function chooses which piece is getting dragged.
grabbed_piece = FALSE
def on_start(event):
    clicked_square = (event.x // 100, event.y // 100)
    if clicked_square in pieces:
        global grabbed_piece
        grabbed_piece = pieces[clicked_square]

def move(event):
    if grabbed_piece:
        canvas.moveto(grabbed_piece, event.x - 50, event.y - 50)
    # coords_label.config(text="Coordinates: " + str(event.x) + ", " + str(event.y))

# This function ensures the piece is centered on the square that it was dropped onto.
#TODO: Need these squares to be valid, ie can't be out of bounds nor can it be an illegal move.
#      If an illegal move is made, return the piece to its original location
def on_drop(event):
    global grabbed_piece
    if grabbed_piece:
        coords = canvas.coords(grabbed_piece)
        x = (coords[0] // 100) * 100
        y = (coords[1] // 100) * 100
        canvas.moveto(grabbed_piece, x, y)
        grabbed_piece = FALSE

# Binds:
canvas.bind("<ButtonPress-1>", on_start)
canvas.bind("<B1-Motion>", move)
canvas.bind("<ButtonRelease-1>", on_drop)

#Testing FEN functionality
starting_position_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
set_up_from_FEN(starting_position_fen)

window.mainloop()