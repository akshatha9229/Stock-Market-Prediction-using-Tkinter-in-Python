import tkinter as tk
from tkinter import messagebox
import sqlite3

# -------- DATABASE --------
conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
conn.commit()

# -------- STOCK DATA --------
data = {
    "APPLE": [150, 155, 160, 165],
    "TESLA": [700, 720, 750, 780],
    "GOOGLE": [2700, 2750, 2800, 2850],
    "AMAZON": [3300, 3350, 3400, 3450]
}

# -------- FUNCTIONS --------
def register():
    u, p = user.get(), pwd.get()
    if u and p:
        try:
            cur.execute("INSERT INTO users VALUES(?, ?)", (u, p))
            conn.commit()
            messagebox.showinfo("Success", "✅ Register Successful! 🎉")
        except:
            messagebox.showerror("Error", "User already exists")
    else:
        messagebox.showwarning("Error", "Fill all fields")

def login():
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user.get(), pwd.get()))
    if cur.fetchone():
        open_prediction()
    else:
        messagebox.showerror("Error", "Invalid Login")

# -------- NEW SCREEN --------
def open_prediction():
    root.destroy()  # close login window
    app = tk.Tk()
    app.title("Stock Predictor")
    app.geometry("400x400")
    app.config(bg="#B0E0E6")

    tk.Label(app, text="Stock Predictor",
             font=("Arial", 18, "bold"),
             bg="#B0E0E6", fg="#1C355E").pack(pady=20)

    tk.Label(app, text="Enter Company Name",
             bg="#B0E0E6", fg="black",
             font=("Arial", 10, "bold")).pack(pady=10)

    comp = tk.Entry(app, font=("Arial", 12), justify="center")
    comp.pack(pady=10, ipady=5)

    result = tk.Label(app, text="", font=("Arial", 12), fg="black")
    result.pack(pady=20)

    def predict():
        name = comp.get().upper()
        if name in data:
            prices = data[name]
            avg = sum([prices[i] - prices[i-1] for i in range(1, len(prices))]) / (len(prices)-1)
            result.config(text=f"Predicted Price: {round(prices[-1] + avg, 2)}")
        else:
            result.config(text="Company not found ❌")

    tk.Button(app, text="Predict",
              bg="#B0E0E6", fg="#1C355E",
              font=("Arial", 14, "bold"),
              command=predict).pack(pady=10, ipadx=10, ipady=10)

    app.mainloop()

# -------- LOGIN UI --------
root = tk.Tk()
root.title("Login")
root.geometry("350x400")
root.config(bg="#B0E0E6")

tk.Label(root, text="📈 Stock Predictor",
         font=("Arial", 18, "bold"),
         bg="#B0E0E6", fg="#1C355E").pack(pady=20)

tk.Label(root, text="Username", bg="#B0E0E6", fg="#264653").pack()
user = tk.Entry(root)
user.pack(pady=5)

tk.Label(root, text="Password", bg="#B0E0E6", fg="#264653").pack()
pwd = tk.Entry(root, show="*")
pwd.pack(pady=5)

tk.Button(root, text="🔑 Login",
          bg="#B0E0E6", fg="#1C355E",
          font=("Arial", 10, "bold"),
          command=login).pack(pady=10, ipadx=10)

tk.Label(root, text="🆕 If You Are A New User",
         font=("Arial", 10, "bold"),
         bg="#B0E0E6", fg="white").pack(pady=5)

tk.Button(root, text="Register",
          bg="#B0E0E6", fg="#1C355E",
          font=("Arial", 10, "bold"),
          command=register).pack(pady=5, ipadx=10)

root.mainloop()
