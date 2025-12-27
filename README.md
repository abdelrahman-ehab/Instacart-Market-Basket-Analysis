# Instacart Market Basket Analysis

## Project Overview
This project analyzes over 3 million grocery orders from Instacart to uncover latent purchasing patterns. By applying Association Rule Mining (Apriori Algorithm), I identified strong product relationships to inform cross-selling strategies and bundle offers. The final output is an interactive Power BI dashboard that functions as a "Strategy Engine" for inventory managers.

## Business Problem
Retailers often struggle to identify which products drive sales of other items. Understanding these "Market Baskets" is crucial for:
- Optimizing store layout (placing related items together).
- Creating effective bundle promotions.
- Predicting churn based on purchasing habits.

## Tech Stack
- **Python:** Data cleaning, preprocessing, and exploratory data analysis (Pandas, NumPy).
- **Machine Learning:** Association Rule Mining using the Apriori algorithm (MLxtend) to calculate Support, Confidence, and Lift.
- **Power BI:** Interactive dashboarding, DAX measure creation, and custom UI design.

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
