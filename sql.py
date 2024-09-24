import sqlite3

# Connect to SQLite
connection = sqlite3.connect("healthcare.db")

# Create a cursor object
cursor = connection.cursor()

# Create tables
create_patients_table = """
CREATE TABLE IF NOT EXISTS Patients (
    patient_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    gender VARCHAR(10),
    phone VARCHAR(15),
    email VARCHAR(100)
);
"""

create_doctors_table = """
CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    specialization VARCHAR(50),
    phone VARCHAR(15),
    email VARCHAR(100)
);
"""

create_appointments_table = """
CREATE TABLE IF NOT EXISTS Appointments (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATETIME,
    reason TEXT,
    FOREIGN KEY(patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES Doctors(doctor_id)
);
"""

create_medical_records_table = """
CREATE TABLE IF NOT EXISTS MedicalRecords (
    record_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    record_date DATE,
    diagnosis TEXT,
    treatment TEXT,
    FOREIGN KEY(patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES Doctors(doctor_id)
);
"""

create_prescriptions_table = """
CREATE TABLE IF NOT EXISTS Prescriptions (
    prescription_id INTEGER PRIMARY KEY,
    record_id INTEGER,
    medication VARCHAR(100),
    dosage VARCHAR(50),
    frequency VARCHAR(50),
    FOREIGN KEY(record_id) REFERENCES MedicalRecords(record_id)
);
"""

# Execute table creation
cursor.execute(create_patients_table)
cursor.execute(create_doctors_table)
cursor.execute(create_appointments_table)
cursor.execute(create_medical_records_table)
cursor.execute(create_prescriptions_table)

# Insert sample data into Patients table
patients_data = [
    ('kaoutar', 'el bannoudi', '2002-04-17', 'female', '123-456-7890', 'kaoutarelban@gmail.com'),
    ('doua', 'ben', '2003-03-22', 'female', '987-654-3210', 'douae@example.com'),
    ('brahim', 'el ', '2000-07-17', 'male', '123-456-7890', 'brahimel@gmail.com'),
    ('houda', 'kha', '2002-11-22', 'female', '987-654-3210', 'houda.kha@example.com'),
    ('ouissame', 'lakhh', '2001-14-17', 'female', '123-456-7890', 'ouissame@gmail.com'),
    ('ahmed', 'ben', '2006-03-22', 'male', '987-654-3210', 'ahmed@example.com'),
]

cursor.executemany("INSERT INTO Patients (first_name, last_name, date_of_birth, gender, phone, email) VALUES (?, ?, ?, ?, ?, ?);", patients_data)

# Insert sample data into Doctors table
doctors_data = [
    ('Alice', 'bogoos', 'Cardiology', '555-1234', 'alice.bogos@hospital.com'),
    ('yasmine', 'alaoui', 'Dermatology', '555-5678', 'yasmine.alaoui@hospital.com'),
]

cursor.executemany("INSERT INTO Doctors (first_name, last_name, specialization, phone, email) VALUES (?, ?, ?, ?, ?);", doctors_data)

# Insert sample data into Appointments table
appointments_data = [
    (1, 1, '2023-09-25 10:00', 'Annual Checkup'),
    (2, 1, '2023-09-26 11:00', 'Skin Rash Examination'),
]

cursor.executemany("INSERT INTO Appointments (patient_id, doctor_id, appointment_date, reason) VALUES (?, ?, ?, ?);", appointments_data)

# Insert sample data into Medical Records table
medical_records_data = [
    (1, 1, '2024-09-25', 'Healthy', 'Regular checkup'),
    (2, 2, '2024-09-26', 'Eczema', 'Topical cream prescribed'),
]

cursor.executemany("INSERT INTO MedicalRecords (patient_id, doctor_id, record_date, diagnosis, treatment) VALUES (?, ?, ?, ?, ?);", medical_records_data)

# Insert sample data into Prescriptions table
prescriptions_data = [
    (1, 'Hydrocortisone Cream', '2 times a day', 'Apply on affected area'),
    (2, 'Cetirizine', 'Once a day', 'Take in the evening'),
]

cursor.executemany("INSERT INTO Prescriptions (record_id, medication, dosage, frequency) VALUES (?, ?, ?, ?);", prescriptions_data)

# Commit and close the connection
connection.commit()
connection.close()

print("Healthcare database created and sample data inserted successfully.")
