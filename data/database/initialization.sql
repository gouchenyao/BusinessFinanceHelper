drop table if exists balance_sheet;

CREATE TABLE balance_sheet
(
  cash text,
  accounts_receivable text,
  inventory text,
  land_and_buildings text,
  equipment text,
  furniture_and_fixtures text,
  accounts_payable text,
  notes_payable text,
  accruals text,
  mortgage text
);


drop table if exists income_statement;

CREATE TABLE income_statement
(
  sales text,
  cost_of_goods text,
  payroll text,
  payroll_withholding text,
  bills text,
  annual_expenses text,
  other_income text
);


drop table if exists employees;

CREATE TABLE employees
(
  last_name text not null,
  first_name text not null,
  address_line_1 text not null,
  address_line_2 text,
  city_name text not null,
  state_name text not null,
  zip_code text not null,
  social_security_number text not null primary key,
  number_of_withholdings text not null,
  salary text not null
);


drop table if exists customers;

CREATE TABLE customers
(
  company_name text not null,
  last_name text,
  first_name text,
  address_line_1 text,
  address_line_2 text,
  city_name text,
  state_name text,
  zip_code text,
  price text not null,
  primary key(company_name, last_name, first_name)
);


drop table if exists vendors;

CREATE TABLE vendors
(
  company_name text not null,
  part text not null,
  price_per_unit text not null,
  address_line_1 text,
  address_line_2 text,
  city_name text,
  state_name text,
  zip_code text,
  primary key(company_name, part)
);


drop table if exists payroll_events;

CREATE TABLE payroll_events
(
  date_paid text not null,
  employee text not null,
  disbursement text not null,
  withholding text not null
);


drop table if exists invoices;

CREATE TABLE invoices
(
  invoice_number INTEGER PRIMARY KEY,
  invoice_date text not null,
  customer text not null,
  quantity text not null,
  price_per_unit text not null,
  total_value text not null
);


drop table if exists purchase_orders;

CREATE TABLE purchase_orders
(
  purchase_order_number INTEGER PRIMARY KEY,
  purchase_order_date text not null,
  supplier text not null,
  part text not null,
  quantity text not null,
  price_per_part text not null,
  total_value text not null
);


drop table if exists inventory_buy;

CREATE TABLE inventory_buy
(
  part text not null,
  price_per_unit text not null,
  quantity text not null,
  total_value text not null
);


drop table if exists inventory_sell;

CREATE TABLE inventory_sell
(
  can_be_built_units text not null,
  complete_units text not null,
  total_value text not null
);