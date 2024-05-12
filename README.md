# SmartGrader with BERT

## Overview

SmartGrader with BERT is an automated assignment grading system designed to streamline the grading process for educators. By leveraging the powerful BERT (Bidirectional Encoder Representations from Transformers) model, SmartGrader aims to provide accurate and efficient grading while saving valuable time for instructors.

## Features

- **Automated Grading**: SmartGrader utilizes the BERT model to automatically grade assignments based on predefined criteria.
- **Customizable Rubrics**: Instructors can define customizable rubrics tailored to their specific assignment requirements.
- **Scalability**: SmartGrader is designed to handle a large volume of assignments, making it suitable for classrooms of any size.
- **Feedback Generation**: The system generates detailed feedback for students based on their performance, aiding in their learning process.
- **Analytics Dashboard**: Instructors have access to an analytics dashboard that provides insights into student performance and assignment trends.

## Installation

To install SmartGrader with BERT, follow these steps:

1. Install Postgresql
2. Install Conda
3. Install Make
4. Create config.ini and insert gmail keys like this.
   ```bash
   [EMAIL]
   sender_email = {your email without curly brackets}@gmail.com
   password = {Your password without curly brackets}
   ```
5. Clone this repository:
  ```bash
  git clone https://github.com/Ravindu-Priyankara/SmartGrader-Web.git
  cd SmartGrader
  ```
6. Create Conda Environment
  ```bash
  conda env create -f environment.yml
  conda activate <environment_name>
  ```
7. Install requirements
  ```python
  pip install -r requirements.txt
  ```
8. Create Database
   ```mysql
   CREATE ROLE ravindu WITH LOGIN PASSWORD 'ravi';
   CREATE DATABASE smartgrader WITH OWNER = ravindu;
   GRANT ALL PRIVILEGES ON DATABASE smartgrader TO ravindu;
   
   /* registered users watch*/
   SELECT * FROM auth_user;
   /*give previleges*/
   GRANT CREATE ON DATABASE smartgrader TO ravindu;
   ```

## Usage

To use SmartGrader with BERT, follow these steps:

1. Run
   ```bash
   make run
   ```
or

  ```python
   python smartGrader/manage.py runserver
   ```
2. Migrate
   ```bash
   make migrate
   ```
3. Normal DB
   ```bash
   make db
   ```
4. DB with Logger
   ```bash
   make log
   ```
5. Database Connect
   ```bash
   make connect
   ```
6. DB restart
   ```bash
   make restart
   ```
7. Stop DB
   ```bash
   make stop
   ```
8. Testing
   ```bash
   make test
   ```
9. pylint test
   ```bash
   make pylint
   ```

## Contributing

We welcome contributions from the community! If you'd like to contribute to SmartGrader with BERT, please follow these guidelines:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes thoroughly.
5. Submit a pull request.

## License


This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.


## Contact

For questions or feedback, please contact h.h.a.r.p.premachandra@gmail.com.
