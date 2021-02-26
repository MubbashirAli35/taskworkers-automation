import asyncio
import aiologger
from aiologger import Logger


async def log():
    logger = Logger.with_default_handlers(name='my-logger')

    await logger.debug("debug")
    await logger.info("info")

    await logger.warning("warning")
    await logger.error("error")
    await logger.critical("critical")

    await logger.shutdown()

if __name__ == '__main__':
    asyncio.run(log())
