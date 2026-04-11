# 🏗️ Builder Pattern with POM (SDET Guide)

## 📌 What is the Builder Pattern?
The Builder Pattern is a creational design pattern used to construct complex objects step by step. It allows you to produce different types and representations of an object using the same construction code.

### 💡 The Problem it Solves in Test Automation:
**The "Telescoping Constructor Anti-Pattern" / "Parameter Creep".**
Imagine a `User` class for a registration form with 10 fields (2 mandatory, 8 optional).
If you use standard constructors, you end up with:
`new User("John", "Doe", null, null, "555-1234", null, null, null);`
This is completely unreadable. What do those `null`s mean? 

In the POM, it leads to methods like `registerUser(String fn, String ln, String phone, String dob, ...)` which are a nightmare to maintain.

### 🛠️ How Our Framework Uses It:
1. **`UserAccount.UserAccountBuilder`**: We created a static inner Builder class. It takes mandatory fields in its constructor and uses fluent "setter" methods (like `withPhone()`) for optional fields.
2. **Data Object passing to POM**: Our `RegistrationPage.java` no longer takes 6 parameters. It takes ONE `UserAccount` object. It then intelligently checks if the optional fields (`user.getPhone() != null`) exist before interacting with the UI.

### 🌟 Advantages for SDETs
*   **Immutability:** The `UserAccount` object has no public setters. Once built, it cannot be accidentally modified during the test execution, preventing flaky test data state.
*   **Fluent Interface:** The test code reads like an English sentence (`UserBuilder(m).withA().withB().build()`).

---

## 🧠 Memory Trick for Interviews
### The "Custom Subway Sandwich" 🥪
*   **Mandatory:** When you walk into Subway, you *must* choose a bread and a meat (The `Builder` Constructor).
*   **Optional:** Then, you walk down the line: "with lettuce", "with tomatoes", "with extra mayo" (The `.with...()` methods). You chain these together.
*   **Build:** Finally, the worker wraps it up and hands it to you (The `.build()` method).
*   **Key Phrase:** *"It solves the Telescoping Constructor problem by constructing complex test-data objects step-by-step using a fluent API."*
