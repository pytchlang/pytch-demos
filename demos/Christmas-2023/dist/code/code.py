import pytch
import random

# Personalize and change this project to learn more about loops, conditionals,
# variables, random & some other Python concepts! We wish you a nice holiday!

# This is just a Python comment that helps you describe your program.
# To learn more about Pytch follow this tutorial:
# https://www.pytch.org/app/suggested-tutorial/hello

# The sprites images and sounds were created on Scratch and are copyright
# the Lifelong Kindergarten Group at MIT Media Lab, and are part of Scratch.
# We use them under the terms of the Creative Commons Attribution-ShareAlike
# 2.0 licence (see https://creativecommons.org/licenses/by-sa/2.0/).

# Music: BatchBug - Snowflake
# https://breakingcopyright.com/song/batchbug-snowflake
# Creative Commons (CC BY 3.0) https://creativecommons.org/licenses/by/3.0

class Reindeer(pytch.Sprite):
    Costumes = ["reindeer.png"]

    @pytch.when_green_flag_clicked
    def hide_me(self):
        self.go_to_xy(-180, -60)
        self.say_for_seconds("Hi there! Press the 's' key to add some snow and the 'm' key to get a surprise!", 7.0)
        self.hide()

class Snow(pytch.Sprite):
    Costumes = ["falling_snow.png"]

    @pytch.when_green_flag_clicked
    def hide_snow(self):
        self.hide()

    @pytch.when_key_pressed("s")
    def play(self):
        self.go_to_xy(0, 360)
        self.show()
        while True:  # Do the below forever:
            # Scroll down the snow image until we reach its end:
            while self.y_position > -360:
                self.change_y(-3)
            # Go back to the top of the image before scrolling down again:
            self.go_to_xy(0, 360)

class Penguin(pytch.Sprite):
    # Costumes is a list where the element in position 0 is penguin_christmas
    # and the element in position 1 is penguin_2024:
    Costumes = ["penguin_christmas.png", "penguin_2024.png"]

    Sounds = ["music.mp3"]

    @pytch.when_green_flag_clicked
    def hide_me(self):
        self.hide()
        # "random_costume" is a variable.  We assign it 0 or 1 randomly:
        random_costume = random.randint(0, 1)
        # and switch to that costume:
        self.switch_costume(random_costume)

    @pytch.when_key_pressed("m")
    def show_me(self):
        self.set_sound_volume(0.25)
        self.start_sound("music")

        self.go_to_xy(0, -60)
        self.show()
        # Check if the costume is the penguin_christmas one:
        if self.costume_number == 0:
            self.say("Merry Christmas everyone from the Pytch team!")
        else:
            # otherwise we must be using the "penguin_2024" one:
            self.say("The Pytch team wish you all a happy new year!")

class BlueSky(pytch.Stage):
    Backdrops = ["sky-1.png", "sky-2.png"]
    Sounds = ["snow.mp3"]

    @pytch.when_key_pressed("s")
    def snow(self):
        while True:
            self.play_sound_until_done("snow")
            self.switch_backdrop(1)
