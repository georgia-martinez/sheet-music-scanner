import sys
sys.path.append("..")

from music_scanner import scan_music

def test_single_line():
    results = scan_music("test.png")

    expected_notes = [
        'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'D5', 'C5', 'B4', 'A4', 'G4',
        'C5', 'B4', 'F4', 'A4', 'C5', 'E5', 'F5', 'E5', 'D5', 'C5', 'B4', 'A4',
        'G4', 'F4', 'E4', 'F4'
    ]

    assert results == expected_notes

def test_multiline():
    results = scan_music("test-multiline.png")

    expected_notes = ['F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'D5', 'C5', 'B4', 'A4', 'G4', 'C5', 'B4', 'F4', 'A4', 'C5', 'E5', 'F5', 'E5', 'D5', 'C5', 'B4', 'A4', 'G4', 'F4', 'E4', 'F4', 'A4', 'G4', 'A4', 'C5', 'C5', 'C5', 'C5', 'C5', 'G4', 'A4', 'C5', 'D5', 'E5', 'D5', 'C5', 'B4', 'C5', 'E5', 'F5', 'G4', 'C5', 'B4', 'A4', 'A4', 'E4', 'A4', 'G4', 'G4', 'B4', 'D5', 'B4', 'G4', 'G4', 'C5', 'A4', 'B4', 'C5', 'A4', 'G4', 'F4', 'G4', 'D5', 'C5', 'G4', 'E5', 'C5', 'G4', 'A4', 'B4', 'B4', 'A4', 'G4', 'G4', 'D5', 'E5', 'D5']

    assert results == expected_notes
