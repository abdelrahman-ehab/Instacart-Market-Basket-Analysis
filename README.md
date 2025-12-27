# Instacart Market Basket Analysis

## Project Overview
This project analyzes over 3 million grocery orders from Instacart to uncover latent purchasing patterns. By implementing a robust ETL pipeline and the **FP-Growth Algorithm**, I identified strong product relationships to inform cross-selling strategies. The final output is an interactive Power BI dashboard powered by SQL Views that functions as a "Strategy Engine" for inventory managers.

## Business Problem
Retailers often struggle to identify which products drive sales of other items. Understanding these "Market Baskets" is crucial for:
- Optimizing store layout (placing related items together).
- Creating effective bundle promotions.
- Predicting churn based on purchasing habits.

## Tech Stack & Architecture
- **Python:** Built an ETL pipeline for data extraction, cleaning, and preprocessing. Implemented the **FP-Growth algorithm** (MLxtend) for efficient frequent itemset mining.
- **SQL:** Conducted in-depth Exploratory Data Analysis (EDA) to understand distribution and trends. Created optimized **SQL Views** to serve as the direct data layer for Power BI, ensuring performance and data consistency.
- **Power BI:** Interactive dashboarding, DAX measure creation, and custom UI design based on Instacart brand guidelines.

## Key Analysis & Metrics
I focused on three core metrics to evaluate relationship strength:
1. **Frequency (Support):** How often a bundle appears in transactions.
2. **Probability (Confidence):** The likelihood of Item B being purchased if Item A is in the cart.
3. **Association Strength (Lift):** How much stronger the link is compared to random chance.

## Dashboard Structure
The Power BI report is structured into three strategic pages:
1. **Executive Summary:** High-level store health, sales trends, and an hourly sales heatmap.
2. **Customer Habits:** Analysis of reorder rates, habit formation, and days between orders.
3. **Strategy Engine:** An interactive tool allowing managers to select a product and immediately receive specific cross-selling recommendations based on Lift and Confidence thresholds.

## Results
- Identified high-value bundles (e.g., Limes and Organic Avocados) with an Association Strength > 2.0.
- Developed a "Day/Hour Heatmap" to pinpoint peak reorder times for inventory planning.
- Created a dynamic "Strategy Verdict" system that automatically categorizes product pairs into "Create Bundle" or "Cross-Sell" actions.
