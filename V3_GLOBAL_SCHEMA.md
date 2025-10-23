# Country Rules Library v3.0 - Global Unified Schema

## Executive Summary

Version 3.0 represents a **complete redesign** with a unified global schema that supports every major TP compliance model worldwide, including edge cases that previous versions couldn't handle.

**Key Achievement:** One schema handles Germany (extraordinary transactions), Belgium (dual filing), US/Canada (penalty protection), Malaysia/Singapore (integrated), France (one-time notifications), and all standard regimes.

---

## What's New in v3.0

### 1. **Global Unified Schema** ⭐ MAJOR

**Before:** Each sheet had slightly different structures

**Now:** 18 common fields across ALL sheets (MF, LF, CbCR, TP Forms)

**Benefit:** Consistent automation, reporting, and data quality

---

### 2. **PENALTY PROTECTION ONLY Field** ⭐ NEW

**Purpose:** Captures US/Canada voluntary TP documentation regimes

**Column:** Added to MF and LF sheets

**Values:** Yes / No

**Example - United States:**
```
Country: United States
Applicability: Conditional
Penalty Protection Only: Yes
Rule Notes: Voluntary MF preparation for penalty protection under IRC §6662.
            No filing requirement.
Deadline Notes: Contemporaneous documentation provides reasonable cause defense
```

**Example - Canada:**
```
Country: Canada
Applicability: Conditional
Penalty Protection Only: Yes
Rule Notes: Voluntary MF for penalty protection.
            No statutory filing requirement.
Deadline Notes: Contemporaneous documentation required for TP adjustment defense
```

---

### 3. **SPECIAL DEADLINE CONDITION Field** ⭐ NEW

**Purpose:** Handles event-triggered or exceptional deadlines

**Column:** Added to MF and LF sheets

**Use Cases:**
- Germany extraordinary transactions (6-month rule)
- Event-driven filings
- Conditional timelines

**Example - Germany Extraordinary Transactions:**
```
Country: Germany
Special Deadline Condition: Extraordinary RPTs → full TPD due within 6 months after FYE
Prep Date Rule: FYE-Based
Prep Date Details: Within 6 months of FYE for extraordinary transactions
Rule Notes: Germany-specific extraordinary transaction rule
```

---

### 4. **CbCR Notifications Sheet** ⭐ REDESIGNED

**Old Name:** "CbCR Requirements"

**New Name:** "CbCR Notifications"

**Focus Changed:** From CbCR report requirements → Notification rules (who files, how often, where)

**New Columns:**
- Notification Frequency (Annual, One-Time, Upon Change)
- Filer Type (UPE, Local CE, One CE for All, Other)
- Joint Filing Allowed? (Yes, No, Not Specified)
- Included in CIT Return? (Yes, No)
- Submission Channel (Within CIT Return, Separate Form, Portal, etc.)
- Notification Validity (How long valid)
- Linked To (CbCR, Standalone)

**Rationale:** CbCR reports are standardized (OECD schema); notifications vary widely by jurisdiction.

**Examples:**

**Belgium - Annual Separate Form:**
```
Notification Frequency: Annual
Filer Type: Local CE
Joint Filing Allowed?: No
Included in CIT Return?: No
Submission Channel: Separate Form
Form Name: Form 275.CBC.NOT
Submission Date Rule: Fixed
Submission Date Details: By 31 Dec following FY
```

**France - One-Time Until Change:**
```
Notification Frequency: Upon Change
Filer Type: UPE
Submission Channel: Portal
Form Name: DAS2-CbCR
Submission Date Details: Within 3 months of change
Notification Validity: Until entity or UPE info changes
Notes: One-time notification valid until circumstances change
```

**UK - In CIT Return:**
```
Notification Frequency: Upon Change
Included in CIT Return?: Yes
Submission Channel: Within CIT Return
Submission Date Details: Within CIT return filing
Notes: Notification included in CIT return; updated when filing entity changes
```

---

### 5. **Enhanced TP Forms Sheet** ⭐ IMPROVED

**New Columns:**
- FORM TRIGGER (When form is required)
- LINKED TO (Which document it relates to)
- Electronic Signature Required?
- Timestamp Required?

**FORM TRIGGER Values:**
- Always
- If MF Required
- If LF Required
- If MF or LF Required
- If CbCR Required
- Other

**LINKED TO Values:**
- MF
- LF
- CbCR
- Standalone

