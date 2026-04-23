# Selenium Advanced Interview Questions - Part 3 (Q16-Q50)

## Framework Design & Architecture (Q16-Q20)

### Q16. Design a complete test automation framework from scratch. Explain structure and best practices.
**Answer:**
```
Framework Structure:
├── src/main/java
│   ├── base
│   │   ├── TestBase.java
│   │   └── DriverFactory.java
│   ├── pages
│   │   ├── BasePage.java
│   │   ├── LoginPage.java
│   │   ├── DashboardPage.java
│   │   └── ProductPage.java
│   ├── utils
│   │   ├── TestDataReader.java
│   │   ├── ConfigManager.java
│   │   ├── ScreenshotManager.java
│   │   └── WaitHelper.java
│   ├── listeners
│   │   ├── TestListener.java
│   │   └── AllureListener.java
│   └── constants
│       └── Constants.java
├── src/test/java
│   ├── LoginTests.java
│   ├── DashboardTests.java
│   └── CheckoutTests.java
├── src/test/resources
│   ├── testdata.json
│   ├── config.properties
│   └── log4j2.xml
└── pom.xml

```

**Implementation:**

```java
// Base Test Class
public abstract class TestBase {
  protected WebDriver driver;
  protected Logger logger = LoggerFactory.getLogger(this.getClass());
  protected ConfigManager config;
  protected TestDataReader testData;
  
  @Before
  public void setUp() {
    config = new ConfigManager();
    testData = new TestDataReader();
    driver = DriverFactory.getDriver(config.getBrowser());
    driver.manage().timeouts()
      .implicitlyWait(Duration.ofSeconds(config.getImplicitWait()));
    logger.info("Test setup completed");
  }
  
  @After
  public void tearDown(ITestResult result) {
    if (result.getStatus() == ITestResult.FAILURE) {
      ScreenshotManager.captureScreenshot(driver, result.getName());
    }
    driver.quit();
    logger.info("Test teardown completed");
  }
}

// Driver Factory
public class DriverFactory {
  public static WebDriver getDriver(String browserName) {
    WebDriver driver;
    
    switch (browserName.toLowerCase()) {
      case "chrome":
        driver = getChromeDriver();
        break;
      case "firefox":
        driver = getFirefoxDriver();
        break;
      case "edge":
        driver = getEdgeDriver();
        break;
      case "safari":
        driver = getSafariDriver();
        break;
      default:
        throw new IllegalArgumentException("Unknown browser: " + browserName);
    }
    
    driver.manage().window().maximize();
    return driver;
  }
  
  private static WebDriver getChromeDriver() {
    ChromeOptions options = new ChromeOptions();
    options.addArguments("--no-sandbox");
    options.addArguments("--disable-dev-shm-usage");
    
    if (Boolean.parseBoolean(System.getenv("HEADLESS"))) {
      options.addArguments("--headless");
    }
    
    return new ChromeDriver(options);
  }
  
  private static WebDriver getFirefoxDriver() {
    FirefoxOptions options = new FirefoxOptions();
    if (Boolean.parseBoolean(System.getenv("HEADLESS"))) {
      options.addArguments("--headless");
    }
    return new FirefoxDriver(options);
  }
  
  private static WebDriver getEdgeDriver() {
    EdgeOptions options = new EdgeOptions();
    return new EdgeDriver(options);
  }
  
  private static WebDriver getSafariDriver() {
    return new SafariDriver();
  }
}

// Base Page Object
public abstract class BasePage {
  protected WebDriver driver;
  protected WebDriverWait wait;
  protected Logger logger = LoggerFactory.getLogger(this.getClass());
  
  public BasePage(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
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
  
  protected boolean isElementDisplayed(By locator) {
    try {
      return driver.findElement(locator).isDisplayed();
    } catch (NoSuchElementException e) {
      return false;
    }
  }
}

// Login Page
public class LoginPage extends BasePage {
  private By emailField = By.id("email");
  private By passwordField = By.id("password");
  private By loginButton = By.id("login-btn");
  private By errorMessage = By.className("error-msg");
  
  public LoginPage(WebDriver driver) {
    super(driver);
  }
  
  public void login(String email, String password) {
    logger.info("Logging in with email: " + email);
    sendKeys(emailField, email);
    sendKeys(passwordField, password);
    click(loginButton);
  }
  
  public DashboardPage loginSuccessfully(String email, String password) {
    login(email, password);
    wait.until(ExpectedConditions.urlContains("dashboard"));
    return new DashboardPage(driver);
  }
  
  public String getErrorMessage() {
    return getText(errorMessage);
  }
}

// Configuration Manager
public class ConfigManager {
  private Properties properties;
  
  public ConfigManager() {
    properties = new Properties();
    try {
      FileInputStream file = new FileInputStream("src/test/resources/config.properties");
      properties.load(file);
      file.close();
    } catch (IOException e) {
      throw new RuntimeException("Failed to load config.properties", e);
    }
  }
  
  public String getBaseUrl() {
    return properties.getProperty("base.url");
  }
  
  public String getBrowser() {
    return properties.getProperty("browser", "chrome");
  }
  
  public int getImplicitWait() {
    return Integer.parseInt(properties.getProperty("implicit.wait", "10"));
  }
  
  public int getExplicitWait() {
    return Integer.parseInt(properties.getProperty("explicit.wait", "15"));
  }
}

// Test Data Reader
public class TestDataReader {
  private JSONObject testData;
  
  public TestDataReader() {
    try {
      String content = Files.readString(Paths.get("src/test/resources/testdata.json"));
      testData = new JSONObject(content);
    } catch (IOException e) {
      throw new RuntimeException("Failed to load test data", e);
    }
  }
  
  public String getData(String key) {
    return testData.getString(key);
  }
  
  public JSONObject getDataObject(String category) {
    return testData.getJSONObject(category);
  }
}

// Screenshot Manager
public class ScreenshotManager {
  public static void captureScreenshot(WebDriver driver, String filename) {
    try {
      File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
      String path = "target/screenshots/" + filename + "_" + System.currentTimeMillis() + ".png";
      new File("target/screenshots").mkdirs();
      Files.copy(src.toPath(), Paths.get(path));
      System.out.println("Screenshot saved: " + path);
    } catch (IOException e) {
      System.out.println("Failed to capture screenshot: " + e.getMessage());
    }
  }
}

// Test Listener
public class TestListener implements ITestListener {
  @Override
  public void onTestStart(ITestResult result) {
    System.out.println("Test started: " + result.getName());
  }
  
  @Override
  public void onTestSuccess(ITestResult result) {
    System.out.println("Test passed: " + result.getName());
  }
  
  @Override
  public void onTestFailure(ITestResult result) {
    System.out.println("Test failed: " + result.getName());
  }
  
  @Override
  public void onTestSkipped(ITestResult result) {
    System.out.println("Test skipped: " + result.getName());
  }
}

// Sample Test Class
@Listeners(TestListener.class)
public class LoginTest extends TestBase {
  private LoginPage loginPage;
  
  @BeforeMethod
  public void testSetup() {
    driver.get(config.getBaseUrl());
    loginPage = new LoginPage(driver);
  }
  
  @Test
  public void testLoginSuccessful() {
    String email = testData.getData("valid_email");
    String password = testData.getData("valid_password");
    
    DashboardPage dashboard = loginPage.loginSuccessfully(email, password);
    assertTrue(dashboard.isDashboardDisplayed());
  }
  
  @Test
  public void testLoginWithInvalidCredentials() {
    loginPage.login("invalid@test.com", "wrongpassword");
    
    String errorMsg = loginPage.getErrorMessage();
    assertTrue(errorMsg.contains("Invalid credentials"));
  }
}

// pom.xml dependencies
/*
<dependencies>
  <dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-java</artifactId>
    <version>4.x</version>
  </dependency>
  
  <dependency>
    <groupId>org.testng</groupId>
    <artifactId>testng</artifactId>
    <version>7.x</version>
  </dependency>
  
  <dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.17.0</version>
  </dependency>
  
  <dependency>
    <groupId>org.json</groupId>
    <artifactId>json</artifactId>
    <version>20220924</version>
  </dependency>
</dependencies>
*/
```

---

## Advanced Topics (Q17-Q50)

### Q17. How do you perform API testing with Selenium? Integrate UI and API testing.
**Answer:**
```java
// Using RestAssured for API testing combined with Selenium

public class APITestHelper {
  private String baseUrl;
  private String apiToken;
  
  public APITestHelper(String baseUrl) {
    this.baseUrl = baseUrl;
    this.apiToken = getAuthToken();
  }
  
  // Get authentication token
  private String getAuthToken() {
    Response response = RestAssured.given()
      .contentType(ContentType.JSON)
      .body("{\"username\":\"user\", \"password\":\"pass\"}")
      .post(baseUrl + "/api/auth/login");
    
    return response.jsonPath().getString("token");
  }
  
  // Create user via API
  public String createUser(String email, String name) {
    Response response = RestAssured.given()
      .header("Authorization", "Bearer " + apiToken)
      .contentType(ContentType.JSON)
      .body("{\"email\":\"" + email + "\", \"name\":\"" + name + "\"}")
      .post(baseUrl + "/api/users");
    
    return response.jsonPath().getString("id");
  }
  
  // Get user data
  public Map<String, Object> getUser(String userId) {
    return RestAssured.given()
      .header("Authorization", "Bearer " + apiToken)
      .get(baseUrl + "/api/users/" + userId)
      .jsonPath()
      .getMap("$");
  }
  
  // Update user via API
  public void updateUser(String userId, String newEmail) {
    RestAssured.given()
      .header("Authorization", "Bearer " + apiToken)
      .contentType(ContentType.JSON)
      .body("{\"email\":\"" + newEmail + "\"}")
      .put(baseUrl + "/api/users/" + userId);
  }
  
  // Delete user via API
  public void deleteUser(String userId) {
    RestAssured.given()
      .header("Authorization", "Bearer " + apiToken)
      .delete(baseUrl + "/api/users/" + userId);
  }
}

// Integrated UI + API test
@Test
public void testUIAndAPICombined() {
  WebDriver driver = new ChromeDriver();
  APITestHelper apiHelper = new APITestHelper("https://api.example.com");
  
  // Create user via API
  String userId = apiHelper.createUser("user@test.com", "Test User");
  logger.info("User created via API: " + userId);
  
  // Verify user in UI
  driver.get("https://example.com/users");
  assertTrue(driver.findElement(By.xpath("//tr[contains(., 'user@test.com')]"))
    .isDisplayed());
  
  // Update user via API
  apiHelper.updateUser(userId, "newemail@test.com");
  
  // Refresh and verify in UI
  driver.navigate().refresh();
  assertTrue(driver.findElement(By.xpath("//tr[contains(., 'newemail@test.com')]"))
    .isDisplayed());
  
  driver.quit();
}

// API request interceptor
public class APIRequestInterceptor {
  private WebDriver driver;
  private List<String> apiRequests = new ArrayList<>();
  
  public APIRequestInterceptor(WebDriver driver) {
    this.driver = driver;
    setupInterceptor();
  }
  
  private void setupInterceptor() {
    ((JavascriptExecutor) driver).executeScript(
      "window.apiRequests = [];" +
      "var originalFetch = window.fetch;" +
      "window.fetch = function(...args) {" +
      "  console.log('API Request:', args[0]);" +
      "  window.apiRequests.push(args[0]);" +
      "  return originalFetch.apply(this, args);" +
      "};"
    );
  }
  
  public List<String> getCapturedRequests() {
    @SuppressWarnings("unchecked")
    List<String> requests = (List<String>) ((JavascriptExecutor) driver)
      .executeScript("return window.apiRequests;");
    return requests;
  }
}

// Complete E2E test with API
@Test
public void testE2EUserJourney() {
  WebDriver driver = new ChromeDriver();
  APITestHelper api = new APITestHelper("https://api.example.com");
  APIRequestInterceptor interceptor = new APIRequestInterceptor(driver);
  
  try {
    // Setup: Create user and product via API
    String userId = api.createUser("e2e@test.com", "E2E User");
    String productId = api.createProduct("Test Product", 99.99);
    
    // UI Test: Login
    driver.get("https://example.com/login");
    driver.findElement(By.id("email")).sendKeys("e2e@test.com");
    driver.findElement(By.id("password")).sendKeys("password");
    driver.findElement(By.id("login")).click();
    
    // Verify API calls were made
    List<String> requests = interceptor.getCapturedRequests();
    assertTrue(requests.stream().anyMatch(r -> r.contains("/api/products")));
    
    // Continue with shopping flow
    driver.findElement(By.xpath("//button[contains(., '" + productId + "')]"))
      .click();
    driver.findElement(By.id("add-to-cart")).click();
    driver.findElement(By.id("checkout")).click();
    
    // Verify order via API
    Map<String, Object> order = api.getLatestOrder(userId);
    assertEquals(1, order.get("items_count"));
    
  } finally {
    driver.quit();
  }
}
```

