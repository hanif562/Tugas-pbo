import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Fungsi untuk membuat koneksi ke database MySQL
def create_connection():
    return mysql.connector.connect(
        host="localhost",  # Ganti dengan host MySQL Anda
        user="root",       # Ganti dengan username MySQL Anda
        password="",       # Ganti dengan password MySQL Anda
        database="kasir"  # Ganti dengan nama database Anda
    )

# Fungsi untuk menambah produk baru
def add_product_window():
    add_product_win = tk.Toplevel()
    add_product_win.title("Tambah Produk")
    add_product_win.geometry("400x350")
    add_product_win.config(bg="#F0F0F0")
    
    # Frame untuk Form Input
    form_frame = tk.Frame(add_product_win, bg="#F0F0F0")
    form_frame.pack(pady=20)

    # Label dan Entry untuk Product ID
    tk.Label(form_frame, text="Product ID", font=("Arial", 12), bg="#F0F0F0").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_product_id = tk.Entry(form_frame, font=("Arial", 12), width=25)
    entry_product_id.grid(row=0, column=1, padx=10, pady=10)

    # Label dan Entry untuk Product Name
    tk.Label(form_frame, text="Product Name", font=("Arial", 12), bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_product_name = tk.Entry(form_frame, font=("Arial", 12), width=25)
    entry_product_name.grid(row=1, column=1, padx=10, pady=10)

    # Label dan Entry untuk Price
    tk.Label(form_frame, text="Price", font=("Arial", 12), bg="#F0F0F0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_price = tk.Entry(form_frame, font=("Arial", 12), width=25)
    entry_price.grid(row=2, column=1, padx=10, pady=10)

    # Label dan Entry untuk Stock
    tk.Label(form_frame, text="Stock", font=("Arial", 12), bg="#F0F0F0").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_stock = tk.Entry(form_frame, font=("Arial", 12), width=25)
    entry_stock.grid(row=3, column=1, padx=10, pady=10)

    # Fungsi untuk menyimpan produk
    def save_product():
        product_id = entry_product_id.get()
        product_name = entry_product_name.get()
        price = entry_price.get()
        stock = entry_stock.get()

        if product_id and product_name and price and stock:
            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO products (product_id, product_name, price, stock) VALUES (%s, %s, %s, %s)",
                               (product_id, product_name, float(price), int(stock)))
                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Success", "Product added successfully!")
                add_product_win.destroy()  # Close window after saving product
                show_products()  # Update the product list
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    # Button untuk menyimpan produk
    btn_save_product = tk.Button(add_product_win, text="Save Product", font=("Arial", 12), bg="#4CAF50", fg="white", command=save_product)
    btn_save_product.pack(pady=10)

    # Button untuk membatalkan
    btn_cancel = tk.Button(add_product_win, text="Cancel", font=("Arial", 12), bg="#FF5722", fg="white", command=add_product_win.destroy)
    btn_cancel.pack(pady=10)

# Fungsi untuk menampilkan semua produk
def show_products():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    # Clear existing data in the treeview
    for row in treeview_products.get_children():
        treeview_products.delete(row)
    
    # Insert new data into the Treeview
    for product in products:
        treeview_products.insert("", "end", values=(product[0], product[1], product[2], product[3]))

    cursor.close()
    connection.close()

# Fungsi untuk mengupdate data produk
def update_product_window():
    selected_item = treeview_products.selection()
    if selected_item:
        item = treeview_products.item(selected_item)
        product_info = item["values"]
        product_id = product_info[0]
        product_name = product_info[1]
        price = product_info[2]
        stock = product_info[3]

        update_win = tk.Toplevel()
        update_win.title("Update Product")
        update_win.geometry("400x350")
        update_win.config(bg="#F0F0F0")

        # Frame untuk Form Input
        form_frame = tk.Frame(update_win, bg="#F0F0F0")
        form_frame.pack(pady=20)

        # Label dan Entry untuk Product ID
        tk.Label(form_frame, text="Product ID", font=("Arial", 12), bg="#F0F0F0").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_product_id = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_product_id.insert(0, product_id)
        entry_product_id.config(state="readonly")
        entry_product_id.grid(row=0, column=1, padx=10, pady=10)

        # Label dan Entry untuk Product Name
        tk.Label(form_frame, text="Product Name", font=("Arial", 12), bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_product_name = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_product_name.insert(0, product_name)
        entry_product_name.grid(row=1, column=1, padx=10, pady=10)

        # Label dan Entry untuk Price
        tk.Label(form_frame, text="Price", font=("Arial", 12), bg="#F0F0F0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_price = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_price.insert(0, price)
        entry_price.grid(row=2, column=1, padx=10, pady=10)

        # Label dan Entry untuk Stock
        tk.Label(form_frame, text="Stock", font=("Arial", 12), bg="#F0F0F0").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        entry_stock = tk.Entry(form_frame, font=("Arial", 12), width=25)
        entry_stock.insert(0, stock)
        entry_stock.grid(row=3, column=1, padx=10, pady=10)

        # Fungsi untuk menyimpan update produk
        def save_update_product():
            updated_name = entry_product_name.get()
            updated_price = entry_price.get()
            updated_stock = entry_stock.get()

            if updated_name and updated_price and updated_stock:
                try:
                    connection = create_connection()
                    cursor = connection.cursor()
                    cursor.execute("UPDATE products SET product_name = %s, price = %s, stock = %s WHERE product_id = %s",
                                   (updated_name, float(updated_price), int(updated_stock), product_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Success", "Product updated successfully!")
                    update_win.destroy()
                    show_products()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        # Button untuk update produk
        btn_save_update_product = tk.Button(update_win, text="Update Product", font=("Arial", 12), bg="#FF9800", fg="white", command=save_update_product)
        btn_save_update_product.pack(pady=10)

        # Button untuk membatalkan
        btn_cancel = tk.Button(update_win, text="Cancel", font=("Arial", 12), bg="#FF5722", fg="white", command=update_win.destroy)
        btn_cancel.pack(pady=10)

# Fungsi untuk menghapus produk
def delete_product():
    selected_item = treeview_products.selection()
    if selected_item:
        item = treeview_products.item(selected_item)
        product_id = item["values"][0]

        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", f"Product with ID {product_id} deleted successfully!")
            show_products()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    else:
        messagebox.showwarning("Selection Error", "Please select a product to delete.")

# Fungsi utama untuk membuka jendela utama
def open_main_window():
    global treeview_products

    main_window = tk.Tk()
    main_window.title("Kasir Inventory")
    main_window.geometry("700x500")
    main_window.config(bg="#F0F0F0")

    # Frame untuk tombol aksi
    action_frame = tk.Frame(main_window, bg="#F0F0F0")
    action_frame.pack(pady=10)

    # Button untuk tambah produk
    btn_add_product = tk.Button(action_frame, text="Add Product", font=("Arial", 12), bg="#4CAF50", fg="white", command=add_product_window, width=15)
    btn_add_product.grid(row=0, column=0, padx=10, pady=10)

    # Button untuk update produk
    btn_update_product = tk.Button(action_frame, text="Update Product", font=("Arial", 12), bg="#FF9800", fg="white", command=update_product_window, width=15)
    btn_update_product.grid(row=0, column=1, padx=10, pady=10)

    # Button untuk delete produk
    btn_delete_product = tk.Button(action_frame, text="Delete Product", font=("Arial", 12), bg="#F44336", fg="white", command=delete_product, width=15)
    btn_delete_product.grid(row=0, column=2, padx=10, pady=10)

    # Treeview untuk menampilkan produk dalam tabel
    treeview_products = ttk.Treeview(main_window, columns=("Product ID", "Product Name", "Price", "Stock"), show="headings")
    treeview_products.heading("Product ID", text="Product ID")
    treeview_products.heading("Product Name", text="Product Name")
    treeview_products.heading("Price", text="Price")
    treeview_products.heading("Stock", text="Stock")

    treeview_products.column("Product ID", width=100)
    treeview_products.column("Product Name", width=200)
    treeview_products.column("Price", width=100)
    treeview_products.column("Stock", width=100)

    treeview_products.pack(pady=20, padx=20)

    # Tampilkan produk pada treeview
    show_products()

    main_window.mainloop()

if __name__ == "__main__":
    open_main_window()
