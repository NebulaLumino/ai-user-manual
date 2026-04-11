# LLMs in Peer Review & Scientific Gatekeeping

## Research Memo | Cycle 118 | Task 3552

---

## Overview

Peer review is the backbone of scientific quality control. Yet the process is slow (months per review cycle), often inconsistent, financially uncompensated, and vulnerable to bias, overload, and burnout. Approximately 30 million academic papers have been published since 2010, creating a review burden that has outpaced the willing reviewer supply. The average peer reviewer spends 30-60 hours per year on reviews, a contribution rarely formally acknowledged in career advancement.

Large language models have entered this picture with disruptive force. Journal editors are deploying AI to assist with reviewer matching, manuscript triage, initial screening, and — increasingly — draft review generation. Some publishers have piloted AI-written review summaries presented alongside submitted manuscripts. The question of whether, how, and to what extent AI should participate in the gatekeeping of scientific knowledge is among the most consequential debates in contemporary scholarly communication.

This memo examines the current state of AI in peer review, the technical approaches being deployed, the ethical tensions, and the emerging norms shaping the future of scientific gatekeeping.

---

## AI Applications

### AI-Assisted Reviewer Matching

The most widely deployed AI application in peer review is reviewer identification. Traditional methods rely on editors manually selecting reviewers based on past publications and expertise self-selection. AI-powered systems like SCOPUS Reviewer Matching, Elsevier's AIRA, and Springer Nature's manuscript screening tools use embedding models trained on paper abstracts, keyword taxonomies (MeSH, ACM Computing Classification System), and citation graphs to identify the most qualified potential reviewers for a given manuscript.

These systems score candidate reviewers on multiple dimensions:
- **Topic relevance:** Semantic similarity between reviewer publication history and submitted manuscript
- **Methodological overlap:** Shared methods, data types, and analytical frameworks
- **Currency:** Recent publications in the domain (versus stale expertise)
- **Workload balancing:** Distribution of review invitations to prevent burnout clustering
- **Conflict of interest detection:** Automated flagging of institutional, collaborative, or financial conflicts

Research by Chen et al. (2023) found that AI-matched reviewers were rated more topic-appropriate by editors than editor-selected reviewers in randomized trials, though this did not consistently translate to higher review quality ratings.

### AI Manuscript Triage and Quality Screening

Before manuscripts reach expert reviewers, many journals use AI to screen for:
- **Technical completeness:** Presence of required sections, word counts, reference formatting
- **Language quality:** AI-assisted readability scoring and grammar checks (with explicit disclosure)
- **Ethical compliance:** Plagiarism detection (using tools like iThenticate, Grammarly, Ouriginal)
- **Sufficiency of novelty/impact:** Controversially, some publishers have piloted AI scoring of "novelty" — a metric deeply contested in the research community

### LLM-Generated Review Drafts

The most ethically fraught application is using LLMs to generate actual review text. Some publishers have piloted AI-assisted review generation where the LLM produces a structured review summary that a human reviewer then edits. The workflow typically follows:

1. The LLM reads the manuscript and generates structured observations organized by evaluation criterion
2. A human reviewer reviews the AI output and provides corrections, additions, and judgment calls
3. The final review is submitted in the reviewer's name

Arguments in favor include increased reviewer efficiency (reducing the time burden on human reviewers) and consistency of review structure. Arguments against focus on the profound epistemic problem: a reviewer's role is not just to describe the paper's properties but to exercise scientific judgment — an act that requires expertise and bears accountability. A review generated from pattern-matching on publication text, even a sophisticated LLM, lacks the reviewer's commitment to the evaluation.

### AI Review Quality Assessment

Journals and publishers are exploring AI tools to assess the quality of reviews they receive. Metrics like:
- **Constructiveness:** Proportion of actionable suggestions versus vague criticism
- **Specificity:** Reference to specific figures, sections, or prior literature
- **Coverage:** Whether all evaluation criteria are addressed
- **Tone:** Politeness, respectfulness, absence of ad hominem language

