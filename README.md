
# 🏀 CoachAI

**CoachAI** is an AI-powered basketball assistant app designed for team management, player stats, and in-game support. Built with Python + Kivy + SQLite + OpenAI.

---

## 🔧 Features

- 📋 Add / Edit / Delete players
- 📝 Enter and track match statistics
- 💬 Smart chatbot assistant (OpenAI)
- 📊 View player details and stats
- ⚙️ Works offline (except chatbot)

---

## 🖥️ How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/CoachAI.git
   cd CoachAI
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python main.py
   ```

---

## 💡 Tech Stack

- Python 3
- Kivy + KivyMD
- SQLite (local DB)
- OpenAI API (chatbot)
- Modular MVC structure

---

## 🗂️ Structure

```
CoachAI/
├── main.py
├── database.py
├── utils.py
├── requirements.txt
├── screens/
├── data/
└── README.md
```

---

## 📂 Note

- Don't forget to set your OpenAI API key in a `.env` file like this:
  ```
  OPENAI_API_KEY=your_key_here
  ```

---

## 👤 Author

**Gökhan Özkan** – [github.com/gokhoz](https://github.com/gokhoz)
