from database import get_db
from app import app
from flask import request, redirect, url_for, render_template
from waitress import serve


@app.route("/")
def root():
    return redirect(url_for("main_menu"))


@app.route("/main_menu")
def main_menu():
    return render_template("main_menu.html")


@app.route("/view_employees")
def view_employees():
    db = get_db()
    cursor = db.execute("select * from employees")
    employees = cursor.fetchall()

    return render_template("view_employees.html", employees=employees)


@app.route("/add_an_employee", methods=["GET", "POST"])
def add_an_employee():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "insert into employees (last_name, first_name, address_line_1, address_line_2, city_name, state_name, zip_code,\
                social_security_number, number_of_withholdings, salary) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
                request.form["last_name"], request.form["first_name"], request.form["address_line_1"],
                request.form["address_line_2"], request.form["city_name"], request.form["state_name"],
                request.form["zip_code"], request.form["social_security_number"],
                request.form["number_of_withholdings"], request.form["salary"]
            ])
        db.commit()
        return redirect(url_for("view_employees"))

    elif request.method == "GET":
        return render_template("add_an_employee.html")


@app.route("/view_customers")
def view_customers():
    db = get_db()
    cursor = db.execute("select * from customers")
    customers = cursor.fetchall()

    return render_template("view_customers.html", customers=customers)


@app.route("/add_a_customer", methods=["GET", "POST"])
def add_a_customer():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "insert into customers (company_name, last_name, first_name, address_line_1, address_line_2,\
                city_name, state_name, zip_code, price) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", [
                request.form["company_name"], request.form["last_name"], request.form["first_name"],
                request.form["address_line_1"], request.form["address_line_2"], request.form["city_name"],
                request.form["state_name"], request.form["zip_code"], request.form["price"]
            ])
        db.commit()
        return redirect(url_for("view_customers"))

    elif request.method == "GET":
        return render_template("add_a_customer.html")


@app.route("/view_vendors")
def view_vendors():
    db = get_db()
    cursor = db.execute("select * from vendors")
    vendors = cursor.fetchall()

    return render_template("view_vendors.html", vendors=vendors)


@app.route("/add_a_vendor", methods=["GET", "POST"])
def add_a_vendor():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "insert into vendors (company_name, part, price_per_unit, address_line_1, address_line_2,\
                city_name, state_name, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?)", [
                request.form["company_name"], request.form["part"], request.form["price_per_unit"],
                request.form["address_line_1"], request.form["address_line_2"], request.form["city_name"],
                request.form["state_name"], request.form["zip_code"]
            ])
        db.execute("insert into inventory_buy (part, price_per_unit, quantity, total_value) values (?, ?, ?, ?)",
                   [request.form["part"], request.form["price_per_unit"], "0", "0"])
        db.commit()
        return redirect(url_for("view_vendors"))

    elif request.method == "GET":
        return render_template("add_a_vendor.html")


@app.route("/pay_an_employee", methods=["GET", "POST"])
def pay_an_employee():
    db = get_db()

    if request.method == "POST":
        # cursor = db.execute("select salary from employees where last_name = ?", [request.form["employee_last_name"]])
        # employee = cursor.fetchone()
        # salary = employee["salary"]
        salary = "12500"

        db.execute("insert into payroll_events (date_paid, employee, disbursement, withholding) values (?, ?, ?, ?)",
                   [request.form["date"], request.form["employee_last_name"], salary, str(4436.45)])

        cursor = db.execute("select cash from balance_sheet")
        before_cash = cursor.fetchone()["cash"]
        db.execute("update balance_sheet set cash = ?", [str(float(before_cash) - 8063.55)])

        cursor = db.execute("select payroll, payroll_withholding from income_statement")
        income_statement = cursor.fetchone()
        before_payroll = income_statement["payroll"]
        before_payroll_withholding = income_statement["payroll_withholding"]
        db.execute("update income_statement set payroll = ?, payroll_withholding = ?",
                   [str(float(before_payroll) + 8063.55),
                    str(float(before_payroll_withholding) + 4436.45)])

        db.commit()
        return redirect(url_for("main_menu"))

    elif request.method == "GET":
        cursor = db.execute("select last_name from employees")
        employees = cursor.fetchall()
        return render_template("pay_an_employee.html", employees=employees)


