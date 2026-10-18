"""
Student Performance Analysis System
Reads student records from students.csv and generates a performance report.
"""

import csv
from abc import ABC, abstractmethod
from pathlib import Path


class Student(ABC):
    """Abstract base class representing a student."""

    def __init__(self, student_id, first_name, last_name, programme, marks):
        self.__student_id = str(student_id)
        self.__first_name = str(first_name)
        self.__last_name = str(last_name)
        self.__programme = str(programme)
        self.__marks = self._validate_marks(marks)

    @staticmethod
    def _validate_marks(marks):
        """Validate and return a dictionary of subject marks."""
        if not marks:
            raise ValueError("At least one subject mark is required.")
        validated = {}
        for subject, mark in marks.items():
            try:
                numeric_mark = float(mark)
            except (TypeError, ValueError):
                raise ValueError(f"Mark for {subject} must be numeric.")
            if not 0 <= numeric_mark <= 100:
                raise ValueError(f"Mark for {subject} must be between 0 and 100.")
            validated[str(subject)] = numeric_mark
        return validated

    @property
    def student_id(self):
        return self.__student_id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def full_name(self):
        return f"{self.__first_name} {self.__last_name}"

    @property
    def programme(self):
        return self.__programme

    @property
    def marks(self):
        # Return a copy so callers cannot directly modify internal data.
        return self.__marks.copy()

    def update_mark(self, subject, mark):
        """Safely update a subject mark after validating it."""
        validated = self._validate_marks({subject: mark})
        self.__marks[str(subject)] = validated[str(subject)]

    def calculate_average(self):
        return sum(self.__marks.values()) / len(self.__marks)

    def determine_grade(self):
        """Grade boundaries used for this project; adjust if lecturer specifies others."""
        average = self.calculate_average()
        if average >= 80:
            return "A"
        if average >= 70:
            return "B"
        if average >= 60:
            return "C"
        if average >= 50:
            return "D"
        return "F"

    @abstractmethod
    def student_type_info(self):
        """Subclasses must provide information about their student type."""
        raise NotImplementedError

    def performance_message(self):
        """Shared method whose behaviour can be overridden by subclasses."""
        return f"{self.full_name} has an average of {self.calculate_average():.2f}%."


class AIUStudent(Student):
    """A general student enrolled at AIU."""

    def student_type_info(self):
        return "AIU student"

    def performance_message(self):
        return f"Student: {self.full_name} | Grade: {self.determine_grade()}"


class ScholarshipStudent(AIUStudent):
    """Student type with scholarship-specific behaviour."""

    def __init__(self, student_id, first_name, last_name, programme, marks,
                 scholarship_amount=0):
        super().__init__(student_id, first_name, last_name, programme, marks)
        self.scholarship_amount = float(scholarship_amount)
        if self.scholarship_amount < 0:
            raise ValueError("Scholarship amount cannot be negative.")

    def is_eligible(self):
        return self.calculate_average() >= 85

    def student_type_info(self):
        return "Scholarship student"

    def performance_message(self):
        if self.is_eligible():
            return (
                f"Scholarship candidate: {self.full_name} "
                f"(average {self.calculate_average():.2f}%)."
            )
        return f"{self.full_name} is not eligible for a scholarship."


class PerformanceAnalyzer:
    """Analyzes a collection of Student objects (composition/has-a relationship)."""

    def __init__(self, students):
        self.students = list(students)
        if not self.students:
            raise ValueError("At least one student is required for analysis.")

    def highest_average(self):
        return max(self.students, key=lambda student: student.calculate_average())

    def lowest_average(self):
        return min(self.students, key=lambda student: student.calculate_average())

    def class_average(self):
        return sum(student.calculate_average() for student in self.students) / len(self.students)


def flexible_average(*marks):
    """
    Flexible interface: accepts any number of marks, e.g.
    flexible_average(75, 80, 70) or flexible_average(75, 80, 70, 90).
    This demonstrates a Python alternative to traditional method overloading.
    """
    if len(marks) == 1 and isinstance(marks[0], (list, tuple)):
        marks = tuple(marks[0])
    if not marks:
        raise ValueError("Supply at least one mark.")
    numeric_marks = []
    for mark in marks:
        try:
            value = float(mark)
        except (TypeError, ValueError):
            raise ValueError("All marks must be numeric.")
        if not 0 <= value <= 100:
            raise ValueError("Every mark must be between 0 and 100.")
        numeric_marks.append(value)
    return sum(numeric_marks) / len(numeric_marks)


def load_students(csv_file):
    """Load CSV records and create the appropriate student objects."""
    students = []
    with open(csv_file, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required_columns = {
            "StudentID", "FName", "LName", "Programme",
            "Math", "English", "Science"
        }
        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError("CSV is missing one or more required column headings.")

        for row in reader:
            marks = {
                "Math": row["Math"],
                "English": row["English"],
                "Science": row["Science"],
            }
            # Create scholarship objects for students meeting the 85% threshold.
            temporary_student = AIUStudent(
                row["StudentID"], row["FName"], row["LName"],
                row["Programme"], marks
            )
            if temporary_student.calculate_average() >= 85:
                student = ScholarshipStudent(
                    row["StudentID"], row["FName"], row["LName"],
                    row["Programme"], marks, scholarship_amount=50000
                )
            else:
                student = temporary_student
            students.append(student)
    return students


def generate_report(students, analyzer):
    """Print an individual report and the class performance summary."""
    print("=" * 68)
    print("             STUDENT PERFORMANCE ANALYSIS REPORT")
    print("=" * 68)

    for student in students:
        print(f"\nStudent ID : {student.student_id}")
        print(f"Name       : {student.full_name}")
        print(f"Programme  : {student.programme}")
        print("Marks      : " + ", ".join(
            f"{subject}={mark:g}" for subject, mark in student.marks.items()
        ))
        print(f"Average    : {student.calculate_average():.2f}%")
        print(f"Grade      : {student.determine_grade()}")
        print(f"Student type: {student.student_type_info()}")
        if isinstance(student, ScholarshipStudent):
            status = "Eligible" if student.is_eligible() else "Not eligible"
            print(f"Scholarship: {status} (amount: KSh {student.scholarship_amount:,.2f})")
        else:
            print("Scholarship: Not eligible / no scholarship record")
        print(f"Message    : {student.performance_message()}")

    highest = analyzer.highest_average()
    lowest = analyzer.lowest_average()
    print("\n" + "-" * 68)
    print("CLASS PERFORMANCE SUMMARY")
    print("-" * 68)
    print(f"Highest average : {highest.full_name} ({highest.calculate_average():.2f}%)")
    print(f"Lowest average  : {lowest.full_name} ({lowest.calculate_average():.2f}%)")
    print(f"Class average   : {analyzer.class_average():.2f}%")
    eligible = [s for s in students if isinstance(s, ScholarshipStudent) and s.is_eligible()]
    print(f"Scholarship-eligible students: {len(eligible)}")
    print("=" * 68)


def main():
    csv_file = Path(__file__).with_name("students.csv")
    students = load_students(csv_file)
    analyzer = PerformanceAnalyzer(students)
    generate_report(students, analyzer)

    # Example flexible-average calls (three marks and a variable number of marks).
    print("\nFlexible interface examples:")
    print(f"Average of three marks (75, 80, 70): {flexible_average(75, 80, 70):.2f}")
    print(f"Average of four marks (75, 80, 70, 90): {flexible_average(75, 80, 70, 90):.2f}")


if __name__ == "__main__":
    main()
