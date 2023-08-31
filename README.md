# Enigma Machine
*enigma.py* is a Python implementation of a 3-rotor Enigma Machine.

## Usage
```py
from enigmamachine import EnigmaMachine

enigma = EnigmaMachine()
enigma.setRotorTypes(4, 2, 5) # Default: I, II, III
enigma.setRotorRings(15, 23, 26) # Default: A, A, A (1, 1, 1)
enigma.setRotorPositions('A', 'B', 'C') # Default: A, A, A (1, 1, 1)
enigma.setPlugboard("LZ SQ AG") # Default: None
enigma.setReflector('C') # Default: B

print(f"Enigma'd Message: {enigma('STBWBKB')}") # "MESSAGE"
```
### Custom Rotors
```py
from enigmamachine import EnigmaMachine, EnigmaRotorBase

class MyRotor(EnigmaRotorBase):
    RTYPE = 'X'
    NOTCH = 'ZUL' # Triggers next rotor to rotate if position goes from Z->A, U->V, or L->M
    WIRING = "QAIBRFLGDCJVEKMZNTOSPWYHXU"
    
enigma = EnigmaMachine()
enigma.setRotorTypes(3, MyRotor, 1)
print(enigma("DSFIHDXCT")) # SCOOBYDOO
```
## Known Issues & TODO
- Add a "reset" method, because right now you need a seperate *EnigmaMachine* instance to decipher data returned from a previous *EnigmaMachine* instance
    - The issue is likely with the *EnigmaRotorBase.setInitialPosition()* or *rotate()* functions
- Expand on tests
- Fix exceptions (maybe)
- Reflector and Plugboard classes could be implemented in a less stupid way (and/or possibly streamlined)
- Implement way to add arbitrary numbers of rotors
