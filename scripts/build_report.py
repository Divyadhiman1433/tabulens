import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "TabuLens_AIPT_Mini_Project_Report.pdf"
CONTENT = json.loads((ROOT / "content" / "project_content.json").read_text())
RESULTS = json.loads((ROOT / "artifacts" / "results.json").read_text())
WIDTH, HEIGHT = letter
TEAL = colors.HexColor("#0F766E")
INK = colors.HexColor("#18181B")
MUTED = colors.HexColor("#52525B")
LINE = colors.HexColor("#D4D4D8")
PAPER = colors.HexColor("#FAFAFA")


def register_fonts() -> tuple[str, str, str]:
    regular = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
    bold = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    mono = Path("/System/Library/Fonts/SFNSMono.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("ReportSans", regular))
        pdfmetrics.registerFont(TTFont("ReportSansBold", bold))
        if mono.exists():
            pdfmetrics.registerFont(TTFont("ReportMono", mono))
            return "ReportSans", "ReportSansBold", "ReportMono"
        return "ReportSans", "ReportSansBold", "Courier"
    return "Helvetica", "Helvetica-Bold", "Courier"


REGULAR, BOLD, MONO = register_fonts()
STYLES = getSampleStyleSheet()
BODY = ParagraphStyle("Body", fontName=REGULAR, fontSize=9.2, leading=13.2, textColor=INK, alignment=TA_LEFT)
SMALL = ParagraphStyle("Small", fontName=REGULAR, fontSize=7.8, leading=10.6, textColor=MUTED)
CAPTION = ParagraphStyle("Caption", fontName=REGULAR, fontSize=7.4, leading=9.4, textColor=MUTED, alignment=TA_CENTER)
CODE = ParagraphStyle("Code", fontName=MONO, fontSize=6.4, leading=8.6, textColor=INK)


def header(pdf: canvas.Canvas, page: int, title: str = "AI PROGRAMMING TOOLS MINI-PROJECT") -> None:
    pdf.setFont(REGULAR, 6.8)
    pdf.setFillColor(MUTED)
    pdf.drawString(0.6 * inch, HEIGHT - 0.45 * inch, title)
    pdf.drawRightString(WIDTH - 0.6 * inch, HEIGHT - 0.45 * inch, "Divya Dhiman | 00702102026")
    pdf.setStrokeColor(LINE)
    pdf.line(0.6 * inch, HEIGHT - 0.55 * inch, WIDTH - 0.6 * inch, HEIGHT - 0.55 * inch)
    pdf.line(0.6 * inch, 0.48 * inch, WIDTH - 0.6 * inch, 0.48 * inch)
    pdf.setFont(REGULAR, 6.8)
    pdf.drawString(0.6 * inch, 0.28 * inch, "Academic AIPT mini-project report")
    pdf.drawRightString(WIDTH - 0.6 * inch, 0.28 * inch, f"Page {page}")


def heading(pdf: canvas.Canvas, text: str, y: float, size: int = 16) -> float:
    pdf.setFillColor(TEAL)
    pdf.setFont(BOLD, size)
    pdf.drawString(0.72 * inch, y, text)
    return y - 0.28 * inch


def paragraph(pdf: canvas.Canvas, text: str, x: float, y: float, width: float, style: ParagraphStyle = BODY) -> float:
    item = Paragraph(text, style)
    _, height = item.wrap(width, HEIGHT)
    item.drawOn(pdf, x, y - height)
    return y - height


def code_box(pdf: canvas.Canvas, title: str, code: str, x: float, y: float, width: float) -> float:
    title_style = ParagraphStyle("CodeTitle", parent=SMALL, fontName=BOLD, textColor=TEAL)
    title_item = Paragraph(title, title_style)
    _, title_height = title_item.wrap(width - 18, 100)
    lines = [line.replace(" ", "&nbsp;") or "&nbsp;" for line in code.splitlines()]
    code_item = Paragraph("<br/>".join(lines), CODE)
    _, code_height = code_item.wrap(width - 20, 400)
    height = title_height + code_height + 26
    pdf.setFillColor(colors.HexColor("#F4F4F5"))
    pdf.setStrokeColor(LINE)
    pdf.roundRect(x, y - height, width, height, 4, fill=1, stroke=1)
    title_item.drawOn(pdf, x + 10, y - title_height - 8)
    code_item.drawOn(pdf, x + 10, y - title_height - code_height - 16)
    return y - height


def image(pdf: canvas.Canvas, path: Path, x: float, y: float, width: float, height: float) -> None:
    item = Image(str(path), width=width, height=height)
    item.drawOn(pdf, x, y)


def table(pdf: canvas.Canvas, data: list[list[str]], x: float, y: float, widths: list[float]) -> float:
    item = Table(data, colWidths=widths, repeatRows=1)
    item.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E4E4E7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), INK),
                ("FONTNAME", (0, 0), (-1, 0), BOLD),
                ("FONTNAME", (0, 1), (-1, -1), REGULAR),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("LEADING", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    _, height = item.wrap(sum(widths), 500)
    item.drawOn(pdf, x, y - height)
    return y - height


def cover(pdf: canvas.Canvas) -> None:
    project = CONTENT["project"]
    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.setFont(BOLD, 12)
    pdf.drawCentredString(WIDTH / 2, HEIGHT - 0.95 * inch, "AI PROGRAMMING TOOLS (AIPT) MINI-PROJECT")
    logo = ROOT / "assets" / "brand" / "igdtuw-logo.png"
    image(pdf, logo, WIDTH / 2 - 0.52 * inch, HEIGHT - 2.28 * inch, 1.04 * inch, 1.04 * inch)
    pdf.setFont(REGULAR, 8)
    pdf.drawCentredString(WIDTH / 2, HEIGHT - 2.7 * inch, project["institution"].upper())
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.5)
    pdf.line(1.25 * inch, HEIGHT - 3.02 * inch, WIDTH - 1.25 * inch, HEIGHT - 3.02 * inch)
    pdf.setFillColor(INK)
    pdf.setFont(BOLD, 24)
    pdf.drawCentredString(WIDTH / 2, HEIGHT - 3.65 * inch, "Dataset Readiness and")
    pdf.drawCentredString(WIDTH / 2, HEIGHT - 4.04 * inch, "Anomaly Screening with Python")
    pdf.setFillColor(TEAL)
    pdf.setFont(BOLD, 12)
    pdf.drawCentredString(WIDTH / 2, HEIGHT - 4.42 * inch, project["name"])
    details = [
        ("Submitted By", project["author"]),
        ("Enrollment No.", project["enrollment"]),
        ("Programme", project["programme"]),
        ("Subject", project["subject"]),
        ("Submitted To", project["submitted_to"]),
    ]
    y = HEIGHT - 5.34 * inch
    for label, value in details:
        pdf.setFont(BOLD, 8.4)
        pdf.setFillColor(MUTED)
        pdf.drawString(1.35 * inch, y, label)
        pdf.setFont(REGULAR, 8.4)
        pdf.setFillColor(INK)
        pdf.drawString(2.8 * inch, y, value)
        pdf.setStrokeColor(LINE)
        pdf.line(1.35 * inch, y - 8, WIDTH - 1.35 * inch, y - 8)
        y -= 0.34 * inch


