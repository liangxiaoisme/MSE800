-- 1. 用户表
CREATE TABLE Users (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

-- 2. 货币表
CREATE TABLE Currencies (
    id INT PRIMARY KEY,
    code VARCHAR(3)
);

-- 3. 交易表
CREATE TABLE   (
    id INT PRIMARY KEY,
    user_id INT,
    currency_from INT,
    currency_to INT,
    amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (currency_from) REFERENCES Currencies(id),
    FOREIGN KEY (currency_to) REFERENCES Currencies(id)
);