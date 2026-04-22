# Core Testing & QA Fundamentals

## 1. Test Pyramid (Unit, Integration, E2E Ratio Optimization)
**Concept:** The Test Pyramid is a framework that helps development and QA teams build a balanced, fast, and reliable test portfolio. It advocates for a foundation of many fast, isolated Unit Tests, a middle layer of Integration Tests, and a small peak of slow, brittle End-to-End (E2E) UI tests.
**Ratio Optimization:** A common healthy ratio is **70% Unit, 20% Integration, 10% E2E**.
**Practical Example:**
*   **Unit (70%):** Testing a `calculateDiscount(price, discountPercentage)` function in isolation to ensure the math logic is correct. *Execution time: Milliseconds.*
*   **Integration (20%):** Testing that the `OrderService` correctly saves the discounted price into the `PostgreSQL` database or communicates correctly with the Stripe API. *Execution time: Seconds.*
*   **E2E (10%):** Using Playwright/Selenium to log in, add an item to the cart, apply a discount code on the UI, checkout, and verify the success page renders. *Execution time: Minutes.*

---

## 2. Test Types
*   **Functional Testing:** Verifies *what* the system does against business requirements.
    *   *Example:* Does the "Login" button successfully authenticate the user when valid credentials are provided?
*   **Non-Functional Testing:** Verifies *how* the system performs (performance, security, usability, reliability).
    *   *Example:* Load testing the login API to ensure it can handle 10,000 concurrent users with less than a 2-second response latency.
*   **Smoke Testing:** A shallow, wide test of critical basic functionality after a new build to ensure it's stable enough for deeper testing.
    *   *Example:* Checking if the application launches, the homepage loads, and the database connects without crashing.
*   **Sanity Testing:** A deep, narrow test focused on a specific component or newly added feature to ensure bugs were fixed.
    *   *Example:* After a developer fixes a bug in the payment module, you aggressively test *only* the payment gateway integration.
*   **Regression Testing:** Running previously passed tests to ensure recent code changes (new features or fixes) haven't broken existing functionality.
    *   *Example:* Running the entire automated UI suite before a production release to ensure the new "dark mode" feature didn't break the checkout button.

---

## 3. Black-Box, White-Box, and Gray-Box Testing
*   **Black-Box Testing:** Testing without knowing the internal code structure. Based purely on inputs and expected outputs.
    *   *Example:* Testing a search bar by typing "shoes" and expecting a list of shoes, without knowing the SQL query used behind the scenes.
*   **White-Box Testing:** Testing with full knowledge of the internal code, logic, and architecture.
    *   *Example:* Writing unit tests to ensure every `if/else` branch in a tax calculation algorithm is executed by the test data.
*   **Gray-Box Testing:** A combination of both. Testing with partial knowledge of internals (e.g., database structure, API endpoints).
    *   *Example:* Submitting a user registration form on the UI (Black-box) and then writing an automated script to query the database directly (White-box knowledge) to verify the password hash was generated correctly.

---

## 4. Boundary Value Analysis (BVA) and Equivalence Partitioning (EP)
**Concept:** Systematic techniques to drastically reduce the number of test cases while maintaining high defect detection rates.
*   **Equivalence Partitioning (EP):** Dividing inputs into groups (partitions) where the system is expected to behave the same way. You only test one representative value per partition.
*   **Boundary Value Analysis (BVA):** Bugs often occur at the edges of boundaries. BVA tests the exact boundary, one unit below, and one unit above.
**Practical Example:** A password field requires exactly 8 to 12 characters.
*   **EP Partitions:**
    *   Invalid (Too short): 1-7 chars -> *Test with length 5*
    *   Valid: 8-12 chars -> *Test with length 10*
    *   Invalid (Too long): 13+ chars -> *Test with length 15*
*   **BVA Test Cases:** You must test the exact boundaries and edges: Lengths **7, 8, 9, 11, 12, 13**.

---

## 5. State Transition and Decision Table Testing
*   **State Transition Testing:** Used when a system moves from one state to another depending on inputs.
    *   *Example:* An ATM card system. State 1: Active. State 2: Blocked. Transition: 3 consecutive wrong PINs move the state from Active to Blocked. Tests verify correct state changes and ensure a blocked card cannot withdraw money.
