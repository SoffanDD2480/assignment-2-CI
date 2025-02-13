# CI Assignment - Continuous Integration System

## 📌 Description

This project is an assignment for the DD2480 course, implementing a **Continuous Integration (CI)** system. The goal is to automate testing and integration processes to ensure code quality and reliability. The system automatically builds and tests submitted code changes using GitHub Actions.

---

## 📂 Project Structure

```
code/
├── ci_server.py → Handles CI server logic
├── email_response.py → Manages email notifications for CI status
├── generate_docs.py → Automates documentation generation
├── git_helpers.py → Provides helper functions for Git interactions
├── syntax_check.py → Performs syntax validation on submitted code
├── test_file.py → Test case for specific functions
├── tests.py → General test cases for CI functionalities

docs/
├── files that document the CI system's core modules and automated documentation generation.
.gitignore
LICENSE 
README.md 
```

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/SoffanDD2480/assignment-2-CI.git
cd assignment-2-CI
```

### 2️⃣ Python and pip version requirement

Use the following versions of Python and Pip:
* Python: 3.11.8 >=
* Pip: 23.3 >=
To check your installed versions, run:

```bash
python --version
pip --version
```

### 3️⃣ Install dependencies

Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 🏃‍♂️ Running the Program

To execute the CI server, use:

```bash
python code/ci_server.py
```

Modify `code/ci_server.py` to adjust CI configurations.

---

## 🛠 Running Tests

The project includes automated tests using **pytest**. Tests are located in the `tests/` directory.

### 🔹 Running all tests
To run all tests:

```bash
pytest tests/
```

### 🔹 Running a specific test
To run a specific test file:

```bash
pytest tests/test_file_right.py
```

To run a specific test function:

```bash
pytest tests/test_file_right.py::test_specific_function
```

If you want to stop execution after the first failed test:

```bash
pytest -x tests/
```

---

## 📊 How It Works

1️⃣ **Input**:
   - A set of code changes is submitted to the repository.
   - The CI system automatically triggers on push or pull request events.

2️⃣ **Processing**:
   - GitHub Actions runs the CI pipeline.
   - The system installs dependencies and runs all test cases.
   - Syntax validation is performed using `syntax_check.py`.
   - Documentation is auto-generated with `generate_docs.py`.
   - Email notifications are managed via `email_response.py`.

3️⃣ **Output**:
   - If all tests pass, the changes are considered valid.
   - If any test fails, the CI pipeline blocks the merge request and outputs errors.
   - Email notifications inform the team of the build status.

---

## 📝 Property (SEMAT)

The document answering the questions for "Property (SEMAT)" can be found [here](Property_SEMAT.md)

---

## 🏗 Contributors

**SoffanDD2480 Team**

- Albin (GH: albinwwoxnerud):
  - Implement autogen of Docs, Github Pages
  - Implement tests for Building DB
  - Implement DB for saving old builds
  - Implement Webhooks for Server
  - Implement Syntax checking and formating
- Dmitry (GH: Dudjfy): 
  - Implement tests for Git helpers, Syntax Checker, Generating docs
  - Implement SEMAT
- Elias (GH: eliasfrode):
  - Implement Server infrastructure
  - Implement Email notifications
- Riccardo (GH: riccacocco):
  - Implement Email notifications
  - Implement README
  - Implement Server infrastructure
  - Implement Syntax checking and formating

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

