from tkinter import *
from PIL import Image, ImageTk
import drag_manager as dm

# Create and size window:
window = Tk()
window.geometry("850x850")
window.configure(background="gray")

# Label for testing:
coords_label = Label(window, text='TESTING')
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
image = Image.open("piece_images\\black_queen.png").convert('RGBA')
resized_image = image.resize((100, 100))
photo_image = ImageTk.PhotoImage(resized_image)
piece = canvas.create_image(150, 150, image=photo_image)

# Drag and Drop functionality:
# This function chooses which piece is getting dragged.
#TODO: Finish functionality.
def on_start(event):
    # Note for future: event.x and event.y are the coordinates of where the mouse was clicked.
    pass

def move(event):
    canvas.moveto(piece, event.x - 50, event.y - 50)
    coords_label.config(text="Coordinates: " + str(event.x) + ", " + str(event.y))

# This function ensures the piece is centered on the square that it was dropped onto.
#TODO: Need these squares to be valid, ie can't be out of bounds nor can it be an illegal move
def on_drop(event):
    coords = canvas.coords(piece)
    x = (coords[0] // 100) * 100
    y = (coords[1] // 100) * 100
    canvas.moveto(piece, x, y)

# Binds:
canvas.bind("<ButtonPress-1>", on_start)
canvas.bind("<B1-Motion>", move)
canvas.bind("<ButtonRelease-1>", on_drop)


window.mainloop()