from tkinter import *
from screeninfo import get_monitors
from PIL import Image, ImageTk
from src.TicTacToe import TicTacToe


class AppGui:
    def __init__(
            self,
            name: str,
            width: int = 760,
            height: int = 760,
            bg: str = '#222'
    ):
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2

        self.__bg = bg
        self.__root = Tk()
        self.__root.title(name)
        self.__root.geometry(f'{width}x{height}+{x_position}+{y_position}')
        self.__root.resizable(False, False)
        self.__root.config(bg=self.__bg)
        self.__game = TicTacToe()
        self.__font_size = 20
        self.__button = {
            'width': int((width / self.__font_size) / 3 + 3),
            'height': int((height / (self.__font_size * 3)) / 3 + 3),
        }
        self.__pole = Frame(self.__root)
        self.__pole.pack()
        self.__status = Frame(self.__root)
        self.__status.pack()

    def run(self):
        self.__game.init()
        self.__show_field()
        self.__show_status()
        self.__root.mainloop()

    def __show_field(self):
        row = 0
        for line in self.__game.fields:
            row += 1
            column = 0
            for cell in line:
                column += 1
                self.__show_button(self.__pole, row, column, cell.value)

    def __clear(self):
        for widget in self.__pole.winfo_children():
            widget.destroy()
        for widget in self.__status.winfo_children():
            widget.destroy()

    def __show_status(self):
        if self.__game.is_human_win:
            status_text = 'You win!'
        elif self.__game.is_computer_win:
            status_text = 'You loose!'
        elif self.__game.is_draw:
            status_text = 'Draw..'
        else:
            status_text = 'Your turn..'

        status_label = Label(
            self.__status,
            text=status_text,
            bg=self.__bg,
            fg='#fff',
            font=('Arial', self.__font_size),
            pady=10,
        )
        status_label.pack()

    def __show_button(self, parent, row: int, column: int, value: int):
        img_size = (220, 220)
        if value > 0:
            image_file = "bot.png" if value == 2 else "human.png"
            image = Image.open('./static/' + image_file)
            image = image.resize(img_size)
            button_function = lambda: self.__is_not_emoty()
        else:
            image = Image.new("RGB", img_size, "white")
            button_function = lambda: self.__button_click(row, column)

        photo = ImageTk.PhotoImage(image)

        button = Button(
            parent,
            command=button_function,
            bd=1,
            bg='#fff',
            activebackground='#fff',
            foreground='#fff',
            width=self.__button['width'],
            height=self.__button['height'],
            font=('Arial', self.__font_size),
        )
        button.config(width=225, height=225)
        button.config(image=photo, compound=CENTER, bg="white")
        button.image = photo
        button.grid(row=row, column=column)

    def __button_click(self, row: int, column: int):
        if bool(self.__game):
            self.__game.human_go(row, column)
            if bool(self.__game):
                self.__game.computer_go()
        else:
            self.__game.init()
        self.__update()

    def __is_not_emoty(self):
        if not bool(self.__game):
            self.__game.init()
            self.__update()

    def __update(self):
        self.__clear()
        self.__show_status()
        self.__show_field()
