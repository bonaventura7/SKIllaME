from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


ITALIAN_STOPWORDS = {
    "a","ad","al","allo","ai","agli","all","agl","alla","alle","anche","ancora","avere","avuto",
    "che","chi","ci","coi","col","come","con","contro","cui","da","dagli","dai","dal","dalla",
    "dalle","dei","del","della","delle","di","e","ed","era","erano","essere","fa","fra","gli",
    "ha","hai","hanno","ho","i","il","in","io","la","le","li","lo","loro","ma","mi","mia",
    "mie","miei","mio","ne","nei","nel","nella","nelle","no","non","noi","nostra","nostre",
    "nostri","nostro","o","od","per","più","poi","quale","quali","quello","quella","quelle","quelli",
    "questo","questa","questi","queste","si","sia","sono","sua","sue","sul","sulla","sulle","suo",
    "suoi","tra","tu","tua","tue","tuo","tuoi","un","una","uno","vi","voi","vostra","vostre",
    "vostri","vostro","nel","nello","degli","dello","dell","dell'","dall","dall'","all'","nell'"
}

FORMULA_PATTERNS = [
    "in particolare",
    "come si evince",
    "si rimanda",
    "si segnala",
    "si precisa",
    "nel periodo d'imposta",
    "ai fini della presente",
    "il presente report",
    "il gruppo",
    "si osserva che",
    "si rileva che",
    "si evidenzia",
    "si ritiene che",
    "fermo restando",
    "in via subordinata",
    "in via preliminare",
    "non appare condivisibile",
]

SUBORDINATE_MARKERS = [
    "che ", "qualora ", "ove ", "mentre ", "laddove ", "nonché ", "sebbene ",
    "affinché ", "poiché ", "in quanto ", "benché ", "al fine di ", "in modo da "
]

PASSIVE_MARKERS = [
    "viene ", "vengono ", "veniva ", "venivano ", "è stato ", "sono stati ",
    "risulta ", "risultano ", "si segnala ", "si precisa ", "si ritiene ", "si osserva "
]

@dataclass
class DocumentMetrics:
    name: str
    paragraphs: int
    non_empty_paragraphs: int
    headings: int
    avg_words_per_sentence: float
    median_words_per_sentence: float
    avg_words_per_paragraph: float
    median_words_per_paragraph: float
    semicolon_rate_per_1000_words: float
    subordinate_marker_rate_per_1000_words: float
    passive_marker_rate_per_1000_words: float
    top_formulas: List[Tuple[str, int]]
    top_terms: List[Tuple[str, int]]
    title_styles: List[Tuple[str, int]]


