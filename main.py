import tkinter as tk

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
        if user_id == "admin":  # Replace with your database validation logic
            self.message_label.config(text="Login Successful!", fg="green")
            self.controller.show_frame(FunctionalityFrame)
        else:
            self.message_label.config(text="Invalid User ID!", fg="red")


class FunctionalityFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Functionality Menu", font=("Helvetica", 18)).pack(pady=20)
        tk.Button(self, text="Logout", command=lambda: controller.show_frame(LoginFrame)).pack(pady=10)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
