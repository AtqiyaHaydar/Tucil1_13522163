# Nama : Atqiya Haydar Luqman
# NIM : 13522163
# Kelas : K3

import time
import pyfiglet
from colorama import Fore, Style

from Randomize import randomize

def read_data_from_file(filename):
  with open(filename, 'r') as file:
    lines = file.readlines()
    buffer_size = int(lines[0])
    matrix_width, matrix_height = map(int, lines[1].split())
    matrix = [line.split() for line in lines[2:2+matrix_height]]
    number_of_sequence = int(lines[2+matrix_height])
    sequences_and_rewards = {}
    for i in range(number_of_sequence):
      sequence = lines[3+matrix_height+i*2].split()
      reward = int(lines[4+matrix_height+i*2])
      sequences_and_rewards[" ".join(sequence)] = reward
    
    return buffer_size, matrix_width, matrix_height, matrix, sequences_and_rewards

def search_horizontal(token, i, j, matrix, matrix_width):
    for col in range(matrix_width):
        if matrix[i][col] == token:
            return True, (i, col)
    return False, (i, j)

def search_vertical(token, i, j, matrix, matrix_height):
    for row in range(matrix_height):
        if matrix[row][j] == token:
            return True, (row, j)
            
    return False, (i, j)

def search_sequence(init, i, j, sequence, matrix, matrix_height, matrix_width):
  token_added = sequence[0].split()
  reward = sequence[1]
  coordinates_added = []
  buffer_added = len(sequence[0].split())
  found_sequence = True

  if init < 2: # Pencarian pertama
    length = range(len(sequence[0].split()))
  else: # Pencarian kedua dan seterusnya
    length = range(2, len(sequence[0].split()))

  if init % 2 != 0: # Init ganjil mencari horizontal
    for t in length:
      if t % 2 != 0:

        if init > 1:
          found, new_row_index = search_vertical(sequence[0].split()[t], i, j, matrix, matrix_height)
          if found: i = new_row_index[0]
        else:
          found, new_row_index = search_horizontal(sequence[0].split()[t], i, j, matrix, matrix_width)
          if found: j = new_row_index[1]

        if found:
          # i = new_row_index[0]
          # j = new_row_index[1]
          coordinates_added.append((i, j))
          continue
        else:
          found_sequence = False
          break

      elif t % 2 == 0:

        if init > 1:
          found, new_col_index = search_horizontal(sequence[0].split()[t], i, j, matrix, matrix_width)
          if found: j = new_col_index[1]
        else:
          found, new_col_index = search_vertical(sequence[0].split()[t], i, j, matrix, matrix_height)
          if found: i = new_col_index[0]

        if found:
          # i = new_col_index[0]
          # j = new_col_index[1]
          coordinates_added.append((i, j))
          continue
        else:
          found_sequence = False
          break

  elif init % 2 == 0: # Init genap mencari vertikal
    for t in length:
      if t % 2 != 0:
        
        if init > 1:
          found, new_col_index = search_horizontal(sequence[0].split()[t], i, j, matrix, matrix_width)
          if found: j = new_col_index[1]
        else:
          found, new_col_index = search_vertical(sequence[0].split()[t], i, j, matrix, matrix_height)
          if found: i = new_col_index[0]

        if found:
          # i = new_col_index[0]
          # j = new_col_index[1]
          coordinates_added.append((i, j))
          continue
        else:
          found_sequence = False
          break
      
      elif t % 2 == 0:
        
        if init > 1:
          found, new_row_index = search_vertical(sequence[0].split()[t], i, j, matrix, matrix_height)
          if found: i = new_row_index[0]
        else:
          found, new_row_index = search_horizontal(sequence[0].split()[t], i, j, matrix, matrix_width)
          if found: j = new_row_index[1]

        if found:
          # i = new_row_index[0]
          # j = new_row_index[1]
          coordinates_added.append((i, j))
          continue
        else:
          found_sequence = False
          break

  if found_sequence:
    found = True
    new_i = i
    new_j = j
    return found, token_added, reward, coordinates_added, buffer_added, new_i, new_j
  else:
    found = False
    return found, [], 0, [], 0, i, j

