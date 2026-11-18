**Employee Dataset** 



**Batch Ingestion into MySQL**

*MySQL*

create database employee\_db;
use employee\_db;

create table employees\_raw(
employee\_id int primary key,
department varchar(30),
experience\_years decimal(5,2),
salary decimal(10,2),
work\_mode varchar(30),
satisfaction\_score decimal(3,2),
gender varchar(10),
education\_level varchar(30)
);

*MySQL*
select count(\*) from employees\_raw;  -- verify: 100



**Relational Storage + Fact/Dimension Modelling**

*MySQL*

CREATE DATABASE IF NOT EXISTS employee\_db;
USE employee\_db;

\-- Step 1: Dimension Tables
CREATE TABLE department\_dim(
department\_id INT PRIMARY KEY AUTO\_INCREMENT,
department\_name VARCHAR(30) UNIQUE
);

CREATE TABLE work\_mode\_dim(
work\_mode\_id INT PRIMARY KEY AUTO\_INCREMENT,
work\_mode\_name VARCHAR(30) UNIQUE
);

CREATE TABLE gender\_dim(
gender\_id INT PRIMARY KEY AUTO\_INCREMENT,
gender\_name VARCHAR(10) UNIQUE
);

CREATE TABLE education\_dim(
education\_id INT PRIMARY KEY AUTO\_INCREMENT,
education\_name VARCHAR(30) UNIQUE
);

\-- Step 2: Fact Table
CREATE TABLE fact\_employee\_performance(
employee\_id INT PRIMARY KEY,
department\_id INT,
work\_mode\_id INT,
gender\_id INT,
education\_id INT,
experience\_years DECIMAL(5,2),
salary DECIMAL(10,2),
satisfaction\_score DECIMAL(3,2),
FOREIGN KEY(department\_id) REFERENCES department\_dim(department\_id),
FOREIGN KEY(work\_mode\_id) REFERENCES work\_mode\_dim(work\_mode\_id),
FOREIGN KEY(gender\_id) REFERENCES gender\_dim(gender\_id),
FOREIGN KEY(education\_id) REFERENCES education\_dim(education\_id)
);

\-- Step 3: Populate Dimension Tables (distinct values from employees\_raw)
INSERT IGNORE INTO department\_dim (department\_name)
SELECT DISTINCT department FROM employees\_raw WHERE department IS NOT NULL;

INSERT IGNORE INTO work\_mode\_dim (work\_mode\_name)
SELECT DISTINCT work\_mode FROM employees\_raw WHERE work\_mode IS NOT NULL;

INSERT IGNORE INTO gender\_dim (gender\_name)
SELECT DISTINCT gender FROM employees\_raw WHERE gender IS NOT NULL;

INSERT IGNORE INTO education\_dim (education\_name)
SELECT DISTINCT education\_level FROM employees\_raw WHERE education\_level IS NOT NULL;

\-- Step 4: Populate Fact Table (all rows via JOIN lookups)
INSERT INTO fact\_employee\_performance
(employee\_id, department\_id, work\_mode\_id, gender\_id, education\_id,
experience\_years, salary, satisfaction\_score)
SELECT
er.employee\_id, dd.department\_id, wd.work\_mode\_id, gd.gender\_id, ed.education\_id,
er.experience\_years, er.salary, er.satisfaction\_score
FROM employees\_raw er
LEFT JOIN department\_dim dd ON er.department = dd.department\_name
LEFT JOIN work\_mode\_dim wd ON er.work\_mode = wd.work\_mode\_name
LEFT JOIN gender\_dim gd ON er.gender = gd.gender\_name
LEFT JOIN education\_dim ed ON er.education\_level = ed.education\_name;

\-- Step 5: Verify
SELECT COUNT(\*) FROM fact\_employee\_performance;

SELECT dd.department\_name, AVG(f.salary) AS avg\_salary, COUNT(\*) AS employee\_count
FROM fact\_employee\_performance f
JOIN department\_dim dd ON f.department\_id = dd.department\_id
GROUP BY dd.department\_name
ORDER BY avg\_salary DESC;



**Analytics Queries**

\-- Total employees
select count(\*) as total\_employees from fact\_employee\_performance;

\-- Average salary by department
select dd.department\_name, avg(f.salary) as avg\_salary, count(\*) as employee\_count
from fact\_employee\_performance f
join department\_dim dd on f.department\_id = dd.department\_id
group by dd.department\_name
order by avg\_salary desc;

\-- Average satisfaction by work mode
select wd.work\_mode\_name, avg(f.satisfaction\_score) as avg\_satisfaction
from fact\_employee\_performance f
join work\_mode\_dim wd on f.work\_mode\_id = wd.work\_mode\_id
group by wd.work\_mode\_name
order by avg\_satisfaction desc;

\-- Experience vs salary buckets
select
case
when experience\_years < 5 then 'Junior (<5 yrs)'
when experience\_years between 5 and 10 then 'Mid (5-10 yrs)'
else 'Senior (>10 yrs)'
end as experience\_bucket,
avg(salary) as avg\_salary,
count(\*) as employee\_count
from fact\_employee\_performance
group by experience\_bucket
order by avg\_salary desc;

\-- Salary by gender
select g.gender\_name, avg(f.salary) as avg\_salary, count(\*) as employee\_count
from fact\_employee\_performance f
join gender\_dim g on f.gender\_id = g.gender\_id
group by g.gender\_name;

\-- Salary by education level
select ed.education\_name, avg(f.salary) as avg\_salary
from fact\_employee\_performance f
join education\_dim ed on f.education\_id = ed.education\_id
group by ed.education\_name
order by avg\_salary desc;

\-- Top paid department per work mode combo
select dd.department\_name, wd.work\_mode\_name, avg(f.salary) as avg\_salary
from fact\_employee\_performance f
join department\_dim dd on f.department\_id = dd.department\_id
join work\_mode\_dim wd on f.work\_mode\_id = wd.work\_mode\_id
group by dd.department\_name, wd.work\_mode\_name
order by avg\_salary desc
limit 5;



DROP DATABASE IF EXISTS employee\_db;

DROP TABLE IF EXISTS employees\_raw;

