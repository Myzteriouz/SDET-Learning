# 50 Advanced Playwright Interview Questions & Answers (Technical & Hands-On)

## Architecture & Core Concepts (Q1-Q5)

### Q1. Explain Playwright's architecture and how it differs from Selenium's WebDriver architecture.
**Answer:**
Playwright uses the **DevTools Protocol (CDP)** to communicate with browsers via a single persistent WebSocket connection, unlike Selenium which sends individual HTTP requests for each command.

**Technical Details:**
- Selenium: Each command = separate HTTP request → slower, more failure points
- Playwright: Single WebSocket connection → fast command transmission, reduced latency
- Playwright talks directly to browser drivers without an intermediary server
- This architecture enables auto-waiting and better synchronization

**Code Example:**
```javascript
// Playwright - Single persistent connection handles all commands
const browser = await chromium.launch();
const page = await browser.newPage();
// All subsequent operations use the same connection
await page.goto('https://example.com');
await page.locator('#button').click();
```

---

### Q2. What is the difference between BrowserContext and Page objects in Playwright? When would you use multiple contexts?
**Answer:**
- **BrowserContext**: Isolated browser session (like an incognito window) with its own cookies, storage, and session data
- **Page**: Single tab/window within a context
- One context can have multiple pages, but they share state

**Use Cases for Multiple Contexts:**
- Testing multiple user accounts simultaneously without interference
- Simulating parallel user sessions in one browser instance
- A/B testing with different user scenarios
- Testing cross-user interactions (one user sends message, another receives)

**Technical Implementation:**
```javascript
const context1 = await browser.newContext();
const context2 = await browser.newContext();

const page1 = await context1.newPage();
const page2 = await context2.newPage();

// page1 and page2 have completely isolated cookies, storage, and session state
// Perfect for multi-user scenarios without launching multiple browsers

await page1.goto('https://app.com');
await page1.locator('#login').click();
await page1.locator('#email').fill('user1@test.com');

// Meanwhile, page2 runs independently
await page2.goto('https://app.com');
await page2.locator('#login').click();
await page2.locator('#email').fill('user2@test.com');
```

---

### Q3. Explain Playwright's auto-waiting mechanism. What conditions does it check before performing actions?
**Answer:**
Auto-waiting is Playwright's built-in synchronization that ensures elements are **actionable** before executing actions.

