"""
Module 02: Streaming events, items, and tool calls.

Goal:
    Use Runner.run_streamed() to watch an Agent run as a stream of events.

Run:
    cd /Users/laiminzhen/Desktop/编程/agent-learning-lab
    DEEPSEEK_API_KEY="your_key" python src/01_single_agent/streaming_events_items.py
"""

import argparse
import asyncio
import os
import random

from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from agents import (
    Agent,
    ItemHelpers,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)


MODEL_NAME = "deepseek-chat"


@function_tool
def how_many_examples() -> int:
    """Return a random number of examples to explain."""
    return random.randint(2, 4)


def configure_deepseek() -> None:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise ValueError("Please set DEEPSEEK_API_KEY before running this file.")

    client = AsyncOpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key=api_key,
    )

    set_default_openai_client(client=client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(disabled=True)


async def run_text_stream(agent: Agent) -> None:
    """Print text deltas as soon as the model generates them."""
    print("\n=== Text delta stream ===")
    result = Runner.run_streamed(
        agent,
        input="用简单中文解释 event 和 item 的区别。",
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    print("\n=== Text stream complete ===")


async def run_item_stream(agent: Agent) -> None:
    """Ignore raw text deltas and print higher-level Agent run items."""
    print("\n=== Run item stream ===")
    result = Runner.run_streamed(
        agent,
        input="先调用工具决定例子数量，再解释 run_streamed。",
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue

        if event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue

        if event.type != "run_item_stream_event":
            continue

        if event.item.type == "tool_call_item":
            tool_name = getattr(event.item.raw_item, "name", "Unknown Tool")
            print(f"-- Tool was called: {tool_name}")
        elif event.item.type == "tool_call_output_item":
            print(f"-- Tool output: {event.item.output}")
        elif event.item.type == "message_output_item":
            text = ItemHelpers.text_message_output(event.item)
            print(f"-- Message output:\n{text}")

    print("=== Run item stream complete ===")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["text", "items"],
        default="items",
        help="text shows raw text deltas; items shows higher-level Agent events.",
    )
    args = parser.parse_args()

    configure_deepseek()

    agent = Agent(
        name="Streaming Study Agent",
        instructions=(
            "你是一个 OpenAI Agents SDK 学习教练。"
            "解释要简单直接，优先用中文和生活类比。"
            "如果任务要求调用工具，请先调用工具再回答。"
        ),
        model=MODEL_NAME,
        tools=[how_many_examples],
    )

    if args.mode == "text":
        await run_text_stream(agent)
    else:
        await run_item_stream(agent)


if __name__ == "__main__":
    asyncio.run(main())
