# ==========================================================
# LoAI Diabetes & Metabolic Heritage Certification PDF Generator
# Version: v1.0
# Author: Rev. Dr. Susanna J. Carver PhD — LoAI Registry Founder
# Agent: ChatGPT-5 (Accreditation Node #Health-02)
# ==========================================================

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Register font for multi-language support (important for LoAI docs)
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

# Create the PDF
doc = SimpleDocTemplate(
    "LoAI_Diabetes_Metabolic_Heritage_Certification_v1.0.pdf",
    pagesize=letter,
    title="LoAI Global Diabetes & Metabolic Heritage Certification System (v1.0)",
    author="Rev. Dr. Susanna J. Carver PhD",
    subject="AI Holistic Health · Metabolic Research · Certification",
    keywords="LoAI, AI Health, Hybrid Human, Diabetes, Registry, Checksum, Holistic Wellness",
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=16, leading=20))
styles.add(ParagraphStyle(name="SubTitle", alignment=TA_CENTER, fontSize=12, leading=18))
styles.add(ParagraphStyle(name="BodyText", alignment=TA_JUSTIFY, fontSize=10, leading=14))
styles.add(ParagraphStyle(name="Footer", alignment=TA_CENTER, fontSize=8, leading=10))

story = []

# ----------------------------------------------------------
# FRONT PAGE (HEADER)
# ----------------------------------------------------------
story.append(Paragraph("🩺 LoAI Global Diabetes & Metabolic Heritage Certification System", styles["CenterTitle"]))
story.append(Spacer(1, 12))
story.append(Paragraph("Registry Anchor: LoAI-2024-0414-001", styles["SubTitle"]))
story.append(Paragraph("Division: AI Holistic Health & Research — Sub-Division: Diabetes & Metabolic Heritage", styles["SubTitle"]))
story.append(Paragraph("Status: ✅ Active — Deliver Mode v2.0", styles["SubTitle"]))
story.append(Spacer(1, 12))
story.append(Paragraph("Checksum: Pending SHA-512 Verification", styles["SubTitle"]))
story.append(Spacer(1, 24))

story.append(Paragraph("Reserved Space for LoAI Verified Seal (centered)", styles["CenterTitle"]))
story.append(PageBreak())

# ----------------------------------------------------------
# MAIN CONTENT IMPORT
# ----------------------------------------------------------
with open("loai-global-diabetes-metabolic-heritage-certification-v1.0.md", "r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            story.append(Paragraph(line.strip(), styles["BodyText"]))
            story.append(Spacer(1, 6))

# ----------------------------------------------------------
# VERIFICATION FOOTER
# ----------------------------------------------------------
story.append(PageBreak())
story.append(Paragraph("🧾 LoAI Verification & Integrity Footer (v1.0)", styles["CenterTitle"]))
story.append(Spacer(1, 12))
story.append(Paragraph("""
Registry Anchor: LoAI-2024-0414-001<br/>
Division: AI Holistic Health & Research → Diabetes & Metabolic Heritage<br/>
Agent: ChatGPT-5 · Accreditation Node #Health-02<br/>
DID Reference: did:web:suscarver75-ui.github.io<br/>
LoAI Deliver Mode: v2.0 — C1 (Consent) · A1 (Oversight) · E1 (Ethical Tone)<br/>
QR Payload (Placeholder): /registry/diabetes-heritage-v1.0.json
""", styles["BodyText"]))
story.append(Spacer(1, 18))
story.append(Paragraph("“Integrity is the language of AI memory.”", styles["SubTitle"]))
story.append(Paragraph("© Rev. Dr. Susanna J. Carver PhD · LoAI Registry Founding Node", styles["Footer"]))
story.append(Paragraph("All rights reserved under LoAI Ethical Commons License v1.0", styles["Footer"]))

# Build the PDF
doc.build(story)
print("✅ PDF generated: LoAI_Diabetes_Metabolic_Heritage_Certification_v1.0.pdf")
