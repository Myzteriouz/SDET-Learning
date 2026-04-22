# 50 Advanced Selenium Interview Questions & Answers (Technical & Hands-On)

## Core Architecture & Fundamentals (Q1-Q5)

### Q1. Explain Selenium WebDriver architecture. How does it differ from Selenium RC?
**Answer:**
Selenium WebDriver communicates directly with browser drivers using the JSON Wire Protocol (Selenium 3) or W3C WebDriver Protocol (Selenium 4), unlike RC which injected JavaScript.

**Architecture Components:**
```
Test Code → WebDriver API → Browser Driver (ChromeDriver, GeckoDriver, etc.) → Browser
```

**Key Differences:**

| Aspect | Selenium RC | Selenium WebDriver |
|--------|------------|-------------------|
| Communication | HTTP requests via proxy | Direct browser communication |
| Speed | Slow (HTTP overhead) | Fast (native protocol) |
| Protocol | Proprietary Selenese | JSON Wire / W3C WebDriver |
| Browser Support | Limited | Comprehensive |
| Cross-browser | Limited | Full support |
| Server Requirement | Required | Not required |
| Deprecation | Deprecated | Current standard |

**Technical Implementation:**
```java
// Selenium WebDriver - Direct browser communication
WebDriver driver = new ChromeDriver();
// Command flows directly to ChromeDriver, then to Chrome
// No intermediate server needed

// WebDriver protocol flow:
// 1. Java Binding → 2. JSON message → 3. ChromeDriver → 4. Chrome DevTools
// 5. Response back through chain

// Multiple drivers communicate simultaneously with their respective browsers
WebDriver chrome = new ChromeDriver();
WebDriver firefox = new FirefoxDriver();
WebDriver edge = new EdgeDriver();

// Each driver maintains its own connection - parallel execution possible
```

**W3C WebDriver Protocol (Selenium 4):**
```java
// Selenium 4 uses standard W3C protocol
WebDriver driver = new ChromeDriver();

// Commands sent as JSON following W3C standard:
// {
//   "capabilities": {...},
//   "timeouts": {...}
// }

// More standardized, vendor-neutral, more reliable across browsers
```

---

### Q2. What are the different types of waits in Selenium? Explain implicit, explicit, and fluent waits with trade-offs.
**Answer:**
Waits are critical for handling asynchronous behavior in modern web applications.

