# NYC Urban Mobility Intelligence Platform 🚖

**Comprehensive NYC Taxi & Rideshare Data Analysis & Prediction System**

> **[Türkçe README için buraya tıklayın](README.tr.md)**

This is an end-to-end data science project designed to understand, predict, and optimize New York City's complex transportation network. Using **~1 Million rows** of real-world data (NYC TLC), it features AI models for demand prediction, market analysis, and driver optimization.

---

## 🌟 Key Features (Step-by-Step)

This project provides critical capabilities needed by transportation companies or city planners:

### 1. Predicting the Future (Demand Prediction)
*   **What it does:** Predicts how many taxis will be needed in Manhattan tomorrow, next week, or at a specific hour.
*   **How it works:** Analyzes historical data to learn hourly, daily, and seasonal trends.
*   **Benefit:** Prevents empty cruising and directs fleets exactly where they are needed. (90% Accuracy)

### 2. Maximizing Revenue (Driver Optimization)
*   **What it does:** Provides smart suggestions to drivers like "Go to the airport now" or "Passengers in this zone tip 15% higher."
*   **How it works:** Analyzes tip data and regional density.
*   **Benefit:** Offers potential to increase driver income by up to 20%.

### 3. Estimating Duration (Customer Satisfaction)
*   **What it does:** Calculates exactly how many minutes a trip will take based on traffic and distance.
*   **How it works:** Processes traffic density and trip distance using the XGBoost algorithm.
*   **Benefit:** Gives customers precise info like "You'll be there in 25 minutes" (Margin of error only ~3 minutes).

### 4. Automatic Data Download (Smart Downloader)
*   **What it does:** Downloads and sets up the massive 1GB dataset for you.
*   **How it works:** Detects missing files when you run the code and fetches them from NYC.gov servers.
*   **Benefit:** Eliminates the hassle of manual downloading; works with a single click.

---

## 🏆 Business Impact & Results

*   **Demand Prediction Accuracy:** 90% (R²: 0.899)
*   **Revenue Increase Potential:** ~20% (via optimized routing)
*   **Duration Prediction Error:** Only ~3 minutes (MAE)
*   **Airport Strategy:** Opportunity to increase average fare from $18 to $53.

---

## 📚 Libraries Used & Their Purpose

Each library in this project was carefully selected to meet specific technical needs:

| Library | Used For | Why Selected? |
| :--- | :--- | :--- |
| **Pandas** | Data Manipulation | Industry standard for filtering, cleaning, and transforming 1 million rows of data. |
| **PyArrow** | Data Reading (Parquet) | To read large datasets (Parquet format) 10x faster and more memory-efficiently than CSV. |
| **Scikit-learn** | Machine Learning | For splitting data (train_test_split) and implementing the Random Forest algorithm. |
| **XGBoost** | Advanced ML | For high speed and accuracy (Gradient Boosting) in complex problems like tip and duration prediction. |
| **Joblib** | Model Saving | To save trained models to disk so they can be reused without retraining. |
| **Requests** | Data Downloading | To automatically download 1GB datasets within the code (Smart Downloader). |

---

## 🛠️ Step-by-Step: How to Run?

Follow these 3 steps to run the project on your machine:

**Step 1: Clone the Project**
Open your terminal or command line:
```bash
git clone https://github.com/Egekocaslqn00/nyc-mobility-intelligence.git
cd nyc-mobility-intelligence
```

**Step 2: Install Requirements**
```bash
pip install -r requirements.txt
```

**Step 3: Start Analysis (One Command)**
Run the following command and sit back. The code will download data, train models, and generate results automatically.
```bash
python src/main_analysis.py
```

---

## 📊 Visualizations

![Hourly Demand Analysis](visualizations/images/hourly_demand.png)
![Market Share](visualizations/images/market_share.png)