def find_maximum_reward(buffer_size, matrix_width, matrix_height, matrix, sorted_sequences):
  max_buffer = ""
  coordinates = []
  max_reward = 0
  execution_time = 0
  start_time = time.time()
  init = 0
  i, j = 0, 0

  while init < buffer_size:
    print("\nInit:", init)
    found = False

    if init == 0: # Mencari titik mulai secara perkolom kemudian perbaris
      start_sequence = sorted_sequences[0][0].split()[0]
      start_point = (0,0)
      for j in range(matrix_width):
        found = False
        for i in range(matrix_height):
          if matrix[i][j] == start_sequence: # Mencari token pertama dari sequence dengan reward tertinggi
            start_point = (0, j)
            max_buffer += matrix[0][j]
            coordinates.append((0, j))
            found = True
            break
        if found:
          break
      
      print("Start Point:", start_point)
      print("Token pertama: ", matrix[start_point[0]][start_point[1]])
      print("Reward mula-mula: ", max_reward)
      
      i = start_point[0]
      j = start_point[1]

    else: 
      if init < 2: # Pencarian pertama

        # Init ganjil, mencari secara vertikal
        if init % 2 != 0: 
          print("Mencari secara vertikal")
          for row in range(0, matrix_height):
            if row == i:
              continue
            else:
              print("\n>> Token yang dicheck:", matrix[row][j], "pada koordinat", (row, j))
              found = False
              for seq_in_row in range(len(sorted_sequences)): # Sequence dicheck secara bergiliran
                print("Sequence yang dicheck:", sorted_sequences[seq_in_row][0])

                if init < 2 and matrix[row][j] == sorted_sequences[seq_in_row][0].split()[0]:
                  found, token_added, reward, coordinates_added, buffer_added, new_i, new_j = search_sequence(init, row, j, sorted_sequences[seq_in_row], matrix, matrix_height, matrix_width)
              
                  if found:
                    coordinates.append((row, j))
                    i = new_i
                    j = new_j

                    for m in range(buffer_added):
                      max_buffer += " " + token_added[m]
                    for n in range(len(coordinates_added)):
                      coordinates.append(coordinates_added[n])

                    max_reward += reward
                    init += (buffer_added - 1)
                    break
                  else:
                    continue
              
            if found:
              print("Sequence berhasil ditemukan!")
              print("Mendapatkan reward:", sorted_sequences[seq_in_row][1])
              print("Koordinat token saat ini:", (i, j))
              print("Token saat ini:", matrix[i][j])
              break
            else:
              print("Sequence tidak ada yang cocok, pencarian token selanjutnya..")

        # Init genap, mencari secara horizontal
        else: 
          print("Mencari secara horizontal")
          for col in range(0, matrix_width):
            if col == j:
              continue
            else:
              print("\n>> Token yang dicheck:", matrix[i][col], "pada koordinat", (i, col))
              found = False
              for seq_in_col in range(len(sorted_sequences)): # Sequence dicheck secara bergiliran
                print("Sequence yang dicheck:", sorted_sequences[seq_in_col][0])
                
                if init < 2 and matrix[i][col] == sorted_sequences[seq_in_col][0].split()[0]:
                  found, token_added, reward, coordinates_added, buffer_added, new_i, new_j = search_sequence(init, i, col, sorted_sequences[seq_in_row], matrix, matrix_height, matrix_width)

                  if found:
                    coordinates.append((i, col))
                    i = new_i
                    j = new_j

                    for m in range(token_added):
                      max_buffer += " " + token_added[m]
                    for n in range(len(coordinates_added)):
                      coordinates.append(coordinates_added[n])

                    max_reward += reward
                    init += (buffer_added - 1)
                    break
                  else:
                    continue
            
            if found:
              print("Sequence berhasil ditemukan!")
              print("Mendapatkan reward:", sorted_sequences[seq_in_col][1])
              print("Koordinat token saat ini:", (i, j))
              print("Token saat ini:", matrix[i][j])
              break
            else:
              print("Sequence tidak ada yang cocok, pencarian token selanjutnya..\n")

      else: # Pencarian kedua dan seterusnya
        
        for seq in range(len(sorted_sequences)):
          # Init ganjil, mencari secara vertikal
          if init % 2 != 0: 
            print("Mencari secara vertikal")
            for row in range(0, matrix_height):
              if row == i:
                continue
              elif matrix[row][j] == sorted_sequences[seq][0].split()[0]:
                print("\n>> Token yang dicheck:", matrix[row][j], "pada koordinat", (row, j))
                print("Sequence yang dicheck:", sorted_sequences[seq][0])

                found, token_added, reward, coordinates_added, buffer_added, new_i, new_j = search_sequence(init, row, j, sorted_sequences[seq], matrix, matrix_height, matrix_width)

                if found:
                  coordinates.append((row, j))
                  i = new_i
                  j = new_j

                  for m in range(1, buffer_added):
                    max_buffer += " " + token_added[m]
                  for n in range(1, len(coordinates_added)):
                    coordinates.append(coordinates_added[n])

                  max_reward += reward
                  init += (buffer_added - 1)
                  break
                else:
                  continue
            
            if found:
              print("Sequence berhasil ditemukan!")
              print("Mendapatkan reward:", sorted_sequences[seq][1])
              print("Koordinat token saat ini:", (i, j))
              print("Token saat ini:", matrix[i][j])
              break
            else:
              print("Sequence tidak ada yang cocok, pencarian token selanjutnya..\n")
          
          if found: break

          # Init genap, mencari secara horizontal
          elif init % 2 == 0:
            print("Mencari secara horizontal")
            for col in range(0, matrix_width):
              if col == j:
                continue
              elif matrix[i][col] == sorted_sequences[seq][0].split()[1]:
                print("\n>> Token yang dicheck:", matrix[i][col], "pada koordinat", (i, col))
                print("Sequence yang dicheck:", sorted_sequences[seq][0])

                found, token_added, reward, coordinates_added, buffer_added, new_i, new_j = search_sequence(init, i, col, sorted_sequences[seq], matrix, matrix_height, matrix_width)

                if found:
                  coordinates.append((i, col))
                  i = new_i
                  j = new_j

                  for m in range(1, buffer_added):
                    max_buffer += " " + token_added[m]
                  for n in range(1, len(coordinates_added)):
                    coordinates.append(coordinates_added[n])

                  max_reward += reward
                  init += (buffer_added - 1)
                  break
                else:
                  continue
            
            if found:
              print("Sequence berhasil ditemukan!")
              print("Mendapatkan reward:", sorted_sequences[seq][1])
              print("Koordinat token saat ini:", (i, j))
              print("Token saat ini:", matrix[i][j])
              break
            else:
              print("Sequence tidak ada yang cocok, pencarian token selanjutnya..\n")
          
          if found: break

    # Increment init
    init += 1

  end_time = time.time()
  execution_time = (end_time - start_time) * 1000
  return max_buffer, coordinates, max_reward, execution_time