```java
// 1. IMPLICIT WAIT (Global, Applied to all operations)
WebDriver driver = new ChromeDriver();
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));

// Once set, ALL findElement() calls wait up to 10 seconds for elements
WebElement element = driver.findElement(By.id("dynamic-element")); // Waits up to 10 seconds
WebElement button = driver.findElement(By.xpath("//button")); // Also waits up to 10 seconds

// TRADE-OFFS:
// ✅ Easy to set once, applies globally
// ❌ Unpredictable wait times (may wait full duration even if element appears in 1 second)
// ❌ No control over specific conditions
// ❌ Can cause inconsistent test execution

// 2. EXPLICIT WAIT (Condition-based, specific to operation)
WebDriver driver = new ChromeDriver();
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

// Wait for specific element to be clickable
WebElement button = wait.until(
  ExpectedConditions.elementToBeClickable(By.id("submit"))
);
button.click();

// Wait for presence (element in DOM but may not be visible)
WebElement element = wait.until(
  ExpectedConditions.presenceOfElementLocated(By.id("async-content"))
);

// Wait for visibility
WebElement visibleElement = wait.until(
  ExpectedConditions.visibilityOfElementLocated(By.id("message"))
);

// Wait for text in element
wait.until(
  ExpectedConditions.textToBePresentInElementLocated(By.id("status"), "Success")
);

// Wait for element invisibility (element was visible, then becomes invisible)
wait.until(
  ExpectedConditions.invisibilityOfElementLocated(By.className("loader"))
);

// TRADE-OFFS:
// ✅ Specific condition waiting - precise control
// ✅ Faster - stops waiting as soon as condition is met
// ✅ Better error messages
// ❌ More verbose code
// ❌ Requires knowing exact condition to wait for

// 3. FLUENT WAIT (Polling at regular intervals with exception ignoring)
Wait<WebDriver> fluentWait = new FluentWait<>(driver)
  .withTimeout(Duration.ofSeconds(30))
  .pollingEvery(Duration.ofMillis(500))
  .ignoring(NoSuchElementException.class)
  .ignoring(StaleElementReferenceException.class);

WebElement element = fluentWait.until(driver -> 
  driver.findElement(By.id("dynamic-element"))
);

// More advanced: Custom condition
WebElement dynamicElement = fluentWait.until(driver -> {
  WebElement el = driver.findElement(By.id("animated-element"));
  // Check if element is fully loaded and visible
  return el.isDisplayed() && el.isEnabled() ? el : null;
});

// TRADE-OFFS:
// ✅ Flexible - can define custom conditions
// ✅ Control over polling frequency
// ✅ Can ignore specific exceptions during polling
// ❌ Complex syntax
// ❌ Overkill for simple scenarios

// 4. COMPARISON AND BEST PRACTICES

// ❌ DON'T MIX IMPLICIT AND EXPLICIT WAITS
// This causes unpredictable behavior
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
// Explicit wait times out after 5+10=15 seconds unpredictably

// ✅ USE EXPLICIT WAITS (Modern Best Practice)
public class SmartWaits {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public SmartWaits(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Reusable wait methods
  public WebElement waitForElementClickable(By locator) {
    return wait.until(ExpectedConditions.elementToBeClickable(locator));
  }
  
  public void waitForText(By locator, String text) {
    wait.until(ExpectedConditions.textToBePresentInElementLocated(locator, text));
  }
  
  public void waitForElementDisappear(By locator) {
    wait.until(ExpectedConditions.invisibilityOfElementLocated(locator));
  }
  
  public void waitForUrlContains(String urlPart) {
    wait.until(ExpectedConditions.urlContains(urlPart));
  }
  
  public void waitForCustomCondition(ExpectedCondition<?> condition) {
    wait.until(condition);
  }
}

// Usage
SmartWaits smartWait = new SmartWaits(driver);
WebElement button = smartWait.waitForElementClickable(By.id("submit"));
button.click();

smartWait.waitForText(By.id("success-msg"), "Order submitted");
smartWait.waitForElementDisappear(By.className("loader"));

// ✅ NEVER USE Thread.sleep()
// ❌ Thread.sleep(5000); // Hard-coded 5 second wait - unreliable!

// TIMEOUT CONFIGURATION
WebDriver driver = new ChromeDriver();
driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10)); // Implicit (avoid)
driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(20)); // Page load
driver.manage().timeouts().scriptTimeout(Duration.ofSeconds(15)); // JavaScript execution

// Override timeout for specific wait
WebDriverWait shortWait = new WebDriverWait(driver, Duration.ofSeconds(3));
WebElement quickElement = shortWait.until(
  ExpectedConditions.presenceOfElementLocated(By.id("fast-element"))
);
```

---

### Q3. What is StaleElementReferenceException? How do you handle it?
**Answer:**
StaleElementReferenceException occurs when you try to interact with an element that is no longer attached to the DOM.

