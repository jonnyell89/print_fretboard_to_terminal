tunings = {
    
    "e_standard": ["E", "A", "D", "G", "B", "E"],

    "open_c": ["C", "G", "C", "G", "C", "E"]
    
}

pitch_notations = {

    "e_standard": [2, 2, 3, 3, 3, 4],

    "open_c": [2, 2, 3, 3, 4, 4]

}

chromatic_scale = {

    "chromatic_scale": ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

}

scale_patterns = {

    "major_scale": [0, 2, 4, 5, 7, 9, 11],

    "natural_minor": [0, 2, 3, 5, 7, 8, 10],

    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],

    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],

    "ionian_mode": [0, 2, 4, 5, 7, 9, 11],

    "dorian_mode": [0, 2, 3, 5, 7, 9, 10],

    "phrygian_mode": [0, 1, 3, 5, 7, 8, 10],

    "lydian_mode": [0, 2, 4, 6, 7, 9, 11],

    "mixolydian_mode": [0, 2, 4, 5, 7, 9, 10],

    "aeolian_mode": [0, 2, 3, 5, 7, 8, 10],

    "locrian_mode": [0, 1, 3, 5, 6, 8, 10],

    "pentatonic_major": [0, 2, 4, 7, 9],

    "pentatonic_minor": [0, 3, 5, 7, 10]
    
}

chord_patterns = {

    "notes_3": [0, 2, 4],

    "notes_4": [0, 2, 4, 6]
    
}

note_intervals = {

    0: "R",
    1: "b2",
    2: "2",
    3: "3m",
    4: "3M",
    5: "4",
    6: "b5",
    7: "5",
    8: "#5",
    9: "6",
    10: "7",
    11: "7M",
    12: "8",
    13: "b9",
    14: "9",
    15: "#9",
    16: "b11",
    17: "11",
    18: "#11",
    19: "12",
    20: "b13",
    21: "13",
    22: "#13"

}

chord_names = {

    "M": [0, 4, 7],
    "m": [0, 3, 7],
    
}

key_names = {

    0: ["C"],
    1: ["Db", "C#"],
    2: ["D"],
    3: ["Eb", "D#"],
    4: ["E"],
    5: ["F"],
    6: ["Gb", "F#"],
    7: ["G"],
    8: ["Ab", "G#"],
    9: ["A"],
    10: ["Bb", "A#"],
    11: ["B"]

}

from typing import List, Dict, Optional

class StringGenerator:

    """
    A class to generate a guitar string representation based on the chromatic scale.

    Attributes:

        root: The root note of the guitar string.
        length: The number of notes on the guitar string.
        chromatic_scale: The twelve note chromatic scale.
        root_index: The root note index of the guitar string, relative to the chromatic scale.
    
    """

    def __init__(self, root: str, length: int = 16, chromatic_scale: List[str] = chromatic_scale["chromatic_scale"]) -> None:

        self.root: str = root
        self.length: int = length
        self.chromatic_scale: List[str] = chromatic_scale
        self.root_index = self.chromatic_scale.index(self.root)

    # Generates a list of notes representing a guitar string, starting from a specific point in the chromatic scale.
    def generate_string(self) -> List[str]:

        return [self.chromatic_scale[(self.root_index + note) % len(self.chromatic_scale)] for note in range(self.length)]
    
    # Sets a new root note for the guitar string representation.
    def set_root(self, new_root: str) -> None:

        self.root: str = new_root

    # Sets a new length for the guitar string representation.
    def set_length(self, new_length: int) -> None:

        self.length: int = new_length



print("--------------------")

demo_string = StringGenerator("C")

print(demo_string.generate_string())



