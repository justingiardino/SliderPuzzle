

class Board(object):

    def __init__(self):
        self.piece_list =[]
        self.main_board = {}
        self.show_board = [['.' for x in range(6)] for y in range(6)]
        self.game_over = False
        self.bad_moves = 0 #need this like a global variable
        self.current_path_moves = []

        self.load_board()
        self.get_pieces_in_path()
        self.build_final_pos()#don't think I'll need this, just leaving it uncommented to run old functions
        self.print_piece_stats()
        self.print_board()


    def load_board(self):
        with open('puzzle_layout.txt', 'r') as puzzle_read:
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
            print("Piece:{}, Length:{}, Start_v:{}, Start_h:{}, Direction:{}\nIn_path:{}, final_v: {}".format(piece,self.main_board[piece].length,self.main_board[piece].start_v,self.main_board[piece].start_h,self.main_board[piece].direction,self.main_board[piece].in_path, self.main_board[piece].final_v))

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

    #maybe need an undo move?
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


    def move_x_block(self):
        self.print_board()
        while not self.game_over:
            print("Trying to move x")
            allowed_moves = self.check_move('x')
            print("\'x\' allowed moves: {}".format(allowed_moves))
            #final position, game over
            if self.main_board['x'].start_h == 4 and self.main_board['x'].start_v == 3:
                self.game_over = True
            #can move right, closer to final position
            elif 'Right' in allowed_moves:
                self.move_piece('x', 'Right')
                self.print_board()

                input("Piece: {} moved: {}\nKeep searching?\n>".format('x', 'Right'))
            #can't move right, need to move blocking piece
            else:
                #x_blocks = self.main_board['x'].in_path['Right']
                #need to find piece that is blocking you directly to the Right
                x_block = self.show_board[self.main_board['x'].start_v][self.main_board['x'].start_h+self.main_board['x'].length]
                #need to find location that blocking piece should be so x can move
                input("Piece currently blocking x: {} In direction: {}\nCalling Recursion\n>".format(x_block, 'Right'))
                self.move_block('x', x_block, 'Right')


    def get_open_coords(self, current_piece, needed_direction):
        print("Checking what coordinates need to be open")
        if needed_direction == 'Left':
            return {'v':self.main_board[current_piece].start_v, 'h':self.main_board[current_piece].start_h-1}
        elif needed_direction == 'Right':
            return {'v':self.main_board[current_piece].start_v, 'h':self.main_board[current_piece].start_h+self.main_board[current_piece].length}
        elif needed_direction == 'Up':
            return {'v':self.main_board[current_piece].start_v-1, 'h':self.main_board[current_piece].start_h}
        elif needed_direction == 'Down':
            return {'v':self.main_board[current_piece].start_v+self.main_board[current_piece].length, 'h':self.main_board[current_piece].start_h}
        else:
            print("Get open coords went wrong..")
            return


    #recursion function
    def move_block(self, current_piece, blocking_piece, move_direction):
        open_coords = self.get_open_coords(current_piece, move_direction)
        v_open = open_coords['v']
        h_open = open_coords['h']
        print("Need position v:{},h:{} open for: {}".format(v_open, h_open, current_piece))

        if self.main_board[blocking_piece].direction == 'v':
            direction_list = ['Up', 'Down']
        else:
            direction_list = ['Left', 'Right']

        try_direction = direction_list.pop()#remove entry from direction_list so you don't try it again

        #go through this loop until you can move this piece
        while self.show_board[v_open][h_open] != '.':
            input("Start of while loop\n>")



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



    def move_x_block_old(self):
        #self.main_board[piece].in_path
        #only grabbing right for now
        x_blocks = self.main_board['x'].in_path['Right']
        if x_blocks != []:
            for block_piece in x_blocks:
                #need a while loop until this block piece is out of x's way
                #final_v could be a list
                while self.main_board[block_piece].start_v not in self.main_board[block_piece].final_v:
                    print("Moving piece: \'{}\' out of the way.".format(block_piece))
                    #need to pass prefferred direction
                    #always try to move piece down first - #why?
                    self.move_main(block_piece, 'Down')
                    if self.main_board[block_piece].length == 2:
                        self.move_main(block_piece, 'Up')



    #probably going to have to combine move_main and check_blocking_piece into one function, where it has current piece, piece blocking it, and preferred direction
    #should I use arrows to show where pieces have been in case I need to go back?

    #pass in a preferred direction variable
    def move_main(self,piece,preferred_direction):
        print("**\nmove_main->piece:{}\n**".format(piece))
        #if you can move the piece, move it
        allowed_moves = self.check_move(piece)
        if allowed_moves:
            #only need if preferred_move is in allowed_moves
            if preferred_direction in allowed_moves:
                print("Piece: {}, Direction(s) it can move, preferring to go {}: {}".format(piece,preferred_direction,allowed_moves))


                if preferred_direction == 'Down':
                    #set current pixel to .
                    print("Moving down")
                    self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h] = '.'
                    #update pixel below
                    self.show_board[self.main_board[piece].start_v+self.main_board[piece].length][self.main_board[piece].start_h] = piece
                    #update start point
                    self.main_board[piece].start_v += 1
                    self.print_board()
                    input("Keep searching?\n>")



                elif preferred_direction == 'Up':

                    print("Moving Up")
                    #update start point
                    self.main_board[piece].start_v -= 1
                    #set new top to current letter
                    self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h] = piece
                    #set bottom pixel to .
                    self.show_board[self.main_board[piece].start_v+self.main_board[piece].length][self.main_board[piece].start_h] = '.'
                    self.print_board()
                    input("Keep searching?\n>")


                elif preferred_direction == 'Left':
                    print("Moving Left")
                    self.main_board[piece].start_h -= 1
                    #set new left to current letter
                    self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h] = piece
                    #set old right pixel to .
                    self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h+self.main_board[piece].length] = '.'
                    self.print_board()
                    input("Keep searching?\n>")


                elif preferred_direction == 'Right':
                    print("Moving Right")
                    #Set current pixel to .
                    self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h] = '.'
                    #update pixel to the right
                    self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h+self.main_board[piece].length] = piece
                    #update start point
                    self.main_board[piece].start_h += 1
                    self.print_board()
                    input("Keep searching?\n>")


                else:
                    print("Not good - bad move.")

                    #reset in path count
                    self.get_pieces_in_path()
            else:
                print("Could not move {}, need to move: {} out of the way".format(preferred_direction,self.main_board[piece].in_path[preferred_direction]))
                #loop through this blocking path to try and move it
                for blocking_piece in self.main_board[piece].in_path[preferred_direction]:
                    self.check_blocking_piece(piece, blocking_piece)


        #else no allowed moves, need to move something blocking it
        else:
            print("Made it to else statement for piece:{}".format(piece))
            for blocking_piece in self.main_board[piece].in_path[preferred_direction]:
                self.check_blocking_piece(piece,blocking_piece)

        print("**End of move_main block\nPiece: {} is bocked".format(piece))
        self.print_board()
        input("Keep searching?\n>")

        return

    def check_blocking_piece(self, local_current_piece, local_blocking_piece):
        #vertical
        if self.main_board[local_blocking_piece].direction == 'v':
            #see if you are at lower bound

            if (self.main_board[local_blocking_piece].start_v + self.main_board[local_blocking_piece].length) < 6:
                self.move_main(local_blocking_piece, 'Down')
            #see if you are at upper bound
            print('should be back from return')
            if (self.main_board[local_blocking_piece].start_v - 1) > -1:
                self.move_main(local_blocking_piece, 'Up')
        #horizontal
        else:
            #this logic will need to be cleaned up
            #will need to have some way of keeping track of back tracking
            #if it is 3 length piece you want to move to the other side of the piece that is blocked
            if self.main_board[local_blocking_piece].length == 3:
                #if the blocked piece starts at h < 3 it is on the left side in the 3 piece needs to move right
                if self.main_board[local_current_piece].start_h < 3:
                    self.move_main(local_blocking_piece, 'Right')
                #else it is on the right side if it is length 3 and needs to go all the way left
                else:
                    self.move_main(local_blocking_piece, 'Right')


            #if it is 2 length piece you want to try left and right


            #see if you are at right bound
            if (self.main_board[local_blocking_piece].start_h + self.main_board[local_blocking_piece].length) < 6:
                self.move_main(local_blocking_piece, 'Right')
            #when I return it comes to here
            #see if you are at left bound
            if (self.main_board[local_blocking_piece].start_h - 1) > -1:
                self.move_main(local_blocking_piece, 'Left')

    def game_play_computer(self):

        while not self.game_over:
            self.print_board
            self.move_x_block_old()

    def get_pieces_in_path(self):
        for piece in self.piece_list:
            #reset dictionary
            self.main_board[piece].in_path.clear()
            #check vertical
            if self.main_board[piece].direction == 'v':
                for v in range(6):
                    #store for easier reading
                    current_letter = self.show_board[v][self.main_board[piece].start_h]
                    #if an actual piece is in your way
                    if current_letter != piece and current_letter != '.':
                        #if letter hasn't already been added
                        if current_letter not in self.main_board[piece].in_path:
                            #if below piece
                            if v > self.main_board[piece].start_v:
                                if 'Down' in self.main_board[piece].in_path.keys():
                                    self.main_board[piece].in_path['Down'].append(current_letter)
                                #else create direction
                                else:
                                    self.main_board[piece].in_path['Down'] = [current_letter]

                            #else above
                            else:
                                if 'Up' in self.main_board[piece].in_path.keys():
                                    self.main_board[piece].in_path['Up'].append(current_letter)
                                #else create direction
                                else:
                                    self.main_board[piece].in_path['Up'] = [current_letter]
            #check horizontal
            else:
                for h in range(6):
                    #store for easier reading
                    current_letter = self.show_board[self.main_board[piece].start_v][h]
                    #if an actual piece is in your way
                    if current_letter != piece and current_letter != '.':
                        #if letter hasn't already been added
                        if current_letter not in self.main_board[piece].in_path:
                            #if to the right of the piece
                            if h > self.main_board[piece].start_h:
                                #if direction has already been added
                                if 'Right' in self.main_board[piece].in_path.keys():
                                    self.main_board[piece].in_path['Right'].append(current_letter)
                                #else create direction
                                else:
                                    self.main_board[piece].in_path['Right'] = [current_letter]

                            #else to the left
                            else:
                                if 'Left' in self.main_board[piece].in_path.keys():
                                    self.main_board[piece].in_path['Left'].append(current_letter)
                                #else create direction
                                else:
                                    self.main_board[piece].in_path['Left'] = [current_letter]
                                #self.main_board[piece].in_path['Left'] =  current_letter

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
            if (self.main_board[piece].start_v + self.main_board[piece].length) < 5:
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
            if (self.main_board[piece].start_h + self.main_board[piece].length) < 5:
                #store for easier reading
                current_letter = self.show_board[self.main_board[piece].start_v][self.main_board[piece].start_h + self.main_board[piece].length]
                if current_letter == '.':
                    move_list.append('Right')

        return move_list

    def show_valid_moves(self):
        for piece in self.piece_list:
            print("Move list for {} : {}".format(piece, self.check_move(piece)))

    def build_final_pos(self):

        for piece in self.piece_list:
            if self.main_board[piece].direction == 'v':
                #only one place to go for 3 long
                if self.main_board[piece].length == 3:
                    self.main_board[piece].final_v.append(3)
                #three places to go for 2 long, not as important
                else:
                    self.main_board[piece].final_v.append(0)
                    self.main_board[piece].final_v.append(3)
                    self.main_board[piece].final_v.append(4)




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
        #used for list of pieces that are in it's path
        self.in_path = {}
        #final coordinates for vertical pieces that could be in the way of x
        self.final_v = []

