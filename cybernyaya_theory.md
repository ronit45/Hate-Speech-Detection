# CyberNyaya: A Theoretical Framework for Vernacular Cyber Harassment Detection

---

## 1. Abstract
The exponential growth of internet penetration in South Asia has led to a parallel rise in digital hostility, specifically cyber harassment, cyberbullying, and criminal intimidation. Conventional natural language processing (NLP) models are traditionally trained on monolithic, grammatically structured English corpora. Consequently, these systems fail catastrophically when applied to "Hinglish"—the portmanteau of Hindi and English characterized by code-switching, Romanized transliteration, and highly contextual vernacular slang.

This project, **CyberNyaya**, presents a dual-model hybrid architecture to bridge this gap. By combining the probabilistic robustness of Multinomial Naive Bayes with the non-linear deep feature extraction of a PyTorch Multi-Layer Perceptron (MLP), the system achieves state-of-the-art precision in parsing unstructured Hinglish. Furthermore, the system autonomously maps detected threats to specific penal codes under the Bharatiya Nyaya Sanhita (BNS), automatically generating formal legal drafts to assist victims in reporting cybercrimes.

---

## 2. Introduction & Problem Statement

### 2.1 The Linguistic Challenge
Modern social media discourse in India does not adhere to standard semantic boundaries. A user is highly unlikely to type *"I am going to murder you"* in a heated exchange. Instead, threats are masked in colloquialisms, such as *"tujhe zinda gaad dunga"* or *"bahar mil tu"*. 

Existing moderation algorithms (such as standard Twitter/Meta filters) rely heavily on English-centric lexical databases (like WordNet) or massive LLMs that lack cultural context for regional dialects. When these filters encounter transliterated Hindi, they treat it as typographical errors or out-of-vocabulary (OOV) noise. 

### 2.2 The Legal Bottleneck
When a victim encounters severe cyber harassment, the bureaucratic friction involved in translating a screenshot of a Hinglish threat into a formal, legally actionable First Information Report (FIR) is immense. Victims often lack the legal literacy to identify which section of the BNS applies to their specific harassment case (e.g., distinguishing between Section 351 for Criminal Intimidation vs. Section 352 for Intentional Insult).

### 2.3 Objectives
1. **Vernacular Normalization:** To construct an NLP pipeline capable of standardizing Romanized Hindi mixed with English.
2. **Threat Stratification:** To classify text into Low, Medium, or High threat levels using deep learning (PyTorch).
3. **Legal Mapping:** To probabilistically map the normalized text to a specific Bharatiya Nyaya Sanhita (BNS) section using a statistical classifier (Naive Bayes).
4. **Automated Redressal:** To dynamically generate legally sound complaint drafts based on the classified threat.

---

## 3. System Architecture & Methodology

The system is designed as a distributed, decoupled architecture consisting of three primary layers: the Client Presentation Layer (React), the API Gateway Layer (FastAPI), and the Machine Learning Inference Engine.

### 3.1 The Machine Learning Inference Engine
The core intelligence of CyberNyaya relies on a bifurcated processing stream. Rather than forcing a single model to perform both threat-level analysis and legal classification, the system routes the preprocessed data into two specialized algorithms.

#### 3.1.1 The Multi-Layer Perceptron (PyTorch)
The MLP is tasked exclusively with understanding the *severity* of a threat. Deep neural networks excel at understanding the hierarchical relationships between features. 
- **Input:** A Term Frequency-Inverse Document Frequency (TF-IDF) vectorized array containing 2000 contextual features.
- **Hidden Layers:** The network utilizes ReLU (Rectified Linear Unit) activation functions across hidden layers (size 512, 128) to introduce non-linearity, allowing the model to learn that the phrase "I will kill you" (High Threat) is mathematically distant from "you killed that joke" (Low Threat).
- **Output:** A Softmax activation in the final layer outputs a probability distribution across three distinct classes: Low, Medium, and High.

#### 3.1.2 The Multinomial Naive Bayes Classifier
Legal classification requires strict probabilistic mapping based on word frequency. Naive Bayes operates on Bayes' Theorem, calculating the probability of a legal code given a set of words.
- **Equation:** $P(BNS | Words) \propto P(BNS) \prod P(Word_i | BNS)$
- Because specific legal offenses (like Intimidation vs. Insult) share highly specific vocabulary distributions, Naive Bayes is exceptionally efficient and less prone to overfitting on smaller, specialized legal datasets compared to deep neural networks.

