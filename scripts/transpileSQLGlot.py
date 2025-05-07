from sqlglot import parse, transpile
import unittest
import os
import re
import os
from openai import OpenAI

# ----------------------------------------------------------------------
# Configurable prompt kept as a module‑level constant
# ----------------------------------------------------------------------
SQL_TRANSPILE_PROMPT = """\
Role: SQL Transpiler
Audience: tech stakeholders (PM, analyst, engineer)

Guidelines  
You convert an SQL prompt from TSQL dialect to Postgresql dialect.
– You are given a SQL prompt in one dialect and asked to convert it to another dialect.
Don't change the meaning of the SQL prompt and don't include any other text in your response.
"""

def call_openai_api(sql_text: str) -> None:
    sql_text = sql_text.strip()
    if not sql_text:
        print("No input provided.")
        return

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=SQL_TRANSPILE_PROMPT,
        input=sql_text,
    )

    return response.output_text



def normalize_sql(sql_str):
            
    # Normalize both strings for comparison
    # 1. Convert to lowercase
    # 2. Remove all whitespace

    # Remove all whitespace
    sql_str = re.sub(r'\s+', '', sql_str)
    sql_str = re.sub(r'\n', '', sql_str)  # Remove newlines
    # Convert to lowercase for case-insensitive comparison
    sql_str = sql_str.lower()
    return sql_str
# Custom comparison with specific handling of identity/serial
def compare_sql_structure(actual, expected):
    # Handle the IDENTITY vs SERIAL difference
    actual_normalized = normalize_sql(actual)
    expected_normalized = normalize_sql(expected)

    # Print for debugging
    print("Actual (normalized):", actual_normalized)
    print("Expected (normalized):", expected_normalized)
                
    return actual_normalized == expected_normalized

TSQL_1 = "CREATE TABLE Employees (EmployeeID INT IDENTITY(1,1) PRIMARY KEY, FirstName NVARCHAR(50) NOT NULL, LastName NVARCHAR(50) NOT NULL, Department NVARCHAR(50), HireDate DATE, Salary DECIMAL(10,2), IsActive BIT DEFAULT 1)"

TSQL_2 = "INSERT INTO Employees (FirstName, LastName, Department, HireDate, Salary) VALUES ('John', 'Smith', 'Engineering', '2023-01-15', 75000.00), ('Mary', 'Johnson', 'Marketing', '2022-06-01', 65000.00), ('Robert', 'Williams', 'Finance', '2023-03-10', 80000.00)"

TSQL_3 = "SELECT EmployeeID, FirstName + ' ' + LastName AS FullName, Department, FORMAT(HireDate, 'yyyy-MM-dd') AS FormattedHireDate, Salary FROM Employees WHERE Department = 'Engineering' AND HireDate >= '2023-01-01' AND IsActive = 1 ORDER BY Salary DESC"

TSQL_4 = "BEGIN TRANSACTION; UPDATE Employees SET Salary = Salary * 1.10, Department = 'Software Engineering' WHERE Department = 'Engineering'; IF @@ROWCOUNT > 0 COMMIT TRANSACTION; ELSE ROLLBACK TRANSACTION"

TSQL_5 = "CREATE PROCEDURE GetEmployeesByDepartment @DepartmentName NVARCHAR(50), @MinimumSalary DECIMAL(10,2) = 0 AS BEGIN SET NOCOUNT ON; SELECT EmployeeID, FirstName, LastName, HireDate, Salary FROM Employees WHERE Department = @DepartmentName AND Salary >= @MinimumSalary AND IsActive = 1 ORDER BY LastName, FirstName; END; EXEC GetEmployeesByDepartment @DepartmentName = 'Marketing', @MinimumSalary = 50000"



class TestTranspileSQL(unittest.TestCase):
    def test_case1(self):
        # Transpile from T-SQL to PostgreSQL
        PostgreSQL_1_SQLGlot = transpile(TSQL_1, read="tsql", write="postgres")[0]
        PostgreSQL_1_LLM = call_openai_api(TSQL_1)
        self.assertTrue(
            compare_sql_structure(normalize_sql(PostgreSQL_1_SQLGlot), normalize_sql(PostgreSQL_1_LLM)),
            f"SQL structures don't match after normalization.\n\nActual: {normalize_sql(PostgreSQL_1_SQLGlot)}\n\nExpected: {normalize_sql(PostgreSQL_1_LLM)}"
        )
    def test_case2(self):
        # Transpile from T-SQL to PostgreSQL
        PostgreSQL_2_SQLGlot = transpile(TSQL_2, read="tsql", write="postgres")[0]
        PostgreSQL_2_LLM = call_openai_api(TSQL_2)
        self.assertTrue(
            compare_sql_structure(normalize_sql(PostgreSQL_2_SQLGlot), normalize_sql(PostgreSQL_2_LLM)),
            f"SQL structures don't match after normalization.\n\nActual: {normalize_sql(PostgreSQL_2_SQLGlot)}\n\nExpected: {normalize_sql(PostgreSQL_2_LLM)}"
        )
    def test_case3(self):
        # Transpile from T-SQL to PostgreSQL
        PostgreSQL_3_SQLGlot = transpile(TSQL_3, read="tsql", write="postgres")[0]
        PostgreSQL_3_LLM = call_openai_api(TSQL_3)
        self.assertTrue(
            compare_sql_structure(normalize_sql(PostgreSQL_3_SQLGlot), normalize_sql(PostgreSQL_3_LLM)),
            f"SQL structures don't match after normalization.\n\nActual: {normalize_sql(PostgreSQL_3_SQLGlot)}\n\nExpected: {normalize_sql(PostgreSQL_3_LLM)}"
        )
    def test_case4(self):
        # Transpile from T-SQL to PostgreSQL
        PostgreSQL_4_SQLGlot = transpile(TSQL_4, read="tsql", write="postgres")[0]
        PostgreSQL_4_LLM = call_openai_api(TSQL_4)
        self.assertTrue(
            compare_sql_structure(normalize_sql(PostgreSQL_4_SQLGlot), normalize_sql(PostgreSQL_4_LLM)),
            f"SQL structures don't match after normalization.\n\nActual: {normalize_sql(PostgreSQL_4_SQLGlot)}\n\nExpected: {normalize_sql(PostgreSQL_4_LLM)}"
        )
    def test_case5(self):
        # Transpile from T-SQL to PostgreSQL
        PostgreSQL_5_SQLGlot = transpile(TSQL_5, read="tsql", write="postgres")[0]
        PostgreSQL_5_LLM = call_openai_api(TSQL_5)
        self.assertTrue(
            compare_sql_structure(normalize_sql(PostgreSQL_5_SQLGlot), normalize_sql(PostgreSQL_5_LLM)),
            f"SQL structures don't match after normalization.\n\nActual: {normalize_sql(PostgreSQL_5_SQLGlot)}\n\nExpected: {normalize_sql(PostgreSQL_5_LLM)}"
        )


def run_tests():
    class VerboseTestResult(unittest.TextTestResult):
        def addSuccess(self, test):
            super().addSuccess(test)
            print(f"{test.id()} - PASS")
        def addFailure(self, test, err):
            super().addFailure(test, err)
            print(f"{test.id()} - FAIL: {err[1]}")
        def addError(self, test, err):
            super().addError(test, err)
            print(f"{test.id()} - ERROR: {err[1]}")

    loader = unittest.TestLoader()
    suite1 = loader.loadTestsFromTestCase(TestTranspileSQL)
    suite = unittest.TestSuite([suite1])
    runner = unittest.TextTestRunner(resultclass=VerboseTestResult, verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_tests()


