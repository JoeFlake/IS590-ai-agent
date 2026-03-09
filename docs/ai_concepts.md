# AI & ML Concepts Reference

## Large Language Models (LLMs)
Large Language Models are neural networks trained on massive text corpora to predict and generate text. Models like GPT-4 use the transformer architecture with self-attention mechanisms to understand context across long sequences. LLMs are pre-trained and then fine-tuned or prompted for specific tasks.

## Retrieval-Augmented Generation (RAG)
RAG combines a retrieval system with a generative model. When a query arrives, relevant documents are retrieved from a vector store and injected into the LLM prompt as context. This allows the model to answer questions based on specific, up-to-date, or private knowledge without retraining. RAG reduces hallucinations and is cheaper than fine-tuning.

## Embeddings
Embeddings are dense numerical vectors that represent text semantically. Similar meanings produce similar vectors. Embedding models (e.g., OpenAI text-embedding-3-small) convert text into high-dimensional vectors (1536 dimensions). Cosine similarity or dot product is used to compare them.

## Vector Databases
Vector databases (Chroma, FAISS, Pinecone, Weaviate) store and index embedding vectors for fast similarity search. They support approximate nearest-neighbor (ANN) search algorithms like HNSW and IVF to retrieve the top-k most similar documents quickly.

## AI Agents
AI agents use an LLM as a reasoning engine to decide which tools to call and in what order. The ReAct (Reasoning + Acting) pattern alternates between thinking and acting. Tool-calling agents (like OpenAI function-calling) are more reliable than text-based ReAct.

## Chain of Thought (CoT)
CoT prompting instructs the model to reason step-by-step before producing a final answer. Zero-shot CoT adds "Let's think step by step" to the prompt. CoT significantly improves accuracy on math and logical reasoning tasks.

## Fine-Tuning vs. Prompting
Fine-tuning updates model weights on task-specific data, improving performance but requiring compute and labeled data. Prompt engineering (few-shot, system prompts) steers existing models without any training. RAG is often preferred over fine-tuning for knowledge injection because it is cheaper and the knowledge is updatable.

## Tokens
LLMs process text as tokens (roughly 4 characters per token in English). Context window size (e.g., 128k tokens for GPT-4o) limits how much text can be processed in one call. Pricing is typically per 1,000 tokens of input and output.

## Temperature & Sampling
Temperature controls randomness in generation. Temperature=0 is deterministic (greedy decoding). Higher values (0.7–1.0) increase creativity and diversity. Top-p (nucleus sampling) and top-k restrict sampling to the most probable tokens.
