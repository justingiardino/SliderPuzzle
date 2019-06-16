my_dict = {}
my_dict['a'] = {}
my_dict['a']['b'] = '>'
print(my_dict)


# my_list = [{'v':1, 'h':2}]
# my_list.append({'v':2, 'h':3})
#
# print(my_list)
#
# if {'v':1, 'h':2} in my_list:
#     print("Valid")
# else:
#     print("Invalid")


# #
# # for i in range(10):
# #     print(i)
# #     if i > 5:
# #         break
# #
# #
# # direction_list = [[1,0], [-1,0], [0,1], [0, -1]]
# #
# # for v,h in direction_list:
# #
# #     print("V: {}, H: {}".format(v,h))
# # with open('maze_layout.txt', 'r') as maze_read:
# #     maze_in = maze_read.read().splitlines()
# #
# # main_maze = []
# # for line in maze_in:
# #     main_maze.append(list(line))
# #
# # print(main_maze)
#
#
# # found_dict = {}
# # for v in range(6):
# #     found_dict[v] = {}
# #     for h in range(6):
# #         found_dict[v][h] = {'found':['']}
# #
# # found_dict[1][2]['found'].append('Up')
# # found_dict[1][2]['found'].append('Down')
# #
# # found_dict[1][2]['found'] = ['']
# #
# #
# #
# #
# # for v in range(6):
# #     for h in range(6):
# #         if 'Down' in found_dict[v][h]['found']:
# #             print("Down found at v:{}, h:{}".format(v,h))
# #         if 'Up' in found_dict[v][h]['found']:
# #                 print("Up found at v:{}, h:{}".format(v,h))
#
# # my_list = ['']
# # if 'Right' in my_list:
# #     print('Found right')
# # else:
# #     print('Not found')
# # my_list = []
# # my_list.append({'c':'Right'})
# # my_list.append({'a':'Left'})
# # print(len(my_list))
# #
# # k = my_list.pop()
# # #this works in spyder but not in anaconda command line
# # print('\033[0;31m dark, \033[1;31m light.\033[0m')
# # print('Checking to make sure color was reset')
# # print(my_list.pop())
# # if len(my_list) > 0:
# #     print(my_list.pop())
# # else:
# #     print("list empty")
# #
# # for i in range(1,5):
# #     print(i)
# #     if i == 3:
# #         break
#
# #
# # list1 = []
# # list2 = []
# # list2.append([])
# # list3 = ['Right']
# # print(list1)
# # print(list2)
#
#
# my_dict = [{'piece': 'a', 'direction': 'Up', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'x', 'direction': 'Right', 'blocked_piece': '', 'alt_direction': 'None'},
# {'piece': 'f', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
# {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
# {'piece': 'f', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'x', 'direction': 'Right', 'blocked_piece': '', 'alt_direction': 'None'},
# {'piece': 'g', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'x', 'direction': 'Left', 'blocked_piece': 'f', 'alt_direction': 'None'},
# {'piece': 'f', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
# {'piece': 'g', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'g', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
# {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
# {'piece': 'f', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'x', 'direction': 'Right', 'blocked_piece': '', 'alt_direction': 'None'},
# {'piece': 'x', 'direction': 'Left', 'blocked_piece': 'f', 'alt_direction': 'None'},
# {'piece': 'f', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
# {'piece': 'g', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'g', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
# {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
# {'piece': 'f', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'x', 'direction': 'Right', 'blocked_piece': '', 'alt_direction': 'None'},
# {'piece': 'x', 'direction': 'Left', 'blocked_piece': 'f', 'alt_direction': 'None'},
# {'piece': 'f', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
# {'piece': 'g', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
# {'piece': 'g', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
# {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'}]
#
# last_x = 0
# last_count = 0
# for dict in my_dict:
#     if dict['piece'] == 'x' and dict['direction'] == 'Right':
#         last_x = last_count
#     last_count += 1
# print("Index of last x: {}".format(last_x))
# print("Move for last x: {}".format(my_dict[last_x]))
#
# print(len(my_dict))
#
#
#
# [{'piece': 'a', 'direction': 'Up', 'blocked_piece': 'x', 'alt_direction': 'None'},
#  {'piece': 'x', 'direction': 'Right', 'blocked_piece': '', 'alt_direction': 'None'},
#  {'piece': 'f', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
#  {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
#  {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
#  {'piece': 'f', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
#  {'piece': 'x', 'direction': 'Right', 'blocked_piece': '', 'alt_direction': 'None'},
#  {'piece': 'g', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
#  {'piece': 'x', 'direction': 'Left', 'blocked_piece': 'f', 'alt_direction': 'None'},
#  {'piece': 'f', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
#  {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
#  {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
#  {'piece': 'g', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
#  {'piece': 'g', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
#  {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
#  {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
#  {'piece': 'f', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
#  {'piece': 'x', 'direction': 'Right', 'blocked_piece': '', 'alt_direction': 'None'},
#  {'piece': 'x', 'direction': 'Left', 'blocked_piece': 'f', 'alt_direction': 'None'},
#  {'piece': 'f', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
#  {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
#  {'piece': 'e', 'direction': 'Left', 'blocked_piece': 'g', 'alt_direction': 'None'},
#  {'piece': 'g', 'direction': 'Down', 'blocked_piece': 'x', 'alt_direction': 'None'},
#  {'piece': 'g', 'direction': 'Up', 'blocked_piece': 'e', 'alt_direction': 'None'},
#  {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'},
#  {'piece': 'e', 'direction': 'Right', 'blocked_piece': 'f', 'alt_direction': 'Left'}]
