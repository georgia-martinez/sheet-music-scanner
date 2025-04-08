import sys
import pytest
sys.path.append("..")

from music_scanner import scan_music

def test_scan_music_sheet():
    results = scan_music("test.png", debug=False)

    expected_notes = [
        'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'D5', 'C5', 'B4', 'A4', 'G4',
        'C5', 'B4', 'F4', 'A4', 'C5', 'E5', 'F5', 'E5', 'D5', 'C5', 'B4', 'A4',
        'G4', 'F4', 'E4', 'F4'
    ]

    assert results == expected_notes
