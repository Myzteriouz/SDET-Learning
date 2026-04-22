# The Complete Playwright Guide: From First Test to Production

**Version:** Playwright 1.59+ | Node.js 22 LTS | April 2026

> A comprehensive, production-ready guide to modern web testing

---

## 📑 Quick Navigation

- [Why Playwright?](#why-playwright) 
- [Setup](#installation-and-project-setup)
- [First Tests](#writing-your-first-tests)
- [Advanced Patterns](#advanced-patterns)
- [API & Mocking](#api-testing-and-mocking)
- [CI/CD](#cicd-integration-with-github-actions)
- [Debugging](#debugging)
- [Best Practices](#best-practices-summary)

---

## Overview

Playwright has become the **definitive framework for modern web application testing**. With native support for **Chromium, Firefox, and WebKit**, built-in auto-waiting, powerful debugging, and a unified API, it solves the pain points that made earlier frameworks frustrating.

This guide covers everything from installation through production patterns: page object models, fixtures, API mocking, visual regression, parallel execution, and CI/CD integration.

## Why Playwright?

### The Three Main Options

Playwright, Cypress, and Selenium are **fundamentally different**—not interchangeable.

| Feature | Playwright | Cypress | Selenium |
|---------|------------|---------|----------|
| Cross-browser | Chromium, Firefox, WebKit | Chromium, Firefox, WebKit | All major browsers |
| Architecture | Runs outside browser via CDP/custom protocols | Runs inside browser | Runs outside via WebDriver |
| Auto-wait | Built-in | Built-in | Requires explicit waits |
| Multi-tab/iframe | First-class support | Limited | Supported |
| Language bindings | JS/TS, Python, .NET, Java | JavaScript only | All major languages |
| Parallel execution | Native sharding | Paid feature | Requires Grid |

Playwright runs tests in a Node.js process, driving browsers through the Chrome DevTools Protocol (for Chromium) and custom control protocols (for Firefox and WebKit). This architecture means no same-origin restrictions, first-class support for multiple tabs and iframes, and headless execution that runs fast in CI without a display server.

### ✅ Bottom Line

**For new projects in 2026, Playwright is the right default choice.**

---

## Installation and Project Setup

### Quick Start

``bash
mkdir playwright-demo && cd playwright-demo
npm init playwright@latest
```

**Select these options when prompted:**
- Language: **TypeScript**
- Tests directory: **tests**
- GitHub Actions workflow: **Yes**
- Install browsers: **Yes**

**Project structure created:**

```
playwright-demo/
├── tests/                        # Your test files
│   └── example.spec.ts
├── tests-examples/
│   └── demo-todo-app.spec.ts     # Reference examples
├── playwright.config.ts          # Configuration
├── package.json
└── .github/
    └── workflows/
        └── playwright.yml        # CI/CD automation
```

Browser binaries are downloaded automatically (200–400 MB total). **Verify installation:**

```bash
npx playwright --version
```

### Production-Ready Structure

For larger projects, organize tests by feature/concern:

```
project/
├── playwright.config.ts              # Main configuration
├── tests/                            # Spec files organized by feature
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   ├── checkout/
│   │   └── cart.spec.ts
│   └── search/
│       └── search.spec.ts
├── pages/                            # Page Object Models
│   ├── login.page.ts
│   ├── dashboard.page.ts
│   └── checkout.page.ts
├── fixtures/                         # Custom test fixtures
│   └── auth.fixture.ts
├── utils/                            # Helpers and test data
│   └── test-data.ts
└── .github/
    └── workflows/
        └── playwright.yml            # CI/CD pipelines
```

### Configuration Deep Dive

The configuration file controls browsers, timeouts, retries, URLs, and reporters. **Get this right once—everything else builds on it.**

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.DEPLOYMENTURL ?? 'http://localhost:3000';

export default defineConfig({
  testDir: './tests',
  
  // Run tests in parallel across files
  fullyParallel: true,
  
  // Fail CI if test.only is committed
  forbidOnly: !!process.env.CI,
  
  // Retry failed tests in CI, never locally
  retries: process.env.CI ? 2 : 0,
  
  // Limit workers in CI to reduce flakiness
  workers: process.env.CI ? 1 : undefined,
  
  // Multiple reporters for different contexts
  reporter: [
    ['html', { open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list']
  ],
  
  use: {
    baseURL,
    // Capture trace only on first retry—cheap and invaluable
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 7'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 14'] },
    },
  ],
});
```

#### Key Configuration Decisions

| Setting | What It Does |
|---------|------|
| `baseURL` | Tests use `page.goto('/')` instead of full URLs. Swap environments via `DEPLOYMENTURL` |
| `trace: 'on-first-retry'` | Records trace only on first retry—exactly when you need to debug |
| `retries` | 0 locally (forces fixing flakiness now) vs 2 in CI (handles environment variance) |
| `projects` | 5 browser configs including mobile emulation for complete coverage |

---

## Writing Your First Tests

### Choosing Locators

**Locator strategy determines test durability.** A test using `getByRole()` survives UI refactors. A test using `.btn-primary-submit` does not.

**Priority order:**

| Priority | Method | Use Case | Stability |
|----------|--------|----------|-----------|
| 1 | getByRole() | Buttons, links, headings, form controls | High |
| 2 | getByLabel() | Form inputs with visible labels | High |
| 3 | getByPlaceholder() | Unlabeled inputs | Medium |
| 4 | getByText() | Unique visible content | Medium |
| 5 | getByTestId() | Custom data-testid attributes | Very High |
| 6 | locator() (CSS/XPath) | Last resort | Low |

A test using getByRole('button', { name: 'Submit' }) survives class-name refactors. A test using .btn-primary.submit-btn does not.

Basic Test Structure

`typescript
// tests/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('loads with correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/My App/);
  });

  test('renders primary navigation', async ({ page }) => {
    const nav = page.getByRole('navigation');
    await expect(nav).toBeVisible();
  });

  test('renders hero heading', async ({ page }) => {
    const hero = page.getByRole('heading', { level: 1 });
    await expect(hero).toBeVisible();
  });
});
```

### Form Interactions

```typescript
// tests/auth/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Login', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('secure-password');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page).toHaveURL(/\/dashboard$/);
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  });

  test('invalid credentials show error message', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('wrong-password');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page.getByText('Invalid credentials')).toBeVisible();
    await expect(page).toHaveURL(/\/login$/);
  });
});
```

### Filtering & Chaining

```typescript
test('add specific item to cart', async ({ page }) => {
  // Chain locators to narrow scope
  const product = page.getByRole('listitem').filter({ hasText: 'Product A' });
  
  await product.getByRole('button', { name: 'Add to cart' }).click();
  
  await expect(page.getByTestId('cart-count')).toHaveText('1');
});
```

---

## Advanced Patterns

### Page Object Model

**Encapsulate page logic into reusable classes.** When UI changes, update one file instead of dozens of tests.

```typescript
// pages/todo.page.ts
import { type Locator, type Page, expect } from '@playwright/test';

export class TodoPage {
  readonly page: Page;
  readonly newTodoInput: Locator;
  readonly todoItems: Locator;
  readonly todoCount: Locator;
  readonly clearCompletedButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.newTodoInput = page.getByPlaceholder('What needs to be done?');
    this.todoItems = page.getByTestId('todo-title');
    this.todoCount = page.getByTestId('todo-count');
    this.clearCompletedButton = page.getByRole('button', { name: 'Clear completed' });
  }

  async goto() {
    await this.page.goto('/');
  }

  async addTodo(text: string) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press('Enter');
  }

  async addMultipleTodos(items: string[]) {
    for (const item of items) {
      await this.addTodo(item);
    }
  }

  async toggleTodo(index: number) {
    const checkbox = this.page.getByRole('checkbox').nth(index);
    await checkbox.check();
  }

  async deleteTodo(index: number) {
    const item = this.page.locator('.todo-list li').nth(index);
    await item.hover();
    await item.getByRole('button', { name: 'Delete' }).click();
  }

  async filterBy(filter: 'All' | 'Active' | 'Completed') {
    await this.page.getByRole('link', { name: filter }).click();
  }

  async expectTodoCount(count: number) {
    await expect(this.todoItems).toHaveCount(count);
  }

  async expectTodoTexts(texts: string[]) {
    await expect(this.todoItems).toHaveText(texts);
  }
}
```

**Usage:**

```typescript
// tests/todo-pom.spec.ts
import { test } from '@playwright/test';
import { TodoPage } from '../pages/todo.page';

test.describe('TodoMVC with Page Object Model', () => {
  let todoPage: TodoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.goto();
  });

  test('manages multiple todos', async () => {
    await todoPage.addMultipleTodos(['Write tests', 'Review PR', 'Deploy']);
    await todoPage.expectTodoCount(3);

    await todoPage.toggleTodo(0);
    await todoPage.filterBy('Active');
    await todoPage.expectTodoCount(2);

    await todoPage.filterBy('Completed');
    await todoPage.expectTodoCount(1);
  });

  test('deletes completed todos', async () => {
    await todoPage.addMultipleTodos(['Task A', 'Task B']);
    await todoPage.toggleTodo(0);
    await todoPage.deleteTodo(0);
    
    await todoPage.expectTodoCount(1);
    await todoPage.expectTodoTexts(['Task B']);
  });
});
```

### Custom Fixtures

**Eliminate boilerplate setup.** Define a fixture once, inject as a parameter to any test.

```typescript
// fixtures/auth.fixture.ts
import { test as base, expect } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
  adminPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Login as regular user
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await expect(page).toHaveURL(/\/dashboard/);
    
    // Provide the authenticated page to the test
    await use(page);
  },
  
  adminPage: async ({ page }, use) => {
    // Login as admin
    await page.goto('/login');
    await page.getByLabel('Email').fill('admin@example.com');
    await page.getByLabel('Password').fill('admin-password');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await expect(page).toHaveURL(/\/admin/);
    
    await use(page);
  },
});

export { expect };
`

Using custom fixtures:

`typescript
// tests/dashboard.spec.ts
import { test, expect } from '../fixtures/auth.fixture';

test('authenticated user sees dashboard', async ({ authenticatedPage }) => {
  // Already logged in—no setup needed
  await expect(authenticatedPage.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
});

test('admin sees admin panel', async ({ adminPage }) => {
  await expect(adminPage.getByRole('heading', { name: 'Admin Panel' })).toBeVisible();
});
```

### State Caching

**Large test suites waste time with repeated logins.** Cache auth state and reuse it:

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // Setup project runs first and saves auth state
    {
      name: 'setup',
      testMatch: /.\.setup\.ts/,
    },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Use saved auth state
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Sign in' }).click();
  
  await expect(page).toHaveURL(/\/dashboard/);
  
  // Save signed-in state
  await page.context().storageState({ path: authFile });
});
```

---

## API Testing & Mocking

**Test API endpoints directly. Mock requests to isolate UI from backend dependencies.**

### Direct API Testing

```typescript
// tests/api/users.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Users API', () => {
  test('GET /api/users returns user list', async ({ request }) => {
    const response = await request.get('/api/users');
    
    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);
    
    const users = await response.json();
    expect(users).toBeInstanceOf(Array);
    expect(users.length).toBeGreaterThan(0);
  });

  test('POST /api/users creates new user', async ({ request }) => {
    const response = await request.post('/api/users', {
      data: {
        name: 'Test User',
        email: 'test@example.com',
      },
    });
    
    expect(response.status()).toBe(201);
    
    const user = await response.json();
    expect(user.name).toBe('Test User');
    expect(user.id).toBeDefined();
  });
});
`

Mocking Network Requests

`typescript
test('displays products from mocked API', async ({ page }) => {
  // Intercept API calls and return mock data
  await page.route('/api/products', route => route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([
      { id: 1, name: 'Mock Product', price: 99.99 },
      { id: 2, name: 'Another Product', price: 149.99 },
    ]),
  }));

  await page.goto('/products');
  
  await expect(page.getByText('Mock Product')).toBeVisible();
  await expect(page.getByText('$99.99')).toBeVisible();
});

test('handles API errors gracefully', async ({ page }) => {
  await page.route('/api/products', route => route.fulfill({
    status: 500,
    contentType: 'application/json',
    body: JSON.stringify({ error: 'Internal Server Error' }),
  }));

  await page.goto('/products');
  
  await expect(page.getByText('Failed to load products')).toBeVisible();
});
`

Modifying Responses

`typescript
test('modifies API response on the fly', async ({ page }) => {
  await page.route('/api/user/profile', async route => {
    // Fetch the actual response
    const response = await route.fetch();
    const json = await response.json();
    
    // Modify it
    json.isPremium = true;
    
    // Return modified response
    await route.fulfill({ response, json });
  });

  await page.goto('/profile');
  
  await expect(page.getByText('Premium Member')).toBeVisible();
});
`

Visual Regression Testing

Playwright includes built-in screenshot comparison for visual regression testing.

`typescript
test('homepage matches snapshot', async ({ page }) => {
  await page.goto('/');
  
  // Full page screenshot comparison
  await expect(page).toHaveScreenshot('homepage.png');
});

test('component matches snapshot', async ({ page }) => {
  await page.goto('/dashboard');
  
  // Screenshot of specific element
  const chart = page.getByTestId('revenue-chart');
  await expect(chart).toHaveScreenshot('revenue-chart.png');
});
`

Configure screenshot options in your config:

`typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      // Allow 0.2% pixel difference
      maxDiffPixelRatio: 0.002,
      // Or allow specific pixel count
      // maxDiffPixels: 100,
    },
  },
});
`

Update snapshots when intentional changes occur:

`bash
npx playwright test --update-snapshots
`

Parallel Execution and Sharding
Running Tests in Parallel

By default, Playwright runs test files in parallel. To run tests within a single file in parallel:

`typescript
// tests/independent-tests.spec.ts
import { test } from '@playwright/test';

