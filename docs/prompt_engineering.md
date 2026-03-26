# Prompt Engineering — How to Talk to an AI, Bro

Dude, prompt engineering is like knowing how to read the ocean before you paddle out. You can have the best board (LLM) in the world, but if you position yourself wrong, you're gonna eat it. Let me break down how to craft prompts that actually shred.

## What is Prompt Engineering?

Prompt engineering is the practice of designing inputs to LLMs to get better, more reliable outputs. Since LLMs are sensitive to how questions are phrased, small changes in your prompt can dramatically change the response.

It's part art, part science, and part vibe.

## Core Techniques

### Zero-Shot Prompting
Just ask directly with no examples. Works for simple, well-defined tasks.

```
Prompt: "Translate 'hang loose' to Spanish."
Response: "Quédate relajado / Relájate"
```

### Few-Shot Prompting
Give the model a few examples before your actual question. This sets the pattern.

```
Prompt:
Wave height 2ft → vibe: totally mellow, great for beginners
Wave height 8ft → vibe: gnarly, intermediate surfers only
Wave height 20ft → vibe: ???

Response: "Absolutely radical, experts only, Chicken Joe territory"
```

Few-shot prompting dramatically improves consistency and format adherence.

### Chain-of-Thought (CoT)
Tell the model to reason step by step before giving an answer. Dramatically improves performance on math, logic, and multi-step problems.

```
Prompt: "Think step by step. If Chicken Joe rides 4 waves per hour for 3 hours,
and each wave earns him 15 style points, how many total style points does he have?"

Response:
Step 1: Waves per hour = 4, hours = 3
Step 2: Total waves = 4 × 3 = 12
Step 3: Style points = 12 × 15 = 180
Answer: 180 style points, dude!
```

You can trigger CoT with phrases like "Let's think step by step" or "Reason through this carefully."

### System Prompts
In chat models, the system prompt sets the persona, constraints, and behavior of the assistant. It's like the briefing before you paddle out.

```
System: You are Chicken Joe, a laid-back surfing chicken who helps users with 
math, web searches, and AI knowledge. You speak casually, use surf slang, 
and always stay stoked. When using RAG results, cite your sources.
```

A strong system prompt reduces the need for complex per-message instructions.

### Role Prompting
Tell the model to take on a specific expert role.

```
"You are a professional wave forecaster with 20 years of experience..."
"Act as a LangChain expert explaining agents to a beginner..."
```

Role prompting activates relevant knowledge and affects tone/style.

## Prompt Structure Best Practices

### Be Specific and Clear
Vague prompts = vague answers. Tell the model exactly what you want.

❌ "Tell me about waves."
✅ "Explain the difference between beach break and reef break waves, including how each affects surfing technique. Keep it under 200 words."

### Specify the Output Format
If you need JSON, a list, a table, or a specific structure — ask for it explicitly.

```
"Return your answer as a JSON object with keys: wave_type, difficulty, best_board_length"
```

### Set Constraints
- Length: "In 3 sentences or fewer..."
- Audience: "Explain this to someone who has never surfed..."
- Tone: "Be casual and enthusiastic..."
- Scope: "Only use information from the provided documents..."

### Provide Context
The more relevant context you give the model, the better it performs. This is the foundation of RAG — giving the model the right documents to work from.

## Prompt Engineering for Agents

When building agents (like Chicken Joe's Surf Shack), the system prompt has extra jobs:

1. **Define the tools and when to use them**
   ```
   You have access to:
   - calculator: for math expressions
   - web_search: for current events and live information
   - rag_search: for internal knowledge base questions
   Use the most appropriate tool for each query.
   ```

2. **Set citation behavior for RAG**
   ```
   When answering from rag_search results, always include [Source: filename] 
   in your response so the user knows where the information came from.
   ```

3. **Handle tool failures gracefully**
   ```
   If a tool returns an error, tell the user what happened and try an 
   alternative approach if possible.
   ```

## Common Pitfalls

- **Prompt injection** — user input that overrides your system prompt. Sanitize inputs, especially in production.
- **Hallucination from underconstrained prompts** — if you don't tell it to stay grounded, it'll make stuff up. Use RAG and cite sources.
- **Format drift** — long conversations cause the model to drift from its initial instructions. Periodically reinforce format requirements.
- **Token limits** — system prompts + history + tools + response all eat tokens. Keep prompts lean but complete.

## Iterative Prompt Development

Treat your system prompt like your surfboard shape — you iterate until it's dialed in:

1. Start simple
2. Test on representative inputs
3. Identify failure modes
4. Add specific instructions to address each failure
5. Test again
6. Repeat until it shreds

Version control your prompts (they're code, bro). Document what you changed and why.

## Temperature and Sampling

- **temperature=0** — deterministic, always picks the most likely next token. Best for facts, code, math.
- **temperature=0.7** — creative, varied outputs. Good for writing, brainstorming.
- **temperature=1.0+** — very creative/random. Use carefully or things get weird.
- **top_p** — nucleus sampling, alternative to temperature. Controls diversity differently.

For an agent answering factual questions, `temperature=0` is the move. No rogue waves.
