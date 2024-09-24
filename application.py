from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pandas import read_sql_query
import os
import sqlite3
import google.generativeai as genai

# Configuration our API Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

load_dotenv() ## load all the environemnt variables

# Function to Load the Google Gemini Module and Providw sql query as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

# Function to retrieve the query from the sqllit database

def get_db_connection():
    conn = sqlite3.connect("healthcare.db")
    return conn
# Define your Prompt

prompts = [
    """
    You are an expert in converting English questions to SQL queries! The SQL database has the following tables:

    1. **Patients** (patient_id, first_name, last_name, date_of_birth, gender, phone, email)
    2. **Doctors** (doctor_id, first_name, last_name, specialization, phone, email)
    3. **Appointments** (appointment_id, patient_id, doctor_id, appointment_date, reason)
    4. **MedicalRecords** (record_id, patient_id, doctor_id, record_date, diagnosis, treatment)
    5. **Prescriptions** (prescription_id, record_id, medication, dosage, frequency)

    Example 1 - How many patients are registered?
    SQL command: SELECT COUNT(*) FROM Patients;

    Example 2 - Show the details of all patients.
    SQL command: SELECT * FROM Patients;

    Example 3 - What are the names of all female patients?
    SQL command: SELECT first_name, last_name FROM Patients WHERE gender = 'female';

    Example 4 - Find the patient with the last name "el bannoudi".
    SQL command: SELECT * FROM Patients WHERE last_name = 'el bannoudi';

    Example 5 - List all patients born after January 1, 2000.
    SQL command: SELECT * FROM Patients WHERE date_of_birth > '2000-01-01';

    Example 6 - How many doctors are there?
    SQL command: SELECT COUNT(*) FROM Doctors;

    Example 7 - List all doctors in Cardiology.
    SQL command: SELECT * FROM Doctors WHERE specialization = 'Cardiology';

    Example 8 - Find the phone number of Dr. Alice.
    SQL command: SELECT phone FROM Doctors WHERE first_name = 'Alice';

    Example 9 - Show all doctors specializing in Dermatology.
    SQL command: SELECT * FROM Doctors WHERE specialization = 'Dermatology';

    Example 10 - Retrieve the last names of all doctors.
    SQL command: SELECT last_name FROM Doctors;

    Example 11 - How many appointments are scheduled for today?
    SQL command: SELECT COUNT(*) FROM Appointments WHERE appointment_date = DATE('now');

    Example 12 - List all appointments scheduled for patient Kaoutar.
    SQL command: SELECT * FROM Appointments WHERE patient_id = (SELECT patient_id FROM Patients WHERE first_name = 'kaoutar');

    Example 13 - What is the reason for appointment ID 1?
    SQL command: SELECT reason FROM Appointments WHERE appointment_id = 1;

    Example 14 - Show all appointments in the next week.
    SQL command: SELECT * FROM Appointments WHERE appointment_date BETWEEN DATE('now') AND DATE('now', '+7 days');

    Example 15 - Retrieve all appointments for doctor Yasmine.
    SQL command: SELECT * FROM Appointments WHERE doctor_id = (SELECT doctor_id FROM Doctors WHERE first_name = 'yasmine');

    Example 16 - How many medical records are there?
    SQL command: SELECT COUNT(*) FROM MedicalRecords;

    Example 17 - Show all medical records for patient Ahmed.
    SQL command: SELECT * FROM MedicalRecords WHERE patient_id = (SELECT patient_id FROM Patients WHERE first_name = 'ahmed');

    Example 18 - What are the diagnoses for patient Houda?
    SQL command: SELECT diagnosis FROM MedicalRecords WHERE patient_id = (SELECT patient_id FROM Patients WHERE first_name = 'houda');

    Example 19 - List all treatments prescribed by Dr. Alice.
    SQL command: SELECT treatment FROM MedicalRecords WHERE doctor_id = (SELECT doctor_id FROM Doctors WHERE first_name = 'Alice');

    Example 20 - Find all medical records created in 2024.
    SQL command: SELECT * FROM MedicalRecords WHERE record_date BETWEEN '2024-01-01' AND '2024-12-31';

    Example 21 - How many prescriptions are there?
    SQL command: SELECT COUNT(*) FROM Prescriptions;

    Example 22 - List all medications prescribed for patient Kaoutar.
    SQL command: SELECT medication FROM Prescriptions WHERE record_id = (SELECT record_id FROM MedicalRecords WHERE patient_id = (SELECT patient_id FROM Patients WHERE first_name = 'kaoutar'));

    Example 23 - What dosage was prescribed for medication Cetirizine?
    SQL command: SELECT dosage FROM Prescriptions WHERE medication = 'Cetirizine';

    Example 24 - Show all medications prescribed on September 26, 2024.
    SQL command: SELECT medication FROM Prescriptions WHERE record_id IN (SELECT record_id FROM MedicalRecords WHERE record_date = '2024-09-26');

    Example 25 - Find all patients who have received the medication Hydrocortisone Cream.
    SQL command: SELECT DISTINCT P.first_name, P.last_name FROM Patients P JOIN MedicalRecords M ON P.patient_id = M.patient_id JOIN Prescriptions R ON M.record_id = R.record_id WHERE R.medication = 'Hydrocortisone Cream';

    Example 26 - Retrieve all appointments along with patient names.
    SQL command: SELECT A.*, P.first_name, P.last_name FROM Appointments A JOIN Patients P ON A.patient_id = P.patient_id;

    Example 27 - Show all patients who have seen Dr. Yasmine.
    SQL command: SELECT DISTINCT P.first_name, P.last_name FROM Patients P JOIN MedicalRecords M ON P.patient_id = M.patient_id JOIN Doctors D ON M.doctor_id = D.doctor_id WHERE D.first_name = 'yasmine';

    Example 28 - Find all patients and their latest appointment date.
    SQL command: SELECT P.first_name, P.last_name, MAX(A.appointment_date) AS latest_appointment FROM Patients P JOIN Appointments A ON P.patient_id = A.patient_id GROUP BY P.patient_id;

    Example 29 - Show all medical records and corresponding patient names.
    SQL command: SELECT M.*, P.first_name, P.last_name FROM MedicalRecords M JOIN Patients P ON M.patient_id = P.patient_id;

    Example 30 - List all doctors and their patients.
    SQL command: SELECT D.first_name AS doctor_first_name, D.last_name AS doctor_last_name, P.first_name AS patient_first_name, P.last_name AS patient_last_name FROM Doctors D JOIN MedicalRecords M ON D.doctor_id = M.doctor_id JOIN Patients P ON M.patient_id = P.patient_id;

    Example 31 - Count the number of appointments per patient.
    SQL command: SELECT patient_id, COUNT(*) FROM Appointments GROUP BY patient_id;

    Example 32 - Find the earliest appointment date for each doctor.
    SQL command: SELECT doctor_id, MIN(appointment_date) AS first_appointment FROM Appointments GROUP BY doctor_id;

    Example 33 - Calculate the total number of medications prescribed per patient.
    SQL command: SELECT M.patient_id, COUNT(*) AS total_medications FROM Prescriptions M JOIN MedicalRecords R ON M.record_id = R.record_id GROUP BY M.patient_id;

    Example 34 - Count how many patients are of each gender.
    SQL command: SELECT gender, COUNT(*) FROM Patients GROUP BY gender;

    Example 35 - Show the average age of patients.
    SQL command: SELECT AVG(JULIANDAY('now') - JULIANDAY(date_of_birth)) / 365 AS average_age FROM Patients;

    Example 36 - List all patients with a specific email domain (e.g., '@gmail.com').
    SQL command: SELECT * FROM Patients WHERE email LIKE '%@gmail.com';

    Example 37 - Show all doctors sorted by their last name.
    SQL command: SELECT * FROM Doctors ORDER BY last_name;

    Example 38 - Retrieve the last five appointments for a specific patient.
    SQL command: SELECT * FROM Appointments WHERE patient_id = (SELECT patient_id FROM Patients WHERE first_name = 'ahmed') ORDER BY appointment_date DESC LIMIT 5;

    Example 39 - Show all medical records with a diagnosis of "Eczema".
    SQL command: SELECT * FROM MedicalRecords WHERE diagnosis = 'Eczema';

    Example 40 - List patients who have not made any appointments.
    SQL command: SELECT * FROM Patients WHERE patient_id NOT IN (SELECT DISTINCT patient_id FROM Appointments);

    Example 41 - Find all patients who have appointments with a specific doctor.
    SQL command: SELECT DISTINCT P.first_name, P.last_name FROM Patients P JOIN Appointments A ON P.patient_id = A.patient_id WHERE A.doctor_id = (SELECT doctor_id FROM Doctors WHERE first_name = 'Alice');

    Example 42 - Show all patients and their corresponding doctors for a specific appointment date.
    SQL command: SELECT P.first_name AS patient_first_name, P.last_name AS patient_last_name, D.first_name AS doctor_first_name, D.last_name AS doctor_last_name FROM Appointments A JOIN Patients P ON A.patient_id = P.patient_id JOIN Doctors D ON A.doctor_id = D.doctor_id WHERE A.appointment_date = '2024-09-26';

    Example 43 - List all doctors who have treated a specific patient.
    SQL command: SELECT DISTINCT D.first_name, D.last_name FROM Doctors D JOIN MedicalRecords M ON D.doctor_id = M.doctor_id WHERE M.patient_id = (SELECT patient_id FROM Patients WHERE first_name = 'Kaoutar');

    Example 44 - Find patients who have seen doctors in a specific specialization.
    SQL command: SELECT DISTINCT P.first_name, P.last_name FROM Patients P JOIN MedicalRecords M ON P.patient_id = M.patient_id JOIN Doctors D ON M.doctor_id = D.doctor_id WHERE D.specialization = 'Pediatrics';

    Example 45 - Show all medical records for a specific doctor with their patients.
    SQL command: SELECT P.first_name AS patient_first_name, P.last_name AS patient_last_name, M.* FROM MedicalRecords M JOIN Patients P ON M.patient_id = P.patient_id WHERE M.doctor_id = (SELECT doctor_id FROM Doctors WHERE first_name = 'Dr. Yasmine');

    Example 46 - List patients with appointments in the next month.
    SQL command: SELECT DISTINCT P.first_name, P.last_name FROM Patients P JOIN Appointments A ON P.patient_id = A.patient_id WHERE A.appointment_date BETWEEN DATE('now') AND DATE('now', '+30 days');

    Example 47 - Show all treatments given for a specific diagnosis.
    SQL command: SELECT DISTINCT treatment FROM MedicalRecords WHERE diagnosis = 'Flu';

    Example 48 - Count how many times each medication has been prescribed.
    SQL command: SELECT medication, COUNT(*) FROM Prescriptions GROUP BY medication;

    Example 49 - Retrieve the details of the most recent appointment for each patient.
    SQL command: SELECT A.* FROM Appointments A WHERE appointment_date = (SELECT MAX(appointment_date) FROM Appointments WHERE patient_id = A.patient_id);

    Example 50 - Find all doctors who have no appointments scheduled.
    SQL command: SELECT * FROM Doctors WHERE doctor_id NOT IN (SELECT DISTINCT doctor_id FROM Appointments);
    """
]




