from validator import SQLQueryValidator

# Sample dictionary of tables and fields
table_fields = {
    "users": ["id", "name", "email"],
    "orders": ["id", "user_id", "product_id"],
    "products": ["id", "name", "price"],
}

# Create SQL query validator instance
validator = SQLQueryValidator(table_fields)

# Sample SQL queries to validate
query1 = "SELECT id, name, email FROM users WHERE id = 1;"
query2 = "SELECT name, price FROM products WHERE price < 10.0 ORDER BY name;"
query3 = (
    "SELECT id, user_id, product_id FROM orders WHERE user_id = 1 AND product_id = 2;"
)
query4 = "SELECT id, name, email FROM customers WHERE id = 1;"

# Validate SQL queries
print(validator.validate_query(query1))  # True
print(validator.validate_query(query2))  # True
print(validator.validate_query(query3))  # True
print(validator.validate_query(query4))  # False