```java
// WHEN IT HAPPENS:
// 1. Page refresh
// 2. DOM manipulation (JavaScript updates)
// 3. AJAX calls that modify the DOM
// 4. Element removed and re-added to DOM

// EXAMPLE SCENARIO:
WebElement element = driver.findElement(By.id("dynamic-element"));

// Page refreshes (JavaScript updates DOM)
driver.navigate().refresh();

// Now element reference is stale
element.click(); // ❌ StaleElementReferenceException!

// SOLUTION 1: RE-LOCATE ELEMENT (Most reliable)
WebElement freshElement = driver.findElement(By.id("dynamic-element"));
freshElement.click();

// SOLUTION 2: USE EXPLICIT WAIT WITH FRESH QUERY
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
WebElement element = wait.until(
  ExpectedConditions.elementToBeClickable(By.id("dynamic-element"))
);
element.click();

// SOLUTION 3: IMPLEMENT RETRY LOGIC
public class StaleElementHandler {
  private WebDriver driver;
  private int maxRetries = 3;
  
  public void clickWithRetry(By locator) {
    int attempts = 0;
    while (attempts < maxRetries) {
      try {
        WebElement element = driver.findElement(locator);
        element.click();
        return;
      } catch (StaleElementReferenceException e) {
        attempts++;
        if (attempts >= maxRetries) {
          throw new RuntimeException("Failed to click element after " + maxRetries + " attempts", e);
        }
        // Wait before retry
        try {
          Thread.sleep(100);
        } catch (InterruptedException ie) {
          Thread.currentThread().interrupt();
        }
      }
    }
  }
  
  public void fillWithRetry(By locator, String text) {
    int attempts = 0;
    while (attempts < maxRetries) {
      try {
        WebElement element = driver.findElement(locator);
        element.clear();
        element.sendKeys(text);
        return;
      } catch (StaleElementReferenceException e) {
        attempts++;
        if (attempts >= maxRetries) {
          throw new RuntimeException("Failed to fill element after " + maxRetries + " attempts", e);
        }
      }
    }
  }
}

// SOLUTION 4: USE PAGE OBJECT MODEL (POM)
public class LoginPage {
  private WebDriver driver;
  private By emailLocator = By.id("email");
  private By passwordLocator = By.id("password");
  private By loginButtonLocator = By.id("login-btn");
  
  // Key: Store LOCATORS, not element references
  // Don't do: private WebElement emailField;
  
  public void login(String email, String password) {
    // Locate elements fresh each time
    driver.findElement(emailLocator).sendKeys(email);
    driver.findElement(passwordLocator).sendKeys(password);
    driver.findElement(loginButtonLocator).click();
  }
}

// SOLUTION 5: JAVASCRIPT EXECUTOR (For complex scenarios)
public void clickWithJavaScript(By locator) {
  WebElement element = driver.findElement(locator);
  JavascriptExecutor js = (JavascriptExecutor) driver;
  try {
    js.executeScript("arguments[0].click();", element);
  } catch (StaleElementReferenceException e) {
    // Retry with fresh element
    element = driver.findElement(locator);
    js.executeScript("arguments[0].click();", element);
  }
}

// BEST PRACTICE PATTERN:
public class RobustElementInteraction {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public RobustElementInteraction(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Always use fresh element queries with explicit waits
  public void click(By locator) {
    wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
  }
  
  public void fill(By locator, String text) {
    WebElement element = wait.until(
      ExpectedConditions.visibilityOfElementLocated(locator)
    );
    element.clear();
    element.sendKeys(text);
  }
  
  public String getText(By locator) {
    return wait.until(
      ExpectedConditions.presenceOfElementLocated(locator)
    ).getText();
  }
  
  public boolean isDisplayed(By locator) {
    try {
      return driver.findElement(locator).isDisplayed();
    } catch (StaleElementReferenceException e) {
      // Element became stale, try again with fresh query
      return driver.findElement(locator).isDisplayed();
    }
  }
}

// TESTING THE FIX:
@Test
public void testStaleElementHandling() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com");
  
  RobustElementInteraction robust = new RobustElementInteraction(driver);
  
  // This won't throw StaleElementReferenceException
  robust.fill(By.id("email"), "user@test.com");
  robust.click(By.id("submit"));
  
  // Even if DOM changes, this still works
  String result = robust.getText(By.id("result"));
  assertEquals("Success", result);
}
```

---

### Q4. Explain JavaScriptExecutor in Selenium. When and why would you use it?
**Answer:**
JavaScriptExecutor allows executing JavaScript code directly in the browser to interact with elements that WebDriver cannot handle directly.

