

class Board(object):

    def __init__(self):
        self.piece_list =[]
        self.main_board = {}
        self.show_board = [['.' for x in range(6)] for y in range(6)]
        self.game_over = False

        self.build_board()
        self.print_piece_stats()
        self.print_board()
        self.game_play()


    def build_board(self):
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
            print("Piece:{}, Length:{}, Start_v:{}, Start_h:{},Direction:{}".format(piece,self.main_board[piece].length,self.main_board[piece].start_v,self.main_board[piece].start_h,self.main_board[piece].direction))

    def print_board(self):
        print("  0 1 2 3 4 5 ",end='')
        for v in range(6):
            print("\n{} ".format(v),end='')
            for h in range(6):
                print("{} ".format(self.show_board[v][h]),end='')
        print('\n')

    def move_piece(self):

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

    def game_play(self):

        while not self.game_over:
            self.move_piece()
            self.print_board()
        print("Game over, you win!")









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

def piece_test():
    piece_list = []
    for i in range(10):
        piece_list.append(Piece('a', 2, i, 'v'))
        print(piece_list[i].start)

if __name__== "__main__":
    #piece_test()
    my_board = Board()
