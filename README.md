# Pyalp

A Python module to control Vialux DMDs based on ALP API via the DLL provided by
Vialux.


# TODOs

- [x] Test the allocation of the ALP device
- [x] Test the white sequence (i.e. generation & display)
- [x] Test the black sequence (i.e. generation & display)
- [x] Test the black & white sequence (i.e. generation & display)
- [x] Test the full-field sequence (i.e. generation & display)
- [ ] Test the checkerboard sequence (i.e. generation & display)
- [ ] Generate moving bar sequence
- [ ] Test the moving bar sequence (i.e. generation & display)
- [ ] Generate moving bars sequence
- [ ] Test the moving bars sequence (i.e. generation & display)
- [x] Add inquiry mechanism for ALP device
- [x] Test inquiry mechanism for ALP device
- [x] Add inquiry mechanism for sequence on ALP device
- [x] Test inquiry mechanism for sequence on ALP device



# Notes

## Conda environment
```
source activate alp
```

## Installation

### Windows
- Install `Git for Windows`.
- Clone `git://github.com/balefebvre/pyalp.git`.
- Install `Python 3.6`.
- Install `PyCharm Community`.
- Run `pip install -e .`.
- Define `ALP_PATH`.
