# 📊 Data-Driven Framework (TestNG + Apache POI)

## 📌 Core Concept
A Data-Driven framework strictly separates the **Test Script Logic** from the **Test Data**. Instead of hardcoding credentials or search terms into the Java code, data is maintained externally (Excel, CSV, JSON, Database). The framework reads this external source and iteratively feeds it into the test script.

### 🛠️ Architecture Components
1.  **Test Data Source:** An Excel file (`.xlsx`) or JSON file containing rows of test parameters.
2.  **Data Reader Utility:** A dedicated class (e.g., `ExcelReader.java` using Apache POI) responsible for parsing the file and converting it into Java objects (usually `Object[][]`).
3.  **Test Runner (TestNG):** Uses the `@DataProvider` annotation to link the Data Reader utility to the `@Test` method. The test method executes once for every row of data returned.

### 🌟 Advantages for SDETs
*   **Scalability without Code Changes:** To test 50 new login scenarios (e.g., blank password, SQL injection string, special characters), a manual tester simply adds 50 rows to the Excel sheet. Zero Java code needs to be modified.
*   **Reusability:** The same login test script is reused infinitely for all data permutations.
*   **Role Separation:** Non-technical stakeholders (Product Owners, Manual QA) can contribute to automation coverage purely by managing the Excel files.

---

## 🧠 Memory Trick for Interviews
### The "Assembly Line & The Hopper" 🏭
*   **The Machine:** Your `@Test` method is an assembly line machine. It knows *how* to process an item, but it doesn't contain the raw materials.
*   **The Hopper:** The `@DataProvider` is the hopper feeding the machine. It grabs raw materials from the warehouse (Excel file).
*   **Execution:** The machine doesn't care if the hopper feeds it 1 item or 10,000 items. It will process them identically without changing its internal gears.
*   **Key Phrase:** *"It achieves maximum test coverage with minimal code by decoupling data from logic, utilizing TestNG's DataProvider and Apache POI to dynamically execute a single script against multiple datasets."*