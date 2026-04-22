# Programming Languages & Advanced Concepts

This document provides a comprehensive overview of advanced programming concepts, design patterns, software principles, and testing methodologies crucial for test automation architecture.

---

## 1. Java Advanced Concepts

### Streams
**Concept:** Introduced in Java 8, Streams provide a declarative approach to process collections of objects. They allow for functional-style operations (filter, map, reduce) on streams of elements.
**Example:**
```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");
// Filter names starting with 'A' and convert to uppercase
List<String> filteredNames = names.stream()
                                  .filter(name -> name.startsWith("A"))
                                  .map(String::toUpperCase)
                                  .collect(Collectors.toList());
```

### Collections
**Concept:** The Java Collections Framework provides an architecture to store and manipulate groups of objects (Set, List, Queue, Deque, Map).
**Example:** Using a `HashMap` to store configuration properties or test data.
```java
Map<String, String> config = new HashMap<>();
config.put("browser", "chrome");
config.put("timeout", "30");
```

### Generics
**Concept:** Generics enable types (classes and interfaces) to be parameters when defining classes, interfaces, and methods. This provides compile-time type safety.
**Example:** Creating a generic API response wrapper.
```java
public class ApiResponse<T> {
    private int statusCode;
    private T data;
    // getters and setters
}
// Usage
ApiResponse<User> userResponse = new ApiResponse<>();
```

### Reflection
**Concept:** Reflection allows an executing Java program to examine or "introspect" upon itself, and manipulate internal properties of the program. Heavily used in frameworks like TestNG to find methods annotated with `@Test`.
**Example:** Instantiating a class dynamically.
```java
Class<?> clazz = Class.forName("com.framework.pages.LoginPage");
Object loginPage = clazz.getDeclaredConstructor(WebDriver.class).newInstance(driver);
```

### Annotations
**Concept:** Annotations provide metadata about the program that is not part of the program itself. They have no direct effect on the operation of the code they annotate.
**Example:** Custom annotation for test case tracking.
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface TestCaseId {
    String value();
}

@Test
@TestCaseId("TC-101")
public void verifyLogin() { ... }
```

---

## 2. Python Advanced Concepts

### Decorators
**Concept:** A decorator is a function that takes another function and extends the behavior of the latter function without explicitly modifying it.
**Example:** A decorator to automatically log execution time of a test step.
```python
import time

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Executed {func.__name__} in {time.time() - start} seconds")
        return result
    return wrapper

@log_execution_time
def click_login_button():
    # click logic
    pass
```

### Generators
**Concept:** Generators are a simple way of creating iterators using the `yield` keyword. They do not store all values in memory, making them highly efficient for large datasets (e.g., streaming large test data files).
**Example:** Generating infinite test user IDs.
```python
def user_id_generator():
    id = 1
    while True:
        yield f"test_user_{id}"
        id += 1

gen = user_id_generator()
print(next(gen)) # test_user_1
```

### Context Managers
**Concept:** Used to allocate and release resources precisely when you want to. The most widely used example of context managers is the `with` statement.
**Example:** Managing database connections or file streams ensuring they close safely even if an error occurs.
```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = connect_to_db()
        return self.conn
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

with DatabaseConnection() as db:
    db.execute("SELECT * FROM users")
```

### OOP (Object-Oriented Programming)
**Concept:** Python supports multiple inheritance, encapsulation, polymorphism, and abstraction.
**Example:** A base page object demonstrating inheritance.
```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver
    def click(self, locator):
        self.driver.find_element(*locator).click()

class LoginPage(BasePage):
    def login(self):
        self.click(('id', 'login-btn'))
