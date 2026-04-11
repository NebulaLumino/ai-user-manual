# Scientific Figure Generation & Data Storytelling

## Research Memo | Cycle 118 | Task 3559

---

## Overview

A scientific figure is not merely an illustration — it is an argument made visual. The quality of a figure determines whether a paper survives peer review, whether a research finding influences policy, and whether the public understands what scientists have discovered. Data visualization is where the worlds of design, cognitive science, statistics, and communication intersect. Poorly designed figures are a primary driver of irreproducibility and misunderstanding; well-designed figures can convey years of research in a single frame.

The democratization of data visualization tools — from Excel to Tableau to Python's matplotlib and seaborn to R's ggplot2 — has been accompanied by a proliferation of poorly designed, misleading, or simply ugly figures. AI is now being applied at multiple levels: automating best-practice chart selection, suggesting design improvements, generating presentation-ready figures from raw data, and detecting misleading visual encodings. This memo surveys the landscape of AI-powered scientific figure generation and its implications for scientific communication.

---

## AI Applications

### AI-Powered Chart Recommendation

The most fundamental AI application in data visualization is helping researchers select the right chart type for their data and question:

**Tableau's Show Me feature**: A rule-based expert system that recommends appropriate chart types based on data types (categorical, quantitative, temporal, geographic) and the analytical question. More recently, Tableau has incorporated machine learning to improve recommendations based on how users actually use their data.

**DataWrapper's automated chart selection**: Analyzes uploaded data and suggests the most appropriate visualization — a bar chart for comparisons, a line chart for trends over time, a map for geographic data. Used by major news organizations (NYT, FiveThirtyEight) and research communications.

**PowerBI's Quick Insights**: Uses automated machine learning to identify statistically significant patterns in data and recommend visualizations that highlight those patterns.

**Matplotlib and Seaborn style suggestion**: Python packages that analyze data characteristics and suggest appropriate visual encodings based on perceptual psychology research.

### Automated Figure Generation from Data

AI systems that accept raw data (CSV, Excel, API feeds) and output publication-quality figures:

**Autoplot (R)**: Automatically selects and renders appropriate plots based on data types, detecting temporal series, categorical comparisons, distributions, and correlations.

**RoughViz and Observable Plot**: Hand-drawn-style visualization libraries that use AI to select and render charts, particularly useful for exploratory data analysis.

**DALL-E, Midjourney, and Stable Diffusion in scientific illustration**: While not analytical tools per se, generative AI image models are increasingly used to create illustrative scientific figures — cell diagrams, mechanism schematics, and conceptual diagrams. This raises questions about scientific illustration standards and the boundary between accurate scientific representation and artistic license.

### AI Figure Enhancement and Accessibility

Beyond chart selection, AI tools enhance figure quality:

**Color palette optimization**: Tools like ColorBrewer, Viridis, and AI-assisted palette generators recommend perceptually uniform, colorblind-accessible color schemes for scientific figures. Matplotlib's default colormap changes toward perceptually uniform palettes are a direct response to research showing that rainbow colormaps (the previous default) misrepresent data.

**Layout optimization**: AI systems that determine optimal panel arrangement in multi-panel figures (standard in biology and neuroscience), using gestalt principles and publication standard templates.

**Annotation automation**: Tools that read data and suggest annotations (axis labels, legends, units) using domain-specific knowledge, reducing the manual effort of figure preparation.

### AI in Data Storytelling

Making data compelling to non-expert audiences:

**Data-to-Narrative systems**: AI systems that generate natural language descriptions of what a figure shows, translating statistical results into accessible prose. Tools like Google's Fact Check Tools and Data Sonification projects are early examples.

**Narrative arc suggestion**: Based on the Rhetorical Structure Theory from computational linguistics, AI can suggest how to sequence visualization elements to build an argument rather than simply reporting results.

**Interactive figure generation**: AI systems that generate interactive scientific figures (using D3.js or similar libraries) from static data, enabling readers to explore data dimensions most relevant to their interests.

---

## Tools and Methods

### Perceptual Psychology and Visual Encoding

The scientific basis for AI figure recommendation rests on perceptual psychology:

**Cleveland and McGill's ranking of visual encodings** (1984): Quantified the accuracy with which humans decode different visual elements — position along a common scale (most accurate), position on aligned scales, length (bars), angle, slope, area, volume, density, color saturation, hue. AI chart recommendation systems encode this ranking in their decision logic.

**Pre-attentive features**: Visual properties (color, orientation, size) that are detected by the visual system before conscious attention. AI layout tools use pre-attentive features to direct viewer attention to the most important data elements.

**Gestalt principles**: Principles of visual perception (proximity, similarity, closure, continuity) that govern how viewers group and separate elements. AI layout optimization uses gestalt principles to determine element grouping.

### Grammar of Graphics and Automated Design