def build() -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter)
    pdf.setTitle("TabuLens AIPT Mini-Project Report")
    pdf.setAuthor("Divya Dhiman")

    cover(pdf)
    pdf.showPage()

    header(pdf, 2)
    y = heading(pdf, "AIM", HEIGHT - 0.92 * inch)
    y = paragraph(pdf, CONTENT["aim"], 0.72 * inch, y, 6.95 * inch)
    y -= 0.22 * inch
    y = heading(pdf, "PROBLEM STATEMENT", y)
    y = paragraph(pdf, CONTENT["problem"], 0.72 * inch, y, 6.95 * inch)
    y -= 0.25 * inch
    pdf.setFillColor(INK)
    pdf.setFont(BOLD, 11)
    pdf.drawString(0.72 * inch, y, "Experimental Design")
    y -= 0.22 * inch
    design = [
        ["Stage", "Python concept", "Output"],
        ["Load", "File handling and Pandas", "DataFrame"],
        ["Profile", "Functions and OOP", "Quality report"],
        ["Clean", "Missing-value preprocessing", "New CSV copy"],
        ["Screen", "Isolation Forest", "Review suggestions"],
        ["Present", "Streamlit and Plotly", "Interactive application"],
    ]
    y = table(pdf, design, 0.72 * inch, y, [1.25 * inch, 2.55 * inch, 2.75 * inch])
    y -= 0.28 * inch
    pdf.setFont(BOLD, 10)
    pdf.setFillColor(TEAL)
    pdf.drawString(0.72 * inch, y, "Included demonstration dataset")
    y -= 0.18 * inch
    sample = RESULTS["source"]
    paragraph(
        pdf,
        f"The reproducible campus-energy sample contains {sample['rows']} rows and {sample['columns']} columns. "
        f"It intentionally includes {sample['missing_cells']} missing cells, {sample['duplicate_rows']} duplicate rows, "
        "and one unusual energy reading so that every part of the application can be demonstrated safely.",
        0.72 * inch,
        y,
        6.95 * inch,
    )
    pdf.showPage()

    header(pdf, 3)
    y = heading(pdf, "CODE", HEIGHT - 0.92 * inch)
    y = paragraph(
        pdf,
        "Only the central application logic is shown. Interface styling and artifact builders are omitted.",
        0.72 * inch,
        y,
        6.95 * inch,
    )
    y -= 0.18 * inch
    code1 = """class DatasetAnalyzer:
    def __init__(self, frame):
        if frame.empty:
            raise ValueError("The dataset must contain at least one row")
        self.frame = frame.copy()

    def profile(self):
        rows, columns = self.frame.shape
        missing_cells = int(self.frame.isna().sum().sum())
        duplicate_rows = int(self.frame.duplicated().sum())
        numeric_columns = self.frame.select_dtypes(include=np.number).shape[1]
        return DatasetProfile(rows, columns, missing_cells,
                              duplicate_rows, numeric_columns, ...)"""
    y = code_box(pdf, "1. Object-oriented dataset profiling", code1, 0.72 * inch, y, 6.95 * inch)
    y -= 0.22 * inch
    code2 = """def clean(self, drop_duplicates=True, fill_missing=True):
    cleaned = self.frame.copy()
    if drop_duplicates:
        cleaned = cleaned.drop_duplicates()
    if fill_missing:
        for column in cleaned.select_dtypes(include=np.number):
            cleaned[column] = cleaned[column].fillna(cleaned[column].median())
        for column in cleaned.select_dtypes(exclude=np.number):
            cleaned[column] = cleaned[column].fillna(cleaned[column].mode()[0])
    return cleaned.drop_duplicates().reset_index(drop=True)"""
    code_box(pdf, "2. Explainable cleaning rules", code2, 0.72 * inch, y, 6.95 * inch)
    pdf.showPage()

    header(pdf, 4)
    y = heading(pdf, "CODE (CONTINUED)", HEIGHT - 0.92 * inch)
    code3 = """def detect_anomalies(self, contamination=0.05):
    numeric = self.frame.select_dtypes(include=np.number)
    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        IsolationForest(contamination=contamination, random_state=42),
    )
    labels = model.fit_predict(numeric)
    result = self.frame.copy()
    result["is_anomaly"] = labels == -1
    return result"""
    y = code_box(pdf, "3. Isolation Forest screening pipeline", code3, 0.72 * inch, y, 6.95 * inch)
    y -= 0.22 * inch
    code4 = """uploaded = st.file_uploader("CSV file", type=["csv"])
frame = pd.read_csv(uploaded) if uploaded else load_sample()
analyzer = DatasetAnalyzer(frame)
profile = analyzer.profile()

st.metric("Quality score", f"{profile.quality_score}/100")
st.dataframe(analyzer.column_report(), width="stretch")
st.download_button("Download cleaned CSV",
                   analyzer.clean().to_csv(index=False))"""
    y = code_box(pdf, "4. Streamlit input, output, and file export", code4, 0.72 * inch, y, 6.95 * inch)
    y -= 0.22 * inch
    paragraph(
        pdf,
        "The AI component is deliberately limited to screening. Isolation Forest learns which numeric records are easier to isolate from the majority, but the application presents those records for human review rather than deleting them automatically.",
        0.72 * inch,
        y,
        6.95 * inch,
    )
    pdf.showPage()

    header(pdf, 5)
    y = heading(pdf, "OUTPUT", HEIGHT - 0.92 * inch)
    y = paragraph(
        pdf,
        "1. Dataset profile before cleaning",
        0.72 * inch,
        y,
        6.95 * inch,
        ParagraphStyle("Label", parent=BODY, fontName=BOLD),
    )
    y -= 0.12 * inch
    data = [
        ["Measure", "Observed value", "Meaning"],
        ["Rows", "182", "180 source records and 2 duplicates"],
        ["Columns", "6", "Three numeric and three non-numeric"],
        ["Missing cells", "7", "Present in three columns"],
        ["Duplicate rows", "2", "Repeated records"],
        ["Readiness score", "84 / 100", "Issues should be reviewed before analysis"],
    ]
    y = table(pdf, data, 0.72 * inch, y, [1.6 * inch, 1.45 * inch, 3.5 * inch])
    image(pdf, ROOT / "assets" / "figures" / "missing_values.png", 1.05 * inch, 2.28 * inch, 6.05 * inch, 3.24 * inch)
    paragraph(
        pdf,
        "Figure 1. Missing values occur in occupancy, temperature and maintenance status. The chart identifies where cleaning choices are required without changing the data.",
        1.0 * inch,
        2.12 * inch,
        6.1 * inch,
        CAPTION,
    )
    pdf.showPage()

    header(pdf, 6)
    y = heading(pdf, "OUTPUT (CONTINUED)", HEIGHT - 0.92 * inch)
    y = paragraph(
        pdf,
        "2. Cleaned-copy comparison",
        0.72 * inch,
        y,
        6.95 * inch,
        ParagraphStyle("Label2", parent=BODY, fontName=BOLD),
    )
    image(
        pdf, ROOT / "assets" / "figures" / "quality_comparison.png", 1.05 * inch, 4.08 * inch, 6.05 * inch, 3.24 * inch
    )
    paragraph(
        pdf,
        "Figure 2. Removing duplicate rows and filling missing values raises the transparent readiness score from 84 to 100 for the demonstration copy.",
        1.0 * inch,
        3.95 * inch,
        6.1 * inch,
        CAPTION,
    )
    image(pdf, ROOT / "assets" / "screenshots" / "cleaning.png", 1.0 * inch, 0.95 * inch, 6.1 * inch, 2.75 * inch)
    paragraph(
        pdf,
        "The interface reports the effect of each cleaning choice and keeps the original upload unchanged. The user downloads a separate CSV when satisfied with the result.",
        0.72 * inch,
        0.84 * inch,
        6.95 * inch,
        SMALL,
    )
    pdf.showPage()

    header(pdf, 7)
    y = heading(pdf, "OUTPUT (CONTINUED)", HEIGHT - 0.92 * inch)
    y = paragraph(
        pdf, "3. Anomaly screening", 0.72 * inch, y, 6.95 * inch, ParagraphStyle("Label3", parent=BODY, fontName=BOLD)
    )
    image(pdf, ROOT / "assets" / "figures" / "anomaly_screen.png", 1.05 * inch, 3.85 * inch, 6.05 * inch, 3.24 * inch)
    paragraph(
        pdf,
        "Figure 3. At a 5% contamination setting, Isolation Forest suggests 10 records for review. The deliberately extreme energy reading is included among the flagged observations.",
        1.0 * inch,
        3.72 * inch,
        6.1 * inch,
        CAPTION,
    )
    y = 3.18 * inch
    y = paragraph(
        pdf,
        "Isolation Forest is an unsupervised method, so no labelled target is required. It repeatedly divides the numeric feature space and assigns shorter isolation paths to records that differ from the majority.",
        0.72 * inch,
        y,
        6.95 * inch,
    )
    y -= 0.18 * inch
    paragraph(
        pdf,
        "Interpretation boundary: an anomaly may be a valid rare event, a measurement error, or a data-entry problem. TabuLens marks it for review and never removes it automatically.",
        0.72 * inch,
        y,
        6.95 * inch,
        ParagraphStyle("Boundary", parent=BODY, fontName=BOLD, textColor=TEAL),
    )
    pdf.showPage()

    header(pdf, 8)
    y = heading(pdf, "APPLICATION INTERFACE", HEIGHT - 0.92 * inch)
    y = paragraph(
        pdf,
        "The Streamlit application organizes the workflow into four tabs so that a beginner can explain one step at a time: overview, cleaning, anomaly screening, and a plain-language method description.",
        0.72 * inch,
        y,
        6.95 * inch,
    )
    image(pdf, ROOT / "assets" / "screenshots" / "overview.png", 0.82 * inch, 3.9 * inch, 6.75 * inch, 3.8 * inch)
    paragraph(
        pdf,
        "Figure 4. Overview tab with the source profile and missing-value visualization.",
        1.0 * inch,
        3.78 * inch,
        6.1 * inch,
        CAPTION,
    )
    image(pdf, ROOT / "assets" / "screenshots" / "anomalies.png", 0.82 * inch, 0.72 * inch, 6.75 * inch, 2.8 * inch)
    pdf.showPage()

    header(pdf, 9)
    y = heading(pdf, "RESULT AND CONCLUSION", HEIGHT - 0.92 * inch)
    y = paragraph(
        pdf,
        "TabuLens demonstrates an end-to-end Python application that reads files, organizes logic in a reusable class, profiles tabular data with Pandas, visualizes results, applies preprocessing, and uses a simple AI method for anomaly screening. The included sample begins with 182 rows, 7 missing cells and 2 duplicate rows. The cleaned copy contains 180 rows with no missing or duplicate records, while the anomaly screen suggests 10 records for review.",
        0.72 * inch,
        y,
        6.95 * inch,
    )
    y -= 0.2 * inch
    pdf.setFillColor(TEAL)
    pdf.setFont(BOLD, 11)
    pdf.drawString(0.72 * inch, y, "Key Learning Outcomes")
    y -= 0.22 * inch
    for item in CONTENT["learning"]:
        y = paragraph(pdf, f"• {item}", 0.92 * inch, y, 6.55 * inch)
        y -= 0.06 * inch
    y -= 0.12 * inch
    pdf.setFillColor(TEAL)
    pdf.setFont(BOLD, 11)
    pdf.drawString(0.72 * inch, y, "Limitations")
    y -= 0.22 * inch
    for item in CONTENT["limitations"]:
        y = paragraph(pdf, f"• {item}", 0.92 * inch, y, 6.55 * inch)
        y -= 0.06 * inch
    y -= 0.16 * inch
    pdf.setFillColor(colors.HexColor("#ECFDF5"))
    pdf.setStrokeColor(TEAL)
    pdf.roundRect(0.72 * inch, y - 0.78 * inch, 6.95 * inch, 0.72 * inch, 4, fill=1, stroke=1)
    paragraph(
        pdf,
        "The app supports data review; it does not decide whether a real observation is correct. Final cleaning decisions require knowledge of the dataset and its subject.",
        0.88 * inch,
        y - 0.15 * inch,
        6.62 * inch,
        ParagraphStyle("Final", parent=BODY, fontName=BOLD),
    )
    pdf.setFillColor(MUTED)
    pdf.setFont(REGULAR, 7.2)
    pdf.drawString(0.72 * inch, 0.78 * inch, "Project source: github.com/Divyadhiman1433/tabulens")
    pdf.drawString(
        0.72 * inch,
        0.63 * inch,
        "Reproducibility: run python scripts/run_analysis.py to regenerate results and figures.",
    )

    pdf.save()
    return OUTPUT


if __name__ == "__main__":
    print(build())
