import pymssql
import tkinter as tk
from tkinter import ttk

userID = None

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Yelp Application")
        self.geometry("600x400")

        # Create a container to hold frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Configure rows and columns for proper resizing
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold frames
        self.frames = {}

        # Show the login frame initially
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class):
        """Display a frame for the given class."""
        # Get the frame if already exists
        frame = self.frames.get(frame_class)

        # Create the frame if not already created
        if frame is None:
            frame = frame_class(self.container, self)
            self.frames[frame_class] = frame

        # Display the frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Login", font=("Helvetica", 18)).pack(pady=20)

        tk.Label(self, text="User ID:").pack(pady=5)
        self.user_id_entry = tk.Entry(self)
        self.user_id_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        self.message_label = tk.Label(self, text="", fg="red")
        self.message_label.pack()

    def login(self):
        """Handle login logic."""
        user_id = self.user_id_entry.get()
        if (len(user_id) != 0):
            connection = pymssql.connect(host='cypress.csil.sfu.ca', user='s_hcm9',
                                         password='LG7r6n4Lnh6NAEbP', database='hcm9354')

            cursor = connection.cursor(as_dict=True)

            #zZsX8VeUYzS1GZl6S6NNmA
            query = f"SELECT * \
                FROM dbo.user_yelp\
                WHERE (user_id = '{user_id}')"
            cursor.execute(query)

            row = cursor.fetchone()
            if row is not None:
                self.message_label.config(text="Login Successful!", fg="green")
                self.controller.show_frame(FunctionalityFrame)
                print(row)
            else:
                self.message_label.config(text="Invalid User ID!", fg="red")
            

            connection.close()
        else:
            self.message_label.config(text="Invalid User ID!", fg="red")



class FunctionalityFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Functionality Menu", font=("Helvetica", 18)).pack(pady=20)
        tk.Button(self, text="Search Business", command=lambda: controller.show_frame(SearchBusiness)).pack(pady=10)
        tk.Button(self, text="Search Users", command=lambda: controller.show_frame(SearchUsers)).pack(pady=10)
        tk.Button(self, text="Make Friend", command=lambda: controller.show_frame(MakeFriend)).pack(pady=10)
        tk.Button(self, text="Review Business", command=lambda: controller.show_frame(ReviewBusiness)).pack(pady=10)
        tk.Button(self, text="Logout", command=lambda: controller.show_frame(LoginFrame)).pack(pady=10)
        

class SearchBusiness(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Search Business", font=("Helvetica", 18)).pack(pady=20)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="City:").grid(row=0, column=0, padx=10, pady=5)
        self.city_entry = tk.Entry(input_frame)
        self.city_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Business Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Minimum Stars:").grid(row=2, column=0, padx=10, pady=5)
        self.stars_entry = tk.Entry(input_frame)
        self.stars_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Order By:").grid(row=3, column=0, padx=10, pady=5)
        self.order_by = tk.StringVar(value="name")  
        tk.OptionMenu(input_frame, self.order_by, "name", "city", "stars").grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self, text="Search", command=self.search_business).pack(pady=10)

        self.message_label = tk.Label(self, text="", fg="red")
        self.message_label.pack()

        self.results_text = tk.Text(self, height=10, width=80)
        self.results_text.pack(pady=10)

    def search_business(self):
        city = self.city_entry.get().strip().title()
        name = self.name_entry.get().strip().title()
        min_stars = self.stars_entry.get().strip()
        order_by = self.order_by.get()

        min_stars = int(min_stars) if min_stars else 0

        try:
            connection = pymssql.connect(host='cypress.csil.sfu.ca', user='s_hcm9',
                                         password='LG7r6n4Lnh6NAEbP', database='hcm9354')

            cursor = connection.cursor(as_dict=True)

            #Test: city = Edmonton, name = Edo Japan
            query = f"\
                SELECT business_id, name, address, city, stars\
                FROM dbo.business\
                WHERE (city = '{city}' OR '{city}' = '')\
                    AND (name LIKE '%{name}%' OR '{name}' = '')\
                    AND (stars >= '{min_stars}')\
                ORDER BY {order_by}"

            cursor.execute(query)
            results = cursor.fetchall()
            self.display_results(results)

            connection.close()
        except Exception as e:
            self.message_label.config(text=f"Error: {e}", fg="red")

    def display_results(self, results):

        self.results_text.delete(1.0, tk.END)

        if not results:
            self.results_text.insert(tk.END, "No businesses found.\n")
            return

        for result in results:
            self.results_text.insert(tk.END, f"Id: {result['business_id']}, Name: {result['name']}, "
                                             f"Address: {result['address']}, City: {result['city']}, Stars: {result['stars']}\n")