**Conditions Checked (in order):**
1. Element is attached to DOM
2. Element is visible (not display:none, visibility:hidden, opacity:0)
3. Element is stable (hasn't moved for last 10 actions/500ms)
4. Element is enabled (not disabled attribute for buttons/inputs)
5. Element is not covered by other elements (clickable without obstruction)

**Technical Details:**
```javascript
// Without explicit waits - Playwright auto-waits up to 30 seconds
await page.locator('#submit-button').click();
// Internally: checks visibility, stability, enables, then clicks

// Auto-waiting applies to all actions:
await page.locator('#email').fill('test@test.com'); // Waits for input to be visible and enabled
await page.locator('#dropdown').selectOption('option1'); // Waits for select to be ready
await page.locator('#checkbox').check(); // Waits for checkbox to be actionable

// Custom timeout for auto-wait
await page.locator('#slow-button').click({ timeout: 60000 }); // 60 second custom timeout

// Disable auto-wait (not recommended)
await page.locator('#element').click({ force: true }); // Bypasses auto-waiting
```

**Why This Matters:**
- Eliminates flaky tests caused by manual sleeps or brittle waits
- Dramatically reduces TimeoutExceptions
- Makes tests more reliable in CI/CD environments

---

### Q4. How does Playwright handle asynchronous JavaScript and AJAX calls differently from Selenium?
**Answer:**
Playwright uses `waitForLoadState()` and `waitForNavigation()` which intelligently monitor network activity, unlike Selenium which requires manual wait conditions.

**Playwright's Approach:**
```javascript
// Wait for network to be idle (AJAX completed)
await page.goto('https://example.com');
await page.waitForLoadState('networkidle');
// All AJAX calls on page load are complete

// Wait for specific network request
const response = await page.waitForResponse(
  resp => resp.url().includes('/api/data') && resp.status() === 200
);
const data = await response.json();

// Wait for navigation without explicit URL
await Promise.all([
  page.waitForNavigation(),
  page.locator('#submit-button').click()
]);

// Combining waits for complex scenarios
await Promise.all([
  page.waitForLoadState('networkidle'),
  page.locator('#load-more-button').click()
]);

// Wait for DOM changes after AJAX
await page.locator('#results').waitFor({ state: 'visible' });
await expect(page.locator('#results div')).toHaveCount(10);
```

**Comparison with Selenium:**
- Selenium: Manual wait for element presence using ExpectedConditions
- Playwright: Automatic network monitoring + actionability checks

---

### Q5. Explain the concept of Playwright Test fixtures and how they improve test maintainability. Can you create a custom fixture?
**Answer:**
Fixtures are reusable test setup mechanisms that reduce code duplication and provide a clean test context.

**Built-in Fixtures:**
- `page`: Browser page object
- `context`: Browser context
- `browser`: Browser instance
- `browserName`: Name of the browser

**Custom Fixture Example:**
```javascript
// fixtures.js
const base = require('@playwright/test');

exports.test = base.test.extend({
  // Authenticate once, reuse across tests
  authenticatedPage: async ({ page }, use) => {
    // Setup: Login before each test
    await page.goto('https://app.com/login');
    await page.locator('#email').fill('user@test.com');
    await page.locator('#password').fill('secure-password');
    await page.locator('#login-btn').click();
    await page.waitForNavigation();
    
    // Make page available to test
    await use(page);
    
    // Teardown: Cleanup after test
    await page.close();
  },

  // Create test data in database, inject into test
  userData: async ({ }, use) => {
    // Setup: Create user data
    const userData = {
      id: '12345',
      email: 'test@example.com',
      name: 'Test User'
    };
    
    await use(userData);
    
    // Teardown: Delete test data
    // await deleteFromDatabase(userData.id);
  },

  // API context for testing APIs
  apiContext: async ({ playwright }, use) => {
    const context = await playwright.request.newContext({
      baseURL: 'https://api.example.com',
      extraHTTPHeaders: {
        'Authorization': 'Bearer token123'
      }
    });
    await use(context);
    await context.dispose();
  }
});

// test.spec.js - Using custom fixtures
const { test } = require('./fixtures');

test('user dashboard loads with authenticated session', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('https://app.com/dashboard');
  await expect(authenticatedPage.locator('h1')).toContainText('Welcome');
});

test('create user with pre-loaded data', async ({ authenticatedPage, userData }) => {
  await authenticatedPage.locator('[data-testid="new-user"]').click();
  await authenticatedPage.locator('#user-email').fill(userData.email);
  await expect(authenticatedPage.locator('#confirmation')).toBeVisible();
});

test('verify API and UI consistency', async ({ apiContext, authenticatedPage, userData }) => {
  // Fetch from API
  const apiResponse = await apiContext.get(`/users/${userData.id}`);
  const apiData = await apiResponse.json();
  
  // Verify UI shows same data
  await authenticatedPage.goto(`/user/${userData.id}`);
  await expect(authenticatedPage.locator('#user-name')).toContainText(apiData.name);
});
```

**Benefits:**
- Eliminates login code duplication
- Provides consistent test setup
- Easy to maintain - change fixture once, affects all tests
- Built-in scope management (page, context, session level)

---

## Locators & Element Selection (Q6-Q10)

### Q6. Explain different types of locators in Playwright and their reliability ranking. When should you use each?
**Answer:**
Playwright supports multiple locator strategies with varying reliability levels:

**Reliability Ranking (Best to Worst):**

```javascript
// 1. TEST ID (MOST RELIABLE) - Use test data attributes
await page.locator('[data-testid="submit-button"]').click();

// 2. ROLE-BASED (VERY RELIABLE) - Semantic HTML
await page.locator('button:has-text("Submit")').click();
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('test@test.com');

// 3. ACCESSIBLE NAME - For labeled inputs
await page.getByLabel('Email Address').fill('test@test.com');
await page.getByPlaceholder('Enter email').fill('test@test.com');

// 4. TEXT CONTENT (MODERATE) - Last resort for text matching
await page.getByText('Click me').click();
await page.locator('text=Exact Match').click();

// 5. CSS SELECTORS (FRAGILE) - May break on style changes
await page.locator('div.btn.primary').click();

// 6. XPATH (MOST FRAGILE) - Breaks with DOM restructuring
await page.locator('//div[@class="btn" and text()="Submit"]').click();
```

**When to Use Each:**

| Locator Type | When to Use | Pros | Cons |
|---|---|---|---|
| Test ID | Always (if available) | Stable, explicit intent | Requires dev coordination |
| Role-based | Semantic HTML, accessibility testing | Accessibility-driven, maintainable | Requires proper HTML |
| Accessible Name | Forms, labeled inputs | User-centric, accessible | Limited use cases |
| Text Content | Unique visible text | Easy to understand | Breaks on text changes |
| CSS Selectors | Dynamic attributes | Better than XPath | Fragile to style changes |
| XPath | Last resort only | Very flexible | Extremely brittle |

**Best Practice Example:**
```javascript
// BAD: Fragile locator
await page.locator('div:nth-child(3) > button:nth-child(2)').click();

// GOOD: Test ID strategy
// Developer adds: <button data-testid="submit-form">Submit</button>
await page.getByTestId('submit-form').click();

// GOOD: Role-based for accessible apps
await page.getByRole('button', { name: /submit form/i }).click();
```

---

### Q7. How do you handle Shadow DOM and Web Components in Playwright? Provide a working example.
**Answer:**
Playwright can pierce Shadow DOM using `>>>` in selectors or `locator.locator()` chaining.

**Technical Implementation:**
```javascript
// Method 1: Using >>> combinator to pierce shadow DOM
const shadowElement = await page.locator('custom-element >>> button').click();

// Method 2: Chaining locators to traverse shadow boundaries
const customElement = page.locator('custom-element');
const shadowButton = customElement.locator('button');
await shadowButton.click();

// Method 3: Complex shadow DOM structure
// Structure: #host > #shadow-root > .wrapper > button
const element = page.locator('#host').locator('>> .wrapper >> button');
await element.click();

// COMPLETE EXAMPLE: Google Search Input (uses Shadow DOM)
test('search in google with shadow dom', async ({ page }) => {
  await page.goto('https://www.google.com');
  
  // Traverse Shadow DOM to reach actual input
  const searchInput = page.locator('xpath=//textarea[@name="q"]');
  await searchInput.fill('Playwright testing');
  
  // Alternative: Using CSS with shadow piercing
  const input = page.locator('[jsname="W5phtc"] >> input');
  
  // Verify the input has correct value
  await expect(searchInput).toHaveValue('Playwright testing');
});

// WORKING EXAMPLE: Custom Web Component
const htmlString = `
  <custom-search>
    #shadow-root (open)
      <input class="search-field" type="text">
      <button class="search-btn">Search</button>
  </custom-search>
`;

test('interact with custom web component', async ({ page }) => {
  await page.setContent(htmlString);
  
  // Click button inside Shadow DOM
  await page.locator('custom-search >>> button.search-btn').click();
  
  // Fill input inside Shadow DOM
  await page.locator('custom-search >>> input.search-field').fill('test query');
  
  // Assert value in shadow input
  const input = page.locator('custom-search >>> input.search-field');
  await expect(input).toHaveValue('test query');
});

// ADVANCED: Debug Shadow DOM structure
test('debug shadow dom structure', async ({ page }) => {
  await page.goto('https://example.com');
  
  // Inspect shadow roots in console
  const shadowInfo = await page.evaluate(() => {
    function getShadowRoots(element, depth = 0) {
      const indent = '  '.repeat(depth);
      let info = `${indent}${element.tagName}\n`;
      
      if (element.shadowRoot) {
        info += `${indent}  [SHADOW ROOT]\n`;
        Array.from(element.shadowRoot.children).forEach(child => {
          info += getShadowRoots(child, depth + 2);
        });
      }
      
      Array.from(element.children).forEach(child => {
        info += getShadowRoots(child, depth + 1);
      });
      
      return info;
    }
    return getShadowRoots(document.documentElement);
  });
  
  console.log('Shadow DOM Structure:\n', shadowInfo);
});
```

**Key Points:**
- Use `>>>` operator to pierce Shadow DOM boundaries
- Playwright automatically handles Shadow DOM unlike Selenium
- For debugging, use DevTools in headed mode
- Avoid over-complicating selectors - use combination of role, test ID, and shadow piercing

---

### Q8. Write a resilient locator strategy for a modern SPA with dynamic IDs and changing selectors.
**Answer:**
```javascript
// BAD: Fragile selectors that break easily
await page.locator('#user-btn-12345').click(); // ID changes dynamically
await page.locator('.menu > .item:nth-child(3)').click(); // Brittle DOM structure

// GOOD: Resilient selector strategy using multiple approaches

class LoginPage {
  constructor(page) {
    this.page = page;
  }
  
  // Strategy 1: Use role-based locators (most resilient)
  async fillEmail(email) {
    await this.page.getByRole('textbox', { name: /email/i }).fill(email);
  }
  
  async fillPassword(password) {
    await this.page.getByRole('textbox', { name: /password/i }).fill(password);
  }
  
  async clickLoginButton() {
    // Multiple fallback strategies
    const button = this.page.getByRole('button', { name: /login|sign in/i });
    await button.click();
  }
  
  // Strategy 2: Combine visible text with data attributes
  async selectDropdownOption(optionText) {
    // First try data attribute (most stable)
    let option = this.page.locator(`[data-option="${optionText}"]`);
    
    // Fallback to visible text
    if (!option) {
      option = this.page.locator(`text=${optionText}`);
    }
    
    await option.click();
  }
  
  // Strategy 3: Use closest() and filter() for complex scenarios
  async clickActionInRow(username, actionType) {
    const row = this.page.locator('tr', { has: this.page.locator(`text=${username}`) });
    const actionButton = row.locator(`button:has-text("${actionType}")`);
    await actionButton.click();
  }
  
  // Strategy 4: Attribute-based with contains for partial matches
  async fillDynamicInput(fieldLabel, value) {
    // Selector: Find label containing text, then get associated input
    const input = this.page.locator(
      `label:has-text("${fieldLabel}") + input, 
       label:has-text("${fieldLabel}") ~ input`
    );
    await input.fill(value);
  }
  
  // Strategy 5: Wait for visible state before interacting
  async clickWithWait(selector) {
    await this.page.locator(selector).waitFor({ state: 'visible' });
    await this.page.locator(selector).click();
  }
  
  // Strategy 6: Combination of multiple selectors with priority
  async getInputByLabel(labelText) {
    return this.page.locator(
      // Priority 1: Label with for attribute
      `label[for]:has-text("${labelText}") ~ input,
       // Priority 2: Label wrapping input
       label:has-text("${labelText}") input,
       // Priority 3: Aria-label
       input[aria-label*="${labelText}"],
       // Priority 4: Placeholder
       input[placeholder*="${labelText}"]`
    ).first();
  }
}

// Usage in test
test('login with resilient selectors', async ({ page }) => {
  const loginPage = new LoginPage(page);
  
  await page.goto('https://example.com/login');
  
  // All these selectors adapt to UI changes
  await loginPage.fillEmail('user@test.com');
  await loginPage.fillPassword('password123');
  await loginPage.clickLoginButton();
  
  // Wait for navigation
  await page.waitForNavigation();
  await expect(page).toHaveURL('**/dashboard');
});

// BONUS: Selector validation helper
async function validateSelectorResilience(page, selectors) {
  for (const selector of selectors) {
    const locator = page.locator(selector);
    const count = await locator.count();
    console.log(`Selector: ${selector} - Found: ${count} elements`);
    
    if (count === 0) {
      console.warn(`⚠️ FRAGILE: Selector found no elements`);
    } else if (count > 1) {
      console.warn(`⚠️ UNSTABLE: Selector found ${count} elements, expected 1`);
    } else {
      console.log(`✅ RESILIENT: Selector unique and stable`);
    }
  }
}

// Test resilience
test('validate selector resilience', async ({ page }) => {
  await page.goto('https://example.com/login');
  
  const selectors = [
    '[data-testid="email-input"]',
    'input[aria-label*="email"]',
    'label:has-text("Email") + input'
  ];
  
  await validateSelectorResilience(page, selectors);
});
```

---

### Q9. How do you handle strict mode locators in Playwright? When and why does it occur?
**Answer:**
Strict mode error occurs when a locator matches multiple elements, and you try to perform an action that requires a single element.

**When Strict Mode Occurs:**
```javascript
// ERROR: This will throw "locator.click() failed because selector resolved to 2 elements"
await page.locator('button').click(); // Multiple buttons on page

// Strict mode settings in config
const config = {
  use: {
    strictSelectors: true // Default in Playwright
  }
};

// SOLUTIONS:

// 1. Make locator more specific (BEST)
await page.locator('button:has-text("Submit")').click();
await page.getByRole('button', { name: 'Submit' }).click();
await page.locator('[data-testid="submit-btn"]').click();

// 2. Add visible filter
await page.locator('button:visible').click();

// 3. Use filter() method
await page.locator('button').filter({ hasText: 'Submit' }).click();

// 4. Use nth() to select specific element
await page.locator('button').nth(0).click(); // First button

// 5. Disable strict mode (NOT RECOMMENDED)
const config = {
  use: {
    strictSelectors: false
  }
};

// REAL EXAMPLE: Handling multiple buttons on page
test('click specific button with strict mode', async ({ page }) => {
  await page.goto('https://example.com');
  
// ❌ Would fail with strict mode error
  // await page.locator('button').click();
  
  // ✅ SOLUTIONS:
  
  // Option 1: Use role and name
  await page.getByRole('button', { name: 'Delete Account' }).click();
  
  // Option 2: Filter by text
  const deleteBtn = page.locator('button').filter({ hasText: 'Delete Account' });
  await deleteBtn.click();
  
  // Option 3: Use closest() to select parent context
  const userCard = page.locator('.user-card:has-text("John Doe")');
  const deleteBtn2 = userCard.locator('button:has-text("Delete")');
  await deleteBtn2.click();
  
  // Option 4: Combination of selectors
  await page.locator('.modal.open >> button[type="submit"]').click();
});
```

---

### Q10. Explain the difference between using locator references vs element handles. When would you use each?
**Answer:**
```javascript
// LOCATORS (Preferred - Query the DOM fresh every time)
const button = page.locator('#submit-btn');
await button.click();
await button.click(); // Works - re-queries DOM each time

// ELEMENT HANDLES (Legacy - Stores reference to specific element)
const elementHandle = await page.locator('#submit-btn').elementHandle();
await elementHandle.click(); // Reference-based

// KEY DIFFERENCES:

const testComparison = async ({ page }) => {
  // LOCATORS: Always fresh query
  const locatorBtn = page.locator('#my-button');
  
  // Locators stay valid even after DOM changes
  await page.evaluate(() => {
    document.getElementById('my-button').remove();
    const newBtn = document.createElement('button');
    newBtn.id = 'my-button';
    newBtn.textContent = 'Click me';
    document.body.appendChild(newBtn);
  });
  
  // Still works because locator re-queries
  await locatorBtn.click();
  
  // ELEMENT HANDLES: Reference becomes stale
  const handleBtn = await page.locator('#stale-button').elementHandle();
  
  // Remove and recreate element
  await page.evaluate(() => {
    document.getElementById('stale-button').remove();
    const newBtn = document.createElement('button');
    newBtn.id = 'stale-button';
    document.body.appendChild(newBtn);
  });
  
  // ❌ Would throw StaleElementException
  // await handleBtn.click();
};

// PRACTICAL COMPARISON:

// SCENARIO 1: Simple interaction (Use Locators)
test('locator for simple click', async ({ page }) => {
  const button = page.locator('[data-testid="submit"]');
  await button.click(); // Fresh query, reliable
});

// SCENARIO 2: Multiple operations on same element (Use Locators)
test('multiple operations with locator', async ({ page }) => {
  const input = page.locator('#email');
  
  // Multiple operations - locator re-queries each time
  await input.fill('test@test.com');
  await input.selectText();
  await input.evaluate(el => el.value.toUpperCase());
  await expect(input).toHaveValue('TEST@TEST.COM');
});

// SCENARIO 3: When you need raw element (Use ElementHandle)
test('element handle for direct DOM access', async ({ page }) => {
  // Get element handle for advanced DOM manipulation
  const button = await page.locator('[data-testid="submit"]').elementHandle();
  
  // Direct JavaScript execution on element
  await button.evaluate(el => {
    el.style.backgroundColor = 'red';
    el.dataset.status = 'modified';
  });
  
  // Get computed properties
  const style = await button.evaluate(el => window.getComputedStyle(el).color);
  console.log('Button color:', style);
});

// BEST PRACTICE PATTERN:
class PageObject {
  constructor(page) {
    this.page = page;
  }
  
  // Always use locators for element references
  async getSubmitButton() {
    return this.page.locator('[data-testid="submit"]');
  }
  
  // Use element handles only for advanced DOM manipulation
  async getButtonElement() {
    return this.page.locator('[data-testid="submit"]').elementHandle();
  }
  
  async submitForm(data) {
    // Use locators for interactions
    await this.page.locator('#email').fill(data.email);
    await this.page.locator('#password').fill(data.password);
    
    // Use element handle for complex DOM operations
    const form = await this.page.locator('form').elementHandle();
    const formData = await form.evaluate(el => {
      return new FormData(el);
    });
    
    // Submit using locator
    await (await this.getSubmitButton()).click();
  }
}

// WHEN TO USE:
// ✅ Locators: 90% of cases - interactions, assertions, waits
// ✅ Element Handles: 10% of cases - advanced DOM inspection, complex JS execution
// ✅ Never mix both in same test
// ✅ Prefer locators for maintainability
```

---

## Advanced Waits & Synchronization (Q11-Q15)

### Q11. Compare implicit waits, explicit waits, and fluent waits in Playwright. What's the recommended approach?
**Answer:**
Playwright eliminates the need for these traditional waits through auto-waiting, but understanding them helps when switching from Selenium.

```javascript
// IMPLICIT WAIT (Not directly in Playwright)
// Automatically applied to all operations
// Problem: Unpredictable wait times, hard to debug
// Playwright Solution: Use actionability checks (built-in auto-wait)

// EXPLICIT WAIT (Playwright equivalent)
// Wait for specific condition to be true
const waitForElementVisible = async (page, selector) => {
  await page.locator(selector).waitFor({ state: 'visible', timeout: 5000 });
};

// FLUENT WAIT (Polling at intervals)
// Check condition at regular intervals
const fluentWaitExample = async (page) => {
  let isReady = false;
  const maxWaitTime = 5000;
  const pollInterval = 100;
  const startTime = Date.now();
  
  while (!isReady && Date.now() - startTime < maxWaitTime) {
    try {
      isReady = await page.locator('#element').isVisible();
    } catch {
      // Ignore errors during polling
    }
    
    if (!isReady) {
      await page.waitForTimeout(pollInterval);
    }
  }
  
  if (!isReady) throw new Error('Element did not become ready in time');
};

// PLAYWRIGHT RECOMMENDED: Auto-waiting (built-in)
test('playwright auto-waiting - best approach', async ({ page }) => {
  // No manual waits needed - Playwright handles it
  
  // 1. Action auto-wait (waits for element actionability)
  await page.locator('#button').click(); // Waits up to 30 seconds by default
  
  // 2. Assertion auto-wait (retries assertion)
  await expect(page.locator('#message')).toBeVisible(); // Retries until visible or timeout
  
  // 3. Network wait
  await page.waitForLoadState('networkidle'); // All network activity complete
  
  // 4. Navigation wait
  await page.waitForNavigation();
  
  // 5. Specific element wait
  await page.locator('#async-content').waitFor({ state: 'visible' });
});

// ADVANCED: Custom waits for complex scenarios
class AdvancedWaits {
  constructor(page) {
    this.page = page;
  }
  
  // Wait for multiple conditions (AND)
  async waitForAllConditions(conditions, timeout = 5000) {
    const startTime = Date.now();
    let allMet = false;
    
    while (!allMet && Date.now() - startTime < timeout) {
      allMet = await Promise.all(
        conditions.map(condition => condition.catch(() => false))
      ).then(results => results.every(r => r === true));
      
      if (!allMet) {
        await this.page.waitForTimeout(100);
      }
    }
    
    if (!allMet) throw new Error('Timeout waiting for conditions');
  }
  
  // Wait for any condition (OR)
  async waitForAnyCondition(conditions, timeout = 5000) {
    return Promise.race([
      Promise.all(conditions),
      this.page.waitForTimeout(timeout).then(() => {
        throw new Error('Timeout waiting for any condition');
      })
    ]);
  }
  
  // Wait for element count to match
  async waitForElementCount(selector, expectedCount, timeout = 5000) {
    const startTime = Date.now();
    let actualCount = 0;
    
    while (Date.now() - startTime < timeout) {
      actualCount = await this.page.locator(selector).count();
      if (actualCount === expectedCount) return;
      await this.page.waitForTimeout(100);
    }
    
    throw new Error(`Expected ${expectedCount} elements, found ${actualCount}`);
  }
  
  // Wait for text to appear and be stable
  async waitForStableText(selector, expectedText, timeout = 5000) {
    const locator = this.page.locator(selector);
    const startTime = Date.now();
    
    // First wait for element to be visible
    await locator.waitFor({ state: 'visible', timeout });
    
    // Then wait for text content to stabilize
    let previousText = '';
    let stableCount = 0;
    
    while (Date.now() - startTime < timeout) {
      const currentText = await locator.textContent();
      
      if (currentText === expectedText && currentText === previousText) {
        stableCount++;
        if (stableCount >= 2) return; // Text stable for 2 checks
      } else {
        stableCount = 0;
      }
      
      previousText = currentText;
      await this.page.waitForTimeout(50);
    }
    
    throw new Error(`Text did not stabilize to "${expectedText}"`);
  }
}

// Usage
test('advanced wait scenarios', async ({ page }) => {
  const waits = new AdvancedWaits(page);
  
  // Wait for multiple conditions
  await waits.waitForAllConditions([
    page.locator('#header').isVisible(),
    page.locator('#content').isVisible(),
    page.locator('#footer').isVisible()
  ]);
  
  // Wait for specific element count (e.g., loaded items)
  await waits.waitForElementCount('.product-item', 10, 5000);
  
  // Wait for text to be stable
  await waits.waitForStableText('#loading-message', 'Ready', 5000);
});

// TIMEOUT CONFIGURATION
test('custom timeout configuration', async ({ page }) => {
  // Set default timeout for all operations
  page.setDefaultTimeout(15000); // 15 seconds for all actions
  page.setDefaultNavigationTimeout(30000); // 30 seconds for navigation
  
  // Override for specific action
  await page.locator('#element').click({ timeout: 60000 }); // 60 seconds for this click
  
  // Override for assertions
  await expect(page.locator('#element')).toBeVisible({
    timeout: 10000 // 10 seconds for this assertion
  });
});

// RECOMMENDED WAIT STRATEGY FOR DIFFERENT SCENARIOS:
/*
1. Page Load: await page.waitForLoadState('networkidle')
2. Single Element: await page.locator('#element').waitFor()
3. Navigation: await page.waitForNavigation()
4. AJAX/API Response: await page.waitForResponse(url => url.includes('/api'))
5. Multiple Elements: await expect(page.locator('.item')).toHaveCount(10)
6. Text Appearance: await expect(page.locator('#msg')).toContainText('Success')
7. Custom Logic: Create custom utility functions
*/
```

---

### Q12. How do you wait for network requests and responses? Explain different approaches and their trade-offs.
**Answer:**
```javascript
test('comprehensive network waiting strategies', async ({ page }) => {
  // STRATEGY 1: Wait for specific response
  const responsePromise = page.waitForResponse(
    resp => resp.url().includes('/api/users') && resp.status() === 200
  );
  
  await page.locator('#load-users-btn').click();
  const response = await responsePromise;
  const data = await response.json();
  console.log('Users data:', data);
  
  // STRATEGY 2: Wait for all network requests to complete
  await page.goto('https://example.com');
  await page.waitForLoadState('networkidle');
  // All background network activity completed
  
  // STRATEGY 3: Wait for multiple responses (Promise.all)
  const [response1, response2] = await Promise.all([
    page.waitForResponse(resp => resp.url().includes('/users')),
    page.waitForResponse(resp => resp.url().includes('/profile'))
  ]);
  
  // STRATEGY 4: Combine navigation and network wait
  const [, response] = await Promise.all([
    page.waitForNavigation(),
    page.waitForResponse(resp => resp.status() === 200),
    page.locator('#submit-btn').click()
  ]);
  
  // STRATEGY 5: Wait for failed responses (error handling)
  await page.waitForResponse(
    resp => resp.url().includes('/api') && resp.status() >= 400
  );
  // Now you know API call failed
  
  // STRATEGY 6: Timeout with custom error message
  try {
    const response = await page.waitForResponse(
      resp => resp.url().includes('/api/data'),
      { timeout: 5000 }
    );
  } catch (error) {
    throw new Error('API call did not complete within 5 seconds');
  }
  
  // STRATEGY 7: Abort request if takes too long
  const abortController = new AbortController();
  const timeoutId = setTimeout(() => abortController.abort(), 5000);
  
  try {
    const response = await page.waitForResponse(resp => {
      if (abortController.signal.aborted) {
        throw new Error('Request timeout');
      }
      return resp.url().includes('/api');
    });
  } finally {
    clearTimeout(timeoutId);
  }
});

// ADVANCED NETWORK HANDLING CLASS
class NetworkHelper {
  constructor(page) {
    this.page = page;
    this.requestLog = [];
    this.responseLog = [];
    this.setupNetworkListeners();
  }
  
  setupNetworkListeners() {
    // Log all requests
    this.page.on('request', request => {
      this.requestLog.push({
        url: request.url(),
        method: request.method(),
        timestamp: Date.now()
      });
    });
    
    // Log all responses
    this.page.on('response', response => {
      this.responseLog.push({
        url: response.url(),
        status: response.status(),
        timestamp: Date.now()
      });
    });
  }
  
  // Wait for specific API call with validation
  async waitForApiCall(apiPattern, timeout = 5000) {
    const startTime = Date.now();
    
    return new Promise((resolve, reject) => {
      const onResponse = async (response) => {
        if (response.url().includes(apiPattern)) {
          this.page.off('response', onResponse);
          
          try {
            const data = await response.json();
            resolve({ response, data, duration: Date.now() - startTime });
          } catch (error) {
            reject(new Error(`Failed to parse response: ${error.message}`));
          }
        }
        
        if (Date.now() - startTime > timeout) {
          this.page.off('response', onResponse);
          reject(new Error(`API call to ${apiPattern} did not complete within ${timeout}ms`));
        }
      };
      
      this.page.on('response', onResponse);
    });
  }
  
  // Wait for multiple API calls
  async waitForMultipleApiCalls(patterns, timeout = 5000) {
    const results = {};
    const startTime = Date.now();
    const completed = new Set();
    
    return Promise.race([
      Promise.all(patterns.map(pattern => {
        return new Promise((resolve) => {
          const onResponse = async (response) => {
            if (response.url().includes(pattern) && !completed.has(pattern)) {
              completed.add(pattern);
              this.page.off('response', onResponse);
              
              const data = await response.json();
              results[pattern] = data;
              resolve(data);
            }
          };
          
          this.page.on('response', onResponse);
        });
      })),
      this.page.waitForTimeout(timeout).then(() => {
        throw new Error(`Timeout waiting for API calls: ${patterns.join(', ')}`);
      })
    ]);
  }
  
  // Get request/response metrics
  getMetrics() {
    return {
      totalRequests: this.requestLog.length,
      totalResponses: this.responseLog.length,
      avgResponseTime: this.calculateAvgResponseTime(),
      slowRequests: this.responseLog.filter(r => r.timestamp - this.getRequestTime(r) > 1000)
    };
  }
  
  clearLogs() {
    this.requestLog = [];
    this.responseLog = [];
  }
  
  private calculateAvgResponseTime() {
    if (this.responseLog.length === 0) return 0;
    
    const totalTime = this.responseLog.reduce((sum, resp) => {
      const reqTime = this.getRequestTime(resp);
      return sum + (resp.timestamp - reqTime);
    }, 0);
    
    return totalTime / this.responseLog.length;
  }
  
  private getRequestTime(response) {
    const request = this.requestLog.find(r => r.url === response.url);
    return request?.timestamp || response.timestamp - 1000;
  }
}

// Usage in tests
test('network helper usage', async ({ page }) => {
  const network = new NetworkHelper(page);
  
  await page.goto('https://example.com');
  
  // Wait for specific API with validation
  const { data, duration } = await network.waitForApiCall('/api/users', 10000);
  console.log(`User API completed in ${duration}ms:`, data);
  
  // Get performance metrics
  const metrics = network.getMetrics();
  console.log('Network metrics:', metrics);
  
  // Assert on performance
  expect(duration).toBeLessThan(3000); // Should complete in < 3 seconds
});

// TRADE-OFFS:
/*
waitForLoadState('networkidle'): 
  ✅ Simple, covers all network activity
  ❌ Can be slow, waits for all background requests

waitForResponse():
  ✅ Specific, fast, reliable
  ❌ Need to know exact URL/response pattern

waitForNavigation():
  ✅ Explicit page change detection
  ❌ Doesn't wait for resources, only navigation

Custom listeners:
  ✅ Complete control, detailed logging
  ❌ Complex to implement, maintenance overhead
*/
```

---

### Q13. Explain how to handle race conditions and timing issues in parallel test execution.
**Answer:**
```javascript
// COMMON RACE CONDITION SCENARIOS

// SCENARIO 1: Shared test data accessed by parallel tests
// ❌ PROBLEMATIC
const testData = { userId: '123' }; // Shared across tests

test('test 1', async ({ page }) => {
  testData.userId = '456'; // Modifies shared data
  await page.goto(`/user/${testData.userId}`);
});

test('test 2', async ({ page }) => {
  // testData.userId might be '456' instead of '123'
  await page.goto(`/user/${testData.userId}`);
});

// ✅ SOLUTION: Isolated test data
test('test 1', async ({ page }) => {
  const userId = '123'; // Local variable
  await page.goto(`/user/${userId}`);
});

test('test 2', async ({ page }) => {
  const userId = '456'; // Different local variable
  await page.goto(`/user/${userId}`);
});

// SCENARIO 2: Port conflicts in parallel tests
// ❌ PROBLEMATIC: All tests try to use port 3000
test.parallel('test 1', async ({ page }) => {
  const server = await startServer(3000); // Might fail if test 2 uses same port
});

// ✅ SOLUTION: Dynamic port allocation
class TestServerManager {
  static async getAvailablePort() {
    const server = require('http').createServer();
    return new Promise((resolve) => {
      server.listen(0, () => {
        const port = server.address().port;
        server.close(() => resolve(port));
      });
    });
  }
}

test.parallel('test 1', async ({ page }) => {
  const port = await TestServerManager.getAvailablePort();
  const server = await startServer(port);
});

// SCENARIO 3: Database state conflicts
// ❌ PROBLEMATIC: Tests interfere with each other's data
const DB = require('database');

test('test 1', async ({ page }) => {
  const user = await DB.createUser({ name: 'User1' });
  // Test 2 might delete this user while test 1 is still running
});

test('test 2', async ({ page }) => {
  const users = await DB.getAllUsers();
  // Might see User1 created by test 1
});

// ✅ SOLUTION: Test isolation with transactions
class TestDatabase {
  constructor() {
    this.transactionId = Date.now() + Math.random();
  }
  
  async createUser(data) {
    return DB.createUser({
      ...data,
      testId: this.transactionId // Tag with test ID
    });
  }
  
  async cleanup() {
    // Delete only data created by this test
    return DB.deleteWhere({ testId: this.transactionId });
  }
}

test('test with isolated database', async ({ page }) => {
  const testDb = new TestDatabase();
  
  try {
    const user = await testDb.createUser({ name: 'User1' });
    // Test logic
  } finally {
    await testDb.cleanup(); // Only removes this test's data
  }
});

// SCENARIO 4: Resource contention (API rate limits, file locks)
// ❌ PROBLEMATIC: Too many parallel requests
test.parallel('api test', async ({ page }) => {
  // Might hit rate limits if 100 tests run in parallel
  await page.request.get('/api/data');
});

// ✅ SOLUTION: Concurrent request limiting
class RateLimitedRequestManager {
  constructor(maxConcurrent = 5) {
    this.maxConcurrent = maxConcurrent;
    this.activeRequests = 0;
    this.queue = [];
  }
  
  async execute(requestFn) {
    while (this.activeRequests >= this.maxConcurrent) {
      await new Promise(resolve => {
        this.queue.push(resolve);
      });
    }
    
    this.activeRequests++;
    
    try {
      return await requestFn();
    } finally {
      this.activeRequests--;
      const resolve = this.queue.shift();
      if (resolve) resolve();
    }
  }
}

const requestManager = new RateLimitedRequestManager(5);

test.parallel('api test with rate limiting', async ({ page }) => {
  await requestManager.execute(async () => {
    return await page.request.get('/api/data');
  });
});

// SCENARIO 5: Element selector conflicts in parallel snapshots
// ❌ PROBLEMATIC: Same selector ID exists in multiple tests
test.parallel('snapshot test 1', async ({ page }) => {
  await page.setContent('<div id="content">Test 1</div>');
  await expect(page).toHaveScreenshot();
});

test.parallel('snapshot test 2', async ({ page }) => {
  await page.setContent('<div id="content">Test 2</div>');
  await expect(page).toHaveScreenshot();
});

// ✅ SOLUTION: Use unique identifiers
test.parallel('snapshot test with unique ids', async ({ page }, testInfo) => {
  const testId = testInfo.title.replace(/\s+/g, '_');
  await page.setContent(`<div id="content-${testId}">Test Content</div>`);
  await expect(page).toHaveScreenshot(`screenshot-${testId}`);
});

// BEST PRACTICE: Complete test isolation pattern
class IsolatedTest {
  constructor(testInfo) {
    this.testInfo = testInfo;
    this.testId = testInfo.testId;
    this.resources = [];
  }
  
  async createTestData(dataFactory) {
    const data = await dataFactory();
    // Tag all data with test ID for cleanup
    data._testId = this.testId;
    this.resources.push(data);
    return data;
  }
  
  async cleanup() {
    // Cleanup all resources created by this test
    for (const resource of this.resources) {
      if (resource.delete) {
        await resource.delete();
      }
    }
  }
  
  async run(testFn) {
    try {
      await testFn(this);
    } finally {
      await this.cleanup();
    }
  }
}

test('isolated parallel test', async ({ page }, testInfo) => {
  const isolated = new IsolatedTest(testInfo);
  
  await isolated.run(async (context) => {
    const user = await context.createTestData(async () => {
      return DB.createUser({ name: `User_${context.testId}` });
    });
    
    // Test logic using user
    await page.goto(`/user/${user.id}`);
  });
  // Cleanup happens automatically
});

// CONFIGURATION FOR PARALLEL EXECUTION
const config = {
  testDir: './tests',
  fullyParallel: true, // Run all tests in parallel
  workers: 4, // 4 workers (adjust based on resources)
  
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    // Each test gets isolated browser context
    contextOptions: {
      ignoreHTTPSErrors: true
    }
  }
};

module.exports = config;

// DEBUGGING PARALLEL TEST ISSUES
/*
1. Set workers to 1 to isolate failures
2. Use unique IDs for all resources (timestamps, UUIDs)
3. Add detailed logging with test ID
4. Use test.describe.serial() for dependent tests
5. Profile with --reporter=html to see timing
6. Monitor resource usage during parallel runs
*/
```

---

### Q14. How do you mock and stub network requests and responses? Provide a complete example.
**Answer:**
```javascript
// NETWORK MOCKING STRATEGIES

// STRATEGY 1: Route-based mocking (most flexible)
test('mock api responses', async ({ page }) => {
  // Intercept and modify responses
  await page.route('**/api/users', route => {
    route.abort(); // Block the request
  });
  
  await page.goto('https://example.com');
  // API call will fail/timeout
});

// STRATEGY 2: Provide mock response
test('stub api with mock data', async ({ page }) => {
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'User 1' },
        { id: 2, name: 'User 2' }
      ])
    });
  });
  
  await page.goto('https://example.com');
  
  // Verify mock was used
  await expect(page.locator('text=User 1')).toBeVisible();
});

// STRATEGY 3: Conditional mocking
test('mock specific requests conditionally', async ({ page }) => {
  await page.route('**/api/**', async route => {
    const request = route.request();
    
    if (request.url().includes('/api/users')) {
      route.fulfill({
        status: 200,
        body: JSON.stringify([{ id: 1, name: 'Mock User' }])
      });
    } else if (request.url().includes('/api/posts')) {
      // Simulate slow response
      await page.waitForTimeout(2000);
      route.continue();
    } else {
      // Let other requests go through
      route.continue();
    }
  });
  
  await page.goto('https://example.com');
});

// ADVANCED MOCKING CLASS
class NetworkMocker {
  constructor(page) {
    this.page = page;
    this.mocks = [];
    this.requestLog = [];
  }
  
  // Mock single endpoint
  async mockEndpoint(urlPattern, response) {
    await this.page.route(urlPattern, route => {
      this.requestLog.push({
        url: route.request().url(),
        timestamp: Date.now(),
        wasMocked: true
      });
      
      route.fulfill({
        status: response.status || 200,
        contentType: response.contentType || 'application/json',
        body: typeof response.body === 'string' 
          ? response.body 
          : JSON.stringify(response.body)
      });
    });
    
    this.mocks.push(urlPattern);
  }
  
  // Mock with dynamic responses based on request
  async mockDynamic(urlPattern, responseFactory) {
    await this.page.route(urlPattern, async route => {
      const request = route.request();
      const response = await responseFactory(request);
      
      route.fulfill(response);
    });
  }
  
  // Mock authentication endpoints
  async mockAuth(credentials = {}) {
    const { email = 'user@test.com', token = 'mock-token-123' } = credentials;
    
    // Mock login endpoint
    await this.page.route('**/api/auth/login', route => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({
          token,
          user: { email, id: 1 }
        })
      });
    });
    
    // Mock refresh token
    await this.page.route('**/api/auth/refresh', route => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({ token })
      });
    });
  }
  
  // Mock with response delay
  async mockWithDelay(urlPattern, response, delayMs = 1000) {
    await this.page.route(urlPattern, async route => {
      await this.page.waitForTimeout(delayMs);
      route.fulfill(response);
    });
  }
  
  // Mock error responses
  async mockError(urlPattern, errorCode = 500) {
    await this.page.route(urlPattern, route => {
      route.fulfill({
        status: errorCode,
        body: JSON.stringify({
          error: `Mock error: ${errorCode}`,
          message: this.getErrorMessage(errorCode)
        })
      });
    });
  }
  
  // Mock sequential responses (different response each call)
  async mockSequential(urlPattern, responses) {
    let callCount = 0;
    
    await this.page.route(urlPattern, route => {
      const response = responses[callCount] || responses[responses.length - 1];
      callCount++;
      
      route.fulfill(response);
    });
  }
  
  // Get request log
  getRequestLog() {
    return this.requestLog;
  }
  
  // Verify endpoint was called
  wasEndpointCalled(urlPattern) {
    return this.requestLog.some(log => 
      log.url.includes(urlPattern)
    );
  }
  
  // Clear all mocks
  async clearMocks() {
    for (const mock of this.mocks) {
      await this.page.unroute(mock);
    }
    this.mocks = [];
    this.requestLog = [];
  }
  
  private getErrorMessage(code) {
    const messages = {
      400: 'Bad Request',
      401: 'Unauthorized',
      403: 'Forbidden',
      404: 'Not Found',
      500: 'Internal Server Error',
      503: 'Service Unavailable'
    };
    return messages[code] || 'Unknown Error';
  }
}

// COMPLETE EXAMPLE: E-commerce checkout flow
test('e-commerce checkout with full network mocking', async ({ page }) => {
  const mocker = new NetworkMocker(page);
  
  try {
    // Mock all required endpoints
    await mocker.mockEndpoint('**/api/products', {
      status: 200,
      body: [
        { id: 1, name: 'Product 1', price: 29.99 },
        { id: 2, name: 'Product 2', price: 49.99 }
      ]
    });
    
    await mocker.mockAuth({
      email: 'customer@test.com',
      token: 'mock-auth-token'
    });
    
    await mocker.mockEndpoint('**/api/cart', {
      status: 200,
      body: { items: [], total: 0 }
    });
    
    // Mock payment processing with delay
    await mocker.mockWithDelay('**/api/payment/process', {
      status: 200,
      body: {
        success: true,
        orderId: 'ORD-123456',
        message: 'Payment successful'
      }
    }, 2000);
    
    // Mock order confirmation
    await mocker.mockEndpoint('**/api/orders', {
      status: 201,
      body: { orderId: 'ORD-123456', status: 'confirmed' }
    });
    
    // Perform checkout flow
    await page.goto('https://shop.example.com');
    
    // Verify products loaded
    await expect(page.locator('text=Product 1')).toBeVisible();
    
    // Add to cart
    await page.locator('[data-testid="add-product-1"]').click();
    await expect(page.locator('[data-testid="cart-count"]')).toContainText('1');
    
    // Go to checkout
    await page.locator('[data-testid="checkout-btn"]').click();
    
    // Verify login called
    await expect(page).toHaveURL('**/checkout');
    expect(mocker.wasEndpointCalled('/api/products')).toBe(true);
    
    // Fill payment details
    await page.locator('[data-testid="card-number"]').fill('4242 4242 4242 4242');
    
    // Process payment
    await page.locator('[data-testid="pay-btn"]').click();
    
    // Verify order confirmation
    await expect(page.locator('text=ORD-123456')).toBeVisible();
    
    // Verify mock calls
    console.log('Request log:', mocker.getRequestLog());
    
  } finally {
    await mocker.clearMocks();
  }
});

// PRACTICAL: Mock specific error scenarios
test('handle payment failure gracefully', async ({ page }) => {
  const mocker = new NetworkMocker(page);
  
  // Mock payment failure
  await mocker.mockError('**/api/payment/process', 402); // Payment required
  
  await page.goto('https://shop.example.com/checkout');
  await page.locator('[data-testid="pay-btn"]').click();
  
  // Verify error message displayed
  await expect(page.locator('[data-testid="error-message"]')).toContainText(
    'Payment failed'
  );
});

// CONFIGURATION: Disable specific third-party requests
test('block tracking and ads', async ({ page }) => {
  // Block requests to tracking/ad domains
  await page.route('**/analytics/**', route => route.abort());
  await page.route('**/ads/**', route => route.abort());
  await page.route('**/*google-analytics*', route => route.abort());
  
  await page.goto('https://example.com');
  // Page loads without tracking/ads
});

// BEST PRACTICES:
/*
1. Use wildcard patterns for flexibility
2. Log all intercepted requests for debugging
3. Mock auth endpoints to avoid dependency on auth service
4. Use sequential mocks for complex workflows
5. Always clear mocks in cleanup
6. Combine mocking with assertions to verify interactions
7. Mock external APIs to make tests faster and more reliable
8. Use different mock responses for different test scenarios
*/
```

---

### Q15. How do you test real-time features (WebSockets, Server-Sent Events) in Playwright?
**Answer:**
```javascript
// WEBSOCKET TESTING

test('websocket real-time updates', async ({ page }) => {
  const messages = [];
  
  // Intercept WebSocket frames
  page.on('websocket', ws => {
    console.log(`WebSocket opened: ${ws.url()}`);
    
    ws.on('frameSent', event => {
      console.log('Sent:', event.payload);
      messages.push({ type: 'sent', payload: event.payload });
    });
    
    ws.on('frameReceived', event => {
      console.log('Received:', event.payload);
      messages.push({ type: 'received', payload: event.payload });
    });
  });
  
  await page.goto('https://example.com/chat');
  
  // Trigger WebSocket message
  await page.locator('[data-testid="message-input"]').fill('Hello');
  await page.locator('[data-testid="send-btn"]').click();
  
  // Wait for server response
  await page.waitForFunction(() => {
    return messages.some(m => m.type === 'received');
  });
  
  // Verify message was sent and received
  const sent = messages.find(m => m.type === 'sent');
  const received = messages.find(m => m.type === 'received');
  
  expect(sent.payload).toContain('Hello');
  expect(received.payload).toBeTruthy();
  
  console.log('Message flow:', messages);
});

// ADVANCED: Mock WebSocket server
class WebSocketMock {
  constructor(page) {
    this.page = page;
    this.ws = null;
    this.connected = false;
    this.messageQueue = [];
  }
  
  // Start mock WebSocket server
  async startMockServer() {
    const WebSocket = require('ws');
    this.wss = new WebSocket.Server({ port: 8080 });
    
    this.wss.on('connection', (ws) => {
      this.ws = ws;
      this.connected = true;
      
      ws.on('message', (data) => {
        // Store received messages
        this.messageQueue.push(JSON.parse(data));
        
        // Send echo response
        ws.send(JSON.stringify({
          type: 'ack',
          originalMessage: data,
          timestamp: Date.now()
        }));
      });
      
      ws.on('close', () => {
        this.connected = false;
      });
    });
  }
  
  // Simulate server sending message
  async sendFromServer(message) {
    if (this.ws && this.connected) {
      this.ws.send(JSON.stringify(message));
    }
  }
  
  // Get received messages
  getReceivedMessages() {
    return this.messageQueue;
  }
  
  // Close mock server
  async close() {
    if (this.wss) {
      this.wss.close();
    }
    this.messageQueue = [];
  }
}

// SERVER-SENT EVENTS (SSE) TESTING

test('server-sent events', async ({ page }) => {
  const events = [];
  
  // Intercept EventSource requests
  await page.route('**/api/events', async route => {
    const response = await route.fetch();
    // EventSource keeps connection open and streams data
    events.push({ type: 'sse-connected' });
  });
  
  // Listen for SSE events in page
  await page.evaluateHandle(() => {
    window.sseEvents = [];
    const eventSource = new EventSource('/api/events');
    
    eventSource.onopen = () => {
      window.sseEvents.push({ type: 'connected' });
    };
    
    eventSource.onmessage = (event) => {
      window.sseEvents.push(JSON.parse(event.data));
    };
    
    eventSource.onerror = () => {
      window.sseEvents.push({ type: 'error' });
      eventSource.close();
    };
  });
  
  await page.goto('https://example.com/notifications');
  
  // Wait for SSE events
  await page.waitForFunction(() => {
    return page.evaluate(() => window.sseEvents.length > 0);
  });
  
  // Get received events
  const receivedEvents = await page.evaluate(() => window.sseEvents);
  console.log('SSE Events:', receivedEvents);
  
  expect(receivedEvents[0].type).toBe('connected');
});

// REAL-TIME UPDATES WITH MOCKING

test('real-time data updates with mock server', async ({ page }) => {
  const mockWss = new WebSocketMock(page);
  await mockWss.startMockServer();
  
  try {
    // Setup page to connect to mock WebSocket
    await page.goto('https://example.com/dashboard');
    
    // Simulate initial data
    await mockWss.sendFromServer({
      type: 'initial-data',
      data: { users: 100, online: 50 }
    });
    
    // Verify initial data displayed
    await expect(page.locator('[data-testid="online-count"]')).toContainText('50');
    
    // Simulate real-time update
    await mockWss.sendFromServer({
      type: 'user-joined',
      data: { userId: 'user-123', onlineCount: 51 }
    });
    
    // Verify UI updated
    await expect(page.locator('[data-testid="online-count"]')).toContainText('51');
    
    // Verify multiple updates
    for (let i = 0; i < 5; i++) {
      await mockWss.sendFromServer({
        type: 'update',
        data: { value: i }
      });
    }
    
    // Verify all updates received
    const messages = mockWss.getReceivedMessages();
    expect(messages.length).toBeGreaterThan(0);
    
  } finally {
    await mockWss.close();
  }
});

// TESTING WEBSOCKET DISCONNECTION AND RECONNECTION

test('websocket reconnection handling', async ({ page }) => {
  let disconnectCount = 0;
  let reconnectCount = 0;
  
  page.on('websocket', ws => {
    ws.on('close', () => {
      disconnectCount++;
      console.log('WebSocket disconnected');
    });
  });
  
  // Inject reconnection logic on page
  await page.evaluate(() => {
    window.wsReconnectAttempts = 0;
    
    function connectWebSocket() {
      const ws = new WebSocket('ws://example.com/live');
      
      ws.onclose = () => {
        window.wsReconnectAttempts++;
        
        // Attempt reconnection with exponential backoff
        if (window.wsReconnectAttempts < 3) {
          setTimeout(connectWebSocket, Math.pow(2, window.wsReconnectAttempts) * 1000);
        }
      };
    }
    
    connectWebSocket();
  });
  
  await page.goto('https://example.com');
  
  // Simulate connection loss
  await page.evaluate(() => {
    // This would require actual WebSocket interception
    // In real scenario, you'd use network conditions
  });
  
  // Wait for reconnection attempts
  await page.waitForFunction(() => {
    return page.evaluate(() => window.wsReconnectAttempts > 0);
  });
  
  const attempts = await page.evaluate(() => window.wsReconnectAttempts);
  expect(attempts).toBeGreaterThan(0);
});

// STRESS TESTING: RAPID MESSAGES

test('handle rapid websocket messages', async ({ page }) => {
  const messageCounters = { sent: 0, received: 0 };
  
  page.on('websocket', ws => {
    ws.on('frameSent', () => messageCounters.sent++);
    ws.on('frameReceived', () => messageCounters.received++);
  });
  
  await page.goto('https://example.com/high-frequency');
  
  // Trigger rapid data updates
  await page.locator('[data-testid="start-streaming"]').click();
  
  // Wait for many messages
  await page.waitForTimeout(5000);
  
  // Stop streaming
  await page.locator('[data-testid="stop-streaming"]').click();
  
  // Verify message counts
  console.log('Message counters:', messageCounters);
  expect(messageCounters.sent).toBeGreaterThan(100);
  expect(messageCounters.received).toBeGreaterThan(100);
});

// BEST PRACTICES FOR REAL-TIME TESTING:
/*
1. Use network event listeners (websocket, page.on)
2. Simulate server-side events with mock servers
3. Test both connection and disconnection scenarios
4. Verify message ordering and content
5. Test reconnection logic with network degradation
6. Monitor WebSocket message frequency for performance
7. Use timeouts to prevent tests hanging on real-time events
8. Mock external real-time services for reliability
*/
```

---

## This document will continue with more sections...

Due to length constraints, I'll create separate files for remaining advanced topics.

