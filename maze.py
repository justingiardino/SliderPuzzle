#create a maze solver first following bookmark then try and do the puzzle one
import time
import platform

#enable ANSI escape codes on windows
if platform.system() == 'Windows':
    import colorama
    colorama.init()

import breadth_first_search
#add display of vertices and then show puzzle solving using vertices


class Maze(object):

    def __init__(self):


        self.debug_mode = 0
        while self.debug_mode != 1 and self.debug_mode != 2:
            self.debug_mode = int(input("Do you want debug mode on?\n1) Yes\n2) No\n>"))

        if platform.system() == 'Windows':
            self.color_dict = {'0':'\033[0m', '1':'\033[0;31m','2':'\033[0;32m','3':'\033[0;37m','4':'\033[0;36m','5':'\033[1;33m','6':'\033[0;35m'}#,'f':'\033[0;37m','g':'\033[1;34m','h':'\033[1;32m','i':'\033[1;36m','j':'\033[1;35m'}
        else:
            self.color_dict = {'0':'\033[0m', '1':'\033[0;31m','2':'\033[0;34m','3':'\033[0;37m','4':'\033[0;36m','5':'\033[1;33m','6':'\033[0;35m'}#,'f':'\033[0;37m','g':'\033[1;34m','h':'\033[1;32m','i':'\033[1;36m','j':'\033[1;35m'}



        self.game_over = False
        self.prev_dir = 'None'#keep track of last direction
        self.vertex_dict = {0:{'adj_dir':{}}} # format 'Vertex Label' : set([adjacent vertex list]) # 1 : [2,3], changing to 'Label' : {vertex1:direction1, vertex2:direction2}
        self.next_vertex_label = 0 #used to increment vertex label count
        self.current_vertex_label = 0 #keep track of which path you are on
        self.prev_vertex_label = 0
        self.final_graph = {}
        self.main_maze = []
        self.vertex_maze = []

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

        for line in maze_in:
            self.main_maze.append(list(line))
            self.vertex_maze.append(list(line))
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

    def build_vertex_graph(self):
        for vertex in self.vertex_dict.keys():
            v = self.vertex_dict[vertex]['coord_v']
            h = self.vertex_dict[vertex]['coord_h']
            self.vertex_maze[v][h] = vertex

    #going to change color of value if the number is greater than 10
    def print_vertex_maze(self):

        str_list = ['#', 'S', ' ', 'E']
        for v in range(self.v_size):
            for h in range(self.h_size):
                curr_val = self.vertex_maze[v][h]
                if curr_val in str_list:
                    print(curr_val,end="")
                else:
                    #number less than 10, print it normally
                    print_info = int(curr_val) / 10
                    #print("Print info: {}".format(print_info))
                    color, vert_number = str(print_info).split('.')
                    print("{}{}\033[0m".format(self.color_dict[color], vert_number),end="")
                    #else number is greate

            print("")


    def game_play(self):
        start = time.time()
        self.solve_maze(self.start_v, self.start_h)
        self.print_maze()
        end = time.time()
        ms_time = round(((end-start) * 1000),4)
        print("Game over, maze completed!\nTime for completion: {} ms".format(ms_time))
        print("Current vertex_dict: {}".format(self.vertex_dict))
        # self.build_vertex_graph()
        # self.print_vertex_maze()
        # self.build_final_graph()
        self.solve_path()


    def solve_path(self):

        print("Adding vertex labels to graph")
        #Need to call build vertex graph before building final graph
        self.build_vertex_graph()
        self.print_vertex_maze()
        print("Searching for optimal path")
        self.build_final_graph()
        print(self.final_graph)
        self.solution_list = list(breadth_first_search.dfs_paths(self.final_graph, 0, self.current_vertex_label))[0]#get rid of unecessary double list
        print("Solution list: {}".format(self.solution_list))
        print("Tens value and color it will be\n" + "-"*25)
        for temp_color in self.color_dict.keys():
            print(" "*5 + "{}{}0\'s\033[0m".format(self.color_dict[temp_color], temp_color))
        print("Printing vertex maze")
        self.print_vertex_maze()

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
        #Redoing logic on adj_dir
        # self.vertex_dict[self.current_vertex_label]['adj_dir'].append(self.next_vertex_label)
        self.current_vertex_label = self.next_vertex_label
        self.vertex_dict[self.next_vertex_label] = {'adj_dir': {}, 'coord_v': v_search, 'coord_h': h_search}

    #in this function, should I keep track of what directino Im moving in? - Will help for printing solution
    #self.vert_direction = {'vertex_start':{'vertex_end1':'direction1', 'vertex_end2':'direction2'}}
    #start here ^
    def build_adj_dir(self, vertex):
        curr_v = self.vertex_dict[vertex]['coord_v']
        curr_h = self.vertex_dict[vertex]['coord_h']
        #current vertex should always be more than the previous vertex - hopefully
        #check vertical direction to see if there is another direction
        #up
        for v_offset in range(1,self.v_size):
            #If we are not at boundary
            if curr_v - v_offset > 0:
                current_maze_val = self.vertex_maze[curr_v - v_offset][curr_h]
                #need to eventually replace E with a vertex label
                if current_maze_val == '#' or current_maze_val == 'E' or current_maze_val == 'S':
                    print("Found wall when searching for piece: {} in direction: {}".format(vertex, 'Up'))
                    break

                elif current_maze_val != ' ':
                    print("Found vertex: {} when searching for piece: {} in direction: {}".format(current_maze_val, vertex, 'Up'))
                    #if the current maze val is greater than the current vertex, want to mark this in forward path
                    if int(vertex) < int(current_maze_val):
                        print("Adding to adj_dir list")
                        self.vertex_dict[vertex]['adj_dir'][current_maze_val] = 'Up'
                    else:
                        print("Not adding to adj_dir")
                    break
                #else nothing

        #down
        for v_offset in range(1,self.v_size):
            #If we are not at boundary
            if curr_v + v_offset < self.v_size:
                current_maze_val = self.vertex_maze[curr_v + v_offset][curr_h]
                #need to eventually replace E with a vertex label
                if current_maze_val == '#' or current_maze_val == 'E':
                    print("Found wall when searching for piece: {} in direction: {}".format(vertex, 'Down'))
                    break

                elif current_maze_val != ' ':
                    print("Found vertex: {} when searching for piece: {} in direction: {}".format(current_maze_val, vertex, 'Down'))
                    #if the current maze val is greater than the current vertex, want to mark this in forward path
                    if int(vertex) < int(current_maze_val):
                        print("Adding to adj_dir list")
                        self.vertex_dict[vertex]['adj_dir'][current_maze_val] = 'Down'
                    else:
                        print("Not adding to adj_dir")
                    break

        #horizontal
        #left
        for h_offset in range(1,self.h_size):
            #If we are not at boundary
            if curr_h - h_offset > 0:
                current_maze_val = self.vertex_maze[curr_v][curr_h - h_offset]
                #need to eventually replace E with a vertex label
                if current_maze_val == '#' or current_maze_val == 'E':
                    print("Found wall when searching for piece: {} in direction: {}".format(vertex, 'Left'))
                    break

                elif current_maze_val != ' ':
                    print("Found vertex: {} when searching for piece: {} in direction: {}".format(current_maze_val, vertex, 'Left'))
                    #if the current maze val is greater than the current vertex, want to mark this in forward path
                    if int(vertex) < int(current_maze_val):
                        print("Adding to adj_dir list")
                        self.vertex_dict[vertex]['adj_dir'][current_maze_val] = 'Left'
                    else:
                        print("Not adding to adj_dir")
                    break

        #right
        for h_offset in range(1,self.h_size):
            #If we are not at boundary
            if curr_h + h_offset < self.h_size:
                current_maze_val = self.vertex_maze[curr_v][curr_h + h_offset]
                #need to eventually replace E with a vertex label
                if current_maze_val == '#' or current_maze_val == 'E':
                    print("Found wall when searching for piece: {} in direction: {}".format(vertex, 'Right'))
                    break

                elif current_maze_val != ' ':
                    print("Found vertex: {} when searching for piece: {} in direction: {}".format(current_maze_val, vertex, 'Right'))
                    #if the current maze val is greater than the current vertex, want to mark this in forward path
                    if int(vertex) < int(current_maze_val):
                        print("Adding to adj_dir list")
                        self.vertex_dict[vertex]['adj_dir'][current_maze_val] = 'Right'
                    else:
                        print("Not adding to adj_dir")
                    break




    def build_final_graph(self):
        for vertex in self.vertex_dict.keys():
            self.build_adj_dir(vertex)
            #want to only take the vertices here, not the direction moving - only want the keys
            print("Current adjacent directions for vertex: {}: {}".format(vertex, self.vertex_dict[vertex]['adj_dir']))
            self.final_graph[vertex] = set(self.vertex_dict[vertex]['adj_dir'].keys())
        print(self.final_graph)



    def solve_maze(self, v_search, h_search):
        if self.main_maze[v_search][h_search] != 'S':
            self.main_maze[v_search][h_search] = 'O'
        self.print_maze()
        print("Current vertex list: {}\nCurrently at v: {}, h: {}\nCurrent vertex label: {}".format(self.vertex_dict, v_search, h_search, self.current_vertex_label))
        if self.debug_mode == 1:
            input("Next Step?\n>")
        else:
            print("Next Step?\n>")
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
                        if self.prev_dir != 'Down':
                            print("New vertex found Down")
                            self.prev_dir = 'Down'
                            self.check_vertex(v_search, h_search)
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
                        if self.prev_dir != 'Up':
                            print("New vertex found Up")
                            self.prev_dir = 'Up'
                            self.check_vertex(v_search, h_search)
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
                        if self.prev_dir != 'Right':
                            print("New vertex found Right")
                            self.prev_dir = 'Right'
                            self.check_vertex(v_search, h_search)
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
                        if self.prev_dir != 'Left':
                            print("New vertex found Left")
                            self.prev_dir = 'Left'
                            self.check_vertex(v_search, h_search)
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
                if self.debug_mode == 1:
                    input("Next step(Move not found)?\n>")
                else:
                    print("Next step(Move not found)?\n>")

                #go back to previous piece and search a direction that wasn't found already or continue going back
                return

            #not sure if this is needed
            if self.game_over:
                break


if __name__ == '__main__':
    m = Maze()
    #m.print_maze()
    m.game_play()
