import tkinter as tk
import sys

def startUI():
    root = tk.Tk()
    mainRoot = tk.Tk()
    configWindow = tk.Tk()
    mainRoot.withdraw()
    configWindow.withdraw()

    root.geometry("960x540")

    def MaintoConf():
        mainRoot.withdraw()
        configWindow.deiconify()
        config()

    def ConftoMain():
        configWindow.withdraw()
        mainRoot.deiconify()
        mainUI

    def toConfig():
        mainRoot.withdraw()
        configWindow.deiconify()

    def quit():
        sys.exit()

    def mainUI():
        labelAsk.pack(padx=20, pady=20)
        labelInstruct.pack(padx=20, pady=20)
        configButton.pack()
        exitButton.pack()

    def config():
        calibrateButton.pack()
        backConfig.pack()

    def countdown(time):
        if time == -1:
            root.destroy()
            mainUI()
            mainRoot.deiconify()
        else:
            if time == 0:
                label.configure(text="Loaded successfully")
                labelWelcome.destroy()
                label.pack(padx=20, pady=225)
            else:
                label.configure(text="time remaining: %d seconds" % time)

            root.after(1000, countdown, time-1)

    # root Widgets
    labelWelcome = tk.Label(root, text="Starting...", font=('Arial', 20))
    labelWelcome.pack(padx=20, pady=225)
    label = tk.Label(root, font=('Arial', 20))
    label.pack()

    # mainRoot Widgets
    labelAsk = tk.Label(mainRoot, text="What do you want to do?", font=('Arial', 20))
    labelInstruct = tk.Label(mainRoot, text="Say what you want to do, or click manually", font=('Arial', 20))
    configButton = tk.Button(mainRoot, text="Configure", font=('Arial', 15), command=MaintoConf)
    exitButton = tk.Button(mainRoot, text="Exit", font=('Arial', 15), command=quit)

    # configWindow Widgets
    calibrateButton = tk.Button(configWindow, text="Calibrate", font=('Arial', 15))
    backConfig = tk.Button(configWindow, text="Back", font=('Arial', 15), command=ConftoMain)

    countdown(5)

    root.mainloop()