These assessments feed back into reviewer recognition programs and can identify reviewers who need training or should be rotated out.

### Post-Publication Review and Commenting Platforms

Platforms like PubPeer have long enabled post-publication critique. AI tools are now being integrated into these platforms to surface potentially problematic papers based on statistical anomalies (e.g., suspiciously uniform result distributions), image duplication detection, and text similarity to prior publications. PubMed's "Similar Articles" and Google Scholar's recommendation systems also use AI to connect readers with relevant critiques.

---

## Tools and Methods

### Semantic Similarity for Reviewer Matching

Reviewer matching typically uses sentence transformer models (e.g., Specter2 for academic text, SciBERT, or E5 embeddings) to represent both the manuscript and reviewer publication records as dense vectors. Cosine similarity between the manuscript vector and each reviewer's publication centroid scores topic relevance:

```
score(reviewer, manuscript) = max_i cos(embed(reviewer_pub_i), embed(manuscript))
```

More sophisticated systems train pairwise classification models that predict "would this reviewer be qualified to review this manuscript?" using features including co-citation patterns, shared authorship networks, and topical embeddings.

### Plagiarism and Text Reuse Detection

AI-powered plagiarism detection goes beyond exact string matching to include:
- **Paraphrase detection:** Using semantic embedding models to detect meaning-level similarity even when surface language differs substantially
- **Translation detection:** Cross-language similarity detection (Chinese paper paraphrased into English)
- **Idea plagiarism:** Semantic similarity across paper contributions even when methodology and wording differ

Tools like iThenticate, Copyscape, and the IEEE/CrossRef "Similarity Check" service combine these methods and maintain massive reference databases.

### Statistical Anomaly Detection for Paper Screening

AI can flag papers with statistical red flags including:
- Unusually low variance in reported results (suspicious precision)
- Overrepresentation of extreme p-values just below significance thresholds
- Digit-level analysis: Benford's law testing on reported numerical values
- Image duplication and manipulation detection (steganographic analysis of figures)

Statcheck (developed by Meta-Research team at TU Munich) and papr's statistical screening tools are open-source examples.

### LLM Review Augmentation

Several research groups have built LLM-based review assistance tools:

**RECONS** (Research Council Open Science): Provides structured review templates and suggests evaluation criteria based on paper domain.

**ReviewerAI**: Uses GPT-4 to generate initial "areas of concern" observations organized by paper section, which human reviewers accept or reject.

**SciMoCat** (in development at several ELSSID publisher partners): A domain-fine-tuned model trained on a corpus of high-quality peer reviews paired with paper manuscripts, designed to produce structural critique at a "competent junior colleague" level.

---

## Challenges

### Reviewer Anonymity and Accountability

Traditional peer review in double-blind or single-blind formats maintains reviewer identity as a credential against bias. AI systems that aggregate reviewer comments or use shared models risk de-anonymizing reviewers whose stylistic patterns or word choices become identifiable. Furthermore, if an AI-assisted review is later found to contain substantive errors in scientific judgment, accountability is diffuse: the human reviewer may claim the AI was responsible; the publisher may claim the human should have verified.

### Quality vs. Efficiency Trade-off

LLMs tend to generate reviews that are fluent, polite, and superficially comprehensive but may miss subtle methodological flaws. Human reviewers with deep domain expertise catch issues that surface-level reading cannot. A study by Liang et al. (2024) comparing GPT-4 generated reviews to human reviews on CS papers found that while LLM reviews were rated as more "organized" and "specific," they missed methodological innovations and overstated confidence in conclusions the LLM had generated.

### Conflict of Interest and Commercial Interests

Publishers deploying AI in peer review have commercial interests in accepting manuscripts (journals profit from publication volume). AI systems designed or configured by publishers could systematically underweight ethical concerns about sponsored content, industry-funded studies, or competing methodologies in ways that benefit the publisher. Independent, transparent auditing of these AI systems is rare.

### Gaming and Adversarial Text

