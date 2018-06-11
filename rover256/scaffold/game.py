import sys
import os
from scaffold.loader import load_level
# User Commands
CMD_QUIT = "QUIT"
CMD_START = "START"
CMD_HELP = "HELP"

# Game Commands
GAME_SCAN = "SCAN"
GAME_SCAN_SHADE = "shade"
GAME_SCAN_ELEVATION = "elevation"

GAME_MOVE = "MOVE"

GAME_WAIT = "WAIT"
GAME_STATS = "STATS"
GAME_FINISH = "FINISH"



# Error Messages
ERR_NO_MENU_ITEM = "No menu item"
ERR_GAME_COMMAND = "Cannot perform this command"
ERR_NO_LEVEL_FILE = "Level file could not be found"
ERR_FAIL_LOAD_LEVEL_FILE = "Unable to load level file"

def quit():
	"""
	Will quit the program
	"""
	sys.exit()
	
def menu_help():
	"""
	Displays the h elp menu of the game
	"""

	help_message = \
		"START <level file> - Starts the game with a provided file.\n" \
		"QUIT - Quits the game\n" \
		"HELP - Shows this message"

	print(help_message)


def menu_start_game(file_path):
	"""
	Will start the game with the given file path
	"""
	rover = load_level(file_path)
	if rover == None:
		print(ERR_FAIL_LOAD_LEVEL_FILE)
	else:
		while (True):
			try:
				command = input()
			except EOFError:
				break
			args = command.split()
			num_args = len(args)
			if num_args == 0:		# Input is Empty Line
				continue
			elif num_args == 1:  	# Input A GAME COMMAND Of One Token. Could be [STATS|FINISH]
				if args[0] == GAME_FINISH:
					rover.finish()
					continue
				elif args[0] == GAME_STATS:
					rover.output_stats()
					continue
				else:
					print(ERR_GAME_COMMAND)
					continue
			elif num_args == 2:		# Input A GAME COMMAND Of Two Tokens. Could be [SCAN|WAIT]
				if args[0] == GAME_WAIT:
					try:
						cycle = int(args[1])
					except ValueError:
						print(ERR_GAME_COMMAND)
						continue
					rover.wait(cycle)
				elif args[0] == GAME_SCAN:
					if args[1] == GAME_SCAN_SHADE:
						rover.scan_shade()
					elif args[1] == GAME_SCAN_ELEVATION:
						rover.scan_elevation()
					else:
						print(ERR_GAME_COMMAND)
						continue
				else:
					print(ERR_GAME_COMMAND)
					continue
			elif num_args == 3:		# Input A GAME COMMAND Of Three Tokens. Could be [MOVE]
				if args[0] == GAME_MOVE:
					try:
						step = int(args[2])
					except ValueError:
						print(ERR_GAME_COMMAND)
						continue

					move_result = rover.move(args[1], step)
					if not move_result:
						print(ERR_GAME_COMMAND)
						continue

				else:
					print(ERR_GAME_COMMAND)
					continue
			else:
				print(ERR_GAME_COMMAND)
				continue


def menu():
	"""
	Start the menu component of the game
	"""
	while(True):
		try:
			command = input()
		except EOFError:
			break
		args = command.split()
		num_args = len(args)
		if num_args == 0:		# No Input Command
			print(ERR_NO_MENU_ITEM)
			continue

		elif num_args == 1:		# Input A Command Of One Token. Could be [QUIT | HELP]
			if args[0] == CMD_QUIT:
				quit()
			elif args[0] == CMD_HELP:
				menu_help()
			else:
				print(ERR_NO_MENU_ITEM)
				continue

		elif num_args == 2: 	# Input A Command Of Two Token. Could be [START <level>]
			if args[0] == CMD_START:
				level_file_path = args[1]
				if not os.path.exists(level_file_path):
					print(ERR_NO_LEVEL_FILE)
					continue
				else:
					menu_start_game(level_file_path)
			else:
				print(ERR_NO_MENU_ITEM)
				continue

		else:
			print(ERR_NO_MENU_ITEM)

if __name__ == '__main__':
	menu()