```

---

## 3. C# / .NET Advanced Concepts

### LINQ (Language Integrated Query)
**Concept:** LINQ provides query capabilities directly into the C# language, allowing you to query collections, databases, and XML in a readable manner.
**Example:** Filtering a list of UI elements.
```csharp
var activeButtons = webElements.Where(el => el.Displayed && el.Enabled).ToList();
```

### Async / Await
**Concept:** Used for asynchronous programming to prevent blocking the main execution thread, highly valuable for I/O operations like API calls or DB queries in tests.
**Example:**
```csharp
public async Task<User> GetUserAsync(int id) {
    var response = await httpClient.GetAsync($"/users/{id}");
    return await response.Content.ReadFromJsonAsync<User>();
}
```

### Attributes
**Concept:** Similar to Java Annotations, Attributes provide metadata to assemblies, classes, or methods (used heavily in NUnit/xUnit).
**Example:**
```csharp
[Test, Category("Smoke")]
public void VerifyHomePageLoads() { ... }
```

---

## 4. JavaScript / TypeScript Advanced Concepts

### Promises and Async/Await
**Concept:** Promises represent the eventual completion (or failure) of an asynchronous operation. `async/await` is syntactic sugar over Promises, making asynchronous code look synchronous. Essential for Playwright/Cypress.
**Example:**
```javascript
// Playwright example
async function login(page) {
    await page.fill('#username', 'admin');
    await page.click('#submit');
    const title = await page.title();
    return title;
}
```

### Closures
**Concept:** A closure is the combination of a function bundled together (enclosed) with references to its surrounding state (the lexical environment).
**Example:** Creating private variables in JS.
```javascript
function makeCounter() {
    let count = 0; // Private variable
    return function() {
        return ++count;
    };
}
const counter = makeCounter();
console.log(counter()); // 1
```

### Prototypes
**Concept:** JavaScript objects inherit properties and methods from a prototype. This is how JS handles inheritance before ES6 classes.
**Example:**
```javascript
function Page(url) { this.url = url; }
Page.prototype.navigate = function() { console.log("Navigating to " + this.url); };
const home = new Page("/home");
home.navigate();
```

---

## 5. Design Patterns in Automation

### Singleton
**Concept:** Ensures a class has only one instance and provides a global point of access.
**Usage:** Managing WebDriver setup, Configuration Managers, or Database connections.

### Factory
**Concept:** Creates objects without exposing the instantiation logic to the client.
**Usage:** `WebDriverFactory.getDriver("chrome")` to abstract browser initialization logic.

### Builder
**Concept:** Separates the construction of a complex object from its representation.
**Usage:** Constructing complex API payloads or User test data objects step-by-step (`new UserBuilder().withName("A").withAge(25).build()`).

### Observer
**Concept:** Defines a one-to-many dependency so that when one object changes state, all its dependents are notified.
**Usage:** Custom reporting or logging engines that "observe" the test runner and log events when tests pass/fail.

### Strategy
**Concept:** Defines a family of algorithms, encapsulates each one, and makes them interchangeable.
**Usage:** Implementing different payment methods (PayPalStrategy, CreditCardStrategy) in an E-Commerce checkout test.

### Decorator
**Concept:** Attaches additional responsibilities to an object dynamically.
**Usage:** Wrapping a standard WebElement with additional logging or auto-waiting capabilities before performing the actual click.

---

## 6. SOLID Principles

*   **S - Single Responsibility Principle (SRP):** A class should have one, and only one, reason to change. (A `LoginPage` class should only handle login interactions, not database cleanups).
*   **O - Open/Closed Principle (OCP):** Software entities should be open for extension, but closed for modification. (Use interfaces/inheritance to add a new browser type rather than modifying existing factory code with more `if/else` blocks).
*   **L - Liskov Substitution Principle (LSP):** Objects of a superclass shall be replaceable with objects of its subclasses without breaking the application. (If a test expects a `BasePage`, providing a `HomePage` subclass shouldn't break the test).
*   **I - Interface Segregation Principle (ISP):** Clients should not be forced to depend upon interfaces that they do not use. (Instead of one massive `IMobileDriver`, have `IAndroidDriver` and `IIOSDriver`).
*   **D - Dependency Inversion Principle (DIP):** High-level modules should not depend on low-level modules. Both should depend on abstractions. (Test scripts should depend on a generic `IWebDriver` interface, not a concrete `ChromeDriver` implementation).

---

## 7. DRY, KISS, YAGNI Principles
*   **DRY (Don't Repeat Yourself):** Avoid duplicating code. If you write the same login logic in 5 tests, move it to a Page Object method.
*   **KISS (Keep It Simple, Stupid):** Avoid unnecessary complexity in framework design. A simple readable framework is better than an over-engineered one that nobody understands.
*   **YAGNI (You Aren't Gonna Need It):** Don't implement features or abstractions until they are actually needed. Don't build a complex cloud-grid integration if you currently only need to run tests locally.

---

## 8. Refactoring Techniques and Code Smells
**Code Smells (Indicators of poor design):**
*   **Duplicated Code:** Same logic in multiple places.
*   **Long Method:** Methods that do too much (e.g., a test that logs in, navigates, creates data, and asserts all in 100 lines).
*   **Large Class:** Page objects containing thousands of lines.
*   **Shotgun Surgery:** Making one small change requires altering many different classes.

**Refactoring Techniques:**
*   **Extract Method:** Moving chunks of code inside a long method into a new, well-named method.
*   **Rename Variable/Method:** Giving clear, intention-revealing names.
*   **Extract Class:** Splitting a large class into two smaller ones based on SRP.

---

## 9. Dependency Injection (DI) and IoC Containers
**Concept:** Inversion of Control (IoC) delegates the responsibility of object creation to a container or framework. DI is a technique to achieve IoC, where dependencies are passed into an object (usually via constructor) rather than the object creating them itself.
**Usage in Testing:** Using DI frameworks like Spring, Guice, or native constructors to inject configurations, WebDriver instances, or API clients into test classes, making tests highly modular and easily mockable.

---

## 10. Mocking and Stubbing Frameworks
**Concept:** Used primarily in Unit and Integration testing to isolate the system under test by replacing external dependencies with controlled, fake versions.
*   **Stub:** Provides pre-programmed responses to calls.
*   **Mock:** A stub that also verifies that specific methods were called with specific parameters.
**Frameworks:**
*   **Mockito (Java):** `when(mockService.getUser(1)).thenReturn(mockUser);`
*   **Moq (C#):** `mock.Setup(m => m.GetUser(1)).Returns(mockUser);`
*   **Jest (JavaScript):** `jest.fn().mockReturnValue(mockUser);`

---

## 11. Unit Testing Best Practices
*   **Fast Execution:** Unit tests should run in milliseconds. No DB or network calls.
*   **Deterministic:** Must pass consistently; no flakiness.
*   **AAA Pattern (Arrange, Act, Assert):** Clear structure for test blocks.
*   **One Assertion per Test (Ideally):** Focus the test on verifying one specific behavior.
*   **Meaningful Names:** Method names should explain what is being tested and the expected outcome (e.g., `calculateDiscount_WithValidCode_ReturnsDiscountedPrice()`).

---

## 12. Integration Testing Approaches
**Concept:** Verifying the interaction between different modules or services.
*   **Big Bang:** Integrating all components at once (risky).
*   **Top-Down / Bottom-Up:** Incremental integration using Stubs (for missing lower components) or Drivers (for missing higher components).
*   **Database Integration:** Testing DAO layers against a real (but isolated/containerized) database using tools like Testcontainers.
*   **API Contract Testing:** Verifying microservice communication using tools like Pact.

---

## 13. TDD and ATDD
*   **TDD (Test-Driven Development):** A developer workflow: Write a failing unit test -> Write the minimal code to make it pass -> Refactor. Ensures high code coverage and modular design.
*   **ATDD (Acceptance Test-Driven Development):** A collaborative workflow: Business, Dev, and QA define acceptance criteria (often in BDD/Gherkin format) *before* development starts. These criteria become the automated acceptance tests. Development is complete when the automated acceptance tests pass.