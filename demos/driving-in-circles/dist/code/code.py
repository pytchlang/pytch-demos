import pytch
import math
import random

n_cars = 11


class Track(pytch.Stage):
    Backdrops = ["racetrack.png"]


class Car(pytch.Sprite):
    Costumes = ["blue-car.png", "red-car.png"]

    def prepare_step(self):
        if random.random() < 0.0025:
            self.wanted_speed = 0.5 + random.random() * 1.0
        next_theta = Car.all_cars[self.next_idx].theta
        max_speed = (next_theta - 15 - self.theta) % 360
        actual_speed = min(self.wanted_speed, max_speed)
        self.wanted_theta = self.theta + actual_speed

    def act_step(self):
        self.theta = self.wanted_theta
        if self.theta >= 360:
            self.theta -= 360
        self.set_pose()

    def set_pose(self):
        # Our theta is our position on the track in DEGREES
        th = self.direction * self.theta
        x = self.radius * math.cos(math.pi * th / 180.0)
        y = self.radius * math.sin(math.pi * th / 180.0)
        r = self.direction * (self.theta + 90)
        self.go_to_xy(x, y)
        self.point_degrees(r)

    @pytch.non_yielding_loops
    def step(self):
        for c in Car.all_cars:
            c.prepare_step()
        for c in Car.all_cars:
            c.act_step()

    @pytch.when_green_flag_clicked
    def create_cars(self):
        self.wanted_speed = 1.0
        self.direction = 1
        self.radius = 135.5
        for i in range(n_cars):
            self.next_idx = (i + 1) % n_cars
            self.theta = 360 * i / n_cars
            pytch.create_clone_of(self)
        self.radius = 155.5
        self.direction = -1
        self.next_costume()
        for i in range(n_cars):
            self.next_idx = n_cars + (i + 1) % n_cars
            self.theta = 360 * i / n_cars
            pytch.create_clone_of(self)
        self.hide()
        Car.all_cars = Car.all_clones()
        while True:
            self.step()
