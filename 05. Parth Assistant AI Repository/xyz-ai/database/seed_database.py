"""
PARTH ASSISTANT AI — Deterministic School ERP Synthetic Dataset Seeder
Generates 300 Students, 220 Parents, 25 Teachers, 15 Classes, 1-Week Attendance,
Conflict-Free Timetable, Marks across 4 Exams, Fees, Assignments, and Leaves.
"""

import json
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.sqlite_db import SQLiteDB, DB_PATH

# Seed for reproducible synthetic data
random.seed(42)

# School Constants
SCHOOL_ID = "SCH-001"
SCHOOL_NAME = "Parth International School"
SCHOOL_LOCATION = "Sector 4, Gomti Nagar, Lucknow, Uttar Pradesh, India"
ACADEMIC_YEAR = "2026-2027"

FIRST_NAMES_BOYS = [
    "Aarav", "Rohan", "Vikram", "Aditya", "Kabir", "Arjun", "Dev", "Ishaan", "Reyansh", "Atharv",
    "Vivaan", "Dhruv", "Krishna", "Ayush", "Shaurya", "Ritvik", "Samar", "Pranav", "Harsh", "Yash",
    "Manish", "Nikhil", "Akash", "Gaurav", "Siddharth", "Varun", "Kunal", "Aniket", "Tushar", "Deepak"
]
FIRST_NAMES_GIRLS = [
    "Ananya", "Priya", "Diya", "Saanvi", "Aanya", "Isha", "Kavya", "Navya", "Riya", "Avni",
    "Pari", "Meera", "Tanvi", "Myra", "Sneha", "Pooja", "Shreya", "Aditi", "Anushka", "Bhavna",
    "Simran", "Neha", "Divya", "Komal", "Swati", "Rashmi", "Tanya", "Akshara", "Pallavi", "Geet"
]
LAST_NAMES = [
    "Sharma", "Patel", "Gupta", "Singh", "Verma", "Mehta", "Kumar", "Mishra", "Pandey", "Trivedi",
    "Shukla", "Saxena", "Srivastava", "Yadav", "Chauhan", "Bhatnagar", "Agarwal", "Bansal", "Joshi", "Kapoor",
    "Chopra", "Malhotra", "Dubey", "Tiwari", "Rathore", "Nair", "Rao", "Reddy", "Ghosh", "Chatterjee"
]
OCCUPATIONS = [
    "Software Engineer", "Doctor", "Civil Engineer", "Chartered Accountant", "Professor",
    "Government Officer", "Bank Manager", "Business Owner", "Architect", "Scientist",
    "Journalist", "Lawyer", "Pharmacist", "Marketing Director", "Consultant"
]
LOCALITIES = [
    "Gomti Nagar", "Aliganj", "Hazratganj", "Indira Nagar", "Mahanagar", "Jankipuram",
    "Vikas Nagar", "Ashiyana", "Rajajipuram", "Cantt Area", "Vibhuti Khand", "Kalyanpur"
]


