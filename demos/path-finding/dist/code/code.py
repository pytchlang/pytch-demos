import pytch
import random

island_stride = 76

# See end for sound credits.


class Background(pytch.Sprite):
    Costumes = ["background-square.png"]

    @pytch.when_green_flag_clicked
    def randomise_layout(self):
        islands = [
            (colour, number)
            for colour in "ABCD"
            for number in [1, 2, 3, 4]
        ]
        random.shuffle(islands)
        State.island_order = islands
        pytch.broadcast_and_wait("arrange-islands")


def coords_of_index(idx):
    row, col = divmod(idx, 4)
    x = (col - 1.5) * island_stride
    y = (row - 1.5) * island_stride
    return (x, y)


class State(pytch.Sprite):
    Costumes = []
    Sounds = ["buzzer.mp3"]

    # Will be created on green-flag by Background:
    island_order = []
    islands_clicked = []

    @pytch.when_I_receive("find-route")
    @pytch.non_yielding_loops
    def find_route(self):
        hops = [[] for _ in State.island_order]

        # Find hops within rows:
        for row_idx in range(4):
            for col_0 in range(4):
                idx_0 = row_idx * 4 + col_0
                kind_0 = State.island_order[idx_0]
                for col_1 in range(col_0 + 1, 4):
                    idx_1 = row_idx * 4 + col_1
                    kind_1 = State.island_order[idx_1]
                    if kind_0[0] == kind_1[0] or kind_0[1] == kind_1[1]:
                        hops[idx_0].append(idx_1)
                        hops[idx_1].append(idx_0)

        # Find hops within columns:
        for col_idx in range(4):
            for row_0 in range(4):
                idx_0 = row_0 * 4 + col_idx
                kind_0 = State.island_order[idx_0]
                for row_1 in range(row_0 + 1, 4):
                    idx_1 = row_1 * 4 + col_idx
                    kind_1 = State.island_order[idx_1]
                    if kind_0[0] == kind_1[0] or kind_0[1] == kind_1[1]:
                        hops[idx_0].append(idx_1)
                        hops[idx_1].append(idx_0)

        # Find shortest paths from source node, stopping
        # if we hit destination node.
        start = State.islands_clicked[0]
        goal = State.islands_clicked[1]
        seen = {start}
        previous_island = [None for i in State.island_order]
        print(seen)
        queue = [start]
        while len(queue) > 0:
            island = queue.pop(0)
            if island == goal:
                break
            for next_island in hops[island]:
                if next_island not in seen:
                    previous_island[next_island] = island
                    seen.add(next_island)
                    queue.append(next_island)
        if previous_island[goal] is None:
            self.play_sound_until_done("buzzer")
        else:
            route = [goal]
            island = goal
            while previous_island[island] is not None:
                island = previous_island[island]
                route.insert(0, island)
            print(route)
            State.route = route
            pytch.broadcast("show-route")


class Island(pytch.Sprite):
    Costumes = [
        f"circle-{colour}-{number}.png"
        for colour in "ABCD"
        for number in [1, 2, 3, 4]
    ]
    Sounds = ["pop.mp3"]
    start_shown = False

    @pytch.when_I_receive("arrange-islands")
    def arrange_islands(self):
        for idx, kind in enumerate(State.island_order):
            self.idx = idx
            self.kind = kind
            pytch.create_clone_of(self)

    @pytch.when_I_start_as_a_clone
    def go_to_position(self):
        x, y = coords_of_index(self.idx)
        self.go_to_xy(x, y)
        self.switch_costume(f"circle-{self.kind[0]}-{self.kind[1]}")
        self.show()

    @pytch.when_this_sprite_clicked
    def note_click(self):
        n_already_clicked = len(State.islands_clicked)

        self.start_sound("pop")
        if n_already_clicked == 0:
            print("start", self.idx, self.kind)
            State.islands_clicked.append(self.idx)
            pytch.broadcast_and_wait("highlight-start")
        elif n_already_clicked == 1:
            print("goal", self.idx, self.kind)
            State.islands_clicked.append(self.idx)
            pytch.broadcast_and_wait("highlight-end")
            pytch.broadcast("find-route")
        elif n_already_clicked == 2:
            pytch.broadcast_and_wait("reset-highlights")
            State.islands_clicked.pop(0)
            pytch.broadcast_and_wait("highlight-start")
            State.islands_clicked.append(self.idx)
            pytch.broadcast_and_wait("highlight-end")
            pytch.broadcast("find-route")


class Highlight(pytch.Sprite):
    Costumes = ["light-highlight.png", "dark-highlight.png"]
    Sounds = ["whoosh-slow.mp3"]
    start_shown = False

    def highlight(self, position_idx, costume_tag):
        x, y = coords_of_index(position_idx)
        self.go_to_xy(x, y)
        self.switch_costume(f"{costume_tag}-highlight")
        self.show()

    @pytch.when_I_receive("highlight-start")
    def highlight_start(self):
        self.is_start = True
        self.highlight(State.islands_clicked[0], "light")

    @pytch.when_I_receive("highlight-end")
    def make_end_highlight(self):
        pytch.create_clone_of(self)

    @pytch.when_I_start_as_a_clone
    def hightlight_end(self):
        self.is_start = False
        self.highlight(State.islands_clicked[1], "dark")

    @pytch.when_I_receive("show-route")
    def show_route(self):
        if not self.is_start:
            return
        for idx in State.route[1:]:
            self.start_sound("whoosh-slow")
            x, y = coords_of_index(idx)
            self.glide_to_xy(x, y, 0.6, "ease-in-out")
            pytch.wait_seconds(0.15)

    @pytch.when_I_receive("reset-highlights")
    def reset_highlights(self):
        self.hide()
        self.delete_this_clone()


# Sound credits:
#
# buzzer.mp3
#   https://freesound.org/people/Breviceps/sounds/493163/
#   Here we use just the first section
#   Used under CC0 (public domain)
#
# whoosh-slow.mp3
#   https://freesound.org/people/qubodup/sounds/60013/
#   Modified by slowing down and inserting leading silence
#   Used under CC0 (public domain)
#
# pop.mp3
#   https://freesound.org/people/Vilkas_Sound/sounds/463388/
#   By freesound user "Vilkas_Sound"
#   Used under CC-BY-3.0 (https://creativecommons.org/licenses/by/3.0/)
