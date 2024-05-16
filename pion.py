import pygame

class Pion:
    def __init__(self, red, green, blue, type):
        self.red = red
        self.green = green
        self.blue = blue
        self.type = type
    
    def get_red(self):
        return self.red
    
    def get_green(self):
        return self.green
    
    def get_blue(self):
        return self.blue
    
    def get_type(self):
        return self.type