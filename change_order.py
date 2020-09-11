import os
def change_order_by_order_list(order_list):
  path = "./result"
  dirs = os.listdir(path)
  dirs_path_list = []
  for i in range(len(dirs)):
    dirs_path_list.append(os.path.join(path, dirs[i]))
  if './result/.DS_Store' in dirs_path_list:
    dirs_path_list = dirs_path_list[1:]
  # print(dirs_path_list)
  for i in range(len(dirs_path_list)):
    with open(dirs_path_list[i], 'r') as f:
      output_list = []
      while True:
        line = f.readline().strip()
        if line =='$' * 50: break
        output_list .append(line)
      Bio_section_index = output_list.index("$Bio section$")
      Experience_index = output_list.index("$Experience$")
      Education_index = output_list.index("$Education$")
      order_dict = {"bio" : Bio_section_index, "exp" : Experience_index, "edu" : Education_index}
      order_tuple_list = sorted(order_dict.items() ,key = lambda x: x[1])
      #建立當前對應list
      Bio_section_list = []
      Experience_list = []
      Education_list = []
      for j in range(len(order_tuple_list)):
        First_part = output_list[order_tuple_list[0][1]:order_tuple_list[1][1]]
        Second_part = output_list[order_tuple_list[1][1]:order_tuple_list[2][1]]
        Third_part = output_list[order_tuple_list[2][1]:]
        if order_tuple_list[j][0] == "exp":
          if j == 0:
            Experience_list = First_part
          elif j == 1:
            Experience_list = Second_part
          elif j == 2:
            Experience_list = Third_part
        elif order_tuple_list[j][0] == "edu":
          if j == 0:
            Education_list = First_part
          elif j == 1:
            Education_list = Second_part
          elif j == 2:
            Education_list = Third_part
        elif order_tuple_list[j][0] == "bio":
          if j == 0:
            Bio_section_list = First_part
          elif j == 1:
            Bio_section_list = Second_part
          elif j == 2:
            Bio_section_list = Third_part
      #建立新的順序list
      New_list = []
      for j in range(len(order_list)):
        if order_list[j] == "bio":
          New_list +=  Bio_section_list
        elif order_list[j] == "edu":
          New_list += Education_list
        elif order_list[j] == "exp":
          New_list += Experience_list
      # print(Bio_section_list)
      # print(Experience_list)
      # print(Education_list)
      write_new_list(New_list, dirs_path_list[i])
      # print(New_list)
      # Experience_list = output_list[order_tuple_list[]]

      # print(order_tuple_list)

def write_new_list(New_list, path):
  # path = path[:-4] + "_new.txt"
  f_w = open(path, 'w')
  for i in range(len(New_list)):
    if New_list[i] == "$Bio section$":
      New_list[i] = " " * ((50 - len("$Bio section$")) // 2) + "$Bio section$"
    elif New_list[i] == "$Experience$":
      New_list[i] = " " * ((50 - len("$Experience$")) // 2) + "$Experience$"
    elif New_list[i] == "$Education$":
      New_list[i] = " " * ((50 - len("$Education$")) // 2) + "$Education$"
    f_w.write(New_list[i])
    f_w.write('\n')
  f_w.write('$' * 50)
  f_w.close()

if __name__ == '__main__':
  change_order_by_order_list(["bio", "exp", "edu"])

