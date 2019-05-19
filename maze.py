#create a maze solver first following bookmark then try and do the puzzle one


#need to keep a dictionary of visited spaces
#found_dict[v][h]['found'] = 'Left'
class Maze(object):

    def __init__(self):
        self.load_maze()
        self.find_start()
        self.game_over = False


    def load_maze(self):

        #with open('maze_layout.txt', 'r') as maze_read:
        #with open('maze_layout_no_alt_path.txt', 'r') as maze_read:
        # with open('maze_layout_complex.txt', 'r') as maze_read:
        with open('maze_layout_more_complex.txt', 'r') as maze_read:
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

        print("Starting coordinates:{},{}".format(self.start_v,self.start_h))

    def print_maze(self):
        for v in range(self.v_size):
            for h in range(self.h_size):
                print(self.main_maze[v][h],end="")
            print("")

    def game_play(self):

        self.solve_maze(self.start_v, self.start_h)
        self.print_maze()

        #direction arrow not resetting when changing direction

    def solve_maze(self, v_search, h_search):

        self.print_maze()
        input("Next Step?\n>")
        #print(self.found_dict)
        #game_over is True when you hit E

        if self.game_over:
            print("Leave")
            #exit

        while not self.game_over:
            print("Game Over: {}".format(self.game_over))
            move_found = False #Use this to see when you don't have a move available and need to go back
            #had to add game over checks to each direction
            if not self.game_over:
                #Check down, wall always at least one space away
                if v_search < self.v_size-2:
                    #if space below is empty and hasn't been visited in that direction
                    if self.main_maze[v_search+1][h_search] == ' ' and 'Down' not in self.found_dict[v_search][h_search]['found']:
                        print("Opening found below")
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Down')
                        self.main_maze[v_search+1][h_search] = 'O'
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = 'v'
                        self.solve_maze(v_search+1,h_search)

                    #if you find exit break the while loop
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
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Up')
                        self.main_maze[v_search-1][h_search] = 'O'
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '^'
                        self.solve_maze(v_search-1,h_search)

                    #if you find exit break the while loop
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
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Right')
                        self.main_maze[v_search][h_search+1] = 'O'
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '>'
                        self.solve_maze(v_search,h_search+1)

                    #if you find exit break the while loop
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
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Left')
                        self.main_maze[v_search][h_search-1] = 'O'
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '<'
                        self.solve_maze(v_search,h_search-1)

                    elif self.main_maze[v_search][h_search-1] == 'E':
                        print("Found Exit left")
                        move_found = True
                        self.found_dict[v_search][h_search]['found'].append('Left')
                        #change icon to direction
                        if self.main_maze[v_search][h_search] != 'S':
                            self.main_maze[v_search][h_search] = '<'
                        self.game_over = True



            if not move_found:
                #print("No move found")
                move_found = False
                input("Next step(Move not found)?\n>")
                self.main_maze[v_search][h_search] = 'X'
                #reset found for this block
                self.found_dict[v_search][h_search]['found'] = ['']
                self.print_maze()
                #go back to previous piece and search a direction that wasn't found already or continue going back
                return
            if self.game_over:
                break








if __name__ == '__main__':
    m = Maze()
    m.print_maze()
    m.game_play()
