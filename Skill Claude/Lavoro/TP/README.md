# design-photocopy-clone

**Design Photocopy & Replication Skill** for the Agent Skills ecosystem (skills.sh).

## Purpose
Enables AI agents to act as a high-fidelity "digital photocopier" for designs embedded in:
- PowerPoint presentations (.pptx)
- Excel workbooks (.xlsx)
- Word documents / PDFs (.docx, .pdf)
- Related image exports or screenshots

It extracts **both structural** (XML-based positions, styles, hierarchies) **and visual** (layout, colors, typography, spacing) information, then produces **photocopy-grade replicas** that preserve exact appearance and intent.

Designed by a Senior Solutions Architect with 35+ years experience in high-availability (HA), resilient complex workflows, smart problem-solving, and production-grade workarounds.

## Key Features
- **Multi-layer extraction** (structural + visual + hybrid) for maximum resilience
- **Photocopy fidelity**: Aims for pixel-close visual match + functional equivalence (formulas in Excel, animations notes in PPT, etc.)
- **Canonical Design Blueprint**: Structured output (JSON) usable for recreation, import, or further processing
- **Multi-format replication outputs**:
  - High-fidelity HTML/CSS/JS preview (absolute or grid-based "photocopy")
  - Detailed native tool instructions (PowerPoint, Excel, Word steps)
  - Executable generators (python-pptx, openpyxl snippets or full scripts)
  - Design tokens + spec for Figma, CSS variables, etc.
- **HA & smart fallbacks**: Parallel paths, confidence scoring, partial success handling, verification loops
- **Workarounds for real-world issues**: Binary formats, font substitution, complex charts, master slides, merged cells, etc.

## Installation
```bash
# From GitHub (once published)
npx skills add yourusername/design-photocopy-clone

# Or local during development
npx skills add ./design-photocopy-clone
```

Supports Claude Code, Cursor, GitHub Copilot, Gemini, and 40+ other agents via skills.sh.

## Usage Examples
- "Analyze the design of this quarterly report.pptx and create a pixel-perfect HTML clone"
- "Extract the layout, colors, and table styles from sales-dashboard.xlsx and generate instructions to recreate it in a new Excel file"
- "Photocopy the branding and slide master from brand-presentation.pptx into a new 10-slide deck"
- "Replicate this invoice.docx design exactly as a modern web form (HTML/CSS)"

## Structure
- `SKILL.md`: Core agent instructions (loaded into context)
- `references/`: Detailed guides (loaded on-demand)
- `scripts/`: Executable helpers (run via agent tools)
- `assets/`: Templates and schemas

## Development & Validation
```bash
# Validate the skill
npx skills-ref validate ./design-photocopy-clone

# Or use the skill-creator for enhancements
npx skills add anthropics/skills --skill skill-creator
```

## License & Contribution
Open for the agent skills ecosystem. Inspired by frontend-design and other production skills.

---

**Senior Solutions Architect Note**: This skill embodies HA principles: no single point of failure in extraction (always ≥2 methods), graceful degradation, auditable outputs, and continuous verification. Use workarounds intelligently — never sacrifice fidelity for convenience.
