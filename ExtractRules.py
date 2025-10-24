# -*- coding: utf-8 -*-
"""
Extract Section 3 (Transfer pricing documentation requirements) into a
country × questions matrix using a fixed schema.

- Row 1: a/b/c section titles
- Row 2: subheadings (TP documentation, CbCR, Master File, Local File, Economic analysis)
- Row 3: question texts
- Row data: answers captured from Section 3 per country

Requires:
  pip install pdfplumber pandas xlsxwriter
"""

from pathlib import Path
import os, sys, re
from typing import List, Tuple
from collections import defaultdict, OrderedDict
import pandas as pd

# ===================== CONFIG =====================
PDF_PATH = Path(r"EY TP Reference Guide 2025.pdf")
COUNTRY_CSV = Path(r"country_codes.csv")  # must contain a 'Country' column
OUT_XLSX = Path("section3_matrix.xlsx")

# For faster testing, only parse the first N pages (set to None for full run)
MAX_PAGES = 50

# Progress prints
PRINT_EVERY_N_PAGES = 10

# ================== SANITY PRINTS ==================
print("PYTHON :", sys.executable)
print("SCRIPT :", os.path.abspath(__file__))
print("CWD    :", os.getcwd())
print("PDF    :", str(PDF_PATH))
print("PDF exists? ", PDF_PATH.exists())
if not PDF_PATH.exists():
    print("❌ PDF not found at the path above. Fix PDF_PATH and rerun.")
    sys.exit(1)

# ================== LOAD COUNTRY ORDER ==================
if not COUNTRY_CSV.exists():
    print("❌ country_codes.csv not found. Please provide a CSV with a 'Country' column in the correct order.")
    sys.exit(1)

codes_df = pd.read_csv(COUNTRY_CSV)
country_col = next((c for c in codes_df.columns if c.strip().lower() == "country"), None)
if not country_col:
    print("❌ 'Country' column not found in country_codes.csv")
    sys.exit(1)

country_list = [str(x).strip() for x in codes_df[country_col].dropna().tolist()]
print(f"[CountryCSV] Loaded {len(country_list)} countries from CSV (order preserved).")

# ================== FIXED SECTION 3 SCHEMA ==================
# (Row1, Row2, Question)
SCHEMA: List[Tuple[str, str, str]] = [
    # a. Applicability
    ("a. Applicability", "", "Does the jurisdiction have transfer pricing documentation guidelines or rules?"),
    ("a. Applicability", "", "If yes, does the transfer pricing documentation need to be submitted or prepared contemporaneously?"),
    ("a. Applicability", "", "Additional details"),
    ("a. Applicability", "", "Does a local branch of a foreign company need to comply with the local transfer pricing rules?"),
    ("a. Applicability", "", "Is there a requirement for transfer pricing documentation to be prepared annually?"),
    ("a. Applicability", "", "Additional details"),
    ("a. Applicability", "", "For a Multinational Enterprise (MNE) with multiple entities in the jurisdiction, is it required to have stand-alone transfer pricing reports for each entity?"),

    # b. Materiality limit or thresholds — TP documentation
    ("b. Materiality limit or thresholds", "TP documentation", "Is there a financial threshold for applicability of TP documentation?"),
    ("b. Materiality limit or thresholds", "TP documentation", "If yes, what financial metric or basis is used to determine the threshold?"),
    ("b. Materiality limit or thresholds", "TP documentation", "Is there any other threshold?"),
    ("b. Materiality limit or thresholds", "TP documentation", "Additional details"),

    # b. Materiality limit or thresholds — CbCR
    ("b. Materiality limit or thresholds", "CbCR", "What is the financial threshold for applicability of CbCR?"),
    ("b. Materiality limit or thresholds", "CbCR", "What financial metric or basis is used to determine the threshold?"),
    ("b. Materiality limit or thresholds", "CbCR", "Is there any other threshold?"),
    ("b. Materiality limit or thresholds", "CbCR", "Additional details"),

    # b. Materiality limit or thresholds — Master File
    ("b. Materiality limit or thresholds", "Master File", "What is the financial threshold for applicability of Master File?"),
    ("b. Materiality limit or thresholds", "Master File", "What financial metric or basis is used to determine the threshold?"),
    ("b. Materiality limit or thresholds", "Master File", "Is there any other threshold?"),
    ("b. Materiality limit or thresholds", "Master File", "Additional details"),

    # b. Materiality limit or thresholds — Local File
    ("b. Materiality limit or thresholds", "Local File", "What is the financial threshold for applicability of Local File?"),
    ("b. Materiality limit or thresholds", "Local File", "What financial metric or basis is used to determine the threshold?"),
    ("b. Materiality limit or thresholds", "Local File", "Is there any other threshold?"),
    ("b. Materiality limit or thresholds", "Local File", "Additional details"),

    # b. Materiality limit or thresholds — Economic analysis
    ("b. Materiality limit or thresholds", "Economic analysis", "Is a financial threshold specified for applicability of Economic analysis?"),
    ("b. Materiality limit or thresholds", "Economic analysis", "What financial metric or basis is used to determine the threshold?"),
    ("b. Materiality limit or thresholds", "Economic analysis", "Is there any other threshold?"),
    ("b. Materiality limit or thresholds", "Economic analysis", "Additional details"),

    # c. Specific requirements
    ("c. Specific requirements", "", "Is there a local language requirement for TP documentation?"),
    ("c. Specific requirements", "", "Additional details"),
    ("c. Specific requirements", "", "Is a safe harbor available?"),
    ("c. Specific requirements", "", "Additional details"),
    ("c. Specific requirements", "", "Is aggregation or individual testing of transactions preferred for an entity?"),
    ("c. Specific requirements", "", "Additional details"),
    ("c. Specific requirements", "", "Is there any other disclosure or compliance requirement?"),
]

