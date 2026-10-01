# Recommended Base Papers for MindCare AI

**Purpose:** Select and justify a defensible research base for the MindCare AI final-year project.  
**Project fit:** Multilingual mental-wellness prototype combining RAG/LLM chat, text classifiers, crisis/privacy-oriented controls, and wellness features.  
**Recommendation:** Use **one primary base paper** and cite the other papers as supporting literature. Do not describe all four as the project’s base papers.

## 1. What a “base paper” should do

A base paper is the main scholarly work that motivates and frames the project. It should have a clear connection to the problem and methods, help establish the research gap, and give a comparison point for the project’s contribution. It does **not** mean the project must reproduce the paper, use its datasets or weights, or achieve its reported results. Those connections must be stated accurately and supported by the paper itself.

For MindCare AI, the most defensible base-paper framing is **RAG-based conversational mental-health support**, with task-specific transformer classifiers and multilingual wellness features presented as this project’s implementation choices and extensions.

## 2. Shortlist and recommendation

### Paper 1 — Recommended primary base paper

**Dutta, A., Mruthyunjaya, S., Saddington, J., & Islam, K. S. (2025). _Mentalic Net: Development of RAG-based Conversational AI and Evaluation Framework for Mental Health Support._** arXiv:2509.04456. https://arxiv.org/abs/2509.04456

**Why it fits:** This is the closest match to the project’s central research problem: using retrieval-augmented conversational AI for mental-health support. It provides a direct conceptual basis for the RAG + prompt-guided response approach and makes evaluation and responsible use relevant to the project discussion.

**How MindCare AI relates:** MindCare AI implements its own local FAISS retrieval pipeline, Ollama-based generation, classifier signals, language-aware prompts, safety/privacy processing, and application features. Describe Mentalic Net as a **conceptual and architectural reference**; do not claim to reproduce it or inherit its results/data.

**Defense-friendly point:** “We selected this paper because it addresses the same broad problem—RAG-based conversational support for mental health. Our implementation is a separate prototype with local retrieval, task-specific classifiers, and English/Urdu/Roman Urdu interaction. We evaluate our components separately and do not claim the paper’s reported score as our own.”

**Caution:** Verify final venue/citation details against the published proceedings if citing a conference version. The project’s existing research notes say the abstract reports RAG, prompt engineering, fine-tuning and a BERTScore of 0.898; do not attribute dataset names, exact model architecture, or detailed metrics unless verified in the full paper.

### Paper 2 — RAG method foundation

**Lewis, P., et al. (2020). _Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks._** Advances in Neural Information Processing Systems (NeurIPS). https://arxiv.org/abs/2005.11401

**Why it fits:** This is a foundational RAG paper explaining the general retrieve-then-generate method. It supports the methodological explanation of retrieving external passages and conditioning a generator on that evidence.

**How MindCare AI relates:** The project uses a local vector index and a configured local language model. It is an application of the general RAG idea, not necessarily the exact architecture, training procedure, or experimental setup in Lewis et al.

**Defense-friendly point:** “Lewis et al. explain the general RAG method; our project applies that principle to a curated mental-health knowledge collection. Retrieval can provide relevant context, but it does not guarantee that generated advice is correct or safe.”

### Paper 3 — Mental-health chatbot evidence and limitations

**Abd-Alrazaq, A. A., et al. (2020). _Effectiveness and Safety of Using Chatbots to Improve Mental Health: Systematic Review and Meta-Analysis._** Journal of Medical Internet Research, 22(7), e16021. https://doi.org/10.2196/16021

**Why it fits:** It provides domain context for mental-health chatbots, including evidence and safety considerations. This helps justify why the project is framed as a wellness-support prototype and why claims about effectiveness, safety, and clinical use must be cautious.

**How MindCare AI relates:** This is supporting evidence, not a technical blueprint for the project’s RAG pipeline or classifiers. Use it to situate the problem and discuss the importance of evaluating benefits and risks; do not imply that the review validates MindCare AI.

**Defense-friendly point:** “Existing chatbot research makes evaluation and safety important, but evidence about other systems cannot establish that our prototype is clinically effective. We therefore describe it as assistive wellness support, not diagnosis or treatment.”

### Paper 4 — Transformer classifier foundation

