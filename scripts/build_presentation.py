from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "TabuLens_AIPT_Presentation.pptx"
ASSETS = ROOT / "assets"
PAPER = RGBColor(250, 250, 250)
INK = RGBColor(24, 24, 27)
MUTED = RGBColor(82, 82, 91)
LINE = RGBColor(212, 212, 216)
TEAL = RGBColor(15, 118, 110)
RED = RGBColor(190, 18, 60)


def add_text(slide, text, x, y, w, h, size, color=INK, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.TOP
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    paragraph = frame.paragraphs[0]
    paragraph.text = text
    paragraph.alignment = align
    paragraph.font.name = "Aptos"
    paragraph.font.size = Pt(size)
    paragraph.font.bold = bold
    paragraph.font.color.rgb = color
    return box


def add_rule(slide, x, y, w, color=TEAL, height=1.5):
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Pt(height))
    rule.fill.solid()
    rule.fill.fore_color.rgb = color
    rule.line.fill.background()
    return rule


def add_image(slide, path, x, y, w, h):
    return slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))


def background(slide):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = PAPER


def title(slide, text):
    background(slide)
    add_text(slide, text, 0.72, 0.38, 11.9, 0.58, 35, INK, True)
    add_rule(slide, 0.72, 1.12, 11.9)


