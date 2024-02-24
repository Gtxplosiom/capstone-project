import tkinter as tk
import sys

def StartUI():
    root = tk.Tk()
    main_root = tk.Tk()
    config_window = tk.Tk()
    main_root.withdraw()
    config_window.withdraw()

    root.geometry("960x540")

    def MaintoConf():
        main_root.withdraw()
        config_window.deiconify()
        Config()

    def ConftoMain():
        config_window.withdraw()
        main_root.deiconify()
        MainUI

    def toConfig():
        main_root.withdraw()
        config_window.deiconify()

    def Quit():
        sys.exit()

    def MainUI():
        label_ask.pack(padx=20, pady=20)
        label_instruct.pack(padx=20, pady=20)
        config_button.pack()
        exit_button.pack()

    def Config():
        calibrate_button.pack()
        back_config.pack()

    def Countdown(time):
        if time == -1:
            root.destroy()
            MainUI()
            main_root.deiconify()
        else:
            if time == 0:
                label.configure(text="Loaded successfully")
                label_welcome.destroy()
                label.pack(padx=20, pady=225)
            else:
                label.configure(text="time remaining: %d seconds" % time)

            root.after(1000, Countdown, time-1)

    def HideHighlight():
        highlight.withdraw()

    def ShowHighlight():
        highlight.deiconify()

    # root Widgets
    label_welcome = tk.Label(root, text="Starting...", font=('Arial', 20))
    label_welcome.pack(padx=20, pady=225)
    label = tk.Label(root, font=('Arial', 20))
    label.pack()
    label2 = tk.Label(root, font=('Arial', 20))
    label2.pack()

    # main_root Widgets
    label_ask = tk.Label(main_root, text="What do you want to do?", font=('Arial', 20))
    label_instruct = tk.Label(main_root, text="Say what you want to do, or click manually", font=('Arial', 20))
    config_button = tk.Button(main_root, text="Configure", font=('Arial', 15), command=MaintoConf)
    exit_button = tk.Button(main_root, text="Exit", font=('Arial', 15), command=Quit)

    # config_window Widgets
    calibrate_button = tk.Button(config_window, text="Calibrate", font=('Arial', 15))
    back_config = tk.Button(config_window, text="Back", font=('Arial', 15), command=ConftoMain)

    # clickOnScreen highlighter widgets
    highlight = tk.Tk()
    highlight.attributes('-alpha', 0.5)
    highlight.attributes('-fullscreen', True)
    canvas_highlight = tk.Canvas(highlight, bg='black')
    canvas_highlight.pack(fill='both', expand=True)

    Countdown(5)

    HideHighlight()

    root.mainloop()