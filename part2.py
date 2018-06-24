# Full Name: Alex Lu
# UMID     : 54523810
# Uniqname : alexjlu

import sys
import sqlite3

# write your code here
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>



def fetch_customers(c):
    c.execute("SELECT Id, CompanyName FROM Customer")
    all_rows = c.fetchall()

    print("ID\tCustomer Name")
    for row in all_rows:
        print("%s\t%s" % (row[0], row[1]))


def fetch_employee(c):
    c.execute("SELECT Id, LastName, FirstName FROM Employee")
    all_rows = c.fetchall()

    print("ID\tEmployee Name")
    for row in all_rows:
        print("%s\t%s %s" % (row[0], row[2], row[1]))


def fetch_order_customer(c, customer):
    command = "SELECT Orderdate FROM 'Order' WHERE CustomerId = '" + customer + "'"
    print(command)
    c.execute(command)
    all_rows = c.fetchall()

    print("Order dates")
    for row in all_rows:
        print("%s" % row[0])


def fetch_order_employee(c, empLastname):
    command = "SELECT Id FROM Employee WHERE LastName='" + empLastname + "'"
    c.execute(command)
    empId = c.fetchall()[0][0]

    command = "SELECT Orderdate FROM 'Order' WHERE EmployeeId=" + str(empId)
    c.execute(command)
    all_rows = c.fetchall()

    print("Order dates")
    for row in all_rows:
        print("%s" % row[0])


if __name__ == '__main__':
    conn = sqlite3.connect('Northwind_small.sqlite')
    c = conn.cursor()

    table = sys.argv[1]
    if table == "customers":
        fetch_customers(c)
    elif table == "employees":
        fetch_employee(c)
    elif table == "orders":
        arg = sys.argv[2]
        if arg.startswith("cust="):
            fetch_order_customer(c, arg[5:])
        elif arg.startswith("emp="):
            fetch_order_employee(c, arg[4:])