import tkinter as tk
from tkinter import messagebox


class LoginWindow:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Clinic Records System")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        title = tk.Label(
            self.root,
            text="Clinic Records System",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)

        tk.Label(
            self.root,
            text="Username"
        ).pack()

        self.username_entry = tk.Entry(
            self.root,
            width=30
        )
        self.username_entry.pack(pady=5)

        tk.Label(
            self.root,
            text="Password"
        ).pack()

        self.password_entry = tk.Entry(
            self.root,
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=5)

        login_button = tk.Button(
            self.root,
            text="Login",
            width=15,
            command=self.login
        )
        login_button.pack(pady=15)

        exit_button = tk.Button(
            self.root,
            text="Exit",
            width=15,
            command=self.root.destroy
        )
        exit_button.pack()

        self.root.mainloop()

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin123":

            messagebox.showinfo(
                "Success",
                "Login Successful"
            )

            self.root.destroy()

            from dashboard import Dashboard
            Dashboard()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Username or Password"
            )


if __name__ == "__main__":
    LoginWindow()