**Validation Logic:**
```
IF FORM TYPE = "MF Summary" → LINKED TO must = "MF"
IF FORM TYPE = "LF Summary" → LINKED TO must = "LF"
IF FORM TYPE = "CbCR Notification" → LINKED TO must = "CbCR"
```

**Examples:**

**Belgium Form 275.MF:**
```
Form Type: MF Summary
Form Trigger: If MF Required
Linked To: MF
What It Contains: Summary form with key MF data points
E-Signature Required?: Yes
Notes: Separate summary form filed alongside full MF report
```

**Italy RS 106:**
```
Form Type: TP Disclosure
Form Trigger: If MF or LF Required
Linked To: Standalone
E-Signature Required?: Yes
Timestamp Required?: Electronic Timestamp
Notes: MF/LF must be electronically timestamped before filing RS 106
```

---

### 6. **Data Dictionary Tab** ⭐ NEW

**Position:** First sheet in workbook

**Contains:**
1. **Global Dropdown Values**
   - All allowed values for every dropdown
   - Notes and examples
   - Which sheets use each field

2. **Validation & Integrity Rules**
   - Automatic rules (enforced by Excel)
   - Manual checks (user responsibility)
   - Examples for each rule

**Benefits:**
- Single source of truth for all validations
- Quick reference for allowed values
- Easy onboarding for new users

---

## Global Fields (18 Common Fields)

These fields appear consistently across MF, LF, and where applicable, CbCR Notifications:

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | COUNTRY | Text | Jurisdiction name |
| 2 | APPLICABILITY | Dropdown | Always, Conditional, Integrated, Notification Only, Never Required, N/A |
| 3 | RULE ID | Text | Unique identifier (e.g., MF-DE-1) |
| 4 | CONDITION GROUP | Integer | 1, 2, 3... for multi-conditions |
| 5 | GROUP LOGIC | Dropdown | AND, OR |
| 6 | METRIC TYPE | Dropdown | Revenue, Employees, RPTs, etc. |
| 7 | METRIC SCOPE | Dropdown | Group, Local Entity, Transaction |
| 8 | THRESHOLD VALUE | Number | Numeric threshold |
| 9 | CURRENCY | Text | EUR, USD, MYR, etc. |
| 10 | OPERATOR | Dropdown | >=, >, =, <, <= |
| 11 | PREP DATE RULE | Dropdown | None, CIT Date, FYE-Based, Fixed, etc. |
| 12 | PREP DATE DETAILS | Text | Specifics |
| 13 | SUBMISSION DATE RULE | Dropdown | None, CIT Date, FYE-Based, Fixed, etc. |
| 14 | SUBMISSION DATE DETAILS | Text | Specifics |
| 15 | UPON REQUEST DAYS | Number | Days if upon request |
| 16 | EFFECTIVE FROM (FY) | Text | When rule took effect |
| 17 | RULE NOTES | Text | Context for thresholds |
| 18 | DEADLINE NOTES | Text | Context for deadlines |

**Sheet-Specific Additions:**

**MF/LF Sheets Add:**
- INTEGRATED_WITH (Local File, TP Form, Other)
- SUBMISSION CHANNEL (e-portal, form, etc.)
- SPECIAL DEADLINE CONDITION (event-based rules)
- PENALTY PROTECTION ONLY (Yes, No)

**CbCR Notifications Add:**
- NOTIFICATION FREQUENCY
- FILER TYPE
- JOINT FILING ALLOWED?
- INCLUDED IN CIT RETURN?
- NOTIFICATION VALIDITY

**TP Forms Add:**
- FORM TYPE
- FORM TRIGGER
- LINKED TO
- ELECTRONIC SIGNATURE REQUIRED?
- TIMESTAMP REQUIRED?

---

## Special Cases - How to Handle

### Case 1: Germany Extraordinary Transactions

**Requirement:** Separate 6-month deadline for extraordinary RPTs

**Implementation:**
```
Sheet: MF Requirements (or LF Requirements)

Row 1: Standard MF requirement
  Country: Germany
  Applicability: Conditional
  Rule ID: MF-DE-1
  Threshold: 750M EUR
  Special Deadline Condition: (blank)

Row 2: Extraordinary transaction rule
  Country: Germany
  Applicability: Conditional
  Rule ID: MF-DE-2
  Metric Type: Always
  Metric Scope: Local Entity
  Special Deadline Condition: Extraordinary RPTs → full TPD due within 6 months after FYE
  Prep Date Rule: FYE-Based
  Prep Date Details: Within 6 months of FYE for extraordinary transactions
  Notes: Germany-specific extraordinary transaction rule
```