# For matching, compile fuzzy prefixes (first ~45 chars) to handle line breaks/bullets
def q_pattern(q: str) -> re.Pattern:
    prefix = re.sub(r"\s+", " ", q.strip())[:45]
    # escape punctuation, ignore straight vs curly quotes, whitespace-insensitive
    prefix = re.escape(prefix)
    prefix = prefix.replace(r"\ ", r"\s+")
    return re.compile(prefix, flags=re.I)

QUESTION_PATTERNS = [q_pattern(q) for _, _, q in SCHEMA]

# ================== PDF LOADING ====================
try:
    import pdfplumber
except ImportError:
    print("❌ pdfplumber not installed. Run: pip install pdfplumber pandas xlsxwriter")
    sys.exit(1)

def extract_lines(page) -> List[str]:
    """Simple line extraction; positions not needed for fixed-schema approach."""
    text = page.extract_text() or ""
    lines = text.splitlines()
    return [re.sub(r"\s+", " ", ln).strip() for ln in lines]

all_lines: List[str] = []
with pdfplumber.open(str(PDF_PATH)) as pdf:
    total_pages = len(pdf.pages)
    pages_to_read = min(total_pages, MAX_PAGES) if MAX_PAGES else total_pages
    for i, page in enumerate(pdf.pages[:pages_to_read], start=1):
        if PRINT_EVERY_N_PAGES and i % PRINT_EVERY_N_PAGES == 0:
            print(f"Reading page {i}/{pages_to_read} ...", end="\r")
        all_lines.extend(extract_lines(page))
print(f"\n[PDF] Loaded {len(all_lines)} lines from {pages_to_read} pages (test mode).")

# ================== CHAPTER SPLIT BY SECTION 1 ==================
SECTION1_RE = re.compile(r"^\s*1\.\s*Tax authority and relevant transfer pricing", re.I)
SECTION4_RE = re.compile(r"^\s*4\.\s", re.I)
SECTION3_RE = re.compile(r"^\s*3\.\s", re.I)

anchors = [idx for idx, ln in enumerate(all_lines) if SECTION1_RE.match(ln)]
if not anchors:
    print("❌ Could not find any '1. Tax authority...' anchors. Check PDF content/first pages limit.")
    sys.exit(1)

# Build blocks between Section 1 anchors (ignore country names; we'll assign from CSV order)
blocks = []
for i, start in enumerate(anchors):
    end = anchors[i+1] if i+1 < len(anchors) else len(all_lines)
    blocks.append(all_lines[start:end])

print(f"[Chapters] Found {len(blocks)} chapters (by Section 1 anchor).")

# Assign countries by CSV order, trimming to available blocks
num_rows = min(len(country_list), len(blocks))
paired = list(zip(country_list[:num_rows], blocks[:num_rows]))
if len(country_list) > len(blocks):
    print(f"⚠️ CSV has {len(country_list)} countries but only {len(blocks)} chapters within page limit; extra countries will be blank.")
elif len(blocks) > len(country_list):
    print(f"⚠️ Found {len(blocks)} chapters but CSV lists {len(country_list)} countries; extra chapters ignored in test mode.")

# ================== FIND SECTION 3 PER CHAPTER ==================
def get_section3_text(lines: List[str]) -> str:
    """Return raw text from '3.' header up to before '4.' within a chapter."""
    txt = "\n".join(lines)
    # find start of 3.
    m3 = SECTION3_RE.search(txt)
    if not m3:
        return ""
    start = m3.start()
    # find next 4.
    m4 = SECTION4_RE.search(txt[m3.end():])
    end = m3.start() + (m4.start() if m4 else len(txt) - m3.start())
    return txt[start:end]