class StyleAnalyzer:
    def __init__(self, doc_paths: List[Path]):
        self.doc_paths = doc_paths

    def _read_xml(self, zf: zipfile.ZipFile, member: str) -> ET.Element | None:
        try:
            with zf.open(member) as fh:
                return ET.parse(fh).getroot()
        except KeyError:
            return None
        except ET.ParseError:
            return None

    def _collect_paragraphs(self, zf: zipfile.ZipFile) -> List[dict]:
        paragraphs = []
        files = ["word/document.xml"]
        files.extend([n for n in zf.namelist() if re.match(r"word/header\d+\.xml", n)])
        files.extend([n for n in zf.namelist() if re.match(r"word/footer\d+\.xml", n)])
        files.extend([n for n in ["word/footnotes.xml", "word/endnotes.xml", "word/comments.xml"] if n in zf.namelist()])

        for member in files:
            root = self._read_xml(zf, member)
            if root is None:
                continue
            for p in root.findall(".//w:p", NS):
                texts = []
                for t in p.findall(".//w:t", NS):
                    texts.append(t.text or "")
                text = "".join(texts).strip()
                pstyle = None
                ppr = p.find("w:pPr", NS)
                if ppr is not None:
                    ps = ppr.find("w:pStyle", NS)
                    if ps is not None:
                        pstyle = ps.attrib.get(f"{{{W_NS}}}val")
                paragraphs.append({"text": text, "style": pstyle, "source": member})
        return paragraphs

    def _sentences(self, text: str) -> List[str]:
        if not text:
            return []
        s = re.split(r"(?<=[\.!?;:])\s+", text)
        return [x.strip() for x in s if x.strip()]

    def _tokens(self, text: str) -> List[str]:
        toks = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ']+", text.lower())
        return toks

    def _top_terms(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, int]]:
        counter = Counter()
        for text in texts:
            for tok in self._tokens(text):
                if len(tok) < 3:
                    continue
                if tok in ITALIAN_STOPWORDS:
                    continue
                counter[tok] += 1
        return counter.most_common(top_n)

    def _formula_counts(self, full_text: str) -> List[Tuple[str, int]]:
        low = full_text.lower()
        counts = []
        for f in FORMULA_PATTERNS:
            counts.append((f, low.count(f)))
        return sorted(counts, key=lambda x: x[1], reverse=True)

    def _metrics_from_paragraphs(self, name: str, paragraphs: List[dict]) -> DocumentMetrics:
        texts = [p["text"] for p in paragraphs]
        non_empty = [t for t in texts if t]
        full_text = "\n".join(non_empty)
        token_count = max(len(self._tokens(full_text)), 1)

        sent_word_lengths = []
        para_word_lengths = []
        for t in non_empty:
            para_word_lengths.append(len(self._tokens(t)))
            for s in self._sentences(t):
                sent_word_lengths.append(len(self._tokens(s)))

        heading_counter = Counter()
        for p in paragraphs:
            style = p.get("style") or ""
            if style:
                heading_counter[style] += 1

        heading_like = sum(v for k, v in heading_counter.items() if "heading" in k.lower() or "titolo" in k.lower())

        semicolon_rate = full_text.count(";") / token_count * 1000
        subordinate_rate = sum(full_text.lower().count(m) for m in SUBORDINATE_MARKERS) / token_count * 1000
        passive_rate = sum(full_text.lower().count(m) for m in PASSIVE_MARKERS) / token_count * 1000

        avg_sent = statistics.mean(sent_word_lengths) if sent_word_lengths else 0.0
        med_sent = statistics.median(sent_word_lengths) if sent_word_lengths else 0.0
        avg_para = statistics.mean(para_word_lengths) if para_word_lengths else 0.0
        med_para = statistics.median(para_word_lengths) if para_word_lengths else 0.0

        return DocumentMetrics(
            name=name,
            paragraphs=len(paragraphs),
            non_empty_paragraphs=len(non_empty),
            headings=heading_like,
            avg_words_per_sentence=round(avg_sent, 2),
            median_words_per_sentence=round(med_sent, 2),
            avg_words_per_paragraph=round(avg_para, 2),
            median_words_per_paragraph=round(med_para, 2),
            semicolon_rate_per_1000_words=round(semicolon_rate, 2),
            subordinate_marker_rate_per_1000_words=round(subordinate_rate, 2),
            passive_marker_rate_per_1000_words=round(passive_rate, 2),
            top_formulas=[x for x in self._formula_counts(full_text) if x[1] > 0][:12],
            top_terms=self._top_terms(non_empty, 20),
            title_styles=heading_counter.most_common(10),
        )

    def _style_map(self, metrics_list: List[DocumentMetrics]) -> dict:
        if not metrics_list:
            return {}

        avg_sent = statistics.mean(m.avg_words_per_sentence for m in metrics_list)
        avg_para = statistics.mean(m.avg_words_per_paragraph for m in metrics_list)
        avg_sub = statistics.mean(m.subordinate_marker_rate_per_1000_words for m in metrics_list)
        avg_passive = statistics.mean(m.passive_marker_rate_per_1000_words for m in metrics_list)
        avg_semicolon = statistics.mean(m.semicolon_rate_per_1000_words for m in metrics_list)

        top_formula_counter = Counter()
        top_term_counter = Counter()
        title_style_counter = Counter()
        for m in metrics_list:
            top_formula_counter.update(dict(m.top_formulas))
            top_term_counter.update(dict(m.top_terms))
            title_style_counter.update(dict(m.title_styles))

        voice = []
        if avg_passive >= 4:
            voice.append("impersonale/istituzionale")
        if avg_sub >= 6:
            voice.append("analitica con subordinate frequenti")
        if avg_sent <= 18:
            voice.append("frasi relativamente brevi")
        elif avg_sent <= 28:
            voice.append("frasi medio-lunghe controllate")
        else:
            voice.append("frasi lunghe e dense")
        if avg_semicolon >= 4:
            voice.append("uso frequente di incisi e segmentazione semicolon")

        structure = {
            "avg_words_per_sentence": round(avg_sent, 2),
            "avg_words_per_paragraph": round(avg_para, 2),
            "heading_styles_seen": title_style_counter.most_common(10),
        }

        syntax = {
            "subordinate_marker_rate_per_1000_words": round(avg_sub, 2),
            "passive_marker_rate_per_1000_words": round(avg_passive, 2),
            "semicolon_rate_per_1000_words": round(avg_semicolon, 2),
        }

        formulas = top_formula_counter.most_common(15)
        lexicon = top_term_counter.most_common(25)

        non_replicate = [
            "commenti interni, placeholder, note operative",
            "refusi o varianti incoerenti del cliente sorgente",
            "nomi propri e residui cliente-specifici",
            "copia meccanica di frasi distintive",
        ]

        style_guidance = [
            "Aprire i paragrafi con una frase neutra, poi scendere nel dettaglio con uno o due livelli di specificazione.",
            "Usare formule ricorrenti solo come ancore stilistiche, non come copia seriale.",
            "Mantenere tono istituzionale, impersonale e professionale.",
            "Collegare il testo a tabelle e allegati con formule di raccordo coerenti.",
        ]

        return {
            "voice_profile": voice,
            "structure_profile": structure,
            "syntax_profile": syntax,
            "top_formulas": formulas,
            "top_terms": lexicon,
            "do_not_replicate": non_replicate,
            "style_guidance": style_guidance,
        }

    def analyze(self) -> dict:
        documents = []
        metrics_objects: List[DocumentMetrics] = []

        for doc in self.doc_paths:
            with zipfile.ZipFile(doc, "r") as zf:
                paragraphs = self._collect_paragraphs(zf)
            metrics = self._metrics_from_paragraphs(doc.name, paragraphs)
            metrics_objects.append(metrics)
            documents.append(asdict(metrics))

        overall = self._style_map(metrics_objects)
        return {
            "documents": documents,
            "overall_style_map": overall,
        }