Submitters can attempt to game AI review-assistance systems by:
- Optimizing manuscripts for favorable AI-generated reviews (using AI to preview how a review might go and revising accordingly)
- Including "invisible" content (adversarial triggers in text invisible to humans but detected by the AI as important)
- Fabricating references to non-existent papers that AI might accept uncritically

The adversarial dynamics between submitter manipulation and AI detection are still evolving, with no stable equilibrium in sight.

### Jurisdiction and Regulatory Gaps

No major jurisdiction yet requires disclosure of AI participation in peer review. As AI becomes more embedded in the process, governance frameworks need to address: whether authors should be told their paper received AI-assisted review; whether reviewers should be required to disclose AI use; and what recourse authors have when an AI error in the review process leads to a wrongful rejection.

---

## Ethics

### Disclosure and Consent

The minimal ethical baseline — disclosure that AI is involved in the review process — is not uniformly adopted. Most major journals have not published clear policies on AI-assisted review. The Committee on Publication Ethics (COPE) has published discussion documents but no binding guidelines as of this writing. Without disclosure norms, authors cannot make informed decisions about submission, reviewers cannot account for AI involvement in their own responses, and readers cannot weight AI-assisted evaluations appropriately.

### Bias Amplification

LLMs trained on existing published literature may encode and amplify biases present in that literature. If a field has historically privileged certain methodologies, populations, or research traditions, an LLM reviewing new papers will tend to judge work against those traditions as higher quality. This can systematically disadvantage novel or non-canonical approaches — the very work that most needs rigorous but open-minded peer review.

### The Integrity of the Scientific Record

The scientific record is premised on human scientific judgment being accountable to a community. If AI systems contribute substantively to what gets published while remaining opaque, the epistemological foundations of that record are weakened. Editors and publishers who deploy AI in review without transparency are, in a real sense, changing the rules of scientific knowledge production without broad community consent.

### Free Labor and the Commodification of Review

Many AI tools being piloted in peer review are developed using the labor of unpaid reviewers — their reviews are used (with or without consent) to train and benchmark the models. While training on publicly available papers is legal, training on the private text of submitted manuscripts — which may not yet be public and which reviewers have not consented to have used for AI training — raises serious ethical questions.

---

## Future Directions

### Tiered Review with AI Triage

A promising model emerging from academic discussion is tiered review: AI handles initial technical screening, completeness checking, and language review; human experts conduct substantive scientific evaluation. This division could dramatically increase system throughput while preserving human judgment for the most important quality signals. Success requires clear delineation of which review functions are appropriate for AI and which require human expertise.

### Registered Reports and AI Pre-Registration

The growing Registered Reports format (where peer review occurs before results are known, addressing publication bias) may benefit from AI assistance in reviewing protocols against prior registrations. Blockchain-based timestamped pre-registration, combined with AI matching of final results against registered methods, could strengthen integrity.

### Open Peer Review with AI Augmentation

Open peer review (where reviewer identities are public) combined with AI tools that help reviewers write more constructively could improve quality while maintaining accountability. Several journals piloting open review have reported that named reviewers write more careful, constructive reviews — suggesting that transparency本身就是 a quality mechanism that AI assistance could augment rather than replace.

### Community Governance of AI in Review

The most important future direction is not technical but governance: the scientific community needs collective norms about AI in peer review, established through bodies like COPE, the International Committee of Medical Journal Editors (ICMJE), and disciplinary societies. These norms should address disclosure, accountability, bias auditing, and the boundary between AI assistance and replacement.

---

## Key References

- Chen, Y. et al. (2023). AI-assisted peer reviewer matching: A randomized controlled trial. *Science and Engineering Ethics*, 29(3).
- Liang, W. et al. (2024). Advancing AI capabilities in peer review: A comparative study of LLM-generated and human reviews. *arXiv preprint*.
- COPE. (2023). Discussion document: Use of AI in peer review. *Committee on Publication Ethics*.
- Norgeot, B. et al. (2022). Protected: Claims of large language model use in scientific writing. *Nature Medicine*, 28(11).
- Statcheck. TU Munich Meta-Research Group. Available at statcheck.info.
