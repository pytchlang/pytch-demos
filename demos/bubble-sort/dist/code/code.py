import pytch
import random


def x_from_idx(idx):
    return -220 + 40 * idx


class Background(pytch.Stage):
    Backdrops = ["solid-blue.png"]

    @pytch.when_stage_clicked
    def do_sort(self):
        cursor = Cursor.the_original()
        bars = Bar.all_instances()
        random.shuffle(bars)
        for i, bar in enumerate(bars):
            bar.move_to_slot(i)
        cursor.show()
        correctly_sorted = False
        while not correctly_sorted:
            correctly_sorted = True
            for i in range(len(bars) - 1):
                cursor.move_to_slot_and_next(i)
                pytch.wait_seconds(0.25)
                if bars[i].costume_number > bars[i + 1].costume_number:
                    correctly_sorted = False
                    bars[i], bars[i + 1] = bars[i + 1], bars[i]
                    bars[i].move_to_slot(i)
                    bars[i + 1].move_to_slot(i + 1)
                    pytch.wait_seconds(0.25)
        cursor.hide()


class Cursor(pytch.Sprite):
    Costumes = ["cursor.png"]

    def move_to_slot_and_next(self, idx):
        self.go_to_xy(x_from_idx(idx) + 20, 0)


class Bar(pytch.Sprite):
    Costumes = [f"bar-{h}.png" for h in range(1, 13)]

    @pytch.when_green_flag_clicked
    def setup(self):
        self.go_to_xy(x_from_idx(0), 0)
        for i in range(11):
            pytch.create_clone_of(self)
            self.go_to_xy(x_from_idx(i + 1), 0)
            self.next_costume()

    def move_to_slot(self, idx):
        self.go_to_xy(x_from_idx(idx), 0)
