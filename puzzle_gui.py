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

#enable ANSI escape codes on windows
if platform.system() == 'Windows':
    import colorama
    colorama.init()

#issue right now: get stuck in a loop of bad moves, need to fix the bad count logic to go back when a loop is found and try something else

#can use alt directions to see if there is a better solution

class Board(object):

    def __init__(self):
        print("\n\nWelcome to the ")

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


        self.debug_mode = 0
        while self.debug_mode != 1 and self.debug_mode != 2 and self.debug_mode != 3:
            self.debug_mode = int(input("Do you want debug mode on?\n1) Yes - All\n2) No\n3) Yes - Reset Only\n>"))

        #color dict goes up to i, shouldn't be more pieces than that
        #Using ANSI escape codes, if windows a will be green, if mac a will be blue
        if platform.system() == 'Windows':
            self.color_dict = {'.':'\033[0m', 'x':'\033[0;31m','a':'\033[0;32m','b':'\033[1;31m','c':'\033[0;36m','d':'\033[1;33m','e':'\033[0;35m','f':'\033[0;37m','g':'\033[1;34m','h':'\033[1;32m','i':'\033[1;36m','j':'\033[1;35m'}
        else:
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
        self.x_final_h = [] #used to keep track of final h spots that x has visited to avoid resetting bad move count
        self.return_to_x = False #use this to kill current recursion tree, get you back to x, and revert moves until you hit a piece that had another move
        self.last_alt_dir = 0

        self.load_board()
        self.print_piece_stats()

    def load_board(self):
        # with open('puzzle_layout.txt', 'r') as puzzle_read:
        # with open('puzzle_layout2.txt', 'r') as puzzle_read:
        #     puzzle_in = puzzle_read.read().splitlines()

        puzzle_choice = 0
        while puzzle_choice != 1 and puzzle_choice != 2:
            puzzle_choice = int(input("Which puzzle? (1) or (2) \n>"))

        if puzzle_choice == 1:
            with open('puzzle_layout.txt', 'r') as puzzle_read:
                puzzle_in = puzzle_read.read().splitlines()
        else:
            with open('puzzle_layout2.txt', 'r') as puzzle_read:
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

        #find where x starts, add this to final h visited
        self.x_final_h.append(self.main_board['x'].start_h)




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

    #get last recursion call where x moved right
    #logic not finished
    def reset_recursion(self):

        self.last_alt_dir = 0
        #if there are no alt paths after an x right move, go back to the last x Right
        #before adding this logic, need to pop moves off the stack
        while self.last_alt_dir == 0:
            last_x = 0
            last_count = 0
            for move_dict in self.current_path_dict:
                if move_dict['piece'] == 'x' and move_dict['direction'] == 'Right':
                    last_x = last_count
                last_count += 1

            # print("Index of last x: {}".format(last_x))
            # print("Move for last x: {}".format(self.current_path_dict[last_x]))

            #find the last position where there is an alt direction, do a minus one because I don't want to take a look at the piece that put bad move count over the top

            for temp_count in range(last_x, last_count-1):
                # print("temp_count: {}".format(temp_count))
                # print("self.current_path_dict[temp_count]: {}".format(self.current_path_dict[temp_count]))
                if self.current_path_dict[temp_count]['alt_direction'] != 'None':
                    self.last_alt_dir = temp_count
            if self.debug_mode == 1 or self.debug_mode == 3:
                input("Index of last alt dir: {}\nMove for last alt dir: {}\n>".format(self.last_alt_dir, self.current_path_dict[self.last_alt_dir]))
            else:
                print("Index of last alt dir: {}\nMove for last alt dir: {}".format(self.last_alt_dir, self.current_path_dict[self.last_alt_dir]))

            #pop all the bad moves off the list
            if self.last_alt_dir == 0:
                while last_count > last_x-1:
                    pop_piece = self.current_path_dict.pop()
                    last_count -=1
                    self.bad_move_count -=1
                    undo_piece = pop_piece['piece']
                    undo_direction = pop_piece['direction']
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
                    print(self.current_path_dict)
                    self.print_board()
                    if self.debug_mode == 1 or self.debug_mode == 3:
                        input("Getting rid of move: {} \n>".format(pop_piece))
                    else:
                        print("Getting rid of move: {} \n>".format(pop_piece))



        if self.debug_mode == 1:
            input("Leaving reset function\n>")
        else:
            print("Leaving reset function\n>")
        self.print_board()

    #Basically the main game
    def move_x_block(self):

        self.print_board()
        while not self.game_over:
            start = time.time()
            print("Trying to move x")
            allowed_moves = self.check_move('x')
            print("x allowed moves: {}\nBad move count: {}".format(allowed_moves, self.bad_move_count))
            #final position, game over
            if self.main_board['x'].start_h == 4 and self.main_board['x'].start_v == 2:
                self.game_over = True
            elif self.return_to_x == True:
                print("Current Path: {}".format(self.current_path_dict))
                if self.debug_mode == 1:
                    input("Return to x was true, hit too many bad moves and need to start recursion path over\n>")
                else:
                    print("Return to x was true, hit too many bad moves and need to start recursion path over\n>")
                self.reset_recursion()
            #can move right, closer to final position
            elif 'Right' in allowed_moves:
                self.move_piece('x', 'Right')
                self.current_path_dict.append({'piece':'x', 'direction':'Right', 'blocked_piece':'', 'alt_direction':'None'})

                if self.main_board['x'].start_h not in self.x_final_h:
                    if self.debug_mode == 1:
                        input("This was a helpful move by x, do want to reset bad_move_count\n>")
                    else:
                        print("This was a helpful move by x, do want to reset bad_move_count")
                    self.x_final_h.append(self.main_board['x'].start_h)
                    self.bad_move_count = 0
                else:
                    if self.debug_mode == 1:
                        input("This was not a helpful move by x, don't want to reset bad_move_count\n>")
                    else:
                        print("This was not a helpful move by x, don't want to reset bad_move_count")

                self.print_board()
                print("Current x final h: {}".format(self.x_final_h))
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
        print("Recursion function called\nComplex move count: {} Bad move count: {}".format(self.complex_move, self.bad_move_count))
        self.recursion_call_list.append(current_piece)
        print("Current recursion call list: {}".format(self.recursion_call_list))

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

            if self.return_to_x == True:
                print("Going back to start of recursion tree..")
                return

            #too complex of a move, requires too many extra steps
            # elif self.complex_move > 2 and self.moving_forward == True and self.complex_back == False:
            #complex move will probably have to be raised
            if self.complex_move > 3 and self.moving_forward == True and self.complex_back == False:
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
            #elif bad move count is greater than 15, and you are moving_forward you want to go backwards
            elif self.bad_move_count > 25 and self.moving_forward == True:
                print("Hit {} bad moves, going back to start of recursion.")
                self.return_to_x = True
                break

            #need to make sure you are moving forward
            elif try_direction in valid_move_list and self.moving_forward:
                self.complex_back = False
                self.move_piece(blocking_piece,try_direction)
                #check for alt direction, going to reset direction_list for now
                if len(direction_list) > 0:
                    alt_temp = direction_list.pop()
                    direction_list.append(alt_temp)
                else:
                    alt_temp = 'None'

                #need to append this move to list, adding extra directions available and what the blocked piece was to be used for recursion call
                self.current_path_dict.append({'piece':blocking_piece, 'direction':try_direction, 'blocked_piece': current_piece, 'alt_direction':alt_temp})
                print("Current move dict: {}".format(self.current_path_dict))
                #bad_move_count = 0 #want to actually increment here
                self.bad_move_count += 1
                #reset complex move count
                self.complex_move = 0
                self.print_board()

            #turn around when you have gone too many bad moves backwards, return to x


            #this is used by complex back
            elif len(direction_list) > 0 and self.moving_forward == False:
                self.moving_forward = True
                print("Direction list: {}".format(direction_list))
                print("Made it to moving forward equals false and there is another direction")
                try_direction = direction_list.pop()

            #when you have too many bad moves and no more directions, go back a level
            # elif self.moving_forward == True and self.bad_move_count > 9:
            #     if self.debug_mode == 1:
            #         input("Too many bad moves: {}, going backwards".format(self.bad_move_count))
            #     else:
            #         print("Too many bad moves: {}, going backwards".format(self.bad_move_count))
            #
            #     self.moving_forward = False

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



            #revert move and return, this is where I will call the revert move function
            #This might just work for old style
            elif self.moving_forward == False:
                #while loop will make sure there isn't another direction moved by the same piece
                #move this all to the revert function
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

                #move this to top of function, that will help with revert function
                #if there is a wall in that direction it's a bad move, need to to go back
                new_blocking_piece = self.get_block_in_direction(blocking_piece,try_direction)
                if new_blocking_piece == None:
                    self.moving_forward = False
                #otherwise need to move that unblocking piece
                else:
                    print("Piece currently blocking: {} is: {} in direction: {}".format(blocking_piece, new_blocking_piece, try_direction))
                    self.complex_move += 1
                    #need to get rid of new blocking piece
                    self.move_block_recursion(blocking_piece, new_blocking_piece, try_direction)
        if self.moving_forward == True and self.complex_back == False:
            print("<->Leaving while loop, successfully moved: {} out of the way of: {}".format(blocking_piece, current_piece))
            #going to decrement bad move count since this was a successful move
            #self.bad_move_count -= 1 #minus two because when you move the piece over to its final place, it increments the bad move counter, want to get rid of that and go down one
        else:
            print("<->Leaving while loop, not able to move: {} out of the way of: {}".format(blocking_piece, current_piece))
            self.moving_forward = False
        print("Stop checking for: {}, current recursion call list in order of call: {}".format(current_piece,self.recursion_call_list))
        self.recursion_call_list.pop()
        return

    def revert_move(self):
        #get piece and direction of bad move
        self.undo_move = self.current_path_dict.pop()
        self.bad_move_count -= 1
        undo_piece = self.undo_move['piece']
        undo_direction = self.undo_move['direction']
        undo_alt_direction = self.undo_move['alt_direction']

        if self.debug_mode == 1:
            input("Undoing last move\nPiece: {} Direction: {}\nAlt Direction: {}\n>".format(undo_piece, undo_direction, undo_alt_direction))
        else:
            print("Undoing last move\nPiece: {} Direction: {}\nAlt Direction: {}\n>".format(undo_piece, undo_direction, undo_alt_direction))

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
        self.complex_move = 0
        self.print_board()
        if self.debug_mode == 1:
            input("Just moved piece: {}, now going to return to previous piece\n>".format(undo_piece))
        else:
            print("Just moved piece: {}, now going to return to previous piece\n>".format(undo_piece))


        #check to see if next piece (backwards) has another another direction
        #if it does, call recursion and try to move that direction
        #if it doesn't, call revert again
        self.undo_move = self.current_path_dict.pop()
        self.bad_move_count -= 1
        undo_piece = self.undo_move['piece']
        undo_direction = self.undo_move['direction']
        undo_alt_direction = self.undo_move['alt_direction']
        if undo_alt_direction == 'None':
            self.revert_move()
        else:
            #this doesn't seem right
            undo_block_piece = self.get_block_in_direction(undo_piece, undo_alt_direction)
            #this will break where I'm at in the first recursion branch
            self.move_block_recursion(undo_piece, undo_block_piece, undo_alt_direction)




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

    #check to see if moving piece all the way in a direction would be helpful, added logic for piece in same direction
    def check_helpful_move(self, blocked_piece, blocking_piece):
        self.get_path_same_direction(blocking_piece)
        move_return_list = []
        #if its a vertical piece, blocking piece can move right or left as long as there is a move in that direction that clears the piece out of column where start_v is
        if self.main_board[blocked_piece].direction == 'v':
            print("Piece blocking vertical piece is horizontal")
            #can move a max of 4 grids over, skip over offset of 0 since that means no movement
            if self.main_board[blocking_piece].pieces_in_direction == []:
                print("Horizontal piece doesn't have any pieces in the same row")
                h_min = -1
                h_max = 6
            else:
                print("Horizontal piece has a piece in the same row")
                #this doesn't actually work like I was hoping, need to check and see if piece can actually move down two, will need a separate section
                horizontal_block = self.main_board[blocking_piece].pieces_in_direction.pop()
                #initial piece is above new piece
                if self.main_board[blocking_piece].start_h < self.main_board[horizontal_block].start_h:
                    h_min = -1
                    h_max = 4
                else:
                    h_min = 2
                    h_max = 6


            for h_offset in range(1,h_max-1):
                #check right, make sure it is in bounds o, do a minus one to get the actual last position of the piece
                if (self.main_board[blocking_piece].start_h + self.main_board[blocking_piece].length - 1 + h_offset) < h_max:
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
                if (self.main_board[blocking_piece].start_h  - h_offset) > h_min:
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
            print("Piece blocking horizontal piece is  vertical")
            #can move a max of 4 grids over, skip over offset of 0 since that means no movement
            if self.main_board[blocking_piece].pieces_in_direction == []:
                print("Vertical piece doesn't have any pieces in the same column")
                v_min = -1
                v_max = 6
            else:
                print("Vertical piece has a piece in the same column")
                #this doesn't actually work like I was hoping, need to check and see if piece can actually move down two, will need a separate section
                vertical_block = self.main_board[blocking_piece].pieces_in_direction.pop()
                #initial piece is above new piece
                if self.main_board[blocking_piece].start_v < self.main_board[vertical_block].start_v:
                    v_min = -1
                    v_max = 4
                else:
                    v_min = 2
                    v_max = 6

            for v_offset in range(1,v_max-1):
                #check up, make sure it is in bounds of 0
                if (self.main_board[blocking_piece].start_v - v_offset) > v_min:
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
                if (self.main_board[blocking_piece].start_v + self.main_board[blocking_piece].length - 1 + v_offset) < v_max:
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

    #use this in check helpful move when there are two pieces oriented in the same direction in the same row or column
    #want to use this in the calculation to prevent a helpful move that isn't going to help
    def get_path_same_direction(self, piece):
        #input("In get_path_same_direction\n>")

        for check_piece in self.piece_list:
            #input("Piece: {} v: {} h: {}\nCheck: {} v: {} h: {}".format(piece, self.main_board[piece].start_v, self.main_board[piece].start_h, check_piece, self.main_board[check_piece].start_v, self.main_board[check_piece].start_h))
            #pieces moving in the same direction
            if self.main_board[check_piece].direction == 'v' and self.main_board[piece].direction == 'v':
                if self.main_board[check_piece].start_h == self.main_board[piece].start_h and check_piece != piece:
                    self.main_board[piece].pieces_in_direction.append(check_piece)
            elif self.main_board[check_piece].direction == 'h' and self.main_board[piece].direction == 'h':
                if self.main_board[check_piece].start_v == self.main_board[piece].start_v and check_piece != piece:
                    self.main_board[piece].pieces_in_direction.append(check_piece)


        print("Pieces in same direction for piece: {} : {}".format( piece, self.main_board[piece].pieces_in_direction))

#pasted this back in, going to use it for reference
    def revert_move_bad():
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
        self.pieces_in_direction = []


if __name__== "__main__":
    my_board = Board()
    my_board.move_x_block()
