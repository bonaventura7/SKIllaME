from __future__ import annotations

import json
import re
import shutil
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET


# Namespace utili per XML Word / docProps
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
CP_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC_NS = "http://purl.org/dc/elements/1.1/"
DCTERMS_NS = "http://purl.org/dc/terms/"

ET.register_namespace("w", W_NS)
ET.register_namespace("cp", CP_NS)
ET.register_namespace("dc", DC_NS)
ET.register_namespace("dcterms", DCTERMS_NS)


@dataclass
class FactoryReport:
    source_doc: str
    output_doc: str
    modified_files: List[str] = field(default_factory=list)
    replacements_count: Dict[str, int] = field(default_factory=dict)
    residual_hits: Dict[str, List[str]] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    success: bool = False
    message: str = ""

    def to_dict(self) -> dict:
        return {
            "source_doc": self.source_doc,
            "output_doc": self.output_doc,
            "modified_files": self.modified_files,
            "replacements_count": self.replacements_count,
            "residual_hits": self.residual_hits,
            "warnings": self.warnings,
            "success": self.success,
            "message": self.message,
        }


class SBNPTemplateFactory:
    """
    Versione potenziata del Clone & Sanitize:
    - usa temp dir sicura
    - preserva design/document structure
    - sanitizza più XML, non solo document.xml
    - modifica solo text nodes (meno fragile di regex su XML globale)
    - genera report JSON
    - residual scan finale
    """

    BASE_XML_TARGETS = [
        "word/document.xml",
        "word/footnotes.xml",
        "word/endnotes.xml",
        "word/comments.xml",
        "docProps/core.xml",
        "docProps/custom.xml",
    ]

    def __init__(
        self,
        source_doc: str,
        output_doc: str,
        report_path: str | None = None,
        create_backup: bool = True,
        dry_run: bool = False,
    ):
        self.source_doc = Path(source_doc)
        self.output_doc = Path(output_doc)
        self.report_path = Path(report_path) if report_path else self.output_doc.with_suffix(".report.json")
        self.create_backup = create_backup
        self.dry_run = dry_run

        # Regole base:
        # - whole word dove sensato
        # - case-insensitive
        # - anni commentati di default: troppo pericolosi se usati globalmente
        self.replacements = {
            r"\bDamiani\b": "[GRUPPO]",
            r"\bBandera\b": "[GRUPPO]",
            r"\bDigital Bros\b": "[GRUPPO]",
            r"\bValenza\b": "[SEDE_CAPOGRUPPO]",
            r"\bValenze\b": "[SEDE_CAPOGRUPPO]",
            # r"\b2024\b": "[FY]",
            # r"\b2023\b": "[FY_PRECEDENTE]",
        }

        self.compiled_patterns = {
            pattern: re.compile(pattern, re.IGNORECASE)
            for pattern in self.replacements
        }

        self.residual_terms = [
            "Damiani",
            "Bandera",
            "Digital Bros",
            "Valenza",
            "Valenze",
        ]

    # ---------------------------
    # Utility
    # ---------------------------

    def _validate_inputs(self) -> Tuple[bool, str]:
        if not self.source_doc.exists():
            return False, f"Source document not found: {self.source_doc}"
        if self.source_doc.suffix.lower() != ".docx":
            return False, f"Source document is not a .docx: {self.source_doc}"
        return True, "OK"

    def _backup_if_needed(self):
        if self.create_backup and self.output_doc.exists():
            backup_path = self.output_doc.with_suffix(self.output_doc.suffix + ".bak")
            shutil.copy2(self.output_doc, backup_path)

    def _extract_docx(self, temp_dir: Path):
        with zipfile.ZipFile(self.source_doc, "r") as zf:
            zf.extractall(temp_dir)

    def _list_target_xml_files(self, temp_dir: Path) -> List[Path]:
        targets = []

        # target fissi
        for rel_path in self.BASE_XML_TARGETS:
            p = temp_dir / rel_path
            if p.exists():
                targets.append(p)

        # header*.xml / footer*.xml
        word_dir = temp_dir / "word"
        if word_dir.exists():
            for child in word_dir.iterdir():
                if child.is_file() and child.suffix == ".xml":
                    if child.name.startswith("header") or child.name.startswith("footer"):
                        targets.append(child)

        return targets

    def _replace_text(self, text: str, report: FactoryReport) -> str:
        if not text:
            return text

        updated = text
        for pattern, compiled in self.compiled_patterns.items():
            replacement = self.replacements[pattern]
            updated, count = compiled.subn(replacement, updated)
            if count:
                report.replacements_count[pattern] = report.replacements_count.get(pattern, 0) + count
        return updated

    def _sanitize_xml_file(self, xml_path: Path, report: FactoryReport) -> bool:
        changed = False
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # tutti i nodi con testo
            for node in root.iter():
                if node.text:
                    new_text = self._replace_text(node.text, report)
                    if new_text != node.text:
                        node.text = new_text
                        changed = True

            if changed and not self.dry_run:
                tree.write(xml_path, encoding="utf-8", xml_declaration=True)

            if changed:
                report.modified_files.append(str(xml_path))
            return changed

        except ET.ParseError:
            report.warnings.append(f"Parse error su XML, skipped: {xml_path}")
            return False
        except Exception as exc:
            report.warnings.append(f"Errore su {xml_path}: {exc}")
            return False

    def _residual_scan(self, temp_dir: Path, report: FactoryReport):
        xml_files = list(temp_dir.rglob("*.xml"))
        for term in self.residual_terms:
            hits = []
            compiled = re.compile(re.escape(term), re.IGNORECASE)
            for xml_file in xml_files:
                try:
                    content = xml_file.read_text(encoding="utf-8", errors="ignore")
                    if compiled.search(content):
                        hits.append(str(xml_file.relative_to(temp_dir)))
                except Exception as exc:
                    report.warnings.append(f"Residual scan failed on {xml_file}: {exc}")
            if hits:
                report.residual_hits[term] = hits

    def _repackage_docx(self, temp_dir: Path):
        if self.dry_run:
            return

        if self.output_doc.exists():
            self._backup_if_needed()
            self.output_doc.unlink()

        with zipfile.ZipFile(self.output_doc, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(temp_dir.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(temp_dir))

    def _verify_output_zip(self, report: FactoryReport):
        if self.dry_run:
            return

        try:
            with zipfile.ZipFile(self.output_doc, "r") as zf:
                bad_file = zf.testzip()
                if bad_file:
                    report.warnings.append(f"ZIP corruption detected in member: {bad_file}")

                required = {"[Content_Types].xml", "word/document.xml"}
                names = set(zf.namelist())
                missing = required - names
                if missing:
                    report.warnings.append(f"Missing required DOCX parts: {sorted(missing)}")

        except Exception as exc:
            report.warnings.append(f"Output ZIP verification failed: {exc}")

    def _save_report(self, report: FactoryReport):
        self.report_path.write_text(
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    # ---------------------------
    # Main
    # ---------------------------

    def generate(self) -> Tuple[bool, str, FactoryReport]:
        report = FactoryReport(
            source_doc=str(self.source_doc),
            output_doc=str(self.output_doc),
        )

        ok, msg = self._validate_inputs()
        if not ok:
            report.message = msg
            self._save_report(report)
            return False, msg, report

        try:
            with tempfile.TemporaryDirectory(prefix="sbnp_factory_") as tmp:
                temp_dir = Path(tmp)

                # 1. Extract
                self._extract_docx(temp_dir)

                # 2. Target files
                targets = self._list_target_xml_files(temp_dir)
                if not targets:
                    report.warnings.append("No target XML files found.")

                # 3. Sanitize
                for xml_file in targets:
                    self._sanitize_xml_file(xml_file, report)

                # 4. Residual scan prima del repack
                self._residual_scan(temp_dir, report)

                # 5. Repack
                self._repackage_docx(temp_dir)

            # 6. Verify ZIP integrity
            self._verify_output_zip(report)

            # 7. Final message
            if self.dry_run:
                report.success = True
                report.message = (
                    f"Dry run completato. Nessun file scritto. "
                    f"Report disponibile in {self.report_path}"
                )
            elif report.residual_hits:
                report.success = True
                report.message = (
                    f"Template generato con warning: residui ancora presenti. "
                    f"Controlla {self.report_path}"
                )
            else:
                report.success = True
                report.message = f"Template generato correttamente. Report: {self.report_path}"

            self._save_report(report)
            return report.success, report.message, report

        except Exception as exc:
            report.success = False
            report.message = str(exc)
            self._save_report(report)
            return False, str(exc), report


if __name__ == "__main__":
    factory = SBNPTemplateFactory(
        source_doc=r"C:\Users\luca.consalter\Desktop\Pilota\Damiani MF  FY 24 draft.docx",
        output_doc=r"C:\Users\luca.consalter\Desktop\Pilota\SBNP_Masterfile_Template_GOLD.docx",
        report_path=r"C:\Users\luca.consalter\Desktop\Pilota\SBNP_Masterfile_Template_GOLD.report.json",
        create_backup=True,
        dry_run=False,   # metti True per test senza scrivere il docx
    )

    success, msg, report = factory.generate()
    print(f"Result: {success}")
    print(f"Message: {msg}")
    print(f"Modified files: {len(report.modified_files)}")
    print(f"Residual hits: {report.residual_hits}")