test.describe.configure({ mode: 'parallel' });

test('test one', async ({ page }) => { / ... / });
test('test two', async ({ page }) => { / ... / });
test('test three', async ({ page }) => { / ... / });
`

Sharding Across Machines

Split your test suite across multiple CI runners:

`bash
Machine 1
npx playwright test --shard=1/3

Machine 2
npx playwright test --shard=2/3

Machine 3
npx playwright test --shard=3/3
`

CI/CD Integration with GitHub Actions

`yaml
.github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [main]
  pullrequest:
    branches: [main]

jobs:
  test:
    timeout-minutes: 30
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3]
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright browsers
        run: npx playwright install chromium --with-deps
      
      - name: Run Playwright tests
        run: npx playwright test --shard=${{ matrix.shard }}/3
        env:
          CI: true
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-${{ matrix.shard }}
          path: playwright-report/
          retention-days: 7
      
      - name: Upload traces
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: traces-${{ matrix.shard }}
          path: test-results/
          retention-days: 7

  merge-reports:
    needs: test
    if: always()
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      
      - name: Download all reports
        uses: actions/download-artifact@v4
        with:
          pattern: playwright-report-
          path: all-reports
      
      - name: Merge reports
        run: npx playwright merge-reports --reporter html ./all-reports
      
      - name: Upload merged report
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
`

Testing Preview Deployments

For projects that deploy each PR to a unique preview URL:

`yaml
.github/workflows/playwright-preview.yml
name: E2E Tests on Preview