---

### Q18. How do you integrate Selenium tests with CI/CD pipelines (Jenkins, GitHub Actions)? Explain setup.
**Answer:**
```yaml
# GitHub Actions workflow (.github/workflows/test.yml)
name: Selenium Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        browser: [chrome, firefox]
        java-version: [11, 17]
    
    services:
      selenium:
        image: selenium/standalone-chrome:latest
        options: >-
          --health-cmd /opt/bin/check-grid.sh
          --health-interval 5s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 4444:4444
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up JDK ${{ matrix.java-version }}
        uses: actions/setup-java@v2
        with:
          java-version: ${{ matrix.java-version }}
          distribution: 'temurin'
      
      - name: Build with Maven
        run: mvn clean compile
      
      - name: Run Selenium tests
        run: |
          export BROWSER=${{ matrix.browser }}
          export HEADLESS=true
          mvn test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: test-results-${{ matrix.browser }}-${{ matrix.java-version }}
          path: target/surefire-reports/
      
      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: screenshots-${{ matrix.browser }}
          path: target/screenshots/
      
      - name: Generate Allure report
        if: always()
        uses: simple-elf/allure-report-action@master
        with:
          allure_results: target/allure-results
          gh_pages_branch: gh-pages
      
      - name: Publish test report
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: Test Results
          path: target/surefire-reports/*.xml
          reporter: 'java-junit'
```

```groovy
// Jenkinsfile for Jenkins CI/CD
pipeline {
  agent any
  
  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timeout(time: 1, unit: 'HOURS')
    timestamps()
  }
  
  parameters {
    choice(
      name: 'BROWSER',
      choices: ['chrome', 'firefox', 'edge'],
      description: 'Select browser'
    )
    booleanParam(
      name: 'HEADLESS',
      defaultValue: true,
      description: 'Run in headless mode'
    )
  }
  
  stages {
    stage('Checkout') {
      steps {
        checkout scm
        script {
          BUILD_NUMBER = "${env.BUILD_NUMBER}"
          echo "Build #${BUILD_NUMBER}"
        }
      }
    }
    
    stage('Setup') {
      steps {
        sh '''
          echo "Java version:"
          java -version
          
          echo "Starting Selenium Grid..."
          docker-compose up -d
          sleep 10
        '''
      }
    }
    
    stage('Build') {
      steps {
        sh 'mvn clean compile'
      }
    }
    
    stage('Test') {
      steps {
        sh '''
          export BROWSER=${BROWSER}
          export HEADLESS=${HEADLESS}
          mvn test -Dbrowser=${BROWSER} -Dheadless=${HEADLESS}
        '''
      }
    }
    
    stage('Report') {
      steps {
        junit 'target/surefire-reports/**/*.xml'
        allure includeProperties: false,
                jdk: '',
                results: [[path: 'target/allure-results']]
      }
    }
    
    stage('Archive') {
      steps {
        archiveArtifacts artifacts: 'target/**/*', 
                         allowEmptyArchive: true
      }
    }
  }
  
  post {
    always {
      // Cleanup
      sh 'docker-compose down'
      
      // Archive results
      archiveArtifacts artifacts: 'target/screenshots/**',
                       allowEmptyArchive: true
    }
    
    success {
      echo 'Tests passed!'
    }
    
    failure {
      echo 'Tests failed!'
      // Send notification
      emailext(
        subject: "Test Build Failed - ${env.BUILD_NUMBER}",
        body: "Build failed. Check console output.",
        to: "${env.CHANGE_AUTHOR_EMAIL}"
      )
    }
  }
}
```

```java
// Maven configuration for CI/CD (pom.xml)
<properties>
  <maven.compiler.source>11</maven.compiler.source>
  <maven.compiler.target>11</maven.compiler.target>
  <browser>chrome</browser>
  <headless>true</headless>
  <tags>@regression</tags>
</properties>

<profiles>
  <profile>
    <id>smoke</id>
    <properties>
      <tags>@smoke</tags>
    </properties>
  </profile>
  
  <profile>
    <id>regression</id>
    <properties>
      <tags>@regression</tags>
    </properties>
  </profile>
  
  <profile>
    <id>headless</id>
    <properties>
      <headless>true</headless>
    </properties>
  </profile>
</profiles>

<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <version>2.22.2</version>
      <configuration>
        <systemPropertyVariables>
          <browser>${browser}</browser>
          <headless>${headless}</headless>
          <tags>${tags}</tags>
        </systemPropertyVariables>
      </configuration>
    </plugin>
  </plugins>
</build>
```

---

### Q19. How do you handle performance testing with Selenium? Measure page load times and bottlenecks.
**Answer:**
```java
public class PerformanceAnalyzer {
  private WebDriver driver;
  
  public PerformanceAnalyzer(WebDriver driver) {
    this.driver = driver;
  }
  
  // Get Navigation Timing API metrics
  public PerformanceMetrics getPageLoadMetrics() {
    JavascriptExecutor js = (JavascriptExecutor) driver;
    
    String script = 
      "var timing = window.performance.timing;" +
      "return {" +
      "  dns: timing.domainLookupEnd - timing.domainLookupStart," +
      "  tcp: timing.connectEnd - timing.connectStart," +
      "  ttfb: timing.responseStart - timing.requestStart," +
      "  download: timing.responseEnd - timing.responseStart," +
      "  domInteractive: timing.domInteractive - timing.navigationStart," +
      "  domComplete: timing.domComplete - timing.navigationStart," +
      "  pageLoadTime: timing.loadEventEnd - timing.navigationStart" +
      "}";
    
    @SuppressWarnings("unchecked")
    Map<String, Long> metrics = (Map<String, Long>) js.executeScript(script);
    
    return new PerformanceMetrics(metrics);
  }
  
  // Get Resource Timing (JS, CSS, Images)
  public List<ResourceTiming> getResourceTimings() {
    JavascriptExecutor js = (JavascriptExecutor) driver;
    
    String script =
      "var resources = window.performance.getEntriesByType('resource');" +
      "return resources.map(r => ({" +
      "  name: r.name," +
      "  type: r.initiatorType," +
      "  duration: r.duration," +
      "  size: r.transferSize" +
      "}));";
    
    @SuppressWarnings("unchecked")
    List<Map<String, Object>> resources = 
      (List<Map<String, Object>>) js.executeScript(script);
    
    return resources.stream()
      .map(r -> new ResourceTiming(r))
      .collect(Collectors.toList());
  }
  
  // Measure specific action performance
  public long measureActionTime(Consumer<WebDriver> action) {
    long startTime = System.currentTimeMillis();
    action.accept(driver);
    return System.currentTimeMillis() - startTime;
  }
  
  // Get Core Web Vitals
  public CoreWebVitals getCoreWebVitals() {
    JavascriptExecutor js = (JavascriptExecutor) driver;
    
    String script =
      "var vitals = {};" +
      "new PerformanceObserver((list) => {" +
      "  for (const entry of list.getEntries()) {" +
      "    if (entry.name === 'first-input') {" +
      "      vitals.fid = entry.processingStart - entry.startTime;" +
      "    }" +
      "  }" +
      "}).observe({entryTypes: ['first-input']});" +
      "new PerformanceObserver((list) => {" +
      "  for (const entry of list.getEntries()) {" +
      "    vitals.lcp = entry.renderTime || entry.loadTime;" +
      "  }" +
      "}).observe({entryTypes: ['largest-contentful-paint']});" +
      "return vitals;";
    
    @SuppressWarnings("unchecked")
    Map<String, Long> vitals = (Map<String, Long>) js.executeScript(script);
    
    return new CoreWebVitals(vitals);
  }
  
  static class PerformanceMetrics {
    Map<String, Long> metrics;
    
    PerformanceMetrics(Map<String, Long> metrics) {
      this.metrics = metrics;
    }
    
    public long getPageLoadTime() {
      return metrics.get("pageLoadTime");
    }
    
    public long getDNSTime() {
      return metrics.get("dns");
    }
    
    public void printReport() {
      System.out.println("=== Page Load Performance Report ===");
      System.out.println("DNS Lookup: " + metrics.get("dns") + "ms");
      System.out.println("TCP Connection: " + metrics.get("tcp") + "ms");
      System.out.println("TTFB: " + metrics.get("ttfb") + "ms");
      System.out.println("Download: " + metrics.get("download") + "ms");
      System.out.println("DOM Interactive: " + metrics.get("domInteractive") + "ms");
      System.out.println("DOM Complete: " + metrics.get("domComplete") + "ms");
      System.out.println("Total Page Load: " + metrics.get("pageLoadTime") + "ms");
    }
  }
}

// Performance test example
@Test
public void testPageLoadPerformance() {
  WebDriver driver = new ChromeDriver();
  PerformanceAnalyzer analyzer = new PerformanceAnalyzer(driver);
  
  driver.get("https://example.com");
  
  // Get metrics
  PerformanceMetrics metrics = analyzer.getPageLoadMetrics();
  metrics.printReport();
  
  // Assert performance thresholds
  assertTrue(metrics.getPageLoadTime() < 3000, 
    "Page load time should be less than 3 seconds");
  assertTrue(metrics.getDNSTime() < 100, 
    "DNS lookup should be less than 100ms");
  
  // Analyze resources
  List<ResourceTiming> resources = analyzer.getResourceTimings();
  resources.forEach(r -> {
    if (r.duration > 1000) {
      System.out.println("Slow resource: " + r.name + " (" + r.duration + "ms)");
    }
  });
  
  driver.quit();
}
```

---

