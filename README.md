# 🌟 Textual SQL Magic 🌟

**First interface**
![text1](https://github.com/user-attachments/assets/94a9d798-460f-4fde-aaf1-d240ea16ff97)
**After submit**
![text2](https://github.com/user-attachments/assets/9b0ce252-9900-4156-8f52-04d5042d5906)


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)

---

## Overview

**Textual SQL Magic** is an intuitive application that enables users to query a database using natural language. Instead of writing complex SQL commands, users can simply type in plain English questions, and the app will convert them into SQL queries. This allows non-technical users to easily retrieve data from databases without needing SQL knowledge.

The core of the app is powered by a **language model (LLM)** that translates human language into structured SQL commands, making it useful for data retrieval across various domains.

---

## Features

- ✨ **Natural Language to SQL**: Convert everyday language questions into SQL queries with ease.
- 💾 **Database Interaction**: Seamlessly fetch data from a connected database based on user queries.
- 🖥️ **Streamlit Interface**: A user-friendly, interactive interface for real-time query interaction.
- 🔄 **Extensibility**: Easily adaptable for any dataset, regardless of the industry or data type.
- 📊 **No SQL Expertise Required**: Users do not need to understand SQL to interact with the database.

---

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io) for real-time, interactive user interfaces.
- **Backend**: Python for processing and managing application logic.
- **Language Model**: [Google Gemini Pro](https://cloud.google.com) for natural language processing and SQL generation.
- **Database**: [SQLite](https://www.sqlite.org) for SQL-based data storage and queries.

---
---
##Usage

Querying the Database
- **Enter a question**: Type your query in plain English (e.g., "How many records are in the users table?").
- **Submit**: Click the button to generate the corresponding SQL query.
- **View Results**: The SQL query is executed against the connected database, and the results are displayed in a table.
  
**Example Queries**
"What is the average age of users?"
"Show me the total sales for the last quarter."
"How many customers signed up last month?"
The app will automatically convert these natural language queries into SQL and fetch the corresponding data from the database.

---


### Prerequisites

- Python 3.x
- SQLite (or any SQL-compatible database)
- API key for the LLM (e.g., Google Generative AI API)


