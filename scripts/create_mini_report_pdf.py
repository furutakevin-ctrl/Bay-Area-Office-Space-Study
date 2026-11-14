from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / "office_space_seed_funding_mini_report.pdf"
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CenterTitle", parent=styles["Title"], fontName="DejaVu-Bold", alignment=TA_CENTER, fontSize=20, leading=24))
styles.add(ParagraphStyle(name="Small", parent=styles["Normal"], fontName="DejaVu", fontSize=8.5, leading=10))
styles["BodyText"].fontName = "DejaVu"
styles["Normal"].fontName = "DejaVu"
styles["Heading1"].fontName = "DejaVu-Bold"

def para(text, style="BodyText"):
    return Paragraph(text, styles[style])

def make_table(rows, widths):
    cells = [[para(str(x), "Small") for x in row] for row in rows]
    t = Table(cells, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#B7C9D6")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6F8")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVu", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(.65 * inch, .4 * inch, "Office Space and Seed Funding Among Bay Area Startups")
    canvas.drawRightString(7.85 * inch, .4 * inch, f"Page {doc.page}")
    canvas.restoreState()

story = [
    para("Office Space and Seed Funding Among Bay Area Startups", "CenterTitle"),
    para("Mini research report", "Normal"), Spacer(1, 12),
    para("<b>Executive summary.</b> This project examined whether seed funding differed between Bay Area startups using private office space and startups using shared office space. The final analysis included 50 startups: 35 private-office companies and 15 shared-office companies. It also recorded whether at least one founder had documented prior startup-founder experience."),
    Spacer(1, 8),
    para("Private-office companies had higher funding on both the mean and median measures. Mean seed funding was $8.32 million for private-office companies versus $3.08 million for shared-office companies. Median funding was $5.30 million versus $2.40 million. A log-funding regression adjusted for funding year estimated that shared-office companies raised approximately 66.7% less than private-office companies, p = 0.0166."),
    Spacer(1, 8),
    para("This is an observational association, not a causal estimate. Company age, industry, founder quality, investor networks, geography, and selection into office type may explain part or all of the observed difference."),
    Spacer(1, 12), para("1. Research design", "Heading1"),
    para("Research question: Among Bay Area startups, is seed funding systematically different for companies using shared office space compared with companies using private office space? The primary hypothesis predicted higher seed funding for private-office startups."),
    Spacer(1, 8),
    make_table([["Variable", "Operational definition"], ["Office type", "Private office or shared/coworking office based on public office evidence."], ["Seed funding", "Amount reported for the identified seed round, in U.S. dollars."], ["Founder experience", "1 if at least one founder had documented prior startup-founder experience; 0 if no documented evidence was found."]], [1.55*inch, 5.55*inch]),
    Spacer(1, 12), para("2. Sample composition", "Heading1"),
    make_table([["Office type", "Companies", "Share", "Mean", "Median"], ["Private", "35", "70%", "$8.32M", "$5.30M"], ["Shared", "15", "30%", "$3.08M", "$2.40M"], ["Total", "50", "100%", "$6.81M", "$3.50M"]], [1.6*inch, .9*inch, .8*inch, 1.25*inch, 1.25*inch]),
    Spacer(1, 8), para("Founder experience was coded as documented prior experience for 26 companies and no documented prior experience for 24 companies. A value of 0 means no evidence was found in the reviewed sources; it does not prove that no founder had ever started a company."),
    Spacer(1, 12), para("3. Four-group comparison", "Heading1"),
    make_table([["Group", "Companies", "Mean", "Median"], ["Private / prior experience", "17", "$8.40M", "$6.00M"], ["Private / no documented experience", "18", "$8.24M", "$3.50M"], ["Shared / no documented experience", "6", "$3.34M", "$2.70M"], ["Shared / prior experience", "9", "$2.90M", "$2.00M"]], [3.0*inch, .85*inch, 1.1*inch, 1.1*inch]),
    PageBreak(), para("4. Model results", "Heading1"),
    make_table([["Term", "Percent difference", "p-value", "Interpretation"], ["Shared office", "-66.7%", "0.0166", "Lower predicted funding than private office."], ["Prior founder experience", "-1.0%", "0.9744", "No detectable independent difference."], ["Office x founder experience", "+23.4%", "0.7205", "No evidence that experience changed the office relationship."]], [1.65*inch, 1.15*inch, .8*inch, 3.25*inch]),
    Spacer(1, 10), para("For founders without documented prior experience, the estimated shared-office difference was approximately -66.7%. For founders with documented prior experience, the combined estimate was approximately -58.9%. The interaction was not statistically significant."),
    Spacer(1, 12), para("5. Robustness checks", "Heading1"),
    make_table([["Check", "Result"], ["Private vs. shared, Mann-Whitney p-value", "0.0021"], ["Prior experience vs. no documented experience, p-value", "0.8688"], ["Private mean after excluding three largest rounds", "$6.22M"], ["Shared mean after excluding three largest rounds", "$3.08M"], ["Private median after excluding three largest rounds", "$4.50M"], ["Shared median after excluding three largest rounds", "$2.40M"]], [5.3*inch, 1.55*inch]),
    Spacer(1, 8), para("The private-office funding advantage remained after excluding the three largest rounds, suggesting that the descriptive result is not driven entirely by a few extreme observations."),
    Spacer(1, 12), para("6. Interpretation and limitations", "Heading1"),
    para("The collected data are consistent with the primary hypothesis: private-office startups raised more seed funding than shared-office startups in this sample. The pattern appears in means, medians, the four-group comparison, the adjusted regression, and the nonparametric test."),
    Spacer(1, 8), para("The result should not be interpreted as evidence that private offices cause higher funding. Stronger or more established companies may be more likely to lease private offices. Other limitations include public-source selection, uncertain office classifications, variation in funding-source quality, possible undercounting of founder experience, small shared-office subgroups, and different market conditions across 2023-2026."),
    Spacer(1, 12), para("7. Reproducibility", "Heading1"),
    para("The project includes Python and R workflows, cleaned data, source and audit fields, model outputs, and figures. From the project root, run source(\"R/run_all.R\") in RStudio to rebuild the R outputs. The study should be described as exploratory and observational rather than causal."),
]

doc = SimpleDocTemplate(str(PDF), pagesize=letter, rightMargin=.65*inch, leftMargin=.65*inch, topMargin=.6*inch, bottomMargin=.65*inch)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(PDF)
