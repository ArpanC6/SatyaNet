"""PDF report generator."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from backend.config import settings
from backend.utils.exceptions import ReportGenerationError
from backend.utils.logger import logger


class ReportGenerator:
    def __init__(self):
        self.log = logger.bind(service="report_generator")
        self.styles = getSampleStyleSheet()

    def generate_situation_report(self, project, summary, evidences, output_path=None):
        out = Path(output_path or settings.reports_dir + "/SatyaNet_" + self._slug(project) + "_" + datetime.utcnow().strftime("%Y%m%d_%H%M%S") + ".pdf")
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            doc = SimpleDocTemplate(str(out), pagesize=A4, title="SatyaNet Report")
            story = []
            story.append(Paragraph("SatyaNet - Situation Report", self.styles["Title"]))
            story.append(Paragraph("Project: " + project, self.styles["Normal"]))
            story.append(Paragraph("Generated: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"), self.styles["Normal"]))
            story.append(Spacer(1, 12))

            summary_data = [
                ["Total Evidence", str(summary.get("total", 0))],
                ["Verified", str(summary.get("verified", 0))],
                ["Needs Review", str(summary.get("needs_review", 0))],
                ["Likely Fake", str(summary.get("likely_fake", 0))],
                ["Avg Trust Score", "{0:.1f}/100".format(summary.get("avg_score", 0))],
            ]
            summary_table = Table(summary_data, colWidths=[6 * cm, 6 * cm])
            summary_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1C2336")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2A3447")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 16))

            rows = [["#", "Location", "Date", "Trust", "Verdict"]]
            for i, ev in enumerate(evidences, 1):
                rows.append([
                    str(i),
                    str(ev.get("location_label", "-"))[:28],
                    str(ev.get("claimed_date", "-")),
                    "{0:.1f}".format(ev.get("trust_score", 0)),
                    str(ev.get("verdict", "-")),
                ])
            ev_table = Table(rows, colWidths=[1 * cm, 5 * cm, 3 * cm, 2.5 * cm, 3 * cm])
            ev_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00D4FF")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#2A3447")),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(ev_table)
            doc.build(story)
            self.log.info("Report generated: " + str(out))
            return out
        except Exception as e:
            raise ReportGenerationError(str(e))

    def _slug(self, text):
        import re
        return re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_")
