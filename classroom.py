import argparse
import sys
from student import *

class Classroom:
    def __init__(self, class_file):
        self.class_file = class_file
        self.students = {}

        self.import_class_info()
        self.parse_class_info()
        #self.print_class_info()

    def  import_class_info(self):
        try: 
            file = open(self.class_file)
        except FileNotFoundError:
            print("File not found ...")
            sys.exit(1)
        
        self.records = [clean_line for clean_line in
                        [line.strip() for line in file.readlines()]
                        if clean_line != '']
        self.records.pop(0)
        
        file.close()

    def parse_class_info(self):
        try:
            self.student_list = [(s[0].strip(), int(s[1].strip()), s[2].strip(), 
                                  int(s[3].strip()), int(s[4].strip()), int(s[5].strip()),
                                  int(s[6].strip()), int(s[7].strip()), int(s[8].strip()),
                                  int(s[9].strip()), int(s[10].strip()), int(s[11].strip()))
                                   for s in [s.split(',') for s in self.records]]
        except  Exception:
            print("Error: Invalid file format.")
            sys.exit(1)
        
        for student in self.student_list:
            try:
                Name, student_ID, Key, Lab_1, Lab_2, Lab_3, Lab_4, \
                Midterm, Exam_1, Exam_2, Exam_3, Exam_4 = student

                new_student = Student(Name=Name, Key = Key, Lab_1 = Lab_1,
                                      Lab_2 = Lab_2, Lab_3 =Lab_3, Lab_4 = Lab_4, 
                                      Midterm=Midterm, Exam_1=Exam_1, Exam_2=Exam_2,
                                      Exam_3=Exam_3, Exam_4=Exam_4)
                if student_ID:
                    self.students[student_ID] = new_student
                else:
                    print("Student must have ID.")
                    sys.exit(1)
            except Exception as excpt:
                print("Error  parsing student info.")
                sys.exit(1)

    def print_class_info(self):
        print("Class Info:")
        print("(Name, ID Number, Key, Lab 1, Lab 2, Lab 3, Lab 4, Midterm, Exam 1, Exam 2, Exam 3, Exam 4)\n")
        for student in self.student_list:
            print(student)
    
    def process_request(self, command):
        
        if command == "GMA":
            
        elif command == "GEA":

        elif command == "GL1A":

        elif command == "GL2A":
        
        elif command == "GL3A":

        elif command == "GL4A":

        elif command == "GG":
        
        else

if __name__ == "__main__":
    classroom = Classroom("course_grades_2023.csv")