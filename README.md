# game-of-life
A python simulation for [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) devised by John Conway.

## Installation
### Dependencies
Recommended **python version: 3.8**
- pyglet
- pyyaml

Use pip to install these packages (`python3 -m pip install <package_name>`)

### Setup

Clone this repository using following command<br>
`git clone https://github.com/VismayVakharia/game-of-life`

## Usage

Run `main.py` to start the simulation

### Configuration

Use the `config.yaml` file to modify the parameters

### GUI Control

- `click` on any cell to toggle it's state
- `space` to play/pause the simulation

### Recording
If the `recording_abspath` parameter is set, animation frames will be saved to the given directory.

To convert these frame to **gif**:
```shell
cd frames/
convert -delay 50 -loop 0 `ls -v` output.gif
```
