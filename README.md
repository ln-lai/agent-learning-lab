# Agent Learning Lab

> 我的 AI Agent 开发工程师学习日志：用代码、图解和复盘记录从 single agent 到 multi-agent system 的完整训练过程。

这个仓库不是单纯的 demo 集合，而是一个公开知识库。每个模块都会记录：

- 今天学了什么概念。
- 这个概念解决什么问题。
- 对应的最小可运行代码。
- 我的理解图、流程图和复盘。
- 后续如何升级成真实项目能力。

## Overall Progress

```text
Agent Engineer Roadmap
[###-------] 30%
```

| Phase | Topic | Status |
| --- | --- | --- |
| 01 | Single Agent basics | Streaming completed |
| 02 | Tools and multi-turn tool use | Started |
| 03 | Agent patterns: routing, judge, guardrails | Started |
| 04 | Multi-agent collaboration and memory | Not started |
| 05 | Portfolio project | Not started |

## Today

今天学习的是：

**Single Agent: Streaming events, items, and tool calls**

它也可以叫：

- streaming output
- streamed run events
- event / item inspection
- tool call event tracing

核心理解：

> `run_streamed` 不只是“字一个个出来”，更重要的是能观察 Agent 运行过程：当前 Agent、工具调用、工具输出、最终消息。

## Current Module

| Item | Path |
| --- | --- |
| Dynamic instructions note | [`notes/01_dynamic_instructions.md`](notes/01_dynamic_instructions.md) |
| Dynamic instructions practice | [`notes/01_dynamic_instructions_practice.md`](notes/01_dynamic_instructions_practice.md) |
| Streaming note | [`notes/02_streaming_events_items.md`](notes/02_streaming_events_items.md) |
| Dynamic instructions code | [`src/01_single_agent/dual_persona_agent.py`](src/01_single_agent/dual_persona_agent.py) |
| Practice code | [`src/01_single_agent/dual_persona_agent_practice.py`](src/01_single_agent/dual_persona_agent_practice.py) |
| Streaming code | [`src/01_single_agent/streaming_events_items.py`](src/01_single_agent/streaming_events_items.py) |
| Diagram 1 | [`assets/01-dynamic-instructions/code-and-flow.png`](assets/01-dynamic-instructions/code-and-flow.png) |
| Diagram 2 | [`assets/01-dynamic-instructions/full-execution-flow.png`](assets/01-dynamic-instructions/full-execution-flow.png) |

### Visual Notes

![code and flow](assets/01-dynamic-instructions/code-and-flow.png)

![full execution flow](assets/01-dynamic-instructions/full-execution-flow.png)

### Run The Code

```bash
pip install -r requirements.txt
export DEEPSEEK_API_KEY="your_key"
python src/01_single_agent/dual_persona_agent.py
```

Preview the dynamic instructions without an API key:

```bash
python src/01_single_agent/dual_persona_agent.py --dry-run
```

Practice only the context-to-instructions chain:

```bash
python src/01_single_agent/dual_persona_agent_practice.py --dry-run
```

Watch high-level streaming run items:

```bash
python src/01_single_agent/streaming_events_items.py --mode items
```

Watch raw text deltas:

```bash
python src/01_single_agent/streaming_events_items.py --mode text
```

## Learning Map

```mermaid
flowchart TD
    A["Single Agent"] --> B["Dynamic instructions"]
    B --> C["Tools"]
    C --> D["Routing / handoffs"]
    D --> E["Agents as tools"]
    E --> F["Judge / guardrails"]
    F --> G["Memory"]
    G --> H["Portfolio project"]
```

## Repository Structure

```text
assets/                 Images and diagrams
notes/                  Learning notes and reflections
src/                    Runnable practice code
```

## How I Judge Whether I Learned It

For each module, I need to be able to answer:

1. What problem does this pattern solve?
2. What are the key SDK objects?
3. What is the execution flow?
4. Can I modify the example into my own scenario?
5. Can I explain it without looking at the code?
