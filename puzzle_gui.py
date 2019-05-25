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
#use this to print color on mac and regular on windows
import platform
import time

class Board(object):

    def __init__(self):
        print("\n\nWelcome to the ")
        #mac color
        if platform.system() == 'Darwin':
            print("""
 _______________________________________
|\033[0;31m     _____               _             \033[0m|
|\033[0;31m    |  __ \             | |            \033[0m|
|\033[0;31m    | |__) |   _ _______| | ___        \033[0m|
|\033[0;31m    |  ___/ | | |_  /_  / |/ _ \       \033[0m|
|\033[0;31m    | |   | |_| |/ / / /| |  __/       \033[0m|
|\033[0;31m    |_|    \__,_/___/___|_|\___|       \033[0m|
|\033[0;31m    _____       _                  _   \033[0m|
|\033[0;31m   / ____|     | |                | |  \033[0m|
|\033[0;31m  | (___   ___ | |_   _____ _ __  | |  \033[0m|
|\033[0;31m   \___ \ / _ \| \ \ / / _ \ '__| | |  \033[0m|
|\033[0;31m   ____) | (_) | |\ v /  __/ |    |_|  \033[0m|
|\033[0;31m  |_____/ \___/|_| \_/ \___|_|    (_)  \033[0m|
|_______________________________________\033[0m|

""")
#\033[33;5m
        else:
            print("""
 _______________________________________
|     _____               _             |
|    |  __ \             | |            |
|    | |__) |   _ _______| | ___        |
|    |  ___/ | | |_  /_  / |/ _ \       |
|    | |   | |_| |/ / / /| |  __/       |
|    |_|    \__,_/___/___|_|\___|       |
|    _____       _                  _   |
|   / ____|     | |                | |  |
|  | (___   ___ | |_   _____ _ __  | |  |
|   \___ \ / _ \| \ \ / / _ \ '__| | |  |
|   ____) | (_) | |\ v /  __/ |    |_|  |
|  |_____/ \___/|_| \_/ \___|_|    (_)  |
|_______________________________________|

""")

        self.debug_mode = 0
        while self.debug_mode != 1 and self.debug_mode != 2:
            self.debug_mode = int(input("Do you want debug mode on?\n1) Yes\n2) No\n>"))

        #color dict goes up to i, shouldn't be more pieces than that
        #Using ANSI escape codes on Mac
        self.color_dict = {'.':'\033[0m', 'x':'\033[0;31m','a':'\033[0;34m','b':'\033[1;31m','c':'\033[0;36m','d':'\033[1;33m','e':'\033[0;35m','f':'\033[0;37m','g':'\033[1;34m','h':'\033[1;32m','i':'\033[1;36m','j':'\033[1;35m'}
        self.piece_list =[]
        self.main_board = {}
        self.undo_move = {}
        self.complex_move = 0 #used when a piece is blocked by a piece that is blocked by another piece, if this number gets too large and complex then want to go back
        self.complex_back = False
        self.recursion_call_list = [] #use this for sanity checks
        self.show_board = [['.' for x in range(6)] for y in range(6)]
        self.start_board = [['.' for x in range(6)] for y in range(6)] #use this to reset show board at the end and then move all pieces
        self.game_over = False
        self.bad_move_count = 0 #used when you try to go down a path that is not helpful
        self.current_path_dict = []
        self.moving_forward = True #set this as false while you are going back through moves

        self.load_board()
        self.print_piece_stats()

    def load_board(self):
        with open('puzzle_layout.txt', 'r') as puzzle_read:
        # with open('puzzle_layout2.txt', 'r') as puzzle_read:
            puzzle_in = puzzle_read.read().splitlines()

        #build board
        start_pieces = {}
        for v in range(6):
            for h in range(6):
                #if finding for the first time, create dictionary value
                current_piece = puzzle_in[v][h]
                #only want to find letters
                if(current_piece != "."):
                    #initialize piece stats if it hasn't been added yet
                    if(current_piece not in start_pieces.keys()):
                        start_pieces[current_piece] = {'start_v':v, 'start_h':h,'length':1, 'init_v':v, 'init_h':h}
                        #check direction, won't be above or to the left
                        #check boundaries, make sure you aren't in the last row or column
                        if(v!=5):
                            if(puzzle_in[v+1][h] == current_piece):
                                #update direction as v - vertical
                                start_pieces[current_piece]['direction'] = 'v'
                        if(h!=5):
                            if(puzzle_in[v][h+1] == current_piece):
                                #update direction as h - horizontal
                                start_pieces[current_piece]['direction'] = 'h'
                        #print("{} found at v={},h={} with direction={}".format(current_piece,v,h, start_pieces[current_piece]['direction']))
                    #increment length if letter has already been added
                    else:
                        start_pieces[current_piece]['length']+=1

        #build final variables
        for piece in start_pieces.keys():
            self.piece_list.append(piece)
            self.main_board[piece] = Piece(piece, start_pieces[piece]['length'], start_pieces[piece]['start_v'], start_pieces[piece]['start_h'], start_pieces[piece]['direction'], start_pieces[piece]['init_v'], start_pieces[piece]['init_h'])

        #build show_board and start_board
        for piece in self.piece_list:
            #print(self.main_board[piece].direction)
            #if horizontal
            if self.main_board[piece].direction == 'h':
                for i in range(self.main_board[piece].length):
                    self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h+i] = piece
                    self.start_board[self.main_board[piece].start_v][self.main_board[piece].start_h+i] = piece
                    #print("Wow_h:{}".format(show_board[self.main_board[piece].start_v][self.main_board[piece].start_h+i]))
            #vertical
            else:
                for i in range(self.main_board[piece].length):
                    self.show_board[self.main_board[piece].start_v+i][self.main_board[piece].start_h] = piece
                    self.start_board[self.main_board[piece].start_v+i][self.main_board[piece].start_h] = piece
                    #print("Wow_v:{}".format(show_board[self.main_board[piece].start_v+i][self.main_board[piece].start_h]))

    def print_piece_stats(self):
        for piece in self.piece_list:
            print("Piece:{}, Length:{}, Start_v:{}, Start_h:{}, Direction:{}".format(piece,self.main_board[piece].length,self.main_board[piece].start_v,self.main_board[piece].start_h,self.main_board[piece].direction))

    def print_final_moves(self):
        for curr_move in self.current_path_dict:
            input("Next move?\n>")
            curr_piece = curr_move['piece']
            curr_direction = curr_move['direction']
            print("Piece: {}, Direction: {}".format(curr_piece, curr_direction))
            self.move_piece(curr_piece,curr_direction)
            self.print_board()
        print("x has reached the exit!")


    def reset_show_board_and_start(self):
        for v in range(6):
            for h in range(6):
                self.show_board[v][h] = self.start_board[v][h]
        for piece in self.piece_list:
            self.main_board[piece].start_v = self.main_board[piece].init_v
            self.main_board[piece].start_h = self.main_board[piece].init_h


    def print_board(self):
        if platform.system() == 'Darwin':
            #Mac version, shows colors
            print("   0 1 2 3 4 5 \n :=============:",end='')
            for v in range(6):
                print("\n{}| ".format(v),end='')
                for h in range(6):
                    curr_piece = self.show_board[v][h]
                    print("{}{}\033[0m ".format(self.color_dict[curr_piece],curr_piece),end='')
                #skip the exit wall
                if v != 2:
                    print("|",end='')
            print('\n :=============:')
        #windows, color characters show up as arrows instead
        else:
            print("   0 1 2 3 4 5 \n :=============:",end='')
            for v in range(6):
                print("\n{}| ".format(v),end='')
                for h in range(6):
                    print("{} ".format(self.show_board[v][h]),end='')
                #skip the exit wall
                if v != 2:
                    print("|",end='')
            print('\n :=============:')


    #run this function assuming that move is valid, not doing any boundary or direction checking
    def move_piece(self, piece, direction):

        if direction == 'Down':
            print("Moving: {} down".format(piece))
            #set current pixel to .
            self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h] = '.'
            #update pixel below
            self.show_board[self.main_board[piece].start_v+self.main_board[piece].length][self.main_board[piece].start_h] = piece
            #update start point
            self.main_board[piece].start_v += 1
        elif direction == 'Up':
            print("Moving: {} Up".format(piece))
            #update start point
            self.main_board[piece].start_v -= 1
            #set new top to current letter
            self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h] = piece
            #set bottom pixel to .
            self.show_board[self.main_board[piece].start_v+self.main_board[piece].length][self.main_board[piece].start_h] = '.'
        elif direction == 'Left':
            print("Moving: {} Left".format(piece))
            #update start point
            self.main_board[piece].start_h -= 1
            #set new left to current letter
            self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h] = piece
            #set old right pixel to .
            self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h+self.main_board[piece].length] = '.'
        elif direction == 'Right':
            print("Moving: {} Right".format(piece))
            #Set current pixel to .
            self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h] = '.'
            #update pixel to the right
            self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h+self.main_board[piece].length] = piece
            #update start point
            self.main_board[piece].start_h += 1
        else:
            print("Not good - bad move. Current piece: {}".format(piece))

    #Basically the main game
    def move_x_block(self):

        self.print_board()
        while not self.game_over:
            start = time.time()
            print("Trying to move x")
            allowed_moves = self.check_move('x')
            print("x allowed moves: {}".format(allowed_moves))
            #final position, game over
            if self.main_board['x'].start_h == 4 and self.main_board['x'].start_v == 2:
                self.game_over = True
            #can move right, closer to final position
            elif 'Right' in allowed_moves:
                self.move_piece('x', 'Right')
                self.current_path_dict.append({'piece':'x', 'direction':'Right'})
                self.bad_move_count = 0
                self.print_board()
                if self.debug_mode == 1:
                    input("Piece: {} moved: {}\nKeep searching?\n>".format('x', 'Right'))
                else:
                    print("Piece: {} moved: {}\nKeep searching?\n>".format('x', 'Right'))
            #can't move right, need to move blocking piece
            else:
                #need to find piece that is blocking you directly to the Right
                x_block = self.show_board[self.main_board['x'].start_v][self.main_board['x'].start_h+self.main_board['x'].length]
                #need to find location that blocking piece should be so x can move
                if self.debug_mode == 1:
                    input("Piece currently blocking x: {} In direction: {}\nCalling Recursion\n>".format(x_block, 'Right'))
                else:
                    print("Piece currently blocking x: {} In direction: {}\nCalling Recursion\n>".format(x_block, 'Right'))
                self.move_block_recursion('x', x_block, 'Right')

        print("""
 _______________________________________
|\033[0;31m     _____               _             \033[0m|
|\033[0;31m    |  __ \             | |            \033[0m|
|\033[0;31m    | |__) |   _ _______| | ___        \033[0m|
|\033[0;31m    |  ___/ | | |_  /_  / |/ _ \       \033[0m|
|\033[0;31m    | |   | |_| |/ / / /| |  __/       \033[0m|
|\033[0;31m    |_|    \__,_/___/___|_|\___|       \033[0m|
|\033[0;31m    _____       _               _   _  \033[0m|
|\033[0;31m   / ____|     | |             | | | | \033[0m|
|\033[0;31m  | (___   ___ | |_   _____  __| | | | \033[0m|
|\033[0;31m   \___ \ / _ \| \ \ / / _ \/ _` | | | \033[0m|
|\033[0;31m   ____) | (_) | |\ V /  __/ (_| | |_| \033[0m|
|\033[0;31m  |_____/ \___/|_| \_/ \___|\__,_| (_) \033[0m|
|_______________________________________|


""")
        end = time.time()
        ms_time = round(((end-start) * 1000),4)
        print("Time for completion: {} ms".format(ms_time))
        input("Resetting board to step through the solution..\n>")
        self.reset_show_board_and_start()
        self.print_board()
        self.print_final_moves()

    #recursion function
    def move_block_recursion(self, current_piece, blocking_piece, move_direction):
        print("Recursion function called\nComplex move count: {}".format(self.complex_move))
        self.recursion_call_list.append(current_piece)

        open_coords = self.get_open_coords(current_piece, move_direction)
        v_open = open_coords['v']
        h_open = open_coords['h']
        print("Need position v:{},h:{} open for: {}".format(v_open, h_open, current_piece))

        direction_list = self.check_helpful_move(current_piece, blocking_piece)
        print("Helpful move(s) by: {}: {}".format(blocking_piece, direction_list))

        try_direction = direction_list.pop()#remove entry from direction_list so you don't try it again


        #go through this loop until you can move this piece
        #create a complex move count, if its > 2 then go back
        while self.show_board[v_open][h_open] != '.':

            #input("Trying to move piece: {} in direction: {} - While loop start \nMoving forward: {}\n>".format(blocking_piece, try_direction, self.moving_forward))
            if self.debug_mode == 1:
                input("Trying to move piece: {} in direction: {} - While loop start \nBad count: {}, Moving forward: {}\n>".format(blocking_piece, try_direction,self.bad_move_count, self.moving_forward))
            else:
                print("Trying to move piece: {} in direction: {} - While loop start \nBad count: {}, Moving forward: {}\n>".format(blocking_piece, try_direction,self.bad_move_count, self.moving_forward))
            print("Current direction_list for piece: {}: {}".format(blocking_piece,direction_list))
            valid_move_list = self.check_move(blocking_piece)

            # #gets stuck in a loop, this may be unneccessary now that I have complex_move
            # if self.bad_move_count > 15 and self.moving_forward == True:
            #     self.moving_forward = False
            #     input("Hit {} \"bad\" moves\n>".format(self.bad_move_count))

            #too complex of a move, requires too many extra steps
            # elif self.complex_move > 2 and self.moving_forward == True and self.complex_back == False:
            #complex move will probably have to be raised
            if self.complex_move > 2 and self.moving_forward == True and self.complex_back == False:
                #maybe set moving_forward as backward here
                self.complex_back = True
                if self.debug_mode == 1:
                    input("Too complex of a move, going back\n>")
                else:
                    print("Too complex of a move, going back\n>")
                self.complex_move -= 1
                self.moving_forward == False
                break

            #put bad move count check before this
            #need to make sure you are moving forward
            elif try_direction in valid_move_list and self.moving_forward:
                self.complex_back = False
                self.move_piece(blocking_piece,try_direction)
                #need to append this move to list
                self.current_path_dict.append({'piece':blocking_piece, 'direction':try_direction})
                print("Current move dict: {}".format(self.current_path_dict))
                #bad_move_count = 0 #want to actually increment here
                self.bad_move_count += 1
                #reset complex move count
                self.complex_move = 0
                self.print_board()


            #moving backward and this current piece has a valid move, hoping this makes it hit the last else block and then try to go the other direction
            #this doesn't  work exactly as expected
            #only want to change direction when going backwards
            elif len(direction_list) > 0 and self.moving_forward == False:
                self.moving_forward = True
                print("Direction list: {}".format(direction_list))
                print("Made it to moving forward equals false and there is another direction")
                try_direction = direction_list.pop()

            #when we need to go to the start of the bad complex move, keep going back until you find where you started
            elif self.complex_back == True and self.complex_move > 1:
                print("Going back on a complex move")
                self.complex_move -= 1
                #I think I need to break here?
                break

            #when you reach the beginning of the complex move start going forward again
            elif self.complex_back == True and self.complex_move == 0:
                self.complex_back = False
                self.moving_forward = True





            #revert move and return
            elif self.moving_forward == False:
                #while loop will make sure there isn't another direction moved by the same piece
                self.undo_move = self.current_path_dict.pop()
                self.bad_move_count -= 1
                while self.undo_move['piece'] == blocking_piece:

                    undo_piece = self.undo_move['piece']
                    undo_direction = self.undo_move['direction']
                    print("Going to undo move for: {}, printing to make sure it's the right piece".format(undo_piece))#may want to actually do a check for this
                    print("Current move dict: {}".format(self.current_path_dict))
                    if undo_direction == 'Left':
                        self.move_piece(undo_piece,'Right')
                    elif undo_direction == 'Right':
                        self.move_piece(undo_piece, 'Left')
                    elif undo_direction == 'Up':
                        self.move_piece(undo_piece, 'Down')
                    elif undo_direction == 'Down':
                        self.move_piece(undo_piece,'Up')
                    else:
                        print("Bad direction passed to move backwards")
                    self.undo_move = self.current_path_dict.pop()
                    self.bad_move_count -= 1
                    self.print_board()
                    if self.debug_mode == 1:
                        input("Just moved piece: {}, now going to return to previous piece or move again\n>".format(undo_piece))
                    else:
                        print("Just moved piece: {}, now going to return to previous piece or move again\n>".format(undo_piece))
                print("Trying break to go one level up")
                #push last piece back to the stack
                self.current_path_dict.append(self.undo_move)
                self.bad_move_count += 1
                #go back to previous move
                break


            else:
                print("Can't move piece: {} in direction: {}.".format(blocking_piece, try_direction))

                #if there is a wall in that direction it's a bad move, need to to go back
                new_blocking_piece = self.get_block_in_direction(blocking_piece,try_direction)
                if new_blocking_piece == None:
                    self.moving_forward = False
                #otherwise need to move that unblocking piece
                else:
                    print("Piece currently blocking: {} is: {} in direction: {}".format(blocking_piece, new_blocking_piece, try_direction))
                    self.complex_move += 1
                    self.move_block_recursion(blocking_piece, new_blocking_piece, try_direction)
        if self.moving_forward == True and self.complex_back == False:
            print("<->Leaving while loop, successfully moved: {} out of the way of: {}".format(blocking_piece, current_piece))
            #going to decrement bad move count since this was a successful move
            self.bad_move_count -= 2 #minus two because when you move the piece over to its final place, it increments the bad move counter, want to get rid of that and go down one
        else:
            print("<->Leaving while loop, not able to move: {} out of the way of: {}".format(blocking_piece, current_piece))
            self.moving_forward = False
        print("Stop checking for: {}, current recursion call list in order of call: {}".format(current_piece,self.recursion_call_list))
        self.recursion_call_list.pop()
        return


    def get_open_coords(self, current_piece, needed_direction):
        #print("Checking what coordinates need to be open")
        if needed_direction == 'Left':
            return {'v':self.main_board[current_piece].start_v, 'h':self.main_board[current_piece].start_h-1}
        elif needed_direction == 'Right':
            return {'v':self.main_board[current_piece].start_v, 'h':self.main_board[current_piece].start_h+self.main_board[current_piece].length}
        elif needed_direction == 'Up':
            return {'v':self.main_board[current_piece].start_v-1, 'h':self.main_board[current_piece].start_h}
        elif needed_direction == 'Down':
            return {'v':self.main_board[current_piece].start_v+self.main_board[current_piece].length, 'h':self.main_board[current_piece].start_h}
        else:
            print("Bad direction passed to get_open_coords")
            return

    #check what the icon is of the piece directly in that direction, or return None if it is up against a wall
    #this assumes block check worked and there is a piece blocking
    def get_block_in_direction(self, piece, direction):
        print("Checking what is blocking piece: {}".format(piece))
        #need to check and make sure piece is not blocking you
        if direction == 'Left':
            #make sure you aren't at left boundary
            if self.main_board[piece].start_h - 1 > -1:
                return self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h-1]
        elif direction == 'Right':
            #make sure you aren't at right boundary
            if (self.main_board[piece].start_h + self.main_board[piece].length) < 6:
                return self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h + self.main_board[piece].length]
        elif direction == 'Up':
            #make sure you arent at the upper bound
            if self.main_board[piece].start_v - 1 > -1:
                return self.show_board[self.main_board[piece].start_v-1][self.main_board[piece].start_h]
        elif direction == 'Down':
            #make sure you aren't at lower bound
            if self.main_board[piece].start_v + self.main_board[piece].length < 6:
                return self.show_board[self.main_board[piece].start_v + self.main_board[piece].length][self.main_board[piece].start_h]
        else: #bad direction
            print("Bad direction passed to get_block_in_direction")
        #if there is a boundary blocking you will reach this return statement
        return None

    #check to see if moving piece all the way in a direction would be helpful
    #need to add logic to prefer a direction that is closer when there are two directions that it can move - maybe
    def check_helpful_move(self, blocked_piece, blocking_piece):
        move_return_list = []
        #if its a vertical piece, blocking piece can move right or left as long as there is a move in that direction that clears the piece out of column where start_v is
        if self.main_board[blocked_piece].direction == 'v':
            #can move a max of 4 grids over, skip over offset of 0 since that means no movement
            for h_offset in range(1,5):
                #check right, make sure it is in bounds of 5, do a minus one to get the actual last position of the piece
                if (self.main_board[blocking_piece].start_h + self.main_board[blocking_piece].length - 1 + h_offset) < 6:
                    can_move = True
                    #get h index of all positions of where the blocking piece could be
                    for piece_offset in range(self.main_board[blocking_piece].length):
                        #if that piece is in the same index as the blocked piece start then it cannot be added as a valid direction
                        if (self.main_board[blocking_piece].start_h + piece_offset + h_offset) == self.main_board[blocked_piece].start_h:
                            can_move = False
                    #if you didn't find a piece that matched the start index then it is a valid move
                    if can_move:
                        #make sure move hasn't alrady been added
                        if 'Right' not in move_return_list:
                            move_return_list.append('Right')

                #check left, make sure it is in bounds of 0
                if (self.main_board[blocking_piece].start_h  - h_offset) > -1:
                    can_move = True
                    #get h index of all positions of where the blocking piece could be
                    for piece_offset in range(self.main_board[blocking_piece].length):
                        #if that piece is in the same index as the blocked piece start then it cannot be added as a valid direction
                        if (self.main_board[blocking_piece].start_h + piece_offset - h_offset) == self.main_board[blocked_piece].start_h:
                            can_move = False
                    #if you didn't find a piece that matched the start index then it is a valid move
                    if can_move:
                        #make sure move hasn't alrady been added
                        if 'Left' not in move_return_list:
                            move_return_list.append('Left')
        #else horizontal
        else:
            #can move a max of 4 grids over, skip over offset of 0 since that means no movement
            for v_offset in range(1,5):
                #check up, make sure it is in bounds of 0
                if (self.main_board[blocking_piece].start_v - v_offset) > -1:
                    can_move = True
                    #get v index of all positions where the blocking piece could be
                    for piece_offset in range(self.main_board[blocking_piece].length):
                        #if that piece is in the same index as the blocked piece start then it cannot be added as a valid direction
                        if(self.main_board[blocking_piece].start_v + piece_offset - v_offset) == self.main_board[blocked_piece].start_v:
                            can_move = False
                    #if you didn't find a piece that matched the start index then it is a valid move
                    if can_move:
                        #make sure move hasn't alrady been added
                        if 'Up' not in move_return_list:
                            move_return_list.append('Up')
                #check Down, make sure it is in bounds of 5, do a minus one to get the actual last position of the piece
                if (self.main_board[blocking_piece].start_v + self.main_board[blocking_piece].length - 1 + v_offset) < 6:
                    can_move = True
                    #get v index of all positions where the blocking piece could be
                    for piece_offset in range(self.main_board[blocking_piece].length):
                        #if that piece is in the same index as the blocked piece start then it cannot be added as a valid direction
                        if(self.main_board[blocking_piece].start_v + piece_offset + v_offset) == self.main_board[blocked_piece].start_v:
                            can_move = False
                    #if you didn't find a piece that matched the start index then it is a valid move
                    if can_move:
                        #make sure move hasn't alrady been added
                        if 'Down' not in move_return_list:
                            move_return_list.append('Down')

        return move_return_list


    def revert_move():
        print("calling revert move")
        #once list is empty it will exit
        while current_path_moves:
            current_move = current_path_moves.pop()
            if current_move['direction'] == 'Left':
                print("Reverting piece: {}Bad moves left to undo: {}".format(current_move['piece'],len(current_path_moves)))
                self.move_piece(current_move['piece'], 'Right')#opposite direction
                self.print_board()
                if self.debug_mode == 1:
                    input("Keep searching?\n>")
                else:
                    print("Keep searching?\n>")
            elif current_move['direction'] == 'Right':
                print("Reverting piece: {}Bad moves left to undo: {}".format(current_move['piece'],len(current_path_moves)))
                self.move_piece(current_move['piece'], 'Left')#opposite direction
                self.print_board()
                if self.debug_mode == 1:
                    input("Keep searching?\n>")
                else:
                    print("Keep searching?\n>")
            elif current_move['direction'] == 'Up':
                print("Reverting piece: {}Bad moves left to undo: {}".format(current_move['piece'],len(current_path_moves)))
                self.move_piece(current_move['piece'], 'Down')#opposite direction
                self.print_board()
                if self.debug_mode == 1:
                    input("Keep searching?\n>")
                else:
                    print("Keep searching?\n>")
            elif current_move['direction'] == 'Down':
                print("Reverting piece: {}Bad moves left to undo: {}".format(current_move['piece'],len(current_path_moves)))
                self.move_piece(current_move['piece'], 'Up')#opposite direction
                self.print_board()
                if self.debug_mode == 1:
                    input("Keep searching?\n>")
                else:
                    print("Keep searching?\n>")
            else:
                print("Not good - bad revert move. Current piece: {}".format(current_move['piece']))

    #use this to see if piece can move to an open space
    def check_move(self, piece):
        #check vertical
        move_list = []
        if self.main_board[piece].direction == 'v':
            #check up, upperbound
            if self.main_board[piece].start_v > 0:
                #store for easier reading
                current_letter = self.show_board[self.main_board[piece].start_v-1][self.main_board[piece].start_h]
                if current_letter == '.':
                    move_list.append('Up')
            #check lower bound
            if (self.main_board[piece].start_v + self.main_board[piece].length) < 6:
                #store for easier reading
                current_letter = self.show_board[self.main_board[piece].start_v+ self.main_board[piece].length][self.main_board[piece].start_h]
                if current_letter == '.':
                    move_list.append('Down')
        #check horizontal
        else:
            #check left
            if self.main_board[piece].start_h > 0:
                #store for easier reading
                current_letter = self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h-1]
                if current_letter == '.':
                    move_list.append('Left')
            #check right
            if (self.main_board[piece].start_h + self.main_board[piece].length) < 6:
                #store for easier reading
                current_letter = self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h + self.main_board[piece].length]
                if current_letter == '.':
                    move_list.append('Right')

        return move_list

    def show_valid_moves(self):
        for piece in self.piece_list:
            print("Move list for {} : {}".format(piece, self.check_move(piece)))


class Piece(object):

    def __init__(self,char, length, start_v, start_h, direction, init_v, init_h):
        #char is pictoral representation on the board
        self.char = char
        #length is how long the piece is
        self.length = length
        #start coordinates
        self.start_v = start_v
        self.start_h = start_h
        self.init_v = init_v
        self.init_h = init_h
        #direction piece is facing
        self.direction = direction


if __name__== "__main__":
    my_board = Board()
    my_board.move_x_block()