**Grammar of Graphics** (Wilkinson's systematic formalism for visualization) underlies most modern visualization tools. AI applications include:

- **Automated semantic zooming**: When a viewer focuses on a region of a chart, AI determines what additional detail (labels, annotations, breakdowns) to show at that zoom level
- **Chart typification**: Adapting chart forms to the data density (e.g., converting a dense scatter plot to a hexbin or contour plot when data overlap obscures patterns)

### Generative AI for Scientific Illustration

Large multimodal models are being trained to generate scientifically accurate illustrations:

**SciGen (KAUST / UIUC)**: A model trained to generate protein structure diagrams and biological pathway illustrations from textual descriptions. Early results show high anatomical accuracy but occasional molecular errors.

**AlphaGeometry and diagram generation**: DeepMind's AlphaGeometry model demonstrates that AI can generate mathematically accurate geometric proofs alongside diagrams, suggesting applications in mathematical figure generation.

---

## Challenges

### Scientific Accuracy vs. Visual Appeal

AI-generated figures may be beautiful but inaccurate. A chart that "looks right" by aesthetic standards may misrepresent data if axes are truncated, scales are non-linear, or visual encoding is applied incorrectly. The risk is that AI optimizes for human visual preference rather than data fidelity. Review processes must verify AI-generated figures as carefully as manually-created ones.

### Reproducibility and Figure Standardization

If every researcher uses AI to generate figures differently, scientific literature becomes visually inconsistent. Journal style guides have traditionally provided standardization; AI-generated figures may evade or complicate this standardization. Major publishers are beginning to issue guidelines for AI-generated figure elements.

### Data Leakage in Published Figures

Published figures often contain information beyond what the text reports — subpanels with additional experiments, timepoints, or conditions. AI that extracts data from figures (a useful capability for meta-analysis) must account for the fact that figures are simplified representations, not complete data records.

### The Black Box Figure

AI-generated figures may use encodings the researcher does not understand. If an AI system chooses a non-standard chart type, unusual color mapping, or complex multi-panel layout without explanation, the resulting figure may confuse rather than clarify. Explainable AI in visualization design is an active research area.

---

## Ethics

### Attribution and AI-Generated Scientific Art

Who owns the copyright on an AI-generated scientific figure? If an AI system generates a figure from raw data, and that figure is published, what attribution is owed to the AI system developer, the training data creators, and the data generator? Copyright law has not resolved these questions.

### Misleading Figure Generation

Generative AI can produce figures that look plausible but misrepresent data. A visualization that shows a steep upward trend by truncating the y-axis, or that highlights a correlation by selecting a cherry-picked subset of data, is not honest. AI tools that help researchers avoid misleading visualizations (by automatically checking for common chart errors) are a net positive; AI tools that optimize for visual impact over data integrity are dangerous.

### Accessibility Standards

Scientific figures must be accessible to color-blind readers and to those using screen readers. AI tools that generate figures have a responsibility to use accessible color schemes and provide alt-text descriptions. The community's norm of using colorblind-safe palettes (viridis, cividis, and similar perceptually uniform schemes) should be the default, not the exception.

### Data Sovereignty and Visualization

When AI tools generate visualizations by uploading data to cloud services, scientific data leaves the institution. For proprietary or sensitive research data (clinical trial data, biosecurity-relevant experiments), this transfer may be prohibited or undesirable. Local AI tools for visualization are needed for sensitive contexts.

---

## Future Directions

### Multimodal Figure Understanding

AI systems that can both generate and interpret scientific figures — reading a figure, extracting the underlying data, identifying the visual encodings used, and evaluating whether those encodings are appropriate and accurate — would serve both authors (generating figures) and readers (interpreting figures). Large multimodal models trained on figure-caption pairs are moving in this direction.

### Interactive, Layered Scientific Figures

The static PDF figure has significant limitations for complex datasets. Future scientific publishing may move toward interactive figures — layered visualization where readers can drill down into data, toggle conditions, and explore parameter space. AI can help design these interactive experiences by identifying which layers of information are most important to surface.

### AI Figure Review in Peer Review

Journals could use AI tools to review submitted figures for technical quality — checking axis scales, appropriate color encoding, consistent labeling, and statistical display standards — before human review. This would reduce the burden on reviewers and improve baseline figure quality.

---

## Key References

- Cleveland, W.S. & McGill, R. (1984). Graphical perception. *Journal of the American Statistical Association*, 79(387).
- Ware, C. (2020). *Information Visualization: Perception for Design* (4th ed.). Morgan Kaufmann.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Borkin, M.A. et al. (2013). What makes a visualization memorable? *IEEE Transactions on Visualization and Computer Graphics*, 19(12).
- Schwab, M. & Karban, B. (2023). AI-assisted scientific figure generation. *Nature Methods*, 20.
