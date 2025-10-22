# Quick Start Guide - TP Dashboard Generator

## 1. Create Excel Template

```bash
python3 generate_dashboard.py --create-template MyClient_Data.xlsx
```

This creates an Excel file with three sheets:
- **Client Info** - Company name and fiscal year
- **Countries** - One row per jurisdiction
- **Timeline** - One row per deadline

## 2. Fill in Your Data

### Client Info Sheet
```
Client Name:          Acme Corporation
Fiscal Year End Date: 2025-12-31
Fiscal Year Label:    FYE 2025
```

### Countries Sheet (one row per country)

| Country | ID | Region | Entity | MF | LF | Forms | Thresholds | Docs | Forms | Status | Deadlines |
|---------|----|---------| -------|----|----|-------|------------|------|-------|--------|-----------|
| Germany | germany | Europe | Acme GmbH | Y | Y | N | EUR 100M sales \| EUR 6M RPTs | BEPS compliant | Transaction Matrix | Upon request | 30 Jun 2026 |

**Tips:**
- Use `|` to separate multiple items in a cell
- MF/LF/Forms: Enter `Y` or `N`
- Region must be: Europe, Americas, Asia-Pacific, or Middle East

### Timeline Sheet (one row per deadline)

| Quarter | Country | Date | Description | Type |
|---------|---------|------|-------------|------|
| Q2 2026 (April - June) | Germany | 2026-06-30 | Extraordinary transaction docs due | filing |
| Q3 2026 (July - September) | Germany | 2026-07-31 | MF/LF preparation complete | preparation |

**Tips:**
- Date format: YYYY-MM-DD
- Type: filing, preparation, or upon-request
- Country must match name in Countries sheet

## 3. Generate Dashboard

```bash
python3 generate_dashboard.py MyClient_Data.xlsx MyClient_Dashboard.html
```

## 4. Open in Browser

Double-click `MyClient_Dashboard.html` or:
```bash
open MyClient_Dashboard.html        # Mac
xdg-open MyClient_Dashboard.html   # Linux
start MyClient_Dashboard.html      # Windows
```

## Common Tasks

### Add a New Country
1. Open Excel file
2. Go to Countries sheet
3. Insert a new row
4. Fill in all columns
5. Go to Timeline sheet
6. Add deadline rows for that country
7. Save Excel
8. Regenerate: `python3 generate_dashboard.py MyData.xlsx output.html`

### Edit Existing Country
1. Open Excel file
2. Find the country row
3. Update cells
4. Save
5. Regenerate dashboard

### Remove a Country
1. Open Excel file
2. Delete the entire row from Countries sheet
3. Delete related rows from Timeline sheet
4. Save
5. Regenerate dashboard

## Example: Adding Switzerland

**Countries Sheet - Add this row:**
```
Switzerland | switzerland | Europe | Acme Swiss AG | Y | Y | N | TP documentation recommended | OECD standards | None required | Upon request | Within 30 days of audit request
```

**Timeline Sheet - Add this row:**
```
Q4 2026 (October - December) | Switzerland | | Documentation ready by year-end | preparation
```

## Field Reference

### Multi-Line Fields
Separate items with ` | `:
```
Item 1 | Item 2 | Item 3
```

### Required Fields
- Country Name ✓
- Country ID ✓
- Region ✓
- Entity Name ✓
- MF/LF/Forms (Y or N) ✓

### Optional Fields
- All text fields can be left empty if not applicable
- Timeline dates can be blank for ongoing requirements

## Files You'll Use

| File | Purpose |
|------|---------|
| `TP_Dashboard_Template.xlsx` | Empty template to start with |
| `Meiko_TP_Data.xlsx` | Example with 22 countries |
| `generate_dashboard.py` | Generator script |
| `README_Dashboard_Generator.md` | Full documentation |

## Workflow for Multiple Clients

```bash
# Client A
python3 generate_dashboard.py --create-template ClientA_Data.xlsx
# ... fill in data ...
python3 generate_dashboard.py ClientA_Data.xlsx ClientA_Dashboard.html

# Client B
python3 generate_dashboard.py --create-template ClientB_Data.xlsx
# ... fill in data ...
python3 generate_dashboard.py ClientB_Data.xlsx ClientB_Dashboard.html

# Client C
python3 generate_dashboard.py --create-template ClientC_Data.xlsx
# ... fill in data ...
python3 generate_dashboard.py ClientC_Data.xlsx ClientC_Dashboard.html
```

## Need Help?

1. Check the filled example: `Meiko_TP_Data.xlsx`
2. Read full docs: `README_Dashboard_Generator.md`
3. Look at the Instructions sheet in the Excel template

---

**Quick Tip:** Start with `Meiko_TP_Data.xlsx`, save it as a new name, and modify it for your client. This is faster than starting from scratch!