def render_markdown(report: dict) -> str:
    lines = []
    lines.append("# Style Report")
    lines.append("")
    lines.append("## Sintesi")
    lines.append("Report automatico di estrazione dello stile documentale da uno o più file .docx.")
    lines.append("")

    lines.append("## Documenti analizzati")
    for d in report["documents"]:
        lines.append(f"- **{d['name']}**: {d['non_empty_paragraphs']} paragrafi non vuoti, media {d['avg_words_per_sentence']} parole/frase, media {d['avg_words_per_paragraph']} parole/paragrafo.")
    lines.append("")

    overall = report.get("overall_style_map", {})
    lines.append("## Voce prevalente")
    for item in overall.get("voice_profile", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Struttura")
    structure = overall.get("structure_profile", {})
    lines.append(f"- Media parole per frase: **{structure.get('avg_words_per_sentence', 0)}**")
    lines.append(f"- Media parole per paragrafo: **{structure.get('avg_words_per_paragraph', 0)}**")
    hs = structure.get("heading_styles_seen", [])
    if hs:
        lines.append("- Stili paragrafo/heading osservati:")
        for style, count in hs:
            lines.append(f"  - `{style}`: {count}")
    lines.append("")

    lines.append("## Pattern sintattici")
    syntax = overall.get("syntax_profile", {})
    lines.append(f"- Subordinate marker per 1000 parole: **{syntax.get('subordinate_marker_rate_per_1000_words', 0)}**")
    lines.append(f"- Passive/impersonal marker per 1000 parole: **{syntax.get('passive_marker_rate_per_1000_words', 0)}**")
    lines.append(f"- Punto e virgola per 1000 parole: **{syntax.get('semicolon_rate_per_1000_words', 0)}**")
    lines.append("")

    lines.append("## Formule ricorrenti")
    for formula, count in overall.get("top_formulas", [])[:15]:
        lines.append(f"- `{formula}` — {count}")
    lines.append("")

    lines.append("## Lessico rilevante")
    for term, count in overall.get("top_terms", [])[:25]:
        lines.append(f"- `{term}` — {count}")
    lines.append("")

    lines.append("## Elementi da NON replicare")
    for item in overall.get("do_not_replicate", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Mappa di stile applicabile")
    for item in overall.get("style_guidance", []):
        lines.append(f"- {item}")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analizza uno o più .docx e produce uno Style Report JSON/Markdown.")
    parser.add_argument("inputs", nargs="+", help="Percorsi ai file .docx da analizzare")
    parser.add_argument("--json-out", default="style_report.json", help="Percorso output JSON")
    parser.add_argument("--md-out", default="style_report.md", help="Percorso output Markdown")
    args = parser.parse_args()

    doc_paths = [Path(p) for p in args.inputs]
    missing = [str(p) for p in doc_paths if not p.exists()]
    if missing:
        raise SystemExit(f"File mancanti: {missing}")

    analyzer = StyleAnalyzer(doc_paths)
    report = analyzer.analyze()

    Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    Path(args.md_out).write_text(render_markdown(report), encoding="utf-8")

    print(f"JSON report: {args.json_out}")
    print(f"Markdown report: {args.md_out}")


if __name__ == "__main__":
    main()
