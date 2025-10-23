# Rule-Based TP Compliance System - Prototype Guide

## Overview

This prototype demonstrates a **rule-based system** for TP compliance determination that:
- ✅ Handles multiple threshold conditions (revenue OR employees OR balance sheet)
- ✅ Separates country rules (reusable) from client data (per engagement)
- ✅ Automatically determines MF/LF/CbCR requirements
- ✅ Flags missing data and generates data request lists
- ✅ Supports complex AND/OR logic

**Prototype Scope:** Germany and Spain

---

## Files Created

| File | Purpose |
|------|---------|
| `Country_Rules_Library.xlsx` | Master rules for all countries (edit once, reuse forever) |
| `Client_Data_Template.xlsx` | Input client/entity data (one per engagement) |
| `apply_rules.py` | Logic engine that applies rules to data |
| `create_rules_template.py` | Script to regenerate templates |

---

## How It Works

### **Architecture:**

```
┌──────────────────────────┐
│ Country_Rules_Library   │ → Defines WHEN requirements apply
│  - MF thresholds        │   (Group revenue >= 750M EUR)
│  - LF thresholds        │   (Local sales >= 100M EUR)
│  - CbCR rules           │   (RPTs > 6M EUR)
│  - Forms & deadlines    │
└──────────────────────────┘
            +
┌──────────────────────────┐
│ Client_Data_Template    │ → Your client's actual numbers
│  - Group revenue: 850M  │   (Real data)
│  - Entity revenue: ?    │   (Use ? for unknown)
│  - RPTs: ?              │
└──────────────────────────┘
            ↓
    ┌───────────────┐
    │ apply_rules.py│ → Logic engine
    └───────────────┘
            ↓
┌──────────────────────────┐
│ Assessment Output       │
│  ✓ MF: REQUIRED         │
│  ⚠️  LF: LIKELY REQUIRED│
│  📋 DATA NEEDED:        │
│     - Entity revenue    │
│     - Goods RPTs        │
└──────────────────────────┘
```

---

## Quick Start

### **Step 1: Review Country Rules**

```bash
# Open the rules library
open Country_Rules_Library.xlsx
```

**What's in there:**
- Sheet 1: **MF Requirements** - Examples for Germany and Spain already filled in
- Sheet 2: **LF Requirements** - Examples already filled in
- Sheet 3: **CbCR Requirements** - Standard 750M threshold
- Sheet 4: **Forms Requirements** - Which forms are required
- Sheet 5: **Deadlines** - Filing and preparation deadlines

**The examples are REAL rules** - you can use them as-is or modify.

### **Step 2: Fill in Client Data**

```bash
# Copy the template
cp Client_Data_Template.xlsx My_Client_Data.xlsx

# Open and fill in
open My_Client_Data.xlsx
```

**Fill in:**
- **Client Info sheet:**
  - Client name
  - FYE date
  - Group revenue (in EUR)

- **Entity Data sheet:**
  - One row per German/Spanish entity
  - Fill in what you know
  - Use `?` for unknown data

**Example:**
```
Country | Entity Name    | Local Revenue | RPTs Goods | RPTs Other | ...
Germany | Acme GmbH      | 120000000     | ?          | ?          | ...
Spain   | Acme Spain SA  | ?             | ?          | ?          | ...
```

### **Step 3: Run the Assessment**

```bash
python3 apply_rules.py Country_Rules_Library.xlsx My_Client_Data.xlsx
```

**Output:**
```
================================================================================
TP COMPLIANCE ASSESSMENT - Acme Corporation
FYE: 2025-12-31
================================================================================

────────────────────────────────────────────────────────────────────────────────
ENTITY: Acme GmbH
Country: Germany
────────────────────────────────────────────────────────────────────────────────

Master File: ✓ REQUIRED
Confidence: HIGH
  ✓ Revenue (850,000,000) >= 750,000,000

Local File: ⚠️  LIKELY REQUIRED - VERIFICATION NEEDED
Confidence: LOW - NEED DATA
  ? RPTs (Goods) data not provided
  ? RPTs (Other) data not provided

📋 DATA NEEDED:
  - RPTs (Transaction (Goods))
  - RPTs (Transaction (Other))
```

---

## Understanding the Rules

### **Multi-Condition Logic**

Rules can have **multiple conditions** with AND/OR logic.

**Example:** Germany LF is required if:
```
(Goods RPTs > 6M EUR) OR (Other RPTs > 600K EUR)
```

This is represented in Excel as:

| Rule ID | Condition Group | Group Logic | Metric Type | Threshold |
|---------|-----------------|-------------|-------------|-----------|
| LF-DE-1 | 1               | OR          | RPTs (Goods)| 6000000   |
| LF-DE-1 | 2               | OR          | RPTs (Other)| 600000    |

