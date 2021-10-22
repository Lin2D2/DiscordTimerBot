from package.bot import Bot
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    bot = Bot()
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
