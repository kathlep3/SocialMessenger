import tkinter as tk
from tkinter import ttk

class SocialMessengerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Social Messenger")
        
        # Left Frame
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Treeview widget to display DS users
        self.user_tree = ttk.Treeview(left_frame, columns=("messages",))
        self.user_tree.heading("#0", text="Friends")
        self.user_tree.heading("messages", text="Messages")
        self.user_tree.bind("<ButtonRelease-1>", self.show_user_messages)
        self.user_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.user_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.user_tree.configure(yscrollcommand=scrollbar.set)

        # Right Frame
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Display widget for messages
        self.message_display = tk.Text(right_frame, wrap="word", state="disabled")
        self.message_display.grid(row=0, column=0, sticky="nsew")

        # Text input widget for new messages
        self.message_input = tk.Text(right_frame, wrap="word")
        self.message_input.grid(row=1, column=0, sticky="nsew")

        # Button to send messages
        send_button = ttk.Button(right_frame, text="Send", command=self.send_message)
        send_button.grid(row=2, column=0, sticky="e")

        # Add User button
        add_user_button = ttk.Button(right_frame, text="Add User", command=self.add_user)
        add_user_button.grid(row=2, column=0, sticky="w")

        # Configure grid weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

    def show_user_messages(self, event):
        selected_item = self.user_tree.selection()
        if selected_item:
            user = self.user_tree.item(selected_item, "text")
            # Retrieve and display messages for the selected user
            # You need to implement this method based on your data structure

    def send_message(self):
        # Retrieve message from the input widget and send it to the selected user
        # You need to implement this method based on your data structure
        pass

    def add_user(self):
        # Add a new user to the list of contacts
        # You need to implement this method based on your data structure
        pass

if __name__ == "__main__":
    app = SocialMessengerApp()
    app.mainloop()
