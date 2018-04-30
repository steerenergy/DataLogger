# This uses tkinter which is a really common multi-platform GUI

from tkinter import *
from tkinter import font


class Window(Frame):
    # Main Window
    def __init__(self, master=None):
        # This is class inheritance
        Frame.__init__(self, master)
        # Setting self.master = master window
        self.master = master
        # Run init_window() function
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # Changing the title of our master widget
        self.master.title("Data Logger")
        self.pack()

        #Title
        self.label = Label(self, text="Data Logger",font=chosenFont)
        self.label.pack()

        # Creating a button instance
        self.logButton = Button(text="Start Logging", height=4, width=20, command=self.test, font=chosenFont)
        self.logButton.pack(side=TOP)

    def test(self):
        if self.logButton['text'] == "Start Logging":
            print("Logging Start")
            self.logButton.config(text="Finish Logging")
        else:
            print("Logging Finish")
            self.logButton.config(text="Start Logging")

    def client_exit(self):
        exit()


# Create Tkinter Instance
root = Tk()

# Size of the window
root.state('zoomed')
chosenFont = font.Font(family="Helvetica", size=20, weight=font.BOLD)

app = Window(root)
root.mainloop()