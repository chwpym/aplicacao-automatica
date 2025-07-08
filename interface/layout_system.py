# Utilitário para centralizar janelas Tkinter

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width/2 - width/2)
    center_y = int(screen_height/2 - height/2)
    window.geometry(f"{width}x{height}+{center_x}+{center_y}") 