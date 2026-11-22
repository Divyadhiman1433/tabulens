# TabuLens Presentation Narration

## Slide 1 - Title

Good morning. I am Divya Dhiman, and my AIPT mini-project is TabuLens. It is a Python application that checks, cleans, visualizes and reviews a CSV dataset before later analysis.

## Slide 2 - Problem

A dataset can contain missing values, repeated rows or unusual records even when the code reads it successfully. TabuLens makes these issues visible before model training and keeps every cleaning decision with the user.

## Slide 3 - Workflow

The workflow has six simple steps. The app reads a CSV, profiles it, explains the issues, creates a cleaned copy, suggests unusual rows for review and exports the result as a new file.

## Slide 4 - AIPT concepts

The project uses file handling for CSV input and output, functions and modules for reusable logic, a DatasetAnalyzer class for object-oriented programming, and Python packages for data processing, visualization and anomaly screening.

## Slide 5 - Sample data

The included sample has 182 rows, 7 missing cells and 2 duplicate rows. Its starting readiness score is 84 out of 100, so the app clearly shows what needs attention.

## Slide 6 - Cleaning

The cleaning step removes duplicate rows, fills numeric gaps with the median and fills text gaps with the most common value. The cleaned copy has 180 rows and a score of 100, while the original file stays unchanged.

## Slide 7 - Anomaly screening

Isolation Forest is used only to suggest unusual numeric records. At the 5 percent setting it flags 10 rows. A flag is not proof of an error, so the user must still review the record.

## Slide 8 - Interface

The interface separates the work into clear tabs. The overview explains the source data, while the anomaly tab shows the selected setting, axes, flagged count and interactive chart.

## Slide 9 - Verification

The results are easy to reproduce. The quality score rises from 84 to 100 after cleaning, and the same source passes lint, unit tests and the Streamlit health check in WebPi.

## Slide 10 - Conclusion

TabuLens combines the main AIPT concepts in one small working application. Its main lesson is that data should be understood before it is used. The score and anomaly flags support human review rather than replace it.
