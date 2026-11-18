import pandas as pd
import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root",
                                password="lava_2006",
                                database="employee_db")
cursor = conn.cursor()

# Safety check to avoid duplicate inserts if run twice
cursor.execute("select count(*) from employees_raw")
existing = cursor.fetchone()[0]

if existing > 0:
    print(f"Table already has {existing} records. Skipping insert to avoid duplicates.")
else:
    data = pd.read_csv(r"C:\Users\hp\Downloads\Employee_DE_Pipeline\Data\Cleaned_Data\employee_cleaned.csv")

    for _, row in data.iterrows():
        cursor.execute("""insert into employees_raw
            (employee_id, department, experience_years, salary, work_mode,
             satisfaction_score, gender, education_level)
            values (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (int(row["employee_id"]), row["department"], row["experience_years"],
             row["salary"], row["work_mode"], row["satisfaction_score"],
             row["gender"], row["education_level"]))

    conn.commit()
    print("Data loaded successfully!")

cursor.execute("select count(*) from employees_raw;")
print("Total records loaded:", cursor.fetchone()[0])

cursor.execute("select * from employees_raw limit 5;")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