@app.route("/view_payroll_events")
def view_payroll_events():
    db = get_db()
    cursor = db.execute("select * from payroll_events")
    payroll_events = cursor.fetchall()

    return render_template("view_payroll_events.html", payroll_events=payroll_events)


@app.route("/create_an_invoice", methods=["GET", "POST"])
def create_an_invoice():
    db = get_db()
    cursor = db.execute("select complete_units from inventory_sell")
    inventory_sell = cursor.fetchone()

    if request.method == "POST":
        db.execute(
            "insert into invoices (invoice_date, customer, quantity, price_per_unit, total_value) values (?, ?, ?, ?, ?)",
            [
                request.form["date"], request.form["customer_company_name"], request.form["number_of_units_to_invoice"],
                "2.5",
                str(int(request.form["number_of_units_to_invoice"]) * 2.5)
            ])

        db.execute("update inventory_sell set complete_units = ?",
                   [str(int(inventory_sell["complete_units"]) - int(request.form["number_of_units_to_invoice"]))])

        cursor = db.execute("select accounts_receivable, inventory from balance_sheet")
        balance_sheet = cursor.fetchone()
        before_accounts_receivable = balance_sheet["accounts_receivable"]
        before_inventory = balance_sheet["inventory"]

        db.execute("update balance_sheet set accounts_receivable = ?, inventory = ?",
                   [str(float(before_accounts_receivable) + int(request.form["number_of_units_to_invoice"]) * 2.5),
                    str(float(before_inventory) - int(request.form["number_of_units_to_invoice"]) * 0.57)])

        cursor = db.execute("select sales, cost_of_goods from income_statement")
        income_statement = cursor.fetchone()
        before_sales = income_statement["sales"]
        before_cost_of_goods = income_statement["cost_of_goods"]
        db.execute("update income_statement set sales = ?, cost_of_goods = ?",
                   [str(float(before_sales) + int(request.form["number_of_units_to_invoice"]) * 2.5),
                    str(float(before_cost_of_goods) + int(request.form["number_of_units_to_invoice"]) * 0.57)])

        db.commit()
        return redirect(url_for("main_menu"))

    elif request.method == "GET":
        cursor = db.execute("select company_name from customers")
        customers = cursor.fetchall()
        return render_template("create_an_invoice.html", customers=customers, inventory_sell=inventory_sell)


@app.route("/view_invoices")
def view_invoices():
    db = get_db()
    cursor = db.execute("select * from invoices")
    invoices = cursor.fetchall()

    # TODO: Show total sales and cost of goods

    return render_template("view_invoices.html", invoices=invoices)