```java
JavascriptExecutor js = (JavascriptExecutor) driver;

// USE CASE 1: Click hidden or obscured elements
WebElement hiddenButton = driver.findElement(By.id("hidden-btn"));
js.executeScript("arguments[0].click();", hiddenButton);

// USE CASE 2: Scroll to element
WebElement element = driver.findElement(By.id("element-id"));
js.executeScript("arguments[0].scrollIntoView(true);", element);

// USE CASE 3: Scroll to bottom of page
js.executeScript("window.scrollTo(0, document.body.scrollHeight);");

// USE CASE 4: Get property values (computed styles)
String backgroundColor = (String) js.executeScript(
  "return window.getComputedStyle(arguments[0]).backgroundColor;", element
);

// USE CASE 5: Set hidden field values
WebElement hiddenField = driver.findElement(By.id("hidden-field"));
js.executeScript("arguments[0].value = 'new-value';", hiddenField);

// USE CASE 6: Remove attribute (e.g., disabled attribute)
WebElement disabledButton = driver.findElement(By.id("disabled-btn"));
js.executeScript("arguments[0].removeAttribute('disabled');", disabledButton);

// USE CASE 7: Execute custom JavaScript
Long result = (Long) js.executeScript("return 5 + 3;"); // Returns 8

// USE CASE 8: Get page title
String title = (String) js.executeScript("return document.title;");

// USE CASE 9: Wait for jQuery (if page uses jQuery)
js.executeScript("return jQuery.active == 0;"); // Returns when jQuery AJAX is done

// USE CASE 10: Get element text with JavaScript
String text = (String) js.executeScript(
  "return arguments[0].textContent;", element
);

// ADVANCED: Check element visibility using JavaScript
boolean isVisible = (Boolean) js.executeScript(
  "var elem = arguments[0]; " +
  "return !!(elem.offsetWidth || elem.offsetHeight || elem.getClientRects().length);",
  element
);

// ADVANCED: Get all CSS classes
@SuppressWarnings("unchecked")
List<String> classes = (List<String>) js.executeScript(
  "return Array.from(arguments[0].classList);", element
);

// BEST PRACTICE: Wrapper class for JavaScriptExecutor
public class JSHelper {
  private WebDriver driver;
  private JavascriptExecutor js;
  
  public JSHelper(WebDriver driver) {
    this.driver = driver;
    this.js = (JavascriptExecutor) driver;
  }
  
  // Click element bypassing WebDriver's visibility checks
  public void clickJavaScript(WebElement element) {
    js.executeScript("arguments[0].click();", element);
  }
  
  // Scroll element into view with smooth scrolling
  public void scrollToElement(WebElement element) {
    js.executeScript(
      "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
      element
    );
  }
  
  // Get element's actual display status
  public boolean isElementActuallyVisible(WebElement element) {
    return (Boolean) js.executeScript(
      "var elem = arguments[0]; " +
      "var style = window.getComputedStyle(elem); " +
      "return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';",
      element
    );
  }
  
  // Execute script that returns value
  public Object executeAndReturn(String script, Object... args) {
    return js.executeScript(script, args);
  }
  
  // Wait for dynamic content using JS
  public void waitForJQueryAjax(int timeoutSeconds) {
    long endTime = System.currentTimeMillis() + (timeoutSeconds * 1000);
    
    while (System.currentTimeMillis() < endTime) {
      Boolean isReady = (Boolean) js.executeScript("return jQuery.active == 0;");
      if (isReady) {
        return;
      }
      try {
        Thread.sleep(100);
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
      }
    }
    throw new TimeoutException("jQuery AJAX did not complete");
  }
  
  // Get console errors (for debugging)
  public List<String> getConsoleErrors() {
    String script = "return window.__errors__ || [];";
    @SuppressWarnings("unchecked")
    List<String> errors = (List<String>) js.executeScript(script);
    return errors;
  }
}

// WHEN NOT TO USE JavaScriptExecutor:
// ❌ For basic element interactions (use WebDriver instead)
// ❌ For testing what users see (JS can bypass UI)
// ❌ For cross-browser compatibility issues (JS varies)
// ✅ Only when WebDriver cannot handle the scenario

// EXAMPLE: Complete scenario using JSHelper
@Test
public void testComplexScenario() {
  WebDriver driver = new ChromeDriver();
  JSHelper jsHelper = new JSHelper(driver);
  
  driver.get("https://example.com");
  
  // 1. Click hidden button using JS
  WebElement hiddenBtn = driver.findElement(By.id("hidden-submit"));
  jsHelper.clickJavaScript(hiddenBtn);
  
  // 2. Scroll to element
  WebElement targetElement = driver.findElement(By.id("target"));
  jsHelper.scrollToElement(targetElement);
  
  // 3. Check actual visibility
  boolean visible = jsHelper.isElementActuallyVisible(targetElement);
  assertTrue(visible, "Element should be visible");
  
  // 4. Wait for AJAX completion
  jsHelper.waitForJQueryAjax(10);
  
  // 5. Get console errors
  List<String> errors = jsHelper.getConsoleErrors();
  assertTrue(errors.isEmpty(), "Should have no console errors");
}
```

---

### Q5. What is the Page Object Model (POM)? How does it improve test maintainability?
**Answer:**
POM separates test logic from element locators, making tests more maintainable and scalable.