### Q20. How do you implement data-driven testing? Use different data sources.
**Answer:**
```java
// Excel-based data-driven testing
public class ExcelDataProvider {
  public static Object[][] getTestData(String filePath, String sheetName) 
      throws IOException {
    FileInputStream fis = new FileInputStream(filePath);
    XSSFWorkbook workbook = new XSSFWorkbook(fis);
    XSSFSheet sheet = workbook.getSheet(sheetName);
    
    int rows = sheet.getPhysicalNumberOfRows();
    int cols = sheet.getRow(0).getPhysicalNumberOfCells();
    
    Object[][] data = new Object[rows - 1][cols];
    
    for (int i = 1; i < rows; i++) {
      XSSFRow row = sheet.getRow(i);
      for (int j = 0; j < cols; j++) {
        data[i - 1][j] = row.getCell(j).getStringCellValue();
      }
    }
    
    workbook.close();
    fis.close();
    
    return data;
  }
}

// JSON-based data provider
public class JSONDataProvider {
  public static Object[][] getTestDataFromJSON(String jsonFilePath, 
                                               String dataKey) throws IOException {
    String content = Files.readString(Paths.get(jsonFilePath));
    JSONArray jsonArray = new JSONArray(content);
    
    Object[][] data = new Object[jsonArray.length()][1];
    
    for (int i = 0; i < jsonArray.length(); i++) {
      data[i][0] = jsonArray.getJSONObject(i);
    }
    
    return data;
  }
}

// CSV-based data provider
public class CSVDataProvider {
  public static Object[][] getTestDataFromCSV(String csvFilePath) 
      throws IOException {
    List<String[]> lines = Files.readAllLines(Paths.get(csvFilePath))
      .stream()
      .map(line -> line.split(","))
      .collect(Collectors.toList());
    
    return lines.stream().skip(1).toArray(Object[][]::new);
  }
}

// Database-based data provider
public class DatabaseDataProvider {
  private Connection connection;
  
  public DatabaseDataProvider(String url, String user, String password) 
      throws SQLException {
    connection = DriverManager.getConnection(url, user, password);
  }
  
  public Object[][] getTestData(String query) throws SQLException {
    Statement stmt = connection.createStatement();
    ResultSet rs = stmt.executeQuery(query);
    
    ResultSetMetaData metadata = rs.getMetaData();
    int colCount = metadata.getColumnCount();
    
    List<Object[]> data = new ArrayList<>();
    while (rs.next()) {
      Object[] row = new Object[colCount];
      for (int i = 0; i < colCount; i++) {
        row[i] = rs.getObject(i + 1);
      }
      data.add(row);
    }
    
    return data.toArray(new Object[0][]);
  }
}

// Data-driven test with multiple sources
public class DataDrivenTests extends TestBase {
  
  // Excel-based
  @Test(dataProvider = "excelData")
  public void testLoginFromExcel(String email, String password) {
    driver.get(config.getBaseUrl());
    driver.findElement(By.id("email")).sendKeys(email);
    driver.findElement(By.id("password")).sendKeys(password);
    driver.findElement(By.id("login")).click();
    
    assertTrue(driver.getCurrentUrl().contains("dashboard"));
  }
  
  @DataProvider(name = "excelData")
  public Object[][] getExcelData() throws IOException {
    return ExcelDataProvider.getTestData(
      "src/test/resources/testdata.xlsx", 
      "LoginData"
    );
  }
  
  // JSON-based
  @Test(dataProvider = "jsonData")
  public void testCreateUserFromJSON(JSONObject userData) {
    driver.get(config.getBaseUrl() + "/create-user");
    
    driver.findElement(By.id("name")).sendKeys(userData.getString("name"));
    driver.findElement(By.id("email")).sendKeys(userData.getString("email"));
    driver.findElement(By.id("phone")).sendKeys(userData.getString("phone"));
    driver.findElement(By.id("submit")).click();
    
    assertTrue(driver.getPageSource().contains("User created successfully"));
  }
  
  @DataProvider(name = "jsonData")
  public Object[][] getJSONData() throws IOException {
    return JSONDataProvider.getTestDataFromJSON(
      "src/test/resources/userdata.json",
      "users"
    );
  }
  
  // CSV-based
  @Test(dataProvider = "csvData")
  public void testSearchFromCSV(String[] searchData) {
    String searchTerm = searchData[0];
    String expectedResult = searchData[1];
    
    driver.get(config.getBaseUrl());
    driver.findElement(By.id("search")).sendKeys(searchTerm);
    driver.findElement(By.id("search-btn")).click();
    
    assertTrue(driver.getPageSource().contains(expectedResult));
  }
  
  @DataProvider(name = "csvData")
  public Object[][] getCSVData() throws IOException {
    return CSVDataProvider.getTestDataFromCSV(
      "src/test/resources/searchdata.csv"
    );
  }
  
  // Parameterized with multiple values
  @Test(dataProvider = "multipleValues")
  public void testWithMultipleValues(String username, String password, 
                                     String expectedResult) {
    driver.get(config.getBaseUrl());
    driver.findElement(By.id("username")).sendKeys(username);
    driver.findElement(By.id("password")).sendKeys(password);
    driver.findElement(By.id("login")).click();
    
    assertEquals(expectedResult, 
      driver.findElement(By.id("result")).getText());
  }
  
  @DataProvider(name = "multipleValues")
  public Object[][] getMultipleValues() {
    return new Object[][] {
      {"user1", "pass1", "Success"},
      {"user2", "pass2", "Success"},
      {"invalid", "wrong", "Error"},
      {"", "", "Error"}
    };
  }
}

// Test data model
class TestData {
  private String email;
  private String password;
  private String firstName;
  private String lastName;
  
  public TestData(String email, String password, String firstName, String lastName) {
    this.email = email;
    this.password = password;
    this.firstName = firstName;
    this.lastName = lastName;
  }
  
  // Getters and setters
}

// Advanced: Data-driven with custom object
@Test(dataProvider = "customData")
public void testWithCustomObjects(TestData data) {
  driver.get(config.getBaseUrl() + "/register");
  
  driver.findElement(By.id("email")).sendKeys(data.getEmail());
  driver.findElement(By.id("password")).sendKeys(data.getPassword());
  driver.findElement(By.id("firstName")).sendKeys(data.getFirstName());
  driver.findElement(By.id("lastName")).sendKeys(data.getLastName());
  driver.findElement(By.id("register")).click();
  
  assertTrue(driver.getPageSource().contains("Registration successful"));
}

@DataProvider(name = "customData")
public Object[][] getCustomData() {
  return new Object[][] {
    {new TestData("user1@test.com", "pass123", "John", "Doe")},
    {new TestData("user2@test.com", "pass456", "Jane", "Smith")},
    {new TestData("user3@test.com", "pass789", "Bob", "Johnson")}
  };
}
```

---

## Advanced Testing Techniques (Q21-Q30)

### Q21. How do you implement visual regression testing in Selenium? Explain tools and strategies.
**Answer:**
Visual regression testing compares screenshots of the application at different times to detect unintended UI changes.

```java
public class VisualRegressionTester {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public VisualRegressionTester(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Using Ashot library for full-page screenshots
  public BufferedImage captureFullPage() throws IOException {
    Screenshot screenshot = new AShot()
      .shootingStrategy(new ViewportPastingStrategy(1000))
      .takeScreenshot(driver);
    
    return screenshot.getImage();
  }
  
  // Capture specific element
  public BufferedImage captureElement(By locator) throws IOException {
    WebElement element = driver.findElement(locator);
    
    Screenshot screenshot = new AShot()
      .coordsProvider(new WebDriverCoordsProvider())
      .takeScreenshot(driver, element);
    
    return screenshot.getImage();
  }
  
  // Compare with baseline
  public void compareWithBaseline(BufferedImage current, String baselineFile) 
      throws IOException {
    BufferedImage baseline = ImageIO.read(new File(baselineFile));
    
    ImageDiffer differ = new ImageDiffer();
    ImageDiff diff = differ.makeDiff(baseline, current);
    
    if (diff.countDiffPixels() > 0) {
      ImageIO.write(diff.getMarkedImage(), "png", 
        new File("target/diffs/diff_" + System.currentTimeMillis() + ".png"));
      
      fail("Visual difference detected. Diff pixels: " + diff.countDiffPixels());
    }
  }
  
  // Ignore dynamic regions
  public BufferedImage captureWithMaskRegions(List<Rectangle> maskRegions) 
      throws IOException {
    Screenshot screenshot = new AShot()
      .shootingStrategy(new ViewportPastingStrategy(1000))
      .takeScreenshot(driver);
    
    BufferedImage image = screenshot.getImage();
    Graphics2D g2d = image.createGraphics();
    g2d.setColor(Color.BLACK);
    
    for (Rectangle region : maskRegions) {
      g2d.fillRect(region.x, region.y, region.width, region.height);
    }
    g2d.dispose();
    
    return image;
  }
}

// Usage example
@Test
public void testVisualRegression() throws IOException {
  VisualRegressionTester visualTester = new VisualRegressionTester(driver);
  
  driver.get("https://example.com/dashboard");
  wait.until(ExpectedConditions.presenceOfElementLocated(By.id("dashboard")));
  
  // Mask dynamic regions (timestamps, counters, etc.)
  List<Rectangle> maskRegions = Arrays.asList(
    new Rectangle(100, 50, 200, 30),  // timestamp region
    new Rectangle(400, 100, 150, 20)  // counter region
  );
  
  BufferedImage current = visualTester.captureWithMaskRegions(maskRegions);
  visualTester.compareWithBaseline(current, "src/test/resources/baseline_dashboard.png");
}
```

---

### Q22. How do you handle Appium testing with Selenium for mobile applications?
**Answer:**
Appium extends Selenium WebDriver to support mobile application testing on iOS and Android.