---

### Case 2: Belgium Dual Filing (Full Reports + Summary Forms)

**Requirement:** Full MF report + Form 275.MF summary

**Implementation:**
```
Sheet: MF Requirements
  Country: Belgium
  Applicability: Conditional
  Rule ID: MF-BE-1
  Threshold: 750M EUR
  Submission Channel: e-filing portal
  Notes: Full Master File report

Sheet: TP Forms
  Country: Belgium
  Form Name: Form 275.MF
  Form Type: MF Summary
  Form Trigger: If MF Required
  Linked To: MF
  What It Contains: Summary form with key MF data points
  Submission Date Rule: Fixed
  Submission Date Details: 31 Dec following FY
  E-Signature Required?: Yes
  Notes: Separate summary form filed alongside full MF report
```

**Result:** Both requirements tracked, relationship clear via LINKED TO field

---

### Case 3: US/Canada Penalty Protection

**Requirement:** Voluntary TP documentation for penalty protection (not mandatory filing)

**Implementation:**
```
Sheet: MF Requirements

United States:
  Country: United States
  Applicability: Conditional
  Penalty Protection Only: Yes
  Prep Date Rule: None
  Prep Date Details: Voluntary preparation recommended
  Submission Date Rule: None
  Submission Date Details: N/A - voluntary
  Rule Notes: Voluntary MF preparation for penalty protection under IRC §6662.
              No filing requirement.
  Deadline Notes: Contemporaneous documentation provides reasonable cause defense

Canada:
  Country: Canada
  Applicability: Conditional
  Penalty Protection Only: Yes
  Prep Date Rule: None
  Prep Date Details: Voluntary preparation recommended
  Submission Date Rule: None
  Submission Date Details: N/A - voluntary
  Rule Notes: Voluntary MF for penalty protection.
              No statutory filing requirement.
  Deadline Notes: Contemporaneous documentation required for TP adjustment defense
```

**Key:** PENALTY PROTECTION ONLY = Yes flags these as voluntary regimes

---

### Case 4: CbCR One-Time / Joint Filings

**Requirement:** France one-time notification, Belgium joint filing

**Implementation:**
```
Sheet: CbCR Notifications

France:
  Notification Frequency: Upon Change
  Filer Type: UPE
  Submission Channel: Portal
  Notification Validity: Until entity or UPE info changes
  Notes: One-time notification valid until circumstances change (UPE change, threshold, etc.)

Germany:
  Notification Frequency: Annual
  Filer Type: One CE for All
  Joint Filing Allowed?: Yes
  Notes: One German group entity can file notification for all German entities
```

---

## Validation & Integrity Rules

### Automatic (Excel-Enforced)

1. **Applicability Dropdown**
   - Values: Always, Conditional, Integrated, Notification Only, Never Required, N/A
   - Cannot be blank

2. **Numeric Validation**
   - UPON REQUEST DAYS must be > 0

3. **Dropdown Consistency**
   - GROUP LOGIC: AND, OR
   - OPERATOR: >=, >, =, <, <=
   - All date rules: standardized 6 values

### Manual (User Responsibility)

1. **Integrated Applicability**
   ```
   IF APPLICABILITY = "Integrated"
   THEN INTEGRATED_WITH must not be blank
   ```

2. **Upon Request Days**
   ```
   IF SUBMISSION DATE RULE = "Upon Request"
   THEN UPON REQUEST DAYS should be numeric
   ```

3. **Multi-Condition Rules**
   ```
   Related conditions must use:
   - Same RULE ID
   - Incrementing CONDITION GROUP (1, 2, 3...)
   - Consistent GROUP LOGIC
   ```

4. **CbCR In CIT**
   ```
   IF INCLUDED IN CIT RETURN = "Yes"
   THEN SUBMISSION CHANNEL = "Within CIT Return"
   ```

5. **Form Type Linking**
   ```
   IF FORM TYPE = "MF Summary"
   THEN LINKED TO = "MF"
   ```

6. **Penalty Protection**
   ```
   IF PENALTY PROTECTION ONLY = "Yes"
   THEN RULE NOTES must explain voluntary nature
   ```

---

## Migration from v2.1 to v3.0

### Step 1: Understand Major Changes

1. **CbCR Requirements** → renamed to **CbCR Notifications**
   - Focus changed from report to notification
   - New columns: Notification Frequency, Filer Type, etc.

