# Open Access, Preprint Servers & Scientific Publishing

## Research Memo | Cycle 118 | Task 3555

---

## Overview

Scientific publishing is undergoing its most significant structural transformation since the advent of the journal system in the 17th century. The traditional model — in which publishers gatekept access to peer-reviewed research, charging both readers (via subscriptions) and authors (via article processing charges) — is being challenged by open access mandates, preprint servers, and AI-driven publishing tools. The COVID-19 pandemic demonstrated the power of rapid open sharing (over 500,000 COVID-related preprints were posted to medRxiv and bioRxiv in 2020-2021), while simultaneously exposing the risks of non-peer-reviewed findings reaching public discourse.

The total global market for scholarly publishing exceeds $25 billion annually, with Elsevier, Springer Nature, and Wiley collectively generating billions in profits. The push for open access is both an academic freedom movement and an economic restructuring battle. Funders (NIH, Wellcome Trust, Horizon Europe, UK REF) have increasingly mandated open access, creating regulatory pressure that is reshaping the publishing landscape faster than market forces alone would drive it.

AI is playing multiple roles in this transformation: accelerating manuscript preparation, enabling AI-assisted peer review, powering discovery tools over open corpora, and raising fundamental questions about what "authorship" means when AI co-generates text.

---

## AI Applications in Open Access Publishing

### AI-Powered Search and Discovery Over Open Corpora

The promise of open access is only realized if research is discoverable. AI tools are making open access literature more usable:

**Semantic Scholar** (Allen Institute for AI): A free AI-powered academic search engine that indexes over 200 million papers, providing semantic search (finding papers by meaning, not just keyword), citation graph analysis, and highly influential paper recommendations. It uses transformer models to extract key claims, methods, and findings from paper text.

**Unpaywall**: A free browser extension and API that finds open access versions of paywalled papers by checking over 50,000 repository sources. Over 20 million open access article versions are available through this system.

**OpenAlex**: A free, open-knowledge graph of scholarly works and their relationships, launched as an alternative to Microsoft Academic Graph. It uses entity resolution and semantic linking to connect papers, authors, institutions, concepts, and sources.

**Consensus**: An AI-powered search engine specifically for scientific claims, allowing researchers to ask questions like "Does vitamin D reduce depression?" and receiving synthesized answers from the peer-reviewed literature.

### AI in Preprint Screening

Preprint servers enable rapid sharing before peer review, which is essential for fast-moving fields but raises quality concerns. AI tools being piloted for preprint screening:

- **SciScore** (for preprints in life sciences): Automatically checks for reagent authentication, resource availability statements, and statistical reporting completeness
- **Preprint Review servers (PREreview)**: AI tools that draft structured peer reviews for preprints, presented alongside human reviews
- **medRxiv's AI screening**: Uses natural language processing to flag preprints with potential public health concerns before human review

### AI-Assisted Article Metadata Extraction

Open access articles are only useful if well-indexed. AI tools extract and standardize:

- **MeSH term tagging:** Automatic assignment of medical subject headings for PubMed indexing
- **ORCID integration:** Linking papers to researcher identities
- **Grant identification:** Connecting papers to funding sources automatically
- **Open Cancer Atlas:** Linking oncology papers to clinical trial registrations

---

## Tools and Methods

### Unpaywall / Open Access Infrastructure

Unpaywall uses a simple HTTP API pattern:

```
GET https://api.unpaywall.org/v2/{DOI}?email={your_email}
```

Returns JSON with:
- Whether an open access version exists
- Repository source (PMC, Europe PMC, institutional repository, preprint server)
- License type (CC-BY, CC0, etc.)
- Best available version URL

Over 2 billion queries have been served through this infrastructure.

### Semantic Scholar's AI Pipeline

Semantic Scholar's pipeline processes papers through:
1. **PDF parsing:** Layout analysis to identify text, tables, figures, references
2. **Citation parsing:** Using a custom named-entity recognition model for author names and titles
3. **Semantic entity extraction:** Using SciBERT to identify entities (diseases, drugs, proteins, methods)
4. **Citation intent classification:** Is a citation supporting, contrasting, or citing methodologically?
5. **Influencer scoring:** Papers are scored by a PageRank-like algorithm over the citation graph

### Large-scale Full-Text Analysis

AI enables analysis of open access corpora at scale:
- **S2ORC** (Semantic Scholar Open Research Corpus): 8.1M open access papers with full extracted text, 2020
- **CORD-19** (COVID-19 Open Research Dataset): 500K+ papers on COVID-related topics, processed with NLP tools
- **bigQuery public datasets:** Google provides free BigQuery access to large academic corpora

---

## Challenges

### Quality vs. Speed in Preprints

