import asyncio
from planner.MetroPlanner import MetroPlanner

async def main():
    planner = MetroPlanner()
    input_text = "Train breakdown at Redhill Station"
    messages = await planner.run(input_text)

    for i, msg in enumerate(messages, 1):
        print(f"\n{i}. [{msg['name']}]")
        print(msg['content'])

asyncio.run(main())
