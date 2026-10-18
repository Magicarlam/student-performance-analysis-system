# student-performance-analysis-system

# Files
- student_performance_analysis.py — Python program.
- students.csv — student dataset used by the program.

# OOP concepts demonstrated
- Encapsulation: Student stores attributes privately and exposes read-only properties; update_mark() validates changes.
- Abstraction: Student is an abstract base class with the abstract student_type_info() method.
- Inheritance: AIUStudent inherits from Student; ScholarshipStudent inherits from AIUStudent.
- Method overriding and polymorphism: both student subclasses provide performance_message(); the program calls it on mixed student objects.
- Composition: PerformanceAnalyzer stores and analyses a collection of student objects.
- Flexible interface: flexible_average(*marks) accepts a variable number of marks (or a list/tuple) and validates them.

# Rules used
- Scholarship eligibility is an average of at least 85%, as specified in the assignment.
- The example scholarship amount is KSh 50,000 for eligible students; replace this with the amount specified by your lecturer if different.
- Grade boundaries are A: 80–100, B: 70–79.99, C: 60–69.99, D: 50–59.99, F: below 50. The assignment does not specify grade boundaries, so confirm these with your lecturer if a different scale is required.

# Brief reflection on challenges
One challenge was designing the class hierarchy so that the general student behaviour could be reused while scholarship students could provide specialised behaviour. Another was validating CSV marks and flexible average inputs to prevent invalid values from producing misleading results. Using a PerformanceAnalyzer that accepts student objects avoids duplicating student information.

# AI-use declaration
AI assistance was used to help structure and review the code and documentation. The student should verify the program, understand the implementation, make any required changes, and be ready to explain the code during physical marking, in line with the lecturer's AI-use policy.
