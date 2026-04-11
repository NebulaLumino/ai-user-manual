# Reproducibility Crisis, Registered Reports & Open Science

## Research Memo | Cycle 118 | Task 3560

---

## Overview

The reproducibility crisis in science — the finding that many published research findings cannot be replicated — has been described as "the most important issue in science today." A landmark 2016 survey by Nature involving over 1,500 researchers found that more than 70% of researchers had tried and failed to reproduce another scientist's findings, and over 50% said they had failed to reproduce their own. The crisis spans fields from psychology and medicine to economics and nutrition science.

The crisis is not merely a quality control problem; it represents a systemic failure of scientific self-correction. When non-reproducible findings are published, cited, incorporated into meta-analyses, and used to inform policy and practice, the epistemic damage accumulates. AI offers both tools to improve reproducibility and new dimensions of risk as AI-generated content introduces novel irreproducibility vectors.

This memo examines the reproducibility crisis, the movement toward open science practices, the role of registered reports as a structural reform, and AI's complex role in either accelerating or mitigating irreproducibility.

---

## The Reproducibility Crisis in Detail

### Psychology and Social Science

The crisis was most publicly visible in psychology. Daryl Bem's 2011 meta-analysis claiming precognition (the ability of the mind to sense future events) was published in a leading psychology journal and passed peer review — yet follow-up studies found the effects disappeared. The Many Labs replication project (2013) attempted to reproduce 21 classic psychology findings; only 14 reached significance. Kahneman and others have argued that publication pressure and p-hacking (the practice of selectively analyzing data until results appear significant) are primary drivers.

### Medicine and Preclinical Biology

The Reproducibility Project: Cancer Biology (Science Exchange, 2015-2020) attempted to replicate 50 high-impact preclinical cancer studies. Only 15% of studies showed results fully consistent with the original, with an additional 30% showing partially reproducible results. The pharmaceutical industry has long noted that compounds that "work" in academic labs frequently fail in industry development.

### Economics and Social Policy

The Replications in Economics Project and work by Cameron, Levine, and others found that many celebrated findings in development economics and labor economics fail to replicate across contexts. A/B testing in tech companies (where experiments can be run on millions of users) has revealed that many social science findings that appear robust in small samples vanish at scale.

### Contributing Factors

Multiple factors contribute to irreproducibility:
- **Publication bias:** Journals prefer positive results. Negative results are rarely published, creating a biased literature.
- **P-hacking and HARKing:** Post-hoc analysis of data to find significant results (p-hacking) or presenting post-hoc hypotheses as if they were pre-specified (Hypothesizing After Results are Known, HARKing).
- **Underpowered studies:** Small samples produce large effect size estimates that shrink toward zero upon replication.
- **Flexible analysis:** Researcher degrees of freedom in preprocessing, covariate selection, and statistical test choice.
- **Insufficient transparency:** Inaccessible data, code, and methods prevent independent verification.

---

## AI Applications in Reproducibility

### AI for Statistical Audit and P-Hacking Detection

AI tools to detect statistical irregularities:

**Statcheck**: An automated tool that extracts statistical results from papers and checks whether reported statistics are mathematically consistent with reported test statistics, degrees of freedom, and p-values. Statcheck found errors in over 50% of papers in a large sample.

**p-curve analysis (Simonsohn et al.)**: Uses the distribution of p-values in a paper to distinguish genuine effects from p-hacked ones. Genuine effects produce a right-skewed p-curve; p-hacked results produce a uniform distribution clustered near .05.

**AI-powered study pre-registration analysis**: Platforms like AsPredicted and OSF support study pre-registration (specifying hypotheses, methods, and analysis plans before data collection). AI tools that compare submitted manuscripts against pre-registrations to detect methodological deviations are being developed.

### AI for Meta-Analysis and Systematic Review

AI is accelerating systematic reviews and meta-analyses:

**Rayyan (Qatar Computing Research Institute)**: An AI-powered tool for systematic review screening — helping researchers screen thousands of abstracts for inclusion/exclusion. It uses active learning to reduce the number of abstracts human reviewers must read.

**SyNet and RobotReviewer**: AI systems that extract PICO (Population, Intervention, Comparator, Outcome) elements from papers, assess risk of bias, and generate structured synopses. Used by Cochrane Collaboration and other systematic review organizations.

**Evidence Atlas**: AI systems that map the evidence landscape for a given clinical question, identifying where evidence is strong, weak, or absent.

### AI for Code and Data Sharing Verification

Reproducibility requires that analysis code and data be accessible:

**Code Review for Reproducibility**: AI tools that analyze submitted code (for papers with code repositories) to verify that the code actually produces the reported results, and to identify potential bugs or analytical choices that would affect findings.

**Data provenance tracking**: AI systems that automatically maintain data provenance chains — tracking which raw data files were used, what transformations were applied, and what outputs were generated — enabling retrospective reproducibility verification.

---

## Registered Reports: A Structural Solution

### How Registered Reports Work

Registered Reports (RR) are a publication format developed by the Open Science Framework and piloted by journals including *Cortex*, *Psychological Science*, and *Nature Communications*. In the RR format:

1. Authors submit a pre-registration describing their hypotheses, methods, and analysis plan
2. The manuscript is peer reviewed before data collection
3. If the plan passes review, the journal commits to publishing results regardless of outcome (positive or negative)
4. Authors execute the study and submit results
5. Results are published with full transparency about deviations from the pre-registration plan

