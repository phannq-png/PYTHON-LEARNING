# 📚 Glossary Management Tool

A lightweight, cross-platform desktop application for managing multilingual vocabulary and technical terms.  
Built with **Python**, **CustomTkinter**, and **SQLite3**.

---

## 🌟 Key Features

### 🧾 Entry Management
- Easily add, delete, and view glossary entries.

### 🚫 Duplicate Prevention
- Automatically validates entries to prevent redundant data.

### 🔄 Smart Data Import / Export
- **Export:** Save data to CSV format using `UTF-8-sig` encoding  
  *(ensures compatibility with Excel and special characters)*  
- **Import:** Bulk load entries from CSV files with built-in skip logic for existing terms

### 🎨 Modern UI
- Clean, responsive interface powered by `CustomTkinter`
- Native **Dark Mode** support

### 💾 Reliable Storage
- Local **SQLite** database for fast and persistent data management

---

## 🛠 Tech Stack

- **Language:** Python 3.x  
- **GUI Framework:** CustomTkinter (Modernized Tkinter)  
- **Database:** SQLite3  
- **Architecture:** Component-based design  

---

## 📂 Project Structure

```text
.
├── src/
│   ├── database/
│   │   └── db_manager.py      # Database connection and SQL logic
│   ├── gui/
│   │   ├── components/
│   │   │   └── menu_bar.py    # Modular Menu Bar component
│   │   └── app.py             # Main application window logic
│   └── main.py                # Application entry point
├── requirements.txt           # Project dependencies
└── README.md
```

---

## 🚀 Getting Started

### 📌 Prerequisites
- Python 3.8 or higher  
- pip (Python package installer)  

### ⚙️ Installation

#### 1. Clone the repository
```bash
git clone https://github.com/yourusername/glossary-management-tool.git
cd glossary-management-tool
```

#### 2. Set up a virtual environment *(optional but recommended)*
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python src/main.py
```

---

## 📖 Usage

### ➕ Adding Terms
- Input source and target language terms in the left panel
- Click **Add**

### ❌ Removing Terms
- Select a row in the table
- Click **Delete**

### 🔁 Backup / Sync
- Use the **File menu** to import or export your database as a CSV file

### 🧹 Clear Data
- Clear the entire list and reset the ID counter via application logic

---

## 📄 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.