def display_grid(matrix):
  for row in matrix:
    print(" ".join(row))

def save_output_to_file(filename, max_reward, max_buffer, coordinates, matrix, execution_time):
  written_coordinates = set()

  with open(filename, 'w') as file:
    file.write("Reward maksimal: {}\n".format(max_reward))
    file.write("Isi buffer: {}\n".format(max_buffer))
    file.write("Koordinat setiap token: \n")
    for coordinate in coordinates:
      if coordinate not in written_coordinates:
          file.write("{} {}\n".format(coordinate, matrix[coordinate[0]][coordinate[1]]))
          written_coordinates.add(coordinate)
    file.write("Waktu eksekusi: {:.3f} ms\n".format(execution_time))

def main():
  print(Fore.BLUE +"\n<< ============ TUCIL 1 ============ >>")
  title = pyfiglet.figlet_format("Breach Protocol", font="slant")
  print(title)
  
  print("<< ========= PILIH METODE MASUKKAN ========= >>\n" + Style.RESET_ALL)
  print("1. Masukkan nama file")
  print("2. Masukkan secara otomatis")
  option = input("\nPilihan: ")

  if option == "1":
    filename = input("\nMasukkan nama file: ")
    buffer_size, matrix_width, matrix_height, matrix, sequences_and_rewards = read_data_from_file(filename)
    sorted_sequences = sorted(sequences_and_rewards.items(), key=lambda x: x[1], reverse=True)
  elif option == "2":
    buffer_size, matrix_width, matrix_height, matrix, sequences_and_rewards = randomize()

  print(Fore.CYAN + "\n<< ============ HASIL INPUT ============ >>\n" + Style.RESET_ALL)
  print(Style.RESET_ALL + "Buffer Size:", buffer_size)
  print("Matrix Width:", matrix_width)
  print("Matrix Height:", matrix_height)
  print("\nMatrix:")
  display_grid(matrix)
  print("\nSequences and Rewards:")
  for sequence, reward in sequences_and_rewards.items():
    print(f"{sequence}: Reward {reward}")

  print(Fore.MAGENTA + "\n<< ========= ALGORITMA BRUTEFORCE ========= >>" + Style.RESET_ALL)
  max_buffer, coordinates, max_reward, execution_time = find_maximum_reward(buffer_size, matrix_width, matrix_height, matrix, sorted_sequences)

  print(Fore.GREEN + "\n<< ============ HASIL OUTPUT ============ >>\n" + Style.RESET_ALL)
  print("Reward maksimal: ", max_reward)
  print("Isi buffer: ", max_buffer)
  print("Koordinat setiap token: ")
  printed_coordinates = set() 
  for coordinate in coordinates:
      if coordinate not in printed_coordinates:
          print(coordinate, matrix[coordinate[0]][coordinate[1]])
          printed_coordinates.add(coordinate)

  print(Fore.BLUE + "\nWaktu eksekusi:", "{:.3f}".format(execution_time), "ms\n" + Style.RESET_ALL)

  print(">> Apakah ingin menyimpan solusi? (y/n)")
  save = input()
  if save == "y":
    filename = input("\nMasukkan nama file (dalam txt): ")
    print(Fore.GREEN + "\nBerhasil menyimpan solusi pada file output.txt!\n" + Style.RESET_ALL)
    save_output_to_file(filename, max_reward, max_buffer, coordinates, matrix, execution_time)
  else:
    print(Fore.GREEN + "\nTerima kasih telah menggunakan program ini!\n" + Style.RESET_ALL)
  
if __name__ == "__main__":
  main()