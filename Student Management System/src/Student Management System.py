import json

Data_File = "students.json"

def load_data():
    try:
        with open(Data_File, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(Data_File, "w") as f:
        json.dump(data, f, indent=4)


def add_student():
    data = load_data()
    student_id = int(input("Enter your student ID: "))
    if student_id in data:
        print("The student Id already exists.")
        return
    name = input("Enter your name: ")
    last_name = input("Enter the last name: ")
    major = input("Please enter your major: ")
    age = input("Enter your age: ")
    data[student_id] = {"name": name, "last_name":last_name, "major":major, "age": age, "grades":[]}
    save_data(data)
    print("student added successfully.")
    
    
    
    
def add_grade():
    data = load_data
    student_id = int(input("student ID: "))
    if student_id not in load_data:
        print("student not found.")
        return
    grade = float(input("Grade: "))
    data[student_id]["grades"].append(grade)
    save_data(data)
    print("Grade added successfully.")
    
    
def calculate_gpa():
    data = load_data
    student_id = int(input("student ID: "))
    if student_id not in load_data:
        print("student not found.")
        return
    grades = data[student_id]["grades"]
    if not grades:
        print("There is not any grades for this student.")
        return
    
    gpa = sum(grades) / len(grades)
    print(f"GPA for {data[student_id]['name']}{data[student_id]['last_name']} = {gpa:.2f}")
    
    
def show_students():
    data = load_data()
    if not data:
        print("No student found in system.")
        return
    print("\nID   | First Name | Last Name  | Major       | Age | Grades")
    print("-----|------------|------------|-------------|-----|-----------------")
    
    for student_id, info in data.items():
         print(f"{student_id:<4} | {info['name']:<11} | {info['last_name']:<10} | {info['major']:<11} | {info['age']:<3} | {info['grades']}")
         
         
         
def main():
    while True:
        print("Student Management System")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. Calculate GPA")
        print("4. Show All Students")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_grade()
        elif choice == "3":
            calculate_gpa()
        elif choice == "4":
            show_students()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
            
            
if __name__ == "__main__":
    main()
           

        
    