@app.route("/create_a_purchase_order", methods=["GET", "POST"])
def create_a_purchase_order():
    db = get_db()

    if request.method == "POST":
        cursor = db.execute("select company_name, part, price_per_unit from vendors where part = ?",
                            [request.form["vendor_part"]])
        vendor = cursor.fetchone()

        db.execute(
            "insert into purchase_orders (purchase_order_date, supplier, part, quantity, price_per_part, total_value)\
                values (?, ?, ?, ?, ?, ?)", [
                request.form["date"], vendor["company_name"], vendor["part"], request.form["quantity"],
                vendor["price_per_unit"],
                str(int(request.form["quantity"]) * float(vendor["price_per_unit"]))
            ])

        cursor = db.execute("select quantity from inventory_buy where part = ?", [vendor["part"]])
        inventory_buy = cursor.fetchone()
        quantity_before_purchase = inventory_buy["quantity"]
        db.execute("update inventory_buy set quantity = ?, total_value = ? where part = ?", [
            str(int(quantity_before_purchase) + int(request.form["quantity"])),
            str((int(quantity_before_purchase) + int(request.form["quantity"])) * float(vendor["price_per_unit"])),
            vendor["part"]
        ])

        cursor = db.execute("select accounts_payable, inventory from balance_sheet")
        balance_sheet = cursor.fetchone()
        before_accounts_payable = balance_sheet["accounts_payable"]
        before_inventory = balance_sheet["inventory"]
        db.execute("update balance_sheet set accounts_payable = ?, inventory = ?",
                   [str(float(before_accounts_payable) + int(request.form["quantity"]) * float(vendor["price_per_unit"])),
                    str(float(before_inventory) + int(request.form["quantity"]) * float(vendor["price_per_unit"]))])

        db.commit()
        return redirect(url_for("main_menu"))

    elif request.method == "GET":
        cursor = db.execute("select company_name, part, price_per_unit from vendors")
        vendors = cursor.fetchall()
        return render_template("create_a_purchase_order.html", vendors=vendors)


@app.route("/view_purchase_orders")
def view_purchase_orders():
    db = get_db()
    cursor = db.execute("select * from purchase_orders")
    purchase_orders = cursor.fetchall()

    return render_template("view_purchase_orders.html", purchase_orders=purchase_orders)


@app.route("/view_inventory")
def view_inventory():
    db = get_db()
    cursor = db.execute("select * from inventory_buy")
    inventory_buy = cursor.fetchall()
    cursor = db.execute("select * from inventory_sell")
    inventory_sell = cursor.fetchone()

    # TODO: Add reorder, units can be built, total value in stock

    return render_template("view_inventory.html", inventory_buy=inventory_buy, inventory_sell=inventory_sell)


@app.route("/view_balance_sheet")
def view_balance_sheet():
    db = get_db()
    cursor = db.execute("select * from balance_sheet")
    balance_sheet = cursor.fetchone()

    total_current_assets = float(balance_sheet["cash"]) + float(balance_sheet["accounts_receivable"]) + float(
        balance_sheet["inventory"])
    total_fixed_assets = float(balance_sheet["land_and_buildings"]) + float(balance_sheet["equipment"])\
        + float(balance_sheet["furniture_and_fixtures"])
    total_assets = total_current_assets + total_fixed_assets

    total_current_liabilities = float(balance_sheet["accounts_payable"]) + float(balance_sheet["notes_payable"])\
        + float(balance_sheet["accruals"])
    total_long_term_debt = float(balance_sheet["mortgage"])
    total_liabilities = total_current_liabilities + total_long_term_debt
    net_worth = total_assets - total_liabilities

    return render_template(
        "view_balance_sheet.html",
        balance_sheet=balance_sheet,
        total_current_assets=total_current_assets,
        total_fixed_assets=total_fixed_assets,
        total_assets=total_assets,
        total_current_liabilities=total_current_liabilities,
        total_long_term_debt=total_long_term_debt,
        total_liabilities=total_liabilities,
        net_worth=net_worth)


@app.route("/view_income_statement")
def view_income_statement():
    db = get_db()
    cursor = db.execute("select * from income_statement")
    income_statement = cursor.fetchone()

    gross_profit = float(income_statement["sales"]) - float(income_statement["cost_of_goods"])
    total_expenses = float(income_statement["payroll"]) + float(income_statement["bills"]) + float(
        income_statement["annual_expenses"])
    operating_income = gross_profit - total_expenses
    income_taxes = operating_income * 0.2
    net_income = operating_income - income_taxes

    return render_template(
        "view_income_statement.html",
        income_statement=income_statement,
        gross_profit=gross_profit,
        total_expenses=total_expenses,
        operating_income=operating_income,
        income_taxes=income_taxes,
        net_income=net_income)


if __name__ == "__main__":
    serve(app, listen="127.0.0.1:80")
