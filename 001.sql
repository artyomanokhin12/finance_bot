create table incomes(
    id SERIAL PRIMARY KEY,
    incomes_name VARCHAR
);

CREATE TABLE spendings(
    id SERIAL PRIMARY KEY,
    spending_name VARCHAR,
    optional_spending BOOLEAN
);