# Stream App framework
st.set_page_config(page_title="SQL Query Retrieval App")
st.header("🌟 Textual SQL Magic 🌟")

# Input for the question
question = st.text_input("🔍 Ask your question:", key="input")
submit = st.button("👉 Ask the Question")

# If the submit button is clicked
if submit:
    with st.spinner('🌀 Fetching data...'):
        # Get the SQL response from the Gemini model
        response = get_gemini_response(question, prompts)
        
        # Sanitize the response to extract the SQL command
        if response.startswith("```sql") and response.endswith("```"):
            response = response[6:-3].strip()  # Remove the backticks and whitespace

        st.write("Executing SQL query:")
        st.code(response)

        # Execute the sanitized SQL query
        try:
            conn = get_db_connection()
            result = pd.read_sql_query(response, conn)
            conn.close()

            if result.empty:
                st.warning("🚫 No results found for your query.")
            else:
                st.subheader("📊 Query Results:")
                st.dataframe(result)
        except Exception as e:
            st.error(f"🚨 An error occurred while executing the SQL query: {str(e)}")
st.subheader("What is Textual SQL Magic?")
st.write("""
Textual SQL Magic is a powerful tool that transforms your natural language questions into SQL queries. It simplifies data retrieval,
 allowing users of all skill levels to interact with databases and extract valuable insights without needing to know SQL syntax.
""")
st.subheader("How to Use Textual SQL Magic")
st.write("""
1. **Ask Your Question:** Type your question in natural language in the input box above."
2. **Submit Your Query:** Click the "👉 Ask the Question".
3. **View the SQL Query:** The app will convert your question into an SQL query, which will be displayed for you to review.
4. **Get Results 🌟**
""")