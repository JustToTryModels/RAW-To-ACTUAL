<div align="center">

# 📈 NVIDIA Stock Price Prediction

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)](https://keras.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

A comprehensive time series forecasting project that analyzes and predicts **NVIDIA Corporation's (NVDA)** stock closing prices using multiple forecasting models — including LSTM, ARIMA, Facebook Prophet, and Exponential Smoothing techniques — on over **25 years of historical market data** (January 1999 – August 2024).

<br>

---

## 📋 Table of Contents

- [What is Stock Price Prediction?](#-what-is-stock-price-prediction)
- [Why NVIDIA?](#-why-nvidia)
- [Project Overview](#-project-overview)
- [Demo](#-demo)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [Exploratory Data Analysis](#-exploratory-data-analysis-eda)
- [Methodology](#-methodology)
- [Model Comparison & Selection](#-model-comparison--selection)
- [Final Model Results](#-final-model-results)
- [10-Day Price Forecast](#-10-day-price-forecast)
- [Installation & Usage](#-installation--usage)

<br>

---

## ❓ What is Stock Price Prediction?

<br>

**Stock price prediction** is the practice of forecasting future stock values using historical data, statistical methods, and machine learning algorithms. Key approaches include:

- 📊 **Technical Analysis:** Examines historical price patterns, trading volumes, and chart indicators
- 💼 **Fundamental Analysis:** Evaluates company financials, industry trends, and economic indicators
- 🤖 **Machine Learning & AI:** Utilizes advanced algorithms (LSTM, ARIMA, Prophet, etc.) to capture complex patterns
- 📰 **Sentiment Analysis:** Analyzes news articles and social media to gauge investor psychology

### ⚠️ Important Limitations
| Limitation | Description |
|------------|-------------|
| **Market Unpredictability** | Markets are influenced by unforeseen events (geopolitical issues, natural disasters) |
| **No Guarantees** | Past performance doesn't guarantee future results |
| **Complementary Tool** | Predictions should be used as one tool among many |
| **Accuracy Limits** | No model can predict stock prices with 100% accuracy |

<br>

---

## 🎯 Why NVIDIA?

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/NVIDIA_logo.svg/1920px-NVIDIA_logo.svg.png" alt="NVIDIA Logo" width="400"/>
</div>

NVIDIA presents a compelling subject for stock price analysis due to several key factors:

### 🏆 Industry Leadership & Innovation
- **Dominant Market Share:** NVIDIA holds a commanding lead in the GPU market
- **Technological Innovation:** Continuously advances GPU technology, driving progress in AI, gaming, and data centers

### 🚀 Growth Potential in Expanding Markets
- **AI & Deep Learning:** NVIDIA's GPUs are critical for training and deploying Large Language Models (LLMs)
- **Major Clients:** Google, Microsoft, OpenAI, Meta, Amazon Web Services, IBM, Tesla, and more
- **Data Centers & Cloud Computing:** Rapidly growing demand for cloud infrastructure

### 💰 Financial Performance
- **Strong Revenue Growth:** Consistently delivered strong revenue driven by AI demand
- **Market Volatility:** NVIDIA's stock shows significant price movements — ideal for time series modeling

<br>

---

## 🎯 Project Overview

### Objective

Predict NVIDIA's future closing stock prices by analyzing 25+ years of historical data using multiple time series forecasting models, and identify the best-performing model for deployment.

<div align="center">

### 🛣️ Approach

| Component | Description |
|-----------|-------------|
| **Data Span** | January 22, 1999 — August 2, 2024 (6,424 trading days) |
| **Models Evaluated** | 6 Forecasting Models |
| **Selected Model** | LSTM (Long Short-Term Memory) |
| **Hyperparameter Tuning** | Grid search over look-back windows & LSTM units |
| **Evaluation Metric** | Root Mean Squared Error (RMSE) |
| **Deployment** | Streamlit Web Application |

</div>

<br>

---

## 🚀 Demo

Try the live stock price prediction model here:

[![Open Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nvidia-stock-price-predictor.streamlit.app/)

<br>

<div align="center">

| Price Action & Forecast | Detailed Forecast |
|:-----------------------:|:-----------------:|
| <img src="https://github.com/MarpakaPradeepSai/NVIDIA-Stock-Price-Predictor/blob/main/Data/Images%20&%20GIF/NVIDIA_GIF_1.gif?raw=true" alt="Price Action & Forecast" width="100%"/> | <img src="https://github.com/MarpakaPradeepSai/NVIDIA-Stock-Price-Predictor/blob/main/Data/Images%20&%20GIF/NVIDIA_GIF_2.gif?raw=true" alt="Detailed Forecast" width="100%"/> |

</div>

> Enter a date range and instantly get predicted NVIDIA closing prices powered by the trained **LSTM model**!

<br>

---

## 📁 Project Structure

```
nvidia-stock-price-prediction/
├── Data/
│   └── NVIDIA.csv                                  # Historical stock dataset (1999–2024)
├── Model/
│   └── NVIDIA_LSTM_LB(5)_U(150)_RMSE(1.32).keras  # Saved best LSTM model
├── Notebook/
│   └── NVIDIA_Stock_Price_Analysis.ipynb           # Full analysis & model comparison notebook
├── app.py                                          # Streamlit web application
├── requirements.txt                                # Python dependencies
├── LICENSE                                         # MIT License
└── README.md                                       # Project documentation
```

<br>

---

## 📊 Dataset

<div align="center">

### Overview

| Metric | Value |
|--------|-------|
| **Data Source** | Yahoo Finance / Kaggle |
| **Date Range** | January 22, 1999 — August 2, 2024 |
| **Total Trading Days** | 6,424 rows |
| **Training Set** | 5,139 rows (80%) |
| **Testing Set** | 1,285 rows (20%) |

</div>

<br>

<div align="center">

### Features

| Feature | Description |
|---------|-------------|
| `Date` | Specific trading day (chronological timeline) |
| `Open` | Stock price at market open — reflects initial investor sentiment |
| `High` | Highest price during the trading session — indicates peak demand |
| `Low` | Lowest price during the day — shows minimum valuation and intraday volatility |
| `Close` | Final trading price at market close — **primary prediction target** |
| `Adj Close` | Closing price adjusted for splits, dividends, and other corporate actions |
| `Volume` | Total shares traded — reflects market activity and liquidity |

</div>

<br>

### 📌 Why This Dataset is Valuable

- **Historical Depth:** Covers 25+ years, capturing multiple economic and technological cycles
- **Diverse Market Conditions:** Includes dot-com bubble, 2008 financial crisis, COVID-19 crash, and the AI boom
- **Rich Information:** Multiple price indicators enable detailed technical analysis
- **Long-term Trends:** Supports identification of growth patterns and seasonal behaviors

<br>

---

## 🔬 Exploratory Data Analysis (EDA)

### 📈 Key Statistical Observations

<div align="center">

| Metric | Close Price | Daily Return |
|--------|-------------|--------------|
| **Mean** | $6.26 | 0.19% |
| **Std Dev** | $16.27 | 3.79% |
| **Min** | $0.034 | -35.23% |
| **Max** | $135.58 | +42.41% |
| **Skewness** | Highly Right-Skewed | 0.616 |

</div>

<br>

### 📉 Volatility Analysis

<div align="center">

| Timeframe | Volatility |
|-----------|------------|
| **Daily** | 3.79% |
| **Weekly** | 8.47% |
| **Monthly** | 17.37% |
| **Annualized** | 60.16% |

</div>

> 💡 **Key Insight:** NVIDIA is a **high-volatility stock** over any timeframe — making it both a challenging and rewarding subject for predictive modeling.

<br>

### 📊 Correlation Findings

- **Open, High, Low, Close, and Adj Close** exhibit near-perfect positive correlation with each other (≈ 0.99+)
- **Volume** shows weak or negative correlation with all price-related variables, indicating independent market activity

<br>

---

## 🔬 Methodology

### 📊 1. Data Preparation
- **Target Variable:** `Close` price (adjusted for splits over 25 years)
- **Train-Test Split:** 80% training, 20% testing — chronological split, no shuffling
- **Scaling:** MinMaxScaler applied to normalize data between [0, 1] for LSTM training

### 🔁 2. Stationarity Check & Transformation (for ARIMA)
- **ADF Test Result:** p-value = 1.0 → **Non-stationary**
- **Best Differencing Order:** d = 1 (found using `ndiffs`)
- **After First-Order Differencing:** p-value ≈ 1.67e-24 → **Stationary** ✅

### ⚙️ 3. Hyperparameter Tuning
- **LSTM:** Grid search over `look_back` ∈ {5, 21, 63, 252} and `units` ∈ {50, 100, 150}
- **SES:** Grid search over `α` ∈ [0.1, 1.0]
- **DES:** Grid search over `α`, `β` ∈ [0.1, 1.0]
- **TES:** Grid search over `α`, `β`, `γ` ∈ [0.1, 1.0]
- **ARIMA:** Grid search over `p` ∈ [0,6], `d` = 0 (pre-differenced data), `q` ∈ [0,6]

<br>

---

## ⚔️ Model Comparison & Selection

Six different forecasting models were trained, tuned, and evaluated on the same 20% hold-out test set. The primary metric used for comparison is **Root Mean Squared Error (RMSE)** — measured in USD.

<br>

### 🚀 Performance Leaderboard (Test Set)

<div align="center">

| Rank | Model | Best Hyperparameters | Test RMSE (USD) |
|:----:|-------|----------------------|:---------------:|
| 🏆 **1** | **LSTM** | `look_back=5`, `units=150` | **$1.32** |
| 2 | ARIMA | `(p=4, d=1, q=3)` | $1.33 (differenced scale) |
| 3 | Double Exponential Smoothing | `α=0.1`, `β=0.2` | $18.22 |
| 4 | Triple Exponential Smoothing | `α=0.1`, `β=0.4`, `γ=0.1` | $18.26 |
| 5 | Facebook Prophet | Default | $31.29 |
| 6 | Simple Exponential Smoothing | `α=0.5` | $36.22 |

</div>

<br>

### 🧠 Why LSTM?

**LSTM (Long Short-Term Memory)** achieved the lowest RMSE of **$1.32** on the test set — outperforming all other models by a significant margin. Here's why LSTM excels for this task:

#### 1. Sequential Data Mastery
Stock prices are inherently sequential — the value at any given time depends on previous values. LSTMs are specifically designed to learn from such ordered sequences via their internal memory cells.

#### 2. Long-Term Dependency Capture
LSTM's gating mechanisms (input, forget, output gates) allow the model to selectively remember relevant historical patterns (e.g., multi-month trends) while discarding noise — something traditional models cannot do.

#### 3. Complex Non-Linear Pattern Learning
NVIDIA's stock is influenced by earnings cycles, GPU demand cycles, macro trends, and AI hype. LSTMs can model these complex, non-linear patterns that ARIMA and exponential smoothing methods fundamentally cannot.

#### 4. Optimal Configuration Found
Through systematic grid search across **12 configurations**, the optimal model used:
- **look_back = 5 days** (using the most recent week of data as context)
- **150 LSTM units** (sufficient model capacity for NVIDIA's volatile price patterns)

<br>

---

## 📈 Final Model Results

<div align="center">

### 🏆 Best LSTM Configuration

| Parameter | Value |
|-----------|-------|
| **Look-back Window** | 5 trading days |
| **LSTM Units** | 150 |
| **Epochs** | 100 |
| **Batch Size** | 32 |
| **Optimizer** | Adam |
| **Loss Function** | Mean Squared Error |

</div>

<br>

<div align="center">

### 💪 LSTM Performance Metrics

| Split | RMSE (USD) |
|-------|:----------:|
| **Training Set** | $0.049 |
| **Test Set** | **$1.32** |

</div>

> ✅ **The model generalizes well — the training and test RMSE are both low with no signs of overfitting!**

<br>

### 🔄 LSTM Grid Search Summary

<div align="center">

| Look-back | Units | Train RMSE | Test RMSE |
|:---------:|:-----:|:----------:|:---------:|
| 5 | 50 | 0.079 | 1.364 |
| 5 | 100 | 0.062 | 1.331 |
| **5** | **150** | **0.049** | **1.325** ✅ |
| 21 | 50 | 0.058 | 1.370 |
| 21 | 100 | 0.060 | 1.339 |
| 21 | 150 | 0.058 | 1.409 |
| 63 | 50 | 0.059 | 1.481 |
| 63 | 100 | 0.060 | 1.389 |
| 63 | 150 | 0.057 | 1.489 |
| 252 | 50 | 0.085 | 1.952 |
| 252 | 100 | 0.050 | 1.473 |
| 252 | 150 | 0.055 | 1.472 |

</div>

<br>

---

## 🔮 10-Day Price Forecast

After selecting the best LSTM model, it was used to generate a **10-day forward forecast** starting from August 5, 2024.

<div align="center">

### 📅 Predicted Closing Prices

| Date | Predicted Close Price |
|------|-----------------------|
| 2024-08-05 (Mon) | **$113.83** |
| 2024-08-06 (Tue) | **$113.54** |
| 2024-08-07 (Wed) | **$112.89** |
| 2024-08-08 (Thu) | **$112.03** |
| 2024-08-09 (Fri) | **$111.04** |
| 2024-08-12 (Mon) | **$109.97** |
| 2024-08-13 (Tue) | **$108.87** |
| 2024-08-14 (Wed) | **$107.75** |
| 2024-08-15 (Thu) | **$106.63** |
| 2024-08-16 (Fri) | **$105.50** |

</div>

> ⚠️ **Disclaimer:** These predictions are for educational purposes only. They should not be used as the sole basis for any investment decision. Always consult a qualified financial advisor.

<br>

---

## 🛠️ Installation & Usage

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MarpakaPradeepSai/NVIDIA-Stock-Price-Predictor.git
   cd NVIDIA-Stock-Price-Predictor
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Run the Streamlit App Locally

```bash
streamlit run app.py
```

The app will open in the default browser at `http://localhost:8501`

### Run the Jupyter Notebook

```bash
jupyter notebook Notebook/NVIDIA_Stock_Price_Analysis.ipynb
```

<br>

---

## 🙏 Thank You

<div align="center">
  <img src="https://github.com/MarpakaPradeepSai/Employee-Churn-Prediction/blob/main/Data/Images%20&%20GIFs/thank-you-33.gif?raw=true" alt="Thank You" width="320">

  If this project was helpful, please consider giving it a ⭐
</div>
```
