import os
import sqlite3

from flask import g
from app import app


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    with app.app_context():
        db = get_db()

        with app.open_resource(os.path.join(app.root_path, 'data', 'database', 'initialization.sql'), mode='r') as f:
            db.cursor().executescript(f.read())

        db.execute(
            'insert into balance_sheet (cash, accounts_receivable, inventory, land_and_buildings, equipment,\
                furniture_and_fixtures, accounts_payable, notes_payable, accruals, mortgage)\
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ["200000", "0", "12360", "0", "0", "0", "0", "0", "0", "0"])

        db.execute(
            'insert into income_statement (sales, cost_of_goods, payroll, payroll_withholding, bills,\
                annual_expenses, other_income) values (?, ?, ?, ?, ?, ?, ?)',
            ["1000000", "228000", "0", "0", "0", "0", "0"])

        db.execute(
            'insert into inventory_sell (can_be_built_units, complete_units, total_value)\
                values (?, ?, ?)', ["0", "4000", "10000"])

        db.execute(
            "insert into employees (last_name, first_name, address_line_1, address_line_2, city_name, state_name, zip_code,\
                social_security_number, number_of_withholdings, salary) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
                "Smith", "John", "111 Front Street", "Apartment 111", "Champaign", "Illinois", "61820", "123-45-6789",
                "0", "12500"
            ])

        db.execute(
            "insert into customers (company_name, last_name, first_name, address_line_1, address_line_2,\
                city_name, state_name, zip_code, price) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ["Amazon", "", "", "", "", "", "", "", "2.5"])

        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)",
            ["", "Wheels", "0.01", "", "", "", "", ""])

        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   ["Wheels", "0.01", "10000", "100"])

        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)",
            ["", "Windshield Glass", "0.05", "", "", "", "", ""])

        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   ["Windshield Glass", "0.05", "10000", "500"])

        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)",
            ["", "Interior", "0.05", "", "", "", "", ""])

        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   ["Interior", "0.05", "1000", "50"])

        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)",
            ["", "Tank", "0.10", "", "", "", "", ""])

        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   ["Tank", "0.10", "10000", "100"])

        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)",
            ["", "Axles", "0.01", "", "", "", "", ""])

        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   ["Axles", "0.01", "10000", "100"])

        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)",
            ["", "Cab", "0.10", "", "", "", "", ""])

        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   ["Cab", "0.10", "10000", "1000"])

        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)",
            ["", "Body", "0.10", "", "", "", "", ""])

        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   ["Body", "0.10", "100", "10"])

        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)",
            ["", "Box", "0.05", "", "", "", "", ""])

        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   ["Box", "0.05", "10000", "500"])

        db.commit()

        print('Initialization of database is completed.')


if __name__ == '__main__':
    init_db()
