import cv2
import argparse
import yaml
import os

from staff import staff_y_coords, remove_staff
from notes import note_head_coords

def scan_music(image_url, debug=False):
  image = cv2.imread(image_url, cv2.IMREAD_COLOR)

  # Convert to gray for preprocessing
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  staff_y = staff_y_coords(image_gray, debug)

  # Remove staff lines before trying to find notes
  # Standard step in OMR projects
  image_no_staff = remove_staff(image_gray, debug)

  note_heads = note_head_coords(image_no_staff, staff_y, debug)

  # Having the notes in this order is more readable
  # Reversed b/c OpenCV has (0, 0) in top left, higher the note -> lower y value
  note_letters = ["E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5"]
  note_letters.reverse()

  note_map = dict(zip(staff_y, note_letters))

  notes = []
  note_names = []

  print(f"# of notes found: {len(note_heads)}")
  print(f"Staff y coords: {staff_y}")

  for index, notehead_center in enumerate(note_heads):
    center_x, center_y = notehead_center

    closest_y = min(staff_y, key=lambda y: abs(y - center_y))

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

def load_env_from_yaml(file_path):
    with open(file_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            for key, value in config.items():
                os.environ[key] = str(value)
        except yaml.YAMLError as exc:
            print(f"Error loading YAML file: {exc}")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog='music_scanner')
  parser.add_argument("filename", help="Path to the input file")

  args = parser.parse_args()

  load_env_from_yaml("config.yaml")

  scan_music(args.filename, True)