# ================== ANSWER EXTRACTION (fixed schema) ==================
def normalize_for_match(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    # normalize bullets/dashes to single space
    s = re.sub(r"^\s*[•▪◦●·\-–—\*]\s+", "", s, flags=re.M)
    return s.strip()

def extract_section3_answers(section_text: str, debug_country: str = "") -> List[str]:
    """Return list of answers aligned with SCHEMA order."""
    answers = [""] * len(SCHEMA)
    if not section_text.strip():
        return answers

    text = normalize_for_match(section_text)
    # Make a single space stream to make regex spans simpler
    stream = re.sub(r"\s+", " ", text).strip()

    # Find spans for each question in order
    spans = []
    pos = 0
    for i, pat in enumerate(QUESTION_PATTERNS):
        m = pat.search(stream, pos)
        if m:
            spans.append((m.start(), m.end()))
            pos = m.end()
            if debug_country:
                print(f"  Q{i+1} found at pos {m.start()}: {SCHEMA[i][2][:60]}...")
        else:
            spans.append((None, None))
            if debug_country:
                print(f"  Q{i+1} NOT FOUND: {SCHEMA[i][2][:60]}...")

    # For each found question, capture text until next found question (or end)
    for i, (s, e) in enumerate(spans):
        if s is None:
            continue
        next_start = len(stream)
        for j in range(i+1, len(spans)):
            if spans[j][0] is not None:
                next_start = spans[j][0]
                break
        ans = stream[e:next_start].strip()
        # Clean up: remove question text if it leaked into answer
        ans = re.sub(r"^[:\-–—]\s*", "", ans)
        answers[i] = ans

    return answers

# ================== BUILD MATRIX ==================
# Header rows
row1 = [""] + [sec for (sec, _, _) in SCHEMA]
row2 = [""] + [sub for (_, sub, _) in SCHEMA]
row3 = ["Country"] + [q for (_, _, q) in SCHEMA]

data_rows = []
tidy_rows = []

# DEBUG: Process first country with detailed output
if paired:
    first_country, first_chap = paired[0]
    print(f"\n[DEBUG] Processing first country: {first_country}")
    sec3 = get_section3_text(first_chap)
    print(f"[DEBUG] Section 3 text length: {len(sec3)} chars")
    if sec3:
        print(f"[DEBUG] First 200 chars of Section 3:\n{sec3[:200]}\n")
    ans_list = extract_section3_answers(sec3, debug_country=first_country)
    print(f"[DEBUG] Extracted {len([a for a in ans_list if a])} non-empty answers out of {len(SCHEMA)}")

for country, chap_lines in paired:
    sec3 = get_section3_text(chap_lines)
    ans_list = extract_section3_answers(sec3)
    row = [country] + ans_list
    data_rows.append(row)

    # tidy rows
    for (sec, sub, q), a in zip(SCHEMA, ans_list):
        tidy_rows.append([country, sec, sub, q, a])

# If CSV had more countries than chapters (in test mode), append empty rows
if len(country_list) > len(paired):
    for country in country_list[len(paired):]:
        row = [country] + [""] * len(SCHEMA)
        data_rows.append(row)
        for (sec, sub, q) in [(s[0], s[1], s[2]) for s in SCHEMA]:
            tidy_rows.append([country, sec, sub, q, ""])

# ================== WRITE EXCEL ==================
with pd.ExcelWriter(OUT_XLSX, engine="xlsxwriter") as xw:
    wb = xw.book
    ws = wb.add_worksheet("Section3_Matrix")
    xw.sheets["Section3_Matrix"] = ws

    ws.write_row(0, 0, row1)
    ws.write_row(1, 0, row2)
    ws.write_row(2, 0, row3)

    start_r = 3
    for r_idx, row in enumerate(data_rows, start=start_r):
        ws.write_row(r_idx, 0, row)

    wrap = wb.add_format({"text_wrap": True, "valign": "top"})
    header_fmt = wb.add_format({"bold": True, "text_wrap": True})

    ws.set_row(0, None, header_fmt)
    ws.set_row(1, None, header_fmt)
    ws.set_row(2, None, header_fmt)
    ws.freeze_panes(3, 1)
    ws.set_column(0, 0, 24)  # Country
    ws.set_column(1, len(row1)-1, 42, wrap)

    # Tidy sheet
    tidy_df = pd.DataFrame(tidy_rows, columns=["Country", "Section", "Subheading", "Question", "Answer"])
    tidy_df.to_excel(xw, index=False, sheet_name="Tidy_Long")

print(f"\n[OK] Wrote: {OUT_XLSX}")
print("Tip: set MAX_PAGES = None for a full run once you're happy with the first-50-pages test.")
