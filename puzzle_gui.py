#looks like it's getting stuck on finding x again, d is trying to force x out of the way when trying to go up. This is a bad direction and why I need to get the revert working

#need to install termcolor on mac
#from termcolor import colored
'''
Color Codes
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
LP  = '\033[36m' # light purple
GY  = '\033[37m' # gray
'''

'''
Black       0;30     Dark Gray     1;30
Blue        0;34     Light Blue    1;34
Green       0;32     Light Green   1;32
Cyan        0;36     Light Cyan    1;36
Red         0;31     Light Red     1;31
Purple      0;35     Light Purple  1;35
Brown       0;33     Yellow        1;33
Light Gray  0;37     White         1;37
'''


class Board(object):

    def __init__(self):
        self.color_dict{'x':'\033[31m','a':'\033[32m','b':'\033[33m'}
        self.piece_list =[]
        self.main_board = {}
        self.show_board = [['.' for x in range(6)] for y in range(6)]
        self.game_over = False
        self.bad_move_count = 0 #need this like a global variable
        self.current_path_dict = []
        self.moving_forward = True #set this as false while you are going back through moves

        self.load_board()
        #self.build_final_pos()#don't think I'll need this, just leaving it uncommented to run old functions
        self.print_piece_stats()
        #self.print_board()

    def load_board(self):
        with open('puzzle_layout.txt', 'r') as puzzle_read:
        #with open('puzzle_layout2.txt', 'r') as puzzle_read:

            puzzle_in = puzzle_read.read().splitlines()
        #build board
        start_pieces = {}
        for v in range(6):
            for h in range(6):
                #print(puzzle_in[v][h])
                #if finding for the first time, create dictionary value
                current_piece = puzzle_in[v][h]
                #only want to find letters
                if(current_piece != "."):
                    #initialize piece stats if it hasn't been added yet
                    if(current_piece not in start_pieces.keys()):
                        start_pieces[current_piece] = {'start_v':v, 'start_h':h,'length':1}
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
            self.main_board[piece] = Piece(piece, start_pieces[piece]['length'], start_pieces[piece]['start_v'], start_pieces[piece]['start_h'], start_pieces[piece]['direction'])

        for piece in self.piece_list:
            #print(self.main_board[piece].direction)
            #if horizontal
            if self.main_board[piece].direction == 'h':
                for i in range(self.main_board[piece].length):
                    self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h+i] = piece
                    #print("Wow_h:{}".format(show_board[self.main_board[piece].start_v][self.main_board[piece].start_h+i]))
            #vertical
            else:
                for i in range(self.main_board[piece].length):
                    self.show_board[self.main_board[piece].start_v+i][self.main_board[piece].start_h] = piece
                    #print("Wow_v:{}".format(show_board[self.main_board[piece].start_v+i][self.main_board[piece].start_h]))

    def print_piece_stats(self):
        for piece in self.piece_list:
            print("Piece:{}, Length:{}, Start_v:{}, Start_h:{}, Direction:{}".format(piece,self.main_board[piece].length,self.main_board[piece].start_v,self.main_board[piece].start_h,self.main_board[piece].direction))

    def print_board(self):
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
            print("Trying to move x")
            allowed_moves = self.check_move('x')
            print("x allowed moves: {}".format(allowed_moves))
            #final position, game over
            if self.main_board['x'].start_h == 4 and self.main_board['x'].start_v == 3:
                self.game_over = True
            #can move right, closer to final position
            elif 'Right' in allowed_moves:
                self.move_piece('x', 'Right')
                self.bad_move_count = 0
                self.print_board()

                input("Piece: {} moved: {}\nKeep searching?\n>".format('x', 'Right'))
            #can't move right, need to move blocking piece
            else:
                #need to find piece that is blocking you directly to the Right
                x_block = self.show_board[self.main_board['x'].start_v][self.main_board['x'].start_h+self.main_board['x'].length]
                #need to find location that blocking piece should be so x can move
                input("Piece currently blocking x: {} In direction: {}\nCalling Recursion\n>".format(x_block, 'Right'))
                self.move_block_recursion('x', x_block, 'Right')

    #recursion function
    #issue right now: recursion never turns back around to go forward
    def move_block_recursion(self, current_piece, blocking_piece, move_direction):

        open_coords = self.get_open_coords(current_piece, move_direction)
        v_open = open_coords['v']
        h_open = open_coords['h']
        print("Need position v:{},h:{} open for: {}".format(v_open, h_open, current_piece))

        direction_list = self.check_helpful_move(current_piece, blocking_piece)
        print("Helpful move(s) by: {}: {}".format(blocking_piece, direction_list))

        try_direction = direction_list.pop()#remove entry from direction_list so you don't try it again

        ##This top block might need to be moved into the else statement and then pass open coords(so leave v_open and h_open up here) and direction_list as parameters
        #that way I can call the recursion function again without resetting the direction_list
        #go through this loop until you can move this piece
        while self.show_board[v_open][h_open] != '.':

            input("Trying to move piece: {} in direction: {} - While loop start \nBad count: {}, Moving forward: {}\n>".format(blocking_piece, try_direction,self.bad_move_count, self.moving_forward))
            valid_move_list = self.check_move(blocking_piece)


            #swapped this one from second check to first, want to make sure it doesn't run away in a direction
            if self.bad_move_count > 20 and self.moving_forward == True:
                self.moving_forward = False
                input("Hit {} \"bad\" moves\n>".format(self.bad_move_count))

            #need to make sure you are moving forward
            elif try_direction in valid_move_list and self.moving_forward:
                self.move_piece(blocking_piece,try_direction)
                #need to append this move to list
                self.current_path_dict.append({'piece':blocking_piece, 'direction':try_direction})
                print("Current move dict: {}".format(self.current_path_dict))
                #bad_move_count = 0 #want to actually increment here
                self.bad_move_count += 1
                self.print_board()

            #moving backward and this current piece has a valid move, hoping this makes it hit the last else block and then try to go the other direction
            elif self.moving_forward == False and len(direction_list) > 0:
                self.moving_forward = True
                self.bad_move_count -= 1
                print("Direction list: {}".format(direction_list))
                print("Made it to moving forward equals false and there is another direction")

            elif self.moving_forward == False:
                #revert move and return
                undo_move = self.current_path_dict.pop()
                self.bad_move_count -= 1
                undo_piece = undo_move['piece']
                undo_direction = undo_move['direction']
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

                self.print_board()
                input("Just moved piece: {}, now going to return to previous piece\n>".format(undo_piece))
                #I might want to call recursion again, but if I do  it will reset the direction_list variable
                #return #doing the return here doesn't return you back to the previous level of the function it gets you back to the first function call


            #idea: else if moving backward and len(direction_list) is 1 meaning there is another direction you can move
            #   then: pop to get that new direction and call recursion going forward, turn moving forward back on
            #   else if moving  backward and len(direction_list) is 0 meaning ther are no more directions to try
            #   then: pop and keep moving back  (revert logic)

            else:
                print("Can't move piece: {} in direction: {}.".format(blocking_piece, try_direction))

                #if there is a wall in that direction it's a bad move, need to try other direction or go back
                new_blocking_piece = self.get_block_in_direction(blocking_piece,try_direction)
                if new_blocking_piece == None:
                    #if there is another direction to try, try it
                    if len(direction_list) > 0:
                        try_direction = direction_list.pop()
                        print("Changing direction, now trying to go: {}".format(try_direction))
                    #otherwise need to revert
                    else:
                        self.moving_forward = False
                #otherwise need to move that unblocking piece
                else:
                    print("Piece currently blocking: {} is: {} in direction: {}".format(blocking_piece, new_blocking_piece, try_direction))
                    self.move_block_recursion(blocking_piece, new_blocking_piece, try_direction)
        print("Leaving while loop, successfully moved: {} out of the way of: {}".format(blocking_piece, current_piece))
        #addded this return, not sure if it is necessary
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
    #need to add logic to prefer a direction that is closer when there are two directions that it can move
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
        #once list is empty it will exit
        while current_path_moves:
            current_move = current_path_moves.pop()
            if current_move['direction'] == 'Left':
                print("Reverting piece: {}Bad moves left to undo: {}".format(current_move['piece'],len(current_path_moves)))
                self.move_piece(current_move['piece'], 'Right')#opposite direction
                self.print_board()
                input("Keep searching?\n>")
            elif current_move['direction'] == 'Right':
                print("Reverting piece: {}Bad moves left to undo: {}".format(current_move['piece'],len(current_path_moves)))
                self.move_piece(current_move['piece'], 'Left')#opposite direction
                self.print_board()
                input("Keep searching?\n>")
            elif current_move['direction'] == 'Up':
                print("Reverting piece: {}Bad moves left to undo: {}".format(current_move['piece'],len(current_path_moves)))
                self.move_piece(current_move['piece'], 'Down')#opposite direction
                self.print_board()
                input("Keep searching?\n>")
            elif current_move['direction'] == 'Down':
                print("Reverting piece: {}Bad moves left to undo: {}".format(current_move['piece'],len(current_path_moves)))
                self.move_piece(current_move['piece'], 'Up')#opposite direction
                self.print_board()
                input("Keep searching?\n>")
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

    def __init__(self,char, length, start_v, start_h, direction):
        #char is pictoral representation on the board
        self.char = char
        #length is how long the piece is
        self.length = length
        #start coordinates
        self.start_v = start_v
        self.start_h = start_h
        #direction piece is facing
        self.direction = direction
        #final coordinates for vertical pieces that could be in the way of x

def piece_test():
    piece_list = []
    for i in range(10):
        piece_list.append(Piece('a', 2, i, 'v'))
        print(piece_list[i].start)

if __name__== "__main__":
    #piece_test()
    my_board = Board()
    #my_board.show_valid_moves()
    my_board.move_x_block()
