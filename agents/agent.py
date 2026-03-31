import math

class Agent:

    def __init__(self, name, position, speed):
        self.name = name
        self.x, self.y = position
        self.speed = speed

    def distance_to(self, goal):
        gx, gy = goal
        return math.sqrt((self.x - gx) ** 2 + (self.y - gy) ** 2)