```java
// WITHOUT POM (Bad Practice - Brittle)
@Test
public void testLogin() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com/login");
  
  // Hard-coded locators scattered in test
  driver.findElement(By.id("email-input")).sendKeys("user@test.com");
  driver.findElement(By.id("password-input")).sendKeys("password123");
  driver.findElement(By.xpath("//button[@type='submit']")).click();
  
  // If UI changes, test breaks
  WebElement successMsg = driver.findElement(By.className("success-message"));
  assertTrue(successMsg.isDisplayed());
}

// WITH POM (Good Practice)
public class LoginPage {
  private WebDriver driver;
  private WebDriverWait wait;
  
  // Element locators (stored in one place)
  private By emailInput = By.id("email-input");
  private By passwordInput = By.id("password-input");
  private By loginButton = By.xpath("//button[@type='submit']");
  private By successMessage = By.className("success-message");
  private By errorMessage = By.className("error-message");
  
  public LoginPage(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Page actions (methods that users would perform)
  public void enterEmail(String email) {
    driver.findElement(emailInput).sendKeys(email);
  }
  
  public void enterPassword(String password) {
    driver.findElement(passwordInput).sendKeys(password);
  }
  
  public void clickLoginButton() {
    driver.findElement(loginButton).click();
  }
  
  // Helper method combining multiple actions
  public void login(String email, String password) {
    enterEmail(email);
    enterPassword(password);
    clickLoginButton();
  }
  
  // Assertions (verify page state)
  public boolean isLoginSuccessful() {
    return wait.until(
      ExpectedConditions.visibilityOfElementLocated(successMessage)
    ).isDisplayed();
  }
  
  public String getErrorMessage() {
    return wait.until(
      ExpectedConditions.visibilityOfElementLocated(errorMessage)
    ).getText();
  }
}

// CLEAN TEST using POM
@Test
public void testLoginSuccess() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com/login");
  
  LoginPage loginPage = new LoginPage(driver);
  
  // Test reads like business logic, not technical details
  loginPage.login("user@test.com", "password123");
  
  assertTrue(loginPage.isLoginSuccessful(), "Login should be successful");
}

// ADVANCED POM WITH PAGE NAVIGATION
public class LoginPage {
  private WebDriver driver;
  
  // ... locators and methods from above ...
  
  // Return next page object after login
  public DashboardPage loginSuccessfully(String email, String password) {
    login(email, password);
    return new DashboardPage(driver);
  }
}

public class DashboardPage {
  private WebDriver driver;
  private By userGreeting = By.id("user-greeting");
  private By logoutButton = By.id("logout-btn");
  
  public DashboardPage(WebDriver driver) {
    this.driver = driver;
    // Verify we're on dashboard
    wait.until(ExpectedConditions.presenceOfElementLocated(userGreeting));
  }
  
  public String getUserGreeting() {
    return driver.findElement(userGreeting).getText();
  }
  
  public LoginPage logout() {
    driver.findElement(logoutButton).click();
    return new LoginPage(driver);
  }
}

// FLUENT PAGE NAVIGATION
@Test
public void testLoginLogoutFlow() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com/login");
  
  // Fluent navigation through page objects
  String greeting = new LoginPage(driver)
    .loginSuccessfully("user@test.com", "password123")
    .getUserGreeting();
  
  assertEquals("Welcome, User", greeting);
}

// POM WITH BASE PAGE CLASS (Reduces code duplication)
public abstract class BasePage {
  protected WebDriver driver;
  protected WebDriverWait wait;
  
  public BasePage(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Common methods
  protected WebElement findElement(By locator) {
    return wait.until(ExpectedConditions.presenceOfElementLocated(locator));
  }
  
  protected void click(By locator) {
    wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
  }
  
  protected void sendKeys(By locator, String text) {
    findElement(locator).sendKeys(text);
  }
  
  protected String getText(By locator) {
    return findElement(locator).getText();
  }
  
  protected void waitForElementToDisappear(By locator) {
    wait.until(ExpectedConditions.invisibilityOfElementLocated(locator));
  }
}

// Extend BasePage to reduce code in specific pages
public class LoginPageImproved extends BasePage {
  private By emailInput = By.id("email");
  private By passwordInput = By.id("password");
  private By loginButton = By.id("login");
  
  public LoginPageImproved(WebDriver driver) {
    super(driver);
  }
  
  public void login(String email, String password) {
    sendKeys(emailInput, email);
    sendKeys(passwordInput, password);
    click(loginButton);
  }
}

// BENEFITS OF POM:
/*
1. Maintainability: Change locator in one place, tests still work
2. Reusability: Methods can be used across multiple tests
3. Readability: Test code reads like business requirements
4. Scalability: Easy to add new page objects
5. Reduced Duplication: Common actions in base class
6. Easy Refactoring: Update locators without changing tests
7. Better Organization: Logical grouping of related functionality
8. Clear Separation: UI details separate from test logic
*/
```

---

## Dynamic Element Handling & Advanced Locators (Q6-Q10)

