import tkinter as tk
from gui.login import LoginWindow

def main():
    root = tk.Tk()
    root.title('🌸 Quản lý cửa hàng bán hoa 🌸')
    root.geometry('1000x650')
    root.configure(bg='#f8f8ff')
    LoginWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
