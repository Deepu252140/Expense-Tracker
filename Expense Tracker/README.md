# Expense Tracker Web Application

A modern, responsive expense tracking application built with Python Flask, HTML, CSS, and SQLite.

## Features

- Add, view, and delete expenses
- Filter expenses by category and date range
- View total expenses and category-wise breakdowns
- Interactive pie chart for expense visualization
- Clean, modern UI with responsive design
- Input validation for data integrity

## Project Structure

```
expense-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── expenses.db           # SQLite database (created automatically)
├── templates/
│   ├── index.html        # Dashboard and expenses list
│   └── add.html          # Add expense form
└── static/
    └── style.css         # CSS styles
```

## Installation and Setup

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   python app.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000/
   ```

## Usage

- **Dashboard:** View all expenses, total amount, category totals, and pie chart
- **Add Expense:** Click "Add Expense" to enter new expenses
- **Filter:** Use the filter form to search by category and date range
- **Delete:** Click the "Delete" link next to any expense to remove it

## Technologies Used

- **Backend:** Python Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript (Chart.js for charts)
- **Styling:** Custom CSS with responsive design

## Notes

- The database file `expenses.db` is created automatically when you first run the app
- All data is stored locally in the SQLite database
- The application runs in debug mode for development