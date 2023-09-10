from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from data.config import BOT_TOKEN
from utils.api import FastAPIClient

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
api_client = FastAPIClient()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
