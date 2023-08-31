#!/usr/bin/python3
"""
Python Implementation of Enigma Machine

TODO & Notes
    - Fix exceptions
    - Write tests

References:
    https://people.physik.hu-berlin.de/~palloks/js/enigma/enigma-u_v20_en.html
    https://www.101computing.net/enigma-machine-emulator/
"""
__all__ = ["EnigmaReflectorBase", "EnigmaRotorBase", "EnigmaMachine"]

class EnigmaException(Exception):
    """Base class for Enigma Machine exceptions
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidRotorException(EnigmaException):
    pass

class InvalidPlugboardException(EnigmaException):
    pass

class InvalidReflectorException(EnigmaException):
    pass


class EnigmaPlugboard:
    """Enigma Machine Plugboard Class

    Designates letters to be swapped before being sent to rotors
    """
    def __init__(self):
        self.plugs = dict()

    def __str__(self):
        if not self.plugs:
            return "No plugboard combinations set\n"
        string = ""
        for combo in self.plugs.items():
            string += f"{combo[0]} <-> {combo[1]}\n"
        return string

    def add(self, combos):
        for combo in combos:
            combo = list(combo.upper())
            if len(combo) != 2 or combo[0] == combo[1]:
                raise InvalidPlugboardException("Plug must be combination of 2 different letters")
            elif combo[0] in self.plugs.keys() or combo[0] in self.plugs.values():
                raise InvalidPlugboardException(f"Plug {combo[1]} already in use")
            elif combo[1] in self.plugs.keys() or combo[1] in self.plugs.values():
                raise InvalidPlugboardException(f"Plug {combo[1]} already in use")
            else:
                self.plugs[combo[0]] = combo[1]

    def __call__(self, letter):
        if letter in self.plugs:
            letter = self.plugs[letter]
        elif letter in self.plugs.values():
            letter = list(self.plugs.keys())[list(self.plugs.values()).index(letter)] # Get key from value
        return letter


class EnigmaReflectorBase:
    def __init__(self):
        pass

    def __str__(self):
        return f"{self.RTYPE}"

    def __call__(self, letter):
        letter = letter.upper()
        if letter in self.REFLECTOR_MAP:
            return self.REFLECTOR_MAP[letter]
        elif letter in self.REFLECTOR_MAP.values():
            return list(self.REFLECTOR_MAP.keys())[list(self.REFLECTOR_MAP.values()).index(letter)] # Get key from value
        else:
            raise InvalidReflectorException(f"Unable to locate letter '{letter}'")

class EnigmaReflectorB(EnigmaReflectorBase):
    REFLECTOR_MAP = {
    "A":"Y",
    "B":"R",
    "C":"U",
    "D":"H",
    "E":"Q",
    "F":"S",
    "G":"L",
    "I":"P",
    "J":"X",
    "K":"N",
    "M":"O",
    "T":"Z",
    "V":"W"
    }
    RTYPE = 'B'

class EnigmaReflectorC(EnigmaReflectorBase):
    REFLECTOR_MAP = {
    "A":"F",
    "B":"V",
    "C":"P",
    "D":"J",
    "E":"I",
    "G":"O",
    "H":"Y",
    "K":"R",
    "L":"Z",
    "M":"X",
    "N":"W",
    "T":"Q",
    "S":"U"
    }
    RTYPE = 'C'


class EnigmaRotorBase:
    """Enigma Machine Rotor Base Class

    'Rotors' which substitute a letter with on from
    the alphabet of their respective type
    """
    RTYPE = ''
    NOTCH = ''
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    WIRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        self.rotor_map = [list(self.ALPHABET), list(self.WIRING)] 
        self.position = 0 # 'A'
        self.ring = 0 # 'A'
        self.direction = 0 # right to left

    def info(self):
        """Returns details of rotor instance

        (rotor type, notch letter, position, ring setting)
        """
        return (self.RTYPE, self.NOTCH, self.ALPHABET[self.position], self.ALPHABET[self.ring])

    def __str__(self):
        return f"Rotor ({self.RTYPE})"

    def __call__(self, letter): # Encipher
        real_index = self.ALPHABET.index(letter)

        # Left and right maps/wiring are assigned based on the direction
        l_map = self.rotor_map[self.direction]
        r_map = self.rotor_map[1 - self.direction]

        substitution = r_map[real_index] # Corresponding rotor letter (possibly shifted) from real index in alphabet
        output = self.ALPHABET[l_map.index(substitution)] # Output is adjust for possible shift before being passed to next rotor/output

        # Switch direction (1/0) for next time this rotor is called
        self.direction = 1 - self.direction 
        return output
        
    def rotate(self, turns=1):
        self.position = (self.position + turns) % 26
        self.rotor_map[0] = self.rotor_map[0][turns:] + self.rotor_map[0][:turns]
        self.rotor_map[1] = self.rotor_map[1][turns:] + self.rotor_map[1][:turns]

    def isNotch(self):
        """Returns True/False, indicating whether or not the next rotor should rotate
        """
        if self.rotor_map[0][0] in list(self.NOTCH): # Accounts for rotors VI, VII, and VIII, which have 2 notches
            return True
        else:
            return False

    def setInitialPosition(self, position):
        """Set initial position of letter ring

        Accepts either letter or number offset.
        """
        if type(position) is int:
            position = (position - 1) % 26 
        else:
            position = self.ALPHABET.index(position.upper())
        self.rotate(position)

    def setRing(self, position):
        """Set position of internal 'wiring' (alphabet) relative to rotor
        """
        if type(position) is int:
            self.ring = (position - 1) % 26 
        else:
            self.ring = self.ALPHABET.index(position.upper())

        self.rotor_map[0] = self.rotor_map[0][-self.ring:] + self.rotor_map[0][:-self.ring]
        self.rotor_map[1] = self.rotor_map[1][-self.ring:] + self.rotor_map[1][:-self.ring]

class EnigmaRotorI(EnigmaRotorBase):
    RTYPE = 'I'
    NOTCH = 'Q'
    WIRING = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"

class EnigmaRotorII(EnigmaRotorBase):
    RTYPE = 'II'
    NOTCH = 'E'
    WIRING = "AJDKSIRUXBLHWTMCQGZNPYFVOE"

class EnigmaRotorIII(EnigmaRotorBase):
    RTYPE = 'III'
    NOTCH = 'V'
    WIRING = "BDFHJLCPRTXVZNYEIWGAKMUSQO"

class EnigmaRotorIV(EnigmaRotorBase):
    RTYPE = 'IV'
    NOTCH = 'J'
    WIRING = "ESOVPZJAYQUIRHXLNFTGKDCMWB"

class EnigmaRotorV(EnigmaRotorBase):
    RTYPE = 'V'
    NOTCH = 'Z'
    WIRING = "VZBRGITYUPSDNHLXAWMJQOFECK"

class EnigmaRotorVI(EnigmaRotorBase):
    RTYPE = 'VI'
    NOTCH = 'ZM'
    WIRING = "JPGVOUMFYQBENHZRDKASXLICTW"

class EnigmaRotorVII(EnigmaRotorBase):
    RTYPE = 'VII'
    NOTCH = 'ZM'
    WIRING = "NZJHGRCXMYSWBOUFAIVLPEKQDT"

class EnigmaRotorVIII(EnigmaRotorBase):
    RTYPE = 'VIII'
    NOTCH = 'ZM'
    WIRING = "FKQHTLXOCBJSPDZRAMEWNIUYGV"


class EnigmaMachine:
    """3-Rotor Enigma Machine
    """
    AVAILABLE_ROTORS = [
        EnigmaRotorI, 
        EnigmaRotorII, 
        EnigmaRotorIII,
        EnigmaRotorIV,
        EnigmaRotorV,
        EnigmaRotorVI,
        EnigmaRotorVII,
        EnigmaRotorVIII
        ]
    def __init__(self, *, r1=1, r2=2, r3=3, reflector='B'):
        self.setRotorTypes(r1, r2, r3)
        self.setReflector(reflector)
        self.plugboard = EnigmaPlugboard()

    def __str__(self):
        string = "~ Rotors ~\n"
        rotor_info = [rotor.info() for rotor in self.rotors]
        string += f"Wheels: {', '.join(info[0] for info in rotor_info)}\n"
        string += f"Positions: {', '.join(info[2] for info in rotor_info)}\n"
        string += f"Rings: {', '.join(info[3] for info in rotor_info)}\n"
        string += f"\n~ PLUGBOARD ~\n{self.plugboard}\n~ Reflector ~\nType: {self.reflector}"
        return string

    def setRotorTypes(self, *rtypes):
        self.rotors = []
        for rtype in rtypes:
            try:
                if type(rtype) is int:
                    self.rotors.append(self.AVAILABLE_ROTORS[rtype - 1]())
                else:
                    self.rotors.append(rtype())
            except IndexError:
                raise InvalidRotorException(f"Invalid rotor option '{rtype}'")

    def setRotorPositions(self, *positions):
        """Set initial positions for rotor letter rings

        Default: A, A, A (1, 1, 1)
        """
        for position, rotor in zip(positions, self.rotors):
            try:
                rotor.setInitialPosition(position)
            except IndexError:
                raise InvalidRotorException(f"Invalid rotor position '{rtype}'")

    def setRotorRings(self, *rings):
        """Assign ring settings to rotors to determine internal offset

        Default: A, A, A (1, 1, 1)
        """
        for ring_setting, rotor in zip(rings, self.rotors):
            try:
                rotor.setRing(ring_setting)
            except IndexError:
                raise InvalidRotorException(f"Invalid rotor ring setting '{rtype}'")

    def setReflector(self, reflector_type):
        reflector_type = reflector_type.upper()
        if reflector_type == 'B':
            self.reflector = EnigmaReflectorB()
        elif reflector_type == 'C':
            self.reflector = EnigmaReflectorC()
        else:
            raise InvalidReflectorException(f"Invalid reflector type '{reflector_type}'")

    def setPlugboard(self, combos):
        self.plugboard.add(combos.split())

    def __call__(self, msg):
        ciphertext = ""
        message = [letter for letter in list(msg.upper()) if letter in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")] # Remove any non-letter characters, and capitalize

        for letter in message:
            # 1. Pass letter through plugboard
            cipher_letter = self.plugboard(letter) 
            notch_hit = True # Initially True because rightmost rotor rotates with each keypress/letter

            # 2. Traverse rotors right to left
            for rotor in reversed(self.rotors): 
                """
                Check if rotor is currently on a notch,
                then rotate rotor if notch was hit on previous rotor
                """
                if notch_hit:
                    notch_hit = rotor.isNotch()
                    rotor.rotate()

                cipher_letter = rotor(cipher_letter)

            # 3. Pass cipher letter through reflector (either A or B)
            cipher_letter = self.reflector(cipher_letter)

            # 4. Traverse rotors left to right
            for rotor in self.rotors:
                cipher_letter = rotor(cipher_letter)

            # 5. Pass letter (now encipher'd) through plugboard again
            ciphertext += self.plugboard(cipher_letter) 

        return ciphertext

     
