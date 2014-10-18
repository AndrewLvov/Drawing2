from tkinter import Tk, Canvas, BOTH
from math import sqrt


WIDTH = 400
HEIGHT = 400


class Shape:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y

    def draw(self):
        raise NotImplementedError('Shape cannot be drawn!')


class Circle(Shape):
    def __init__(self, canvas, x, y, radius):
        super(Circle, self).__init__(canvas, x, y)
        self.radius = radius

    def draw(self):
        left = self.x - self.radius * sqrt(2)
        right = self.x + self.radius * sqrt(2)
        top = self.y - self.radius * sqrt(2)
        bottom = self.y + self.radius * sqrt(2)
        self.canvas.create_oval(left, top, right, bottom)


class Rectangle(Shape):
    def __init__(self, canvas, x, y, right, bottom):
        super(Rectangle, self).__init__(canvas, x, y)
        self.right = right
        self.bottom = bottom

    def draw(self):
        left = 2 * self.x - self.right
        right = self.right
        top = 2 * self.y - self.bottom
        bottom = self.bottom
        self.canvas.create_rectangle(left, top, right, bottom)


class XSquareGraph(Shape):
    def __init__(self, canvas, x, y, left, right):
        super(XSquareGraph, self).__init__(canvas, x, y)
        self.left = left
        self.right = right

    def draw(self):
        def f(x):
            return x*x
        start_x = self.left
        for i in range(self.left, self.right):
            self.canvas.create_line(start_x + self.x, HEIGHT - (f(start_x) + self.y),
                                    i + self.x, HEIGHT - (f(i) + self.y))
            start_x = i


def draw_from_script(filename, canvas):
    with open(filename, 'r') as f:
        for line in f:
            # shape coord1 coord2 coord3 ...
            # line = circle 20 20 30
            # split: ['circle', '20', '20', '30']
            # конструкция вот такая:
            # shape, x, y, *params = ['circle', '20', '20', '30']
            # *params подхватит все остальные элементы массива
            # запишет 'circle' в shape, '20' в x, '20' в y, и ['30'] в params
            shape, x, y, *params = line.split()
            x = int(x)
            y = int(y)
            params = map(int, params)
            if shape == 'circle':
                c = Circle(canvas, x, y, *params)
                c.draw()
            elif shape == 'rect':
                # если params = [200, 200],
                # получится вызов Rectangle(canvas, x, y, 200, 200)
                r = Rectangle(canvas, x, y, *params)
                r.draw()
            elif shape == 'x2_graph':
                g = XSquareGraph(canvas, x, y, *params)
                g.draw()


def draw_custom(canvas):
    canvas.create_line(0, 0, 50, 50)


def main():
    root = Tk()
    root.title = 'BitCoin graph'
    root.geometry("{}x{}".format(WIDTH, HEIGHT))
    canvas = Canvas(root)
    canvas.pack(fill=BOTH, expand=1)

    try:
        draw_from_script('shapes.txt', canvas)
    except IOError:
        draw_custom(canvas)

    root.mainloop()

if __name__ == '__main__':
    main()