# Financial Accounting Program

This project is a comprehensive financial accounting application developed in Python, designed to run on Windows operating systems. The application fully supports the Arabic language with right-to-left (RTL) alignment, making it accessible for Arabic-speaking users.

## Features

- **Accounts Management**: Manage customer and supplier accounts, including adding, modifying, deleting, and viewing accounts. Calculate outstanding debts and payables.
- **Transactions Handling**: Handle purchase and sales invoices with functionalities to add, modify, delete, and view invoices. Calculate total purchases and sales.
- **Financial Reporting**: Generate various financial reports, including profit and loss statements, total revenue, total expenses, and final balance reports.
- **Localization**: Fully translated into Arabic, ensuring all strings and messages are appropriately localized.
- **RTL Support**: User interface components are designed to support right-to-left alignment for a better user experience for Arabic users.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd financial-accounting-program
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Project Structure

```
financial-accounting-program
├── src
│   ├── main.py
│   ├── modules
│   │   ├── accounts.py
│   │   ├── transactions.py
│   │   ├── reports.py
│   │   └── utilities.py
│   ├── localization
│   │   ├── arabic.py
│   │   └── rtl_support.py
│   └── ui
│       ├── main_window.py
│       ├── rtl_styles.py
│       └── components.py
├── requirements.txt
├── README.md
└── LICENSE
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.