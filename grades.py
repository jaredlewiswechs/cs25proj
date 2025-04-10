import json
import os

import match
import matplotlib.pyplot as plt
from datetime import datetime
import statistics


class GradeTracker:
    def __init__(self, data_file="grades.json"):
        self.data_file = data_file
        self.grades = {}
        self.load_grades()

    def print_banner(self):
        """Display welcome banner with version and date"""
        print("\n🎓==============================🎓")
        print("     STUDENT GRADE TRACKER")
        print("          Version 2.0")
        print(f"        {datetime.now().strftime('%Y-%m-%d')}")
        print("🎓==============================🎓\n")

    def save_grades(self):
        """Save grades to JSON file with backup"""
        # Create backup of existing file
        if os.path.exists(self.data_file):
            backup_file = f"{self.data_file}.bak"
            try:
                os.replace(self.data_file, backup_file)
                print(f"📋 Backup created: {backup_file}")
            except OSError as e:
                print(f"⚠️ Could not create backup: {e}")

        # Save current data
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.grades, f, indent=2)
            print(f"💾 Grades saved to {self.data_file}")
            return True
        except (IOError, OSError) as e:
            print(f"❌ Error saving grades: {e}")
            return False

    def load_grades(self):
        """Load grades from file or use empty dict if not found"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as f:
                    self.grades = json.load(f)
                print(f"✅ Loaded {len(self.grades)} student records from file.")
            else:
                print("📂 No saved file found. Starting with empty gradebook.")
                self.grades = {}
        except json.JSONDecodeError:
            print("⚠️ Error reading file. File may be corrupted.")
            if os.path.exists(f"{self.data_file}.bak"):
                choice = input("Would you like to restore from backup? (y/n): ").lower()
                if choice == 'y':
                    try:
                        with open(f"{self.data_file}.bak", "r") as f:
                            self.grades = json.load(f)
                        print(f"✅ Restored {len(self.grades)} student records from backup.")
                    except:
                        print("❌ Could not restore from backup.")
                        self.grades = {}
            else:
                self.grades = {}

    def add_student(self):
        """Add a new student to the gradebook"""
        name = input("👤 Enter new student name: ").strip().title()
        if not name:
            print("⚠️ Student name cannot be empty.")
            return

        if name in self.grades:
            print(f"⚠️ Student '{name}' already exists.")
            return

        self.grades[name] = []
        print(f"✅ Added student: {name}")

    def add_grade(self):
        """Add a grade for an existing student"""
        if not self.grades:
            print("⚠️ No students in system. Please add a student first.")
            return

        # Show student list
        self.list_students()

        name = input("👤 Enter student name or number: ").strip()

        # Handle numeric selection
        try:
            if name.isdigit() and 1 <= int(name) <= len(self.grades):
                name = list(self.grades.keys())[int(name) - 1]
        except (ValueError, IndexError):
            pass

        # Find student (case insensitive)
        student_found = None
        for student in self.grades:
            if student.lower() == name.lower():
                student_found = student
                break

        if student_found:
            try:
                grade_input = input(f"✏️ Enter grade for {student_found} (0-100): ")
                grade = float(grade_input)

                if 0 <= grade <= 100:
                    self.grades[student_found].append(grade)
                    print(f"✅ Added grade {grade} for {student_found}")

                    # Ask if user wants to add more grades for this student
                    more = input("Add another grade for this student? (y/n): ").lower()
                    if more == 'y':
                        self.add_multiple_grades(student_found)
                else:
                    print("⚠️ Grade must be between 0 and 100.")
            except ValueError:
                print("⚠️ Please enter a valid number.")
        else:
            print(f"🚫 Student '{name}' not found.")
            create = input("Would you like to add this student? (y/n): ").lower()
            if create == 'y':
                self.grades[name.title()] = []
                print(f"✅ Added student: {name.title()}")
                more = input("Add grades for this student now? (y/n): ").lower()
                if more == 'y':
                    self.add_multiple_grades(name.title())

    def add_multiple_grades(self, student):
        """Add multiple grades for a student in one go"""
        print(f"Enter grades for {student} (press Enter with no input to finish)")

        count = 0
        while True:
            try:
                grade_input = input(f"Grade {count + 1}: ")
                if not grade_input:
                    break

                grade = float(grade_input)
                if 0 <= grade <= 100:
                    self.grades[student].append(grade)
                    count += 1
                else:
                    print("⚠️ Grade must be between 0 and 100.")
            except ValueError:
                print("⚠️ Please enter a valid number.")

        if count > 0:
            print(f"✅ Added {count} grades for {student}")

    def list_students(self):
        """Display numbered list of students"""
        if not self.grades:
            print("⚠️ No students in system.")
            return

        print("\n👥 Students:")
        for i, student in enumerate(self.grades.keys(), 1):
            print(f"{i}. {student}")
        print()

    def view_grades(self):
        """View all student grades with statistics"""
        if not self.grades:
            print("⚠️ No students in system.")
            return

        print("\n📊 Gradebook:")
        print("=" * 60)
        print(f"{'Student':<20} | {'Grades':<25} | {'Avg':<5} | {'Min':<4} | {'Max':<4}")
        print("-" * 60)

        for student, grades_list in self.grades.items():
            if grades_list:
                avg = statistics.mean(grades_list)
                min_grade = min(grades_list)
                max_grade = max(grades_list)
                grades_display = ', '.join(f"{g:.1f}" for g in grades_list)

                # Truncate long grade lists for display
                if len(grades_display) > 25:
                    grades_display = grades_display[:22] + "..."

                print(f"{student:<20} | {grades_display:<25} | {avg:5.1f} | {min_grade:4.1f} | {max_grade:4.1f}")
            else:
                print(f"{student:<20} | No grades entered yet")
        print("=" * 60)

        # Show class statistics
        all_grades = [g for grades in self.grades.values() for g in grades]
        if all_grades:
            class_avg = statistics.mean(all_grades)
            print(f"\n📈 Class average: {class_avg:.1f}")

            # Count grade distribution
            a_count = sum(1 for g in all_grades if g >= 90)
            b_count = sum(1 for g in all_grades if 80 <= g < 90)
            c_count = sum(1 for g in all_grades if 70 <= g < 80)
            d_count = sum(1 for g in all_grades if 60 <= g < 70)
            f_count = sum(1 for g in all_grades if g < 60)

            print(f"📊 Grade distribution: A: {a_count}, B: {b_count}, C: {c_count}, D: {d_count}, F: {f_count}")

    def visualize_grades(self):
        """Create visualization options"""
        if not self.grades or not any(self.grades.values()):
            print("⚠️ No grades to visualize.")
            return

        print("\n📊 Visualization Options:")
        print("1. Student Averages Bar Chart")
        print("2. Grade Distribution Pie Chart")
        print("3. Individual Student Performance")
        print("4. Class Performance Over Time")
        print("5. Back to Main Menu")

        choice = input("Select visualization type: ").strip()

        if choice == "1":
            self.plot_averages()
        elif choice == "2":
            self.plot_distribution()
        elif choice == "3":
            self.plot_student_performance()
        elif choice == "4":
            self.plot_class_performance()
        elif choice == "5":
            return
        else:
            print("❌ Invalid choice.")

    def plot_averages(self):
        """Plot average grade for each student"""
        students = []
        averages = []

        for student, grades_list in self.grades.items():
            if grades_list:  # Only include students with grades
                students.append(student)
                averages.append(statistics.mean(grades_list))

        if not students:
            print("⚠️ No student grades to plot.")
            return

        plt.figure(figsize=(10, 6))
        bars = plt.bar(students, averages, color='skyblue', edgecolor='blue')
        plt.title("📊 Student Average Grades", fontsize=14, fontweight='bold')
        plt.ylabel("Average Grade")
        plt.ylim(0, 100)
        plt.axhline(y=90, color='green', linestyle='--', alpha=0.5)
        plt.axhline(y=80, color='orange', linestyle='--', alpha=0.5)
        plt.axhline(y=70, color='red', linestyle='--', alpha=0.5)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Add labels on top of bars
        for bar, avg in zip(bars, averages):
            plt.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height() + 1,
                     f"{avg:.1f}", ha='center', fontweight='bold')

        plt.tight_layout()

        filename = "averages_chart.png"
        plt.savefig(filename)
        plt.show()
        print(f"✅ Chart saved as '{filename}'")

    def plot_distribution(self):
        """Plot grade distribution as pie chart"""
        # Get all grades
        all_grades = [g for grades in self.grades.values() for g in grades]

        if not all_grades:
            print("⚠️ No grades to plot.")
            return

        # Count grade distribution
        a_count = sum(1 for g in all_grades if g >= 90)
        b_count = sum(1 for g in all_grades if 80 <= g < 90)
        c_count = sum(1 for g in all_grades if 70 <= g < 80)
        d_count = sum(1 for g in all_grades if 60 <= g < 70)
        f_count = sum(1 for g in all_grades if g < 60)

        # Create pie chart
        labels = ['A (90-100)', 'B (80-89)', 'C (70-79)', 'D (60-69)', 'F (0-59)']
        sizes = [a_count, b_count, c_count, d_count, f_count]
        colors = ['green', 'lightgreen', 'yellow', 'orange', 'red']
        explode = (0.1, 0, 0, 0, 0)  # explode the 'A' slice

        plt.figure(figsize=(10, 8))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title("📊 Grade Distribution", fontsize=14, fontweight='bold')

        filename = "grade_distribution.png"
        plt.savefig(filename)
        plt.show()
        print(f"✅ Chart saved as '{filename}'")

    def plot_student_performance(self):
        """Plot individual student performance"""
        self.list_students()

        name = input("👤 Enter student name or number: ").strip()

        # Handle numeric selection
        try:
            if name.isdigit() and 1 <= int(name) <= len(self.grades):
                name = list(self.grades.keys())[int(name) - 1]
        except (ValueError, IndexError):
            pass

        # Find student (case insensitive)
        student_found = None
        for student in self.grades:
            if student.lower() == name.lower():
                student_found = student
                break

        if not student_found:
            print(f"🚫 Student '{name}' not found.")
            return

        grades_list = self.grades[student_found]
        if not grades_list:
            print(f"⚠️ No grades recorded for {student_found}.")
            return

        # Create progress plot
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(grades_list) + 1), grades_list, 'o-', linewidth=2, markersize=8)
        plt.title(f"📈 {student_found}'s Grade Progress", fontsize=14, fontweight='bold')
        plt.xlabel("Assignment Number")
        plt.ylabel("Grade")
        plt.ylim(0, 100)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Add horizontal lines for grade boundaries
        plt.axhline(y=90, color='green', linestyle='--', alpha=0.5, label='A')
        plt.axhline(y=80, color='blue', linestyle='--', alpha=0.5, label='B')
        plt.axhline(y=70, color='orange', linestyle='--', alpha=0.5, label='C')
        plt.axhline(y=60, color='red', linestyle='--', alpha=0.5, label='D')

        plt.legend()
        plt.tight_layout()

        filename = f"{student_found.lower().replace(' ', '_')}_progress.png"
        plt.savefig(filename)
        plt.show()
        print(f"✅ Chart saved as '{filename}'")

    def plot_class_performance(self):
        """Plot class performance over time (average per assignment)"""
        # Get maximum number of assignments for any student
        max_assignments = max((len(grades) for grades in self.grades.values()), default=0)

        if max_assignments == 0:
            print("⚠️ No grades to plot.")
            return

        # Initialize lists to store averages
        assignment_avgs = []

        # Calculate average for each assignment number
        for i in range(max_assignments):
            grades_for_assignment = [
                grades[i] for student, grades in self.grades.items()
                if i < len(grades)
            ]

            if grades_for_assignment:
                assignment_avgs.append(statistics.mean(grades_for_assignment))
            else:
                assignment_avgs.append(0)

        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, max_assignments + 1), assignment_avgs, 'o-',
                 linewidth=2, markersize=8, color='blue')
        plt.title("📊 Class Performance by Assignment", fontsize=14, fontweight='bold')
        plt.xlabel("Assignment Number")
        plt.ylabel("Class Average")
        plt.ylim(0, 100)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(range(1, max_assignments + 1))

        # Add horizontal lines for grade boundaries
        plt.axhline(y=90, color='green', linestyle='--', alpha=0.5)
        plt.axhline(y=80, color='orange', linestyle='--', alpha=0.5)
        plt.axhline(y=70, color='red', linestyle='--', alpha=0.5)

        plt.tight_layout()

        filename = "class_performance.png"
        plt.savefig(filename)
        plt.show()
        print(f"✅ Chart saved as '{filename}'")

    def remove_student(self):
        """Remove a student from the gradebook"""
        if not self.grades:
            print("⚠️ No students in system.")
            return

        # Show student list
        self.list_students()

        name = input("👤 Enter student name or number to remove: ").strip()

        # Handle numeric selection
        try:
            if name.isdigit() and 1 <= int(name) <= len(self.grades):
                name = list(self.grades.keys())[int(name) - 1]
        except (ValueError, IndexError):
            pass

        # Find student (case insensitive)
        student_found = None
        for student in self.grades:
            if student.lower() == name.lower():
                student_found = student
                break

        if student_found:
            confirm = input(f"❗ Are you sure you want to remove {student_found}? (y/n): ").lower()
            if confirm == 'y':
                del self.grades[student_found]
                print(f"✅ Removed student: {student_found}")
        else:
            print(f"🚫 Student '{name}' not found.")

    def export_report(self):
        """Export gradebook as text report"""
        if not self.grades:
            print("⚠️ No data to export.")
            return

        filename = input("Enter report filename (without extension): ").strip() or "grade_report"
        filename = f"{filename}.txt"

        try:
            with open(filename, "w") as f:
                f.write("STUDENT GRADE REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")

                # Write student data
                for student, grades_list in self.grades.items():
                    f.write(f"Student: {student}\n")
                    f.write("-" * 30 + "\n")

                    if grades_list:
                        avg = statistics.mean(grades_list)
                        min_grade = min(grades_list)
                        max_grade = max(grades_list)

                        f.write(f"Grades: {', '.join(str(g) for g in grades_list)}\n")
                        f.write(f"Average: {avg:.2f}\n")
                        f.write(f"Minimum: {min_grade:.2f}\n")
                        f.write(f"Maximum: {max_grade:.2f}\n")

                        # Determine letter grade
                        letter = "A" if avg >= 90 else "B" if avg >= 80 else "C" if avg >= 70 else "D" if avg >= 60 else "F"
                        f.write(f"Letter Grade: {letter}\n")
                    else:
                        f.write("No grades recorded.\n")

                    f.write("\n")

                # Write class summary
                all_grades = [g for grades in self.grades.values() for g in grades]
                if all_grades:
                    f.write("\nCLASS SUMMARY\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Class Average: {statistics.mean(all_grades):.2f}\n")
                    f.write(f"Highest Grade: {max(all_grades):.2f}\n")
                    f.write(f"Lowest Grade: {min(all_grades):.2f}\n")

                    # Count grade distribution
                    a_count = sum(1 for g in all_grades if g >= 90)
                    b_count = sum(1 for g in all_grades if 80 <= g < 90)
                    c_count = sum(1 for g in all_grades if 70 <= g < 80)
                    d_count = sum(1 for g in all_grades if 60 <= g < 70)
                    f_count = sum(1 for g in all_grades if g < 60)

                    f.write("\nGrade Distribution:\n")
                    f.write(f"A (90-100): {a_count}\n")
                    f.write(f"B (80-89): {b_count}\n")
                    f.write(f"C (70-79): {c_count}\n")
                    f.write(f"D (60-69): {d_count}\n")
                    f.write(f"F (0-59): {f_count}\n")

            print(f"✅ Report saved as '{filename}'")
        except IOError as e:
            print(f"❌ Error exporting report: {e}")

    def run(self):
        """Main application loop"""
        self.print_banner()

        while True:
            print("\n📚 MENU")
            print("-" * 40)
            print("1️⃣  Add Student")
            print("2️⃣  Add Grade")
            print("3️⃣  View All Grades")
            print("4️⃣  Visualize Grades")
            print("5️⃣  Remove Student")
            print("6️⃣  Export Report")
            print("7️⃣  Save Changes")
            print("8️⃣  Save and Exit")
            print("-" * 40)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_grade()
            elif choice == "3":
                self.view_grades()
            elif choice == "4":
                self.visualize_grades()
            elif choice == "5":
                self.remove_student()
            elif choice == "6":
                self.export_report()
            elif choice == "7":
                self.save_grades()
            elif choice == "8":
                if self.save_grades():
                    print("👋 Thanks for using Grade Tracker!")
                    break
            else:
                print("❌ Invalid choice. Please enter 1–8.")


if __name__ == "__main__":
    app = GradeTracker()
    app.run()






name = input("Enter name: ")

match name:
    case "jared" | "john":
        print("Hello")