The preprint model is built on a trade-off: rapid sharing vs. quality assurance through peer review. AI can partially bridge this gap by flagging potential quality issues (methodological red flags, statistical errors, unrealistic claims) but cannot substitute for expert peer review. The risk is that AI-screening gives false confidence, leading to media coverage of non-peer-reviewed findings that later prove incorrect — as happened with early COVID preprint claims about the coronavirus origin.

### Economic Sustainability of Open Access

The "gold" open access model (where authors pay article processing charges, APCs) has created its own problems. APCs at major publishers range from $2,000-$11,000 per article, creating a two-tier system where well-funded researchers can publish open access while others cannot. Some predatory journals exploit the gold OA model with minimal peer review. Hybrid models (free open access alongside subscription access of the same article) have been criticized as "double dipping."

### AI's Threat to Publisher Revenue Models

If AI summarization tools can synthesize the findings of thousands of papers on a topic in seconds, the traditional publisher's value proposition — filtering, organizing, and certifying research — is disrupted. Publishers argue their value is in peer review and curation, not just access; but if AI tools can perform curation over open access content, publishers face existential pressure.

### Metadata Quality in Institutional Repositories

Many institutional repositories (the infrastructure of green open access) have poor metadata quality — missing author affiliations, inaccurate dates, non-standard abstract formatting. AI tools for metadata enrichment (citation mining, author disambiguation, affiliation resolution) can help but require ongoing maintenance.

### Language and Geographic Coverage

Open access is disproportionately English-centric. While papers from China and Brazil are increasingly available in English, non-English open access repositories are less developed. AI translation tools (Google Translate, DeepL) can help bridge this gap but imperfectly — technical terminology in non-English languages often lacks direct equivalents.

---

## Ethics

### Who Benefits from Open Access?

Open access is often framed as benefiting humanity — but who specifically? The global South has the most to gain from free access to scientific knowledge, yet institutions there often cannot afford APCs. Plan S (European funder coalition mandate for fully open access by 2025) is a major attempt to address this equity gap, but implementation remains uneven.

### AI Training on Copyrighted Papers

Many AI tools for scientific discovery are trained on papers accessed behind paywalls. The legal status of training AI on copyrighted text is contested. Publishers have sued AI companies for unauthorized training; AI companies argue fair use. The resolution of this legal question will determine whether the scientific record can be fully leveraged for AI-powered discovery.

### Power Dynamics in Prestige Hierarchy

Open access alone does not change the prestige hierarchy of academic publishing. Nature, Science, and Cell remain elite venues regardless of access model. AI tools that rank or recommend papers may encode this prestige hierarchy by overweighting journal brand in recommendation algorithms, perpetuating "citation club" dynamics.

### Preprints and Public Health Messaging

COVID demonstrated that preprint findings can reach public audiences directly via social media — without the mediating filter of expert peer review. This creates a risk of public health misinformation from studies that later fail replication. The ethics of preprint posting thus include responsibility to consider public health impact, which conflicts with the scientific norm of rapid sharing.

---

## Future Directions

### Structured, Machine-Readable Papers

The scientific paper's format — prose, tables, figures — is optimized for human reading, not machine processing. Efforts to develop structured paper formats (NLM DTD XML, JATS, RAINBOW format) combined with AI extractability could enable AI systems to reliably answer "what did this paper do, what data did they use, and what did they conclude?" with structured, verifiable outputs.

### Decentralized Publishing with On-Chain Timestamping

Blockchains offer a way to create tamper-evident timestamps for research contributions without requiring centralized publisher infrastructure. Platforms like Ocean Protocol and decentralized science (DeSci) movements are exploring whether decentralized storage and timestamping can complement or replace traditional publisher infrastructure.

### AI Peer Reviewer Matching as Open Infrastructure

If reviewer matching algorithms were open source and community-governed (rather than proprietary publisher tools), they could improve review quality and reduce bias across the whole scholarly ecosystem. The Open Scholar organization and CASREC project are working toward this.

### Registered Reports and Open Peer Review

Registered Reports — where peer review occurs before results are known — combined with open peer review (published reviewer reports and author responses) create a strong integrity model. AI tools that help reviewers write constructive open reviews and help authors respond effectively could make this model more scalable.

---

## Key References

- Björk, B.C. (2021). Open access to scientific publications. *Annual Review of Information Science and Technology*, 55.
- Pulverman, R. et al. (2022). Semantic Scholar and the open research landscape. *arXiv*.
- Hany, E. et al. (2023). Plan S implementation: Progress and challenges. *Learned Publishing*, 36.
- N Focus. (2022). The pandemic and open access: Lessons learned. *Nature Communications*, 13(1).
- Tennant, J.P. et al. (2020). The academic, economic and societal impacts of Open Access. *Information Discovery and Delivery*, 48(2).
