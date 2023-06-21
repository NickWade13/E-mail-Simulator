import os
import subprocess

# --- Email Class --- #
class Email:
    def __init__(self, senders_email, recipient_email, subject_line, email_content, has_been_read=False, attachments=None):
        # Initialize the Email object with the provided attributes
        self.senders_email = senders_email
        self.recipient_email = recipient_email
        self.subject_line = subject_line
        self.email_content = email_content
        self.has_been_read = has_been_read
        self.attachments = attachments if attachments else []

    def mark_as_read(self):
        # Mark the email as read by setting the has_been_read attribute to True
        self.has_been_read = True

    def __str__(self):
        # Return a string representation of the Email object
        return f"To: {self.recipient_email}\nFrom: {self.senders_email}\nSubject: {self.subject_line}\nContent: {self.email_content}"

    __inbox = []

    @classmethod
    def populate_inbox(cls):
        # Create sample email objects and add them to the inbox
        sample_emails = [
            {
                'senders_email': 'friend@sample1.com',
                'recipient_email': 'your_email@sample.com',
                'subject_line': 'Hello!',
                'email_content': 'Hi, how are you?',
                'attachments': ['sample_attachment.txt']
            },
            {
                'senders_email': 'work@sample2.com',
                'recipient_email': 'your_email@sample.com',
                'subject_line': 'Weekly Rota',
                'email_content': 'Please see below the weekly rota...',
                'attachments': []
            },
            {
                'senders_email': 'hyperion@sample3.com',
                'recipient_email': 'your_email@sample.com',
                'subject_line': 'Your most recent task',
                'email_content': 'Your most recent task was great! 100%',
                'attachments': []
            }
        ]

        # Create sample_attachment.txt if it doesn't exist
        attachment_path = 'sample_attachment.txt'
        if not os.path.exists(attachment_path):
            with open(attachment_path, 'w') as file:
                file.write('This is a sample attachment.')

        for email in sample_emails:
            # Create an Email object for each sample email and add it to the inbox
            email_object = Email(
                email['senders_email'],
                email['recipient_email'],
                email['subject_line'],
                email['email_content']
            )
            email_object.attachments = email.get('attachments', [])
            Email.__inbox.append(email_object)

    @classmethod
    def get_inbox(cls):
        # Get the inbox (list of Email objects)
        return cls.__inbox

    @classmethod
    def get_email(cls, index):
        # Get the Email object at the specified index in the inbox
        if 0 <= index < len(cls.__inbox):
            return cls.__inbox[index]
        raise IndexError("Invalid email number.")

    @classmethod
    def delete_email(cls, index):
        # Delete the Email object at the specified index in the inbox
        if 0 <= index < len(cls.__inbox):
            del cls.__inbox[index]
        else:
            raise IndexError("Invalid email number.")

    @classmethod
    def send_email(cls):
        # Prompt the user to enter the sender, recipient, subject, content, and attachments of the email
        while True:
            sender = input("Your email address: ")
            if sender:
                break
            else:
                print("Email address is required. Please try again.")

        while True:
            recipient = input("Recipient's email address: ")
            if recipient:
                break
            else:
                print("Recipient's email address is required. Please try again.")

        while True:
            subject = input("Subject: ")
            if subject != "":
                break
            else:
                print("Subject is required. Please try again.")

        content = input("Email content: ")

        attachments = []
        has_attachment = False  # Flag to track attachment status

        while True:
            print("Example attachment path: /path/to/attachment.txt")
            attachment = input("Enter attachment path (leave empty to finish): ")

            if not attachment:
                if has_attachment:
                    another_attachment = input("Do you want to add another attachment? (yes/no): ")
                    if another_attachment.lower() == "no":
                        break
                else:
                    break

            if os.path.isfile(attachment):
                attachments.append(attachment)
                has_attachment = True  # Set the flag to True when attachment is added
                print("Attachment added successfully.")
            else:
                print("Invalid attachment path. Please try again.")

        # Create a new Email object with the provided information and add it to the inbox
        email = cls(sender, recipient, subject, content, attachments=attachments)
        cls.__inbox.append(email)
        print("Email sent successfully!")

    def open_attachments(self):
        # Open the attachments associated with the email
        if self.attachments:
            print("\nAttachments:")
            for attachment in self.attachments:
                print(attachment)
                try:
                    subprocess.run(['start', '', attachment], shell=True)
                except Exception as e:
                    print(f"Failed to open attachment: {str(e)}")
        else:
            print("No attachments.")

    def __repr__(self):
        # Return a string representation of the Email object
        return self.__str__()

# --- Functions --- #
def list_emails():
    # Display the list of emails in the inbox
    inbox = Email.get_inbox()
    print("\nInbox:")
    for index, email in enumerate(inbox, start=1):
        status = "Read" if email.has_been_read else "Unread"
        print(f"{index}. {status} - {email.subject_line}")

def read_email(index):
    # Read the email at the specified index in the inbox
    while True:
        try:
            email = Email.get_email(index - 1)
            print("\nEmail Details:\n")
            print(email)
            email.mark_as_read()

            if email.attachments:
                while True:
                    open_attachments = input("Do you want to open the attachment(s)? (yes/no): ")
                    if open_attachments.lower() == "yes":
                        email.open_attachments()
                        break
                    elif open_attachments.lower() == "no":
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")

            print(f"\nEmail from {email.senders_email} has been marked as read.")
            break  
        except IndexError:
            print("Invalid email number.\n")
            index = int(input("Enter the email number you want to read: "))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            break

# --- Email Program --- #
print("\nWelcome to the Email Simulator!")

Email.populate_inbox()  # Populate the inbox with sample emails

menu = True

while menu:
    try:
        user_choice = int(input('''\nWould you like to:

1. Read an email
2. View unread emails
3. Send an email
4. Delete an email
5. Quit application

Enter selection: '''))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if user_choice == 1:
        # Display the list of emails in the inbox
        list_emails()
        while True:
            try:
                index = int(input("\nEnter the email number you want to read: "))
                read_email(index)  # Read the email at the specified index
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
            except IndexError as e:
                print(str(e))

    elif user_choice == 2:
        # Display the list of unread emails in the inbox
        print("\nUnread Emails:\n")
        inbox = Email.get_inbox()
        unread_emails_count = 0
        for index, email in enumerate(inbox, start=1):
            if not email.has_been_read:
                print(f"{index}. {email.subject_line}")
                unread_emails_count += 1

        if unread_emails_count == 0:
            print("You have no more unread emails.")

    elif user_choice == 3:
        Email.send_email()  # Send a new email

    elif user_choice == 4:
        # Display the list of emails in the inbox
        list_emails()
        while True:
            try:
                index = int(input("\nEnter the email number you want to delete: "))
                Email.delete_email(index - 1)  # Delete the email at the specified index
                print("\nEmail deleted successfully.")
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
            except IndexError as e:
                print(str(e))

    elif user_choice == 5:
        menu = False
        print("Thank you for using the Email Simulator. Goodbye!")

    else:
        print("Invalid input. Please enter a number between 1 and 5.")
