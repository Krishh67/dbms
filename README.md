# College Canteen Food Ordering System

A web-based food ordering system built with Flask and MySQL, featuring real-time order tracking, voice search, and a chef dashboard.

## Features

### Customer Features
- User authentication and registration
- Browse menu items by category (Meals, Drinks, Canteen items)
- Voice search functionality with Indian English support
- Shopping cart management
- Real-time order tracking
- Payment processing
- Order history view

### Chef Features
- Dedicated chef dashboard
- Real-time order notifications
- Order status management (pending → cooking → ready)
- Auto-refreshing order list
- Order analytics

## Project Video


https://github.com/user-attachments/assets/6b6f9d25-f910-4f38-baa9-b69c20a9f25d



## Technology Stack

- **Backend:** Python Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Additional Features:** 
  - Speech Recognition
  - Text-to-Speech
  - Real-time Updates


## Project Structure

```
college_canteen/
├── static/
│   ├── images/
│   │   ├── logo.png
│   │   └── menu_items/
│   ├── css/
│   └── js/
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── category/
│   │   ├── meals.html
│   │   ├── drinks.html
│   │   └── menu.html
│   ├── cart.html
│   ├── checkout.html
│   ├── payment.html
│   ├── order_confirmation.html
│   ├── order_status.html
│   └── chef_dashboard.html
├── app.py
├── database.sql
└── README.md
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/Krishh67/college_canteen.git
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up MySQL database
```bash
mysql -u root -p < database.sql
```

5. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. Run the application
```bash
python app.py
```

## Database Normalization

The database is designed following normalization principles:
- 1NF: All tables have primary keys and atomic values
- 2NF: No partial dependencies
- 3NF: No transitive dependencies
- BCNF: Every determinant is a candidate key

## SQL Features Used

- JOIN operations
- Aggregation functions
- Transaction management
- Foreign key constraints
- Complex queries with CASE statements
- Real-time data updates

## Detailed Info

[project_report.docx](https://github.com/user-attachments/files/19752359/project_report.docx)



## Contact

For any queries, please contact:
- Email: krishp4216@gmail.com
- Project Link: [https://github.com/Krishh67/college_canteen](https://github.com/Krishh67/dbms)
