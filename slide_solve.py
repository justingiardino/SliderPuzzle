'''
Black       0;30     Dark Gray     1;30
Blue        0;34x     Light Blue    1;34x
Green       0;32x     Light Green   1;32x
Cyan        0;36x     Light Cyan    1;36x
Red         0;31x     Light Red     1;31x
Purple      0;35x     Light Purple  1;35x
Brown       0;33     Yellow        1;33x
Light Gray  0;37x     White         1;37
'\033[0;31m'
'''

#need to build stats on vertices like moves available

#use this to print color
import platform
import time

#enable ANSI escape codes on windows
if platform.system() == 'Windows':
    import colorama
    colorama.init()

class Board(object):

    def __init__(self):
        #initialize variables
        # self.vertex_dict = {}
        self.num_moves_reverted = 0 #use this to add to vertex label when you have reverted a move
        self.current_vertex_label = 0
        self.piece_list = [] #keep track of all available pieces on the board
        self.piece_objects = {} #keep track of all piece objects, this is the same as the old main_board
        self.vertex_dict = {0:[]} #keep track of possible other moves, old -> "vertices" {Label1: {vertex1: {piece1:direction1}, vertex2: {piece2:direction2}}}
        self.game_over = False #when you find the exit turn back around
        self.move_count = 0
        self.forward_move_list = [] #use this to view the solution that was found
        self.board_list = [] #keep track of all the different board setups I've been in so I don't move back into a bad move
        # self.move_list = [] #used for debugging loop I'm stuck in

        print("\n\n\nWelcome to the new slide puzzle solver!\n" + "-"*39)

        self.debug_mode = 0
        valid_debug = [1,2,3,4,5]
        while self.debug_mode not in valid_debug:
            self.debug_mode = int(input("Do you want debug mode on?\n1) Yes\n2) No\n3) After first exit found\n4) After first 100 moves\n5) After first revert move\n>"))

        #set colors for pieces
        if platform.system() == 'Windows':
            self.color_dict = {'.':'\033[0m', 'x':'\033[0;31m','a':'\033[0;32m',
            'b':'\033[1;31m','c':'\033[0;36m','d':'\033[1;33m','e':'\033[0;35m',
            'f':'\033[0;37m','g':'\033[1;34m','h':'\033[1;32m','i':'\033[1;36m',
            'j':'\033[1;35m'}
        else:
            self.color_dict = {'.':'\033[0m', 'x':'\033[0;31m','a':'\033[0;34m',
            'b':'\033[1;31m','c':'\033[0;36m','d':'\033[1;33m','e':'\033[0;35m',
            'f':'\033[0;37m','g':'\033[1;34m','h':'\033[1;32m','i':'\033[1;36m',
            'j':'\033[1;35m'}

        self.load_board()

        if self.debug_mode == 1:
            self.print_piece_stats()

    def load_board(self):
        puzzle_choice = 0
        puzzle_vals = [1,2,3,4]
        while puzzle_choice not in puzzle_vals:
            puzzle_choice = int(input("Which puzzle? (1), (2), (3) or (4) \n>"))

        if puzzle_choice == 1:
            with open('Sliders/puzzle_layout.txt', 'r') as puzzle_read:
                puzzle_in = puzzle_read.read().splitlines()
        elif puzzle_choice == 2:
            with open('Sliders/puzzle_layout2.txt', 'r') as puzzle_read:
                puzzle_in = puzzle_read.read().splitlines()
        elif puzzle_choice == 3:
            with open('Sliders/puzzle_layout3.txt', 'r') as puzzle_read:
                puzzle_in = puzzle_read.read().splitlines()
        elif puzzle_choice == 4:
            with open('Sliders/puzzle_not_square.txt', 'r') as puzzle_read:
                puzzle_in = puzzle_read.read().splitlines()


        self.v_size = len(puzzle_in)
        self.h_size = len(puzzle_in[0])
        # print("Width of board: {}".format(self.h_size))
        self.show_board = [['.' for x in range(self.h_size)] for y in range(self.v_size)]#initialize show board

        #build board
        start_pieces = {}
        for v in range(self.v_size):
            for h in range(self.h_size):
                #if finding for the first time, create dictionary value
                current_piece = puzzle_in[v][h]
                #only want to find letters
                if(current_piece != "."):
                    #initialize piece stats if it hasn't been added yet
                    if(current_piece not in start_pieces.keys()):
                        start_pieces[current_piece] = {'start_v':v, 'start_h':h,'length':1} #, 'init_v':v, 'init_h':h}
                        #check direction, won't be above or to the left
                        #check boundaries, make sure you aren't in the last row or column
                        if(v < self.v_size-1):
                            if(puzzle_in[v+1][h] == current_piece):
                                #update direction as v - vertical
                                start_pieces[current_piece]['direction'] = 'v'
                        if(h < self.h_size-1):
                            if(puzzle_in[v][h+1] == current_piece):
                                #update direction as h - horizontal
                                start_pieces[current_piece]['direction'] = 'h'
                    #increment length if letter has already been added
                    else:
                        start_pieces[current_piece]['length']+=1

        #build piece object
        for piece in start_pieces.keys():
            self.piece_list.append(piece)
            self.piece_objects[piece] = Piece(piece, start_pieces[piece]['length'], start_pieces[piece]['start_v'], start_pieces[piece]['start_h'], start_pieces[piece]['direction'])

        #build show_board
        for piece in self.piece_list:
            #if horizontal
            if self.piece_objects[piece].direction == 'h':
                for i in range(self.piece_objects[piece].length):
                    self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h+i] = piece
            #vertical
            else:
                for i in range(self.piece_objects[piece].length):
                    self.show_board[self.piece_objects[piece].start_v+i][self.piece_objects[piece].start_h] = piece
        if self.debug_mode == 1:
            input("Show board: \n{}\n".format(self.show_board))
        else:
            print("Show board: \n{}\n".format(self.show_board))



    #utility function for viewing piece info
    def print_piece_stats(self):
        for piece in self.piece_list:
            print("Piece:{}, Length:{}, Start_v:{}, Start_h:{}, Direction:{}".format(piece,self.piece_objects[piece].length,self.piece_objects[piece].start_v,self.piece_objects[piece].start_h,self.piece_objects[piece].direction))

    #modified for changing board size
    def print_board(self):

        #top row
        print("   ",end='')
        for row in range(self.h_size):
            print("{} ".format(row),end='')
        print("\n :" + "="*(2*self.h_size) +"=:",end='')

        for v in range(self.v_size):
            print("\n{}| ".format(v),end='')
            for h in range(self.h_size):
                curr_piece = self.show_board[v][h]
                print("{}{}\033[0m ".format(self.color_dict[curr_piece],curr_piece),end='')
            #skip the exit wall
            if v != self.piece_objects['x'].start_v:
                print("|",end='')
        #bottom row
        print("\n :" + "="*(2*self.h_size) +"=:")

    #return a list of all available moves in format of {'piece': 'x', 'direction': 'None'}
    def check_moves(self, prev_piece, prev_dir):
        move_list = []
        for piece in self.piece_list:
            if self.piece_objects[piece].direction == 'v':
                #check up, upperbound
                if self.piece_objects[piece].start_v > 0:
                    #store for easier reading
                    current_letter = self.show_board[self.piece_objects[piece].start_v-1][self.piece_objects[piece].start_h]
                    if current_letter == '.':
                        #don't want to just undo last move - had to change these to or but not sure if that's what I really want
                        if prev_piece != piece or prev_dir != 'Down':
                            move_list.append({'piece': piece, 'direction': 'Up'})
                #check lower bound
                if (self.piece_objects[piece].start_v + self.piece_objects[piece].length) < self.v_size:
                    #store for easier reading
                    current_letter = self.show_board[self.piece_objects[piece].start_v+ self.piece_objects[piece].length][self.piece_objects[piece].start_h]
                    if current_letter == '.':
                        #don't want to just undo last move
                        if (prev_piece != piece or prev_dir != 'Up'):
                            move_list.append({'piece': piece, 'direction': 'Down'})
            #check horizontal
            else:
                #check left
                if self.piece_objects[piece].start_h > 0:
                    #store for easier reading
                    current_letter = self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h-1]
                    if current_letter == '.':
                        #don't want to just undo last move
                        if (prev_piece != piece or prev_dir != 'Right'):
                            move_list.append({'piece': piece, 'direction': 'Left'})
                #check right
                if (self.piece_objects[piece].start_h + self.piece_objects[piece].length) < self.h_size:
                    #store for easier reading
                    current_letter = self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h + self.piece_objects[piece].length]
                    if current_letter == '.':
                        #don't want to just undo last move
                        if (prev_piece != piece or prev_dir != 'Left'):
                            move_list.append({'piece': piece, 'direction': 'Right'})
        return move_list


    #main function
    def launch_solver(self):
        print("Starting to solve puzzle")
        # self.update_board_list()
        self.print_board()
        start = time.time()
        # temp_list = self.show_board.copy()
        # self.board_list.append(temp_list)
        #self.update_board_list()
        #passing none since x hasn't moved yet
        #calling this to add first show board to board list
        self.get_temp_board('x','None',self.show_board)
        self.solve_puzzle({'piece': 'x', 'direction':'None', 'vertex_label':0})
        #self.solve_maze_old(self.start_v, self.start_h)
        #self.print_maze()
        end = time.time()
        ms_time = round(((end-start) * 1000),4)
        print("Game over, Puzzle solved!\nTime for completion: {} ms.".format(ms_time))
        self.print_board_list()
        print("Vertex dict")
        for curr_vertex in self.vertex_dict.keys():
            print("Vertex: {}, Adjacencies: {}".format(curr_vertex, self.vertex_dict[curr_vertex]))

    def check_game_over(self):
        print("Checking for game over..")
        # self.print_piece_stats()
        if self.piece_objects['x'].start_h == self.h_size - 2:
            # print("Game over!")
            return True
        else:
            return False

    #main recursive function
    #curr_move should be a dict with the last move = {piece: 'x', direction: 'Right', vertex_label; 0}
    #instead of curr_move I'm going to have to save the state of the board so I don't do a duplicate move
    def solve_puzzle(self, curr_move):
        # self.print_board()
        print("All of curr_move: {}".format(curr_move))
        print("Called recursion, last piece moved: {}".format(curr_move['piece']))
        print("Current forward_move_list: {}\nLength: {}".format(self.forward_move_list, len(self.forward_move_list)))

        # print("Current forward_move_list: {}\nLength: {}".format(self.forward_move_list, len(self.forward_move_list)))
        #print("Current move list: {}".format(self.move_list))
        if self.debug_mode == 1:
            input("Continue?\n>")
        else:
            print("Continue?\n>")

        #need to check all available moves
        found_moves = self.check_moves(curr_move['piece'], curr_move['direction'])
        print("Available moves: {}".format(found_moves))

        #if you end up trying a different direction, then you either didn't move forward, or you moved forward and then moved back, so I should check for bad moves before the loop
        #continue to try moving all directions until there are no more to try
        while found_moves:
            self.current_vertex_label = curr_move['vertex_label']
            try_move = found_moves.pop()

            print("At top of found moves loop for last piece: {} direction: {}\nCurrent vertex label: {}\nRemaining moves: {}".format(curr_move['piece'], curr_move['direction'], curr_move['vertex_label'], found_moves))
            # print("Current forward_move_list: {}\nLength: {}".format(self.forward_move_list, len(self.forward_move_list)))
            #build new vertex here
            print("Current vertex dict: {}".format(self.vertex_dict))
            if self.debug_mode == 1:
                input("Going to try moving piece: {} in direction: {}\n>".format(try_move['piece'], try_move['direction']))
            else:
                print("Going to try moving piece: {} in direction: {}\n>".format(try_move['piece'], try_move['direction']))

            #move the piece
            if(self.move_piece(try_move['piece'], try_move['direction'])):
                # self.board_list.append(self.show_board)

                # self.move_list.append(curr_move)
                self.print_board()
                # print("Current show board: \n{}".format(self.show_board))
                # temp_list = self.show_board.copy()
                # self.board_list.append(temp_list)
                # self.update_board_list()
                # self.get_temp_board('x','None')
                print("Just moved: {}".format(try_move))
                if self.check_game_over() == True:
                    # print("Game over!!")
                    if self.debug_mode == 3:
                        print("Resetting debug mode to 1")
                        self.debug_mode = 1

                    print("Remaining found moves: {}\n\n".format(found_moves))
                    print("-*-"*22 + "\nCurrent forward move list: {}\n\nNumber of moves tried: {}".format(self.forward_move_list, len(self.forward_move_list)))
                    self.print_board()
                    print("Current vertex label: {}\nCurrent vertex dict: {}".format(self.current_vertex_label,self.vertex_dict))
                    if self.debug_mode == 1:

                        input("Exit found! Undoing move to check for other directions\n>")
                    else:
                        print("Exit found! Undoing move to check for other directions\n>")

                    #still need to create a dictionary value at this point
                    #but it should be just a vertex and an empty list
                    #create an list of vertexes where exit is at
                    #  START HERE

                    self.revert_move(try_move['piece'], try_move['direction'])
                    self.print_board()
                    if self.debug_mode == 1:
                        input("Continue?\n>")
                    else:
                        print("Continue?\n>")
                else:
                    # print("Current board list: {}".format(self.board_list))
                    if self.debug_mode == 1:
                        input("Next Step?\n>")
                    else:
                        print("Next Step?\n>")

                    print("Calling recursive function on this new piece")
                    self.solve_puzzle({'piece': try_move['piece'], 'direction': try_move['direction'], 'vertex_label':self.current_vertex_label})
            else:
                print("Move piece false on piece: {}".format(try_move['piece']))

        if self.debug_mode == 5:
            input("Resetting debug to 1\n>")
            self.debug_mode = 1
        print("No more moves found, last piece that was moved was: {} in direction: {}\nGoing back one level".format(curr_move['piece'], curr_move['direction']))
        self.print_board()
        # input("\n\n" + "-"*25 + "\nThis is where I need to undo move before going back one level\n>")
        self.revert_move(curr_move['piece'], curr_move['direction'])
        #how can I change current_vertex_label here - ?
        self.print_board()

    def check_board_in_list(self, check_board):
        print("Starting check board in list")
        #check each already added board against current
        #match_found = False
        for i, board in enumerate(self.board_list):
            curr_board_diff = False
            for v in range(self.v_size):
                if curr_board_diff == True:
                    break
                for h in range(self.h_size):
                    #if pixels don't match then this could be a valid move
                    # print("v: {}, h: {}, check_board: {}, board: {}".format(v, h, check_board[v][h], board[v][h]))
                    if check_board[v][h] != board[v][h]:
                        print("Pieces don't match, going to break")
                        curr_board_diff = True
                        break
                # print("End of h loop")
            # print("End of v loop(entire board)")
            if curr_board_diff == False:
                #match_found = True
                print("No differences found, this is a match with board: {}".format(i))
                print("Current vertex label: {}, adding to vertex dict for matching board".format(self.current_vertex_label))
                #don't creat vertex dict until you need it
                if self.current_vertex_label not in self.vertex_dict.keys():
                    self.vertex_dict[self.current_vertex_label] = []

                self.vertex_dict[self.current_vertex_label].append(i)
                print("Current vertex dict: {}".format(self.vertex_dict))

                return False
        print("End of board loop(all boards)")
        print("No match found, this move can be added")
        return True



    #have to create a copy of the current board to avoid the pointer issue
    #checks to see if the attempted move would be a move that has already been made
    #returns boolen of a valid (not duplicate)  move or not
    def get_temp_board(self, piece, direction, curr_board):
        print("Creating temp board to check if board has already been viewed")
        temp_board = [x[:] for x in curr_board]
        #if piece is horizontal
        if self.piece_objects[piece].direction == 'h':
            v_offset_piece = self.piece_objects[piece].start_v
            h_offset_piece = self.piece_objects[piece].start_h
            v_offset_blank = self.piece_objects[piece].start_v
            h_offset_blank = self.piece_objects[piece].start_h+self.piece_objects[piece].length
        else:
            v_offset_piece = self.piece_objects[piece].start_v
            h_offset_piece = self.piece_objects[piece].start_h
            v_offset_blank = self.piece_objects[piece].start_v+self.piece_objects[piece].length
            h_offset_blank = self.piece_objects[piece].start_h


        # if self.debug_mode == 1:
        #     input("temp_board before: {}\n>".format(temp_board))
        # else:
        #     print("temp_board before: {}\n>".format(temp_board))
        valid_direction = True #getting weird issue with firs move if I don't have this
        if direction == 'Down':
            v_offset_piece = self.piece_objects[piece].start_v+self.piece_objects[piece].length
            h_offset_piece = self.piece_objects[piece].start_h
            v_offset_blank = self.piece_objects[piece].start_v
            h_offset_blank = self.piece_objects[piece].start_h

        elif direction == 'Up':
            v_offset_piece = self.piece_objects[piece].start_v-1
            h_offset_piece = self.piece_objects[piece].start_h
            v_offset_blank = self.piece_objects[piece].start_v+self.piece_objects[piece].length-1
            h_offset_blank = self.piece_objects[piece].start_h

        elif direction == 'Left':

            v_offset_piece = self.piece_objects[piece].start_v
            h_offset_piece = self.piece_objects[piece].start_h-1
            v_offset_blank = self.piece_objects[piece].start_v
            h_offset_blank = self.piece_objects[piece].start_h+self.piece_objects[piece].length -1

        elif direction == 'Right':
            v_offset_piece = self.piece_objects[piece].start_v
            h_offset_piece = self.piece_objects[piece].start_h+self.piece_objects[piece].length
            v_offset_blank = self.piece_objects[piece].start_v
            h_offset_blank = self.piece_objects[piece].start_h
        else:
            print("No valid direction passed")
            valid_direction = False

        # print("Offsets\nv_piece: {}, h_piece: {}\nv_blank: {}, h_blank: {}".format(v_offset_piece, h_offset_piece, v_offset_blank, h_offset_blank))
        if valid_direction == True:
            temp_board[v_offset_piece][h_offset_piece] = piece
            temp_board[v_offset_blank][h_offset_blank] = '.'

        if self.check_board_in_list(temp_board) == False:
            # print("This board has already been created")
            if self.debug_mode == 1:
                # input("Current board list: {}\n>".format(self.board_list))
                input("This board has already been created\n>")
            else:
                # print("Current board list: {}\n>".format(self.board_list))
                print("This board has already been created\n>")
            return False

        else:
            # print("This board has not been created, adding now")
            if self.debug_mode == 1:
                # input("Current board list: {}\n>".format(self.board_list))
                input("This board has not been created, adding now\n>")
            else:
                # print("Current board list: {}\n>".format(self.board_list))
                print("This board has not been created, adding now\n>")
            self.board_list.append(temp_board)
            if self.debug_mode == 1:
                self.debug_board_list(temp_board)
                # print("Temp board: {}\nCurrent board list: {}".format(temp_board, self.board_list))
                input(">")

            return True

    def debug_board_list(self,temp_board):
        print("Temp board:")
        for row in temp_board:
            print("\t{}".format(row))

        self.print_board_list()

    def print_board_list(self):
        print("\n\nBoard list: {}")
        for i, board in enumerate(self.board_list):
            print(i)
            for row in board:
                print("\t{}".format(row))

    #not doing any boundary checking or piece checking, just need to undo the move
    def revert_move(self, piece, direction):
        if direction == 'Up':
            print("Moving: {} back Down".format(piece))
            #set current pixel to .
            self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = '.'
            #update pixel below
            self.show_board[self.piece_objects[piece].start_v+self.piece_objects[piece].length][self.piece_objects[piece].start_h] = piece
            #update start point
            self.piece_objects[piece].start_v += 1
            #remove from forward_move_list
            self.forward_move_list.pop()


        elif direction == 'Down':
            print("Moving: {} back Up".format(piece))

            #update start point
            self.piece_objects[piece].start_v -= 1
            #set new top to current letter
            self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = piece
            #set bottom pixel to .
            self.show_board[self.piece_objects[piece].start_v+self.piece_objects[piece].length][self.piece_objects[piece].start_h] = '.'
            #remove from forward_move_list
            self.forward_move_list.pop()

        elif direction == 'Right':
            print("Moving: {} back Left".format(piece))

            #update start point
            self.piece_objects[piece].start_h -= 1
            #set new left to current letter
            self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = piece
            #set old right pixel to .
            self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h+self.piece_objects[piece].length] = '.'
            #remove from forward_move_list
            self.forward_move_list.pop()

        elif direction == 'Left':
            print("Moving: {} back Right".format(piece))

            #Set current pixel to .
            self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = '.'
            #update pixel to the right
            self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h+self.piece_objects[piece].length] = piece
            #update start point
            self.piece_objects[piece].start_h += 1
            #remove from forward_move_list
            self.forward_move_list.pop()

        else:
            print("Not good - bad move in revert move. Current piece: {}".format(piece))



    #before updating board need to make sure this move hasn't already been made
    #run this function assuming that move is valid, not doing any boundary or direction checking
    #this will not move the piece until it finds that the move has not been made
    def move_piece(self, piece, direction):
        # temp_board = [x[:] for x in self.show_board]
        # input("temp_board before: {}\n>".format(temp_board))
        if len(self.forward_move_list) + 1 > 99:
            print("This would put me over 100, shouldn't move")
            return False

        if direction == 'Down':
            print("Moving: {} Down".format(piece))
            #set current pixel to .
            if(self.get_temp_board(piece,direction, self.show_board) == True):
                print("New move")
                self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = '.'
                #update pixel below
                self.show_board[self.piece_objects[piece].start_v+self.piece_objects[piece].length][self.piece_objects[piece].start_h] = piece
                #update start point
                self.piece_objects[piece].start_v += 1
                self.forward_move_list.append({'piece':piece, 'direction':direction})
                #adding to vertex dict
                #don't creat vertex dict until you need it
                if self.current_vertex_label not in self.vertex_dict.keys():
                    self.vertex_dict[self.current_vertex_label] = []

                self.vertex_dict[self.current_vertex_label].append(len(self.forward_move_list))
                self.current_vertex_label = len(self.board_list) - 1#increment vertex label
                # self.vertex_dict[self.current_vertex_label] = []
                print("Current vertex dict: {}".format(self.vertex_dict))
                return True
            else:
                print("Not a new move, need to try a different direction")
                return False

        elif direction == 'Up':
            print("Moving: {} Up".format(piece))
            if(self.get_temp_board(piece,direction, self.show_board) == True):
                print("New move")
                #update start point
                self.piece_objects[piece].start_v -= 1
                #set new top to current letter
                self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = piece
                #set bottom pixel to .
                self.show_board[self.piece_objects[piece].start_v+self.piece_objects[piece].length][self.piece_objects[piece].start_h] = '.'
                self.forward_move_list.append({'piece':piece, 'direction':direction})
                #don't creat vertex dict until you need it
                if self.current_vertex_label not in self.vertex_dict.keys():
                    self.vertex_dict[self.current_vertex_label] = []

                self.vertex_dict[self.current_vertex_label].append(len(self.forward_move_list))
                self.current_vertex_label = len(self.board_list) - 1
                # self.vertex_dict[self.current_vertex_label] = []
                print("Current vertex dict: {}".format(self.vertex_dict))
                return True
            else:
                print("Not a new move, need to try a different direction")
                return False

        elif direction == 'Left':
            print("Moving: {} Left".format(piece))
            if(self.get_temp_board(piece,direction, self.show_board) == True):
                print("New move")
                #update start point
                self.piece_objects[piece].start_h -= 1
                #set new left to current letter
                self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = piece
                #set old right pixel to .
                self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h+self.piece_objects[piece].length] = '.'
                self.forward_move_list.append({'piece':piece, 'direction':direction})
                #don't creat vertex dict until you need it
                if self.current_vertex_label not in self.vertex_dict.keys():
                    self.vertex_dict[self.current_vertex_label] = []

                self.vertex_dict[self.current_vertex_label].append(len(self.forward_move_list))
                self.current_vertex_label = len(self.board_list) - 1
                # self.vertex_dict[self.current_vertex_label] = []
                print("Current vertex dict: {}".format(self.vertex_dict))
                return True
            else:
                print("Not a new move, need to try a different direction")
                return False

        elif direction == 'Right':
            print("Moving: {} Right".format(piece))
            if(self.get_temp_board(piece,direction, self.show_board) == True):
                print("New move")
                #Set current pixel to .
                self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = '.'
                #update pixel to the right
                self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h+self.piece_objects[piece].length] = piece
                #update start point
                self.piece_objects[piece].start_h += 1
                self.forward_move_list.append({'piece':piece, 'direction':direction})
                #don't creat vertex dict until you need it
                if self.current_vertex_label not in self.vertex_dict.keys():
                    self.vertex_dict[self.current_vertex_label] = []

                self.vertex_dict[self.current_vertex_label].append(len(self.forward_move_list))
                self.current_vertex_label = len(self.board_list) - 1
                # self.vertex_dict[self.current_vertex_label] = []
                print("Current vertex dict: {}".format(self.vertex_dict))
                return True
            else:
                print("Not a new move, need to try a different direction")
                return False
        else:
            print("Not good - bad move. Current piece: {}".format(piece))


class Piece(object):

    def __init__(self,char, length, start_v, start_h, direction): #, init_v, init_h):

        self.char = char
        self.length = length
        self.start_v = start_v
        self.start_h = start_h
        self.direction = direction
        self.pieces_in_direction = []


if __name__ == "__main__":
    piece_objects = Board()
    piece_objects.launch_solver()