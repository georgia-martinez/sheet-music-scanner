from staff import staff_y_coords
from notes import note_boxes


def scan_music(image_url):
  y_coords = staff_y_coords(image_url)
  notes_boxes = note_boxes(image_url)

  note_letters = ["E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5"]

  note_map = dict(zip(y_coords, note_letters))

  notes = []

  for note_box in notes_boxes:
    x1, y1, x2, y2 = note_box

    center_y = (y1 + y2) / 2

    closest_y = min(y_coords, key=lambda y: abs(y - center_y))

    notes.append(note_map[closest_y] + " 4n")

  return notes

if __name__ == "__main__":
  scan_music()