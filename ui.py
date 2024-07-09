# ui.py
# A3
# Replace the following placeholders with your information.

# Kathleen Pham
# kathlep3@uci.edu
# 79281883
from pathlib import Path
from Profile import Profile, Post
import os


def printDirectories(directory):
    myPath = Path(directory)
    print(myPath)
    for currentPath in myPath.iterdir():
        if currentPath.is_file():
            print(currentPath)
        elif currentPath.is_dir():
            printDirectories(currentPath)


def outputFiles(directory):
    myPath = Path(directory)
    for currentPath in myPath.iterdir():
        if currentPath.is_file():
            print(currentPath)


def searchFile(directory, inputt):
    myPath = Path(directory)
    for currentPath in myPath.iterdir():
        if currentPath.is_file():
            if inputt in str(currentPath):
                print(currentPath)


def outputFileExtension(directory, extension):
    myPath = Path(directory)
    for currentPath in myPath.iterdir():
        if currentPath.is_file():
            filename = str(currentPath)
            if filename.endswith("." + extension):
                print(currentPath)


def deleteFile(file):
    path = Path(file)
    contentCheck = os.stat(file).st_size
    if contentCheck == 0:
        print("EMPTY")
    elif contentCheck != 0:
        if file.endswith('.dsu') and os.path.exists(file):
            os.remove(path)
            print(file, "DELETED")
        elif not file.endswith('.dsu'):
            raise ValueError()


def readFile(file):
    path = Path(file)
    contentCheck = os.stat(file).st_size
    if contentCheck == 0:
        print("EMPTY")
    elif contentCheck != 0:
        if file.endswith('.dsu') and os.path.exists(file):
            fileContent = path.read_text()
            print(fileContent)
        elif not file.endswith('.dsu'):
            raise ValueError()


def allprofile(pathString):
    profile = Profile()
    profile.load_profile(pathString)
    print()
    print("Username:")
    print(profile.username)
    print()
    print("Password:")
    print(profile.password)
    print()
    print("Bio:")
    print(profile.bio)
    print()
    allposts(pathString)


def allposts(pathString):
    profile = Profile()
    post = Post()
    profile.load_profile(pathString)
    print("All Posts:")
    print("__________________")
    posts = profile._posts
    i = 0
    for post in posts:
        print("Post ID:", i)
        print("Entry:", post.entry)
        print("Timestamp:", post.timestamp)
        i += 1
        print()


def commandC(input1, input3):
    path_loc = "."
    NOTES = input1 + input3 + ".dsu"
    myPath = Path(path_loc)/NOTES
    if myPath.exists() is False:
        myPath.touch(exist_ok=True)
    elif myPath.exists() is True:
        print("File already exists.")
    profile = Profile()
    profile.username = input("Username: ")
    profile.password = input("Password: ")
    profile.bio = input("Enter a bio: ")
    pathString = str(myPath)
    profile.save_profile(pathString)
    return pathString


def commandO(pathString):
    profile = Profile()
    profile.load_profile(pathString)
    print()
    print("This is your existing profile:")
    print("________________________")
    allprofile(pathString)
    return pathString


def commandE(cmdLine, pathString):
    cleanInput = []
    current_item = ""
    in_quotes = False
    profile = Profile()
    profile.load_profile(pathString)
    username = profile.username
    password = profile.password
    for char in cmdLine:
        if char == '"' or char == "'":
            in_quotes = not in_quotes
        elif char == " " and not in_quotes:
            if current_item:
                cleanInput.append(current_item)
                current_item = ""
        else:
            current_item += char
    if current_item:
        cleanInput.append(current_item)

    edited = False

    for i in range(len(cleanInput)):
        if cleanInput[i] == "-usr":
            username = cleanInput[i+1]
            profile.username = username.replace(" ", "x")
            print("Success! Here is your new username:\n" + profile.username + "\n")
            edited = True

        if cleanInput[i] == "-pwd":
            password = cleanInput[i+1]
            profile.password = password.replace(" ", "_")
            print("Success! Here is your new password:\n" + profile.password + "\n")
            edited = True

        if cleanInput[i] == "-bio":
            try:
                profile.bio = cleanInput[i+1]
                print("Success! Here is your new bio:\n" + profile.bio + "\n")

                bio = profile.bio
                server = input("Please enter server:\n")
                port = int(input("Please enter port:\n"))
                send_post(server, port, username=username, password=password, message=None, bio=bio)
                edited = True
            except IndexError as e:
                print("Error. You cannot have an empty bio. Try again.")
                print()

        if cleanInput[i] == "-addpost":
            try:
                entry = cleanInput[i+1]
                new_post = Post(entry)
                profile.add_post(new_post)
                print("\nThis was your post:\n" + entry)
                print()
                print("These were your post details:\n", new_post)
                print()
                server = input("Please enter server:\n")
                port = int(input("Please enter port:\n"))
                send_post(server, port, username=username, password=password, message=new_post)
                edited = True
            except IndexError as e:
                print("Error. You cannot have an empty post. Try again.")
                print()

        if cleanInput[i] == "-delpost":
            index = int(cleanInput[i+1])
            profile.del_post(index)
            print("Post", index, "deleted.")
            edited = True

    if edited:
        profile.save_profile(pathString)

    if not edited:
        print("Invalid command. Please try again.")


def commandP(cmdLine, pathString):
    cleanInput = cmdLine.split(' ')
    profile = Profile()
    profile.load_profile(pathString)
    for i in range(len(cleanInput)):
        if cleanInput[i] == "-usr":
            print("Username:")
            print(profile.username)
            print()
        if cleanInput[i] == "-pwd":
            print("Password:")
            print(profile.password)
            print()
        if cleanInput[i] == "bio":
            print("Bio:")
            print(profile.bio)
            print()
        if cleanInput[i] == "-all":
            print("All Profile Content:")
            allprofile(pathString)
            allposts(pathString)
            print()
        if cleanInput[i] == "-posts":
            allposts(pathString)
            print()
        if cleanInput[i] == "-post":
            index = int(cleanInput[i+1])
            print(f"Post {index}:")
            print(profile._posts[i+1])
            print()


if __name__ == "__main__":
    commandC("TestFolder/", "anothertest")