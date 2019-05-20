

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

my_list = ['Test']
for item in my_list:
    print(item)
