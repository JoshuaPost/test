# TP Compliance Dashboard Generator

A reusable tool to generate Transfer Pricing (TP) Compliance Dashboards from Excel data files.

## Overview

This tool allows you to:
- **Upload** an Excel file with country TP requirements
- **Generate** a fully interactive HTML dashboard
- **Add** new countries by simply adding rows to Excel
- **Edit** existing country data by updating Excel cells
- **Reuse** the same template for multiple clients

## Quick Start

### Step 1: Prepare Your Data

Use the provided Excel template to enter your data:

```bash
# Start with the empty template
TP_Dashboard_Template.xlsx

# Or use the Meiko example
Meiko_TP_Data.xlsx
```

### Step 2: Generate Dashboard

```bash
python3 generate_dashboard.py Meiko_TP_Data.xlsx output_dashboard.html
```

### Step 3: Open Dashboard

Open `output_dashboard.html` in your web browser.

## File Structure

```
project/
├── generate_dashboard.py           # Main generator script
├── extract_meiko_data.py          # Script to populate template with Meiko data
├── TP_Dashboard_Template.xlsx     # Empty template (use this for new clients)
├── Meiko_TP_Data.xlsx             # Example filled with Meiko data
├── Meiko.html                     # Current Meiko dashboard (reference)
└── README_Dashboard_Generator.md  # This file
```

## Excel Template Structure

### Sheet 1: Client Info

| Field               | Value            |
|---------------------|------------------|
| Client Name         | Meiko Group      |
| Fiscal Year End Date| 2025-12-31       |
| Fiscal Year Label   | FYE 2025         |

### Sheet 2: Countries

Each row represents one jurisdiction. Columns:

1. **Country Name** - Full name (e.g., "Germany")
2. **Country ID** - Lowercase ID (e.g., "germany" or "hong-kong")
3. **Region** - One of: Europe, Americas, Asia-Pacific, Middle East
4. **Entity Name** - Your company entity in that country
5. **Master File** - Y or N
6. **Local File** - Y or N
7. **Mandatory Forms** - Y or N
8. **Thresholds** - List separated by ` | `
9. **Documentation Approach** - List separated by ` | `
10. **Forms and Disclosures** - List separated by ` | `
11. **Filing Status** - Short status description
12. **Deadlines** - List separated by ` | `

**Example row:**
```
Germany | germany | Europe | Acme GmbH | Y | Y | N | Threshold 1 | Threshold 2 | Doc 1 | Doc 2 | Form 1 | Form 2 | Filing status text | Deadline 1 | Deadline 2
```

### Sheet 3: Timeline

Each row represents one deadline/event. Columns:

1. **Quarter** - "December 2025", "Q1 2026", "Q2 2026", etc.
2. **Country** - Must match country name from Countries sheet
3. **Date** - YYYY-MM-DD format (or leave blank)
4. **Description** - What needs to be done
5. **Type** - filing / preparation / upon-request

**Example row:**
```
Q2 2026 (April - June) | Germany | 2026-06-30 | Extraordinary transaction documentation due | filing
```

## Adding a New Country

1. Open your Excel file (e.g., `Meiko_TP_Data.xlsx`)
2. Go to the "Countries" sheet
3. Add a new row with the country data
4. Go to the "Timeline" sheet
5. Add deadline rows for that country
6. Save the Excel file
7. Run the generator:
   ```bash
   python3 generate_dashboard.py Meiko_TP_Data.xlsx output.html
   ```

## Editing Existing Data

1. Open your Excel file
2. Find the row for the country you want to edit
3. Update the cells
4. Save the file
5. Regenerate the dashboard:
   ```bash
   python3 generate_dashboard.py Meiko_TP_Data.xlsx output.html
   ```

## Using for Multiple Clients

### Option 1: Separate Files
```
clients/
├── client-a-data.xlsx
├── client-b-data.xlsx
└── client-c-data.xlsx

# Generate dashboards
python3 generate_dashboard.py clients/client-a-data.xlsx dashboards/client-a.html
python3 generate_dashboard.py clients/client-b-data.xlsx dashboards/client-b.html
python3 generate_dashboard.py clients/client-c-data.xlsx dashboards/client-c.html
```