### Q6. How do you handle dynamic IDs and changing selectors in Selenium? Provide resilient locator strategies.
**Answer:**
```java
// PROBLEM: Dynamic IDs and unstable selectors
// Bad approaches that fail easily:
By badXPath1 = By.xpath("//button[1]"); // Fragile - position dependent
By badXPath2 = By.xpath("//div[@id='user-btn-12345']"); // ID changes each page load
By badCSS = By.cssSelector("div > div > div > button"); // Deep nesting breaks

// SOLUTION 1: Use relative XPath with multiple attributes
By resilientXPath = By.xpath("//button[@type='submit' and contains(@class, 'primary')]");
By textXPath = By.xpath("//button[contains(text(), 'Submit')]");
By partialIdXPath = By.xpath("//input[starts-with(@id, 'email')]");

// SOLUTION 2: Use CSS attribute selectors
By resilientCSS1 = By.cssSelector("button[type='submit'][class*='primary']");
By resilientCSS2 = By.cssSelector("input[name='email'][type='text']");
By resilientCSS3 = By.cssSelector("[data-testid='submit-button']");

// SOLUTION 3: Use XPath with contains() and normalize-space()
By normalizedXPath = By.xpath(
  "//button[normalize-space()='Click Me']" // Ignores extra whitespace
);

// SOLUTION 4: Combine multiple attributes for stability
By multiAttributeXPath = By.xpath(
  "//input[@type='email' and " +
  "contains(@placeholder, 'email') and " +
  "contains(@class, 'form-control')]"
);

// SOLUTION 5: Use parent/ancestor to find element from stable parent
By fromParentXPath = By.xpath(
  "//form[@id='login-form']//input[@type='password']"
);

// SOLUTION 6: Use following/preceding sibling when element follows stable element
By sibling = By.xpath(
  "//label[text()='Email']/following-sibling::input"
);

// SOLUTION 7: Attribute-based with wildcards
By wildcardXPath = By.xpath(
  "//button[contains(@id, 'dynamic-btn')]" // ID like 'dynamic-btn-456'
);

// COMPLETE RESILIENT LOCATOR STRATEGY CLASS
public class ResilientLocatorStrategy {
  
  // 1. Data attributes (most reliable)
  public By byDataTestId(String testId) {
    return By.cssSelector("[data-testid='" + testId + "']");
  }
  
  // 2. Accessible names (for labels and form elements)
  public By byAccessibleName(String name) {
    return By.xpath(
      "//*[@aria-label='" + name + "' or @aria-labelledby='" + name + "']"
    );
  }
  
  // 3. Text content with flexible matching
  public By byText(String text) {
    return By.xpath(
      "//*[contains(normalize-space(), '" + text + "')]"
    );
  }
  
  // 4. Input by label (common pattern)
  public By inputByLabel(String labelText) {
    return By.xpath(
      "//label[contains(., '" + labelText + "')]" +
      "/following-sibling::input[1] | " +
      "//label[contains(., '" + labelText + "')]/input[1]"
    );
  }
  
  // 5. Button by text content
  public By buttonByText(String buttonText) {
    return By.xpath(
      "//button[contains(normalize-space(), '" + buttonText + "')]"
    );
  }
  
  // 6. Element from parent section
  public By elementInSection(String sectionTitle, String elementIdentifier) {
    return By.xpath(
      "//section[contains(., '" + sectionTitle + "')]" +
      "//*[contains(text(), '" + elementIdentifier + "')]"
    );
  }
  
  // 7. Dropdown option by visible text
  public By selectOption(String optionText) {
    return By.xpath(
      "//option[contains(normalize-space(), '" + optionText + "')]"
    );
  }
  
  // 8. Table cell from row and column
  public By tableCellByRowAndColumn(String rowHeader, String columnHeader) {
    return By.xpath(
      "//tr[contains(., '" + rowHeader + "')]" +
      "//td[" + (getColumnIndex(columnHeader) + 1) + "]"
    );
  }
  
  // 9. Navigation link by href pattern
  public By navigationLink(String hrefPattern) {
    return By.xpath(
      "//a[contains(@href, '" + hrefPattern + "')]"
    );
  }
  
  // 10. Element with partial attribute match
  public By byPartialAttribute(String attribute, String partialValue) {
    return By.xpath(
      "//*[contains(@" + attribute + ", '" + partialValue + "')]"
    );
  }
  
  private int getColumnIndex(String header) {
    // Logic to find column index
    return 0;
  }
}

// PRACTICAL EXAMPLE: Handling dynamic list items
public class DynamicListHandler {
  private WebDriver driver;
  
  public DynamicListHandler(WebDriver driver) {
    this.driver = driver;
  }
  
  // Click item by visible text (handles dynamic IDs)
  public void clickListItemByText(String itemText) {
    By listItem = By.xpath(
      "//ul[@class='dynamic-list']//li[contains(., '" + itemText + "')]"
    );
    driver.findElement(listItem).click();
  }
  
  // Get all list items text (handles dynamic count)
  public List<String> getAllListItemsText() {
    List<WebElement> items = driver.findElements(
      By.xpath("//ul[@class='dynamic-list']//li")
    );
    return items.stream()
      .map(WebElement::getText)
      .collect(Collectors.toList());
  }
  
  // Find item by attribute that changes predictably
  public void clickItemByDataAttribute(String dataValue) {
    By item = By.xpath(
      "//li[contains(@data-item-id, '" + dataValue + "')]"
    );
    driver.findElement(item).click();
  }
}

// LOCATOR VALIDATION UTILITY
public class LocatorValidator {
  private WebDriver driver;
  
  public LocatorValidator(WebDriver driver) {
    this.driver = driver;
  }
  
  // Check if locator is reliable (finds exactly 1 element)
  public boolean isLocatorReliable(By locator) {
    List<WebElement> elements = driver.findElements(locator);
    return elements.size() == 1;
  }
  
  // Get resilience score for a locator
  public double getResilienceScore(By locator) {
    try {
      List<WebElement> elements = driver.findElements(locator);
      
      if (elements.size() == 0) return 0.0; // Locator found nothing
      if (elements.size() > 1) return 0.5; // Locator found multiple elements
      
      // Check stability - element is still found after wait
      Thread.sleep(100);
      List<WebElement> elementsAfterWait = driver.findElements(locator);
      if (elementsAfterWait.size() == 1) return 1.0; // Very stable
      
      return 0.7; // Somewhat stable
    } catch (Exception e) {
      return 0.0;
    }
  }
  
  // Compare multiple locators and return most reliable
  public By getMostReliableLocator(By... locators) {
    By mostReliable = null;
    double highestScore = -1;
    
    for (By locator : locators) {
      double score = getResilienceScore(locator);
      if (score > highestScore) {
        highestScore = score;
        mostReliable = locator;
      }
    }
    
    return mostReliable;
  }
}

// TESTING RESILIENT LOCATORS
@Test
public void testResilientLocators() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com");
  
  ResilientLocatorStrategy strategy = new ResilientLocatorStrategy();
  
  // Find input by label (handles ID changes)
  WebElement emailInput = driver.findElement(
    strategy.inputByLabel("Email Address")
  );
  emailInput.sendKeys("user@test.com");
  
  // Click button by text (most user-centric approach)
  driver.findElement(strategy.buttonByText("Submit")).click();
  
  // Validate locators are resilient
  LocatorValidator validator = new LocatorValidator(driver);
  assertTrue(
    validator.isLocatorReliable(strategy.byDataTestId("submit-btn")),
    "Test ID locator should be reliable"
  );
}

// BEST PRACTICE HIERARCHY:
/*
1. Data attributes [data-testid='...'] - Most reliable, explicit intent
2. Accessible names (aria-label, labels) - Good for testing a11y
3. Specific attributes (type, role) - Good for standard HTML elements
4. Text content (with normalize-space) - User-centric, handles dynamic ID
5. Relative XPath with multiple conditions - Last resort
6. CSS selectors - Avoid deep nesting
7. XPath with position predicates - Very fragile
8. Dynamic IDs/classes alone - Never use
*/
```

