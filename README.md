
# 📦 Resource Optimizer for Amazon Deliveries

An interactive system for optimizing and recommending resources for Amazon deliveries, built with Python and Streamlit. Uses real Amazon delivery data from Kaggle to help improve delivery efficiency and logistics planning.

---

## 🚀 Features

- **Delivery Time Prediction:** Predicts delivery time based on agent, location, weather, traffic, and vehicle type.
- **Vehicle Recommendation:** Suggests the best vehicle type for the lowest predicted delivery time, given the delivery conditions.
- **Interactive Dashboard:** Visualize statistics, distributions, and correlations in delivery data.
- **Dynamic Filtering:** Filter data by area and vehicle type for custom analysis.
- **Modern UI:** All features accessible via a user-friendly Streamlit web interface.

---

## 🗂️ Project Structure

```
resource-optimizer-delivery/
├── app/
│   ├── main.py               # Data loading and cleaning
│   ├── optimizer.py          # Delivery time prediction model
│   └── recommender.py        # Vehicle recommendation logic
├── data/
│   ├── amazon_delivery.csv   # Dataset file
│   └── README.md             # Data instructions
├── frontend/
│   └── app_ui.py             # Streamlit dashboard (main app)
├── tests/
│   └── test_optimizer.py     # Unit tests
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## 📁 Dataset

Based on: [Amazon Delivery - Kaggle Notebook](https://www.kaggle.com/code/fareedalianwar/amazon-delivery)

---

## ▶️ Getting Started

Clone the repository and install dependencies:

```bash
git clone https://github.com/seu-usuario/resource-optimizer-delivery.git
cd resource-optimizer-delivery
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run frontend/app_ui.py
```

---

## 🖥️ How to Use

1. **Launch the app**: Open the provided local URL after running the Streamlit command.
2. **Explore tabs**:
   - **Statistics**: View KPIs and delivery data.
   - **Visualization**: Analyze distributions, locations, and categorical breakdowns.
   - **Data Analysis**: See correlations and advanced plots.
   - **Prediction**: Enter delivery conditions to predict delivery time and get the best vehicle recommendation.
3. **Filter data**: Use the sidebar to filter by area and vehicle type.
4. **Get recommendations**: In the Prediction tab, fill in the form and see both the predicted delivery time and the recommended vehicle for your scenario.

---

## 🧑‍💻 Technologies

- Python 3.10+
- Streamlit
- scikit-learn
- pandas, numpy, altair

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

