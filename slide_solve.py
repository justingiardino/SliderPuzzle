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
        self.piece_list = [] #keep track of all available pieces on the board
        self.piece_objects = {} #keep track of all piece objects, this is the same as the old main_board
        self.vertex_dict = {0:{}} #keep track of possible other moves, "vertices" {Label1: {vertex1: {piece1:direction1}, vertex2: {piece2:direction2}}}
        self.opposite_dir = {'Right':'Left', 'Left':'Right', 'Up':'Down', 'Down':'Up'} #not actually used yet
        self.move_count = 0
        self.board_list = [] #keep track of all the different board setups I've been in so I don't move back into a bad move
        # self.move_list = [] #used for debugging loop I'm stuck in

        print("\n\n\nWelcome to the new slide puzzle solver!\n" + "-"*39)

        self.debug_mode = 0
        while self.debug_mode != 1 and self.debug_mode != 2:
            self.debug_mode = int(input("Do you want debug mode on?\n1) Yes\n2) No\n>"))

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

        while puzzle_choice != 1 and puzzle_choice != 2 and puzzle_choice != 3:
            puzzle_choice = int(input("Which puzzle? (1), (2), or (3) \n>"))

        if puzzle_choice == 1:
            with open('Sliders/puzzle_layout.txt', 'r') as puzzle_read:
                puzzle_in = puzzle_read.read().splitlines()
        elif puzzle_choice == 2:
            with open('Sliders/puzzle_not_square.txt', 'r') as puzzle_read:
                puzzle_in = puzzle_read.read().splitlines()
        else:
            with open('Sliders/puzzle_layout3.txt', 'r') as puzzle_read:
                puzzle_in = puzzle_read.read().splitlines()

        self.v_size = len(puzzle_in)
        self.h_size = len(puzzle_in[0])
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
        input("Show board: \n{}\n".format(self.show_board))

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

    # def update_board_list(self):
    #     # temp_board = [x[:] for x in self.show_board]
    #     # if temp_board in self.board_list:
    #     #     print("This board already existed")
    #     # print(temp_board)
    #     self.board_list.append(temp_board)


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
        self.solve_puzzle({'piece': 'x', 'direction':'None'})
        #self.solve_maze_old(self.start_v, self.start_h)
        #self.print_maze()
        end = time.time()
        ms_time = round(((end-start) * 1000),4)
        print("Game over, Puzzle solved!\nTime for completion: {} ms".format(ms_time))


    #main recursive function
    #curr_move should be a dict with the last move = {piece: 'x', direction: 'Right'}
    #instead of curr_move I'm going to have to save the state of the board so I don't do a duplicate move
    def solve_puzzle(self, curr_move):
        # self.print_board()
        print("Called recursion, last piece moved: {}".format(curr_move['piece']))
        #print("Current move list: {}".format(self.move_list))
        if self.debug_mode == 1:
            input("Continue?\n>")
        else:
            print("Continue?\n>")

        #need to check all available moves
        found_moves = self.check_moves(curr_move['piece'], curr_move['direction'])
        print("Available moves: {}".format(found_moves))

        #continue to try moving all directions until there are no more to try
        while found_moves:
            try_move = found_moves.pop()


            #build new vertex here
            input("Going to try moving piece: {} in direction: {}\n>".format(try_move['piece'], try_move['direction']))

            #move the piece
            if(self.move_piece(try_move['piece'], try_move['direction'])):
                # self.board_list.append(self.show_board)
                self.move_count += 1
                # self.move_list.append(curr_move)
                self.print_board()
                print("Current show board: \n{}".format(self.show_board))
                # temp_list = self.show_board.copy()
                # self.board_list.append(temp_list)
                # self.update_board_list()
                # self.get_temp_board('x','None')
                print("Just moved: {}".format(try_move))
                print("Current board list: {}".format(self.board_list))
                if self.debug_mode == 1:
                    input("Next Step?\n>")
                else:
                    print("Next Step?\n>")

                print("Calling recursive function on this new piece")
                self.solve_puzzle({'piece': try_move['piece'], 'direction': try_move['direction']})
            else:
                print("Move piece false on piece: {}".format(try_move['piece']))

        print("No more moves found, last piece that was moved was: {} in direction: {}".format(curr_move['piece'], curr_move['direction']))
        self.print_board()
        input("\n\n" + "-"*25 + "\nThis is where I need to undo move before going back one level\n>")

    #have to create a copy of the current board to avoid the pointer issue
    #checks to see if the attempted move would be a move that has already been made
    #returns boolen of a valid (not duplicate)  move or not
    def get_temp_board(self, piece, direction, curr_board):
        temp_board = [x[:] for x in curr_board]
        v_offset_piece = 0
        h_offset_piece = 0
        v_offset_blank = 0
        h_offset_blank = 0

        input("temp_board before: {}\n>".format(temp_board))

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

        print("Offsets\nv_piece: {}, h_piece: {}\nv_blank: {}, h_blank: {}".format(v_offset_piece, h_offset_piece, v_offset_blank, h_offset_blank))
        temp_board[v_offset_piece][h_offset_piece] = piece
        temp_board[v_offset_blank][h_offset_blank] = '.'

        input("temp_board after: {}\nChecking to see if board is already in list\n>".format(temp_board))
        if temp_board in self.board_list:
            print("This board has already been created")
            input("Current board list: {}\n>".format(self.board_list))
            return False
        else:
            print("This board has not been created, adding now")
            self.board_list.append(temp_board)
            input("Current board list: {}\n>".format(self.board_list))
            return True




    #before updating board need to make sure this move hasn't already been made
    #run this function assuming that move is valid, not doing any boundary or direction checking
    def move_piece(self, piece, direction):
        # temp_board = [x[:] for x in self.show_board]
        # input("temp_board before: {}\n>".format(temp_board))

        if direction == 'Down':
            print("Moving: {} down".format(piece))
            #set current pixel to .
            if(self.get_temp_board(piece,direction, self.show_board) == True):
                print("New move")
                self.show_board[self.piece_objects[piece].start_v][self.piece_objects[piece].start_h] = '.'
                #update pixel below
                self.show_board[self.piece_objects[piece].start_v+self.piece_objects[piece].length][self.piece_objects[piece].start_h] = piece
                #update start point
                self.piece_objects[piece].start_v += 1
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