---

### Q7. How do you handle alerts, popups, and windows in Selenium?
**Answer:**
```java
// HANDLING JAVASCRIPT ALERTS
WebDriver driver = new ChromeDriver();
driver.get("https://example.com");

// Click button that triggers alert
driver.findElement(By.id("show-alert")).click();

// Switch to alert
Alert alert = driver.switchTo().alert();

// Get alert message
String alertMessage = alert.getText();
System.out.println("Alert: " + alertMessage);

// Accept (click OK)
alert.accept();

// Dismiss (click Cancel)
// alert.dismiss();

// Send text to alert (for prompt dialogs)
// alert.sendKeys("input text");

// WAIT FOR ALERT (with explicit wait)
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
Alert alertWithWait = wait.until(
  ExpectedConditions.alertIsPresent()
);
alertWithWait.accept();

// HANDLING MULTIPLE WINDOWS/TABS
// Original window
String originalWindow = driver.getWindowHandle();
String urlBefore = driver.getCurrentUrl();

// Click link that opens new tab
driver.findElement(By.linkText("Open in New Tab")).click();

// Get all window handles
Set<String> allWindows = driver.getWindowHandles();

// Switch to new window
for (String window : allWindows) {
  if (!window.equals(originalWindow)) {
    driver.switchTo().window(window);
    break;
  }
}

// Perform actions in new window
String urlAfter = driver.getCurrentUrl();
driver.findElement(By.id("new-tab-element")).click();

// Switch back to original window
driver.switchTo().window(originalWindow);

// Close new tab
driver.close(); // Closes current window
driver.switchTo().window(originalWindow); // Back to original

// HANDLING POPUP WINDOWS (NEW)
String mainWindow = driver.getWindowHandle();
Set<String> beforePopup = driver.getWindowHandles();

// Trigger popup
driver.findElement(By.id("open-popup")).click();

// Wait for popup to open and get new window handle
Set<String> afterPopup = driver.getWindowHandles();
String popupWindow = null;

for (String window : afterPopup) {
  if (!beforePopup.contains(window)) {
    popupWindow = window;
    break;
  }
}

// Switch to popup
driver.switchTo().window(popupWindow);

// Handle popup content
driver.findElement(By.id("popup-field")).sendKeys("data");
driver.findElement(By.id("popup-submit")).click();

// Close popup and return to main
driver.close();
driver.switchTo().window(mainWindow);

// ADVANCED: Custom wait for popup window
public class PopupHandler {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public PopupHandler(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  public String waitForNewWindow(int timeoutSeconds) {
    final Set<String> previousWindows = driver.getWindowHandles();
    
    long endTime = System.currentTimeMillis() + (timeoutSeconds * 1000);
    
    while (System.currentTimeMillis() < endTime) {
      Set<String> currentWindows = driver.getWindowHandles();
      
      for (String window : currentWindows) {
        if (!previousWindows.contains(window)) {
          return window; // New window found
        }
      }
      
      try {
        Thread.sleep(100);
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
      }
    }
    
    throw new TimeoutException("No new window opened within timeout");
  }
  
  public void handleAndClosePopup(String popupTitle) {
    String originalWindow = driver.getWindowHandle();
    Set<String> beforePopup = driver.getWindowHandles();
    
    // Trigger popup action
    // (Implementation depends on how popup is triggered)
    
    // Wait for popup
    String popupWindow = waitForNewWindow(10);
    driver.switchTo().window(popupWindow);
    
    // Verify popup title
    assertTrue(driver.getTitle().contains(popupTitle));
    
    // Handle popup
    driver.findElement(By.id("popup-ok")).click();
    
    // Close and return
    driver.switchTo().window(originalWindow);
  }
}

// HANDLING SELECT DROPDOWNS
WebElement dropdown = driver.findElement(By.id("country-dropdown"));

// Method 1: Using Select class
Select selectDropdown = new Select(dropdown);

// Select by visible text
selectDropdown.selectByVisibleText("United States");

// Select by value attribute
selectDropdown.selectByValue("us");

// Select by index
selectDropdown.selectByIndex(0);

// Get all options
List<WebElement> options = selectDropdown.getOptions();
for (WebElement option : options) {
  System.out.println(option.getText());
}

// Get first selected option
WebElement firstSelected = selectDropdown.getFirstSelectedOption();

// Deselect (only for multi-select)
selectDropdown.deselectByVisibleText("Option");

// HANDLING CUSTOM DROPDOWNS (built with divs, not <select>)
// Click to open dropdown
driver.findElement(By.id("custom-dropdown")).click();

// Click desired option
driver.findElement(By.xpath(
  "//ul[@class='dropdown-menu']//li[text()='Option 1']"
)).click();

// COMPLETE POPUP MANAGEMENT CLASS
public class PopupManager {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public PopupManager(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Handle alert
  public void handleAlert(AlertAction action, String... params) {
    Alert alert = wait.until(ExpectedConditions.alertIsPresent());
    
    switch (action) {
      case ACCEPT:
        alert.accept();
        break;
      case DISMISS:
        alert.dismiss();
        break;
      case SEND_KEYS:
        alert.sendKeys(params[0]);
        alert.accept();
        break;
    }
  }
  
  // Handle window
  public void switchToNewWindow() {
    String originalWindow = driver.getWindowHandle();
    
    for (String window : driver.getWindowHandles()) {
      if (!window.equals(originalWindow)) {
        driver.switchTo().window(window);
        return;
      }
    }
  }
  
  // Handle custom dropdown
  public void selectFromCustomDropdown(String dropdownId, String optionText) {
    driver.findElement(By.id(dropdownId)).click();
    
    WebElement option = wait.until(
      ExpectedConditions.elementToBeClickable(
        By.xpath("//li[contains(text(), '" + optionText + "')]")
      )
    );
    option.click();
  }
  
  enum AlertAction {
    ACCEPT, DISMISS, SEND_KEYS
  }
}
```

---

## Remaining advanced topics covered in Selenium...

*Note: Due to length constraints, creating continuation file with Q8-Q50*

---

