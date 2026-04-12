# 🔑 Keyword-Driven Framework

## 📌 Core Concept
A Keyword-Driven framework completely externalizes both **Test Data** AND **Test Instructions (Actions)** into an external file (usually Excel). The automation code simply acts as an "Engine" that reads the spreadsheet, looks at the requested keyword (e.g., `CLICK`, `TYPE`), and translates it into Selenium commands.

### 🛠️ Architecture Components
1.  **Test Cases (Excel):** A spreadsheet containing columns like: `Test Step`, `Keyword`, `Locator Type`, `Locator Value`, and `Data`.
2.  **Action Keywords Class:** A Java class containing wrapper methods for Selenium actions (e.g., `public void click(String xpath)`).
3.  **Execution Engine (Java Reflection):** A loop that reads the Excel rows one by one. It uses the **Java Reflection API** to dynamically find the method in the `ActionKeywords` class that matches the string in the Excel file, and executes it.

### 🌟 Advantages for SDETs
*   **Zero-Code Test Creation:** A manual tester who knows absolutely zero Java or Selenium can write a fully functional, 50-step End-to-End automation test simply by filling out an Excel spreadsheet using standard keywords.
*   **High Abstraction:** If the underlying tool changes (e.g., migrating from Selenium to Playwright), you only update the underlying `ActionKeywords.java` class. The hundreds of Excel test cases remain entirely untouched.

---

## 🧠 Memory Trick for Interviews
### The "Marionette Puppet" 🎭
*   **The Excel File (The Puppeteer):** The spreadsheet is pulling the strings. It dictates exactly *what* to do and *when* to do it.
*   **The Execution Engine (The Strings):** The Java Reflection engine acts as the strings, reading the command and pulling the right limb.
*   **The Action Class (The Puppet):** The Selenium code just blindly executes the action without knowing the broader context of the test.
*   **Key Phrase:** *"It achieves ultimate abstraction by externalizing test steps and data into spreadsheets, utilizing the Java Reflection API to dynamically invoke Selenium actions, enabling zero-code automation for non-technical QA."*