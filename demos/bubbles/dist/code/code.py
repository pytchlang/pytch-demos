import pytch
from math import pi, cos, sin
import random

# Inspired by "Recreate Pang’s sprite spawning mechanic"
# in Wireframe 10 (https://wireframe.raspberrypi.org/issues/10)


class Enemy(pytch.Sprite):
    Costumes = ["shinyorb.png"]
    Size_by_generation = [1.0, 0.7, 0.5, 0.35, 0.25]

    @pytch.when_green_flag_clicked
    def init(self):
        self.generation = 0
        self.go_to_xy(0, 120)
        self.drift_down()

    @pytch.when_this_sprite_clicked
    def split(self):
        self.generation += 1
        if self.generation < len(self.Size_by_generation):
            self.split_dir = -1
            pytch.create_clone_of(self)
            self.split_dir = +1
            pytch.create_clone_of(self)
        self.hide()

    @pytch.when_I_start_as_a_clone
    def separate_and_shrink(self):
        new_size = self.Size_by_generation[self.generation]
        self.change_x(self.split_dir * 80 * new_size)
        self.change_y(random.random() * 80 * new_size)
        self.set_size(new_size)
        self.drift_down()

    def drift_down(self):
        t = random.random() * 2.0 * pi
        speed = -0.15 - 0.1 * random.random()
        while True:
            self.change_y(speed + 0.15 * self.size * sin(2 * t))
            self.change_x(0.25 * self.size * cos(t))
            t += 0.025


class Sky(pytch.Stage):
    Backdrops = ["starry-sky.jpg"]


# Image credits:
#
# shinyorb.png
#   https://openclipart.org/detail/3806/shiny-orb
#   Image by OpenClipArt user "noonespillow"
#   Placed into the public domain by creator
#
# starry-sky.jpg
#   https://unsplash.com/photos/LUpDjlJv4_c
#   Photo by Andy Holmes (https://unsplash.com/@andyjh07)
#   Excerpt taken and darkened
#   Used under the Unsplash License