```java
public class MobileTestingHelper {
  private AppiumDriver driver;
  
  // Setup for Android testing
  public static AppiumDriver setupAndroidDriver(String apkPath) 
      throws MalformedURLException {
    DesiredCapabilities capabilities = new DesiredCapabilities();
    capabilities.setCapability("platformName", "Android");
    capabilities.setCapability("platformVersion", "12");
    capabilities.setCapability("deviceName", "Android Emulator");
    capabilities.setCapability("automationName", "UiAutomator2");
    capabilities.setCapability("app", apkPath);
    capabilities.setCapability("autoGrantPermissions", true);
    
    AppiumDriver driver = new AndroidDriver(
      new URL("http://127.0.0.1:4723/wd/hub"), 
      capabilities
    );
    
    return driver;
  }
  
  // Setup for iOS testing
  public static AppiumDriver setupIOSDriver() throws MalformedURLException {
    DesiredCapabilities capabilities = new DesiredCapabilities();
    capabilities.setCapability("platformName", "iOS");
    capabilities.setCapability("platformVersion", "15.0");
    capabilities.setCapability("deviceName", "iPhone 12");
    capabilities.setCapability("automationName", "XCUITest");
    capabilities.setCapability("bundleId", "com.example.app");
    
    AppiumDriver driver = new IOSDriver(
      new URL("http://127.0.0.1:4723/wd/hub"), 
      capabilities
    );
    
    return driver;
  }
  
  // Find elements using AppiumBy locators
  public static class MobileLocators {
    // Android specific
    public static By androidResourceId(String id) {
      return AppiumBy.id("com.example.app:id/" + id);
    }
    
    // iOS specific
    public static By iOSPredicate(String predicate) {
      return AppiumBy.iOSNsPredicateString(predicate);
    }
    
    // Accessibility ID (works on both)
    public static By accessibilityId(String id) {
      return AppiumBy.accessibilityId(id);
    }
    
    // UiAutomator (Android)
    public static By uiAutomator(String selector) {
      return AppiumBy.androidUIAutomator(selector);
    }
  }
}

// Mobile test example
@Test
public void testMobileLogin() throws MalformedURLException {
  AppiumDriver driver = MobileTestingHelper.setupAndroidDriver("path/to/app.apk");
  
  try {
    // Find and interact with mobile elements
    MobileElement emailField = (MobileElement) driver.findElement(
      MobileTestingHelper.MobileLocators.accessibilityId("email_input")
    );
    emailField.sendKeys("user@test.com");
    
    MobileElement passwordField = (MobileElement) driver.findElement(
      MobileTestingHelper.MobileLocators.accessibilityId("password_input")
    );
    passwordField.sendKeys("password123");
    
    // Tap button (mobile gesture)
    MobileElement loginButton = (MobileElement) driver.findElement(
      MobileTestingHelper.MobileLocators.accessibilityId("login_button")
    );
    loginButton.click();
    
    // Verify navigation
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    wait.until(ExpectedConditions.presenceOfElementLocated(
      MobileTestingHelper.MobileLocators.accessibilityId("dashboard")
    ));
    
    System.out.println("Mobile login test passed");
    
  } finally {
    driver.quit();
  }
}
```

---

### Q23. How do you implement accessibility testing in Selenium? Check for WCAG compliance.
**Answer:**
Accessibility testing ensures applications are usable by people with disabilities and comply with WCAG (Web Content Accessibility Guidelines).

```java
public class AccessibilityTester {
  private WebDriver driver;
  private AxeBuilder axeBuilder;
  
  public AccessibilityTester(WebDriver driver) {
    this.driver = driver;
    this.axeBuilder = new AxeBuilder();
  }
  
  // Scan entire page with Axe
  public AxeResults scanPage() {
    return axeBuilder.analyze(driver);
  }
  
  // Scan specific element
  public AxeResults scanElement(By locator) {
    WebElement element = driver.findElement(locator);
    return axeBuilder.include(element).analyze(driver);
  }
  
  // Check color contrast
  public void checkContrast(By locator) {
    WebElement element = driver.findElement(locator);
    String foreground = element.getCssValue("color");
    String background = element.getCssValue("background-color");
    
    // Parse RGB colors and calculate contrast ratio
    double ratio = calculateContrastRatio(foreground, background);
    
    // WCAG AA requires 4.5:1 for normal text, 3:1 for large text
    assertTrue(ratio >= 4.5, "Color contrast ratio is " + ratio + ". Required: 4.5");
  }
  
  // Verify heading hierarchy
  public void verifyHeadingHierarchy() {
    List<WebElement> headings = driver.findElements(By.xpath("//h1|//h2|//h3|//h4|//h5|//h6"));
    
    int previousLevel = 0;
    for (WebElement heading : headings) {
      String tagName = heading.getTagName();
      int currentLevel = Integer.parseInt(tagName.substring(1));
      
      // Headings should not skip levels
      assertTrue(currentLevel <= previousLevel + 1, 
        "Heading hierarchy broken: " + tagName);
      
      previousLevel = currentLevel;
    }
  }
  
  // Check alt text on images
  public void verifyImageAltText() {
    List<WebElement> images = driver.findElements(By.tagName("img"));
    
    for (WebElement img : images) {
      String altText = img.getAttribute("alt");
      assertTrue(altText != null && !altText.isEmpty(), 
        "Image missing alt text: " + img.getAttribute("src"));
    }
  }
  
  // Check form labels
  public void verifyFormLabels() {
    List<WebElement> inputs = driver.findElements(By.tagName("input"));
    
    for (WebElement input : inputs) {
      String id = input.getAttribute("id");
      if (id != null && !id.isEmpty()) {
        List<WebElement> labels = driver.findElements(
          By.xpath("//label[@for='" + id + "']")
        );
        assertTrue(!labels.isEmpty(), "Input missing associated label: " + id);
      }
    }
  }
  
  // Private helper
  private double calculateContrastRatio(String foreground, String background) {
    // Parse RGB and calculate WCAG contrast ratio
    // Simplified example - actual implementation would parse CSS colors
    return 5.0;  // Placeholder
  }
}

// Accessibility test
@Test
public void testAccessibilityCompliance() {
  AccessibilityTester tester = new AccessibilityTester(driver);
  
  driver.get("https://example.com");
  
  // Run Axe scan
  AxeResults results = tester.scanPage();
  
  // Assert no violations
  assertTrue(results.getViolations().isEmpty(), 
    "Accessibility violations found: " + results.getViolations());
  
  // Additional checks
  tester.verifyHeadingHierarchy();
  tester.verifyImageAltText();
  tester.verifyFormLabels();
  
  System.out.println("Page is WCAG compliant");
}
```

---

### Q24. How do you implement cross-browser testing with Selenium? Manage multiple browser configurations.
**Answer:**
```java
@RunWith(Parameterized.class)
public class CrossBrowserTests {
  private WebDriver driver;
  private String browser;
  
  public CrossBrowserTests(String browser) {
    this.browser = browser;
  }
  
  @Parameterized.Parameters(name = "{index}: Testing with {0}")
  public static Collection<String> browsers() {
    return Arrays.asList("chrome", "firefox", "edge", "safari");
  }
  
  @Before
  public void setUp() {
    driver = WebDriverFactory.createDriver(browser);
  }
  
  @After
  public void tearDown() {
    if (driver != null) {
      driver.quit();
    }
  }
  
  @Test
  public void testLoginFunctionality() {
    driver.get("https://example.com/login");
    
    driver.findElement(By.id("email")).sendKeys("user@test.com");
    driver.findElement(By.id("password")).sendKeys("password");
    driver.findElement(By.id("login")).click();
    
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    wait.until(ExpectedConditions.urlContains("dashboard"));
    
    assertTrue(driver.getCurrentUrl().contains("dashboard"));
  }
}

public class WebDriverFactory {
  public static WebDriver createDriver(String browserName) {
    switch (browserName.toLowerCase()) {
      case "chrome":
        return createChromeDriver();
      case "firefox":
        return createFirefoxDriver();
      case "edge":
        return createEdgeDriver();
      case "safari":
        return createSafariDriver();
      default:
        throw new IllegalArgumentException("Unsupported browser: " + browserName);
    }
  }
  
  private static WebDriver createChromeDriver() {
    ChromeOptions options = new ChromeOptions();
    options.addArguments("--start-maximized");
    options.addArguments("--disable-blink-features=AutomationControlled");
    options.setExperimentalOption("excludeSwitches", new String[]{"enable-automation"});
    options.setExperimentalOption("useAutomationExtension", false);
    
    return new ChromeDriver(options);
  }
  
  private static WebDriver createFirefoxDriver() {
    FirefoxOptions options = new FirefoxOptions();
    options.addArguments("--start-maximized");
    return new FirefoxDriver(options);
  }
  
  private static WebDriver createEdgeDriver() {
    EdgeOptions options = new EdgeOptions();
    options.addArguments("--start-maximized");
    return new EdgeDriver(options);
  }
  
  private static WebDriver createSafariDriver() {
    return new SafariDriver();
  }
}
```

---

### Q25. How do you implement retry mechanisms and flaky test handling?
**Answer:**
```java
public class RetryAnalyzer implements IRetryAnalyzer {
  private int retryCount = 0;
  private static final int MAX_RETRY = 2;
  
  @Override
  public boolean retry(ITestResult result) {
    if (retryCount < MAX_RETRY && result.getStatus() == ITestResult.FAILURE) {
      retryCount++;
      System.out.println("Retrying test: " + result.getName() + 
                        " (Attempt " + (retryCount + 1) + ")");
      return true;
    }
    return false;
  }
}

// Use in test
@Test(retryAnalyzer = RetryAnalyzer.class)
public void testFlakySituation() {
  // Test code
}

// Advanced retry with conditions
public class SmartRetryAnalyzer implements IRetryAnalyzer {
  private int retryCount = 0;
  
  @Override
  public boolean retry(ITestResult result) {
    Throwable throwable = result.getThrowable();
    
    // Only retry on specific exceptions
    boolean shouldRetry = throwable instanceof TimeoutException ||
                         throwable instanceof StaleElementReferenceException;
    
    if (shouldRetry && retryCount < 2) {
      retryCount++;
      System.out.println("Retrying due to: " + throwable.getClass().getSimpleName());
      return true;
    }
    return false;
  }
}

// Wait wrapper for better stability
public class FlakeSafeWait {
  private WebDriver driver;
  private WebDriverWait wait;
  private static final int MAX_ATTEMPTS = 3;
  
  public FlakeSafeWait(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  public void clickWithRetry(By locator) {
    int attempts = 0;
    while (attempts < MAX_ATTEMPTS) {
      try {
        wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
        return;
      } catch (StaleElementReferenceException | TimeoutException e) {
        attempts++;
        if (attempts >= MAX_ATTEMPTS) throw e;
        sleep(500);
      }
    }
  }
  
  public void fillWithRetry(By locator, String text) {
    int attempts = 0;
    while (attempts < MAX_ATTEMPTS) {
      try {
        WebElement element = wait.until(
          ExpectedConditions.visibilityOfElementLocated(locator)
        );
        element.clear();
        element.sendKeys(text);
        return;
      } catch (StaleElementReferenceException | TimeoutException e) {
        attempts++;
        if (attempts >= MAX_ATTEMPTS) throw e;
        sleep(500);
      }
    }
  }
  
  private void sleep(long ms) {
    try {
      Thread.sleep(ms);
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
    }
  }
}
```

---

### Q26. How do you implement advanced reporting with Allure and ExtentReports?
**Answer:**
```java
// ExtentReports implementation
public class ExtentReportManager {
  private static ExtentReports extentReports;
  private static ExtentTest extentTest;
  
  public static void initReport() {
    ExtentSparkReporter sparkReporter = new ExtentSparkReporter("target/ExtentReport.html");
    sparkReporter.config().setDocumentTitle("Automation Test Report");
    sparkReporter.config().setReportName("Test Execution Report");
    
    extentReports = new ExtentReports();
    extentReports.attachReporter(sparkReporter);
    extentReports.setSystemInfo("OS", System.getProperty("os.name"));
    extentReports.setSystemInfo("Java Version", System.getProperty("java.version"));
    extentReports.setSystemInfo("Browser", "Chrome");
  }
  
  public static void createTest(String testName) {
    extentTest = extentReports.createTest(testName);
  }
  
  public static void logPass(String message) {
    extentTest.pass(message);
  }
  
  public static void logFail(String message, String screenshot) {
    extentTest.fail(message);
    extentTest.addScreenCaptureFromPath(screenshot);
  }
  
  public static void logInfo(String message) {
    extentTest.info(message);
  }
  
  public static void flushReport() {
    if (extentReports != null) {
      extentReports.flush();
    }
  }
}

// Allure reporting
@Listener(AllureTestListener.class)
public class AllureTests {
  private WebDriver driver;
  
  @BeforeMethod
  public void setUp() {
    driver = new ChromeDriver();
  }
  
  @Test
  @Story("User Authentication")
  @Feature("Login")
  @Severity(SeverityLevel.CRITICAL)
  @Description("Test user login with valid credentials")
  public void testLoginWithAllure() {
    Allure.step("Navigate to login page", () -> {
      driver.get("https://example.com/login");
    });
    
    Allure.step("Enter credentials", () -> {
      driver.findElement(By.id("email")).sendKeys("user@test.com");
      driver.findElement(By.id("password")).sendKeys("password");
    });
    
    Allure.step("Click login button", () -> {
      driver.findElement(By.id("login")).click();
    });
    
    Allure.step("Verify dashboard", () -> {
      assertTrue(driver.getCurrentUrl().contains("dashboard"));
    });
  }
  
  @AfterMethod
  public void tearDown() {
    driver.quit();
  }
}

// allure.properties configuration
// allure.results.directory=target/allure-results
```

