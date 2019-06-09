#create a maze solver first following bookmark then try and do the puzzle one
import time


import breadth_first_search
#add display of vertices and then show puzzle solving using vertices


class Maze(object):

    def __init__(self):
        self.game_over = False
        self.prev_dir = 'None'#keep track of last direction
        self.vertex_dict = {0:{'adj_dir':[]}} # format 'Vertex Label' : set([adjacent vertex list]) # 1 : [2,3]
        self.next_vertex_label = 0 #used to increment vertex label count
        self.current_vertex_label = 0 #keep track of which path you are on
        self.prev_vertex_label = 0
        self.final_graph = {}

        self.load_maze()
        self.find_start()

    def load_maze(self):
        # with open('maze_layout.txt', 'r') as maze_read:
        # with open('maze_layout_no_alt_path.txt', 'r') as maze_read:
        # with open('maze_layout_complex.txt', 'r') as maze_read:
        with open('maze_layout_more_complex.txt', 'r') as maze_read:
        # with open('maze_layout_another_complex.txt', 'r') as maze_read:
        # with open('maze_layout_last_complex.txt', 'r') as maze_read:
            maze_in = maze_read.read().splitlines()
        #get board dimensions
        self.v_size = len(maze_in)
        self.h_size = len(maze_in[0])
        self.main_maze = []
        for line in maze_in:
            self.main_maze.append(list(line))
        self.build_blank_found()

    def build_blank_found(self):
        self.found_dict = {}
        for v in range(self.v_size):
            self.found_dict[v] = {}
            for h in range(self.h_size):
                self.found_dict[v][h] = {'found':['']}
        #print("Build Test:{}".format(self.found_dict[0][0]))

    def find_start(self):
        for v in range(self.v_size):
            for h in range(self.h_size):
                if self.main_maze[v][h] == 'S':
                    self.start_v = v
                    self.start_h = h
        #update vertex_dict
        self.vertex_dict[0]['coord_v'] = self.start_v
        self.vertex_dict[0]['coord_h'] = self.start_h
        #print("Starting coordinates:{},{}".format(self.start_v,self.start_h))

    def print_maze(self):
        for v in range(self.v_size):
            for h in range(self.h_size):
                print(self.main_maze[v][h],end="")
            print("")

    def game_play(self):
        start = time.time()
        self.solve_maze(self.start_v, self.start_h)
        self.print_maze()
        end = time.time()
        ms_time = round(((end-start) * 1000),4)
        print("Game over, maze completed!\nTime for completion: {} ms".format(ms_time))
        print("Searching for optimal path")
        self.build_final_graph()
        print(self.final_graph)
        self.solution_list = list(breadth_first_search.dfs_paths(self.final_graph, 0, self.current_vertex_label))
        print("Solution list: {}".format(self.solution_list))

    #check to see what we need to do with vertex_dict
    def check_vertex(self, v_search, h_search):

        #check to see if vertex is already at this location
        for vertex in self.vertex_dict.keys():
            if self.vertex_dict[vertex]['coord_v'] == v_search and self.vertex_dict[vertex]['coord_h'] == h_search:
                print("This vertex ({}) already exists\nResetting current vertex label.\nLeaving function.".format(vertex))
                self.current_vertex_label = vertex
                return

        print("Leaving for loop, didn't find an existing vertex here. Need to add a new one")

        #Adding new vertex to dict
        self.next_vertex_label += 1
        #Adding new vertex to adj_dir of last vertex
        self.vertex_dict[self.current_vertex_label]['adj_dir'].append(self.next_vertex_label)
        self.current_vertex_label = self.next_vertex_label
        self.vertex_dict[self.next_vertex_label] = {'adj_dir': [], 'coord_v': v_search, 'coord_h': h_search}


    def build_final_graph(self):
        for vertex in self.vertex_dict.keys():
            self.final_graph[vertex] = set(self.vertex_dict[vertex]['adj_dir'])



    def solve_maze(self, v_search, h_search):
        if self.main_maze[v_search][h_search] != 'S':
            self.main_maze[v_search][h_search] = 'O'
        self.print_maze()
        print("Current vertex list: {}\nCurrently at v: {}, h: {}\nCurrent vertex label: {}".format(self.vertex_dict, v_search, h_search, self.current_vertex_label))

        input("Next Step?\n>")
        #add vertex to set
        # self.next_vertex_label += 1
        # self.vertex_dict[0].add(self.next_vertex_label)
        while not self.game_over:
            #print("Game Over: {}".format(self.game_over))
            move_found = False #Use this to see when you don't have a move available and need to go back
            #had to add game over checks to each direction
            if not self.game_over:
                #Check down, wall always at least one space away
                if v_search < self.v_size-2:
                    #if space below is empty and hasn't been visited in that direction
                    if self.main_maze[v_search+1][h_search] == ' ' and 'Down' not in self.found_dict[v_search][h_search]['found']:
                        print("Opening found below")
                        if self.prev_dir != 'Down':
                            print("New vertex found Down")
                            self.prev_dir = 'Down'
                            self.check_vertex(v_search, h_search)
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Down')
                        #change icon to direction if not the start piece
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = 'v'

                        self.solve_maze(v_search+1,h_search)

                    #if you find exit set game_over = True
                    elif self.main_maze[v_search+1][h_search] == 'E':
                        print("Found Exit below")
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Down')
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = 'v'
                        self.game_over = True

            if not self.game_over:
                #up, 1 because 0 will always be a wall
                if v_search > 1:
                    #If space above is empty and hasn't been visited
                    if self.main_maze[v_search-1][h_search] == ' ' and 'Up' not in self.found_dict[v_search][h_search]['found']:
                        print("Opening found above")
                        if self.prev_dir != 'Up':
                            print("New vertex found Up")
                            self.prev_dir = 'Up'
                            self.check_vertex(v_search, h_search)
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Up')
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '^'
                        self.solve_maze(v_search-1,h_search)

                    #if you find exit set game_over = True
                    elif self.main_maze[v_search-1][h_search] == 'E':
                        print("Found Exit Above")
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Up')
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '^'
                        self.game_over = True
                        return


            if not self.game_over:
                #right
                if h_search < self.h_size-2:
                    #if space to right is open and hasn't been visited yet
                    if self.main_maze[v_search][h_search+1] == ' ' and 'Right' not in self.found_dict[v_search][h_search]['found']:
                        print("Opening found to the right")
                        if self.prev_dir != 'Right':
                            print("New vertex found Right")
                            self.prev_dir = 'Right'
                            self.check_vertex(v_search, h_search)
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Right')
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '>'
                        self.solve_maze(v_search,h_search+1)

                    #if you find exit set game_over = True
                    elif self.main_maze[v_search][h_search+1] == 'E':
                        print("Found Exit right")
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Right')
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '>'
                        self.game_over = True

            if not self.game_over:
                #left
                if h_search > 1:
                    #if space to left is open and hasn't been visited yet
                    if self.main_maze[v_search][h_search-1] == ' ' and 'Left' not in self.found_dict[v_search][h_search]['found']:
                        print("Opening found to the left")
                        if self.prev_dir != 'Left':
                            print("New vertex found Left")
                            self.prev_dir = 'Left'
                            self.check_vertex(v_search, h_search)
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Left')
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '<'
                        self.solve_maze(v_search,h_search-1)

                    #if you find exit set game_over = True
                    elif self.main_maze[v_search][h_search-1] == 'E':
                        print("Found Exit left")
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Left')
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '<'
                        self.game_over = True



            if not move_found:
                move_found = False
                print("Move not found")
                self.main_maze[v_search][h_search] = 'X'

                #reset found for this block
                self.found_dict[v_search][h_search]['found'] = ['']
                self.print_maze()
                input("Next step(Move not found)?\n>")

                #go back to previous piece and search a direction that wasn't found already or continue going back
                return

            #not sure if this is needed
            if self.game_over:
                break


if __name__ == '__main__':
    m = Maze()
    #m.print_maze()
    m.game_play()