---

## 4. The NLP Pipeline: Handling Code-Switching

The most critical component of the architecture is the Natural Language Processing pipeline. If raw, unstructured Hinglish is fed directly into a neural network, the model will suffer from extreme sparsity. The NLP pipeline executes the following sequential steps:

### 4.1 Tokenization and Noise Reduction
The raw text string is converted to lowercase, and all non-alphabetic characters (emojis, punctuation, special symbols) are stripped using Regular Expressions (`re`). This reduces the dimensional space of the data.

### 4.2 Vernacular Translation (The Hinglish Map)
To bridge the gap between English and Hindi, a deterministic dictionary mapping technique is employed. Common Hindi slang words are translated into their English conceptual equivalents before vectorization.
- *Example:* The word "gadha" is mapped to "idiot". The word "maar" is mapped to "kill".
By doing this, the mathematical vectors for "He is an idiot" and "Wo ek gadha hai" become identical in hyperspace, allowing the models to learn from a unified conceptual dataset rather than struggling with two distinct languages.

### 4.3 TF-IDF Vectorization
Once normalized, the text is converted into numbers using TF-IDF (Term Frequency - Inverse Document Frequency).
- **Term Frequency (TF):** Measures how frequently a word appears in a specific sentence.
- **Inverse Document Frequency (IDF):** Penalizes words that appear too frequently across the *entire* dataset (like "the", "is", "hai").
This ensures that rare, aggressive words (like "murder" or "bomb") carry massive mathematical weight, while common conversational words are ignored by the PyTorch model.

---

## 5. Adversarial Training & Edge Cases

A major theoretical hurdle in NLP is the "Contextual Blindness" of models. Early iterations of CyberNyaya suffered from false positives when encountering idioms. For example, "This weather is killing me" would be flagged as a High Threat because the model over-indexed on the word "killing."

To theoretically resolve this, the system employs **Adversarial Training**. The dataset was artificially injected with thousands of extreme edge cases:
1. **Benign Violence (Idioms):** "Shoot a video", "You killed that presentation".
2. **Context-Switches:** "This curry is bomb" vs "I will bomb your house".
By forcing the PyTorch MLP to calculate the gradients between these highly similar yet semantically opposite phrases, the neural network adjusted its internal weights to look at *n-gram combinations* (e.g., "killing me" vs "killing you") rather than isolated words. This resulted in an accuracy leap to nearly 90% in real-world messy data distributions.

---

## 6. Full-Stack Integration

### 6.1 Backend (FastAPI)
FastAPI was chosen over Flask/Django due to its asynchronous ASGI architecture and native Pydantic validation. The backend loads the serialized PyTorch (`.pt`) and Scikit-Learn (`.pkl`) models directly into RAM upon startup. When a POST request arrives, the text is routed through the NLP pipeline and fed to the RAM-cached models, resulting in inference times of under 50 milliseconds.

### 6.2 Frontend (React & Vite)
The user interface is constructed using React.js, governed by a custom utilitarian CSS design system. It handles network state (loading spinners, error boundaries) and parses the JSON response from the backend. The frontend visually translates the abstract machine learning outputs into color-coded Threat Badges (Red for High, Green for Low) and renders the final formal legal complaint draft for the user.

---

## 7. Results and Performance Metrics

The theoretical maximum accuracy of any NLP model in the wild is gated by the inherent ambiguity of human language. However, in controlled, real-world distribution testing (75% benign text, 15% toxic, 10% severe threats), the system achieved:
- **PyTorch MLP Accuracy:** 88.50%
- **Naive Bayes Accuracy:** 89.60%

These metrics indicate that the dual-model approach successfully filters out background noise (typos, conversational fillers) while maintaining a strict, aggressive mathematical boundary for genuine threats.

---

## 8. Conclusion

CyberNyaya proves that the barrier to vernacular cybercrime reporting can be entirely dismantled using applied Machine Learning. By intercepting code-switched Hinglish, applying deterministic normalization, and utilizing a bifurcated deep-learning/statistical inference engine, the system successfully bridges the gap between digital hostility and formal legal action. 

The theoretical framework established here can be trivially expanded to include other major South Asian languages (e.g., Benglish, Tanglish) simply by updating the initial dictionary normalization mapping, requiring zero changes to the underlying PyTorch architecture.