def piece_test():
    piece_list = []
    for i in range(10):
        piece_list.append(Piece('a', 2, i, 'v'))
        print(piece_list[i].start)

if __name__== "__main__":
    #piece_test()
    my_board = Board()
    #my_board.show_valid_moves()
    #my_board.game_play_computer()
    my_board.move_x_block()




""" Old user functions
    def move_piece_user(self):

        piece_in = 'z'
        while piece_in not in self.piece_list:
            piece_in = input("What piece would you like to move?\n>")

        valid_move = []
        for current_v in range(6):
            for current_h in range(6):
                if self.show_board[current_v][current_h] == piece_in:
                    if self.main_board[piece_in].direction == 'h':
                        #check boundaries and check pieces to left and right
                        #print(current_h)
                        if(current_h != 0) and (self.show_board[current_v][current_h-1] == '.'):
                            valid_move.append('Left')
                        if(current_h != 5) and (self.show_board[current_v][current_h+1] == '.'):
                            valid_move.append('Right')

                    #vertical
                    else:
                        if(current_v != 0) and (self.show_board[current_v-1][current_h] == '.'):
                            valid_move.append('Up')
                        if(current_v != 5) and (self.show_board[current_v+1][current_h] == '.'):
                            valid_move.append('Down')


        valid_move.append('Cancel')

        move_in = 'Init'
        while move_in not in valid_move:
            move_in = input("Valid moves:{}\nWhat direction would you like to move?\n>".format(valid_move))

        if move_in == 'Left':
            # self.show_board[]
            self.main_board[piece_in].start_h -= 1
            for i in range(self.main_board[piece_in].length):
                self.show_board[self.main_board[piece_in].start_v][self.main_board[piece_in].start_h+i] = piece_in
            #set last index back to .
            self.show_board[self.main_board[piece_in].start_v][self.main_board[piece_in].start_h+self.main_board[piece_in].length] = '.'

        elif move_in == 'Right':

            #set first index back to .
            self.show_board[self.main_board[piece_in].start_v][self.main_board[piece_in].start_h] = '.'
            self.main_board[piece_in].start_h += 1
            for i in range(self.main_board[piece_in].length):
                self.show_board[self.main_board[piece_in].start_v][self.main_board[piece_in].start_h+i] = piece_in

        elif move_in == 'Up':
            self.main_board[piece_in].start_v -= 1
            for i in range(self.main_board[piece_in].length):
                self.show_board[self.main_board[piece_in].start_v+i][self.main_board[piece_in].start_h] = piece_in
            #set last index back to .
            self.show_board[self.main_board[piece_in].start_v+self.main_board[piece_in].length][self.main_board[piece_in].start_h] = '.'

        elif move_in == 'Down':
            #set first index back to .
            self.show_board[self.main_board[piece_in].start_v][self.main_board[piece_in].start_h] = '.'
            self.main_board[piece_in].start_v += 1
            for i in range(self.main_board[piece_in].length):
                self.show_board[self.main_board[piece_in].start_v+i][self.main_board[piece_in].start_h] = piece_in
        else:
            print("Cancelling move")

        #game over check, this means it is at the exit point
        if self.main_board[piece_in].start_v == 2 and self.main_board[piece_in].start_h == 4:
            self.game_over = True


    def game_play_user(self):

        while not self.game_over:
            self.move_piece_user()
            self.print_board()
        print("Game over, you win!")
"""
