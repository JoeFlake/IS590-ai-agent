# Machine Learning Fundamentals

## What is Machine Learning?
Machine learning (ML) is a subfield of artificial intelligence where systems learn patterns from data rather than being explicitly programmed. A model is trained on labeled or unlabeled examples and generalizes to make predictions on new, unseen data.

## Types of Machine Learning

### Supervised Learning
The model learns from labeled training data (input-output pairs). Goal: predict output for new inputs. Common tasks: classification (predicting a category) and regression (predicting a continuous value). Algorithms: linear regression, logistic regression, decision trees, random forests, SVMs, neural networks.

### Unsupervised Learning
No labels provided. The model finds structure in data. Common tasks: clustering (grouping similar items), dimensionality reduction (compressing features), anomaly detection. Algorithms: k-means, DBSCAN, PCA, autoencoders.

### Reinforcement Learning
An agent learns by interacting with an environment and receiving rewards or penalties. Goal: maximize cumulative reward. Applications: game playing (AlphaGo), robotics, recommendation systems.

## Neural Networks
Neural networks are inspired by the brain. They consist of layers of nodes (neurons) connected by weighted edges. Each layer learns increasingly abstract representations of the input. Deep learning uses many hidden layers (deep networks) trained via backpropagation and gradient descent.

## Training Concepts

### Loss Functions
A loss function measures how wrong the model's predictions are. Common losses: Mean Squared Error (regression), Cross-Entropy (classification). Training minimizes the loss over the training set.

### Gradient Descent
An optimization algorithm that iteratively adjusts model weights in the direction that reduces the loss. Variants: Stochastic Gradient Descent (SGD), Adam, RMSProp. Learning rate controls step size.

### Overfitting and Underfitting
Overfitting: the model memorizes training data and performs poorly on new data. Underfitting: the model is too simple to capture patterns. Regularization (L1/L2), dropout, and early stopping reduce overfitting.

### Train/Val/Test Split
Data is divided into training (model learns), validation (hyperparameter tuning), and test (final evaluation) sets. Typical splits: 70/15/15 or 80/10/10. Cross-validation rotates splits for more reliable evaluation.

## Transformers
The Transformer architecture (Vaswani et al., 2017) powers modern LLMs. Self-attention allows the model to relate any token to any other token in the sequence, regardless of distance. Multi-head attention runs multiple attention heads in parallel. Transformers replaced RNNs for NLP tasks due to parallelizability and better long-range dependencies.

## Evaluation Metrics

### Classification
- **Accuracy**: fraction of correct predictions
- **Precision**: true positives / (true positives + false positives)
- **Recall**: true positives / (true positives + false negatives)
- **F1 Score**: harmonic mean of precision and recall
- **AUC-ROC**: area under the ROC curve, measures discrimination ability

### Regression
- **MAE**: Mean Absolute Error
- **RMSE**: Root Mean Squared Error
- **R²**: coefficient of determination (proportion of variance explained)

## Feature Engineering
The process of creating or transforming input variables to improve model performance. Includes normalization (scaling to [0,1]), standardization (zero mean, unit variance), one-hot encoding (categorical to binary), and handling missing values.

## Hyperparameter Tuning
Hyperparameters control training (learning rate, batch size, number of layers) and are not learned from data. Tuning methods: grid search, random search, Bayesian optimization, and automated ML (AutoML) tools.

## Transfer Learning
Reusing a model trained on one task as the starting point for another. Pre-trained models (BERT, ResNet) capture general representations that transfer well to new tasks with limited data. Fine-tuning updates some or all weights on the target task.
