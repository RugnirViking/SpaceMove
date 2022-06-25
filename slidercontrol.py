import pygame


class SliderControl():
    # a class that uses pygame to display a slider
    # the slider is a rectangle with a line in the middle
    # the line can be moved around to change the value
    # the value is a float between 0 and 1
    # the value is updated when the line is moved

    def __init__(self, x, y, width, height, label, color, fgcolor=(0,0,0),value=0.5, min_value=0, max_value=1):
        # stores all the variables and sets the initial values
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.label = label
        self.line_width = 2
        self.line_color = fgcolor
        self.background_color = color
        self.drag_start_pos = (0,0)
        self.dragging = False
        self.hasmoved = False

    def draw(self, surface, engine):
        # draws a line the width of the slider, and draws a narrow box at the position indicated by the value

        pygame.draw.rect(surface, self.background_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.line_color, (self.x, self.y, self.width, self.height), self.line_width)
        pygame.draw.rect(surface, self.line_color, (self.x + self.value * self.width, self.y, self.line_width, self.height))

        # draws the label text
        font=engine.smallfont2
        text = font.render(str(int(self.value * 100)) + "%", True, self.line_color)
        textRect = text.get_rect()
        textRect.right = self.x + self.width / 2
        textRect.centery = self.y + self.height / 2
        surface.blit(text, textRect)

        # draws the label text
        font=engine.smallfont
        text = font.render(self.label, True, self.background_color)
        textRect = text.get_rect()
        textRect.right = self.x - 40
        textRect.centery = self.y + self.height / 2
        surface.blit(text, textRect)



    def mouseup(self, pos):
        if self.dragging and not self.hasmoved:
            self.dragging = False
            self.hasmoved = False
            if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
                self.value = (pos[0] - self.x) / self.width
            return True
        elif self.dragging:
            self.dragging = False
            self.hasmoved = False
            return True
        else:
            # sets the value to the position of the mouse click
            if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
                self.value = (pos[0] - self.x) / self.width
                return True
            else:
                return False


    def mousedown(self, pos):
        # if the mouse is clicked, start a drag event
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            self.drag_start_pos = pos
            self.dragging = True

    def mousemove(self, pos):
        # if the mouse is dragged, update the value
        if self.dragging:
            self.value = (pos[0] - self.drag_start_pos[0]) / self.width + (self.drag_start_pos[0]-self.x) / self.width
            if self.value < 0:
                self.value = 0
            if self.value > 1:
                self.value = 1
            self.hasmoved=True