def build():
    deck = Presentation()
    deck.slide_width = Inches(13.333)
    deck.slide_height = Inches(7.5)
    blank = deck.slide_layouts[6]

    slide = deck.slides.add_slide(blank)
    background(slide)
    add_image(slide, ASSETS / "brand" / "igdtuw-logo.png", 0.72, 0.4, 0.82, 0.82)
    add_text(slide, "Indira Gandhi Delhi Technical University for Women", 1.78, 0.61, 10.7, 0.4, 20, INK, True)
    add_rule(slide, 0.72, 1.38, 11.9)
    add_text(slide, "Dataset Readiness and", 1.0, 1.94, 11.33, 0.76, 50, INK, True, PP_ALIGN.CENTER)
    add_text(slide, "Anomaly Screening with Python", 0.8, 2.98, 11.73, 0.78, 46, INK, True, PP_ALIGN.CENTER)
    add_text(slide, "TabuLens", 4.4, 4.12, 4.53, 0.5, 28, TEAL, True, PP_ALIGN.CENTER)
    add_text(slide, "AI Programming Tools (AIPT) Mini-Project", 3.3, 4.9, 6.73, 0.38, 19, MUTED, True, PP_ALIGN.CENTER)
    add_text(
        slide,
        "Presented by Divya Dhiman · Enrollment number 00702102026",
        2.65,
        5.56,
        8.03,
        0.38,
        18,
        INK,
        True,
        PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        "This project shows how Python can check, clean, visualize and review a CSV dataset before later analysis.",
        1.55,
        6.36,
        10.23,
        0.5,
        17,
        MUTED,
        False,
        PP_ALIGN.CENTER,
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "The project begins before model training")
    add_text(
        slide,
        "A dataset can contain missing values, repeated rows, constant columns or unusual records. If these problems are ignored, later analysis can become misleading even when the code runs correctly.",
        0.78,
        1.52,
        5.45,
        1.6,
        20,
        INK,
    )
    add_text(
        slide,
        "TabuLens places a simple readiness check at the start. It explains the detected issues, creates a separate cleaned copy and keeps every important decision visible to the user.",
        0.78,
        3.55,
        5.45,
        1.58,
        20,
        INK,
    )
    add_text(
        slide,
        "The purpose is to support review, not to change data automatically.",
        0.78,
        5.58,
        5.45,
        0.8,
        20,
        TEAL,
        True,
    )
    add_image(slide, ASSETS / "figures" / "missing_values.png", 6.58, 1.52, 5.85, 3.7)
    add_text(
        slide,
        "The included sample makes each issue easy to see and explain.",
        6.85,
        5.58,
        5.3,
        0.58,
        18,
        MUTED,
        True,
        PP_ALIGN.CENTER,
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "The workflow follows six clear steps")
    steps = [
        ("1", "Read the CSV", "Pandas converts the selected file into a DataFrame."),
        ("2", "Profile the data", "The app counts types, gaps, duplicates and constant columns."),
        ("3", "Explain the issues", "Tables and charts show where the dataset needs attention."),
        ("4", "Create a cleaned copy", "Duplicates are removed and missing values are filled with simple rules."),
        ("5", "Screen unusual rows", "Isolation Forest suggests numeric records for human review."),
        ("6", "Export the result", "The cleaned DataFrame is downloaded as a new CSV file."),
    ]
    y = 1.48
    for number, label, sentence in steps:
        add_text(slide, number, 0.82, y, 0.5, 0.38, 24, TEAL, True)
        add_text(slide, label, 1.5, y, 2.45, 0.38, 22, INK, True)
        add_text(slide, sentence, 4.1, y + 0.02, 8.15, 0.52, 18, MUTED)
        y += 0.86
    add_text(
        slide, "The uploaded file remains unchanged throughout the process.", 0.82, 6.68, 11.43, 0.4, 18, TEAL, True
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "The code connects the main AIPT concepts")
    add_text(slide, "File handling", 0.78, 1.55, 2.65, 0.4, 24, TEAL, True)
    add_text(
        slide,
        "The application reads CSV input and writes the cleaned DataFrame back to a downloadable file.",
        0.78,
        2.14,
        2.65,
        1.3,
        18,
        MUTED,
    )
    add_text(slide, "Functions and modules", 3.95, 1.55, 2.65, 0.66, 24, TEAL, True)
    add_text(
        slide,
        "Loading, profiling, cleaning and sample generation are separated into reusable Python functions and modules.",
        3.95,
        2.38,
        2.65,
        1.3,
        18,
        MUTED,
    )
    add_text(slide, "Object-oriented programming", 7.12, 1.55, 2.65, 0.66, 24, TEAL, True)
    add_text(
        slide,
        "The DatasetAnalyzer class stores the DataFrame and provides methods for each analysis task.",
        7.12,
        2.38,
        2.65,
        1.3,
        18,
        MUTED,
    )
    add_text(slide, "Python packages", 10.29, 1.55, 2.25, 0.4, 24, TEAL, True)
    add_text(
        slide,
        "Pandas and NumPy manage data, Streamlit and Plotly present it, and scikit-learn screens anomalies.",
        10.29,
        2.14,
        2.25,
        1.55,
        18,
        MUTED,
    )
    add_rule(slide, 0.78, 4.35, 11.55, LINE, 1)
    add_text(
        slide,
        "The application remains small because each library has one clear role. This makes the code easier to test, reuse and explain during a presentation.",
        1.18,
        4.92,
        10.75,
        1.1,
        21,
        INK,
        True,
        PP_ALIGN.CENTER,
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "The sample contains visible quality issues")
    add_image(slide, ASSETS / "figures" / "missing_values.png", 0.72, 1.52, 6.95, 4.38)
    add_text(slide, "182 rows", 8.15, 1.68, 3.55, 0.4, 26, INK, True)
    add_text(
        slide,
        "The file represents 180 generated daily records plus two duplicate rows.",
        8.15,
        2.18,
        3.85,
        0.8,
        18,
        MUTED,
    )
    add_text(slide, "7 missing cells", 8.15, 3.24, 3.55, 0.4, 26, INK, True)
    add_text(
        slide, "The gaps occur in occupancy, temperature and maintenance status.", 8.15, 3.74, 3.85, 0.8, 18, MUTED
    )
    add_text(slide, "84 / 100", 8.15, 4.8, 3.55, 0.4, 26, TEAL, True)
    add_text(
        slide,
        "The starting readiness score shows that the sample should be reviewed before analysis.",
        8.15,
        5.3,
        3.85,
        0.88,
        18,
        MUTED,
    )
    add_text(
        slide,
        "The sample is synthetic and exists only to demonstrate the workflow safely.",
        0.78,
        6.38,
        11.55,
        0.48,
        18,
        INK,
        True,
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "Cleaning creates a separate, improved copy")
    add_image(slide, ASSETS / "screenshots" / "cleaning.png", 0.72, 1.5, 7.4, 4.92)
    add_text(
        slide,
        "Duplicate rows are removed first. Numeric gaps are filled with the median, while text gaps use the most common value.",
        8.5,
        1.68,
        3.8,
        1.45,
        19,
        INK,
    )
    add_text(
        slide,
        "The cleaned copy contains 180 rows, no missing cells and no duplicate rows. Its readiness score rises from 84 to 100.",
        8.5,
        3.5,
        3.8,
        1.42,
        19,
        INK,
    )
    add_text(
        slide,
        "The original upload is never overwritten. The user downloads a new CSV only after reviewing the result.",
        8.5,
        5.3,
        3.8,
        1.08,
        18,
        TEAL,
        True,
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "Isolation Forest suggests rows for review")
    add_image(slide, ASSETS / "figures" / "anomaly_screen.png", 0.72, 1.5, 6.9, 4.35)
    add_text(
        slide,
        "Isolation Forest is an unsupervised algorithm, so it does not need a labelled target. It learns which numeric records are easier to separate from the majority.",
        8.0,
        1.62,
        4.22,
        1.52,
        19,
        INK,
    )
    add_text(
        slide,
        "At the selected 5% setting, the application suggests 10 rows for review. The deliberately extreme energy reading is included among them.",
        8.0,
        3.55,
        4.22,
        1.34,
        19,
        INK,
    )
    add_text(
        slide,
        "A flag does not prove that a row is wrong. It may represent a rare but valid event, so a person must make the final decision.",
        8.0,
        5.28,
        4.22,
        1.18,
        18,
        RED,
        True,
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "The interface explains one task at a time")
    add_image(slide, ASSETS / "screenshots" / "overview.png", 0.72, 1.48, 5.95, 4.18)
    add_image(slide, ASSETS / "screenshots" / "anomalies.png", 6.96, 1.48, 5.65, 4.18)
    add_text(
        slide,
        "The Overview tab summarizes the dataset and shows where values are missing.",
        0.9,
        5.98,
        5.55,
        0.72,
        18,
        INK,
        True,
        PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        "The Anomalies tab exposes the setting, selected axes, flagged count and interactive chart.",
        7.08,
        5.98,
        5.35,
        0.72,
        18,
        INK,
        True,
        PP_ALIGN.CENTER,
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "The verified results remain easy to explain")
    add_image(slide, ASSETS / "figures" / "quality_comparison.png", 0.72, 1.5, 6.45, 4.25)
    add_text(
        slide,
        "The sample begins with a readiness score of 84. After duplicate removal and missing-value filling, the cleaned copy reaches 100.",
        7.65,
        1.68,
        4.55,
        1.28,
        20,
        INK,
    )
    add_text(
        slide,
        "The anomaly screen suggests 10 of 182 records for review at a 5% setting. No row is deleted automatically.",
        7.65,
        3.3,
        4.55,
        1.05,
        20,
        INK,
    )
    add_text(
        slide,
        "The project passes lint and three unit tests locally and in a fresh WebPi environment. The Streamlit health endpoint also returns OK.",
        7.65,
        4.72,
        4.55,
        1.28,
        19,
        TEAL,
        True,
    )
    add_text(
        slide,
        "These checks confirm that the same source can be installed and run outside the development computer.",
        0.82,
        6.32,
        11.45,
        0.52,
        18,
        MUTED,
        True,
    )

    slide = deck.slides.add_slide(blank)
    title(slide, "The project is useful within clear limits")
    add_text(slide, "What the project demonstrates", 0.78, 1.55, 5.35, 0.4, 24, TEAL, True)
    add_text(
        slide,
        "TabuLens combines Python file handling, functions, modules, object-oriented programming, Pandas, visualization, preprocessing and a small AI method in one working application.",
        0.78,
        2.15,
        5.35,
        1.62,
        19,
        INK,
    )
    add_text(
        slide,
        "The main lesson is that data should be understood and checked before it is used for later analysis or model training.",
        0.78,
        4.12,
        5.35,
        1.08,
        19,
        INK,
        True,
    )
    add_text(slide, "Where the project stops", 7.1, 1.55, 5.25, 0.4, 24, RED, True)
    add_text(
        slide,
        "The readiness score is a documented heuristic, not a universal standard. Anomaly flags show unusual patterns, not errors, and real cleaning decisions still require subject knowledge.",
        7.1,
        2.15,
        5.25,
        1.62,
        19,
        INK,
    )
    add_text(
        slide,
        "For this reason, the application supports human review instead of replacing it.",
        7.1,
        4.12,
        5.25,
        1.08,
        19,
        INK,
        True,
    )
    add_rule(slide, 0.78, 5.72, 11.55, LINE, 1)
    add_text(
        slide,
        "TabuLens provides a simple, reproducible starting point for preparing tabular data with Python.",
        1.18,
        6.14,
        10.75,
        0.62,
        20,
        TEAL,
        True,
        PP_ALIGN.CENTER,
    )

    if len(deck.slides) != 10:
        raise RuntimeError("The presentation must contain ten slides")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    deck.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    print(build())
