# 01 Dynamic Instructions / 双人格 Agent

## 今天学的是什么

今天学的是 OpenAI Agents SDK 里的 **dynamic system prompt**，也就是动态 instructions。

普通 Agent 的 instructions 是固定字符串：

```python
Agent(
    name="Assistant",
    instructions="你是一个技术导师。",
)
```

动态 instructions 则是把一个函数传给 Agent：

```python
Agent(
    name="Study Agent",
    instructions=custom_instructions,
)
```

这样 Agent 每次运行前，都会根据本次传入的 context 动态生成真正的系统提示词。

## 为什么重要

真实 Agent 往往不是永远用同一个回答策略。

比如学习场景里：

- 用户问代码概念：应该进入技术导师模式。
- 用户表达焦虑：应该进入学习教练模式。
- 用户问职业规划：应该进入职业顾问模式。

所以这个模块的本质是：

> 同一个 Agent，根据运行上下文，切换不同的行为策略。

## 两张理解图

### 代码与逻辑流程

![code and flow](../assets/01-dynamic-instructions/code-and-flow.png)

### 完整执行流程

![full execution flow](../assets/01-dynamic-instructions/full-execution-flow.png)

## 核心对象

| Object | Meaning |
| --- | --- |
| `CustomContext` | 本次运行的上下文数据，比如风格、模式、用户状态 |
| `RunContextWrapper` | SDK 包装后的运行上下文，里面能拿到 `context` |
| `custom_instructions` | 动态生成 system prompt 的函数 |
| `Agent(...)` | 定义一个 Agent 的身份、模型、工具、交接能力 |
| `Runner.run(...)` | 真正执行一次 Agent 任务 |

## 执行流程

```text
用户输入
  -> 选择本次 context
  -> Runner.run(agent, user_message, context=context)
  -> SDK 调用 custom_instructions
  -> 根据 context 生成 system prompt
  -> LLM 根据 system prompt + user message 生成回答
  -> 返回 result.final_output
```

## 今天的练习

本仓库里的代码把官方的 `haiku / pirate / robot` 改成学习场景：

- `technical`：技术导师模式，用结构化方式解释概念。
- `coach`：学习教练模式，先处理情绪，再给行动建议。

代码路径：

```text
src/01_single_agent/dual_persona_agent.py
```

## 我现在的理解

动态 instructions 不是简单换一个 prompt 文案，而是让 Agent 的行为由运行上下文驱动。

这意味着 Agent 设计开始从“写死一个聊天机器人”进入“根据任务状态切换策略”的阶段。后面 routing、handoff、agents-as-tools 都是在这个思想上继续扩展。

## 下一步

下一步要学 streaming，让 Agent 的输出可以边生成边显示。

