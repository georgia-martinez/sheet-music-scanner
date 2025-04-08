import cv2

from staff import staff_y_coords, remove_staff, isolate_staffs, horizontal_image
from notes import note_head_coords


def scan_music(image_url, debug=False):
  image = cv2.imread(image_url, cv2.IMREAD_COLOR)

  # Convert to gray for preprocessing
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  staff_images = isolate_staffs(image_gray, debug)

  for staff_image in staff_images:
    horizontal = horizontal_image(staff_image)

    staff_y = staff_y_coords(horizontal, debug)

    # Remove staff lines before trying to find notes
    # Standard step in OMR projects
    image_no_staff = remove_staff(staff_image, debug)

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
      _, center_y = notehead_center

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

    # TODO: Send data to frontend

if __name__ == "__main__":
  scan_music("test.png", False)