def generate_seed_data():
    db = SQLiteDB()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Clear existing tables
        tables = [
            "attendance", "marks", "timetable", "class_sessions", "leave_requests",
            "fees", "assignments", "announcements", "support_requests", "teacher_classes",
            "subjects", "students", "classes", "teachers", "parents", "school_info", "users"
        ]
        for t in tables:
            cursor.execute(f"DELETE FROM {t}")
        
        # 1. School Info
        cursor.execute("""
        INSERT INTO school_info (school_id, name, location, city, state, pincode, board, established_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (SCHOOL_ID, SCHOOL_NAME, SCHOOL_LOCATION, "Lucknow", "Uttar Pradesh", "226010", "CBSE", 2012))

        # 2. Classes (6 to 12)
        classes_data = [
            ("C-06A", "6-A", "A", ACADEMIC_YEAR, "T310", "Room 101", 40),
            ("C-06B", "6-B", "B", ACADEMIC_YEAR, "T311", "Room 102", 40),
            ("C-07A", "7-A", "A", ACADEMIC_YEAR, "T312", "Room 103", 40),
            ("C-07B", "7-B", "B", ACADEMIC_YEAR, "T313", "Room 104", 40),
            ("C-08A", "8-A", "A", ACADEMIC_YEAR, "T314", "Room 105", 40),
            ("C-08B", "8-B", "B", ACADEMIC_YEAR, "T315", "Room 106", 40),
            ("C-09A", "9-A", "A", ACADEMIC_YEAR, "T302", "Room 201", 40),
            ("C-09B", "9-B", "B", ACADEMIC_YEAR, "T301", "Room 202", 40),
            ("C-10A", "10-A", "A", ACADEMIC_YEAR, "T301", "Room 203", 40),
            ("C-10B", "10-B", "B", ACADEMIC_YEAR, "T302", "Room 204", 40),
            ("C-10C", "10-C", "C", ACADEMIC_YEAR, "T303", "Room 205", 40),
            ("C-11A", "11-A", "A", ACADEMIC_YEAR, "T304", "Room 301", 40),
            ("C-11B", "11-B", "B", ACADEMIC_YEAR, "T305", "Room 302", 40),
            ("C-12A", "12-A", "A", ACADEMIC_YEAR, "T306", "Room 303", 40),
            ("C-12B", "12-B", "B", ACADEMIC_YEAR, "T307", "Room 304", 40),
        ]
        cursor.executemany("""
        INSERT INTO classes (class_id, class_name, section, academic_year, class_teacher_id, room_number, capacity, student_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, 20)
        """, classes_data)

        # 3. 25 Teachers
        teachers_list = [
            ("T301", "EMP-1001", "Sunita Verma", "sunita.verma@school.example.edu", "+91-9876500301", "Mathematics", "Senior PGT Mathematics", "Mathematics", "10-A, 9-B, 11-A", "2018-06-15", 8, "M.Sc. Mathematics, B.Ed."),
            ("T302", "EMP-1002", "Dr. K. Mehta", "k.mehta@school.example.edu", "+91-9876500302", "Science", "Head of Science Department", "Science, Physics", "10-B, 9-A, 12-A", "2015-04-10", 12, "Ph.D. Physics, B.Ed."),
            ("T303", "EMP-1003", "Anil Kumar Srivastava", "anil.srivastava@school.example.edu", "+91-9876500303", "Computer Science", "PGT Computer Science", "Computer Science", "10-C, 11-A, 12-A", "2019-07-01", 7, "M.Tech CSE"),
            ("T304", "EMP-1004", "Pooja Trivedi", "pooja.trivedi@school.example.edu", "+91-9876500304", "English", "Senior PGT English", "English", "11-A, 12-A, 10-A", "2016-08-20", 10, "M.A. English Literature, B.Ed."),
            ("T305", "EMP-1005", "Rameshwar Shukla", "rameshwar.shukla@school.example.edu", "+91-9876500305", "Hindi", "PGT Hindi", "Hindi", "11-B, 12-B, 10-B", "2017-03-12", 9, "M.A. Hindi, B.Ed."),
            ("T306", "EMP-1006", "Dr. Shalini Pandey", "shalini.pandey@school.example.edu", "+91-9876500306", "Chemistry", "PGT Chemistry", "Chemistry", "12-A, 12-B, 11-B", "2016-01-05", 11, "Ph.D. Chemistry"),
            ("T307", "EMP-1007", "Rajeev Saxena", "rajeev.saxena@school.example.edu", "+91-9876500307", "Biology", "PGT Biology", "Biology", "12-B, 11-A, 10-A", "2018-09-15", 8, "M.Sc. Zoology, B.Ed."),
            ("T308", "EMP-1008", "Manish Joshi", "manish.joshi@school.example.edu", "+91-9876500308", "Social Science", "TGT Social Studies", "Social Science", "9-A, 9-B, 10-B", "2020-02-01", 6, "M.A. History, B.Ed."),
            ("T309", "EMP-1009", "Vikas Singh Rathore", "vikas.rathore@school.example.edu", "+91-9876500309", "Physical Education", "Sports Director", "Physical Education", "10-A, 10-B, 11-A, 12-A", "2014-05-10", 13, "M.P.Ed."),
            ("T310", "EMP-1010", "Meenakshi Bhatnagar", "meenakshi.b@school.example.edu", "+91-9876500310", "Mathematics", "TGT Mathematics", "Mathematics", "6-A, 7-A, 8-A", "2021-04-15", 5, "M.Sc. Mathematics, B.Ed."),
            ("T311", "EMP-1011", "Sanjay Dubey", "sanjay.dubey@school.example.edu", "+91-9876500311", "Science", "TGT Science", "Science", "6-B, 7-B, 8-B", "2019-11-20", 7, "M.Sc. Chemistry, B.Ed."),
            ("T312", "EMP-1012", "Kavita Chauhan", "kavita.chauhan@school.example.edu", "+91-9876500312", "English", "TGT English", "English", "7-A, 8-A, 9-A", "2020-08-01", 6, "M.A. English, B.Ed."),
            ("T313", "EMP-1013", "Deepak Mishra", "deepak.mishra@school.example.edu", "+91-9876500313", "Hindi", "TGT Hindi", "Hindi", "7-B, 8-B, 9-B", "2018-07-15", 8, "M.A. Hindi, B.Ed."),
            ("T314", "EMP-1014", "Preeti Agarwal", "preeti.agarwal@school.example.edu", "+91-9876500314", "Social Science", "TGT Social Studies", "Social Science", "8-A, 6-A, 7-A", "2021-01-10", 5, "M.A. Geography, B.Ed."),
            ("T315", "EMP-1015", "Gaurav Malhotra", "gaurav.malhotra@school.example.edu", "+91-9876500315", "Computer Science", "TGT Computer Science", "Computer Science", "8-B, 6-B, 7-B", "2022-03-01", 4, "MCA"),
            ("T316", "EMP-1016", "Rashmi Tiwari", "rashmi.tiwari@school.example.edu", "+91-9876500316", "Mathematics", "TGT Mathematics", "Mathematics", "6-B, 8-B, 10-C", "2017-09-01", 9, "M.Sc. Mathematics, B.Ed."),
            ("T317", "EMP-1017", "Alok Kumar Yadav", "alok.yadav@school.example.edu", "+91-9876500317", "Science", "TGT Science", "Science", "6-A, 8-A, 10-C", "2019-02-15", 7, "M.Sc. Physics, B.Ed."),
            ("T318", "EMP-1018", "Nidhi Kapoor", "nidhi.kapoor@school.example.edu", "+91-9876500318", "English", "TGT English", "English", "6-A, 6-B, 10-C", "2020-06-01", 6, "M.A. English, B.Ed."),
            ("T319", "EMP-1019", "Harish Chandra", "harish.chandra@school.example.edu", "+91-9876500319", "Hindi", "TGT Hindi", "Hindi", "6-A, 6-B, 10-A", "2018-04-12", 8, "M.A. Hindi, B.Ed."),
            ("T320", "EMP-1020", "Swati Bansal", "swati.bansal@school.example.edu", "+91-9876500320", "Social Science", "TGT Social Studies", "Social Science", "6-B, 7-B, 10-C", "2021-08-15", 5, "M.A. Political Science, B.Ed."),
            ("T321", "EMP-1021", "Arun Kumar Nair", "arun.nair@school.example.edu", "+91-9876500321", "Physics", "PGT Physics", "Physics", "11-A, 11-B, 12-B", "2015-11-01", 11, "M.Sc. Physics, B.Ed."),
            ("T322", "EMP-1022", "Sneha Rao", "sneha.rao@school.example.edu", "+91-9876500322", "Chemistry", "PGT Chemistry", "Chemistry", "11-A, 10-B, 9-B", "2019-05-15", 7, "M.Sc. Chemistry, B.Ed."),
            ("T323", "EMP-1023", "Amitabh Ghosh", "amitabh.ghosh@school.example.edu", "+91-9876500323", "Biology", "PGT Biology", "Biology", "11-B, 10-C, 9-A", "2017-08-20", 9, "M.Sc. Botany, B.Ed."),
            ("T324", "EMP-1024", "Priyanka Reddy", "priyanka.reddy@school.example.edu", "+91-9876500324", "Mathematics", "PGT Mathematics", "Mathematics", "11-B, 12-B, 10-B", "2018-01-10", 8, "M.Sc. Mathematics, B.Ed."),
            ("T325", "EMP-1025", "Tanmay Chatterjee", "tanmay.chatterjee@school.example.edu", "+91-9876500325", "Physical Education", "Physical Trainer", "Physical Education", "6-A, 7-A, 8-A, 9-A", "2020-10-01", 6, "B.P.Ed.")
        ]
        cursor.executemany("""
        INSERT INTO teachers (teacher_id, employee_id, name, email, phone, department, designation, subjects, classes, joining_date, experience_years, qualification)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, teachers_list)

        # 4. 220 Parents
        parents_list = []
        # Predefined parent anchors
        parents_list.append(("P201", "Rajesh Sharma", "rajesh.sharma@parent.example.com", "+91-9876500201", "Father", "Flat 402, Royal Palms, Gomti Nagar", "Lucknow", "Uttar Pradesh", "226010", "Software Architect"))
        parents_list.append(("P202", "Suresh Patel", "suresh.patel@parent.example.com", "+91-9876500202", "Father", "House 12, Sector B, Aliganj", "Lucknow", "Uttar Pradesh", "226024", "Civil Engineer"))
        parents_list.append(("P203", "Manoj Gupta", "manoj.gupta@parent.example.com", "+91-9876500203", "Father", "24/B Indira Nagar", "Lucknow", "Uttar Pradesh", "226016", "Chartered Accountant"))
        parents_list.append(("P204", "Sunita Singh", "sunita.singh@parent.example.com", "+91-9876500204", "Mother", "Plot 89, Hazratganj", "Lucknow", "Uttar Pradesh", "226001", "Professor"))
        parents_list.append(("P205", "Dinesh Verma", "dinesh.verma@parent.example.com", "+91-9876500205", "Father", "56 Vikas Nagar", "Lucknow", "Uttar Pradesh", "226022", "Bank Manager"))
        
        for p_idx in range(6, 221):
            pid = f"P{p_idx + 200:03d}"
            p_rel = "Father" if p_idx % 3 == 0 else ("Mother" if p_idx % 3 == 1 else "Guardian")
            first = random.choice(FIRST_NAMES_BOYS if p_rel == "Father" else FIRST_NAMES_GIRLS)
            last = random.choice(LAST_NAMES)
            p_name = f"{first} {last}"
            p_email = f"{first.lower()}.{last.lower()}{p_idx}@parent.example.com"
            p_phone = f"+91-98765{p_idx + 10000:05d}"
            loc = random.choice(LOCALITIES)
            addr = f"House {p_idx * 3}, Block {chr(65 + (p_idx % 6))}, {loc}"
            occ = random.choice(OCCUPATIONS)
            parents_list.append((pid, p_name, p_email, p_phone, p_rel, addr, "Lucknow", "Uttar Pradesh", "226010", occ))
        
        cursor.executemany("""
        INSERT INTO parents (parent_id, name, email, phone, relationship, address, city, state, pincode, occupation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, parents_list)

        # 5. 300 Students (20 students per class across 15 classes)
        students_list = []
        # Predefined student anchors
        students_list.append(("S101", "ADM-2024-0101", "Aarav (Rahul) Sharma", "Male", "2010-04-14", "C-10A", "10-A", "A", 1, "P201", "aarav.sharma@school.edu", "+91-9876500101", "Flat 402, Royal Palms, Gomti Nagar", "Lucknow", "Uttar Pradesh", "226010", "2024-04-01", "ACTIVE", ACADEMIC_YEAR))
        students_list.append(("S102", "ADM-2024-0102", "Ananya Patel", "Female", "2010-08-22", "C-10A", "10-A", "A", 2, "P202", "ananya.patel@school.edu", "+91-9876500102", "House 12, Sector B, Aliganj", "Lucknow", "Uttar Pradesh", "226024", "2024-04-01", "ACTIVE", ACADEMIC_YEAR))
        students_list.append(("S103", "ADM-2024-0103", "Rohan Gupta", "Male", "2011-02-10", "C-09B", "9-B", "B", 1, "P203", "rohan.gupta@school.edu", "+91-9876500103", "24/B Indira Nagar", "Lucknow", "Uttar Pradesh", "226016", "2024-04-01", "ACTIVE", ACADEMIC_YEAR))
        students_list.append(("S104", "ADM-2024-0104", "Priya Singh", "Female", "2010-11-05", "C-10B", "10-B", "B", 1, "P204", "priya.singh@school.edu", "+91-9876500104", "Plot 89, Hazratganj", "Lucknow", "Uttar Pradesh", "226001", "2024-04-01", "ACTIVE", ACADEMIC_YEAR))
        students_list.append(("S105", "ADM-2024-0105", "Vikram Verma", "Male", "2011-06-18", "C-09A", "9-A", "A", 1, "P205", "vikram.verma@school.edu", "+91-9876500105", "56 Vikas Nagar", "Lucknow", "Uttar Pradesh", "226022", "2024-04-01", "ACTIVE", ACADEMIC_YEAR))

        # Fill remaining 295 students across the 15 classes
        student_counter = 6
        for c_id, c_name, c_sec, _, _, _, _ in classes_data:
            # Determine existing count for this class from anchors
            existing_in_class = sum(1 for s in students_list if s[5] == c_id)
            needed = 20 - existing_in_class
            for roll in range(existing_in_class + 1, existing_in_class + needed + 1):
                sid = f"S{student_counter + 100:03d}"
                adm = f"ADM-2024-{student_counter + 100:04d}"
                gender = "Male" if student_counter % 2 == 0 else "Female"
                first = random.choice(FIRST_NAMES_BOYS if gender == "Male" else FIRST_NAMES_GIRLS)
                last = random.choice(LAST_NAMES)
                s_name = f"{first} {last}"
                
                # Link to parent (siblings share parent)
                parent_idx = ((student_counter - 1) % 220) + 1
                pid = f"P{parent_idx + 200:03d}"
                
                email = f"{first.lower()}.{last.lower()}{student_counter}@school.edu"
                phone = f"+91-98765{student_counter + 20000:05d}"
                loc = random.choice(LOCALITIES)
                addr = f"{roll * 2}, Street {c_sec}, {loc}"
                
                # Approximate birth year based on grade (6th = 2014, 12th = 2008)
                grade_num = int(c_name.split("-")[0])
                birth_year = 2026 - (grade_num + 5)
                dob = f"{birth_year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
                
                students_list.append((
                    sid, adm, s_name, gender, dob, c_id, c_name, c_sec, roll, pid,
                    email, phone, addr, "Lucknow", "Uttar Pradesh", "226010", "2024-04-01", "ACTIVE", ACADEMIC_YEAR
                ))
                student_counter += 1

        cursor.executemany("""
        INSERT INTO students (student_id, admission_number, name, gender, date_of_birth, class_id, class_name, section, roll_number, parent_id, email, phone, address, city, state, pincode, admission_date, status, academic_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, students_list)

        # 6. Subjects (10 standard subjects mapped across classes)
        subjects_master = [
            ("Mathematics", "MATH", "T301"),
            ("Science", "SCI", "T302"),
            ("English", "ENG", "T304"),
            ("Hindi", "HIN", "T305"),
            ("Social Science", "SST", "T308"),
            ("Computer Science", "CS", "T303"),
            ("Physics", "PHY", "T321"),
            ("Chemistry", "CHEM", "T306"),
            ("Biology", "BIO", "T307"),
            ("Physical Education", "PE", "T309")
        ]
        
        subjects_list = []
        teacher_classes_list = []
        asgn_id = 1
        
        for c_id, c_name, c_sec, _, _, _, _ in classes_data:
            grade_num = int(c_name.split("-")[0])
            
            # Select age-appropriate subjects
            if grade_num <= 10:
                active_subs = [s for s in subjects_master if s[0] in ["Mathematics", "Science", "English", "Hindi", "Social Science", "Computer Science", "Physical Education"]]
            else:
                active_subs = [s for s in subjects_master if s[0] in ["English", "Physics", "Chemistry", "Mathematics", "Biology", "Computer Science", "Physical Education"]]
            
            for sub_name, code, t_id in active_subs:
                sub_id = f"SUB-{c_name}-{code}"
                subjects_list.append((sub_id, sub_name, c_id, c_name, f"{code}-{grade_num}", t_id, 100, 35, "ACTIVE"))
                
                # Teacher-Class assignment
                teacher_classes_list.append((
                    f"ASGN-{asgn_id:04d}", t_id, c_id, sub_id, ACADEMIC_YEAR, 5, "ACTIVE"
                ))
                asgn_id += 1

        cursor.executemany("""
        INSERT INTO subjects (subject_id, subject_name, class_id, class_name, subject_code, teacher_id, maximum_marks, passing_marks, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, subjects_list)

        cursor.executemany("""
        INSERT INTO teacher_classes (assignment_id, teacher_id, class_id, subject_id, academic_year, periods_per_week, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, teacher_classes_list)

        # 7. Timetable (Guaranteed Conflict-Free: 25 Teachers > 15 Classes)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        periods_times = [
            (1, "08:00", "08:45"),
            (2, "08:45", "09:30"),
            (3, "09:45", "10:30"),
            (4, "10:30", "11:15"),
            (5, "11:45", "12:30"),
            (6, "12:30", "01:15"),
            (7, "01:15", "02:00")
        ]

        timetable_list = []
        tt_id = 1

        for d_idx, day in enumerate(days):
            for p_num, start_t, end_t in periods_times:
                for c_idx, (c_id, c_name, c_sec, _, _, room, _) in enumerate(classes_data):
                    # Get all valid subjects for this class
                    class_subs = [s for s in subjects_list if s[2] == c_id]
                    # Select subject by rotating index based on class, day, and period
                    sub_idx = (c_idx + (p_num - 1) + d_idx) % len(class_subs)
                    chosen_sub = class_subs[sub_idx]
                    
                    # Teacher assigned uniquely to this subject/class
                    # Map teacher offset guaranteeing 15 distinct teachers across 15 classes in slot (day, p_num)
                    t_idx = (c_idx + (p_num - 1) * 3 + d_idx * 5) % len(teachers_list)
                    t_id = teachers_list[t_idx][0]

                    timetable_list.append((
                        f"TT-{tt_id:05d}", c_id, c_sec, day, p_num, start_t, end_t, chosen_sub[0], t_id, room
                    ))
                    tt_id += 1

        cursor.executemany("""
        INSERT INTO timetable (timetable_id, class_id, section, day, period, start_time, end_time, subject_id, teacher_id, room_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, timetable_list)

        # 8. 1-Week Full Attendance Dataset (Monday 2026-08-17 to Sunday 2026-08-23)
        dates_days = [
            ("2026-08-17", "Monday"),
            ("2026-08-18", "Tuesday"),
            ("2026-08-19", "Wednesday"),
            ("2026-08-20", "Thursday"),
            ("2026-08-21", "Friday"),
            ("2026-08-22", "Saturday"),
            ("2026-08-23", "Sunday")  # Holiday
        ]

        attendance_records = []
        att_id = 1

        for dt, day_name in dates_days:
            if day_name == "Sunday":
                # All students marked HOLIDAY for their scheduled subjects
                for s in students_list:
                    sid, _, _, _, _, c_id, _, _, _, _, _, _, _, _, _, _, _, _, _ = s
                    class_subs = [sub for sub in subjects_list if sub[2] == c_id]
                    for sub in class_subs:
                        sub_id, _, _, _, _, t_id, _, _, _ = sub
                        attendance_records.append((
                            f"ATT-{att_id:06d}", sid, c_id, sub_id, t_id, dt, day_name,
                            "HOLIDAY", f"{dt} 08:00:00", "System", "Sunday Weekly Holiday"
                        ))
                        att_id += 1
            else:
                # Monday - Saturday attendance per student and core subject
                for s in students_list:
                    sid, _, s_name, _, _, c_id, c_name, _, roll, _, _, _, _, _, _, _, _, _, _ = s
                    class_subs = [sub for sub in subjects_list if sub[2] == c_id]
                    
                    # Individual daily student consistency
                    student_rand = random.random()
                    is_full_day_absent = student_rand < 0.05
                    is_on_leave = 0.05 <= student_rand < 0.07
                    
                    for sub in class_subs:
                        sub_id, sub_name, _, _, _, t_id, _, _, _ = sub
                        
                        if is_full_day_absent:
                            status = "ABSENT"
                            remark = "Uninformed Absence"
                        elif is_on_leave:
                            status = "LEAVE"
                            remark = "Medical / Approved Leave"
                        else:
                            sub_rand = random.random()
                            if sub_rand < 0.02:
                                status = "ABSENT"
                                remark = f"Absent for {sub_name}"
                            elif sub_rand < 0.05:
                                status = "LATE"
                                remark = "Late arrival"
                            else:
                                status = "PRESENT"
                                remark = "Attended class"
                        
                        # Deterministic anchor override for Rahul Sharma on Monday
                        if sid == "S101" and dt == "2026-08-17" and "MATH" in sub_id:
                            status = "ABSENT"
                            remark = "Sick leave requested"

                        attendance_records.append((
                            f"ATT-{att_id:06d}", sid, c_id, sub_id, t_id, dt, day_name,
                            status, f"{dt} 08:30:00", t_id, remark
                        ))
                        att_id += 1

        cursor.executemany("""
        INSERT INTO attendance (attendance_id, student_id, class_id, subject_id, teacher_id, date, day, status, marked_at, marked_by, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, attendance_records)

        # 9. Exams (4 Exams across Academic Year)
        exams_data = [
            ("EXAM-UT1", "Unit Test 1", "Unit Test", ACADEMIC_YEAR, "ALL", "2026-07-10", "2026-07-15", "COMPLETED"),
            ("EXAM-MID", "Mid Term", "Term Exam", ACADEMIC_YEAR, "ALL", "2026-09-18", "2026-09-28", "COMPLETED"),
            ("EXAM-UT2", "Unit Test 2", "Unit Test", ACADEMIC_YEAR, "ALL", "2026-11-20", "2026-11-25", "COMPLETED"),
            ("EXAM-FIN", "Final Examination", "Annual Exam", ACADEMIC_YEAR, "ALL", "2026-02-15", "2026-02-28", "COMPLETED")
        ]
        cursor.executemany("""
        INSERT INTO exams (exam_id, exam_name, exam_type, academic_year, class_id, start_date, end_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, exams_data)

        # 10. Marks Dataset
        marks_list = []
        mark_id = 1

        for ex_id, ex_name, _, _, _, ex_date, _, _ in exams_data:
            max_m = 25.0 if "Unit Test" in ex_name else 100.0
            pass_m = max_m * 0.35

            for s in students_list:
                sid, _, s_name, _, _, c_id, c_name, _, roll, _, _, _, _, _, _, _, _, _, _ = s
                class_subs = [sub for sub in subjects_list if sub[2] == c_id]

                for sub in class_subs:
                    sub_id, sub_name, _, _, _, _, _, _, _ = sub
                    
                    # Generate realistic scores (85% pass rate, mean around 72%)
                    score_pct = min(100.0, max(15.0, random.gauss(72.0, 15.0)))
                    
                    # Anchor overrides
                    if sid == "S101" and "MATH" in sub_id:
                        score_pct = 94.0
                    elif sid == "S102" and "SCI" in sub_id:
                        score_pct = 90.0
                    elif sid == "S103" and "MATH" in sub_id:
                        score_pct = 98.0

                    obt_marks = round((score_pct / 100.0) * max_m, 1)
                    pct = round((obt_marks / max_m) * 100.0, 1)
                    res = "PASS" if obt_marks >= pass_m else "FAIL"
                    
                    if pct >= 91: grade = "A1"
                    elif pct >= 81: grade = "A2"
                    elif pct >= 71: grade = "B1"
                    elif pct >= 61: grade = "B2"
                    elif pct >= 51: grade = "C1"
                    elif pct >= 41: grade = "C2"
                    elif pct >= 35: grade = "D"
                    else: grade = "E"

                    marks_list.append((
                        f"MRK-{mark_id:06d}", sid, sub_id, c_id, ex_id, ex_name,
                        obt_marks, max_m, pct, grade, res, ex_date
                    ))
                    mark_id += 1

        cursor.executemany("""
        INSERT INTO marks (mark_id, student_id, subject_id, class_id, exam_id, exam_name, marks_obtained, maximum_marks, percentage, grade, result, exam_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, marks_list)

        # 11. Class Sessions (Teacher Activity during the week)
        sessions_list = []
        sess_id = 1
        for dt, day_name in dates_days[:6]:  # Mon-Sat
            for tt in timetable_list[:40]:  # sample timetable slots
                _, c_id, _, _, p_num, _, _, sub_id, t_id, _ = tt
                status = "COMPLETED" if sess_id % 12 != 0 else "CANCELLED"
                topic = f"Topic {p_num}: Fundamental Concepts and Application"
                att_marked = 1 if status == "COMPLETED" else 0
                remarks = "Class concluded on schedule" if status == "COMPLETED" else "Teacher on leave / special event"

                sessions_list.append((
                    f"SESS-{sess_id:05d}", t_id, c_id, sub_id, dt, p_num, status, topic, att_marked, remarks
                ))
                sess_id += 1

        cursor.executemany("""
        INSERT INTO class_sessions (session_id, teacher_id, class_id, subject_id, date, period, status, topic, attendance_marked, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sessions_list)

        # 12. Leave Requests
        leave_list = [
            ("L-101", "S101", "P201", "Medical Leave", "2026-08-17", "2026-08-17", "Viral Fever", "APPROVED", "T301", "2026-08-16 18:00:00"),
            ("L-102", "S104", "P204", "Family Function", "2026-08-21", "2026-08-22", "Sister's Wedding in Delhi", "APPROVED", "T302", "2026-08-18 10:00:00"),
            ("L-103", "S110", "P210", "Medical Leave", "2026-08-20", "2026-08-20", "Doctor's Appointment", "PENDING", None, "2026-08-19 20:00:00"),
            ("L-104", "S125", "P225", "Casual Leave", "2026-08-19", "2026-08-19", "Personal reasons", "REJECTED", "T304", "2026-08-18 09:00:00")
        ]
        cursor.executemany("""
        INSERT INTO leave_requests (leave_id, student_id, parent_id, leave_type, start_date, end_date, reason, status, approved_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, leave_list)

        # 13. Fees
        fees_list = []
        fee_id = 1
        for s in students_list:
            sid = s[0]
            # Term 1 Tuition Fee
            fees_list.append((f"FEE-{fee_id:05d}", sid, ACADEMIC_YEAR, "Tuition Fee (Q1)", 24000.0, "2026-07-15", 24000.0, "2026-07-10", "PAID"))
            fee_id += 1
            # Term 2 Tuition Fee
            status = "PAID" if fee_id % 4 != 0 else ("PARTIAL" if fee_id % 4 == 1 else "PENDING")
            paid = 24000.0 if status == "PAID" else (12000.0 if status == "PARTIAL" else 0.0)
            p_date = "2026-08-10" if status in ["PAID", "PARTIAL"] else None
            fees_list.append((f"FEE-{fee_id:05d}", sid, ACADEMIC_YEAR, "Tuition Fee (Q2)", 24000.0, "2026-10-15", paid, p_date, status))
            fee_id += 1

        cursor.executemany("""
        INSERT INTO fees (fee_id, student_id, academic_year, fee_type, amount, due_date, paid_amount, payment_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, fees_list)

        # 14. Assignments
        assignments_list = [
            ("ASN-001", "T301", "C-10A", "SUB-10-A-MATH", "Quadratic Equations Problem Set", "Solve Exercises 4.1 to 4.3 from NCERT textbook.", "2026-08-17", "2026-08-24", "ACTIVE"),
            ("ASN-002", "T302", "C-10A", "SUB-10-A-SCI", "Light Reflection & Refraction Lab Report", "Submit experimental findings on concave mirrors.", "2026-08-18", "2026-08-25", "ACTIVE"),
            ("ASN-003", "T304", "C-10A", "SUB-10-A-ENG", "Essay on Environmental Conservation", "Write a 300-word argumentative essay on sustainable energy.", "2026-08-16", "2026-08-22", "COMPLETED"),
            ("ASN-004", "T301", "C-09B", "SUB-9-B-MATH", "Polynomials Factorization Worksheet", "Complete questions 1 to 20 on algebraic identities.", "2026-08-17", "2026-08-23", "ACTIVE"),
            ("ASN-005", "T303", "C-11A", "SUB-11-A-CS", "Python Object Oriented Programming", "Build a Class hierarchy for School Management.", "2026-08-15", "2026-08-22", "ACTIVE")
        ]
        cursor.executemany("""
        INSERT INTO assignments (assignment_id, teacher_id, class_id, subject_id, title, description, assigned_date, due_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, assignments_list)

        # 15. Announcements
        announcements_list = [
            ("ANN-001", "Independence Day Celebrations", "Parth International School will host flag hoisting at 08:30 AM on August 15.", "Principal Office", "ALL", "2026-08-10 09:00:00", "HIGH", "ACTIVE"),
            ("ANN-002", "Parent-Teacher Meeting (PTM)", "PTM for Classes 9 to 12 is scheduled for Saturday, August 29 between 9 AM and 1 PM.", "Management", "PARENTS", "2026-08-18 11:00:00", "HIGH", "ACTIVE"),
            ("ANN-003", "Science Exhibition Submissions", "All students participating in the Annual Science Fair must submit synopses by August 25.", "Science Dept", "STUDENTS", "2026-08-15 14:00:00", "NORMAL", "ACTIVE"),
            ("ANN-004", "Staff Training Workshop", "AI Pedagogy workshop for all faculty on Friday afternoon.", "Academic Coordinator", "TEACHERS", "2026-08-17 16:00:00", "NORMAL", "ACTIVE")
        ]
        cursor.executemany("""
        INSERT INTO announcements (announcement_id, title, message, created_by, audience, created_at, priority, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, announcements_list)

        # 16. Support Requests
        support_list = [
            ("REQ-1001", "Rajesh Sharma", "P201", "PARENT", "TEACHER", "T301", "Discuss Rahul's Mathematics progress and attendance", "COMPLETED", "2026-08-19 10:30:00", "2026-08-19 14:00:00"),
            ("REQ-1002", "Suresh Patel", "P202", "PARENT", "TEACHER", "T301", "Inquire about upcoming Olympiad preparation for Ananya", "ACCEPTED", "2026-08-19 15:20:00", None),
            ("REQ-1003", "Manoj Gupta", "P203", "PARENT", "MANAGEMENT", "M401", "Transport route inquiry for Indira Nagar bus stop", "PENDING", "2026-08-20 08:15:00", None)
        ]
        cursor.executemany("""
        INSERT INTO support_requests (request_id, created_by, user_id, role, target_type, target_id, reason, status, created_at, resolved_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, support_list)

        # 17. Seed Users (Auth Accounts)
        users_list = [
            # Core demo roles
            ("S101", "student1", "password123", "STUDENT", "Aarav (Rahul) Sharma", "aarav.sharma@school.edu", None, None, "10-A", None, "+91-9876500101"),
            ("S102", "student2", "password123", "STUDENT", "Ananya Patel", "ananya.patel@school.edu", None, None, "10-A", None, "+91-9876500102"),
            ("P201", "parent1", "password123", "PARENT", "Rajesh Sharma", "rajesh.sharma@parent.example.com", json.dumps(["S101"]), None, None, None, "+91-9876500201"),
            ("P202", "parent2", "password123", "PARENT", "Suresh Patel", "suresh.patel@parent.example.com", json.dumps(["S102"]), None, None, None, "+91-9876500202"),
            ("T301", "teacher1", "password123", "TEACHER", "Sunita Verma", "sunita.verma@school.example.edu", None, json.dumps(["10-A", "9-B", "11-A"]), None, "Mathematics", "+91-9876500301"),
            ("T302", "teacher2", "password123", "TEACHER", "Dr. K. Mehta", "k.mehta@school.example.edu", None, json.dumps(["10-B", "9-A", "12-A"]), None, "Science", "+91-9876500302"),
            ("M401", "principal1", "password123", "PRINCIPAL", "Dr. V. K. Raman", "principal@school.example.edu", None, None, None, None, "+91-9876500001")
        ]

        # Seed additional student users
        for s in students_list[2:]:
            users_list.append((
                s[0], f"student_{s[0].lower()}", "password123", "STUDENT", s[2], s[10],
                None, None, s[6], None, s[11]
            ))

        # Seed additional parent users
        parent_child_map = {}
        for s in students_list:
            pid = s[9]
            parent_child_map.setdefault(pid, []).append(s[0])
            
        for p in parents_list[2:]:
            pid = p[0]
            linked_children = parent_child_map.get(pid, [])
            users_list.append((
                pid, f"parent_{pid.lower()}", "password123", "PARENT", p[1], p[2],
                json.dumps(linked_children), None, None, None, p[3]
            ))

        # Seed additional teacher users
        for t in teachers_list[2:]:
            classes_arr = [c.strip() for c in t[8].split(",")]
            users_list.append((
                t[0], f"teacher_{t[0].lower()}", "password123", "TEACHER", t[2], t[3],
                None, json.dumps(classes_arr), None, t[6], t[4]
            ))

        cursor.executemany("""
        INSERT INTO users (user_id, username, password_hash, role, name, email, child_ids, assigned_classes, grade_section, subject, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, users_list)

        conn.commit()

    print("==================================================")
    print("PARTH INTERNATIONAL SCHOOL ERP SEED SUMMARY")
    print("==================================================")
    print(f"School: {SCHOOL_NAME} ({SCHOOL_LOCATION})")
    print(f"Students: {len(students_list)}")
    print(f"Parents: {len(parents_list)}")
    print(f"Teachers: {len(teachers_list)}")
    print(f"Classes: {len(classes_data)}")
    print(f"Subjects: {len(subjects_list)}")
    print(f"Teacher-Class Assignments: {len(teacher_classes_list)}")
    print(f"Timetable Entries: {len(timetable_list)}")
    print(f"Attendance Records: {len(attendance_records)}")
    print(f"Marks Records: {len(marks_list)}")
    print(f"Class Sessions: {len(sessions_list)}")
    print(f"Fee Records: {len(fees_list)}")
    print(f"Leave Records: {len(leave_list)}")
    print(f"Assignments: {len(assignments_list)}")
    print(f"Announcements: {len(announcements_list)}")
    print(f"Support Requests: {len(support_list)}")
    print(f"User Accounts: {len(users_list)}")
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    generate_seed_data()
