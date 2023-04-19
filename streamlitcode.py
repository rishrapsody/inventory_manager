import streamlit as st
import sqlite3
import barcode
from barcode import Code128
from barcode.writer import ImageWriter
from prettytable import PrettyTable
import csv
import pandas as pd
import os
import time

# Create an SQL database connection
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Create a table to store product information
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        product_type TEXT NOT NULL,
        product_size TEXT NOT NULL,
        product_quantity TEXT NOT NULL,
        price REAL NOT NULL,
        barcode TEXT NOT NULL
    )
''')
conn.commit()


def delete_product(product_id):
    # Delete product from the database and associated barcode image
    try:
        c.execute("SELECT barcode FROM products WHERE id=?", (product_id,))
        barcode_path = c.fetchone()[0]
        print(barcode_path)
        c.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        os.remove("{}.png".format(barcode_path))
        st.success("Product deleted successfully!")
    except Exception as e:
        st.write("Error while performing Delete operation. Please contact the Admin")
        st.write("Error: {}".format(e))
        pass

# Streamlit app
def generate_barcode(name, product_type,product_size,product_quantity,price, barcode_path):
    # Generate a unique barcode
    data = "{}-{}-{}-{}".format(name,product_type,product_quantity,product_size)
    barcode.generate('Code128', data, output=barcode_path, writer=ImageWriter(),text="{}+{}".format(name,product_type))

def export_csv(products):
    # Export product information as CSV
    try:
        with open('products.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Type","Size", "Quantity","Price"])
            for product in products:
                writer.writerow([product[1], product[2], product[3],product[4],product[5]])
        st.success("Product data exported as CSV!")
    except Exception as e:
        print(e)
        st.write("Eror while exporting data to csv")
        st.write("Error: {}".format(e))

@st.cache_data(experimental_allow_widgets=True)
def main():
    st.title("Inventory Manager")
    navigation = st.sidebar.radio("Go to", ('Add Product', 'View Products','Delete Product'))


    if navigation == 'Add Product':
        st.subheader("Add Product")
        # Input form for product information
        school_name = st.text_input("School Name")
        product_type = st.selectbox("Type",options=['Pant','Shirt','TShirt'])
        product_size = st.number_input("Size",min_value=1,step=1)
        product_quantity = st.number_input("Quantity",min_value=1,step=1)
        product_price = st.number_input("Product Price", min_value=1, step=1)
        
        try:
            add_product = st.button("Add Product")
            if add_product:
                try:
                    if school_name and float(product_size) and int(product_quantity) and float(product_price):
                        # Generate a unique barcode and store product information in the database
                        barcode_path = f'barcodes/{school_name}'
                        generate_barcode(school_name, product_type,product_size,product_quantity,product_price, barcode_path)
                        c.execute("INSERT INTO products (name, product_type,product_size,product_quantity,price, barcode) VALUES (?, ?, ?, ?, ?, ?)", (school_name, product_type,product_size,product_quantity,product_price, barcode_path))
                        conn.commit()
                        st.success("Product added successfully!")
                        st.image("{}.png".format(barcode_path))
                except Exception as e:
                    st.write("Product Size/Qty/Price can only be number/float")
                    st.write("Error: {}".format(e))
                    pass

        except Exception as e:
            print(e)
            st.write("Eror processing Product Inputs")
            st.write("Error: {}".format(e))
    
    elif navigation == 'View Products':
        st.subheader("View Products")
        # Query the database and display product information in a pretty table format
        try:
            c.execute("SELECT * FROM products")
            products = c.fetchall()
        except Exception as e:
            st.write("Error while fetching DB info")
        df = pd.DataFrame(products, columns=[col[0] for col in c.description])
        st.table(df)
        st.write("")
    
        if st.button("Export CSV"):
            export_csv(products)
    
    elif navigation == 'Delete Product':
        product_id = st.text_input("Enter Product ID to delete")
        if st.button("Delete"):
            delete_product(product_id)
    
    
    conn.close()




if __name__ == "__main__":
    if not os.path.exists("barcodes"):
        os.makedirs("barcodes")
    main()
