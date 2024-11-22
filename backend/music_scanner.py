from staff import staff_y_coords


def scan_music():
  y_coords = staff_y_coords("test.png", debug=True);

  print(y_coords)

if __name__ == "__main__":
  scan_music()