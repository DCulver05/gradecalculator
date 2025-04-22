import matplotlib.pyplot as plt

# Step 1: Reading files

def read_students(filename):
    students = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 3:
                students[parts[1] + " " + parts[2]] = parts[0]  # student name -> student ID
            else:
                print(f"Skipping invalid student line: {line.strip()}")
    return students


def read_assignments(filename):
    assignments = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.split()
            assignments[parts[0]] = (parts[1], int(parts[2]))  # assignment ID -> (name, max points)
    return assignments

def read_submissions(filename):
    submissions = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.split()
            student_id = parts[0]
            assignment_id = parts[1]
            score = int(parts[2])
            submissions[(student_id, assignment_id)] = score
    return submissions

# Step 2: Option 1 - Student Grade Calculation

def student_grade(students, submissions, assignments):
    student_name = input("What is the student's name: ")
    student_id = students.get(student_name, None)

    if not student_id:
        print("Student not found")
        return

    total_points = 0
    total_possible = 1000
    for key, score in submissions.items():
        if key[0] == student_id:
            assignment_id = key[1]
            total_points += score * assignments[assignment_id][1] / 100

    grade = round((total_points / total_possible) * 100)
    print(f"{grade}%")

# Step 3: Option 2 - Assignment Statistics

def assignment_statistics(assignments, submissions):
    assignment_name = input("What is the assignment name: ")
    assignment_id = None
    for key, value in assignments.items():
        if value[0] == assignment_name:
            assignment_id = key
            break

    if not assignment_id:
        print("Assignment not found")
        return

    scores = []
    for key, score in submissions.items():
        if key[1] == assignment_id:
            scores.append(score)

    min_score = min(scores)
    max_score = max(scores)
    avg_score = sum(scores) / len(scores)

    print(f"Min: {min_score}%")
    print(f"Avg: {round(avg_score)}%")
    print(f"Max: {max_score}%")

# Step 4: Option 3 - Assignment Graph (Histogram)

def assignment_graph(assignments, submissions):
    assignment_name = input("What is the assignment name: ")
    assignment_id = None
    for key, value in assignments.items():
        if value[0] == assignment_name:
            assignment_id = key
            break

    if not assignment_id:
        print("Assignment not found")
        return

    scores = []
    for key, score in submissions.items():
        if key[1] == assignment_id:
            scores.append(score)

    # Plotting histogram
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Scores for {assignment_name}")
    plt.xlabel("Score Percentage")
    plt.ylabel("Number of Students")
    plt.show()

# Step 5: Main Program to Handle Menu and User Input

def main():
    # Reading data files
    students = read_students("data/students.txt")
    assignments = read_assignments("data/assignments.txt")
    submissions = read_submissions("data/submissions.txt")

    # Menu loop
    while True:
        print("1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        selection = int(input("Enter your selection: "))

        if selection == 1:
            student_grade(students, submissions, assignments)
        elif selection == 2:
            assignment_statistics(assignments, submissions)
        elif selection == 3:
            assignment_graph(assignments, submissions)
        else:
            print("Invalid selection")
            break

if __name__ == "__main__":
    main()
