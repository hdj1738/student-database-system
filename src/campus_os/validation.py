def get_valid_input(prompt, value_type, positive=False):
    while True:
        try:
            value = value_type(input(prompt))

            if not value:
                print("Cannot be empty.")
                continue
            
            if value_type == str:
                if value.strip()=="":
                    print("Cannot be empty or whitespace.")
                    continue

            if positive and value <= 0:
                print("Value must be positive.")
                continue

            if "name" in prompt.lower() and (not any(char.isalpha() for char in value)
                    or any(not (char.isalpha() or char.isspace() or char in "-.'") for char in value)):
                print("Enter valid text using letters, spaces, apostrophes, or hyphens.")
                continue

            return value

        except ValueError:
            print("Invalid type. Try again.")
        

def get_valid_marks():
    while True:
        try:
            marks_input = input(
                "Enter student marks (e.g. Math,90 Python,85): "
            )

            if not marks_input.strip():
                print("Marks cannot be empty.")
                continue

            marks = marks_input.split()
            format_marks = {}

            for item in marks:
                subject, mark = item.split(",")
                mark = int(mark)

                if mark < 0 or mark > 100:
                    print("Marks must be between 0 and 100.")
                    break

                if not subject:
                    print("Subject cannot be empty.")
                    break

                format_marks[subject] = mark

            else:
                return format_marks

        except ValueError:
            print("Invalid format. Use Subject,Mark (e.g. Math,90).")