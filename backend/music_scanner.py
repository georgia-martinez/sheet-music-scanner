import cv2

from staff import staff_y_coords
from notes import notehead_coords

def scan_music(image_url, debug=False):
  image = cv2.imread(image_url)
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  y_coords = staff_y_coords(image_gray, debug)
  noteheads = notehead_coords(image_gray, debug)

  note_letters = ["E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5"]
  note_letters.reverse()

  note_map = dict(zip(y_coords, note_letters))

  notes = []
  note_names = []

  print(f"# of notes found: {len(noteheads)}")
  print(f"Staff y coords: {y_coords}")

  for index, notehead_center in enumerate(noteheads):
    center_x, center_y = notehead_center

    closest_y = min(y_coords, key=lambda y: abs(y - center_y))

    note_name = note_map[closest_y]

    note_data = { "note": note_name, "duration": "4n", "time": index }

    note_names.append(note_name)
    notes.append(note_data)

  print(note_names)

  data = {
    "bpm": 80,
    "notes": notes
  }

  return data


if __name__ == "__main__":
  scan_music("test.png", True)