*   **Decision Table Testing:** Used for complex business logic with multiple condition combinations (if/then rules).
    *   *Example:* E-commerce shipping logic.
        *   Condition 1: Prime Member? (Y/N)
        *   Condition 2: Cart > $50? (Y/N)
        *   Rule 1: Y, Y -> Free 1-Day Shipping
        *   Rule 2: Y, N -> Free 2-Day Shipping
        *   Rule 3: N, Y -> Free Standard Shipping
        *   Rule 4: N, N -> $5.99 Shipping

---

## 6. Exploratory Testing and Test Case Design Techniques
*   **Exploratory Testing:** Simultaneous learning, test design, and test execution. It is unscripted and relies on the tester's intuition, domain knowledge, and heuristics to find edge-case bugs that rigid automated scripts miss.
    *   *Example:* A tester exploring a new chat feature by rapidly clicking "send," pasting 10MB images, using emojis, and disconnecting the network cable mid-send to see how the app handles unexpected stress, rather than following a step-by-step Excel script.

---

## 7. Test Coverage Metrics
*   **Code Coverage (Line Coverage):** The percentage of executable lines of code that are touched by automated tests.
*   **Branch Coverage:** The percentage of control flow branches (e.g., the `true` and `false` paths of an `if` statement) executed.
*   **Path Coverage:** The percentage of all possible execution paths through a function from start to finish.
**Practical Example:**
```java
public String checkNumber(int x) {
    if (x > 0) {
        return "Positive";
    } else {
        return "Non-Positive";
    }
}
```
*   To get 100% *Line Coverage*, testing `checkNumber(5)` might be enough for some tools if they don't count the `else` block strictly.
*   To get 100% *Branch Coverage*, you **must** write two tests: `checkNumber(5)` (tests the `true` branch) and `checkNumber(-1)` (tests the `false` branch).

---

## 8. Mutation Testing
**Concept:** A technique to evaluate the *quality of your tests*. It modifies (mutates) the application's source code slightly to introduce deliberate bugs (mutants). If your test suite still passes, your tests are weak (they failed to "kill the mutant"). If the tests fail, your tests are strong.
**Practical Example:**
*   *Original Code:* `if (age >= 18) { grantAccess(); }`
*   *Mutant Code (Injected by tool):* `if (age > 18) { grantAccess(); }`
*   If your only automated test uses `age = 20`, the test passes on both the original and mutated code. The mutant survives. You need a BVA test with `age = 18` to kill this mutant, proving your tests are robust.

---

## 9. Risk-Based Testing Prioritization
**Concept:** Prioritizing test execution based on the probability of a failure and the business impact of that failure. Critical when time is limited before a release.
**Practical Example:**
*   *High Risk (Test First/Heavily Automate):* Checkout gateway, User Authentication, Database writes. If these fail, the company loses money and reputation immediately.
*   *Low Risk (Test Later/Manual checks):* Changing the copyright year in the website footer. If this fails, the impact is purely cosmetic.

---

## 10. Shift-Left Testing Strategy
**Concept:** Moving testing earlier in the Software Development Life Cycle (SDLC). Instead of waiting for a feature to be "finished" by developers to test it, QA is involved from Day 1.
**Practical Example:**
*   *Traditional:* Dev writes code -> Deploys to QA environment -> QA writes/runs tests (Bugs found late are expensive to fix).
*   *Shift-Left:* QA reviews the Jira ticket before coding starts and identifies missing edge cases in requirements. Dev and QA pair-program or use BDD (Behavior Driven Development). Static analysis and unit tests run automatically on every single code commit.

---

## 11. Testing in Production (TiP) and Canary Testing
**Concept:** Moving beyond pre-production environments to validate code safely in the real world.
*   **Testing in Production (TiP):** Running safe, non-destructive automated tests (or using synthetic monitoring) in the live environment to ensure infrastructure, configurations, and third-party integrations hold up under real user load.
*   **Canary Testing:** Releasing a new feature to a very small subset of live users (e.g., 5% of traffic).
**Practical Example:** 
A company rolls out a new Database schema. Instead of switching all users over, they route 2% of traffic to the new schema (Canary). Automated observability tools monitor the error rates and server load. If metrics remain stable for 1 hour, the rollout expands to 10%, then 50%, then 100%. If metrics spike, the system automatically rolls back the release.