### Option 2: Batch Generation Script
Create a script to generate all client dashboards:

```bash
#!/bin/bash
for client in clients/*.xlsx; do
    name=$(basename "$client" .xlsx)
    python3 generate_dashboard.py "$client" "dashboards/${name}.html"
done
```

## Field Formatting Rules

### Multi-Line Fields

Use the pipe character `|` to separate items:

```
Threshold 1 | Threshold 2 | Threshold 3
```

This will render as:
- Threshold 1
- Threshold 2
- Threshold 3

### Date Format

Always use `YYYY-MM-DD`:
- ✅ 2026-06-30
- ❌ 06/30/2026
- ❌ 30-Jun-2026

### Country ID Rules

- Lowercase only
- No spaces (use hyphens)
- Examples:
  - United States → `us` or `united-states`
  - Hong Kong → `hongkong` or `hong-kong`
  - United Arab Emirates → `uae` or `united-arab-emirates`

### Region Values

Must be exactly one of:
- Europe
- Americas
- Asia-Pacific
- Middle East

### Boolean Fields (Y/N)

For Master File, Local File, Mandatory Forms:
- Use `Y` for Yes
- Use `N` for No
- Case insensitive (y, Y, yes, YES all work)

## Tips & Best Practices

1. **Keep Data Consistent**
   - Use the same country names in both Countries and Timeline sheets
   - Use consistent date formats
   - Use consistent region names

2. **Don't Delete Headers**
   - Row 1 contains column headers - don't delete
   - You can delete row 2 (instructions) if you want

3. **Backup Your Data**
   - Keep copies of your Excel files
   - Version control with git is recommended

4. **Test After Changes**
   - Regenerate the dashboard after making changes
   - Open in browser to verify everything looks correct

5. **Add Countries Gradually**
   - Start with a few countries
   - Test the generation
   - Add more countries incrementally

## Troubleshooting

### Dashboard Not Generating

**Error:** "Excel file not found"
- Check the file path is correct
- Use absolute or relative path correctly

**Error:** "Sheet not found"
- Ensure sheets are named exactly: "Client Info", "Countries", "Timeline"
- Don't rename the sheets

### Countries Not Showing

- Check that Country ID is unique and lowercase
- Verify Region is one of the four valid values
- Ensure all required columns have data

### Timeline Items Missing

- Verify Country name matches exactly with Countries sheet
- Check date format is YYYY-MM-DD
- Ensure Quarter format matches examples

### Special Characters Issues

- Use plain text, avoid special formatting
- The pipe character `|` is reserved for separating items
- If you need a pipe in text, use HTML entity `&#124;`

## Current Limitations

The generator currently has these limitations:

1. **Partial HTML Generation**
   - The current version updates statistics and client name
   - Full HTML template generation is in development
   - For now, it modifies the Meiko.html template

2. **Manual Region Grid**
   - Regional entity cards require manual arrangement
   - Future versions will auto-generate from data

3. **Timeline Grouping**
   - Timeline quarters must be manually grouped
   - Future versions will auto-group by date

## Roadmap

### Version 1.0 (Current)
- ✅ Excel template creation
- ✅ Data extraction
- ⚠️ Basic HTML generation (partial)

### Version 2.0 (Planned)
- Complete HTML generation from scratch
- Auto-generate regional grids
- Auto-group timeline by quarters
- Data validation and error checking
- PDF export capability

### Version 3.0 (Future)
- Web interface for data entry
- Database backend
- Multi-user support
- Real-time collaboration

## Support

For questions or issues:
1. Check this README
2. Review the Excel template instructions
3. Examine the Meiko_TP_Data.xlsx example
4. Contact the development team

## License

Internal tool for transfer pricing compliance management.

---

**Last Updated:** 2025-10-22
**Version:** 1.0
**Author:** Transfer Pricing Team
