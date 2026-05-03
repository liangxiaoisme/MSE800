# Money Exchange Application Database

## Tables Created: 5

### 1. Users
- Stores user information (email, phone, name)
- **Why**: Core requirement to identify transaction initiators

### 2. Currency
- Stores available currencies with codes and symbols
- **Why**: Normalization - avoid duplicating currency data

### 3. ExchangeRate
- Stores exchange rates between currency pairs
- **Why**: Enables rate lookup for conversions

### 4. Transaction
- Records all exchange transactions with amounts and fees
- **Why**: Audit trail for all user transactions

### 5. Log
- Logs transaction status and timestamps
- **Why**: Transaction history and status tracking

