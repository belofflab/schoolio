from aiogram import executor
from loader import dp

if __name__ == '__main__':
  import handlers
  executor.start_polling(dp)