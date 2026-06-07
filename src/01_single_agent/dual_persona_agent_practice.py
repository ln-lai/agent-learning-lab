"""
Practice 01: Dynamic instructions / dual persona agent.

This file is intentionally a practice scaffold.
Fill the TODO parts one by one, then run:

    python src/01_single_agent/dual_persona_agent_practice.py --dry-run

Goal:
    Understand this sentence:
    Dynamic system prompt = generate instructions from runtime context
    right before the Agent runs.
"""

import argparse
import asyncio
from dataclasses import dataclass
from typing import Literal

from agents import Agent, RunContextWrapper


# TODO 1:
# Define the runtime context.
# It should store one field: persona.
# persona can only be "technical" or "coach".
@dataclass
class StudyContext:
    persona: Literal["technical", "coach"]


def choose_persona(user_message: str) -> Literal["technical", "coach"]:
    """Choose which persona this run should use."""
    # TODO 2:
    # If the user sounds anxious, return "coach".
    # Otherwise, return "technical".
    anxious_keywords = ["焦虑", "迷茫", "压力", "慢", "学不动"]
    if any(keyword in user_message for keyword in anxious_keywords):
        return "coach"
    return "technical"


def build_instructions(persona: Literal["technical", "coach"]) -> str:
    """Generate the actual instructions for this run."""
    # TODO 3:
    # Return different system prompts for different personas.
    if persona == "technical":
        return "你是一个 Agent 技术导师。请用结构化方式解释概念。"
    return "你是一个学习教练。请先共情，再给一个很小的下一步行动。"


def dynamic_instructions(
    run_context: RunContextWrapper[StudyContext],
    agent: Agent[StudyContext],
) -> str:
    """The SDK calls this before running the Agent."""
    context = run_context.context
    return build_instructions(context.persona)


def preview_case(user_message: str) -> None:
    persona = choose_persona(user_message)
    context = StudyContext(persona=persona)

    print("\n" + "=" * 72)
    print(f"User: {user_message}")
    print(f"Context: {context}")
    print(f"Generated instructions: {build_instructions(context.persona)}")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.dry_run:
        print("This practice file only supports --dry-run for now.")
        return

    test_messages = [
        "Runner.run 是做什么的？",
        "我感觉学得很慢，有点焦虑。",
        "dynamic instructions 和普通 prompt 有什么区别？",
    ]

    for message in test_messages:
        preview_case(message)


if __name__ == "__main__":
    asyncio.run(main())

