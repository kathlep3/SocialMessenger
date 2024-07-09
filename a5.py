'''This file is the GUI portion of the assignment'''
import tkinter as tk
from tkinter import ttk, simpledialog
from typing import Text
from ds_messenger import DirectMessenger
from Profile import Profile


class LoginWindow(tk.Toplevel):
    '''This class is a new window I created to login'''
    def __init__(self, root):
        '''Init variables'''
        super().__init__(root)
        self.title("Login")
        self.geometry("300x150")

        self.server_label = tk.Label(self, text="DS Server Address:")
        self.server_label.pack()
        self.server_entry = tk.Entry(self)
        self.server_entry.pack()

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        '''This has code to collect the login info'''
        server = self.server_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        print("Server:", server)
        print("Username:", username)
        print("Password:", password)
        self.destroy()


class Body(tk.Frame):
    '''This class is responsible for the Body'''
    def __init__(self, root, recipient_selected_callback=None):
        '''Init variables for Body'''
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        '''In charge of selecting a contact'''
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)
        x, y = event.x_root, event.y_root
        popup = tk.Toplevel(self.root)
        popup.geometry(f'+{x}+{y}')
        popup_label = tk.Label(popup, text=f'Selected contact: {entry}')
        popup_label.pack()

    def insert_contact(self, contact: str):
        '''Inserts contacts'''
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        '''Inserts the treeview for contacts'''
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        '''Inserts the user's message to send'''
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        '''Inserts the message from contact'''
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        '''This will take the message to send so it can send'''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        '''Sets the text in the entry box'''
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        '''Responsible for connecting functions to buttons'''
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.heading("#0", text="Friends")
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    '''Footer class'''
    def __init__(self, root, send_callback=None):
        '''Init variables for Footer'''
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        '''Functionality for clicking send'''
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        '''Responsible for connecting buttons to functions'''
        save_button = tk.Button(master=self,
                                text="Send",
                                width=20,
                                command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    '''This is the popup window that will let you add friends'''
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        '''Init variables for adding friend window'''
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        ''''The body of the window'''
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        '''Collects the info in the entry boxes'''
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    '''The main frame'''
    def __init__(self, root):
        '''Init variables of MainApp'''
        tk.Frame.__init__(self, root)
        self.root = root

        self.login_window = LoginWindow(self.root)
        self.login_window.transient(root)
        self.login_window.grab_set()
        self.login_window.wait_window()

        self.username = "katpham"
        self.password = "mypass"
        self.server = "168.235.86.101"
        self.recipient = "caittest"
        self.direct_messenger = DirectMessenger(self.server,
                                                self.username,
                                                self.password)
        self.profile = Profile()
        self.path = "TestFolder/mytest.dsu"

        self._draw()
        self.profile.load_profile(self.path)
        print(self.profile.get_friend())
        for friend in self.profile.get_friend():
            self.body.insert_contact(friend)

    def close(self):
        '''Closes the window'''
        self.root.destroy()

    def send_message(self):
        '''Sends a message'''
        self.profile.load_profile(self.path)
        text_message = self.body.get_text_entry()
        if self.recipient:
            self.direct_messenger.send_message(text_message, self.recipient)
            self.body.set_text_entry("")
            self.body.insert_user_message(text_message)
            self.profile.add_message(text_message)
            self.profile.save_profile(self.path)
            print("Message sent.")

    def add_contact(self):
        '''Adds a contact to the treeview widget'''
        self.profile.load_profile(self.path)
        new_contact = tk.simpledialog.askstring("Add Contact", "Enter Friend:")
        self.profile.add_friend(new_contact)
        self.body.insert_contact(new_contact)
        self.profile.save_profile(self.path)
        print("Contact added.")

    def recipient_selected(self, recipient):
        '''Selects a specific friend'''
        self.recipient = recipient

    def configure_server(self):
        '''Configures the server'''
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = DirectMessenger(self.server,
                                                self.username,
                                                self.password)

    def publish(self, message: str):
        '''Publishes the message'''
        if self.recipient:
            self.direct_messenger.send_message(message, self.recipient)

    def check_new(self):
        '''Will allow you to check for new messages'''
        new_messages = self.direct_messenger.retrieve_new()
        for message in new_messages:
            print("New message:", message.message)
            print("From:", message.recipient)
            print("Timestamp", message.timestamp)
            print()

    def _draw(self):
        '''Connects buttons to functions'''
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close', command=self.close)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