---

### Q27. How do you implement Shadow DOM and Web Components testing?
**Answer:**
```java
public class ShadowDOMHelper {
  private WebDriver driver;
  
  public ShadowDOMHelper(WebDriver driver) {
    this.driver = driver;
  }
  
  // Get element within shadow DOM
  public WebElement getShadowElement(String hostSelector, String shadowSelector) {
    WebElement host = driver.findElement(By.cssSelector(hostSelector));
    WebElement shadowRoot = (WebElement) ((JavascriptExecutor) driver)
      .executeScript("return arguments[0].shadowRoot", host);
    
    return shadowRoot.findElement(By.cssSelector(shadowSelector));
  }
  
  // Deep shadow DOM traversal
  public WebElement getDeepShadowElement(String... selectors) {
    JavascriptExecutor js = (JavascriptExecutor) driver;
    
    String script = "function getShadowElement(selectors) {" +
      "  let element = document.querySelector(selectors[0]);" +
      "  for (let i = 1; i < selectors.length; i++) {" +
      "    element = element.shadowRoot.querySelector(selectors[i]);" +
      "  }" +
      "  return element;" +
      "}" +
      "return getShadowElement(arguments[0]);";
    
    return (WebElement) js.executeScript(script, (Object) selectors);
  }
  
  // Fill shadow DOM input
  public void fillShadowInput(String hostSelector, String inputSelector, String text) {
    WebElement input = getShadowElement(hostSelector, inputSelector);
    JavascriptExecutor js = (JavascriptExecutor) driver;
    js.executeScript("arguments[0].value = arguments[1]; " +
                     "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
                     input, text);
  }
  
  // Click shadow element
  public void clickShadowElement(String hostSelector, String elementSelector) {
    WebElement element = getShadowElement(hostSelector, elementSelector);
    JavascriptExecutor js = (JavascriptExecutor) driver;
    js.executeScript("arguments[0].click();", element);
  }
}

// Test shadow DOM
@Test
public void testShadowDOMElements() {
  ShadowDOMHelper shadowHelper = new ShadowDOMHelper(driver);
  
  driver.get("https://example.com");
  
  // Interact with shadow elements
  shadowHelper.fillShadowInput("#host-element", "input", "test value");
  shadowHelper.clickShadowElement("#host-element", "button");
  
  // Verify
  WebElement result = shadowHelper.getShadowElement("#host-element", ".result");
  assertTrue(result.getText().contains("expected"));
}
```

---

### Q28. How do you handle browser tabs and windows management in Selenium?
**Answer:**
```java
public class WindowHandlingHelper {
  private WebDriver driver;
  
  public WindowHandlingHelper(WebDriver driver) {
    this.driver = driver;
  }
  
  // Switch between windows
  public void switchToWindow(int windowIndex) {
    List<String> windowHandles = new ArrayList<>(driver.getWindowHandles());
    driver.switchTo().window(windowHandles.get(windowIndex));
  }
  
  // Switch by window title
  public void switchToWindowByTitle(String title) {
    for (String handle : driver.getWindowHandles()) {
      driver.switchTo().window(handle);
      if (driver.getTitle().equals(title)) {
        return;
      }
    }
  }
  
  // Open new tab
  public void openNewTab() {
    ((JavascriptExecutor) driver).executeScript("window.open('about:blank', '_blank');");
  }
  
  // Close specific window
  public void closeWindow(int windowIndex) {
    List<String> windowHandles = new ArrayList<>(driver.getWindowHandles());
    String currentHandle = driver.getWindowHandle();
    driver.switchTo().window(windowHandles.get(windowIndex));
    driver.close();
    driver.switchTo().window(currentHandle);
  }
  
  // Get all window titles
  public List<String> getAllWindowTitles() {
    List<String> titles = new ArrayList<>();
    for (String handle : driver.getWindowHandles()) {
      driver.switchTo().window(handle);
      titles.add(driver.getTitle());
    }
    return titles;
  }
  
  // Handle pop-ups
  public void handlePopUp() {
    String parentWindow = driver.getWindowHandle();
    
    for (String handle : driver.getWindowHandles()) {
      driver.switchTo().window(handle);
      if (!handle.equals(parentWindow)) {
        driver.close();
      }
    }
    
    driver.switchTo().window(parentWindow);
  }
}

@Test
public void testWindowHandling() {
  WindowHandlingHelper windowHelper = new WindowHandlingHelper(driver);
  
  driver.get("https://example.com");
  String parentWindow = driver.getWindowHandle();
  
  // Open new window
  driver.findElement(By.xpath("//a[@target='_blank']")).click();
  windowHelper.switchToWindow(1);  // Switch to new window
  
  // Do something in new window
  assertTrue(driver.getTitle().contains("New Page"));
  driver.close();
  
  // Back to parent
  driver.switchTo().window(parentWindow);
  assertTrue(driver.getTitle().contains("Main Page"));
}
```

---

### Q29. How do you implement Docker and containerization for test automation?
**Answer:**
```dockerfile
# Dockerfile for Selenium tests
FROM maven:3.8-openjdk-11

# Install dependencies
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-browser-l10n \
    chromium-codecs-ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project
COPY . .

# Run tests
CMD ["mvn", "test", "-Dbrowser=chrome", "-Dheadless=true"]
```

```yaml
# docker-compose.yml for Selenium Grid
version: '3.8'

services:
  selenium-hub:
    image: selenium/hub:latest
    container_name: selenium-hub
    ports:
      - "4444:4444"
      - "4442:4442"
      - "4443:4443"
    environment:
      SE_SESSION_REQUEST_TIMEOUT: 300
      SE_SESSION_RETRY_INTERVAL: 5
  
  chrome:
    image: selenium/node-chrome:latest
    container_name: chrome-node
    depends_on:
      - selenium-hub
    ports:
      - "7900:7900"
    environment:
      SE_EVENT_BUS_HOST: selenium-hub
      SE_EVENT_BUS_PUBLISH_PORT: 4442
      SE_EVENT_BUS_SUBSCRIBE_PORT: 4443
      SE_NODE_MAX_SESSIONS: 3
      SE_VNC_NO_VNCDISPLAY: 1
  
  firefox:
    image: selenium/node-firefox:latest
    container_name: firefox-node
    depends_on:
      - selenium-hub
    ports:
      - "7901:7900"
    environment:
      SE_EVENT_BUS_HOST: selenium-hub
      SE_EVENT_BUS_PUBLISH_PORT: 4442
      SE_EVENT_BUS_SUBSCRIBE_PORT: 4443
  
  test-runner:
    build: .
    container_name: test-runner
    depends_on:
      - selenium-hub
      - chrome
      - firefox
    environment:
      SELENIUM_HUB_URL: http://selenium-hub:4444
      CHROME_URL: http://chrome-node:4444
      FIREFOX_URL: http://firefox-node:4444
    volumes:
      - ./target:/app/target
    command: mvn test
```

```java
// Connect to Selenium Grid
public class GridTestSetup {
  public static WebDriver getRemoteDriver(String browserName, String hubUrl) 
      throws MalformedURLException {
    DesiredCapabilities capabilities = new DesiredCapabilities();
    
    switch (browserName.toLowerCase()) {
      case "chrome":
        capabilities = DesiredCapabilities.chrome();
        break;
      case "firefox":
        capabilities = DesiredCapabilities.firefox();
        break;
    }
    
    return new RemoteWebDriver(new URL(hubUrl + "/wd/hub"), capabilities);
  }
}

// Test with Grid
@Test
public void testWithGrid() throws MalformedURLException {
  String hubUrl = "http://localhost:4444";
  WebDriver driver = GridTestSetup.getRemoteDriver("chrome", hubUrl);
  
  try {
    driver.get("https://example.com");
    // Test code
  } finally {
    driver.quit();
  }
}
```

---

### Q30. How do you implement continuous monitoring and test analytics?
**Answer:**
```java
public class TestAnalytics {
  private String testName;
  private long startTime;
  private long endTime;
  private boolean passed;
  private String errorMessage;
  
  public void startTest(String name) {
    this.testName = name;
    this.startTime = System.currentTimeMillis();
  }
  
  public void endTest(boolean status, String error) {
    this.endTime = System.currentTimeMillis();
    this.passed = status;
    this.errorMessage = error;
  }
  
  public long getDuration() {
    return endTime - startTime;
  }
  
  public void sendToAnalytics() {
    String payload = "{\n" +
      "  \"testName\": \"" + testName + "\",\n" +
      "  \"status\": \"" + (passed ? "PASSED" : "FAILED") + "\",\n" +
      "  \"duration\": " + getDuration() + ",\n" +
      "  \"timestamp\": " + System.currentTimeMillis() + ",\n" +
      "  \"error\": \"" + (errorMessage != null ? errorMessage : "") + "\"\n" +
      "}";
    
    try {
      RestAssured.given()
        .contentType(ContentType.JSON)
        .body(payload)
        .post("https://analytics-server/api/test-results");
    } catch (Exception e) {
      System.out.println("Failed to send analytics: " + e.getMessage());
    }
  }
}

// Usage in listener
@Listeners(AnalyticsListener.class)
public class AnalyticsTests {
  private TestAnalytics analytics;
  
  @BeforeMethod
  public void setUp() {
    analytics = new TestAnalytics();
  }
  
  @Test
  public void testExample() {
    analytics.startTest("testExample");
    try {
      // Test code
      analytics.endTest(true, null);
    } catch (Exception e) {
      analytics.endTest(false, e.getMessage());
      throw e;
    } finally {
      analytics.sendToAnalytics();
    }
  }
}
```

---

## Advanced Architecture & Optimization (Q31-Q40)

### Q31. How do you implement Selenium Grid 4 for distributed testing? Explain architecture.
**Answer:**
Selenium Grid 4 enables parallel test execution across multiple machines and browsers. 

Key Architecture Components:
- **Router**: Entry point for test requests
- **Distributor**: Assigns tests to available nodes
- **Session Map**: Tracks active sessions
- **Node**: Actual browser instance
- **Event Bus**: Handles communication

