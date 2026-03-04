# 🏏 Match Insights Dashboard

This Streamlit app provides **batting and bowling insights** for Matches using ball-by-ball data.  
It calculates player performance metrics, including **Player Performance Index (PPI)**, and shows **phase-wise stats** for each match.

---

## **Features**

- Select  **Season**, **Team 1**, **Team 2**, and **Match Date**.  
- View **batting and bowling stats** sorted by **PPI**.  
- Understand **Player Performance Index (PPI)**:  
  - Batters: Runs, Strike Rate, Dot Balls  
  - Bowlers: Wickets, Economy, Dot Balls  
- View **phase-wise performance** (Powerplay / Middle / Death).  
- User-friendly interface — no need to know `match_id`.

---

## **Installation**

1. Clone the repository:

git clone https://github.com/yourusername/ipl-insights.git
cd ipl-insights

2. Create a virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Run the Streamlit app:

streamlit run app.py

## **Project Structure**

ipl-insights/
├─ app.py                  # Main Streamlit app
├─ match_insights.py       # Functions to generate match insights
├─ ipl_ball_by_ball.csv    # Ball-by-ball IPL dataset
├─ requirements.txt        # Python dependencies
└─ README.md

## 📌 Author

👤 **Sachin Kumar Gupta**

🔗 [LinkedIn](linkedin.com/in/sachingupta-ds) | [Portfolio](https://sachin-kumar-gupta.github.io/portfolio/#home)

---

## ⭐ If you like this project...

Please consider ⭐ starring the repository or sharing it with your network!
