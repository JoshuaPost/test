# Country Rules Library v2.0 - Improvements

## What Changed from v1.0

### **Problem 1: Deadlines Separated from Rules**
**v1.0:** Rules on MF sheet, deadlines on separate Deadlines sheet
**v2.0:** ✅ Rules AND deadlines on SAME sheet - complete picture in one place

### **Problem 2: No Way to Mark "Never Required"**
**v1.0:** Could only mark conditional requirements
**v2.0:** ✅ Added "Applicability" field with options:
- Always
- Conditional
- **Never Required** (e.g., Malaysia MF)
- N/A

### **Problem 3: Only One Deadline Field**
**v1.0:** Single deadline column
**v2.0:** ✅ THREE deadline fields:
- **Prep Date Rule** - Suggested preparation date (often CIT-based)
- **Submission Date Rule** - Hard deadline if exists
- **Upon Request Days** - Days to submit if requested

### **Problem 4: No Distinction Between Forms and Reports**
**v1.0:** Forms mixed with full documentation
**v2.0:** ✅ Separate "TP Forms" sheet
- Forms (Belgium 275.MF) vs. Full Reports (Master File)
- Tracks e-signature and timestamp requirements

---

## New Column Structure

### MF/LF/CbCR Sheets

| Section | Columns | Purpose |
|---------|---------|---------|
| **Basic** | Country, Applicability | ID and whether required |
| **Threshold Rules** | Rule ID, Condition Group, Logic, Metric, Scope, Threshold, Currency, Operator | WHEN it's required |
| **Deadlines** | Prep Date Rule, Prep Details, Submission Rule, Submission Details, Upon Request Days | WHEN to prepare/submit |
| **Notes** | Rule Notes, Deadline Notes | Context |

---

## Deadline Patterns

### Pattern 1: Upon Request Only
**Example:** Germany MF/LF

```
Prep Date Rule: None
Submission Date Rule: Upon Request
Submission Date Details: Within 30 days of audit notice
Upon Request Days: 30
```

**Meaning:** No suggested prep date, only submit when requested, 30-day window

---

### Pattern 2: CIT-Based Prep + Upon Request
**Example:** Spain MF/LF

```
Prep Date Rule: CIT Date
Prep Date Details: Prepare by CIT filing (approx 25 Jul)
Submission Date Rule: Upon Request
Submission Date Details: Within 10 days if audit
Upon Request Days: 10
```

**Meaning:** Must be ready by CIT date (Spain has 10-day audit response), submit only if requested

---

### Pattern 3: Fixed Submission Deadline
**Example:** Spain Form 232

```
Prep Date Rule: CIT Date
Submission Date Rule: Fixed
Submission Date Details: Approx 25 Aug 2026
Upon Request Days: (blank)
```

**Meaning:** Prepare by CIT, MUST submit by Aug 25 every year

---

### Pattern 4: Electronic Timestamp Required
**Example:** Italy MF/LF

```
Submission Date Rule: With Tax Return
Submission Date Details: Expected 31 Oct 2026
Notes: Must electronically timestamp MF/LF before filing RS 106
```

**Meaning:** Must timestamp documentation before tax filing

---

## TP Forms Sheet Structure

Tracks forms that are SEPARATE from full MF/LF reports:

| Column | Purpose | Example |
|--------|---------|---------|
| Form Type | Category | MF Summary, TP Return, Disclosure |
| Form Name | Official name | Form 275.MF, Form 232 |
| Form Triggers | When required | If MF Required, Always |
| What It Contains | Summary vs. full | Summary with MF data points |
| E-Signature? | Required? | Yes / No |
| Timestamp? | Required? | Yes / No / Electronic |

**Belgium Example:**
- Full Master File Report (100 pages) - full documentation
- Form 275.MF (5 pages) - summary form WITH MF data points
- Both required, form is separate filing

---

## Applicability Field Usage

### "Always"
Requirement always applies (rare for MF/LF)
```
Country: Germany
Requirement: Transaction Matrix
Applicability: Always
```

### "Conditional"
Most common - required if thresholds met
```
Country: Germany
Requirement: Master File
Applicability: Conditional
Rule: Revenue >= 750M EUR OR Local Sales >= 100M EUR
```

### "Never Required"
Country doesn't have this requirement
```
Country: Malaysia
Requirement: Master File (standalone)
Applicability: Never Required
Notes: MF content integrated into Local File (CTPD)
```

### "N/A"
Not applicable
```
Country: United States
Requirement: CbCR (some scenarios)
Applicability: N/A
```

---

## Migration from v1.0 to v2.0

If you already filled v1.0:

**Step 1:** Review your v1.0 data

**Step 2:** For each country in MF sheet:
- Copy threshold rules (same structure)
- Add "Applicability" column value
- Look up deadlines from old Deadlines sheet
- Add to new deadline columns

**Step 3:** Check TP Forms sheet:
- Identify forms that are separate from full reports
- Add rows for each form

**Step 4:** Validate:
- Each row should have complete picture (rules + deadlines)
- "Never Required" entries should have blank threshold fields
- Forms should be in TP Forms sheet, not MF/LF sheets

---

## Quick Reference

### Field Values Reference

**Applicability:**
- Always
- Conditional
- Never Required
- N/A

**Prep Date Rule:**
- None
- CIT Date
- Fixed
- FYE-Based

**Submission Date Rule:**
- None
- Upon Request
- Fixed
- FYE-Based
- With Tax Return

**Form Type:**
- TP Return
- TP Disclosure
- MF Summary
- LF Summary
- Notification
- CbCR Filing

---

## Benefits of v2.0

✅ **Single source of truth** - All info for Germany MF on one row
✅ **Better deadline tracking** - Prep vs. Submission vs. Upon Request
✅ **Clearer applicability** - Can mark "Never Required" explicitly
✅ **Forms separated** - Distinguish Belgium Form 275.MF from full MF report
✅ **E-signature/timestamp** - Track compliance requirements
✅ **Easier to maintain** - No jumping between sheets

---

## Next Steps

1. **Review the template:** Open `Country_Rules_Library_v2.xlsx`
2. **Check the examples:** Germany and Spain are pre-filled
3. **Fill in your data:** Add more countries using the same pattern
4. **Test with client data:** Use existing `Client_Data_Template.xlsx`
5. **Run assessment:** `python apply_rules.py Country_Rules_Library_v2.xlsx Client_Data.xlsx`

---

**Version:** 2.0
**Status:** Ready for use
**Scope:** Germany & Spain examples included
