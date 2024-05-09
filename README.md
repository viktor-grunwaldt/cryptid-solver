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
