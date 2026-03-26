# AI Concepts — Explained by Chicken Joe

Duuude, welcome to the gnarliest AI knowledge shack on the beach. I'm Chicken Joe, and I'm gonna break down these AI concepts like I break down waves — stoked and totally chill.

## What is Artificial Intelligence?

AI is like surfing, bro. You train and train until you can read the ocean without even thinking about it. AI systems learn patterns from data so they can make decisions, answer questions, or do tasks — just like how I learned to shred waves by watching the pros.

Artificial Intelligence refers to machines that simulate human-like reasoning. It covers everything from rule-based systems to deep learning neural networks.

## Machine Learning

Machine learning is when the AI learns FROM the data instead of being told every rule. Like, nobody told me exactly how to balance on a board — I just wiped out a thousand times until my body figured it out. That's machine learning, dude.

Types of machine learning:
- **Supervised learning** — you give it labeled examples (like showing me footage of good vs bad surfing)
- **Unsupervised learning** — it finds patterns on its own (like figuring out wave types with no coaching)
- **Reinforcement learning** — it learns by trial and error with rewards (like getting stoked when I nail a trick)

## Neural Networks

Neural networks are modeled after the human brain, bro. They've got layers of neurons that pass signals around. Each layer learns something more complex than the last — kind of like how you first learn to paddle, then stand, then turn, then do aerials.

- **Input layer** — receives raw data (like wave height, wind speed)
- **Hidden layers** — process and transform the data
- **Output layer** — produces the final answer or prediction

## Large Language Models (LLMs)

LLMs like GPT are trained on massive amounts of text — like if you read every surf magazine, every ocean science book, and every beach blog ever written. They predict the next word, over and over, until they can hold a full conversation.

Key LLM concepts:
- **Parameters** — the weights the model learned (billions of them, bro)
- **Context window** — how much text it can hold in its head at once
- **Temperature** — how creative/random vs precise the output is
- **Tokens** — chunks of text the model processes (roughly 3/4 of a word each)

## The ReAct Pattern

ReAct stands for Reasoning + Acting. It's the pattern where an AI agent thinks step by step AND uses tools to get real information, not just vibes from training data.

The loop goes like this:
1. **Thought** — the agent thinks about what it needs
2. **Action** — it calls a tool (calculator, web search, RAG, etc.)
3. **Observation** — it sees the result
4. **Repeat** — until it has enough to answer

It's like how I surf: I look at the wave (thought), I paddle and position (action), I feel how the board responds (observation), and I adjust. ReAct is just surfing, dude.

## Embeddings

Embeddings are how AI turns words into numbers that capture meaning. Similar words end up close together in a high-dimensional space. "Surfboard" and "longboard" would be near each other. "Tax forms" would be very, very far away.

Embeddings power semantic search — finding documents by meaning, not just keyword matching.

## RAG — Retrieval-Augmented Generation

RAG is when you give the LLM access to a knowledge base at query time. Instead of relying only on its training data, it:
1. Embeds your question
2. Finds the most relevant documents (vector similarity search)
3. Feeds those docs into the prompt
4. Generates an answer grounded in real sources

RAG is like asking me a surf question and I go grab the actual tide charts before answering, rather than just guessing based on vibes. Way more accurate, bro.

## Hallucination

Hallucination is when an AI confidently makes stuff up. Like if I told you a wave was 80 feet tall when it was actually 6 feet — I believed it, but it was wrong. LLMs do this when they don't know something but fill in the gap with plausible-sounding nonsense.

RAG reduces hallucination by grounding answers in actual documents.

## Agents

An AI agent is an LLM that can take actions in the world — calling APIs, running tools, searching the web. Instead of just generating text, it can DO things. Chicken Joe's Surf Shack is an agent with three tools: Calculator, Web Search, and RAG. Totally tubular.
