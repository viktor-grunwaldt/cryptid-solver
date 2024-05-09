# Cryptid Solver

[Cryptid](https://boardgamegeek.com/boardgame/246784/cryptid) is a deduction board game, and because there is desire to check, how much better and faster computer can deduct all needed information to find the creature.

## How to use

click on field and using buttons below select if given field is true or false for given player.

## How to run (development mode)

To run it, for now you need to use Python 3+, recommended is to use `venv`:

Linux way:

```bash
python -m venv venv
source venv/bin/activate
```

Windows way:

```cmd
.\venv\bin\Activate.ps1
```

or

```cmd
.\venv\Scripts\Activate.ps1
```

then when in venv install all required packages:

```bash
pip install -r requirements.txt
```

If you are ready to go, run `main.py` in `src` directory.

## When finished

If you want to exit from `venv` write simple

```bash
deactivate
```

And you can remove `venv` folder.

## TODO

- [x] Add buttons to add structures
  - [ ] Make that only one structure of each type can exist on the map
- [ ] Add ability to put multiple circles on one field
- [ ] Display viable clues for each player
- [x] Add ability to select number of players
- [ ] Function for deducting the clues

## Additional information

### All possible clues

1. The habitat is (not) on {biome} or {biome}
2. The habitat is (not) within one space of {biome}
3. The habitat is (not) within one space of either animal territory
4. The habitat is (not) within two spaces of a {structure}
5. The habitat is (not) within two spaces of {animal} territory
6. The habitat is (not) within three spaces of a {color} structure
