# Machine Learning Fundamentals — Surf Edition

Yo, machine learning is basically teaching a computer to surf. You don't write out every rule — you just throw it in the water thousands of times until it figures out how to ride. Let's break it down, dude.

## What is Machine Learning?

Machine learning (ML) is a subset of AI where systems learn patterns from data instead of being explicitly programmed. Given enough examples, an ML model finds the underlying structure and generalizes to new inputs.

Three pillars:
1. **Data** — the ocean of examples you learn from
2. **Model** — the algorithm that finds patterns
3. **Training** — the process of optimizing the model on your data

## Types of Machine Learning

### Supervised Learning
You give the model labeled input-output pairs. It learns the mapping.

- **Classification** — predict a category (is this wave surfable? yes/no)
- **Regression** — predict a number (how tall will this wave be?)

Examples: linear regression, decision trees, neural networks, SVMs.

### Unsupervised Learning
No labels — the model finds structure on its own.

- **Clustering** — group similar things (grouping waves by shape/size)
- **Dimensionality reduction** — compress data while keeping meaning (PCA, embeddings)

### Reinforcement Learning
An agent takes actions in an environment and receives rewards or penalties. It learns to maximize reward over time.

Like teaching a surfbot to ride waves by giving it +10 points for staying upright and -5 for wiping out. Eventually it figures out the moves.

## The Training Process

1. **Initialize** — start with random weights
2. **Forward pass** — run data through the model, get predictions
3. **Calculate loss** — measure how wrong the predictions are
4. **Backpropagation** — calculate how much each weight contributed to the error
5. **Update weights** — move weights in the direction that reduces loss (gradient descent)
6. **Repeat** — thousands of times over your dataset

**Epoch** = one full pass through the training data.
**Batch size** = how many samples per gradient update.
**Learning rate** = how big the weight update steps are. Too high = overshoots. Too low = takes forever.

## Key Concepts

### Gradient Descent
The optimization algorithm that updates model weights. You're always moving downhill on the loss surface — like water finding the lowest point on the beach.

Variants:
- **SGD** — stochastic gradient descent, one sample at a time
- **Mini-batch SGD** — batches of samples (most common)
- **Adam** — adaptive learning rates per parameter (the gnarly modern default)

### Overfitting vs Underfitting
- **Overfitting** — memorized the training data but fails on new data. Like a surfer who can only ride one specific wave shape.
- **Underfitting** — model too simple to capture the pattern. Like trying to surf with a boogie board when you need a longboard.
- **Generalization** — the goal: performs well on unseen data.

Fixes for overfitting: more data, dropout, regularization (L1/L2), early stopping.

### Train / Validation / Test Split
- **Training set** — what the model learns from (~70-80%)
- **Validation set** — used to tune hyperparameters and catch overfitting (~10-15%)
- **Test set** — final evaluation, touch it only once (~10-15%)

Never let your model see the test set during training. That's the ultimate wipeout.

### Hyperparameters vs Parameters
- **Parameters** — learned during training (weights, biases). The model owns these.
- **Hyperparameters** — set by you before training (learning rate, batch size, number of layers). You tune these.

## Neural Networks

A neural network is a function approximator built from layers of connected nodes (neurons).

```
Input → [Hidden Layer 1] → [Hidden Layer 2] → Output
```

Each neuron:
1. Computes a weighted sum of its inputs
2. Adds a bias term
3. Applies an activation function (ReLU, sigmoid, tanh)

**ReLU** (Rectified Linear Unit) is the most common: `f(x) = max(0, x)`. Simple and works great.

### Deep Learning
Neural networks with many hidden layers. "Deep" = lots of layers. Excels at images, text, audio. Requires lots of data and compute — but rides the gnarliest waves.

## Transformers

The architecture behind modern LLMs (GPT, Claude, Gemini). Key innovation: the **attention mechanism**.

Attention lets the model focus on relevant parts of the input when generating each output token — like how a good surfer watches the wave behind them while paddling forward.

**Self-attention** — every token attends to every other token in the sequence.
**Multi-head attention** — multiple attention patterns in parallel, each capturing different relationships.

## Evaluation Metrics

| Task | Metrics |
|---|---|
| Classification | Accuracy, Precision, Recall, F1, AUC-ROC |
| Regression | MSE, RMSE, MAE, R² |
| Language Models | Perplexity, BLEU, ROUGE |
| Ranking/Retrieval | MRR, NDCG, Recall@K |

## Feature Engineering

Before deep learning, most of ML was about crafting good input features. Even now it matters:
- Normalize numerical features (zero mean, unit variance)
- Encode categoricals (one-hot, label encoding, embeddings)
- Handle missing values (imputation, indicators)
- Create interaction features when domain knowledge suggests them

Chicken Joe tip: garbage in, garbage out. Even the sickest model can't surf on a polluted beach.
