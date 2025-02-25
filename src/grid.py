class Grid:
    def __init__(self, position):
        self.position = position
        self.number = 0
        self.clicked = False
        self.hover = False  # Add hover state
        self.wrong = False  # Add wrong state
        self.IsUserInput = False
        self.OrignalNumber = 0

    def generate_number(self, number):
        self.number = number
        self.OrignalNumber=number

    def click(self, start_number, max_number):
        if self.clicked:
            return None
        if start_number <= max_number:
            self.clicked = True
            self.number = start_number
            return self.number
        return None

    def reset(self):
        self.clicked = False
        self.number = 0

    def is_clicked(self):
        return self.clicked

    def get_position(self):
        return self.position

    def get_number(self):
        return self.number

    def set_hover(self, hover):
        self.hover = hover

    def is_hover(self):
        return self.hover