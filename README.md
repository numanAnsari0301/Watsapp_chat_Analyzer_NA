# 💬 WhatsApp Chat Analyzer

A Streamlit web app that turns an exported WhatsApp chat into an interactive dashboard: message statistics, timelines, activity patterns, most active users, word cloud, common words and emoji usage. Built with Python, NumPy, pandas and Matplotlib.

> **Privacy:** the chat is processed locally on your machine. Nothing is sent to any external service.

---
## [live link(click)] (https://watsapp-chat-analyzer-na-7pq0.onrender.com)
## ✨ Features

- **Top statistics:** total messages, total words, media messages and shared links
- **Monthly timeline:** how chat activity changes month by month
- **Daily timeline:** message volume for every day in the chat
- **Activity map:** busiest day of the week and busiest month
- **Most busy users:** who talks the most in a group, with a percentage table
- **Word cloud:** the words that define the conversation
- **Most common words:** top words by frequency, with stop words removed
- **Emoji analysis:** emoji counts as a table and a pie chart
- **Per-user view:** analyze the whole group ("Overall") or any single participant
- Supports multi-language chats, including Hindi and Hinglish

---

## 🛠️ Tech Stack

| Purpose | Library |
|---|---|
| Language | Python 3.9+ |
| Numerical work | NumPy |
| Data handling | pandas |
| UI | Streamlit |
| Charts | Matplotlib, Seaborn |
| Word cloud | wordcloud |
| Emoji extraction | emoji |

---

## 📁 Project Structure

```
whatsapp-chat-analyzer/
├── app.py             # Streamlit UI
├── preprocessor.py    # Parses the raw .txt export into a DataFrame
├── helper.py          # Analysis functions (stats, timelines, words, emojis)
├── stop_hinglish.txt  # Stop words list (optional)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 📤 How to Export a WhatsApp Chat

1. Open the chat (individual or group) in WhatsApp
2. Tap **⋮ (menu) → More → Export chat**
3. Choose **Without media**
4. Save the `.txt` file and upload it using the sidebar in the app

Both the 12-hour and 24-hour time formats are supported.

---

## 🧠 How It Works

1. **Preprocessing:** `preprocessor.py` splits the raw text with regular expressions into date, time, user and message, then derives year, month, day, hour and other columns.
2. **Analysis:** `helper.py` filters by the selected user and computes statistics, timelines, word frequencies and emoji counts using pandas and NumPy.
3. **Visualization:** `app.py` renders the results with Streamlit and Matplotlib.

---

## 🖼️ Screenshots

<!-- Replace with your own screenshots -->
| Overview | Timelines |
|---|---|
| ![Overview](screenshots/overview.png) | ![Timelines](screenshots/timelines.png) |

| Word Cloud | Emoji Analysis |
|---|---|
| ![Word Cloud](screenshots/wordcloud.png) | ![Emojis](screenshots/emojis.png) |

---

## ⚠️ Notes

- The app currently loads fonts from `C:/Windows/Fonts/` (Nirmala UI and Segoe UI Emoji) for Hindi text and emoji rendering. On Linux or macOS, point `font_path` to a font that supports Devanagari, or bundle a font file in the repo.
- Matplotlib cannot draw color emoji. The emoji table shows them correctly, while pie chart labels may appear monochrome.

---

## 🔮 Future Improvements

- Sentiment analysis of messages
- Response-time analysis between participants
- Hourly activity heatmap
- Export the report as PDF
- Deployment on Streamlit Community Cloud

---

## 🤝 Contributing

Contributions are welcome. Fork the repo, create a feature branch, and open a pull request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

## 👤 Author

**Your Name**
GitHub: [@your-username](https://github.com/your-username)
