import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from CluePuzzleSolver import Player, ProbabilityTable

class MainApp(tk.Tk):
   def __init__(self):
       tk.Tk.__init__(self)
       self.title("Clue Solver")
       self.geometry("400x500")
       self.selected_player = None
       self.frames = {}

       for F in (StartPage, PageOne, PageTwo):
           frame = F(self)
           self.frames[F] = frame
           frame.place(relx=0, rely=0, relwidth=1, relheight=1)

       self.show_frame(StartPage)

   def show_frame(self, cont):
       frame = self.frames[cont]
       frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Player Page", font=("Helvetica", 17))
        label.pack(fill=tk.BOTH)
        self.parent = parent
        self.players = ['Computer', 'Player 2', 'Player 3', 'Player 4']
        for player_name in self.players:
            button = tk.Button(self, text=player_name, command=lambda p=player_name: self.select_player(p))
            button.pack()

    def select_player(self, player_name):
        self.parent.selected_player = Player(player_name)
        self.parent.show_frame(PageOne)

class PageOne(tk.Frame):
    def __init__(self, parent):
       tk.Frame.__init__(self, parent)
       self.parent = parent
       self.selected_player = self.parent.selected_player
       player_name = self.selected_player.name if self.selected_player else 'No player selected'
       label = tk.Label(self, text=f"Selected player: {self.selected_player}", font=("Helvetica", 17))
       label.pack(fill=tk.BOTH)
       
       if self.selected_player:
            for method_name in dir(self.selected_player):
                if callable(getattr(self.selected_player, method_name)) and not method_name.startswith("__"):
                    button = tk.Button(self, text=method_name, command=lambda m=method_name: self.call_method(m))
                    button.pack()

       back_button = tk.Button(self, text="Back to Start Page", command=self.go_to_start_page)
       back_button.pack()
       
    def go_to_start_page(self):
        self.parent.show_frame(StartPage)

class PageTwo(tk.Frame):
   def __init__(self, parent):
       tk.Frame.__init__(self, parent)
       label = tk.Label(self, text="Page Two", font=("Helvetica", 17))
       label.pack(fill=tk.BOTH)

app = MainApp()
app.mainloop()