2. **New MF/LF Columns:**
   - SPECIAL DEADLINE CONDITION
   - PENALTY PROTECTION ONLY

3. **Enhanced TP Forms:**
   - FORM TRIGGER
   - LINKED TO
   - E-SIGNATURE REQUIRED?
   - TIMESTAMP REQUIRED?

### Step 2: Data Migration

**For MF/LF:**
- Add SPECIAL DEADLINE CONDITION column (usually blank)
- Add PENALTY PROTECTION ONLY column (usually "No")
- For US/Canada: Set PENALTY PROTECTION ONLY = "Yes"
- For Germany extraordinary: Fill SPECIAL DEADLINE CONDITION

**For CbCR:**
- Rename sheet to "CbCR Notifications"
- Restructure using new columns
- Focus on notification rules, not report requirements

**For TP Forms:**
- Add FORM TRIGGER column
- Add LINKED TO column
- Add E-SIGNATURE and TIMESTAMP columns
- Link forms to MF/LF/CbCR using LINKED TO

### Step 3: Validate

- Check Data Dictionary for dropdown values
- Verify integrity rules are met
- Test with sample client data

---

## Examples in v3.0 Template

### MF Requirements Sheet

1. **Germany** - Standard conditional + Extraordinary transactions
2. **Malaysia** - Integrated with Local File
3. **United States** - Penalty protection only
4. **Canada** - Penalty protection only

### CbCR Notifications Sheet

1. **Belgium** - Annual separate form
2. **France** - One-time until change
3. **UK** - In CIT return
4. **Germany** - Joint filing allowed

### TP Forms Sheet

1. **Belgium Form 275.MF** - MF Summary
2. **Belgium Form 275.LF** - LF Summary
3. **Spain Form 232** - TP Return
4. **Italy RS 106** - TP Disclosure with timestamp
5. **Germany Transaction Matrix** - Always required

---

## Benefits of v3.0

| Benefit | Impact |
|---------|--------|
| **Global Unified Schema** | Consistent automation across all compliance types |
| **Handles All Edge Cases** | Germany extraordinary, US/Canada penalty protection, Belgium dual filing |
| **CbCR Clarity** | Notification vs. report clearly separated |
| **Form Relationships** | Clear linkage via LINKED TO field |
| **Data Dictionary** | Single source of truth for validations |
| **Future-Proof** | Extensible for new jurisdictions and requirements |
| **Quality Assurance** | Built-in validation prevents errors |

---

## File Structure

```
Country_Rules_Library_v3.0.xlsx
├── Data Dictionary (Sheet 1)
│   ├── Global Dropdown Values
│   └── Validation & Integrity Rules
├── MF Requirements (Sheet 2)
│   └── 22 columns (18 global + 4 specific)
├── LF Requirements (Sheet 3)
│   └── 22 columns (18 global + 4 specific)
├── CbCR Notifications (Sheet 4)
│   └── 14 columns (notification-focused)
└── TP Forms (Sheet 5)
    └── 13 columns (enhanced with triggers and links)
```

---

## Next Steps

1. **Open template:** `Country_Rules_Library_v3.0.xlsx`
2. **Review Data Dictionary:** First sheet - comprehensive guide
3. **Check examples:** All sheets have real-world examples
4. **Fill your data:** Add countries using unified schema
5. **Validate:** Use Data Dictionary to ensure quality
6. **Test:** Run with client data

---

## Version History

**v3.0** (2025-10-23) - Global Unified Schema:
- 18 common fields across all sheets
- PENALTY PROTECTION ONLY (US/Canada)
- SPECIAL DEADLINE CONDITION (Germany extraordinary)
- CbCR Notifications redesigned
- Enhanced TP Forms (FORM TRIGGER, LINKED TO)
- Data Dictionary tab
- Examples: Germany, Belgium, US, Canada, Malaysia, France, UK

**v2.1** (2025-10-23):
- Integrated applicability
- INTEGRATED_WITH column
- EFFECTIVE FROM (FY)
- SUBMISSION CHANNEL
- Data validation

**v2.0** (2025-10-23):
- Combined rules and deadlines
- Three deadline types
- Separate TP Forms sheet

**v1.0** (2025-10-23):
- Initial rule-based system

---

**Status:** Production Ready - Global Compliance
**Coverage:** All major TP compliance models worldwide
**Quality:** Enterprise-grade with comprehensive validation
