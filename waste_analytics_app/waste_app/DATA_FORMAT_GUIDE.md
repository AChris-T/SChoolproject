# Data Format Guide

This guide explains the expected format for uploading data to the Waste Analytics system.

## Sample Data Files

Two sample CSV files are provided for testing:
- **audit_data_sample.csv** - Physical waste audit measurements
- **survey_data_sample.csv** - Student survey responses

You can use these as templates to format your own data.

---

## Audit Data Format (`audit_data.csv`)

### Required Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `hall` | text | Hostel/Hall name | Awo, Tedder, Independence |
| `floor_block` | text | Floor or block designation | Floor 1, Block C |
| `date` | date | Date of audit (YYYY-MM-DD format) | 2025-05-01 |
| `day_number` | int | Day of week (1–7) | 1-7 |
| `biodegradable_kg` | float | Weight of organic/food waste | 3.42 |
| `non_biodegradable_kg` | float | Weight of plastics/packaging | 4.95 |
| `recyclable_kg` | float | Weight of recyclable materials | 1.15 |
| `hazardous_kg` | float | Weight of hazardous items | 0.02 |
| `population` | int | Number of students on floor/block | 160 |

### Sample Audit Data Row
```
Independence,Block C,2025-05-01,1,3.42,4.95,1.15,0.02,160
```

---

## Survey Data Format (`survey_data.csv`)

### Required Columns

| Column | Type | Description | Valid Values |
|--------|------|-------------|--------------|
| `respondent_id` | int | Unique respondent ID | 1, 2, 3… |
| `hall` | text | Hostel name | Awo, Tedder, Independence |
| `level` | int | Academic year level | 100, 200, 300, 400, 500 |
| `meals_per_day` | int | Meals consumed in hostel daily | 1, 2, 3 |
| `packaged_food_frequency` | int | How often packaged food is consumed | 0=Never, 1=Occasionally, 2=Often |
| `disposal_frequency_per_week` | int | How many times waste is disposed | 1–7 |
| `recycling_awareness` | int | Recycling awareness level | 1–5 (1=Low, 5=High) |
| `visitor_effect` | int | Do visitors increase waste? | 0=No, 1=Yes |
| `separation_behaviour` | int | Waste separation frequency | 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Always |
| `waste_scale` | int | Self-reported waste generation | 1=Small, 2=Medium, 3=Large |

### Sample Survey Data Row
```
1,Independence,100,2,1,4,3,0,1,1
```

---

## Important Notes

1. **Date Format**: Always use YYYY-MM-DD format (e.g., 2025-05-01)
2. **Decimal Values**: Use decimal points (.) not commas for numbers
3. **Missing Values**: Regression analysis requires at least 8 complete survey rows
4. **Per-Capita Calculation**: Based on `population` and `day_number` fields
5. **File Formats**: Accepted formats are CSV (.csv) or Excel (.xlsx)

---

## How to Upload

1. Go to the sidebar → **📂 Load Data**
2. Click "Audit CSV / Excel" and select your audit_data.csv file
3. Click "Survey CSV / Excel" and select your survey_data.csv file
4. Navigate through the pages to explore your data

---

## Regression Model Requirements

The "Survey & Regression" page requires:
- Minimum **8 complete survey records** (all 10 columns filled)
- No missing values in the required columns
- Proper numeric formatting for all numeric fields