This format addresses the core incentive problem: publication bias toward positive results. When journals commit to publishing results regardless of outcome, the incentive to p-hack or HARK disappears.

### Evidence on Registered Reports

Studies comparing RR to traditional publication formats find:
- Higher proportion of null findings published (reducing publication bias)
- More precise effect size estimates (reflecting reduced publication bias)
- No observed reduction in quality (referees do not appear to lower standards knowing results will be published)
- Increased methodological rigor in pre-registrations (peer review before data collection catches design flaws)

The proportion of journals offering RR has grown from 3 in 2013 to over 300 as of 2024.

### AI in Registered Report Review

AI tools can assist RR peer review:
- Checking pre-registration completeness against reporting standards (e.g., CONSORT for clinical trials, PRISMA for systematic reviews)
- Flagging statistical power analysis (are sample sizes justified?)
- Suggesting methodological improvements before data collection
- Comparing submitted protocols against final manuscripts for deviation detection

---

## Open Science as Reproducibility Infrastructure

### Pre-Registration and Open Methods

Pre-registration platforms (OSF, ClinicalTrials.gov, AEA RCT Registry) create public, timestamped records of research plans. When combined with publication of analysis code (GitHub, GitLab, Dataverse) and data (when ethically permissible), pre-registration enables retrospective evaluation of whether results were obtained as planned.

### Open Data

Mandatory data sharing (as required by many funders and some journals) allows independent verification of results. The tension between open data and participant privacy is managed through de-identification standards, controlled access mechanisms, and synthetic data generation.

### Open Code and Computational Reproducibility

The tide has turned toward code availability. Top journals (Nature, Science, PNAS) now require code availability for computational papers. GitHub-hosted code repositories are standard. Binder and similar tools enable one-click computational reproducibility by containerizing environments.

### AI and Reproducibility Risk

AI introduces new reproducibility threats:

**LLM-generated text without data access**: An AI can generate a plausible-sounding analysis description without having verified it against the actual data. If the description and data don't match, reproducibility is compromised. The problem of "AI hallucinations" in scientific contexts is significant.

**Training data contamination**: AI models trained on large corpora may have seen test data or related data, inflating their apparent performance in ways that won't generalize. This "data contamination" problem affects AI systems evaluated on scientific benchmarks.

**Non-determinism in AI systems**: Many AI systems (neural networks with random initialization, RL agents with exploration noise) are non-deterministic. Exact reproducibility requires explicit random seed control, which is often not documented in scientific publications using AI.

---

## Ethics

### Publication Ethics and the Negative Result Problem

The failure to publish negative results is a publication ethics violation — withholding information that could save lives, guide future research, and prevent redundant experimentation. AI tools that identify where negative results exist but were not published (by scanning trial registries and comparing to publications) could expose this problem and create pressure for change.

### AI as a Threat Multiplier for Irreproducibility

Generative AI lowers the cost of producing plausible-sounding but potentially irreproducible research. AI-assisted literature reviews may hallucinate citations; AI-generated methods descriptions may be inaccurate; AI-generated discussion sections may overstate generalizability. Without careful human review, AI accelerates the production of unreliable scientific knowledge.

### Accountability for AI-Generated Findings

When a finding generated by an AI-assisted analysis is published and later found irreproducible, accountability is diffuse. The researcher, the AI tool developer, and the journal that published it all share some responsibility — but no existing framework distributes it clearly.

### Equity in Reproducibility

The reproducibility crisis is most severe in under-resourced contexts where research infrastructure (statistical consultation, code review, lab standards) is absent. Reproducibility reforms that assume institutional resources (pre-registration platforms, open data repositories, statistical auditors) may be inaccessible to researchers in lower-resource settings, creating inequity.

---

## Future Directions

### Blockchain-Based Research Integrity

Blockchains can create tamper-evident records of research activity — data collection events, analysis runs, pre-registrations — that make post-hoc modification of research records detectable. If widely adopted, blockchain-based research integrity infrastructure could substantially improve reproducibility by making methodological changes visible.

### Registered Reports as Default

Several commentators have argued that the RR format should become the default for hypothesis-testing research, with traditional publication as the exception. This structural change would address the incentive problem at its root, rather than relying on post-hoc detection of p-hacking.

### AI-Powered Replication Prediction

AI models trained on past replication studies can predict which findings are most likely to replicate — using features like effect size, sample size, researcher reputation, and study design quality. While far from perfect, such prediction models could help prioritize which findings to attempt to replicate first and which to take with more skepticism.

### Integrated Open Science Workflows

The most promising future direction is integrated open science workflows: pre-registration (timestamped, public), data sharing (in FAIR-compliant repositories), code sharing (containerized, versioned), open peer review (published reviewer reports), and post-publication commenting — all connected through a unified platform. AI can help at each step: drafting pre-registrations, standardizing data formats, checking code, and synthesizing reviewer comments.

---

## Key References

- Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251).
- Camerer, C.F. et al. (2016). Evaluating replicability in laboratory experiments. *Science*, 351(6280).
- Nosek, B.A. et al. (2015). Psychology. Promoting an open research culture. *Science*, 348(6242).
- Errington, T.M. et al. (2021). Investigating the replicability of preclinical cancer biology. *eLife*, 10.
- Ioannidis, J.P.A. (2005). Why most published research findings are false. *PLOS Medicine*, 2(8).
- Simmons, J.P., Nelson, L.D., & Simonsohn, U. (2011). False-positive psychology. *Psychological Science*, 22(11).
