import sqlite3 as sql
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def initDB():
    conn = sql.connect('database.db')
    print( "Opened database successfully")   
    
    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, addr TEXT, city TEXT, pin TEXT)')
    print ("Table created successfully")
    conn.close()





def get_unique_subcategories(rows, category):
    displayed_subcategories = set()
    unique_subcategories = []
    for row in rows:
        if row['productCategory'] == category and row['productSubCategory'] not in displayed_subcategories:
            displayed_subcategories.add(row['productSubCategory'])
            unique_subcategories.append(row['productSubCategory'])
    return unique_subcategories




@app.route('/')
def home():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("""SELECT * from PRODUCTS """)
    rows = cur.fetchall()
 

    unique_categories = set(row['productCategory'] for row in rows)

    subcategories_counters = {}
    for row in rows:
        category = row['productCategory']
        subcategory = row['productSubCategory']
        if category not in subcategories_counters:
            subcategories_counters[category] = {}
        if subcategory not in subcategories_counters[category]:
            subcategories_counters[category][subcategory] = 1
        else:
            subcategories_counters[category][subcategory] += 1

    return render_template(
        'home.html',
        rows=rows,
        unique_categories=unique_categories,
        subcategories_counters=subcategories_counters,
        get_unique_subcategories=get_unique_subcategories
    )









@app.route('/details/<string:product_no>')
def details(product_no):
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT * FROM PRODUCTS WHERE productNo = ?", (product_no,))
    row = cur.fetchone()

    rows = dict(row)
    

    return render_template('details.html', rows=rows)






@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_key = request.form.get('searchKey', '')
    else:
        search_key = request.args.get('searchKey', '')
        
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT * FROM PRODUCTS WHERE productName LIKE ?", ('%' + search_key + '%',))
    rows = cur.fetchall()
    
    unique_categories = set(row['productCategory'] for row in rows)

    subcategories_counters = {}
    for row in rows:
        category = row['productCategory']
        subcategory = row['productSubCategory']
        if category not in subcategories_counters:
            subcategories_counters[category] = {}
        if subcategory not in subcategories_counters[category]:
            subcategories_counters[category][subcategory] = 1
        else:
            subcategories_counters[category][subcategory] += 1

    return render_template(
        'search.html',
        rows=rows,
        unique_categories=unique_categories,
        subcategories_counters=subcategories_counters,
        get_unique_subcategories=get_unique_subcategories,
        search_key=search_key
    )





@app.route('/search/<string:categoryKey>')
def searchCategory(categoryKey):

    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    
    cur.execute("SELECT * FROM PRODUCTS WHERE productSubCategory LIKE ? OR productCategory LIKE ?", ( categoryKey , categoryKey))

    rows = cur.fetchall()
    
    unique_categories = set(row['productCategory'] for row in rows)

    subcategories_counters = {}
    for row in rows:
        category = row['productCategory']
        subcategory = row['productSubCategory']
        if category not in subcategories_counters:
            subcategories_counters[category] = {}
        if subcategory not in subcategories_counters[category]:
            subcategories_counters[category][subcategory] = 1
        else:
            subcategories_counters[category][subcategory] += 1

    return render_template(
        'search.html',
        rows=rows,
        unique_categories=unique_categories,
        subcategories_counters=subcategories_counters,
        get_unique_subcategories=get_unique_subcategories,
        search_key=""
    )








if __name__ == '__main__':
    initDB()
    app.run(debug=True)