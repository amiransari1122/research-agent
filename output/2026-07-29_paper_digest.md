# Paper Digest - hallucination detection and mitigation in retrieval-augmented generation (RAG) systems
2026-07-29

Based on the provided search results, I have selected 10 papers/articles that are most relevant to the topic of hallucination detection and mitigation in retrieval-augmented generation (RAG) systems.

**Group 1: Hallucination Detection Methods**

1. **CORTEX: Token-Level Hallucination Detection in RAG via Comparative Internal Representations**
https://arxiv.org/html/2606.31033v1
CORTEX detects hallucinations in RAG systems by comparing internal representations of the model. It achieves robust localized hallucination detection through a combination of contextual residual and label-persistence smoothing.
Relevant to the topic because it proposes a novel method for hallucination detection in RAG systems.
Novelty/gap: The paper leaves open the question of how to extend CORTEX to other types of generation tasks.

2. **Lumina: Detecting Hallucinations in RAG System with Context–Knowledge Signals**
https://arxiv.org/html/2509.21875v3
Lumina detects hallucinations in RAG systems by quantifying context-knowledge signals. It outperforms prior utilization-based methods and remains robust under relaxed assumptions about retrieval quality.
Relevant to the topic because it proposes a novel framework for hallucination detection in RAG systems.
Novelty/gap: The paper does not explore the application of Lumina to other domains or tasks.

**Group 2: Hallucination Mitigation Strategies**

3. **RAG-HAT: A Hallucination-Aware Tuning Pipeline for LLM in Retrieval-Augmented Generation**
https://aclanthology.org/2024.emnlp-industry.113.pdf
RAG-HAT is a fine-tuning pipeline that combines hallucination detection and mitigation. It uses a detection model to identify hallucinations and revises the RAG output to remove them.
Relevant to the topic because it proposes a novel pipeline for hallucination mitigation in RAG systems.
Novelty/gap: The paper does not evaluate RAG-HAT on a wide range of tasks or domains.

4. **Mitigating Hallucinations in Retrieval-Augmented Generation (RAG) Systems**
https://medium.com/@nakateashwath/mitigating-hallucinations-in-retrieval-augmented-generation-rag-systems-a65880ec5505
This blog post discusses the sources of hallucinations in RAG systems and proposes a layered approach to mitigate them. It emphasizes the importance of strengthening retrieval, structuring generation, and verifying outputs.
Relevant to the topic because it provides a comprehensive overview of hallucination mitigation strategies in RAG systems.
Novelty/gap: The post does not provide a detailed evaluation of the proposed approach.

**Group 3: Retrieval-Augmented Generation**

5. **Hybrid Retrieval for Hallucination Mitigation in Large Language Models**
https://arxiv.org/html/2504.05324v1
This paper evaluates the relationship between retriever effectiveness and hallucination reduction in LLMs. It proposes a hybrid retrieval module that combines sparse and dense retrieval signals.
Relevant to the topic because it explores the impact of retrieval on hallucination mitigation in RAG systems.
Novelty/gap: The paper does not explore the application of hybrid retrieval to other tasks or domains.

6. **Retrieval-Augmented Generation and Hallucination Span Detection**
https://aclanthology.org/2025.semeval-1.151.pdf
This paper discusses the task of hallucination span detection in RAG systems. It proposes a system that leverages a RAG approach and prompting a FLAN-T5 model to identify hallucination spans.
Relevant to the topic because it explores the task of hallucination span detection in RAG systems.
Novelty/gap: The paper does not evaluate the system on a wide range of tasks or domains.

**Group 4: Applications and Evaluations**

7. **Hallucination Mitigation for Retrieval-Augmented Large Language Models**
https://www.mdpi.com/2227-7390/13/5/856
This paper reviews recent research on hallucinations in retrieval-augmented LLMs. It discusses the causes of hallucinations and corresponding mitigation methods.
Relevant to the topic because it provides a comprehensive overview of hallucination mitigation strategies in RAG systems.
Novelty/gap: The paper does not provide a detailed evaluation of the proposed approaches.

8. **GitHub - Kanisha-Shah/Hallucination-Mitigation-Using-RAG: A Columbia University capstone project focused on mitigating hallucinations in Medical Question Answering systems using Retrieval-Augmented Generation (RAG), ElasticSearch, and LLM-based validation.**
https://github.com/Kanisha-Shah/Hallucination-Mitigation-Using-RAG
This repository presents a system that uses RAG and LLM-based validation to mitigate hallucinations in medical question answering systems.
Relevant to the topic because it explores the application of RAG to a specific domain (medical question answering).
Novelty/gap: The repository does not provide a detailed evaluation of the system.

9. **ReDeEP: Detecting Hallucination in Retrieval-Augmented Generation via Mechanistic Interpretability**
https://arxiv.org/html/2410.11414v2
ReDeEP detects hallucinations in RAG systems by decoupling the model's utilization of external context and parametric knowledge. It also proposes AARF, which mitigates hallucinations by modulating the contributions of Knowledge FFNs and Copying Heads.
Relevant to the topic because it proposes a novel method for hallucination detection and mitigation in RAG systems.
Novelty/gap: The paper does not explore the application of ReDeEP to other tasks or domains.

10. **MEGA-RAG: a retrieval-augmented generation framework with ...**
https://pmc.ncbi.nlm.nih.gov/articles/PMC12540348
MEGA-RAG is a framework that mitigates hallucinations in LLMs using a combination of retrieval-augmented generation and knowledge distillation.
Relevant to the topic because it proposes a novel framework for hallucination mitigation in RAG systems.
Novelty/gap: The paper does not provide a detailed evaluation of the proposed framework.

If I were picking a thesis angle from this batch, I would focus on exploring the application of hallucination detection and mitigation strategies to specific domains or tasks, such as medical question answering or financial analysis. This could involve evaluating the effectiveness of existing methods in these domains and proposing novel approaches to address the unique challenges of each domain. For example, one could explore the use of domain-specific knowledge graphs or retrieval mechanisms to improve the accuracy of RAG systems in these domains. This angle would allow for a deep dive into the challenges and opportunities of applying RAG systems to real-world applications, and could lead to the development of more effective and reliable hallucination mitigation strategies.