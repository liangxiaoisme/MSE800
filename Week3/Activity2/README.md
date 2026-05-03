# Database Design for Finance Money Exchange System

## Project Overview

This repository contains the database design for a finance money exchange application. The goal is to design a normalized relational schema that manages users, accounts, transactions, exchange rates, payment methods, and fees.

## Core Entities and Attributes

1. **User**: `User_id (PK)`, `Full_name`, `Email`, `Phone_number`, `KYC_status`, `Created_at`
2. **Account**: `Account_id (PK)`, `User_id (FK)`, `Currency_code`, `Balance`, `Account_status`, `Opened_at`
3. **Transaction**: `Transaction_id (PK)`, `Source_account_id (FK)`, `Dest_account_id (FK)`, `Exchange_rate_id (FK)`, `Amount`, `Status`
4. **Exchange Rate**: `Rate_id (PK)`, `Base_currency`, `Target_currency`, `Rate_value`, `Valid_from`, `Valid_to`
5. **Payment Method**: `Method_id (PK)`, `User_id (FK)`, `Method_type`, `Provider`, `Is_verified`, `Added_at`
6. **Fee**: `Fee_id (PK)`, `Transaction_id (FK)`, `Fee_type`, `Amount`, `Currency_code`, `Applied_at`

## Database Relationships

### 1. One-to-Many (1:N): User → Accounts
One user can hold multiple currency accounts. `User_id` is stored as a FK in the `Account` table.

### 2. One-to-Many (1:N): User → Payment Methods
One user can register multiple payment methods. `User_id` is stored as a FK in the `Payment_Method` table.

### 3. Many-to-Many (M:N): Accounts ↔ Transactions
An account can send or receive many transactions. Resolved by two FKs in `Transaction`: `Source_account_id` and `Dest_account_id`.

### 4. One-to-Many (1:N): Exchange Rate → Transactions
One rate snapshot applies to many transactions. `Exchange_rate_id` is stored as a FK in `Transaction`.

### 5. One-to-Many (1:N): Transaction → Fees
One transaction can incur multiple fees. `Transaction_id` is stored as a FK in the `Fee` table.

## Conclusion

This design avoids redundancy by placing foreign keys on the "Many" side of every relationship, keeping the schema clean, auditable, and easy to extend.
