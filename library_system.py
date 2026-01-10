# ================== FILE MANAGER ==================
import csv
from collections import Counter

class FileManager:
    def read(self, filename):
        data = []
        try:
            with open(filename, "r", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            return []
        return data

    def write(self, filename, data, fieldnames):
        with open(filename, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def append(self, filename, row, fieldnames):
        try:
            with open(filename, "r", newline='') as f:
                reader = csv.DictReader(f)
                existing = [r for r in reader]
        except FileNotFoundError:
            existing = []

        existing.append(row)
        self.write(filename, existing, fieldnames)


fm = FileManager()


# ================== FILE INIT ==================
def init_files():
    files = {
        "admin.csv": ["username", "password"],
        "students.csv": ["sid", "name", "stype", "password", "status"],
        "books.csv": ["bid", "title", "author", "qty"],
        "issued_books.csv": ["sid", "bid", "days_kept", "late_days", "fine", "rent", "total"],
        "fine.csv": ["sid", "bid", "days_kept", "late_days", "fine", "rent", "total"]
    }
    for filename, fields in files.items():
        try:
            with open(filename, "x", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
        except FileExistsError:
            pass

    # Default admin
    admins = fm.read("admin.csv")
    if not admins:
        fm.append("admin.csv", {"username":"admin","password":"admin123"}, ["username","password"])


# ================== STUDENT TYPES ==================
class Student:
    rent_per_day = 10
    fine_rate = 0
    issue_limit = 0

    def __init__(self, sid, name, stype, status="Regular", password=None):
        self.sid = sid
        self.name = name
        self.stype = stype
        self.status = status
        self.password = password


class Undergraduate(Student):
    fine_rate = 20
    issue_limit = 2


class Postgraduate(Student):
    fine_rate = 15
    issue_limit = 4


class Research(Student):
    fine_rate = 10
    issue_limit = 6


class Guest(Student):
    fine_rate = 0
    issue_limit = 0


# ================== ADMIN SUBSYSTEMS ==================
class StudentManager:
    fieldnames = ["sid","name","stype","password","status"]

    def menu(self):
        while True:
            print("\n" + "="*50)
            print("        STUDENT MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Add Student\n2. View Students\n3. Delete Student\n4. Exit")
            ch = input("Choice: ")
            if ch=="1": self.add_student()
            elif ch=="2": self.view_students()
            elif ch=="3": self.delete_student()
            else: break

    def add_student(self):
        sid = input("Student ID: ")
        name = input("Name: ")
        stype = input("Type (UG/PG/RS/GUEST): ").upper()
        pwd = input("Password: ")
        fm.append("students.csv", {"sid":sid,"name":name,"stype":stype,"password":pwd,"status":"Regular"}, self.fieldnames)
        print("Student added successfully.")

    def view_students(self):
        print("\n" + "-"*50)
        print("STUDENT LIST")
        print("-"*50)
        students = fm.read("students.csv")
        issued_books = fm.read("issued_books.csv")
        fine_data = fm.read("fine.csv")
        for s in students:
            sid = s["sid"]
            print(f"ID     : {sid}")
            print(f"Name   : {s['name']}")
            print(f"Type   : {s['stype']}")
            print(f"Status : {s['status']}")
            # Show allotted books
            books = [b["bid"] for b in issued_books if b["sid"]==sid]
            print(f"Books  : {', '.join(books) if books else 'None'}")
            # Show total fine
            fines = [int(f["total"]) for f in fine_data if f["sid"]==sid]
            total_fine = sum(fines)
            print(f"Fine   : Rs. {total_fine}")
            print("-"*50)

    def delete_student(self):
        sid = input("Enter Student ID to delete: ")
        students = fm.read("students.csv")
        updated = [s for s in students if s["sid"]!=sid]
        if len(updated)==len(students): print("Student not found."); return
        fm.write("students.csv", updated, self.fieldnames)
        # Remove issued books & fines
        issued = fm.read("issued_books.csv")
        fm.write("issued_books.csv", [b for b in issued if b["sid"]!=sid],
                 ["sid","bid","days_kept","late_days","fine","rent","total"])
        fines = fm.read("fine.csv")
        fm.write("fine.csv", [f for f in fines if f["sid"]!=sid],
                 ["sid","bid","days_kept","late_days","fine","rent","total"])
        print("Student deleted successfully.")


class BookManager:
    fieldnames = ["bid","title","author","qty"]

    def menu(self):
        while True:
            print("\n" + "="*50)
            print("          BOOK MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Add Book\n2. View Books\n3. Delete Book\n4. Exit")
            ch = input("Choice: ")
            if ch=="1": self.add_book()
            elif ch=="2": self.view_books()
            elif ch=="3": self.delete_book()
            else: break

    def add_book(self):
        bid = input("Book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        qty = input("Quantity: ")
        fm.append("books.csv", {"bid":bid,"title":title,"author":author,"qty":qty}, self.fieldnames)
        print("Book added successfully.")

    def view_books(self):
        print("\n" + "-"*50)
        print("BOOK LIST")
        print("-"*50)
        books = fm.read("books.csv")
        for b in books:
            print(f"ID     : {b['bid']}")
            print(f"Title  : {b['title']}")
            print(f"Author : {b['author']}")
            print(f"Qty    : {b['qty']}")
            print("-"*50)

    def delete_book(self):
        bid = input("Enter Book ID to delete: ")
        books = fm.read("books.csv")
        updated = [b for b in books if b["bid"]!=bid]
        if len(updated)==len(books): print("Book not found."); return
        fm.write("books.csv", updated, self.fieldnames)
        print("Book deleted successfully.")


class FineManager:
    fieldnames = ["sid","bid","days_kept","late_days","fine","rent","total"]

    def menu(self):
        while True:
            print("\n" + "="*50)
            print("          FINE MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Manage Student Fine\n2. View Reports\n3. Exit")
            ch = input("Choice: ")
            if ch=="1": self.manage_fine()
            elif ch=="2": self.reports()
            else: break

    def manage_fine(self):
        sid = input("Enter Student ID: ")
        fines = fm.read("fine.csv")
        updated = []
        found = False
        for f in fines:
            if f["sid"]==sid:
                found=True
                fine = int(f["fine"])
                rent = int(f["rent"])
                while True:
                    print("\n" + "-"*50)
                    print("FINE DETAILS")
                    print("-"*50)
                    print(f"Student ID : {sid}")
                    print(f"Book ID    : {f['bid']}")
                    print(f"Late Days  : {f['late_days']}")
                    print(f"Fine       : Rs. {fine}")
                    print(f"Rent       : Rs. {rent}")
                    print(f"Total      : Rs. {fine+rent}")
                    print("-"*50)
                    print("1. Remove Fine Amount")
                    print("2. Remove Rent Amount")
                    print("3. Exit")
                    ch = input("Choice: ")
                    if ch=="1":
                        amt=int(input("Amount to remove: "))
                        if amt<=fine: fine-=amt
                    elif ch=="2":
                        amt=int(input("Amount to remove: "))
                        if amt<=rent: rent-=amt
                    else: break
                total=fine+rent
                updated.append({"sid":sid,"bid":f["bid"],"days_kept":f["days_kept"],"late_days":f["late_days"],
                                "fine":fine,"rent":rent,"total":total})
            else:
                updated.append(f)
        if not found: print("No fine record found."); return
        fm.write("fine.csv", updated, self.fieldnames)
        # Update student status
        students = fm.read("students.csv")
        total_fine = sum(f["total"] for f in updated if f["sid"]==sid)
        for s in students:
            if s["sid"]==sid:
                s["status"]="Blocked" if total_fine>1000 else "Regular"
        fm.write("students.csv", students, ["sid","name","stype","password","status"])
        print("Fine updated successfully.")

    def reports(self):
        print("\n" + "="*50)
        print("          ADMIN REPORTS")
        print("="*50)
        # Total fine collected
        fines = fm.read("fine.csv")
        total_fine=sum(int(f["total"]) for f in fines)
        print(f"Total Fine Collected : Rs. {total_fine}")
        # Most issued books
        issued=fm.read("issued_books.csv")
        bids=[i["bid"] for i in issued]
        most_issued = Counter(bids).most_common(5)
        print("Most Issued Books:")
        for book,count in most_issued:
            print(f"Book ID: {book} | Times Issued: {count}")
        # Students with highest fines
        fine_summary=Counter()
        for f in fines: fine_summary[f["sid"]]+=int(f["total"])
        top_fines = fine_summary.most_common(5)
        print("\nStudents with Highest Fines:")
        for sid,total in top_fines:
            sname=[s["name"] for s in fm.read("students.csv") if s["sid"]==sid][0]
            print(f"ID: {sid} | Name: {sname} | Total Fine: Rs. {total}")
        # Blocked students
        blocked=[s for s in fm.read("students.csv") if s["status"]=="Blocked"]
        print("\nBlocked Students:")
        for s in blocked:
            print(f"ID: {s['sid']} | Name: {s['name']} | Status: {s['status']}")
        print("="*50)


class PasswordManager:
    student_fields = ["sid","name","stype","password","status"]
    admin_fields = ["username","password"]

    def menu(self):
        while True:
            print("\n" + "="*50)
            print("          PASSWORD MANAGEMENT")
            print("="*50)
            print("1. Change Student Password\n2. Change Admin Password\n3. Exit")
            ch = input("Choice: ")
            if ch=="1": self.change_student_password()
            elif ch=="2": self.change_admin_password()
            else: break

    def change_student_password(self):
        sid = input("Student ID: ")
        old = input("Old Password: ")
        students = fm.read("students.csv")
        for s in students:
            if s["sid"]==sid and s["password"]==old:
                new = input("New Password: ")
                s["password"]=new
                fm.write("students.csv", students, self.student_fields)
                print("Student password changed successfully.")
                return
        print("Student not found or old password incorrect.")

    def change_admin_password(self):
        username = input("Admin username: ")
        old = input("Old Password: ")
        admins = fm.read("admin.csv")
        for a in admins:
            if a["username"]==username and a["password"]==old:
                new = input("New Password: ")
                a["password"]=new
                fm.write("admin.csv", admins, self.admin_fields)
                print("Admin password changed successfully.")
                return
        print("Admin not found or old password incorrect.")


# ================== ADMIN ==================
class Admin:
    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        admins = fm.read("admin.csv")
        for a in admins:
            if a["username"]==username and a["password"]==password:
                return True
        return False


# ================== ISSUE MANAGER ==================
class IssueManager:
    fine_fields = ["sid","bid","days_kept","late_days","fine","rent","total"]
    issued_fields = ["sid","bid","days_kept","late_days","fine","rent","total"]

    def request_book(self, student):
        if student.status=="Blocked":
            print("You are BLOCKED due to high fines. Cannot request books.")
            return
        bid = input("Enter Book ID to request: ")
        books = fm.read("books.csv")
        for b in books:
            if b["bid"]==bid and int(b["qty"])>0:
                b["qty"]=str(int(b["qty"])-1)
                fm.write("books.csv", books, ["bid","title","author","qty"])
                # add to issued
                fm.append("issued_books.csv", {"sid":student.sid,"bid":bid,"days_kept":0,"late_days":0,"fine":0,"rent":0,"total":0}, self.issued_fields)
                print("Book issued successfully.")
                return
        print("Book not available.")

    def return_book(self, student):
        bid = input("Enter Book ID to return: ")
        days_kept = int(input("Enter days kept: "))
        issued = fm.read("issued_books.csv")
        new_issued=[]
        for i in issued:
            if i["sid"]==student.sid and i["bid"]==bid:
                late_days = max(0, days_kept-7)
                fine = late_days*student.fine_rate
                rent = days_kept*student.rent_per_day
                total = fine+rent
                fm.append("fine.csv", {"sid":student.sid,"bid":bid,"days_kept":days_kept,"late_days":late_days,"fine":fine,"rent":rent,"total":total}, self.fine_fields)
                print(f"Book returned. Fine: {fine}, Rent: {rent}, Total: {total}")
            else:
                new_issued.append(i)
        fm.write("issued_books.csv", new_issued, self.issued_fields)
        # update book qty
        books = fm.read("books.csv")
        for b in books:
            if b["bid"]==bid:
                b["qty"]=str(int(b["qty"])+1)
        fm.write("books.csv", books, ["bid","title","author","qty"])


# ================== STUDENT MODULE ==================
class StudentModule:
    def login(self):
        sid = input("Student ID: ")
        pwd = input("Password: ")
        students = fm.read("students.csv")
        student=None
        for s in students:
            if s["sid"]==sid and s["password"]==pwd:
                stype=s["stype"]
                status=s["status"]
                if stype=="UG": student=Undergraduate(sid,s["name"],stype,status)
                elif stype=="PG": student=Postgraduate(sid,s["name"],stype,status)
                elif stype=="RS": student=Research(sid,s["name"],stype,status)
                else: student=Guest(sid,s["name"],stype,status)
                student.password = pwd
                break
        if not student:
            print("Invalid login"); return
        # Auto update fines and status on login
        self.update_fines_status(student)
        self.menu(student)

    def update_fines_status(self, student):
        # calculate total fines
        fine_data = fm.read("fine.csv")
        total_fine = sum(int(f["total"]) for f in fine_data if f["sid"]==student.sid)
        students = fm.read("students.csv")
        for s in students:
            if s["sid"]==student.sid:
                s["status"]="Blocked" if total_fine>1000 else "Regular"
        fm.write("students.csv", students, ["sid","name","stype","password","status"])
        student.status = "Blocked" if total_fine>1000 else "Regular"

    def menu(self, student):
        im=IssueManager()
        while True:
            print("\n" + "="*50)
            print(f"Welcome {student.name} (ID: {student.sid}, Status: {student.status})")
            print("="*50)
            print("1. View Available Books")
            print("2. Request Book")
            print("3. Return Book")
            print("4. View Fine")
            print("5. View Allotted Books")
            print("6. Change Password")
            print("7. Exit")
            ch=input("Choice: ")
            if ch=="1":
                books=fm.read("books.csv")
                for b in books:
                    print(f"\nID: {b['bid']}\nTitle: {b['title']}\nAuthor: {b['author']}\nQty: {b['qty']}")
            elif ch=="2": im.request_book(student)
            elif ch=="3": im.return_book(student)
            elif ch=="4":
                fine=fm.read("fine.csv")
                total=0
                print("\n" + "-"*50)
                print("YOUR FINE DETAILS")
                print("-"*50)
                for f in fine:
                    if f["sid"]==student.sid:
                        print(f"Book ID: {f['bid']}, Fine: {f['fine']}, Rent: {f['rent']}, Total: {f['total']}")
                        total+=int(f["total"])
                print(f"\nTotal Fine: Rs. {total}")
                print("-"*50)
            elif ch=="5":
                issued=fm.read("issued_books.csv")
                print("\nALLOTTED BOOKS:")
                for b in issued:
                    if b["sid"]==student.sid:
                        overdue=" (OVERDUE)" if int(b["days_kept"])>7 else ""
                        print(f"Book ID: {b['bid']}, Days Kept: {b['days_kept']}{overdue}")
            elif ch=="6":
                old=input("Old password: ")
                if old==student.password:
                    new=input("New password: ")
                    students=fm.read("students.csv")
                    for s in students:
                        if s["sid"]==student.sid:
                            s["password"]=new
                    student.password=new
                    fm.write("students.csv", students, ["sid","name","stype","password","status"])
                    print("Password changed successfully.")
                else:
                    print("Old password incorrect")
            else: break


# ================== SYSTEM ==================
class LibrarySystem:
    def admin_menu(self):
        if not Admin().login():
            print("Invalid login"); return
        sm=StudentManager()
        bm=BookManager()
        fmgr=FineManager()
        pmgr=PasswordManager()
        while True:
            print("\n" + "="*50)
            print("ADMIN MENU")
            print("="*50)
            print("1. Student Management\n2. Book Management\n3. Fine Management\n4. Password Management\n5. Exit")
            ch=input("Choice: ")
            if ch=="1": sm.menu()
            elif ch=="2": bm.menu()
            elif ch=="3": fmgr.menu()
            elif ch=="4": pmgr.menu()
            else: break

    def student_menu(self):
        StudentModule().login()

    def run(self):
        init_files()
        while True:
            print("\n1. Admin Login\n2. Student Login\n3. Exit")
            ch=input("Choice: ")
            if ch=="1": self.admin_menu()
            elif ch=="2": self.student_menu()
            else: break


# ================== RUN ==================
if __name__=="__main__":
    LibrarySystem().run()
