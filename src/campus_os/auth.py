from campus_os.students import Password, Student
from campus_os.validation import get_valid_input
from campus_os.cli import main

if __name__=="__main__":        
    while True:
        pswd = get_valid_input("Enter password: ", str)
        password = Password(pswd)
        if password.pw == "hiralissocool":
            main()
            break
        print("Incorrect password.")