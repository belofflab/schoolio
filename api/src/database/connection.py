import databases
from src.data.config import DATABASE_URL

database = databases.Database(DATABASE_URL)
