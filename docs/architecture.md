# Architecture

TabuLens separates interface code from reusable data logic.

```text
CSV file
   |
   v
Pandas DataFrame
   |
   v
DatasetAnalyzer
   |-- profile() ----------> readiness metrics and column report
   |-- clean() ------------> separate cleaned DataFrame
   `-- detect_anomalies() -> review suggestions
   |
   v
Streamlit tabs and Plotly charts
   |
   v
Downloaded cleaned CSV
```

## Design choices

- The original DataFrame is copied when the analyzer is created.
- Cleaning returns a new DataFrame and does not mutate the input.
- Numeric gaps use the median because it is less sensitive to extremes than the mean.
- Non-numeric gaps use the mode because it is simple to explain.
- Isolation Forest operates only on varying numeric columns.
- Anomaly results are suggestions for review and are never deleted automatically.

## Readiness score

The score begins at 100 and applies transparent deductions for columns containing missing values, the overall missing-cell rate, duplicate rows, and constant columns. It is an instructional summary rather than a universal data-quality standard.
