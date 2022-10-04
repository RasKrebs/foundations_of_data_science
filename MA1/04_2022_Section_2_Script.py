"""

DiplomaProgram Class

"""
class DiplomaProgram:
    
    #Constructor
    def __init__(self, name):
        self.name = name
        self.courses = []
        self.graduated_students = []
        self.students_with_distinction = []
        self.students_who_failed = []
        
    # Adding Course Function
    def add_course(self, course):
        
        #Ensuring course does not already exists in list of courses
        if course.name in self.courses:
            return
        else:
            self.courses.append(course.name)
    
    # Remove course function
    def remove_course(self, course):
        self.courses.remove(course.name)
    
    # Adding student to graduate list, but ensuring student does not already exists
    
    #function for checking if student fulfill the requirements for graduation
    def add_graduated_students(self, student):
        # Failsafe, so that students are not added twice
        if student.name in self.graduated_students:
            """
            Eventhough a student have passed, we wan't to check if they have passed with 
            distinction, therefore we call the passed_with_distinction function as well
            """
            self.passed_with_distinction(student)
            return
        elif len(student.passed_courses) == len(self.courses):
            self.graduated_students.append(student.name)
            self.passed_with_distinction(student)
        else:
            if student.name in self.students_who_failed:
                return
            else:
                self.students_who_failed.append(student.name)
    
    # Function for checking if student fulfill the requirements for passing with distinction
    def passed_with_distinction(self, student):
        """
        Because any student that pass will be passed to this function, we want to ensure they are removed 
        from the list of students that have not passed
        """
        
        if student.name in self.students_who_failed:
            self.students_who_failed.remove(student.name)
        
        #Seeing if student is already in list, and ending function if True
        if student.name in self.students_with_distinction:
            return
        else: # Pass counter for checking if students fulfill passed with distinction requirements
            pass_counter = 0
            for x in student.grades.values():
                for value in x:
                    if value == 'Pass':
                        pass_counter += 1
            
            if pass_counter >= 17:
                self.students_with_distinction.append(student.name)
            else:
                return


"""

Course Class

"""


class Course:
    
    #Initialize
    def __init__(self, name, associated_program):
        self.name = name
        self.students = []
        self.student_grades = {}
        self.passed_students = []
        
        # We make sure to pass a graduate program at the initialization of the class. Both to access later, but also to make it so the courses is assigned to the corresponding program
        self.program = associated_program
        associated_program.add_course(self)
        associated_program.graduated_students.clear() # To clear graduate students, if new course is added
        

    #add student to students list
    def add_student(self, student):
        
        #checks if student already exist in list
        if student in self.students:
            return(print(f'student {student.name} already added to list of students'))
        else:
            
            #adds student if student does not exists already
            student.grades[self.name] = []
            self.students.append(student)
            self.student_grades[student] = []
            
            student.courses.append(self.name)
    
    #Remove student from course
    def remove_student(self, student):
        self.students.remove(student)
    
    #Add grade
    def grade(self, student, result):
        #Appending result to student key in the grades dictionary for all students
        self.student_grades[student].append(result)
        
        #Appending grade to the respective students, in their grade dictionary under the key, defined by the course name
        student.grades[self.name].append(result)
        
        #Calling funciton for students that have passed, every time a grade is added to update it.
        self.student_that_pass(student)
    
    #Remove Grade
    def remove_grade(self, student:object, number:int):
        """
        Args:
            student (object): Input student object
            number (int): Refers to which number assignment, you wish to remove the grade for
        """
        self.student_grades[student].pop(number-1)
    
    #Function for finding students that have passed
    def student_that_pass(self, student):
        # Checking if student has already passed
        if student in self.passed_students:
            self.program.add_graduated_students(student)
            return
        
        # If pass count is greater then 3, than pass
        elif self.student_grades[student].count('Pass') >= 3:
            self.passed_students.append(student)
            
            #Appending course name to list of courses passed by student under the student
            student.passed_courses.append(self.name)
            
            #Calling function under DiplomaProgram to run and see if student fullfill the obligations to pass the program
            self.program.add_graduated_students(student)
        else:
            return

"""

Student Class

"""


class Student:
    def __init__(self, fName, lName, UUID):
        self.fName = fName
        self.lName = lName
        self.name = fName + " " + lName
        self.UUID = UUID
        self.courses = []
        self.grades = {}
        self.passed_courses = []
    
    def __str__(self):
        print(f"Student Name: {self.name} \nStudent Enrolled in: {', '.join(map(str, self.courses))}\n")
        return


# Creating Students
jacob = Student('Jacob', 'Hansen', 1)
william = Student('William', 'Fatcher', 2)
john = Student('John', 'Doe', 3)
doe = Student('Doe', 'John', 4)

student_list = [jacob, william, john, doe] # Student objects for looping purposes


#Creating Diploma Program With Associated Courses
data_science = DiplomaProgram('Data Science')

python = Course('Python Programming Course', data_science)
data = Course('Data Mining and Machine Learning Course', data_science)
va = Course('Visual Analytics', data_science)
ta = Course('Text Analytics', data_science)
for_deletion = Course('This Will Be Deleted', data_science)


course_list = [python, data, va, ta] 


# Printing courses under data science diploma program
data_science.courses

# Exercise remove course function
data_science.remove_course(for_deletion)

# Looping through Students for adding to course program
for student in student_list:
    python.add_student(student)
    data.add_student(student)
    va.add_student(student)
    ta.add_student(student)


#Assigning grades in a convenient manner
grades = ['Pass', 'Fail']
for student in student_list:
    for i in range(5):
        python.grade(student, 'Pass')
        data.grade(student, 'Pass')
        va.grade(student, 'Pass')

for student in student_list[0:2]: ## Half of the students will fail there Text Analytics course assignments
    for i in range(5):
        ta.grade(student, 'Fail')

for student in student_list[2:4]: ## Other half will Pass
    for i in range(5):
        ta.grade(student, 'Pass')



#Printing student names and course names
print("Students:")
for student in student_list:
    print(student.name)

print("\nCourses:")

for course in course_list:
    print(course.name)


#Printing Jacob's Grades
print('\n Jacob Grades:')
print(jacob.grades)

#Printing Doe's Grades
print('\n Doe Grades:')
print(doe.grades)

#Printing Jacob Passed Courses
print('\n Jacob passed courses:')
print(jacob.passed_courses)

#Printing Doe's passed courses
print('\n Doe passed courses:')
print(doe.passed_courses)

#Outputting list of students who passed with distinction
print('\n Passed who passed with distinction under data science diploma program:')
print(data_science.students_with_distinction)

#Outputting list of students who failed
print('\n List of students who faild under data science diploma program:')
print(data_science.students_who_failed)
