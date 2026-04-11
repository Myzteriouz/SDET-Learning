# Implementing Parallel Execution with TestNG & Singleton

To achieve parallel execution in a Selenium framework, we combine the **Thread-Safe Singleton Pattern** with **TestNG's execution engine**.

## 1. How TestNG Handles Parallelism
TestNG has native support for multi-threading. You control this entirely via the `testng.xml` file.

```xml
<suite name="My Suite" parallel="methods" thread-count="3">
```

- **`parallel="methods"`**: TestNG will assign a new Java Thread to every individual `@Test` method. (Other options include `classes` or `tests`).
- **`thread-count="3"`**: TestNG will maintain a thread pool of 3. If you have 10 tests, 3 will start immediately. As soon as one finishes, the next one in the queue takes its place.

## 2. Why Basic Selenium Fails Here
If you instantiate a standard `public static WebDriver driver;` in a Base Test, TestNG will cause chaos.
- Thread 1 opens Google.
- Thread 2 starts a millisecond later, overwriting the `driver` variable and navigating to Bing.
- Thread 1 tries to search on Google, but the browser is now on Bing, causing a `NoSuchElementException`.

## 3. The Solution: ThreadLocal + Singleton
By pairing TestNG with our `WebDriverManager` Singleton, we solve this:

1. TestNG spawns Thread `ID 14` for `testGoogleSearch()`.
2. TestNG spawns Thread `ID 15` for `testBingSearch()`.
3. Thread 14 hits `@BeforeMethod` and calls `WebDriverManager.getInstance().getDriver()`. 
   - The Singleton sees that Thread 14 has no driver in its `ThreadLocal` map. It creates **Browser A**.
4. Thread 15 hits `@BeforeMethod` and calls `WebDriverManager.getInstance().getDriver()`.
   - The Singleton sees that Thread 15 has no driver in its `ThreadLocal` map. It creates **Browser B**.

Both tests run simultaneously without ever interfering with one another.

## 4. Lifecycle Hooks Matter (`@BeforeMethod` vs `@BeforeClass`)
For parallel **method** execution, you *must* initialize your driver in `@BeforeMethod`. 

- If you use `@BeforeClass`, the driver is initialized once per class. 
- If you have 5 tests in that class running in parallel, all 5 threads will try to use that single class-level browser, defeating the purpose of `ThreadLocal`.

## 5. Teardown and Memory Leaks
Because TestNG uses a Thread Pool (the threads are recycled, not destroyed), you must clean up the `ThreadLocal` variable after every test.

```java
@AfterMethod
public void tearDown() {
    WebDriverManager.getInstance().quitDriver();
}
```
Inside `quitDriver()`, calling `driver.remove()` ensures that when TestNG recycles Thread 14 for a new test 5 minutes later, it doesn't accidentally try to use the "dead" browser session from earlier.