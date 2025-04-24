import os
import matplotlib.pyplot as plt

DATA_DIR = 'data'

def load_students():
    students = {}
    with open(os.path.join(DATA_DIR, 'students.txt')) as f:
        for line in f:
            line = line.strip()
            if line:
                sid = line[:3]
                name = line[3:]
                students[name] = sid
    return students

def load_assignments():
    assignments = {}
    id_to_name = {}
    points = {}
    with open(os.path.join(DATA_DIR, 'assignments.txt')) as f:
        lines = [line.strip() for line in f if line.strip()]
        for i in range(0, len(lines), 3):
            name = lines[i]
            aid = lines[i+1]
            pts = int(lines[i+2])
            assignments[name] = aid
            id_to_name[aid] = name
            points[aid] = pts
    return assignments, id_to_name, points

def load_submissions():
    submissions = {}
    submissions_dir = os.path.join(DATA_DIR, 'submissions')
    for filename in os.listdir(submissions_dir):
        filepath = os.path.join(submissions_dir, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line:
                    sid, aid, percent = line.split('|')
                    sid = sid.strip()
                    aid = aid.strip()
                    percent = percent.strip()
                    if sid not in submissions:
                        submissions[sid] = {}
                    submissions[sid][aid] = float(percent)
    return submissions


def student_grade(students, assignments, points, submissions):
    name = input("What is the student's name: ")
    if name not in students:
        print("Student not found")
        return
    sid = students[name]
    total_earned = 0
    total_possible = 0
    for aid in points:
        if sid in submissions and aid in submissions[sid]:
            score = submissions[sid][aid]
            earned = points[aid] * score / 100.0
            total_earned += earned
        total_possible += points[aid]
    percent = round(100 * total_earned / total_possible)
    print(f"{percent}%")

def assignment_stats(assignments, id_to_name, points, submissions):
    name = input("What is the assignment name: ")
    if name not in assignments:
        print("Assignment not found")
        return
    aid = assignments[name]
    scores = []
    for sid in submissions:
        if aid in submissions[sid]:
            scores.append(submissions[sid][aid])
    if scores:
        print(f"Min: {round(min(scores))}%")
        print(f"Avg: {int(sum(scores) / len(scores))}%")

        print(f"Max: {round(max(scores))}%")
    else:
        print("No submissions for this assignment.")

def assignment_graph(assignments, id_to_name, points, submissions):
    name = input("What is the assignment name: ")
    if name not in assignments:
        print("Assignment not found")
        return
    aid = assignments[name]
    scores = []
    for sid in submissions:
        if aid in submissions[sid]:
            scores.append(submissions[sid][aid])
    if not scores:
        print("No submissions for this assignment.")
        return
    plt.hist(scores, bins=[0,25,50,75,100])
    plt.title(f'Scores for {name}')
    plt.xlabel('Score (%)')
    plt.ylabel('Number of Students')
    plt.show()

def main():
    students = load_students()
    assignments, id_to_name, points = load_assignments()
    submissions = load_submissions()
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("Enter your selection: ")
    if choice == '1':
        student_grade(students, assignments, points, submissions)
    elif choice == '2':
        assignment_stats(assignments, id_to_name, points, submissions)
    elif choice == '3':
        assignment_graph(assignments, id_to_name, points, submissions)

if __name__ == '__main__':
    main()
