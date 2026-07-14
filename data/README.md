# Data Description

The dataset used in this project is proprietary and cannot be shared publicly.

Below are sample structures of each dataset to help understand the schema.

---

## 1. CP Results (`cp_results.xlsx`)

Main dataset containing manufacturing batch data, defect counts, and yield (Okper).

### Sample Data

| Art | Code | BatchNo | wCPg | OkQty | Okper | GDper | RCDper | SFInDate | PackedDate |
|-----|------|--------|------|-------|-------|-------|--------|----------|------------|
| A.XXXX.MM10.0 | 650 | B001 | 143.676 | 10600 | 46.63 | 19.71 | 33.66 | 16/01/2023 | 12/01/2024 |
| A.XXXX.MM10.0 | 815 | B002 | 143.679 | 10500 | 52.28 | 16.37 | 31.35 | 10/02/2023 | 09/01/2024 |
| A.XXXX.MM6.0 | 296 | B003 | 30.76 | 47002 | 85.69 | 4.41 | 9.90 | 28/02/2023 | 02/01/2024 |
| A.XXXX.MM8.0 | 969 | B004 | 73.368 | 14751 | 54.26 | 17.24 | 28.50 | 10/06/2023 | 28/01/2024 |
| A.XXXX.MM8.0 | 650 | B005 | 73.368 | 19000 | 71.09 | 11.62 | 17.29 | 12/07/2023 | 15/01/2024 |

---

**Note:**

- The dataset contains a large number of features (70+ columns including defect metrics and process variables)
- Only a subset is shown here for illustration.

---

## 2. Data Dictionary (`Swarovski_dictionary.xlsx`)

This Excel file contains multiple sheets providing metadata and lookup tables used in the project.

---

### Sheet 1: Description

Contains high-level descriptions of dataset columns and feature groups.

| Feature Type | Description |
|-------------|------------|
| Product & Batch Info | Product identifiers, batch numbers, and tracking details |
| Weight & Quantity Metrics | Measurements related to bead weight and counts |
| Date Features | Production and packaging timestamps |
| Defect Features | Defect percentages across different manufacturing stages |
| Derived Metrics | Yield, defect ratios, and efficiency-related features |

---

### Sheet 2: Colour Codes

Mapping of colour codes to colour categories used in production.

| Color Code | Color |
|-----------|------|
| C101 | Color_A |
| C102 | Color_B |
| C103 | Color_C |
| C104 | Color_D |
| C105 | Color_E |

---

### Sheet 3: Product Codes

Mapping of product codes to product categories.

| Code | Product |
|------|--------|
| P101 | Type_A |
| P102 | Type_B |
| P103 | Type_C |
| P104 | Type_D |
| P105 | Type_E |

---

**Note:**

- The original Excel file contains detailed mappings and descriptions.
- Values have been anonymized for confidentiality.

---

## Final Note

- These samples are illustrative and do not represent actual production values.
- The original datasets must be placed inside the `data/` directory to execute the notebook.