on:
  deploymentstatus:

jobs:
  test:
    if: github.event.deploymentstatus.state == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'
      
      - run: npm ci
      - run: npx playwright install chromium --with-deps
      
      - name: Run tests against preview
        run: npx playwright test
        env:
          DEPLOYMENTURL: ${{ github.event.deploymentstatus.targeturl }}
```

---

## Debugging

### Local Debugging

**Debug with the Playwright Inspector:**

```bash
npx playwright test --debug
```

**Debug a specific test:**

```bash
npx playwright test tests/login.spec.ts:15 --debug
```

### VS Code Extension

- ✅ Run/debug tests from editor
- ✅ Live locator picking
- ✅ Trace viewing in sidebar
- ✅ Breakpoint support

### Traces

**Failed test? Download and inspect the trace locally:**

```bash
npx playwright show-trace trace.zip
```

**The trace shows:**
- DOM snapshots at each action
- Network requests & responses
- Console output
- Screenshots

### Codegen

**Record interactions and generate test code:**

```bash
npx playwright codegen https://your-app.com
```

As you interact with the page, codegen generates locator code in real time.

---

## Best Practices Summary

### 🎯 Core Principles

| Practice | Why |
|----------|-----|
| **Test user behavior** | Users see rendered content. Tests should do the same |
| **Isolate completely** | Each test gets fresh context. No inter-test dependencies |
| **Mock third-party APIs** | Don't fail on external service outages |
| **Semantic locators** | `getByRole()` > `getByTestId()` > CSS > XPath |
| **Web-first assertions** | `await expect(locator)` waits and retries automatically |
| **Stay updated** | New browser versions monthly—stay current |
| **CI on every PR** | Catch regressions before merge |
| **Use traces** | Shows exactly what happened when tests fail |

---

## Quick Reference

```bash
npx playwright test                          # Run all tests
npx playwright test tests/login.spec.ts      # Specific file
npx playwright test --headed                 # See the browser
npx playwright test --ui                     # Interactive mode
npx playwright test --project=chromium       # Specific browser
npx playwright test --debug                  # Debug inspector
npx playwright show-report                   # View results
```

---

## Next Steps

1. **Install** and run your first test
2. **Explore** the VS Code extension
3. **Build** a page object model
4. **Set up** GitHub Actions CI/CD
5. **Master** trace viewing

**Happy testing! 🎉**