```yaml
# Detailed Grid 4 setup
version: '3.8'

services:
  # Event Bus - Central communication hub
  event_bus:
    image: selenium/event-bus:latest
    container_name: selenium-event-bus
    ports:
      - "5557:5557"
      - "5558:5558"
    environment:
      SE_GRID_HUB_HOST: event_bus
  
  # Session Map - Tracks sessions
  session-map:
    image: selenium/sessions:latest
    container_name: selenium-session-map
    ports:
      - "5559:5559"
    depends_on:
      - event_bus
    environment:
      SE_EVENT_BUS_HOST: event_bus
      SE_EVENT_BUS_PUBLISH_PORT: 5557
      SE_EVENT_BUS_SUBSCRIBE_PORT: 5558
  
  # Session Queue
  session-queue:
    image: selenium/session-queue:latest
    container_name: selenium-session-queue
    ports:
      - "5559:5559"
    depends_on:
      - event_bus
    environment:
      SE_EVENT_BUS_HOST: event_bus
      SE_EVENT_BUS_PUBLISH_PORT: 5557
      SE_EVENT_BUS_SUBSCRIBE_PORT: 5558
  
  # Router - Entry point
  router:
    image: selenium/router:latest
    container_name: selenium-router
    ports:
      - "4444:4444"
    depends_on:
      - event_bus
      - session-map
      - session-queue
    environment:
      SE_GRID_PUBLIC_URL: http://localhost:4444
      SE_SESSION_MAP_HOST: session-map
      SE_SESSION_MAP_PORT: 5559
      SE_SESSION_QUEUE_HOST: session-queue
      SE_EVENT_BUS_HOST: event_bus
      SE_EVENT_BUS_PUBLISH_PORT: 5557
      SE_EVENT_BUS_SUBSCRIBE_PORT: 5558
  
  # Chrome Nodes
  chrome1:
    image: selenium/node-chrome:latest
    container_name: chrome-node-1
    depends_on:
      - event_bus
    ports:
      - "7900:7900"
    environment:
      SE_EVENT_BUS_HOST: event_bus
      SE_EVENT_BUS_PUBLISH_PORT: 5557
      SE_EVENT_BUS_SUBSCRIBE_PORT: 5558
      SE_NODE_MAX_SESSIONS: 3
      SE_NODE_SESSION_TIMEOUT: 300
      SE_VNC_NO_VNCDISPLAY: 1
  
  chrome2:
    image: selenium/node-chrome:latest
    container_name: chrome-node-2
    depends_on:
      - event_bus
    ports:
      - "7901:7900"
    environment:
      SE_EVENT_BUS_HOST: event_bus
      SE_EVENT_BUS_PUBLISH_PORT: 5557
      SE_EVENT_BUS_SUBSCRIBE_PORT: 5558
      SE_NODE_MAX_SESSIONS: 3
  
  # Firefox Nodes
  firefox1:
    image: selenium/node-firefox:latest
    container_name: firefox-node-1
    depends_on:
      - event_bus
    ports:
      - "7902:7900"
    environment:
      SE_EVENT_BUS_HOST: event_bus
      SE_EVENT_BUS_PUBLISH_PORT: 5557
      SE_EVENT_BUS_SUBSCRIBE_PORT: 5558
      SE_NODE_MAX_SESSIONS: 2
```

```java
// Connect to Grid 4
public class Grid4Setup {
  public static WebDriver getGridDriver(String browser) throws MalformedURLException {
    DesiredCapabilities capabilities = new DesiredCapabilities();
    
    switch (browser.toLowerCase()) {
      case "chrome":
        capabilities.setBrowserName("chrome");
        capabilities.setCapability("browserVersion", "latest");
        capabilities.setCapability("platformName", "linux");
        break;
      case "firefox":
        capabilities.setBrowserName("firefox");
        capabilities.setCapability("browserVersion", "latest");
        break;
    }
    
    return new RemoteWebDriver(new URL("http://localhost:4444"), capabilities);
  }
}

// Parallel test execution
@RunWith(Parameterized.class)
public class ParallelGridTests {
  private WebDriver driver;
  private String browser;
  
  public ParallelGridTests(String browser) {
    this.browser = browser;
  }
  
  @Parameterized.Parameters(name = "{index}: {0}")
  public static Collection<String> browsers() {
    return Arrays.asList("chrome", "firefox", "chrome", "firefox");
  }
  
  @Before
  public void setUp() throws MalformedURLException {
    driver = Grid4Setup.getGridDriver(browser);
  }
  
  @After
  public void tearDown() {
    if (driver != null) {
      driver.quit();
    }
  }
  
  @Test
  public void testLoginParallel() {
    driver.get("https://example.com/login");
    // Test implementation
  }
}
```

---

### Q32. How do you implement custom wait conditions and advanced synchronization?
**Answer:**
```java
public class CustomWaits {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public CustomWaits(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Wait for AJAX to complete
  public void waitForAjax() {
    wait.until(driver -> {
      JavascriptExecutor js = (JavascriptExecutor) driver;
      Long activeAjaxRequests = (Long) js.executeScript(
        "return (typeof jQuery != 'undefined') ? jQuery.active : 0"
      );
      return activeAjaxRequests == 0;
    });
  }
  
  // Wait for Angular to be ready
  public void waitForAngular() {
    wait.until(driver -> {
      JavascriptExecutor js = (JavascriptExecutor) driver;
      try {
        Boolean isReady = (Boolean) js.executeScript(
          "return window.getAllAngularTestabilities().findIndex(x => !x.isStable()) === -1"
        );
        return isReady != null && isReady;
      } catch (Exception e) {
        return false;
      }
    });
  }
  
  // Wait for React to be ready
  public void waitForReact() {
    wait.until(driver -> {
      JavascriptExecutor js = (JavascriptExecutor) driver;
      try {
        Boolean isPending = (Boolean) js.executeScript(
          "return window.reactDevTools ? window.reactDevTools.isPending() : false"
        );
        return !isPending;
      } catch (Exception e) {
        return true;
      }
    });
  }
  
  // Wait for element to have text
  public void waitForElementText(By locator, String text) {
    wait.until(ExpectedConditions.textToBePresentInElementLocated(locator, text));
  }
  
  // Custom: Wait for element visibility with retry
  public WebElement waitForElementWithRetry(By locator, int maxRetries) {
    for (int i = 0; i < maxRetries; i++) {
      try {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
      } catch (TimeoutException e) {
        if (i < maxRetries - 1) {
          sleep(500);
          ((JavascriptExecutor) driver).executeScript("location.reload();");
        }
      }
    }
    throw new TimeoutException("Element not found after retries");
  }
  
  // Wait for URL pattern
  public void waitForUrlPattern(Pattern pattern) {
    wait.until(driver -> pattern.matcher(driver.getCurrentUrl()).matches());
  }
  
  // Wait for JavaScript to complete
  public void waitForJavaScript() {
    wait.until(driver -> {
      JavascriptExecutor js = (JavascriptExecutor) driver;
      String readyState = (String) js.executeScript("return document.readyState");
      return "complete".equals(readyState);
    });
  }
  
  // Wait for document ready and no loading spinners
  public void waitForPageReady() {
    waitForJavaScript();
    wait.until(ExpectedConditions.invisibilityOfElementLocated(By.className("loader")));
  }
  
  private void sleep(long ms) {
    try {
      Thread.sleep(ms);
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
    }
  }
}

// Usage
@Test
public void testWithCustomWait() {
  CustomWaits customWaits = new CustomWaits(driver);
  
  driver.get("https://example.com");
  customWaits.waitForAjax();
  customWaits.waitForPageReady();
  
  // Test continues
}
```

---

### Q33. How do you implement test parameterization and configuration management?
**Answer:**
```java
// Configuration management
public class TestConfig {
  private Properties properties;
  private static TestConfig instance;
  
  private TestConfig() {
    properties = new Properties();
    try {
      String env = System.getProperty("env", "dev");
      FileInputStream file = new FileInputStream("src/test/resources/config_" + env + ".properties");
      properties.load(file);
      file.close();
    } catch (IOException e) {
      throw new RuntimeException("Failed to load configuration", e);
    }
  }
  
  public static TestConfig getInstance() {
    if (instance == null) {
      instance = new TestConfig();
    }
    return instance;
  }
  
  public String getProperty(String key) {
    return properties.getProperty(key);
  }
  
  public String getProperty(String key, String defaultValue) {
    return properties.getProperty(key, defaultValue);
  }
}

// Test parameterization with data provider
public class ParameterizedTestData {
  
  public static Object[][] loginTestData() {
    return new Object[][] {
      {"validUser@test.com", "validPassword", true, "dashboard"},
      {"invalidUser@test.com", "wrongPassword", false, "error"},
      {"", "", false, "error"},
      {"user@test.com", "", false, "error"}
    };
  }
  
  public static Object[][] searchTestData() {
    return new Object[][] {
      {"selenium", 100, true},
      {"playwright", 50, true},
      {"", 0, false}
    };
  }
}

// Test with parameterization
public class ParameterizedTests {
  private WebDriver driver;
  
  @BeforeMethod
  public void setUp() {
    driver = new ChromeDriver();
  }
  
  @Test(dataProvider = "loginData", dataProviderClass = ParameterizedTestData.class)
  public void testLogin(String email, String password, boolean shouldSucceed, 
                        String expectedElement) {
    String baseUrl = TestConfig.getInstance().getProperty("base.url");
    driver.get(baseUrl + "/login");
    
    driver.findElement(By.id("email")).sendKeys(email);
    driver.findElement(By.id("password")).sendKeys(password);
    driver.findElement(By.id("login-btn")).click();
    
    WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    
    if (shouldSucceed) {
      wait.until(ExpectedConditions.presenceOfElementLocated(By.id(expectedElement)));
      assertTrue(driver.getCurrentUrl().contains(expectedElement));
    } else {
      wait.until(ExpectedConditions.presenceOfElementLocated(By.id(expectedElement)));
      assertTrue(driver.getPageSource().contains(expectedElement));
    }
  }
  
  @AfterMethod
  public void tearDown() {
    driver.quit();
  }
}

// config_dev.properties
/*
base.url=http://localhost:8080
browser=chrome
implicit.wait=10
explicit.wait=15
admin.username=admin
admin.password=admin123
*/

// config_prod.properties
/*
base.url=https://production.example.com
browser=chrome
implicit.wait=15
explicit.wait=20
admin.username=prodadmin
admin.password=prodpass123
*/
```

---