**Same Rule ID** = related conditions
**Different Group numbers** = separate conditions
**Group Logic** = how to combine (OR/AND)

### **Complex Example:**

"MF required if (Group revenue >= 500M) AND (Employees > 250 OR Balance Sheet > 43M)"

| Rule ID | Group | Logic | Metric | Threshold |
|---------|-------|-------|--------|-----------|
| MF-X-1  | 1     | AND   | Revenue| 500000000 |
| MF-X-1  | 2     | OR    | Employees | 250   |
| MF-X-1  | 2     | OR    | Balance Sheet | 43000000 |

Group 1 (Revenue) must be TRUE **AND** Group 2 (Employees OR Balance Sheet) must be TRUE.

---

## Handling Missing Data

### **Use `?` for Unknown Values**

When you don't have data, enter `?` (question mark):

```
Local Revenue: ?
RPTs Goods: ?
```

### **System Response:**

The engine will:
1. ✅ Evaluate what it **can** with available data
2. ⚠️  Flag requirements as "LIKELY REQUIRED" when data is missing
3. 📋 Generate list of needed data

**Example:**

```
Master File: ✓ REQUIRED
  Reason: Group revenue (850M) > threshold (750M)
  → Can confirm with group-level data alone

Local File: ⚠️  LIKELY REQUIRED - VERIFICATION NEEDED
  Reason: Cannot evaluate - need local RPT data
  → Need more data to confirm

📋 DATA NEEDED:
  - Goods RPT amounts (to verify if > 6M threshold)
  - Other RPT amounts (to verify if > 600K threshold)
```

---

## Modifying Rules

### **Add a New Condition:**

To add "employees > 250" as an alternative MF trigger for Germany:

1. Open `Country_Rules_Library.xlsx`
2. Go to "MF Requirements" sheet
3. Add a new row:

```
Rule ID: MF-DE-1
Condition Group: 3
Group Logic: OR
Metric Type: Employees
Metric Scope: Local Entity
Threshold: 250
Currency: (blank)
Operator: >
Notes: Employee threshold for German MF
```

### **Add a New Country:**

1. Add rows to each sheet (MF, LF, CbCR, etc.)
2. Use country name consistently across all sheets
3. Follow the same Rule ID pattern: `MF-[COUNTRY]-1`

---

## Current Limitations

**Prototype Version 1.0:**
- ✅ Germany and Spain rules
- ✅ Multi-condition AND/OR logic
- ✅ Missing data handling
- ✅ Console output

**Not Yet Implemented:**
- ❌ HTML dashboard generation (coming next)
- ❌ Deadline calculations based on FYE
- ❌ Forms determination based on MF/LF requirements
- ❌ All 22+ countries
- ❌ Currency conversion
- ❌ PDF export

---

## Next Steps

### **After You Fill the Templates:**

1. **Review the assessment output**
   - Are requirements correct?
   - Do the data gaps make sense?

2. **Refine the rules** if needed
   - Add missing conditions
   - Adjust thresholds
   - Add notes for clarification

3. **Iterate on client data**
   - Gather missing data from client
   - Update Excel file
   - Re-run assessment

### **Phase 2: HTML Dashboard**

Once rules are validated, I'll build:
- HTML dashboard generator using these rules
- Country detail pages generated from rules
- Interactive highlighting (keep existing features)
- Data gap section with request list
- Timeline with calculated deadlines

---

## Example Workflow

```bash
# 1. Start with templates
python3 create_rules_template.py

# 2. Customize rules for your jurisdictions
open Country_Rules_Library.xlsx
# Edit MF/LF/CbCR thresholds

# 3. Create client file
cp Client_Data_Template.xlsx Acme_Corp_Data.xlsx

# 4. Fill in client data
open Acme_Corp_Data.xlsx
# Enter group revenue, entity data

# 5. Run assessment
python3 apply_rules.py Country_Rules_Library.xlsx Acme_Corp_Data.xlsx

# 6. Review output, identify data gaps

# 7. Get missing data from client, update file

# 8. Re-run assessment
python3 apply_rules.py Country_Rules_Library.xlsx Acme_Corp_Data.xlsx

# 9. Generate dashboard (Phase 2)
# python3 generate_dashboard_from_rules.py ... (coming soon)
```

---

## Support

**Questions about:**
- Rule structure → Check Instructions sheet in Country_Rules_Library.xlsx
- Client data format → Check Instructions sheet in Client_Data_Template.xlsx
- Logic engine → Read the assessment output carefully
- Adding countries → Follow the Germany/Spain examples

---

**Version:** 1.0 Prototype
**Last Updated:** 2025-10-23
**Scope:** Germany & Spain
**Status:** Ready for testing
