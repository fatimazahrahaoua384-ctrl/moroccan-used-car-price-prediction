# Research notes

## A. Dataset: MUCars-2024
- Source: https://doi.org/10.17632/vjrbcb2rrt.2
- License: CC BY 4.0
- File: cars_dataframe.csv (21.8 MB)
- Rows / columns: (à compléter)
- Collection method: (à compléter)

## B. First look at the data 

Notebook: `notebooks/01_first_look.ipynb` (2026-11-22)

**Overview:** 101,896 rows × 15 columns, one CSV file (21.8 MB). No listing date column.

### Missing values
| Column | % missing |
|---|---|
| Price (target) | 25.0 |
| First Owner | 14.4 |
| Origin | 11.8 |
| Number of Doors | 11.2 |
| Condition | 3.5 |
| Fiscal Power | 0.3 |
| Sector | 0.2 |
| All others | 0.0 |

### Issues found
1. **Target missing for 25% of rows** (25,483 listings). They cannot be used to train a supervised model. Plan: remove them from training, never impute the target.
2. **Price has extreme values.** min = 1, median = 110,000, mean ≈ 498,000, max = 1.6 billion. The mean is driven by outliers, so the median is the reliable reference. Values like 1 or 1.6e9 look like errors or placeholders (hypothesis, to check).
3. **2,805 fully duplicated rows (~2.8%).** Unclear whether they are real duplicate listings or different cars with identical features (mileage is binned and there is no listing ID). To investigate before deciding.
4. **Mileage is text, in ranges of unequal width** (5,000, 10,000 and 50,000 km). The most frequent range is "200 000 - 249 999" (10,075 rows). Hypothesis: this may be a catch-all choice. To check.
5. **Year is text and contains "1980 ou plus ancien"** (307 rows), which is a category, not a number.
6. **Fiscal Power is text** (e.g. "8 CV"): the number must be extracted.
7. **Equipment is a list stored as a string**: needs parsing.
8. **Brand:** the top 24 brands look clean, but a lowercase "mini" appeared in `head()`: possible spelling variants to normalize.

### Open questions
- What is the unit of Price? The median (110,000) is consistent with MAD, but I must confirm it in the dataset description.
- Which price outliers are errors, and which are legitimate luxury cars?
- Does a missing value (First Owner, Origin) carry information?

### Next steps
- Study the price distribution (quantiles, lowest and highest values).
- Decide how to handle duplicates.
- Parse Mileage, Year, Fiscal Power and Equipment.
- Split train/test before any statistical preprocessing. 
### Update after price checks
- Brands: 81 unique values, no case variants.
- Years: last values are 2015-2024, consistent with a 2024 collection.
- Price quantiles: 1% = 10,500; 5% = 27,000; 25% = 60,000; 50% = 110,000; 75% = 170,000; 95% = 370,000; 99% = 760,000. These magnitudes look plausible for MAD, but the unit is still to be confirmed.
- 126 prices are exactly 1, and others are 2, 3 or 4: placeholders, not real prices. 557 rows are below 5,000.
- 123 prices are above 5 million (85 above 10 million). Several have repeated digits (99,999,999; 55,555,555; 33,333,333), which suggests data entry errors.
- Plan: remove clearly invalid prices with a business rule before the split. Apply any statistical clipping after the split, on the training set only.

## C. Existing project: Morocco-Used-Car-Market-Analysis
(à compléter)

## D. What influences used car prices in Morocco
(à compléter)