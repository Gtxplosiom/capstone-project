import tkinter as tk

class Animate:
    def __init__(self, root):
        self.root = root
        self.root_width = 300
        self.root_height = 300
        self.x = 0
        self.y = 0

        self.root.geometry(f'{self.root_width}x{self.root_height}+{self.x}+{self.y}')

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.root_state = self.screen_height

        self.button_resize = tk.Button(root, text="Resize", command=self.resize)
        self.button_resize.place(x=0, y=0)

        self.button_move = tk.Button(root, text="Move", command=self.move)
        self.button_move.place(x=0, y=50)

        self.sidebar()

    def resize(self):
        self.root_width += 50
        self.root_height += 50
        root.geometry(f'{self.root_width}x{self.root_height}')

    def move(self):
        self.x += 50
        root.geometry(f'{self.root_width}x{self.root_height}+{self.x}+{self.y}')

    def animate_move(self):
        self.x += 5

        self.root.geometry(f'{self.root_width}x{self.root_height}+{self.x}+{self.y}')

        if self.screen_width <= 0:
            self.root.after(5, self.animate_move)
        else:
            print("Reached screen width.")
            self.root.destroy()

    def sidebar(self):
        self.x += 5

        self.root_state -= 2.8

        self.root.geometry(f'{self.root_width}x{self.root_height}+{self.x}+{self.y}')

        print(self.root_state)

        if self.root_state <= 50:
            print("sidebar-ed")
        else:
            self.root.after(10, self.sidebar)

if __name__ == '__main__':
    root = tk.Tk()
    app = Animate(root)
    root.mainloop()
