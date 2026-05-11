# Finance Money Exchange Application

> MSE800 - Week 4 Activity 2 | Object-Oriented Programming with Python & SQLite

A Python-based currency exchange system demonstrating OOP principles with a normalized SQLite database. The application supports multi-currency exchange operations, real-time rate calculations, transaction management, and audit trail logging.

---

## Application Scenario

**Global Travel Money Exchange (GTME)** is a financial services company that provides currency exchange services to international travelers and businesses. The company operates multiple exchange booths across major airports and city centers. To modernize their operations and reduce manual calculation errors, GTME has commissioned this digital Finance Money Exchange Application.

The application serves two primary user groups:
- **Regular Customers** who need to exchange currencies for travel or business purposes
- **Administrative Staff** who manage exchange rates, currencies, and monitor transactions

The system must handle daily exchange operations efficiently while maintaining accurate records for audit and compliance purposes.

---

## Features

### For Regular Users
- Register account with email, phone, and name
- Login / Authenticate
- View current exchange rates between currency pairs
- Calculate conversion preview (before executing)
- Perform currency exchange with fee calculation
- View personal transaction history

### For Administrators
- Manage currencies (add, update, deactivate)
- Update exchange rates between currency pairs
- View all system transactions
- Manage user accounts
- Generate operational reports
- View audit logs for compliance monitoring

---

## Files

| File | Description |
|------|-------------|
| `exchange.py` | Core module containing Currency, ExchangeRate, Transaction, and User classes |
| `database.py` | SQLite database operations - table creation, queries, and data access |
| `main.py` | Entry point - CLI menu for user interaction and program flow |
| `utils.py` | Utility functions for validation, formatting, and helpers |

---

## How to Run

```bash
python main.py
```

### Example Output

```
========================================
  Finance Money Exchange Application
========================================
1. Login
2. Register
3. View Exchange Rates
4. Calculate Conversion
5. Perform Exchange
6. View Transaction History
7. Admin Menu
0. Exit

Select an option: 3

Current Exchange Rates:
USD -> EUR: 0.85
USD -> GBP: 0.73
USD -> CNY: 6.45
EUR -> USD: 1.18
...
```

---

## Database Design

The application uses a normalized SQLite database (`exchange.db`) with 5 interconnected tables:

| Table | Columns | Purpose |
|-------|---------|---------|
| **Users** | id, email, phone, name, password_hash, created_at | Store user account information |
| **Currency** | id, code, name, symbol, is_active | Manage available currencies (USD, EUR, GBP, CNY...) |
| **ExchangeRate** | id, from_currency_id, to_currency_id, rate, updated_at | Store exchange rates between currency pairs |
| **Transaction** | id, user_id, exchange_rate_id, amount, converted_amount, fee, status, created_at | Record all exchange transactions |
| **Log** | id, transaction_id, old_status, new_status, timestamp | Track transaction status changes for audit trail |

### Why 5 Tables?
1. **Users** - Core requirement to identify transaction initiators
2. **Currency** - Normalization: avoid duplicating currency data across records
3. **ExchangeRate** - Enables rate lookup for conversions
4. **Transaction** - Complete audit trail for all user transactions
5. **Log** - Transaction history and status tracking for compliance

---

## OOP Features Used

| OOP Principle | Implementation |
|---------------|----------------|
| **Class** | `Currency`, `ExchangeRate`, `Transaction`, `User` - bundles data and behavior together |
| **Instance Variables** | `self.code`, `self.rate`, `self.amount` - store each object's unique data |
| **Methods** | `calculate_conversion()`, `execute_exchange()`, `get_rate()` - perform operations on object data |
| **Modularity** | Class definitions and main program are in separate files |
| **Encapsulation** | Internal state is protected; only intended interfaces are exposed |
| **Database Abstraction** | Data access layer is separated from business logic |

---

## Use Case Overview

```
+------------------+                         +------------------+
|   Regular User   |                         |      Admin       |
+------------------+                         +------------------+
         |                                           |
         |-- Register Account                        |-- Manage Currencies
         |-- Login / Authenticate                     |-- Update Exchange Rates
         |-- View Exchange Rates                      |-- View All Transactions
         |-- Calculate Conversion                     |-- Manage Users
         |-- Perform Exchange                         |-- Generate Reports
         |-- View Transaction History                 |-- View Audit Logs
         |                                           |
         +--------------+       +--------------------+
                        |       |
            +-----------+-------+-----------+
            |  Finance Money Exchange App   |
            +-------------------------------+
```

### Use Case Relationships
- `Register Account` <<include>> `Login` (auto-login after registration)
- `Perform Exchange` <<include>> `View All Transactions` (record transaction)
- `Calculate Conversion` <<extend>> `Update Exchange Rates` (ensure current rate)
- `View Transaction History` <<extend>> `Generate Reports`

---

## Scope Definition

### In Scope
- User registration and authentication
- Currency catalog management
- Exchange rate management
- Conversion calculation and exchange execution
- Transaction recording and history viewing
- Audit logging
- Report generation
- OOP design with proper class structure
- SQLite database with normalized 5-table schema

### Out of Scope
- External payment gateway integration
- Real-time rate fetching from financial APIs
- Multi-language UI support
- Mobile or web application (CLI only)
- User notification system
- Advanced analytics and forecasting
- Cryptocurrency support
- Concurrent multi-user processing

---

## Project Structure

```
Week4/Activity2/
|-- exchange.py       # Core business classes
|-- database.py       # Database operations
|-- main.py           # Application entry point
|-- utils.py          # Helper utilities
|-- exchange.db       # SQLite database (auto-generated)
|-- README.md         # This file
|-- Scenario.docx     # Detailed application scenario
|-- UseCaseDiagram.png # UML use case diagram
```

---

## Author

MSE800 - Software Engineering
