# start.py
import asyncio
import test_izlabot
import test_yukla

async def main():
    await asyncio.gather(
        test_izlabot.main(),
        test_yukla.main()
    )

if __name__ == "__main__":
    asyncio.run(main())
