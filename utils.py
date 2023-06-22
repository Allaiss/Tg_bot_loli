from aiogram.utils.helper import Helper, ListItem

class DialogStates(Helper):
    WAIT_NAME = ListItem()
    WAIT_AGE = ListItem()

class GameStates(Helper):
    WAIT_MOVE = ListItem()
