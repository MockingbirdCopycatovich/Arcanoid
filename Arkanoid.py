from tkinter import *
from random import randint

WIDTH = 802
HEIGHT = 600
DELAY = 20
BALL_RADIUS = 10
SPEED_X = 5
SPEED_Y = - 5
craft_width = 120
craft_height = 20
text_position_x = 50
text_position_y = HEIGHT - 10
level_of_diff = 5
brick_width = 78
brick_height = 20
wictory_flag = False



TITLE = "Arkanoid"

win = Tk()
win.title(TITLE)
win.geometry(str(WIDTH)+"x"+str(HEIGHT))



canvas = Canvas(win, width=WIDTH, height=HEIGHT)
canvas.pack()

colors = ['green', 'blue', 'yellow', 'purple', 'orange', 'brown', 'magenta', 'lime', 'pink', 'red', 'grey', 'cyan']
class Score:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.text_id = canvas.create_text(self.x, self.y, text= "Score: " + str(self.score),
                                          font=('Times New Roman', 12), fill='black')

class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.canvas_object = canvas.create_rectangle(self.x - self.width // 2, self.y - self.height // 2,
                                                     self.x +self.width // 2, self.y + self.height // 2,
                                                     fill=self.color, outline='black')
class Craft:
    def __init__(self, x, y, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.y = y
        self.x = x
        self.canvas_object = canvas.create_rectangle(self.x - self.width // 2, self.y - self.height // 2,
                                                     self.x + self.width // 2, self.y + self.height // 2,
                                                     fill=self.color, outline='black')

    def draw(self):
        if self.x < self.width // 2:
            self.x = self.width // 2
        if self.x > WIDTH - self.width // 2:
            self.x = WIDTH - self.width // 2
        canvas.coords(self.canvas_object, self.x - self.width // 2, self.y - self.height // 2,
                                                     self.x + self.width // 2, self.y + self.height // 2)
class Ball:
    def __init__(self, x, y, speed_x, speed_y, radius, color):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.color = color
        self.flag = True
        self.last_positions = []
        self.tail_objects = []
        self.canvas_object = canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                                fill=self.color, outline='black')

    def draw(self):
        self.clear_tail()
        self.draw_tail()
        canvas.coords(self.canvas_object, self.x - self.radius, self.y - self.radius, self.x + self.radius,
                      self.y + self.radius)

    def move(self):

        self.last_positions.append((self.x, self.y))
        if len(self.last_positions) > 5:
            self.last_positions.pop(0)

        self.x = self.x + self.speed_x
        if self.x >= WIDTH - self.radius:
            self.speed_x = - abs(self.speed_x)
        if self.x <= self.radius:
            self.speed_x = abs(self.speed_x)
        self.y = self.y + self.speed_y
        if self.y >= HEIGHT - self.radius:
            self.flag = False
            self.speed_y = - abs(self.speed_y)
        if self.y <= self.radius:
            self.speed_y = abs(self.speed_y)
    def craft_collision(self):
        l_site = c.x - c.width // 2
        r_site = c.x + c.width // 2
        platform_top = c.y - c.height // 2

        if platform_top <= self.y + self.radius <= c.y + c.height // 2:
            if l_site <= self.x and self.x <= r_site:
                self.speed_y = -abs(self.speed_y)
                hit_position = (self.x - c.x) / (c.width / 2)
                self.speed_x = hit_position * 10

    def brick_collision(self):
        for shtuka in bricks:
            x1 = shtuka.x - shtuka.width // 2
            x2 = shtuka.x + shtuka.width // 2
            y1 = shtuka.y - shtuka.height // 2
            y2 = shtuka.y + shtuka.height // 2

            if (y1 <= self.y <= y2 or y1 <= self.y + self.radius <= y2) and x1 <= self.x <= x2:
                if b.flag:
                    canvas.delete(shtuka.canvas_object)
                if b.flag:
                    bricks.remove(shtuka)
                if b.flag:
                    s.score += 10
                if b.flag:
                    canvas.itemconfig(s.text_id, text= "Score: " + str(s.score))
                self.speed_y *= -1
                break

    def draw_tail(self):
        for i, (x, y) in enumerate(self.last_positions):
            tail_radius = self.radius * (0.6 - i * 0.1)
            tail_object = canvas.create_oval(x - tail_radius, y - tail_radius, x + tail_radius, y + tail_radius,
                                             fill=self.color, outline='')

            self.tail_objects.append(tail_object)

    def clear_tail(self):
        for obj in self.tail_objects:
            canvas.delete(obj)
        self.tail_objects.clear()


def move(event):
    if not b.flag and not wictory_flag:
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text="You Lost!", font=('Times New Roman', 30), fill='gold')
        canvas.delete(c.canvas_object)
        return
    elif not wictory_flag:
        c.x = event.x
        c.draw()


def check_win():
    global wictory_flag
    if not bricks:
        wictory_flag = True
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text="You Win!", font=('Times New Roman', 30), fill='gold')
        return True
    return False


def animation():
    if not wictory_flag:
        check_win()
        b.brick_collision()
        b.craft_collision()
        b.move()
        b.draw()
        canvas.after(DELAY, animation)



ball_color = colors[randint(0, len(colors)-1)]
colors.remove(ball_color)
craft_color = colors[randint(0, len(colors)-1)]
colors.remove(craft_color)
b = Ball(WIDTH // 2, HEIGHT // 3 * 2, SPEED_X, SPEED_Y, BALL_RADIUS, ball_color)
c = Craft(WIDTH / 2, HEIGHT - 100, craft_width, craft_height, craft_color)
s = Score(text_position_x, text_position_y, 0)
bricks = []
skip_y = 2 * brick_height // 3
for i in range(0, level_of_diff):
    brick_color = colors[randint(0, len(colors)-1)]
    colors.remove(brick_color)
    skip_x = 40
    for j in range(0, 10):
        bricks.append( Brick(skip_x, skip_y,
                             brick_width, brick_height, brick_color))
        skip_x = skip_x + 2 + brick_width
    skip_y += 2 + brick_height


win.bind('<Motion>', move)
animation()
canvas.configure(bg='lightblue')
win.mainloop()