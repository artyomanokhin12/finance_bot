#!/bin/bash

psql -U postgres -c "INSERT INTO incomes (incomes_name) VALUES ('Зарплата'), ('Подарки'), ('В долг'), ('Прочие'); INSERT INTO spendings (spendings_name, optional_spending) VALUES ('Кафе', 'false'), ('Бар', 'false'), ('Здоровье', 'false'), ('Такси', 'false'), ('Книги', 'false'), ('Подписки', 'false'), ('Развлечения', 'false'), ('Алкоголь', 'false'), ('Никотин', 'false'), ('Концерты', 'false'), ('Одежда', 'false'), ('Долг', 'false'), ('Прочие', 'false'), ('Дом', 'true'), ('Продукты', 'true'), ('Транспорт', 'true'), ('Связь и интернет', 'true');"