class FretboardGenerator:

    """
    A class to generate a chromatic guitar fretboard representation in both horizontal and vertical orientations.
    
    Attributes:

        length: The number of frets on the chromatic guitar fretboard.
        chromatic_scale: The twelve note chromatic scale.
        tuning: The root note of each guitar string, representing the tuning of the guitar.
        strings: The guitar strings as StringGenerator objects.
        fretboard_dict: The horizontal and vertical orientations of the chromatic guitar fretboard.
        frets: The frets on the guitar fretboard.

    """

    def __init__(self, length: int = 16, chromatic_scale: List[str] = chromatic_scale["chromatic_scale"], tuning: List[str] = tunings["e_standard"]) -> None:
        
        self.length: int = length
        self.chromatic_scale: List[str] = chromatic_scale
        self.tuning: List[str] = tuning[::-1]
        self.strings: List[StringGenerator] = [StringGenerator(root, self.length, self.chromatic_scale) for root in self.tuning]
        self.fretboard_dict: Dict[str, List[List[str]]] = {}
        self.generate_fretboard_x()
        self.generate_fretboard_y()
        self.frets: List[str] = [str(fret) for fret in range(self.length)]

    # Generates a two-dimensional list of six guitar strings representing a chromatic guitar fretboard, in horizontal orientation.
    def generate_fretboard_x(self) -> None:

        horizontal_fretboard: List[List[str]] = [string.generate_string() for string in self.strings]

        self.fretboard_dict["x"] = horizontal_fretboard

    # Generates a vertically orientated chromatic guitar fretboard by rotating the horizontally orientated chromatic guitar fretboard 90 degrees clockwise.
    def generate_fretboard_y(self) -> None:

        horizontal_fretboard: List[List[str]] = self.fretboard_dict["x"]

        number_of_strings: int = len(horizontal_fretboard)

        length_of_strings: int = len(horizontal_fretboard[0])

        vertical_fretboard: List[List[str]] = [[0 for _ in range(number_of_strings)] for _ in range(length_of_strings)]

        for i in range(number_of_strings):

            for j in range(length_of_strings):

                vertical_fretboard[j][number_of_strings - 1 - i] = horizontal_fretboard[i][j]
                    
        self.fretboard_dict["y"] = vertical_fretboard

    # Applies a list of numbers representing fret markers to a chromatic, scale or chord based guitar fretboard in a specific orientation.
    def apply_fret_marker(self, fretboard_dict: Dict[Optional[int], Dict[str, List[List[str]]]], orientation: str, chord: Optional[int] = None) -> None:

        if not self._is_valid_fretboard(fretboard_dict, orientation, chord):

            return

        if orientation == "x":

            self._apply_fret_marker_x(fretboard_dict, chord)

        elif orientation == "y":

            self._apply_fret_marker_y(fretboard_dict, chord)

    # Prints a chromatic, scale or chord based guitar fretboard in a specific orientation.
    def print_fretboard(self, fretboard_dict: Dict[Optional[int], Dict[str, List[List[str]]]], orientation: str, chord: Optional[int] = None) -> None:

        if not self._is_valid_fretboard(fretboard_dict, orientation, chord):

            return

        if chord:

            fretboard = fretboard_dict[chord][orientation]

        else:

            fretboard = fretboard_dict[orientation]

        self._print_fretboard(fretboard)

    # Helper method -> Error handling: Checks if both the chord and orientation parameters are present in the fretboard dictionary.
    def _is_valid_fretboard(self, fretboard_dict: Dict[Optional[int], Dict[str, List[List[str]]]], orientation: str, chord: Optional[int] = None) -> bool:

        if chord:

            if chord not in fretboard_dict:

                print(f"Error: {chord} chord not found in fretboard dictionary.")

                return False

            if orientation not in fretboard_dict[chord]:

                print(f"Error: {orientation} orientation not found in fretboard dictionary.")

                return False
            
        else:

            if orientation not in fretboard_dict:

                print(f"Error: {orientation} orientation not found in fretboard dictionary.")

                return False
            
        return True
    
    # Helper method -> Logic: Applies a list of numbers representing fret markers to a specific horizontally orientated guitar fretboard.
    def _apply_fret_marker_x(self, fretboard_dict: Dict[Optional[int], Dict[str, List[List[str]]]], chord: Optional[int] = None) -> None:

        if chord:

            fretboard_dict[chord]["x"].append(self.frets)

        else:

            fretboard_dict["x"].append(self.frets)

    # Helper method -> Logic: Applies a list of numbers representing fret markers to a specific vertically orientated guitar fretboard.
    def _apply_fret_marker_y(self, fretboard_dict: Dict[Optional[int], Dict[str, List[List[str]]]], chord: Optional[int] = None) -> None:

        if chord:

            for index, fret in enumerate(self.frets):
    
                fretboard_dict[chord]["y"][index].insert(0, fret)

        else:

            for index, fret in enumerate(self.frets):
    
                fretboard_dict["y"][index].insert(0, fret)

    # Helper method -> Logic: Prints a series of lists representing guitar strings that together represent the guitar fretboard in both horizontal and vertical orientations.
    def _print_fretboard(self, fretboard: List[List[str]]) -> None:

        for string in fretboard:

            print([f"{note:<2}" for note in string])



print("--------------------")

demo_fretboard = FretboardGenerator()

demo_fretboard_dict = demo_fretboard.fretboard_dict

demo_fretboard.apply_fret_marker(demo_fretboard_dict, orientation="x")

demo_fretboard.apply_fret_marker(demo_fretboard_dict, orientation="y")

demo_fretboard.print_fretboard(demo_fretboard_dict, orientation="x")

demo_fretboard.print_fretboard(demo_fretboard_dict, orientation="y")