**Liu, Y., et al. (2019). _RoBERTa: A Robustly Optimized BERT Pretraining Approach._** arXiv:1907.11692. https://arxiv.org/abs/1907.11692

**Why it fits:** The project’s task-specific emotion, stress, and depression classifiers are documented as fine-tuned RoBERTa-based models. This paper supports explaining the pretrained transformer backbone used for those classification experiments.

**How MindCare AI relates:** MindCare AI fine-tunes task-specific classifiers on its selected datasets. RoBERTa is a model foundation, not a mental-health diagnosis method, and the paper does not validate the project’s datasets, classifier metrics, or clinical use.

**Defense-friendly point:** “RoBERTa provides the pretrained language-model backbone. We fine-tune separate task heads/models for our selected text-classification tasks and report their held-out dataset results independently; these outputs are not clinical diagnoses.”

## 3. Which one should we choose?

**Recommended primary base paper: Mentalic Net (Paper 1).** It is the closest domain-and-method match to MindCare AI’s central conversational RAG system. Use Lewis et al. as the technical foundation for RAG, Abd-Alrazaq et al. for mental-health chatbot context and responsible interpretation, and Liu et al. for the classifier backbone.

This gives a clear hierarchy for the report and viva:

1. **Primary base:** Mentalic Net — mental-health conversational RAG system.
2. **Method support:** Lewis et al. — general RAG method.
3. **Domain/evidence support:** Abd-Alrazaq et al. — mental-health chatbot evidence and safety context.
4. **Model support:** Liu et al. — RoBERTa model foundation.

If the supervisor expects the base paper to be a peer-reviewed published work rather than a preprint, confirm the final publication information for Mentalic Net first. If that cannot be verified or the paper’s full text is inaccessible, retain Mentalic Net as a motivating reference and ask the supervisor whether the primary base should instead be framed around the peer-reviewed mental-health chatbot evidence paper, with Lewis et al. as the technical method reference. Do not silently substitute one paper while keeping claims from another.

## 4. Suggested viva answer

> “Our primary research reference is Mentalic Net because it studies RAG-based conversational AI for mental-health support, which is the main direction of our project. We use Lewis et al. to explain the general RAG method, Abd-Alrazaq et al. to discuss the mental-health chatbot evidence and safety context, and Liu et al. as background for our RoBERTa-based classifiers. MindCare AI is our own implementation: it combines local FAISS retrieval and Ollama generation with task-specific text classifiers, English/Urdu/Roman Urdu prompting, safety-oriented processing, and wellness features. We do not claim to reproduce those papers, use their results as ours, or provide clinical diagnosis. Our classifier results are dataset-specific, and our full human-reviewed RAG response evaluation remains unfinished.”

## 5. Claims to avoid in the report and defense

- Do not call all four papers “the base paper.” Identify one primary base and label the others supporting literature.
- Do not claim MindCare AI reproduces Mentalic Net or uses its datasets, weights, or exact architecture unless verified.
- Do not compare classifier accuracy/F1 directly with a response-generation metric such as BERTScore.
- Do not present the project’s classifier metrics as clinical accuracy or diagnosis performance.
- Do not claim completed RAG/LLM effectiveness based on the current incomplete human-scoring run.
- Do not cite a paper’s result as evidence that MindCare AI is safe or effective.

## 6. References

1. Dutta, A., Mruthyunjaya, S., Saddington, J., & Islam, K. S. (2025). _Mentalic Net: Development of RAG-based Conversational AI and Evaluation Framework for Mental Health Support._ arXiv:2509.04456. https://arxiv.org/abs/2509.04456
2. Lewis, P., et al. (2020). _Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks._ NeurIPS. https://arxiv.org/abs/2005.11401
3. Abd-Alrazaq, A. A., et al. (2020). _Effectiveness and Safety of Using Chatbots to Improve Mental Health: Systematic Review and Meta-Analysis._ Journal of Medical Internet Research, 22(7), e16021. https://doi.org/10.2196/16021
4. Liu, Y., et al. (2019). _RoBERTa: A Robustly Optimized BERT Pretraining Approach._ arXiv:1907.11692. https://arxiv.org/abs/1907.11692

**Before submission:** Verify each bibliographic record, author list, venue, DOI/arXiv identifier, and the specific claims you cite against the primary paper or publisher page. Follow the department’s preferred citation style.
