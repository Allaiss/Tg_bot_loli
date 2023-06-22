from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from datetime import datetime
from random import sample
import os

from transport import *
from utils import *
from const import *


bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
users_data = {}

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await bot.send_message(msg.from_user.id, START_MSG)

@dp.message_handler(commands=["my_age"])
async def hello(msg: types.Message):
    uid = msg.from_user.id
    if uid in users_data and users_data[uid]["age"]:
        await bot.send_message(uid, MY_AGE_MSG.format(users_data[uid]["name"], users_data[uid]["age"]))
    else:
        await bot.send_message(uid, MY_AGE_404_MSG)

@dp.message_handler(commands=["hello"])
async def my_age(msg: types.Message):
    await bot.send_message(msg.from_user.id, HELLO_START_MSG)
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(DialogStates.WAIT_NAME[0])

@dp.message_handler(commands=["help"])
async def help(msg: types.Message):
    await bot.send_message(msg.from_user.id, get_help())

@dp.message_handler(commands=["time"])
async def clock(msg: types.Message):
    time = datetime.now().time()
    await bot.send_message(msg.from_user.id, str(time)[:8])

@dp.message_handler(commands=["calc"])
async def calc(msg: types.Message):
    arg = msg.get_args()
    await bot.send_message(msg.from_user.id, eval(arg))

@dp.message_handler(commands=["year"])
async def year(msg: types.Message):
    arg = msg.get_args()
    ans = get_year_info(arg)
    if ans is None:
        await bot.send_message(msg.from_user.id, ERR)
    else:
        await bot.send_message(msg.from_user.id, ans)

@dp.message_handler(commands=["quiz"])
async def quiz(msg: types.Message):
    ans = get_question(1)
    if ans is None:
        await bot.send_message(msg.from_user.id, ERR)
    else:
        for q in ans:
            text = "Вопрос: " + q["question"] + "\n"
            text += "Ответ: " + q["answer"]
            await bot.send_message(msg.from_user.id, text)

@dp.message_handler(commands=["dog"])
async def dog(msg: types.Message):
    ans = get_dog()
    if ans is None:
        await bot.send_message(msg.from_user.id, ERR)
    else:
        await bot.send_message(msg.from_user.id, ans)

@dp.message_handler(commands=["fox"])
async def fox(msg: types.Message):
    ans = get_fox()
    if ans is None:
        await bot.send_message(msg.from_user.id, ERR)
    else:
        await bot.send_message(msg.from_user.id, ans)

@dp.message_handler(commands=["game"])
async def game(msg: types.Message):
    uid = msg.from_user.id
    if uid not in users_data:
        users_data[uid] = {}
    users_data[uid]["bc"] = "".join(sample("1234567890", 4))
    await bot.send_message(msg.from_user.id, GAME_START_MSG)
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(GameStates.WAIT_MOVE[0])

@dp.message_handler(commands=["love"])
async def love(msg: types.Message):
    await bot.send_message(msg.from_user.id, ILU)

@dp.message_handler()
async def echo(msg: types.Message):
    await bot.send_message(msg.from_user.id, f"{msg.text}")

@dp.message_handler(state=DialogStates.WAIT_NAME)
async def wait_name(msg: types.Message):
    uid = msg.from_user.id
    if uid not in users_data:
        users_data[uid] = {}
    users_data[uid]["name"] = msg.text
    await bot.send_message(uid, HELLO_NAME_MSG.format(msg.text))
    state = dp.current_state(user=uid)
    await state.set_state(DialogStates.WAIT_AGE[0])

@dp.message_handler(state=DialogStates.WAIT_AGE)
async def wait_age(msg: types.Message):
    uid = msg.from_user.id
    try:
        a = int(msg.text)
        assert 0 < a < 200
        users_data[uid]["age"] = a
        await bot.send_message(uid, HELLO_AGE_COMPLETE_MSG.format(msg.text))
        state = dp.current_state(user=uid)
        await state.set_state()
    except Exception:
        await bot.send_message(uid, HELLO_AGE_ERROR_MSG)

@dp.message_handler(state=GameStates.WAIT_MOVE[0])
async def wait_move(msg: types.Message):
    uid = msg.from_user.id
    try:
        if msg.text == "exit":
            await bot.send_message(uid, GAME_OVER_MSG)
            state = dp.current_state(user=uid)
            await state.set_state()
            return
        num = (msg.text)
        ans = users_data[uid]["bc"]
        b, c = 0, 0
        for i in range(4):
            if num[i] == ans[i]:
                b += 1
            elif num[i] in ans:
                c += 1
        if b == 4:
            await bot.send_message(uid, WIN_MSG)
            state = dp.current_state(user=uid)
            await state.set_state()
        else:
            await bot.send_message(uid, GAME_CONTINUE_MSG.format(b, c))
    except Exception:
        await bot.send_message(uid, GAME_ERR_MSG)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

