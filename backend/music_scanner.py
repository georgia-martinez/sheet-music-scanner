from staff import staff_y_coords, remove_staff_lines
from notes import note_boxes

def scan_music(image_url):
  y_coords = staff_y_coords(image_url, False)
  notehead_centers = note_boxes(image_url, False)

  note_letters = ["E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5"]
  note_letters.reverse()

  note_map = dict(zip(y_coords, note_letters))

  notes = []

  print(y_coords)

  for index, notehead_center in enumerate(notehead_centers):
    center_x, center_y = notehead_center

    closest_y = min(y_coords, key=lambda y: abs(y - center_y))

    note_name = note_map[closest_y]

    print(f"{center_y=} {note_name=}")

    note_data = { "note": note_name, "duration": "4n", "time": index }

    notes.append(note_data)

  data = {
    "bpm": 80,
    "notes": notes
  }

  return data


if __name__ == "__main__":
  scan_music("test.png")
  # remove_staff_lines("test.png")