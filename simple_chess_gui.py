import tkinter

#create and size window:
window = tkinter.Tk()
window.geometry("850x850")
window.configure(background="gray")

#create canvas:
canvas = tkinter.Canvas(window, highlightbackground= "black", width=800, height=800)
canvas.place(relx=.5, rely=.5, anchor=tkinter.CENTER)
#create squares of board:
for row in range(8):
    for column in range(8):
        if (row + column) % 2 == 0:
            color="#F0D9B5"
        else:
            color="#B58863"
        canvas.create_rectangle(row * 100 + 1, column * 100 + 1, (row + 1) * 100 + 1, (column + 1) * 100 + 1, 
                                fill=color)

canvas.create_rectangle
canvas.pack()


window.mainloop()