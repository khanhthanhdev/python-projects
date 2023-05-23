# You must install curses to run this program: pip install window-curses
"""
    The function is a speed typing test program that displays a random text and calculates the user's
    typing speed in words per minute.
    
    :param stdscr: The standard screen object in curses, which represents the entire screen and provides
    methods for displaying text and handling user input

    The code contains the following functions:

start_screen(stdscr): This function displays the welcome message and waits for the user to press any key to start the game.

display_text(stdscr, target, current, wpm=0): This function displays the target text, the current text typed by the user, and the current WPM on the screen. The correct characters are displayed in green, while incorrect characters are displayed in red.

load_text(): This function reads a text file and returns a random line from the file.

wpm_test(stdscr): This function runs the main game loop. It prompts the user to type the target text, measures the user's typing speed, and updates the screen accordingly. The function exits when the user types the entire target text.

main(stdscr): This function initializes the curses library, sets up the color pairs, displays the start screen, and runs the game loop. After the game loop exits, it displays a message prompting the user to continue or quit the game.
"""

import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)
	stdscr.addstr(1, 0, f"WPM: {wpm}")

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)

def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def wpm_test(stdscr):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
	while True:
		wpm_test(stdscr)
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
		key = stdscr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)