class SearchUsers(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Search Users", font=("Helvetica", 18)).pack(pady=20)

        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Minimum Review Count:").grid(row=1, column=0, padx=10, pady=5)
        self.count_entry = tk.Entry(input_frame)
        self.count_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Minimum Average Stars:").grid(row=2, column=0, padx=10, pady=5)
        self.stars_entry = tk.Entry(input_frame)
        self.stars_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self, text="Search", command=self.search_user).pack(pady=10)

        self.message_label = tk.Label(self, text="", fg="red")
        self.message_label.pack()

        self.results_text = tk.Text(self, height=10, width=80)
        self.results_text.pack(pady=10)

    def search_user(self):
        min_count = self.count_entry.get().strip()
        name = self.name_entry.get().strip().title()
        avg_stars = self.stars_entry.get().strip()

        avg_stars = int(avg_stars) if avg_stars else 0
        min_count = int(min_count) if min_count else 0

        try:
            connection = pymssql.connect(host='cypress.csil.sfu.ca', user='s_hcm9',
                                         password='LG7r6n4Lnh6NAEbP', database='hcm9354')

            cursor = connection.cursor(as_dict=True)

            #Test: name = Megh
            print(min_count)
            query = f"\
                SELECT user_id, name, review_count, useful, funny, cool, average_stars, yelping_since\
                FROM dbo.user_yelp\
                WHERE (review_count >= '{min_count}')\
                AND (name LIKE '%{name}%' OR '{name}'  = '')\
                AND (average_stars >= '{avg_stars}')"

            cursor.execute(query)

            results = cursor.fetchall()
            self.display_results(results)

            connection.close()
        except Exception as e:
            self.message_label.config(text=f"Error: {e}", fg="red")

    def display_results(self, results):

        self.results_text.delete(1.0, tk.END)

        if not results:
            self.results_text.insert(tk.END, "No user found.\n")
            return

        for result in results:
            self.results_text.insert(tk.END, f"Id: {result['user_id']}, Name: {result['name']}, "
                                             f"Minimum Review Count: {result['review_count']}, "
                                             f"Useful: {result['useful']}, Funny: {result['funny']}, "
                                             f"Cool: {result['cool']}, Average Stars: {result['average_stars']}\n")

class MakeFriend(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Make Friend", font=("Helvetica", 18)).pack(pady=20)

        # Input fields for searching users
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Search by Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(input_frame, text="Search", command=self.search_users).grid(row=0, column=2, padx=10, pady=5)

        # Treeview to display users
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Reviews", "Stars"), show="headings", height=10)
        self.tree.heading("ID", text="User ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Reviews", text="Review Count")
        self.tree.heading("Stars", text="Average Stars")
        self.tree.pack(pady=10)

        # Button to make friend
        tk.Button(self, text="Make Friend", command=self.make_friend).pack(pady=10)

        # Message Label
        self.message_label = tk.Label(self, text="", fg="red")
        self.message_label.pack()

    def search_users(self):
        """Search and display users based on name."""
        name = self.name_entry.get().strip().title()

        try:
            connection = pymssql.connect(host='cypress.csil.sfu.ca', user='s_hcm9',
                                         password='LG7r6n4Lnh6NAEbP', database='hcm9354')
            cursor = connection.cursor(as_dict=True)

            query = """
                SELECT user_id, name, review_count, average_stars
                FROM dbo.user_yelp
                WHERE name LIKE %s
            """
            params = (f"%{name}%",)
            cursor.execute(query, params)

            results = cursor.fetchall()

            # Clear previous results
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insert new results
            for result in results:
                self.tree.insert("", "end", values=(result["user_id"], result["name"],
                                                    result["review_count"], result["average_stars"]))

            connection.close()
        except Exception as e:
            self.message_label.config(text=f"Error: {e}", fg="red")

    def make_friend(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.message_label.config(text="Please select a user to make a friend.", fg="red")
            return

        user_id = self.tree.item(selected_item, "values")[0]  # Get the User ID from the selected row
        self.message_label.config(text=f"Friendship successfully created with User ID {user_id}!", fg="green")

    def display_results(self, results):

        self.results_text.delete(1.0, tk.END)

        if not results:
            self.results_text.insert(tk.END, "No user found.\n")
            return

        for result in results:
            self.results_text.insert(tk.END, f"Id: {result['user_id']}, Name: {result['name']}, "
                                             f"Minimum Review Count: {result['review_count']}, "
                                             f"Useful: {result['useful']}, Funny: {result['funny']}, "
                                             f"Cool: {result['cool']}, Average Stars: {result['average_stars']}\n")


class ReviewBusiness(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Review Business", font=("Helvetica", 18)).pack(pady=20)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
    
