import os
import traceback
import typing
import logging
# import sqlite3
import certifi
import aiohttp
import discord

from dotenv import load_dotenv

from discord.ext import commands

os.environ['SSL_CERT_FILE'] = certifi.where()
load_dotenv()

TOKEN = os.getenv("TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH")

class Client(commands.Bot):
    client: aiohttp.ClientSession

    def __init__(
        self,
        prefix: str,
        ext_dir: str = "components",
        *args: typing.Any,
        **kwargs: typing.Any
    ) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            *args,
            **kwargs,
            command_prefix=commands.when_mentioned_or(prefix),
            intents=intents
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ext_dir = ext_dir
        self.synced = False

    async def _load_extensions(self) -> None:
        if not os.path.isdir(self.ext_dir):
            self.logger.error(f"Extension directory {self.ext_dir} does not exist.")
            return
        for filename in os.listdir(self.ext_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                try:
                    await self.load_extension(f"{self.ext_dir}.{filename[:-3]}")
                    self.logger.info(f"Loaded extension {filename[:-3]}")
                except commands.ExtensionError:
                    self.logger.error(f"Failed to load extension {filename[:-3]}\n{traceback.format_exc()}")

    async def on_error(self, event_method: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.logger.error(f"An error occurred in {event_method}.\n{traceback.format_exc()}")

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as {self.user} ({self.user.id})")

    async def setup_hook(self) -> None:
        self.client = aiohttp.ClientSession()
        await self._load_extensions()
        if not self.synced:
            await self.tree.sync()
            self.synced = not self.synced
            self.logger.info("Synced command tree")


# def database() -> None:
#     connection = sqlite3.connect(DATABASE_PATH)
#     cur = connection.cursor()

#     TABLE = '''
#             CREATE TABLE IF NOT EXISTS user_data (
#                 discord_id INTEGER PRIMARY KEY,
#             );
#             '''

#     try:
#         cur.execute(TABLE)
#     except sqlite3.Error as e:
#         print(e.message)
#     finally:
#         cur.close()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
    bot = Client(prefix="!", ext_dir="components")

    bot.run(TOKEN)

if __name__ == "__main__":
    # print(os.path.exists(DATABASE_PATH))
    # database()
    main()