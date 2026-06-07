"""
Module 01: Single Agent with dynamic instructions.

Goal:
    Use one Agent, but switch its behavior with runtime context.

Run:
    cd /Users/laiminzhen/Desktop/编程/agent-learning-lab
    DEEPSEEK_API_KEY="your_key" python src/01_single_agent/dual_persona_agent.py
"""

import asyncio
import argparse
import os
from dataclasses import dataclass
from typing import Literal

from openai import AsyncOpenAI
from agents import (
    Agent,
    RunContextWrapper,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)


MODEL_NAME = "deepseek-chat"


@dataclass
class StudyContext:
    persona: Literal["technical", "coach"]


def choose_persona(user_message: str) -> Literal["technical", "coach"]:
    """Choose a learning persona with simple rules.

    This is intentionally simple for learning. In a real project, this could be
    another classifier agent or a more robust intent classifier.
    """
    coach_keywords = ["焦虑", "害怕", "迷茫", "学不动", "压力", "慢", "坚持"]
    if any(keyword in user_message for keyword in coach_keywords):
        return "coach"
    return "technical"


def build_instructions(persona: Literal["technical", "coach"]) -> str:
    if persona == "technical":
        return (
            "你是一个 Agent 开发技术导师。"
            "回答要结构化，先用一句话解释核心概念，"
            "再给一个小例子，最后给一个检查理解的问题。"
        )

    return (
        "你是一个学习教练。"
        "用户可能在学习 Agent 时感到焦虑。"
        "先共情，再把问题拆成一个很小的下一步行动。"
        "语气温和、直接，不要空泛鼓励。"
    )


def dynamic_instructions(
    run_context: RunContextWrapper[StudyContext],
    agent: Agent[StudyContext],
) -> str:
    context = run_context.context
    return build_instructions(context.persona)


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


async def run_case(
    agent: Agent[StudyContext],
    user_message: str,
    dry_run: bool = False,
) -> None:
    persona = choose_persona(user_message)
    context = StudyContext(persona=persona)

    print("\n" + "=" * 72)
    print(f"User: {user_message}")
    print(f"Chosen persona: {persona}")
    print("-" * 72)

    if dry_run:
        print("Generated instructions:")
        print(build_instructions(persona))
        return

    result = await Runner.run(agent, user_message, context=context)
    print(result.final_output)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview persona selection and generated instructions without calling the model.",
    )
    args = parser.parse_args()

    if not args.dry_run:
        configure_deepseek()

    agent = Agent[StudyContext](
        name="Study Agent",
        instructions=dynamic_instructions,
        model=MODEL_NAME,
    )

    test_messages = [
        "OpenAI Agents SDK 里的 Runner.run 是做什么的？",
        "我感觉 Agent 学得有点慢，有点焦虑，怎么办？",
        "dynamic instructions 和普通 system prompt 有什么区别？",
    ]

    for message in test_messages:
        await run_case(agent, message, dry_run=args.dry_run)


if __name__ == "__main__":
    asyncio.run(main())