### Q34. How do you handle dynamic element locators and XPath/CSS selector best practices?
**Answer:**
```java
public class RobustLocators {
  
  // Preference order for locators
  public static class LocatorStrategy {
    // 1. ID (most stable)
    public static By byId(String id) {
      return By.id(id);
    }
    
    // 2. Class name
    public static By byClassName(String className) {
      return By.className(className);
    }
    
    // 3. CSS Selector (more reliable than XPath)
    public static By byCss(String selector) {
      return By.cssSelector(selector);
    }
    
    // 4. XPath (last resort, less stable)
    public static By byXpath(String xpath) {
      return By.xpath(xpath);
    }
    
    // Attribute-based (stable)
    public static By byAttribute(String attribute, String value) {
      return By.cssSelector("[" + attribute + "='" + value + "']");
    }
    
    // Data attributes (very stable)
    public static By byDataAttribute(String dataAttr, String value) {
      return By.cssSelector("[data-" + dataAttr + "='" + value + "']");
    }
  }
  
  // Dynamic locators with partial matches
  public static class DynamicLocators {
    
    // XPath with partial text
    public static By buttonByPartialText(String text) {
      return By.xpath("//button[contains(text(), '" + text + "')]");
    }
    
    // CSS with attribute contains
    public static By inputByPlaceholder(String placeholder) {
      return By.cssSelector("input[placeholder*='" + placeholder + "']");
    }
    
    // XPath with starts-with
    public static By elementByIdStart(String idStart) {
      return By.xpath("//*[starts-with(@id, '" + idStart + "')]");
    }
    
    // CSS with descendant combinator
    public static By elementInContainer(String containerClass, String elementTag) {
      return By.cssSelector("." + containerClass + " > " + elementTag);
    }
    
    // XPath with preceding sibling
    public static By inputAfterLabel(String labelText) {
      return By.xpath("//label[text()='" + labelText + "']/following-sibling::input");
    }
    
    // Resilient XPath with multiple attributes
    public static By inputWithMultipleAttributes(String type, String name) {
      return By.xpath("//input[@type='" + type + "'][@name='" + name + "']");
    }
  }
}

// Usage
@Test
public void testRobustLocators() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com");
  
  // Most stable: ID
  driver.findElement(RobustLocators.LocatorStrategy.byId("submit-button")).click();
  
  // Data attributes (very stable)
  driver.findElement(RobustLocators.LocatorStrategy.byDataAttribute("testid", "login-form"))
    .isDisplayed();
  
  // Dynamic locators for changing IDs
  driver.findElement(RobustLocators.DynamicLocators.elementByIdStart("btn_"))
    .click();
  
  // Resilient to text changes
  driver.findElement(RobustLocators.DynamicLocators.buttonByPartialText("Sign"))
    .click();
  
  driver.quit();
}
```

Best Practices:
1. Prefer stable locators: ID → Data Attributes → CSS → XPath
2. Avoid index-based XPath (nth-child)
3. Use partial matching for dynamic text
4. Keep locators simple and maintainable
5. Prioritize business logic over technical implementation

---

### Q35. How do you implement keyboard interactions and advanced mouse actions?
**Answer:**
```java
public class AdvancedInteractions {
  private WebDriver driver;
  private Actions actions;
  private WebDriverWait wait;
  
  public AdvancedInteractions(WebDriver driver) {
    this.driver = driver;
    this.actions = new Actions(driver);
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Keyboard interactions
  public void typeWithSpecialKeys(By locator, String text) {
    actions.click(driver.findElement(locator))
      .sendKeys(text)
      .sendKeys(Keys.TAB)
      .perform();
  }
  
  public void selectAllAndDelete(By locator) {
    actions.click(driver.findElement(locator))
      .keyDown(Keys.CONTROL)
      .sendKeys("a")
      .keyUp(Keys.CONTROL)
      .sendKeys(Keys.DELETE)
      .perform();
  }
  
  public void submitForm(By locator) {
    actions.click(driver.findElement(locator))
      .sendKeys(Keys.ENTER)
      .perform();
  }
  
  // Mouse interactions
  public void hoverOverElement(By locator) {
    WebElement element = driver.findElement(locator);
    actions.moveToElement(element).perform();
    wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("tooltip")));
  }
  
  public void doubleClick(By locator) {
    actions.doubleClick(driver.findElement(locator)).perform();
  }
  
  public void rightClick(By locator) {
    actions.contextClick(driver.findElement(locator)).perform();
  }
  
  // Drag and drop
  public void dragAndDrop(By source, By target) {
    WebElement sourceElement = driver.findElement(source);
    WebElement targetElement = driver.findElement(target);
    actions.dragAndDrop(sourceElement, targetElement).perform();
  }
  
  // Drag by offset
  public void dragByOffset(By locator, int xOffset, int yOffset) {
    WebElement element = driver.findElement(locator);
    actions.dragAndDropBy(element, xOffset, yOffset).perform();
  }
  
  // Slider interaction
  public void moveSlider(By sliderLocator, int offset) {
    WebElement slider = driver.findElement(sliderLocator);
    actions.clickAndHold(slider)
      .moveByOffset(offset, 0)
      .release()
      .perform();
  }
  
  // Multi-key combination
  public void performKeyCombo(By locator, Keys... keys) {
    actions.click(driver.findElement(locator));
    for (Keys key : keys) {
      actions.keyDown(key);
    }
    actions.sendKeys("C");
    for (Keys key : keys) {
      actions.keyUp(key);
    }
    actions.perform();
  }
}

// Usage
@Test
public void testAdvancedInteractions() {
  AdvancedInteractions advanced = new AdvancedInteractions(driver);
  
  // Hover and click
  advanced.hoverOverElement(By.id("menu-item"));
  advanced.doubleClick(By.id("element"));
  
  // Drag and drop
  advanced.dragAndDrop(By.id("source"), By.id("target"));
  
  // Keyboard combinations
  advanced.performKeyCombo(By.id("input"), Keys.CONTROL);
}
```

---

### Q36. How do you implement screenshot capture and visual debugging?
**Answer:**
```java
public class ScreenshotManager {
  private WebDriver driver;
  private String screenshotDir = "target/screenshots/";
  
  public ScreenshotManager(WebDriver driver) {
    this.driver = driver;
    new File(screenshotDir).mkdirs();
  }
  
  // Simple screenshot
  public String captureScreenshot(String filename) throws IOException {
    File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
    String path = screenshotDir + filename + "_" + System.currentTimeMillis() + ".png";
    Files.copy(src.toPath(), Paths.get(path));
    return path;
  }
  
  // Full-page screenshot
  public String captureFullPage(String filename) throws IOException {
    Screenshot screenshot = new AShot()
      .shootingStrategy(new ViewportPastingStrategy(1000))
      .takeScreenshot(driver);
    
    String path = screenshotDir + filename + "_fullpage_" + System.currentTimeMillis() + ".png";
    ImageIO.write(screenshot.getImage(), "png", new File(path));
    return path;
  }
  
  // Element screenshot
  public String captureElement(String filename, By locator) throws IOException {
    WebElement element = driver.findElement(locator);
    File screenshot = element.getScreenshotAs(OutputType.FILE);
    String path = screenshotDir + filename + "_element_" + System.currentTimeMillis() + ".png";
    Files.copy(screenshot.toPath(), Paths.get(path));
    return path;
  }
  
  // Highlighted element screenshot
  public String captureWithHighlight(String filename, By locator) throws IOException {
    WebElement element = driver.findElement(locator);
    
    // Highlight element
    ((JavascriptExecutor) driver).executeScript(
      "arguments[0].style.border='3px solid red'", element);
    
    String path = captureScreenshot(filename + "_highlighted");
    
    // Remove highlight
    ((JavascriptExecutor) driver).executeScript(
      "arguments[0].style.border=''", element);
    
    return path;
  }
}

// Listener for automatic screenshots
@Listeners(ScreenshotListener.class)
public class ScreenshotTests {
  protected WebDriver driver;
  protected ScreenshotManager screenshotManager;
  
  @BeforeMethod
  public void setUp() {
    driver = new ChromeDriver();
    screenshotManager = new ScreenshotManager(driver);
  }
  
  @Test
  public void testExample() throws IOException {
    driver.get("https://example.com");
    screenshotManager.captureScreenshot("step1_homepage");
    
    driver.findElement(By.id("login-link")).click();
    screenshotManager.captureScreenshot("step2_login_page");
  }
}

// Screenshot listener
public class ScreenshotListener implements ITestListener {
  @Override
  public void onTestFailure(ITestResult result) {
    WebDriver driver = ((WebDriverTestBase) result.getInstance()).driver;
    ScreenshotManager manager = new ScreenshotManager(driver);
    
    try {
      manager.captureScreenshot("failure_" + result.getName());
      System.out.println("Screenshot captured for failed test");
    } catch (IOException e) {
      System.out.println("Failed to capture screenshot: " + e.getMessage());
    }
  }
}
```

---

### Q37. How do you implement fluent test patterns and builder patterns?
**Answer:**
```java
// Fluent Page Object Pattern
public class LoginPageFluent {
  private WebDriver driver;
  private WebDriverWait wait;
  
  private By emailInput = By.id("email");
  private By passwordInput = By.id("password");
  private By loginButton = By.id("login-btn");
  
  public LoginPageFluent(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  public LoginPageFluent navigateTo(String url) {
    driver.get(url);
    return this;
  }
  
  public LoginPageFluent enterEmail(String email) {
    wait.until(ExpectedConditions.visibilityOfElementLocated(emailInput))
      .sendKeys(email);
    return this;
  }
  
  public LoginPageFluent enterPassword(String password) {
    driver.findElement(passwordInput).sendKeys(password);
    return this;
  }
  
  public DashboardPageFluent clickLogin() {
    driver.findElement(loginButton).click();
    return new DashboardPageFluent(driver);
  }
  
  public LoginPageFluent clearEmail() {
    driver.findElement(emailInput).clear();
    return this;
  }
}

// Usage
@Test
public void testFluentPattern() {
  LoginPageFluent login = new LoginPageFluent(driver);
  
  login.navigateTo("https://example.com/login")
    .enterEmail("user@test.com")
    .enterPassword("password123")
    .clickLogin()
    .verifyDashboardLoaded();
}

// Builder Pattern
public class TestDataBuilder {
  private String email;
  private String password;
  private String firstName;
  private String lastName;
  private boolean isAdmin;
  
  public TestDataBuilder withEmail(String email) {
    this.email = email;
    return this;
  }
  
  public TestDataBuilder withPassword(String password) {
    this.password = password;
    return this;
  }
  
  public TestDataBuilder withFirstName(String firstName) {
    this.firstName = firstName;
    return this;
  }
  
  public TestDataBuilder withLastName(String lastName) {
    this.lastName = lastName;
    return this;
  }
  
  public TestDataBuilder asAdmin() {
    this.isAdmin = true;
    return this;
  }
  
  public TestData build() {
    return new TestData(email, password, firstName, lastName, isAdmin);
  }
}

// Usage
@Test
public void testBuilderPattern() {
  TestData user = new TestDataBuilder()
    .withEmail("user@test.com")
    .withPassword("pass123")
    .withFirstName("John")
    .withLastName("Doe")
    .asAdmin()
    .build();
  
  // Use user object in test
}
```

---

### Q38. How do you handle certificate and SSL errors in Selenium?
**Answer:**
```java
public class SSLHandling {
  
  public static WebDriver setupChromeWithSSLBypass() {
    ChromeOptions options = new ChromeOptions();
    options.setAcceptInsecureCerts(true);  // Accept SSL certificates
    options.addArguments("--allow-insecure-localhost");
    options.addArguments("--ignore-certificate-errors");
    
    return new ChromeDriver(options);
  }
  
  public static WebDriver setupFirefoxWithSSLBypass() {
    FirefoxOptions options = new FirefoxOptions();
    options.setAcceptInsecureCerts(true);
    options.setPreference("security.ssl.allow_unreliable_default_config", true);
    
    return new FirefoxDriver(options);
  }
  
  public static WebDriver setupEdgeWithSSLBypass() {
    EdgeOptions options = new EdgeOptions();
    options.setAcceptInsecureCerts(true);
    options.addArguments("--allow-insecure-localhost");
    
    return new EdgeDriver(options);
  }
}

// Usage
@Test
public void testWithSSLBypass() {
  WebDriver driver = SSLHandling.setupChromeWithSSLBypass();
  
  try {
    driver.get("https://self-signed-cert-site.example.com");
    assertTrue(driver.getTitle().contains("Expected Title"));
  } finally {
    driver.quit();
  }
}
```

