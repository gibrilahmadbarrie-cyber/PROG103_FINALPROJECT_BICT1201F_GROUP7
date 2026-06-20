import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from reports import generate_pdf_report

from database import *

import matplotlib.pyplot as plt


class Dashboard:
    def generate_report(self):
        generate_pdf_report()

        messagebox.showinfo(
            "Success",
            "PDF Report Generated Successfully"
        )

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Clinic Records Dashboard")
        self.root.geometry("1000x650")

        title = tk.Label(
            self.root,
            text="Clinic Records Management System",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        self.create_statistics()
        self.create_search_filter()
        self.create_table()
        self.create_buttons()

        self.load_records()

        self.root.mainloop()
    def create_statistics(self):

        self.stats_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11, "bold")
        )

        self.stats_label.pack(pady=5)

    def update_statistics(self):

        records = get_records()

        total = len(records)

        active = 0
        inactive = 0
        pending = 0

        for record in records:

            if record[3] == "Active":
                active += 1

            elif record[3] == "Inactive":
                inactive += 1

            elif record[3] == "Pending":
                pending += 1

        self.stats_label.config(
            text=f"Total Records: {total}   |   Active: {active}   |   Inactive: {inactive}   |   Pending: {pending}"
        )

    def create_search_filter(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Search").grid(row=0, column=0)

        self.search_entry = tk.Entry(frame)
        self.search_entry.grid(row=0, column=1)

        tk.Button(
            frame,
            text="Search",
            command=self.search_data
        ).grid(row=0, column=2, padx=5)

        tk.Label(frame, text="Gender").grid(row=0, column=3)

        self.gender_var = tk.StringVar()

        gender_box = ttk.Combobox(
            frame,
            textvariable=self.gender_var,
            values=["", "Male", "Female"]
        )

        gender_box.grid(row=0, column=4)

        tk.Label(frame, text="Status").grid(row=0, column=5)

        self.status_var = tk.StringVar()

        status_box = ttk.Combobox(
            frame,
            textvariable=self.status_var,
            values=["", "Active", "Inactive", "Pending"]
        )

        status_box.grid(row=0, column=6)

        tk.Button(
            frame,
            text="Filter",
            command=self.filter_data
        ).grid(row=0, column=7, padx=5)

        tk.Button(
            frame,
            text="Refresh",
            command=self.load_records
        ).grid(row=0, column=8)
    def create_table(self):

        columns = (
            "ID",
            "Name",
            "Gender",
            "Status",
            "Contact"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="x", padx=10)

    def load_records(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        records = get_records()

        for record in records:
            self.tree.insert("", tk.END, values=record)

        self.update_statistics()

    def search_data(self):

        keyword = self.search_entry.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        records = search_records(keyword)

        for record in records:
            self.tree.insert("", tk.END, values=record)

    def filter_data(self):

        gender = self.gender_var.get()
        status = self.status_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        records = filter_records(
            gender,
            status
        )

        for record in records:
            self.tree.insert("", tk.END, values=record)
    def create_buttons(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(
            frame,
            text="Add Record",
            width=15,
            command=self.add_record_window
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            frame,
            text="Delete Record",
            width=15,
            command=self.delete_record
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            frame,
            text="Bar Chart",
            width=15,
            command=self.show_bar_chart
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            frame,
            text="Pie Chart",
            width=15,
            command=self.show_pie_chart
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            frame,
            text="Generate Report",
            width=15,
            command=self.generate_report
        ).grid(row=0, column=4, padx=5)
    def add_record_window(self):

        window = tk.Toplevel(self.root)

        window.title("Add Record")
        window.geometry("300x300")

        tk.Label(window, text="Full Name").pack()

        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="Gender").pack()

        gender_box = ttk.Combobox(
            window,
            values=["Male", "Female"]
        )
        gender_box.pack()

        tk.Label(window, text="Status").pack()

        status_box = ttk.Combobox(
            window,
            values=["Active", "Inactive", "Pending"]
        )
        status_box.pack()

        tk.Label(window, text="Contact").pack()

        contact_entry = tk.Entry(window)
        contact_entry.pack()

        def save_record():

            add_record(
                name_entry.get(),
                gender_box.get(),
                status_box.get(),
                contact_entry.get()
            )

            messagebox.showinfo(
                "Success",
                "Record Added Successfully"
            )

            self.load_records()

            window.destroy()

        tk.Button(
            window,
            text="Save",
            command=save_record
        ).pack(pady=10)

    def delete_record(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select a Record"
            )
            return

        record = self.tree.item(selected[0])

        record_id = record["values"][0]

        delete_record(record_id)

        self.load_records()

        messagebox.showinfo(
            "Success",
            "Record Deleted"
        )
    def show_bar_chart(self):

        records = get_records()

        active = 0
        inactive = 0
        pending = 0

        for record in records:

            if record[3] == "Active":
                active += 1

            elif record[3] == "Inactive":
                inactive += 1

            elif record[3] == "Pending":
                pending += 1

        plt.figure(figsize=(6, 4))

        plt.bar(
            ["Active", "Inactive", "Pending"],
            [active, inactive, pending]
        )

        plt.title("Records by Status")

        plt.show()

    def show_pie_chart(self):
        def generate_report(self):

            filename = generate_pdf_report()

            messagebox.showinfo(
                "Success",
                f"{filename} generated successfully"
            )

        records = get_records()

        male = 0
        female = 0

        for record in records:

            if record[2] == "Male":
                male += 1
            else:
                female += 1

        plt.figure(figsize=(6, 6))

        plt.pie(
            [male, female],
            labels=["Male", "Female"],
            autopct="%1.1f%%"
        )

        plt.title("Gender Distribution")

        plt.show()
if __name__ == "__main__":
    Dashboard()

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime

from database import get_records


def generate_pdf_report():

    document = SimpleDocTemplate(
        "Clinic_Report.pdf"
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "CLINIC RECORDS REPORT",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    date_generated = Paragraph(
        f"Generated On: {datetime.now()}",
        styles["Normal"]
    )

    elements.append(date_generated)

    elements.append(
        Spacer(1, 20)
    )

    records = get_records()

    total_records = len(records)

    summary = Paragraph(
        f"Total Records: {total_records}",
        styles["Heading2"]
    )

    elements.append(summary)

    elements.append(
        Spacer(1, 20)
    )

    data = [
        [
            "ID",
            "Name",
            "Gender",
            "Status",
            "Contact"
        ]
    ]

    for record in records:
        data.append(list(record))

    table = Table(data)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ])
    )

    elements.append(table)

    document.build(elements)

    return "Clinic_Report.pdf"