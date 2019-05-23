

# with open('maze_layout.txt', 'r') as maze_read:
#     maze_in = maze_read.read().splitlines()
#
# main_maze = []
# for line in maze_in:
#     main_maze.append(list(line))
#
# print(main_maze)


# found_dict = {}
# for v in range(6):
#     found_dict[v] = {}
#     for h in range(6):
#         found_dict[v][h] = {'found':['']}
#
# found_dict[1][2]['found'].append('Up')
# found_dict[1][2]['found'].append('Down')
#
# found_dict[1][2]['found'] = ['']
#
#
#
#
# for v in range(6):
#     for h in range(6):
#         if 'Down' in found_dict[v][h]['found']:
#             print("Down found at v:{}, h:{}".format(v,h))
#         if 'Up' in found_dict[v][h]['found']:
#                 print("Up found at v:{}, h:{}".format(v,h))

# my_list = ['']
# if 'Right' in my_list:
#     print('Found right')
# else:
#     print('Not found')
my_list = []
my_list.append({'c':'Right'})
my_list.append({'a':'Left'})
print(len(my_list))

k = my_list.pop()
#this works in spyder but not in anaconda command line
print('\033[0;31m dark, \033[1;31m light.\033[0m')
print('Checking to make sure color was reset')
print(my_list.pop())
if len(my_list) > 0:
    print(my_list.pop())
else:
    print("list empty")

for i in range(1,5):
    print(i)
    if i == 3:
        break