---

### Q39. How do you implement proper error logging and exception handling?
**Answer:**
```java
public class TestLogger {
  private static Logger logger = LoggerFactory.getLogger(TestLogger.class);
  
  public static void logInfo(String message) {
    logger.info(message);
  }
  
  public static void logWarning(String message) {
    logger.warn(message);
  }
  
  public static void logError(String message, Exception e) {
    logger.error(message, e);
  }
  
  public static void logDebug(String message) {
    logger.debug(message);
  }
}

// Custom exception handling
public class ElementNotFindException extends RuntimeException {
  public ElementNotFindException(By locator, WebDriver driver) {
    super("Element not found: " + locator + ". Current URL: " + 
          driver.getCurrentUrl() + ". Page source length: " + 
          driver.getPageSource().length());
  }
}

public class TestBase {
  protected WebDriver driver;
  protected WebDriverWait wait;
  protected Logger logger = LoggerFactory.getLogger(this.getClass());
  
  @BeforeMethod
  public void setUp() {
    try {
      driver = new ChromeDriver();
      wait = new WebDriverWait(driver, Duration.ofSeconds(10));
      logger.info("Test setup completed");
    } catch (Exception e) {
      logger.error("Failed to setup test", e);
      throw new RuntimeException("Test setup failed", e);
    }
  }
  
  @AfterMethod
  public void tearDown(ITestResult result) {
    try {
      if (result.getStatus() == ITestResult.FAILURE) {
        logger.error("Test failed: " + result.getName());
        logger.error("Failure reason: " + result.getThrowable().getMessage());
        
        // Capture screenshot
        try {
          File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
          String path = "target/screenshots/failure_" + result.getName() + ".png";
          Files.copy(src.toPath(), Paths.get(path));
          logger.error("Screenshot saved: " + path);
        } catch (IOException e) {
          logger.error("Failed to capture screenshot", e);
        }
      } else {
        logger.info("Test passed: " + result.getName());
      }
    } finally {
      if (driver != null) {
        try {
          driver.quit();
          logger.info("Driver closed");
        } catch (Exception e) {
          logger.error("Error closing driver", e);
        }
      }
    }
  }
  
  protected void handleTestException(String message, Exception e) {
    logger.error(message, e);
    try {
      File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
      Files.copy(src.toPath(), Paths.get("target/screenshots/error.png"));
    } catch (IOException ioe) {
      logger.error("Failed to capture screenshot", ioe);
    }
    throw new AssertionError(message, e);
  }
}
```

---

### Q40. How do you implement performance optimization in test automation?
**Answer:**
Test optimization strategies:

1. **Parallel Execution**
```java
@RunWith(Parameterized.class)
public class ParallelTests {
  // Tests run in parallel across multiple threads
}
```

2. **Resource Reuse**
```java
public class SharedWebDriverPool {
  private static ThreadLocal<WebDriver> driverPool = new ThreadLocal<>();
  
  public static WebDriver getDriver() {
    if (driverPool.get() == null) {
      driverPool.set(new ChromeDriver());
    }
    return driverPool.get();
  }
  
  public static void quitDriver() {
    WebDriver driver = driverPool.get();
    if (driver != null) {
      driver.quit();
      driverPool.remove();
    }
  }
}
```

3. **Smart Waits**
- Use explicit waits instead of implicit waits
- Minimize wait times with optimal conditions
- Avoid Thread.sleep()

4. **Test Isolation**
- Use test data cleanup
- Implement proper setup/teardown
- Avoid test interdependencies

5. **Code Optimization**
- Use Page Object Model
- Reuse common methods
- Minimize DOM queries

---

This comprehensive coverage provides Q16-Q40. Shall I continue with Q41-Q50 for Mobile Testing, DevOps Integration, and additional advanced topics?
```

This covers Q16-Q20. Remaining Q21-Q50 would cover additional topics like mobile testing, visual regression, accessibility testing, advanced reporting, and more framework patterns.

Would you like me to continue with Q21-Q50?


## Final Advanced Topics (Q41-Q50)

### Q41. How do you implement cloud-based testing with BrowserStack/Sauce Labs?
**Answer:**
Cloud-based testing platforms allow you to test on real browsers and devices in the cloud without local infrastructure.

`java
public class CloudTestingSetup {
  public static WebDriver setupBrowserStack() throws MalformedURLException {
    DesiredCapabilities caps = new DesiredCapabilities();
    caps.setCapability("os", "Windows");
    caps.setCapability("browser", "Chrome");
    caps.setCapability("browser_version", "latest");
    
    String username = System.getenv("BROWSERSTACK_USERNAME");
    String accessKey = System.getenv("BROWSERSTACK_ACCESS_KEY");
    String url = "https://" + username + ":" + accessKey + "@hub.browserstack.com/wd/hub";
    
    return new RemoteWebDriver(new URL(url), caps);
  }
}
`

### Q42. How do you implement self-healing tests with automatic locator recovery?
**Answer:**
Self-healing tests maintain multiple locators for elements and automatically try alternatives when one fails, reducing test flakiness.

`java
public class SelfHealingFramework {
  private Map<String, List<By>> elementLocators = new HashMap<>();
  
  public void selfHealingClick(String elementKey) {
    for (By locator : elementLocators.get(elementKey)) {
      try {
        driver.findElement(locator).click();
        return;
      } catch (NoSuchElementException e) {
        continue;
      }
    }
    throw new ElementNotFindException("Element not found with any locator");
  }
}
`

### Q43. How do you implement test data management and cleanup strategies?
**Answer:**
Proper test data management ensures tests are isolated, repeatable, and don't pollute the system.

`java
public class TestDataManager {
  private List<String> createdResources = new ArrayList<>();
  
  public String createTestUser(String email) {
    String userId = RestAssured.given()
      .post("/api/users")
      .jsonPath().getString("id");
    createdResources.add("user:" + userId);
    return userId;
  }
  
  public void cleanupAll() {
    for (String resource : createdResources) {
      RestAssured.delete("/api/" + resource.split(":")[0] + "/" + resource.split(":")[1]);
    }
    createdResources.clear();
  }
}
`

### Q44. How do you implement environment-specific testing and configuration management?
**Answer:**
Environment-specific configs allow running the same tests against different environments (dev, staging, prod) without code changes.

`java
public class EnvironmentConfig {
  private Properties props = new Properties();
  
  public EnvironmentConfig(String env) {
    try {
      props.load(new FileInputStream("config_" + env + ".properties"));
    } catch (IOException e) {
      throw new RuntimeException("Config load failed", e);
    }
  }
  
  public String getBaseUrl() { return props.getProperty("base.url"); }
  public int getTimeout() { return Integer.parseInt(props.getProperty("timeout")); }
}
`

### Q45. How do you implement feature flagging in automation tests?
**Answer:**
Feature flags allow conditional test execution based on feature enablement status, supporting A/B testing and gradual rollouts.

`java
public class FeatureFlagTesting {
  public boolean isFeatureEnabled(String featureName) {
    return RestAssured.get("/api/features/" + featureName)
      .jsonPath().getBoolean("enabled");
  }
  
  @Test
  public void testNewFeature() {
    if (isFeatureEnabled("new_dashboard")) {
      driver.get(baseUrl + "/new-dashboard");
    } else {
      driver.get(baseUrl + "/dashboard");
    }
  }
}
`

### Q46. How do you implement multi-viewport/responsive testing?
**Answer:**
Testing across different viewport sizes ensures responsive design works across all devices.

`java
public class ResponsiveTests {
  private static final String[] VIEWPORTS = {"320x568", "768x1024", "1920x1080"};
  
  @Test(dataProvider = "viewports")
  public void testResponsiveLayout(String viewport) {
    String[] dims = viewport.split("x");
    driver.manage().window().setSize(
      new Dimension(Integer.parseInt(dims[0]), Integer.parseInt(dims[1]))
    );
    
    driver.get("https://example.com");
    assertTrue(driver.findElement(By.id("content")).isDisplayed());
  }
}
`

### Q47. How do you handle rate limiting and API throttling in tests?
**Answer:**
Rate limiting handlers ensure tests don't overwhelm APIs and respect rate limit boundaries.

`java
public class RateLimitHandler {
  private Queue<Long> requests = new ConcurrentLinkedQueue<>();
  private int maxRequests = 100;
  private long timeWindow = 60000;
  
  public synchronized void executeWithLimit(Runnable action) throws InterruptedException {
    long now = System.currentTimeMillis();
    requests.removeIf(t -> now - t > timeWindow);
    
    if (requests.size() >= maxRequests) {
      long waitTime = requests.peek() + timeWindow - now;
      Thread.sleep(waitTime);
    }
    requests.offer(now);
    action.run();
  }
}
`

### Q48. How do you implement comprehensive test reporting and analytics?
**Answer:**
Comprehensive reporting provides visibility into test execution, trends, and system health.

`java
public class TestReporting {
  public static void generateReport() {
    ExtentSparkReporter reporter = new ExtentSparkReporter("target/report.html");
    ExtentReports extent = new ExtentReports();
    extent.attachReporter(reporter);
    
    // Tests automatically captured and reported
    extent.flush();
  }
}
`

### Q49. How do you implement test orchestration across multiple stages?
**Answer:**
Test orchestration executes tests in logical stages, failing fast on smoke tests before running longer test suites.

`java
public class TestOrchestration {
  public void executeTestPipeline() {
    executeSmokeTests();      // Fast feedback
    executeFunctionalTests(); // Core functionality
    executeIntegrationTests();// System integration
    executePerformanceTests();// Performance benchmarks
    generateReport();
  }
}
`

### Q50. How do you implement DevOps integration and CI/CD best practices?
**Answer:**
Full CI/CD integration automates test execution, reporting, and deployment decisions.

`yaml
# GitHub Actions Example
name: Test Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-java@v2
        with:
          java-version: '11'
      
      - name: Run Tests
        run: mvn test -Denv=staging
      
      - name: Generate Report
        if: always()
        run: mvn allure:report
      
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: target/allure-results/
`

---

## Complete 50 Q&A Summary

This comprehensive guide covers all aspects of enterprise-grade test automation:
- **Q1-Q15** (Parts 1-2): Fundamentals, selectors, waits, exceptions, POM
- **Q16-Q20** (Part 3): Framework design, API testing, CI/CD, performance, data-driven
- **Q21-Q30**: Visual testing, mobile, accessibility, cross-browser, retry, reporting
- **Q31-Q40**: Grid 4, custom waits, config, locators, interactions, screenshots, patterns
- **Q41-Q50**: Cloud testing, self-healing, data management, environment config, features, responsive, rate limiting, reporting, orchestration, DevOps

Covers all SDET-level competencies for modern test automation frameworks.
