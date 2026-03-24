# Prompt Engineering Reference

## What is Prompt Engineering?
Prompt engineering is the practice of designing inputs to LLMs to elicit desired outputs. It is a critical skill for using foundation models effectively without fine-tuning. Good prompts are clear, specific, and structured.

## Zero-Shot Prompting
Asking the model to perform a task with no examples. Works well for tasks within the model's training. Example: "Translate the following sentence to French: 'The sky is blue.'"

## Few-Shot Prompting
Providing 2–10 examples of input-output pairs before the actual query. This demonstrates the format and style of desired responses. Few-shot prompting is especially useful for classification, extraction, and format-constrained outputs.

## Chain of Thought (CoT) Prompting
Instructing the model to reason step by step before giving a final answer. Dramatically improves performance on math, logic, and multi-step reasoning tasks.
- **Zero-shot CoT**: Add "Let's think step by step." to the prompt
- **Manual CoT**: Provide full reasoning chains as few-shot examples

## System Prompts
In chat models, the system message sets the role, persona, constraints, and capabilities of the assistant before any conversation begins. System prompts are processed first and have strong influence on model behavior throughout the conversation.

## Role Prompting
Assigning a persona to the model: "You are an expert Python developer..." Role prompting shifts the model's tone, vocabulary, and approach to match the specified persona.

## Instruction Clarity
Vague prompts produce vague outputs. Best practices:
- Be explicit about output format (JSON, bullet list, paragraph)
- Specify length constraints ("in 2-3 sentences")
- Define what to do AND what not to do
- Use delimiters (triple backticks, XML tags) to separate instructions from content

## Prompt Injection and Safety
Prompt injection is when user input manipulates the model's behavior by embedding instructions in the input. Defenses: input sanitization, separating instructions from user content, reinforcing the system prompt with assertions.

## Structured Output
Modern LLMs support JSON mode and structured output via function calling / tool schemas. This guarantees the model returns valid JSON conforming to a schema, eliminating parsing failures. LangChain's `with_structured_output` wraps this pattern.

## Temperature and Prompt Interaction
Low temperature (0–0.2) works best for factual, deterministic tasks. Higher temperature (0.7–1.0) is better for creative, generative tasks. Prompts that say "be creative" or "explore ideas" pair with higher temperature; prompts that say "be precise" pair with lower temperature.

## ReAct Prompting
ReAct (Reasoning + Acting) is a prompting strategy for agents. The model is prompted to interleave Thought (reasoning), Action (tool call), and Observation (result) steps. This creates a traceable reasoning loop that is more reliable than asking the model to solve complex tasks in a single response.

## Prompt Chaining
Breaking complex tasks into a sequence of simpler prompts where each output feeds the next. Reduces hallucination and makes errors easier to debug. LangChain's LCEL is designed around this pattern.

## Common Pitfalls
- **Ambiguous instructions**: model picks one interpretation, often wrong
- **Overloaded prompts**: too many instructions cause the model to drop some
- **Negative instructions only**: "Don't do X" is less effective than "Do Y instead"
- **No output format spec**: model output is unpredictable, hard to parse downstream
- **Assuming world knowledge**: for recent events or private data, always retrieve and inject context