class ScaleFretboardGenerator(FretboardGenerator):

    """
    A class to generate a guitar fretboard representation containing the notes of a specific scale, in both horizontal and vertical orientations.

    Attributes:

        key: The first note in the scale.
        scale_pattern: The series of intervals that make up the scale.
        key_index: The first note in the scale, relative to the chromatic scale.
        scale_notes: The series of notes that make up the scale, derived from the chromatic scale.
        scale_fretboard_dict: The horizontal and vertical orientations of the guitar fretboard containing the notes from the scale.
    
    """

    def __init__(self, key: str = "C", scale_pattern: List[int] = scale_patterns["major_scale"]) -> None:

        # Refers to the FretboardGenerator class constructor.
        super().__init__()

        self.key: str = key
        self.scale_pattern: List[int] = scale_pattern        
        self.key_index: int = self.chromatic_scale.index(self.key)
        self.scale_notes: List[str] = self.calculate_scale_notes()
        self.scale_fretboard_dict: Dict[str, List[List[str]]] = {}
        self.generate_scale_fretboard()

    # Generates a list of notes representing the scale, derived from the chromatic scale.
    def calculate_scale_notes(self) -> List[str]:

        scale_notes: List[str] = [self.chromatic_scale[(self.key_index + note) % len(self.chromatic_scale)] for note in self.scale_pattern]

        return scale_notes

    # Generates a scale orientated guitar fretboard in both horizontal and vertical orientations.
    def generate_scale_fretboard(self) -> None:

        self.scale_fretboard_dict["x"] = self._apply_scale_to_fretboard(self.fretboard_dict["x"])

        self.scale_fretboard_dict["y"] = self._apply_scale_to_fretboard(self.fretboard_dict["y"])
    
    # Helper method -> Logic: Applies the scale to the standard chromatic guitar fretboard.
    def _apply_scale_to_fretboard(self, fretboard: List[List[str]]) -> List[List[str]]:

        scale_fretboard: List[List[str]] = [[note if note in self.scale_notes else "__" for note in string] for string in fretboard]

        return scale_fretboard



print("--------------------")

demo_scale_fretboard = ScaleFretboardGenerator()

demo_scale_fretboard_dict = demo_scale_fretboard.scale_fretboard_dict

demo_scale_fretboard.apply_fret_marker(demo_scale_fretboard_dict, orientation="x")

# demo_scale_fretboard.apply_fret_marker(demo_scale_fretboard_dict, orientation="y")

demo_scale_fretboard.print_fretboard(demo_scale_fretboard_dict, orientation="x")

demo_scale_fretboard.print_fretboard(demo_scale_fretboard_dict, orientation="y")



class ChordFretboardGenerator(ScaleFretboardGenerator):

    """
    A class to generate a guitar fretboard representation containing the notes of a specific chord derived from the inherited scale, in both horizontal and vertical orientations.

    Attributes:

        chord_pattern: The series of intervals that make up the chord.
        chord_notes_dict: The series of notes that make up the chord, derived from the inherited scale.
        chord_fretboard_dict: The horizontal and vertical orientations of the guitar fretboard containing the notes from the chord, derived from the inherited scale.
    
    """

    def __init__(self, chord_pattern: List[int] = chord_patterns["notes_3"]) -> None:

        # Refers to the ScaleFretboardGenerator constructor.
        super().__init__()

        self.chord_pattern: List[int] = chord_pattern
        self.chord_notes_dict: Dict[int, List[str]] = {}
        self.calculate_chord_notes()
        self.chord_fretboard_dict: Dict[int, Dict[str, List[List[str]]]] = {}
        self.generate_chord_fretboards()

    # Generates a list of notes representing the chords for each scale degree, based on the chord pattern and derived from the inherited scale.
    def calculate_chord_notes(self) -> None:

        scale_degrees: int = len(self.scale_notes)

        for degree_index in range(scale_degrees):

            chord_notes: List[str] = [self.scale_notes[(degree_index + note) % scale_degrees] for note in self.chord_pattern]

            self.chord_notes_dict[degree_index + 1] = chord_notes

    # Generates a chord orientated guitar fretboard in both horizontal and vertical orientations.
    def generate_chord_fretboards(self) -> None:

        for chord_index, chord in self.chord_notes_dict.items():

            self.chord_fretboard_dict[chord_index] = {

                "x": self._apply_chords_to_fretboard_x(chord),
                "y": self._apply_chords_to_fretboard_y(chord)

            }
    
    # Helper method -> Logic: Applies the chord notes to the scale orientated horizontal guitar fretboard.
    def _apply_chords_to_fretboard_x(self, chord: List[str]) -> List[List[str]]:

        horizontal_fretboard = self.scale_fretboard_dict["x"]

        chord_fretboard_x: List[List[str]] = [[note if note in chord else "__" for note in string] for string in horizontal_fretboard]

        return chord_fretboard_x

    # Helper method -> Logic: Applies the chord notes to the scale orientated vertical guitar fretboard.
    def _apply_chords_to_fretboard_y(self, chord: List[str]) -> List[List[str]]:

        vertical_fretboard = self.scale_fretboard_dict["y"]

        chord_fretboard_y: List[List[str]] = [[note if note in chord else "__" for note in string] for string in vertical_fretboard]

        return chord_fretboard_y



print("--------------------")

demo_chord_fretboard = ChordFretboardGenerator()

demo_chord_fretboard_dict = demo_chord_fretboard.chord_fretboard_dict

print(demo_chord_fretboard.scale_notes)

print(demo_chord_fretboard.chord_notes_dict)

demo_chord_fretboard.apply_fret_marker(demo_chord_fretboard_dict, orientation="x", chord=1)

# demo_chord_fretboard.apply_fret_marker(demo_chord_fretboard_dict, orientation="y", chord=1)

demo_chord_fretboard.print_fretboard(demo_chord_fretboard_dict, orientation="x", chord=1)

demo_chord_fretboard.print_fretboard(demo_chord_fretboard_dict, orientation="y", chord=1)




