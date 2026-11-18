import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["employee_nosql"]

data = pd.read_csv(r"C:\Users\hp\Downloads\Employee_DE_Pipeline\Data\Cleaned_Data\employee_cleaned.csv")
records = data.to_dict(orient="records")

# Safety check to avoid duplicate inserts if run twice
if db.employees.count_documents({}) == 0:
    db.employees.insert_many(records)
    print(f"Inserted {len(records)} documents into MongoDB.")
else:
    print(f"Collection already has {db.employees.count_documents({})} documents. Skipping insert.")

# Sample queries
print(db.employees.find_one({"department": "IT"}))
print(db.employees.count_documents({"salary": {"$gt": 60000}}))
print(list(db.employees.aggregate([
    {"$group": {"_id": "$department", "avgSalary": {"$avg": "$salary"}}}
])))
