# 01 Dynamic Instructions Practice

这一节先不要追求多写代码，只练一句话：

> 动态 system prompt = 运行 Agent 之前，根据上下文临时生成 instructions。

## 练习文件

```text
src/01_single_agent/dual_persona_agent_practice.py
```

## 练习目标

你需要能亲手解释这 3 个点：

1. `StudyContext` 保存本次运行的状态。
2. `choose_persona()` 根据用户输入决定本次用哪个人格。
3. `dynamic_instructions()` 根据 context 生成本次真正交给模型的 instructions。

## 先跑 dry-run

```bash
python src/01_single_agent/dual_persona_agent_practice.py --dry-run
```

你应该看到类似链路：

```text
User: 我感觉学得很慢，有点焦虑。
Context: StudyContext(persona='coach')
Generated instructions: 你是一个学习教练。请先共情，再给一个很小的下一步行动。
```

## 真正要吃透的问题

这段代码里，用户输入没有直接变成 system prompt。

它先经过：

```text
user_message -> choose_persona -> StudyContext -> dynamic_instructions -> instructions
```

所以“动态”不是模型自己变聪明了，而是我们在运行前把状态传进去，让 Agent 根据状态生成不同的系统指令。

## 你练完之后要能回答

1. `StudyContext` 是给谁看的？
2. `choose_persona()` 和 `dynamic_instructions()` 分别负责什么？
3. 为什么不直接在 prompt 里写“如果用户焦虑就安慰他”？

