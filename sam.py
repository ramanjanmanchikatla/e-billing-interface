
from tkinter import *
from tkinter import simpledialog, messagebox
import os
import datetime
from tkinter import filedialog
from twilio.rest import Client


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("400x300")
        
        # Username and Password
        Label(self.root, text="Login", font=("Arial", 20, "bold")).pack(pady=20)
        self.username = StringVar()
        self.password = StringVar()
        Label(self.root, text="Username", font=("Arial", 12)).pack(pady=5)
        Entry(self.root, textvariable=self.username, font=("Arial", 12), width=25).pack()
        Label(self.root, text="Password", font=("Arial", 12)).pack(pady=5)
        Entry(self.root, textvariable=self.password, font=("Arial", 12), width=25, show="*").pack()
        
        # Login Button
        Button(self.root, text="Login", command=self.check_login, font=("Arial", 12), bg="blue", fg="white", width=15).pack(pady=20)

    def check_login(self):
        # Hardcoded credentials for simplicity
        if self.username.get() == "admin" and self.password.get() == "password":
            self.root.destroy()
            MenuSetupPage()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password!")


class MenuSetupPage:
    def __init__(self):
        self.root = Tk()
        self.root.title("Menu Setup")
        self.root.geometry("400x400")
        
        self.menu_items = {}
        
        Label(self.root, text="Menu Setup", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Add Menu Item Section
        Label(self.root, text="Item Name", font=("Arial", 12)).pack(pady=5)
        self.item_name = StringVar()
        Entry(self.root, textvariable=self.item_name, font=("Arial", 12), width=25).pack()
        
        Label(self.root, text="Price", font=("Arial", 12)).pack(pady=5)
        self.item_price = IntVar()
        Entry(self.root, textvariable=self.item_price, font=("Arial", 12), width=25).pack()
        
        Button(self.root, text="Add Item", command=self.add_menu_item, font=("Arial", 12), bg="green", fg="white", width=15).pack(pady=10)
        
        # Display Menu Items
        self.menu_display = Text(self.root, font=("Arial", 12), width=40, height=10)
        self.menu_display.pack(pady=10)
        
        # Proceed to Billing Interface
        Button(self.root, text="Proceed", command=self.proceed_to_billing, font=("Arial", 12), bg="blue", fg="white", width=15).pack(pady=10)

        self.root.mainloop()

    def add_menu_item(self):
        item_name = self.item_name.get().strip()
        item_price = self.item_price.get()
        
        if not item_name or not item_price:
            messagebox.showerror("Input Error", "Both Item Name and Price are required!")
            return
        
        self.menu_items[item_name] = item_price
        self.menu_display.insert(END, f"{item_name} - {item_price}\n")
        self.item_name.set("")
        self.item_price.set("")

    def proceed_to_billing(self):
        if not self.menu_items:
            messagebox.showerror("Menu Error", "Please add at least one menu item!")
        else:
            self.root.destroy()
            root = Tk()
            BillApp(root, self.menu_items)


class BillApp:
    def __init__(self, root, menu_items):
        self.root = root
        self.root.title("Restaurant Billing System")
        self.root.geometry("1280x720")
        self.menu_items = menu_items  # Menu items dynamically passed
        self.item_vars = {}  # To hold quantity variables for each item
        self.total_all_bill = 0
        self.total_tax = 0
        self.final_bill = 0

        # Variables
        self.c_name = StringVar()
        self.phone = StringVar()
        self.email = StringVar()
        self.bill_no = StringVar()
        self.bill_no.set(str(self.get_today_bill_number()))

        # Customer Details Frame
        F1 = LabelFrame(self.root, text="Customer Details", font=("times new roman", 15, "bold"), fg="gold", bg="black", bd=10, relief=GROOVE)
        F1.place(x=0, y=0, relwidth=1)

        Label(F1, text="Customer Name", bg="black", fg="white", font=("times new roman", 18, "bold")).grid(row=0, column=0, padx=20, pady=5)
        Entry(F1, width=15, textvariable=self.c_name, font="arial 15", bd=7, relief=SUNKEN).grid(row=0, column=1, padx=10, pady=5)

        Label(F1, text="Phone No.", bg="black", fg="white", font=("times new roman", 18, "bold")).grid(row=0, column=2, padx=20, pady=5)
        Entry(F1, width=15, textvariable=self.phone, font="arial 15", bd=7, relief=SUNKEN).grid(row=0, column=3, padx=10, pady=5)

        Label(F1, text="Email Address", bg="black", fg="white", font=("times new roman", 18, "bold")).grid(row=0, column=4, padx=20, pady=5)
        Entry(F1, width=15, textvariable=self.email, font="arial 15", bd=7, relief=SUNKEN).grid(row=0, column=5, padx=10, pady=5)

        Label(F1, text="Bill Number", bg="black", fg="white", font=("times new roman", 18, "bold")).grid(row=1, column=0, padx=20, pady=5)
        Entry(F1, width=15, textvariable=self.bill_no, font="arial 15", bd=7, relief=SUNKEN).grid(row=1, column=1, padx=10, pady=5)

        # Scrollable Menu Frame
        F2 = LabelFrame(self.root, text="Menu", font=("times new roman", 15, "bold"), fg="gold", bg="black", bd=10, relief=GROOVE)
        F2.place(x=5, y=120, width=650, height=380)

        # Create Canvas and Scrollbar
        canvas = Canvas(F2, bg="black", bd=0, highlightthickness=0)
        scrollbar = Scrollbar(F2, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="black")

        # Configure the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Add menu items dynamically
        for i, (item_name, price) in enumerate(self.menu_items.items()):
            Label(scrollable_frame, text=f"{item_name} ({price})", font=("times new roman", 16, "bold"), bg="black", fg="lightgreen").grid(row=i, column=0, padx=10, pady=10, sticky="w")
            qty_var = IntVar()
            Entry(scrollable_frame, width=10, textvariable=qty_var, font="arial 16", bd=7, relief=SUNKEN).grid(row=i, column=1, padx=10, pady=10)
            self.item_vars[item_name] = (price, qty_var)

        # Update the scrollable frame size
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Bill Area
        F3 = Frame(self.root, bd=10, relief=GROOVE)
        F3.place(x=660, y=120, width=400, height=380)
        Label(F3, text="Bill Area", font="arial 15 bold", bd=7, relief=GROOVE).pack(fill=X)
        scroll_y = Scrollbar(F3, orient=VERTICAL)
        self.textarea = Text(F3, yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH, expand=1)

        # Button Frame
        F4 = LabelFrame(self.root, text="Billing Menu", font=("times new roman", 15, "bold"), fg="gold", bg="black", bd=10, relief=GROOVE)
        F4.place(x=0, y=500, relwidth=1, height=200)

        Button(F4, text="Total", command=self.calculate_total, bg="cadetblue", fg="white", bd=7, pady=15, width=10, font="arial 15 bold").grid(row=0, column=0, padx=10, pady=5)
        Button(F4, text="Generate Bill", command=self.generate_bill, bg="cadetblue", fg="white", bd=7, pady=15, width=10, font="arial 15 bold").grid(row=0, column=1, padx=10, pady=5)
        Button(F4, text="Clear", command=self.clear_data, bg="cadetblue", fg="white", bd=7, pady=15, width=10, font="arial 15 bold").grid(row=0, column=2, padx=10, pady=5)
        Button(F4, text="Save", command=self.save_bill, bg="cadetblue", fg="white", bd=7, pady=15, width=10, font="arial 15 bold").grid(row=0, column=3, padx=10, pady=5)
        Button(F4, text="Payment Options", command=self.payment_options, bg="cadetblue", fg="white", bd=7, pady=15, width=15, font="arial 15 bold").grid(row=0, column=4, padx=10, pady=5)
        Button(F4, text="Send Bill via SMS", command=self.send_sms, bg="cadetblue", fg="white", bd=7, pady=15, width=15, font="arial 15 bold").grid(row=0, column=5, padx=10, pady=5)
        self.welcome_bill()

    def get_today_bill_number(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        file_path = f"bill_number_{today}.txt"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                last_number = int(file.read().strip())
        else:
            last_number = 0
        next_number = last_number + 1
        with open(file_path, "w") as file:
            file.write(str(next_number))
        return next_number

    def calculate_total(self):
        self.total_all_bill = 0
        self.total_tax = 0

        for item_name, (price, qty_var) in self.item_vars.items():
            quantity = qty_var.get()
            if quantity > 0:
                self.total_all_bill += price * quantity

        self.total_tax = self.total_all_bill * 0.05  # 5% tax
        self.final_bill = self.total_all_bill + self.total_tax

    def generate_bill(self):
        self.textarea.delete("1.0", END)
        self.textarea.insert(END, f"Customer Name: {self.c_name.get()}\n")
        self.textarea.insert(END, f"Phone: {self.phone.get()}\n")
        self.textarea.insert(END, f"Email: {self.email.get()}\n")
        self.textarea.insert(END, f"Bill Number: {self.bill_no.get()}\n")
        self.textarea.insert(END, "-" * 43 + "\n")
        self.textarea.insert(END, f"{'Item':<25}{'Qty':<10}{'Price':<10}\n")
        self.textarea.insert(END, "-" * 43 + "\n")

        for item_name, (price, qty_var) in self.item_vars.items():
            quantity = qty_var.get()
            if quantity > 0:
                self.textarea.insert(END, f"{item_name:<25}{quantity:<10}{price * quantity:<10}\n")

        self.textarea.insert(END, "-" * 43 + "\n")
        self.textarea.insert(END, f"Subtotal: {self.total_all_bill:.2f}\n")
        self.textarea.insert(END, f"Tax (5%): {self.total_tax:.2f}\n")
        self.textarea.insert(END, f"Total: {self.final_bill:.2f}\n")

    def clear_data(self):
        self.c_name.set("")
        self.phone.set("")
        self.email.set("")
        self.bill_no.set(str(self.get_today_bill_number()))
        self.textarea.delete('1.0', END)

        for qty_var in self.item_vars.values():
            qty_var[1].set(0)

        self.total_all_bill = 0
        self.total_tax = 0
        self.final_bill = 0
    def payment_options(self):
        """Handle payment options for the bill."""
        payment_method = simpledialog.askstring("Payment Method", "Enter Payment Method (Cash, Online, Card):")
        if not payment_method:
            messagebox.showerror("Input Error", "Payment method cannot be empty!")
            return

        payment_method = payment_method.lower()
        if payment_method == "cash":
            self.textarea.insert(END, "\n\nPayment Method: Cash")
        elif payment_method == "online":
            gpay_number = simpledialog.askstring("GPay/PhonePe Number", "Please enter your GPay/PhonePe number:")
            if gpay_number:
                self.textarea.insert(END, f"\n\nPayment Method: Online\nGPay/PhonePe Number: {gpay_number}")
            else:
                messagebox.showerror("Invalid Input", "GPay/PhonePe number cannot be empty.")
        elif payment_method == "card":
            self.textarea.insert(END, "\n\nPayment Method: Card")
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid payment method (Cash, Online, Card).")

    def send_sms(self, gpay_number=None):
        """Send bill details to the customer's phone via SMS using Twilio."""
        phone_number = self.phone.get()
        if not phone_number:
            messagebox.showerror("Phone Number Missing", "Please enter a valid phone number to send the SMS.")
            return

        # Twilio credentials (Replace with your actual credentials)
        account_sid = 'ACf383b5b921e3962de6caea46be6fe47f'
        auth_token = 'd2d8465f7683509c41adac9c20d194b7'
        from_phone_number = '+1 252 528 8596'

        # Create Twilio client
        client = Client(account_sid, auth_token)

        # Generate the bill content
        bill_content = f"Bill No: {self.bill_no.get()}\n"
        bill_content += f"Customer Name: {self.c_name.get()}\n"
        bill_content += f"Phone: {self.phone.get()}\n"
        bill_content += "\n\n" + self.textarea.get('1.0', END)

        if gpay_number:
            bill_content += f"\n\nGPay/PhonePe Payment: {gpay_number}"

        # Send the message
        try:
            client.messages.create(
                body=bill_content,
                from_=from_phone_number,
                to=phone_number
            )
            messagebox.showinfo("Success", f"Bill sent to {phone_number} successfully!")
        except Exception as e:
            messagebox.showerror("SMS Error", f"Failed to send SMS. Error: {str(e)}")

    def save_bill(self):
        save_path = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            save_path.write(self.textarea.get('1.0', END))
            save_path.close()
            messagebox.showinfo("Saved", "Bill has been saved successfully!")

    def welcome_bill(self):
        self.textarea.delete("1.0", END)
        self.textarea.insert(END, "Welcome to Restaurant Billing System\n")
        self.textarea.insert(END, "-" * 40+ "\n")
        self.textarea.insert(END, "Thank You for choosing us!\n")
        self.textarea.insert(END, "-" * 40 + "\n")


if __name__ == "__main__":
    root = Tk()
    LoginPage(root)
    root.mainloop()
