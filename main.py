import asyncio
from dotenv import load_dotenv
from brain import VtuberBrain
from paths import PROJECT_ROOT

load_dotenv(PROJECT_ROOT / ".env")

if __name__ == "__main__":
    my_vtuber = VtuberBrain(local_ai=True)
    asyncio.run(my_vtuber.run())
