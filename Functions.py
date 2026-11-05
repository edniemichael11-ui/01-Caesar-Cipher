
import os
import time


def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def Main_Menu():
    """Displays the main menu."""
    print("CAESAR CIPHER MESSAGING")
    print("-----------------------")
    print("1. Start a message")
    print("2. Read and reply to a message")
    print("3. Quit")


def get_user_input_Main_menu():
    """Gets and validates the main menu choice."""
    while True:
        action = input("Enter your choice: ").strip()
        if action in ("1", "2", "3"):
            return action
        print("Invalid choice. Try again.")


def get_alphabet():
    """Gets and validates the supported characters."""
    while True:
        alphabet = input("Enter supported characters: ")
        if not alphabet or "\n" in alphabet:
            print("Alphabet cannot be empty.")
        elif len(set(alphabet)) != len(alphabet):
            print("Alphabet cannot contain duplicates.")
        else:
            return alphabet


def get_shift():
    """Gets an integer shift from the user."""
    while True:
        try:
            return int(input("Enter shift: "))
        except ValueError:
            print("Invalid shift. Enter an integer.")


def encrypt(message, alphabet, shift):
    """Encrypts or decrypts a message using a Caesar cipher."""
    result = []
    for character in message:
        if character in alphabet:
            index = alphabet.index(character)
            result.append(alphabet[(index + shift) % len(alphabet)])
        else:
            result.append(character)
    return "".join(result)


def get_user_message(prompt="Enter your message: "):
    """Gets a nonempty, single-line message."""
    while True:
        message = input(prompt)
        if message.strip() and "\n" not in message:
            return message
        print("Message cannot be empty.")


def get_file_path():
    """Gets a filename ending in .txt."""
    filename = input("Enter filename: ").strip()
    if not filename.lower().endswith(".txt"):
        filename += ".txt"
    return filename


def confirm_overwrite(filename):
    """Asks permission before overwriting an existing file."""
    if not os.path.exists(filename):
        return True
    while True:
        answer = input("File exists. Overwrite? (Y/N): ").strip().upper()
        if answer == "Y":
            return True
        if answer == "N":
            return False
        print("Enter Y or N.")


def save_new_file(filename, alphabet, shift, message):
    """Creates a conversation file and saves its first message."""
    with open(filename, "w") as file:
        file.write(f"{alphabet}\n{shift}\n{message}\n")


def createMessage():
    """Creates a new conversation and saves its first message."""
    alphabet = get_alphabet()
    shift = get_shift()
    message = get_user_message()
    encrypted = encrypt(message, alphabet, shift)
    filename = get_file_path()
    if not confirm_overwrite(filename):
        print("File was not created.")
        return
    save_new_file(filename, alphabet, shift, encrypted)
    print("Encrypted message:", encrypted)
    print(f"Message saved to {filename}!")


def find_file():
    """Finds a conversation file or returns to the menu."""
    while True:
        filename = input("Enter filename (M for main menu): ").strip()
        if filename.upper() == "M":
            return None
        if not filename.lower().endswith(".txt"):
            filename += ".txt"
        if os.path.isfile(filename):
            return filename
        print(f"Error: File '{filename}' was not found.")


def load_file(filename):
    """Reads and validates conversation settings and messages."""
    with open(filename, "r") as file:
        lines = file.readlines()
    if len(lines) < 3:
        raise ValueError("Conversation file is incomplete.")
    alphabet = lines[0].rstrip("\n")
    shift = int(lines[1].strip())
    if not alphabet or len(set(alphabet)) != len(alphabet):
        raise ValueError("Invalid alphabet in conversation file.")
    return alphabet, shift, [line.rstrip("\n") for line in lines[2:]]


def display_messages(messages, alphabet, shift):
    """Decrypts and displays all messages in order."""
    print("\nMESSAGES")
    print("--------")
    for number, message in enumerate(messages, start=1):
        print(f"{number}. {encrypt(message, alphabet, -shift)}")


def append_reply(filename, encrypted):
    """Appends an encrypted reply without erasing earlier messages."""
    with open(filename, "a") as file:
        file.write(encrypted + "\n")


def replyToMessage(filename, alphabet, shift):
    """Gets, encrypts, and saves a reply."""
    print("\nSupported characters:")
    print(alphabet)
    reply = get_user_message("Enter your reply: ")
    encrypted = encrypt(reply, alphabet, shift)
    print("Encrypted message:", encrypted)
    append_reply(filename, encrypted)
    print(f"Message saved to {filename}!")


def readMessages():
    """Loads a conversation and displays its messages."""
    filename = find_file()
    if filename is None:
        print("Returning to main menu...")
        return
    try:
        alphabet, shift, messages = load_file(filename)
        display_messages(messages, alphabet, shift)
        replyToMessage(filename, alphabet, shift)
    except (OSError, ValueError, IndexError):
        print("Error: Invalid conversation file.")


def main():
    """Runs the main menu and controls the program."""
    while True:
        clear_screen()
        Main_Menu()
        choice = get_user_input_Main_menu()
        if choice == "1":
            clear_screen()
            createMessage()
        elif choice == "2":
            clear_screen()
            readMessages()
            time.sleep(5)
        else:
            print("Goodbye!")
            break
