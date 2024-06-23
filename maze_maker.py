import pygame as p
from typing import List, Tuple
from random import choice


class Node:
    def __init__(self, pos: Tuple[int, int], edge_len: int) -> None:
        self.pos = pos
        self.coords = p.Vector2(x=pos[1]*edge_len, y=pos[0]*edge_len)
        self.inbound: List[int] = [0, 0, 0, 0]  # lrtb
        self.outbound: str = 'none'

    def draw_node(self, s, edge_len: int) -> None:
        if not self.inbound[0] and self.outbound != 'left':
            p.draw.line(s, "white", self.coords, self.coords + (0, edge_len))
        if not self.inbound[1] and self.outbound != 'right':
            p.draw.line(s, "white", self.coords + (edge_len, 0),
                        self.coords + (edge_len, edge_len))
        if not self.inbound[2] and self.outbound != 'top':
            p.draw.line(s, "white", self.coords, self.coords + (edge_len, 0))
        if not self.inbound[3] and self.outbound != 'bottom':
            p.draw.line(s, "white", self.coords + (0, edge_len),
                        self.coords + (edge_len, edge_len))

    def p(self) -> None:
        print(self.pos)
        print("in: ", self.inbound)
        print("out: ", self.outbound)


def setup(grid_size: int, edge_len: int) -> None:
    node_grid: List[List[Node]] = [
        [Node((column, row), edge_len) for row in range(grid_size)] for column in range(grid_size)]

    for row, node_row in enumerate(node_grid):
        for column, node in enumerate(node_row):
            if column == grid_size - 1:  # last column
                if row != grid_size - 1:
                    node.outbound = 'bottom'
                if row == 0:  # lrtb
                    node.inbound = [1, 0, 0, 0]  # only left
                else:
                    node.inbound = [1, 0, 1, 0]  # left and top
                continue
            node.outbound = 'right'
            if column != 0:  # not first column
                node.inbound = [1, 0, 0, 0]
    return node_grid


def change_root(node_grid: List[List[Node]], root_pos: Tuple[int, int], grid_size: int) -> Tuple[str, int, int]:

    direction_dict = {'left': 0, 'right': 1, 'top': 2, 'bottom': 3}
    direction_dict2 = {'left': 1, 'right': 0, 'top': 3, 'bottom': 2}

    curr_root = node_grid[root_pos[1]][root_pos[0]]

    x, y = root_pos
    direction_str = ''
    direction = choice(['x', 'y'])
    magnitude = choice([-1, 1])
    if direction == 'x':
        x += magnitude
    else:
        y += magnitude
    if 0 <= x < grid_size and 0 <= y < grid_size:
        if direction == 'x':
            if magnitude == -1:
                direction_str = 'left'
            else:
                direction_str = 'right'
        else:
            if magnitude == 1:
                direction_str = 'bottom'
            else:
                direction_str = 'top'
        curr_root.outbound = direction_str
        curr_root.inbound[direction_dict[direction_str]] = 0
        new_root = node_grid[y][x]
        new_root.inbound[direction_dict2[direction_str]] = 1
        new_root.outbound = ''
        return (x, y)
    else:
        return change_root(node_grid, root_pos, grid_size)


def draw_grid(s: p.Surface, node_grid: List[List[Node]], edge_len: int) -> None:
    s.fill('black')
    for list in node_grid:
        for node in list:
            node.draw_node(s, edge_len)
            # node.p()


def main():
    p.init()
    clock = p.time.Clock()
    fps = 3
    initial_itarations = 5000

    height, width = 800, 800

    # square grid
    grid_size = 20
    edge_len = 700 // grid_size  # make it '/' if need a lot more grid_size

    w = p.display.set_mode((height, width))
    s = p.Surface((701, 701))

    node_grid: List[List[Node]] = setup(grid_size, edge_len)
    root_pos = (grid_size - 1, grid_size - 1)

    me = (0, 0)
    # p.draw.circle(
    #         w, 'red',
    #         (root_pos[0]*edge_len + edge_len*.5 + 50,
    #          root_pos[1]*edge_len + edge_len*.5 + 50),
    #         5)# use for me_pos
    while initial_itarations:
        root_pos = change_root(node_grid, root_pos, grid_size)
        initial_itarations -= 1
    while True:
        clock.tick(fps)
        w.fill('black')

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit
                exit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    p.quit()
                    exit()

        root_pos = change_root(node_grid, root_pos, grid_size)

        draw_grid(s, node_grid, edge_len)
        w.blit(s, (50, 50))
        p.draw.circle(
            w, 'red',
            (root_pos[0]*edge_len + edge_len*.5 + 50,
                root_pos[1]*edge_len + edge_len*.5 + 50),
            5)
        p.display.flip()


if __name__ == '__main__':
    main()
