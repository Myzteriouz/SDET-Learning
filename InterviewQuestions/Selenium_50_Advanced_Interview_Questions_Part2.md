# Selenium Advanced Interview Questions - Part 2 (Q8-Q50)

## Advanced Locator Strategies (Q8-Q10)

### Q8. What are the best practices for XPath and CSS selectors? When should you use each?
**Answer:**
```java
// XPath vs CSS Selectors - Detailed Comparison

// XPath ADVANTAGES:
// 1. Can traverse up the DOM (ancestor/parent)
// 2. Can use complex conditions
// 3. Can select by text content
// 4. Can use multiple attributes

// CSS ADVANTAGES:
// 1. Faster performance (native browser support)
// 2. Simpler syntax for common scenarios
// 3. Better cross-browser compatibility
// 4. Cleaner code

// XPATH EXAMPLES - When to use

// 1. Select by text (XPath exclusive)
By byText = By.xpath("//button[text()='Submit']");
By byPartialText = By.xpath("//button[contains(text(), 'Subm')]");
By byNormalizedText = By.xpath("//button[normalize-space()='Click Me']"); // Handles whitespace

// 2. Select by multiple conditions (XPath)
By multipleConditions = By.xpath(
  "//input[@type='email' and @name='email' and @required='required']"
);

// 3. Select parent/ancestor elements (XPath exclusive)
By selectParent = By.xpath(
  "//span[text()='Error']/parent::div[@class='form-group']"
);
By selectAncestor = By.xpath(
  "//input[@name='email']/ancestor::form[@id='login-form']"
);

// 4. Select following/preceding siblings (XPath)
By selectSibling = By.xpath(
  "//label[text()='Password']/following-sibling::input"
);

// 5. Select by position with conditions (XPath)
By selectByPosition = By.xpath(
  "(//button[@class='action'])[2]" // Second button with class 'action'
);

// 6. Complex nested conditions (XPath)
By complexXPath = By.xpath(
  "//table[@id='users-table']" +
  "//tr[td[1][text()='John']]" +
  "//td[contains(@class, 'email')]"
);

// CSS SELECTOR EXAMPLES - When to use

// 1. Attribute selectors (CSS is faster)
By byAttribute = By.cssSelector("input[type='email']");
By byMultipleAttributes = By.cssSelector("button[type='submit'][class~='primary']");
By byAttributePrefix = By.cssSelector("input[id^='user-']"); // Starts with
By byAttributeSuffix = By.cssSelector("a[href$='.pdf']"); // Ends with
By byAttributeContains = By.cssSelector("div[data-id*='dynamic']"); // Contains

// 2. Child selectors (cleaner with CSS)
By childSelector = By.cssSelector("form > input[type='email']");
By descendantSelector = By.cssSelector("form input[type='email']");

// 3. Pseudo-classes (CSS)
By firstChild = By.cssSelector("li:first-child");
By lastChild = By.cssSelector("li:last-child");
By nthChild = By.cssSelector("tr:nth-child(3)");
By nthOfType = By.cssSelector("button:nth-of-type(2)");

// 4. Pseudo-elements (CSS for styling selectors)
By notClass = By.cssSelector("button:not(.disabled)");
By empty = By.cssSelector("div:empty"); // Empty elements
By focus = By.cssSelector("input:focus"); // Focused elements

// PERFORMANCE COMPARISON
public class LocatorPerformanceTest {
  private WebDriver driver;
  
  public void testPerformance() {
    driver.get("https://example.com");
    
    // Slow XPath (traverses entire DOM)
    long startXPath = System.currentTimeMillis();
    for (int i = 0; i < 100; i++) {
      driver.findElements(By.xpath("//*[@class='item']"));
    }
    long xpathTime = System.currentTimeMillis() - startXPath;
    
    // Fast CSS (native browser support)
    long startCSS = System.currentTimeMillis();
    for (int i = 0; i < 100; i++) {
      driver.findElements(By.cssSelector(".item"));
    }
    long cssTime = System.currentTimeMillis() - startCSS;
    
    System.out.println("XPath time: " + xpathTime + "ms");
    System.out.println("CSS time: " + cssTime + "ms");
    System.out.println("CSS is " + (xpathTime / cssTime) + "x faster");
  }
}

// DECISION MATRIX - Which to use

/*
Scenario                              | Best Choice | Why
--------------------------------------|------------|------------------
Find by text content                  | XPath      | CSS can't do this
Find parent/ancestor element          | XPath      | CSS can't traverse up
Simple class selection                | CSS        | Faster, cleaner
Multiple simple attributes            | CSS        | Cleaner syntax
Complex nested conditions             | XPath      | More powerful
Dynamic attribute values              | XPath      | More flexible
Performance-critical code             | CSS        | Native browser support
Attribute contains/starts-with        | Both       | Both work well
Following/preceding siblings          | XPath      | CSS limited
Accessibility attributes (aria)       | Both       | Both work
*/

// BEST PRACTICE: Combine both strategies
public class HybridLocatorStrategy {
  private WebDriver driver;
  
  // Use CSS for speed when possible
  public WebElement getButtonByClass(String className) {
    return driver.findElement(By.cssSelector("button." + className));
  }
  
  // Use XPath when you need text matching
  public WebElement getButtonByText(String buttonText) {
    return driver.findElement(By.xpath(
      "//button[normalize-space()='" + buttonText + "']"
    ));
  }
  
  // Use XPath for complex relationships
  public WebElement getInputNextToLabel(String labelText) {
    return driver.findElement(By.xpath(
      "//label[contains(text(), '" + labelText + "')]/following-sibling::input"
    ));
  }
  
  // Use CSS for attribute-based selection
  public WebElement getInputByDataAttribute(String dataTestId) {
    return driver.findElement(By.cssSelector("[data-testid='" + dataTestId + "']"));
  }
}

// ANTI-PATTERNS TO AVOID

// ❌ BAD: Fragile XPath by position
By badXPath1 = By.xpath("//div[1]/div[2]/button[3]"); // Position-dependent

// ❌ BAD: Over-complicated XPath
By badXPath2 = By.xpath(
  "//*[@id='wrapper']/*[1]/div[2]/form/fieldset[1]/div/label[1]/following-sibling::input[1]"
);

// ❌ BAD: Using @id for dynamic IDs
By badXPath3 = By.xpath("//button[@id='btn-12345']"); // ID changes every page load

// ✅ GOOD: Specific, resilient locators
By goodCSS = By.cssSelector("button[type='submit'][class*='primary']");
By goodXPath = By.xpath("//button[text()='Submit' and @type='submit']");

// COMMON XPATH MISTAKES
public class XPathMistakes {
  
  // ❌ Wrong: Equal vs Contains
  // Should use contains() for partial matches
  By bad1 = By.xpath("//div[@class='form-group']"); // Breaks if class is 'form-group active'
  By good1 = By.xpath("//div[contains(@class, 'form-group')]"); // Works

  // ❌ Wrong: Case-sensitive text matching
  By bad2 = By.xpath("//button[text()='submit']"); // Won't match "Submit"
  By good2 = By.xpath("//button[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='submit']");

  // ❌ Wrong: Not handling whitespace
  By bad3 = By.xpath("//button[text()='Click Me']"); // Breaks with extra spaces
  By good3 = By.xpath("//button[normalize-space()='Click Me']"); // Handles whitespace

  // ❌ Wrong: Assuming parent relationship
  // Always verify actual structure
  By bad4 = By.xpath("//label[contains(text(), 'Email')]/input"); // Wrong - input is sibling
  By good4 = By.xpath("//label[contains(text(), 'Email')]/following-sibling::input"); // Correct
}

// XPATH GENERATOR FOR COMPLEX SCENARIOS
public class XPathBuilder {
  private String elementName = "*";
  private Map<String, String> attributes = new HashMap<>();
  private String textContent = null;
  private String relativeElement = null;
  
  public XPathBuilder element(String name) {
    this.elementName = name;
    return this;
  }
  
  public XPathBuilder withAttribute(String name, String value) {
    attributes.put(name, value);
    return this;
  }
  
  public XPathBuilder withText(String text) {
    this.textContent = text;
    return this;
  }
  
  public XPathBuilder followedBy(String element) {
    this.relativeElement = element;
    return this;
  }
  
  public String build() {
    StringBuilder xpath = new StringBuilder("//" + elementName);
    
    // Add attribute conditions
    if (!attributes.isEmpty()) {
      xpath.append("[");
      attributes.forEach((key, value) -> {
        xpath.append("@").append(key).append("='").append(value).append("' and ");
      });
      xpath.setLength(xpath.length() - 5); // Remove last " and "
      xpath.append("]");
    }
    
    // Add text condition
    if (textContent != null) {
      xpath.append("[contains(text(), '").append(textContent).append("')]");
    }
    
    // Add following element
    if (relativeElement != null) {
      xpath.append("/").append(relativeElement);
    }
    
    return xpath.toString();
  }
}

// Usage
XPathBuilder builder = new XPathBuilder()
  .element("input")
  .withAttribute("type", "email")
  .withAttribute("name", "email")
  .build(); // Returns: //input[@type='email' and @name='email']
```

---

### Q9. How do you handle file uploads and downloads in Selenium?
**Answer:**
```java
// FILE UPLOAD HANDLING

// Method 1: Send file path to input element (simplest)
WebElement fileInput = driver.findElement(By.id("file-upload"));
fileInput.sendKeys("/path/to/file.pdf");

// Method 2: Using absolute path (Windows)
String filePath = "C:\\Users\\TestData\\file.xlsx";
driver.findElement(By.id("upload-input")).sendKeys(filePath);

// Method 3: For multiple file uploads
WebElement multiFileInput = driver.findElement(By.name("files[]"));
multiFileInput.sendKeys("/file1.pdf");
multiFileInput.sendKeys("/file2.pdf"); // Send multiple times

// ADVANCED: File upload with validation
public class FileUploadHandler {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public FileUploadHandler(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Upload file and verify success
  public void uploadFileAndVerify(String filePath, String successMessage) {
    // Find file input
    WebElement fileInput = driver.findElement(By.id("file-upload"));
    
    // Upload file
    fileInput.sendKeys(new File(filePath).getAbsolutePath());
    
    // Click upload button
    driver.findElement(By.id("upload-btn")).click();
    
    // Verify upload success
    WebElement successMsg = wait.until(
      ExpectedConditions.visibilityOfElementLocated(
        By.id("upload-success")
      )
    );
    
    assertTrue(successMsg.getText().contains(successMessage));
  }
  
  // Upload with progress tracking
  public void uploadFileWithProgress(String filePath) {
    WebElement fileInput = driver.findElement(By.id("file-upload"));
    fileInput.sendKeys(new File(filePath).getAbsolutePath());
    
    // Wait for progress bar to appear
    wait.until(ExpectedConditions.visibilityOfElementLocated(
      By.id("progress-bar")
    ));
    
    // Wait for progress bar to complete (width 100%)
    wait.until(driver -> {
      String width = driver.findElement(By.id("progress-bar"))
        .getCssValue("width");
      return width.equals("100%");
    });
    
    System.out.println("Upload completed!");
  }
  
  // Validate file upload
  public boolean isFileUploaded(String expectedFileName) {
    List<WebElement> uploadedFiles = driver.findElements(
      By.xpath("//span[@class='uploaded-file']")
    );
    
    return uploadedFiles.stream()
      .anyMatch(el -> el.getText().contains(expectedFileName));
  }
}

// FILE DOWNLOAD HANDLING (Different from upload)

// Method 1: Configure Chrome to auto-download
public void setupChromeForDownload() {
  ChromeOptions options = new ChromeOptions();
  
  // Set download directory
  String downloadPath = System.getProperty("user.home") + "/Downloads";
  Map<String, Object> prefs = new HashMap<>();
  prefs.put("download.default_directory", downloadPath);
  prefs.put("download.prompt_for_download", false);
  prefs.put("profile.default_content_settings.popups", 0);
  
  options.setExperimentalOption("prefs", prefs);
  
  WebDriver driver = new ChromeDriver(options);
}

// Method 2: Verify download without checking file system
public void verifyDownloadViaLink() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com");
  
  // Get download link
  WebElement downloadLink = driver.findElement(By.id("download-btn"));
  String downloadUrl = downloadLink.getAttribute("href");
  
  // Verify URL is valid download link
  assertTrue(downloadUrl.contains(".pdf"));
}

// Method 3: Download file and verify content
public class FileDownloadHandler {
  private WebDriver driver;
  private String downloadDirectory;
  
  public FileDownloadHandler(WebDriver driver, String downloadDirectory) {
    this.driver = driver;
    this.downloadDirectory = downloadDirectory;
  }
  
  // Download file and wait for completion
  public File downloadFile(String downloadLinkSelector) throws Exception {
    // Setup download directory
    File downloadDir = new File(downloadDirectory);
    if (!downloadDir.exists()) {
      downloadDir.mkdirs();
    }
    
    // Get initial file count
    int initialFileCount = downloadDir.listFiles().length;
    
    // Click download button
    driver.findElement(By.cssSelector(downloadLinkSelector)).click();
    
    // Wait for new file
    long startTime = System.currentTimeMillis();
    long timeout = 30000; // 30 seconds
    
    while (System.currentTimeMillis() - startTime < timeout) {
      if (downloadDir.listFiles().length > initialFileCount) {
        // New file appeared
        File[] files = downloadDir.listFiles();
        return files[files.length - 1]; // Return newest file
      }
      Thread.sleep(500);
    }
    
    throw new TimeoutException("File download timeout");
  }
  
  // Verify downloaded file content
  public boolean verifyPDFContent(File pdfFile, String expectedText) throws Exception {
    // Using PDFBox library
    PDDocument document = PDDocument.load(pdfFile);
    PDFTextStripper stripper = new PDFTextStripper();
    String content = stripper.getText(document);
    document.close();
    
    return content.contains(expectedText);
  }
  
  // Verify Excel file
  public boolean verifyExcelContent(File excelFile, String sheetName, 
                                    String cellValue) throws Exception {
    FileInputStream fis = new FileInputStream(excelFile);
    XSSFWorkbook workbook = new XSSFWorkbook(fis);
    XSSFSheet sheet = workbook.getSheet(sheetName);
    
    boolean found = false;
    for (Row row : sheet) {
      for (Cell cell : row) {
        if (cell.getStringCellValue().contains(cellValue)) {
          found = true;
          break;
        }
      }
    }
    
    workbook.close();
    fis.close();
    
    return found;
  }
}

// ADVANCED: Handle download with network interception (Selenium 4)
public void captureDownloadUrl() {
  WebDriver driver = new ChromeDriver();
  
  // Capture requests
  List<String> downloadUrls = new ArrayList<>();
  
  driver.get("https://example.com");
  
  // Click download button
  WebElement downloadBtn = driver.findElement(By.id("download"));
  
  // Get href attribute
  String downloadUrl = downloadBtn.getAttribute("href");
  downloadUrls.add(downloadUrl);
  
  // Verify URL
  assertTrue(downloadUrl.contains(".pdf"));
}

// TESTING FILE OPERATIONS
@Test
public void testFileUploadAndDownload() throws Exception {
  WebDriver driver = new ChromeDriver();
  FileUploadHandler uploadHandler = new FileUploadHandler(driver);
  FileDownloadHandler downloadHandler = new FileDownloadHandler(
    driver,
    System.getProperty("user.home") + "/Downloads"
  );
  
  driver.get("https://example.com/file-operations");
  
  // Upload file
  String uploadPath = "src/test/resources/sample.pdf";
  uploadHandler.uploadFileAndVerify(uploadPath, "File uploaded successfully");
  
  // Download file
  File downloadedFile = downloadHandler.downloadFile("[data-testid='download-btn']");
  
  // Verify file
  assertTrue(downloadedFile.exists());
  assertTrue(downloadedFile.length() > 0);
  
  // Verify content
  boolean contentValid = downloadHandler.verifyPDFContent(
    downloadedFile,
    "Expected text in PDF"
  );
  assertTrue(contentValid);
}
```

---

### Q10. How do you handle dynamic dropdowns and custom select elements?
**Answer:**
```java
// STANDARD HTML SELECT ELEMENT
Select standardDropdown = new Select(driver.findElement(By.id("country")));

// Select by visible text
standardDropdown.selectByVisibleText("United States");

// Select by value
standardDropdown.selectByValue("us");

// Select by index
standardDropdown.selectByIndex(0);

// Get all options
List<WebElement> allOptions = standardDropdown.getOptions();
for (WebElement option : allOptions) {
  System.out.println(option.getText());
}

// Get first selected option
WebElement selected = standardDropdown.getFirstSelectedOption();

// Check if multiple select
boolean isMultiple = standardDropdown.isMultiple();

// Deselect (only for multi-select)
standardDropdown.deselectByVisibleText("Option");
standardDropdown.deselectAll();

// CUSTOM DROPDOWN (Built with DIV/UL/LI)
// HTML Structure:
// <div class="custom-dropdown">
//   <button class="dropdown-btn">Select...</button>
//   <ul class="dropdown-menu">
//     <li data-value="opt1">Option 1</li>
//     <li data-value="opt2">Option 2</li>
//   </ul>
// </div>

public class CustomDropdownHandler {
  private WebDriver driver;
  private WebDriverWait wait;
  private By dropdownButton;
  private By dropdownMenu;
  private By menuItems;
  
  public CustomDropdownHandler(WebDriver driver, By button, By menu, By items) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    this.dropdownButton = button;
    this.dropdownMenu = menu;
    this.menuItems = items;
  }
  
  // Open dropdown
  private void openDropdown() {
    WebElement button = driver.findElement(dropdownButton);
    wait.until(ExpectedConditions.elementToBeClickable(button)).click();
    
    // Wait for menu to appear
    wait.until(ExpectedConditions.visibilityOfElementLocated(dropdownMenu));
  }
  
  // Select by visible text
  public void selectByText(String text) {
    openDropdown();
    
    By menuItem = By.xpath(
      dropdownMenu + "//li[contains(text(), '" + text + "')]"
    );
    
    WebElement item = wait.until(
      ExpectedConditions.elementToBeClickable(menuItem)
    );
    item.click();
    
    // Wait for dropdown to close
    wait.until(ExpectedConditions.invisibilityOfElementLocated(dropdownMenu));
  }
  
  // Select by data attribute
  public void selectByDataValue(String dataValue) {
    openDropdown();
    
    By menuItem = By.xpath(
      "//li[@data-value='" + dataValue + "']"
    );
    
    driver.findElement(menuItem).click();
  }
  
  // Get all available options
  public List<String> getAllOptions() {
    openDropdown();
    
    List<WebElement> items = driver.findElements(menuItems);
    return items.stream()
      .map(WebElement::getText)
      .collect(Collectors.toList());
  }
  
  // Check if option exists
  public boolean optionExists(String optionText) {
    return getAllOptions().contains(optionText);
  }
  
  // Get selected value
  public String getSelectedValue() {
    return driver.findElement(dropdownButton).getText();
  }
}

// USAGE
@Test
public void testCustomDropdown() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com");
  
  CustomDropdownHandler dropdown = new CustomDropdownHandler(
    driver,
    By.cssSelector(".dropdown-btn"),
    By.cssSelector(".dropdown-menu"),
    By.cssSelector(".dropdown-menu li")
  );
  
  // Select option
  dropdown.selectByText("United States");
  
  // Verify selection
  assertEquals("United States", dropdown.getSelectedValue());
}

// ADVANCED: Dropdown with search/filter
public class SearchableDropdownHandler {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public SearchableDropdownHandler(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Open dropdown and filter
  public void selectFromFilterableDropdown(String dropdownId, String searchText) {
    // Click dropdown to open
    WebElement dropdown = driver.findElement(By.id(dropdownId));
    dropdown.click();
    
    // Type in search field
    WebElement searchField = wait.until(
      ExpectedConditions.presenceOfElementLocated(
        By.xpath("//input[@placeholder='Search...']")
      )
    );
    searchField.sendKeys(searchText);
    
    // Wait for filtered results
    By filteredItem = By.xpath(
      "//li[contains(text(), '" + searchText + "')]"
    );
    WebElement item = wait.until(
      ExpectedConditions.elementToBeClickable(filteredItem)
    );
    item.click();
  }
}

// DROPDOWN WITH KEYBOARD NAVIGATION
public void selectDropdownWithKeyboard(String dropdownId, int optionIndex) {
  WebElement dropdown = driver.findElement(By.id(dropdownId));
  dropdown.click();
  
  // Navigate using arrow keys
  for (int i = 0; i < optionIndex; i++) {
    dropdown.sendKeys(Keys.ARROW_DOWN);
  }
  
  // Select with Enter
  dropdown.sendKeys(Keys.ENTER);
}

// MULTI-SELECT DROPDOWN
public class MultiSelectDropdownHandler {
  private WebDriver driver;
  private Select select;
  
  public MultiSelectDropdownHandler(WebDriver driver, By locator) {
    this.driver = driver;
    this.select = new Select(driver.findElement(locator));
  }
  
  // Select multiple options
  public void selectMultiple(String... values) {
    for (String value : values) {
      select.selectByVisibleText(value);
    }
  }
  
  // Get all selected options
  public List<String> getSelectedOptions() {
    return select.getAllSelectedOptions().stream()
      .map(WebElement::getText)
      .collect(Collectors.toList());
  }
  
  // Deselect all and select new ones
  public void replaceSelection(String... newValues) {
    select.deselectAll();
    selectMultiple(newValues);
  }
}

// DROPDOWN WITH AJAX LOADING
public void selectDropdownWithAjaxLoading(String dropdownSelector, 
                                          String optionText) {
  WebElement dropdown = driver.findElement(By.cssSelector(dropdownSelector));
  dropdown.click();
  
  // Wait for options to load via AJAX
  WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  By menuItems = By.cssSelector(".dropdown-menu li");
  
  wait.until(ExpectedConditions.presenceOfAllElementsLocatedBy(menuItems));
  
  // Select option
  WebElement option = wait.until(
    ExpectedConditions.elementToBeClickable(
      By.xpath("//li[contains(text(), '" + optionText + "')]")
    )
  );
  option.click();
}

// TESTING VARIOUS DROPDOWN SCENARIOS
@Test
public void testAllDropdownScenarios() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com");
  
  // Standard dropdown
  Select standardSelect = new Select(
    driver.findElement(By.id("standard-dropdown"))
  );
  standardSelect.selectByVisibleText("Option 1");
  
  // Custom dropdown
  CustomDropdownHandler customDropdown = new CustomDropdownHandler(
    driver,
    By.cssSelector(".custom-dropdown .btn"),
    By.cssSelector(".custom-dropdown .menu"),
    By.cssSelector(".custom-dropdown .menu li")
  );
  customDropdown.selectByText("Option 2");
  
  // Searchable dropdown
  SearchableDropdownHandler searchDropdown = new SearchableDropdownHandler(driver);
  searchDropdown.selectFromFilterableDropdown(
    "searchable-dropdown",
    "Search Term"
  );
  
  // Multi-select dropdown
  MultiSelectDropdownHandler multiSelect = new MultiSelectDropdownHandler(
    driver,
    By.id("multi-select")
  );
  multiSelect.selectMultiple("Option 1", "Option 2", "Option 3");
  
  // Verify selections
  List<String> selected = multiSelect.getSelectedOptions();
  assertEquals(3, selected.size());
}
```

---

## Waits & Synchronization (Q11-Q15)

### Q11. How do you handle AJAX calls and asynchronous JavaScript in Selenium?
**Answer:**
```java
// AJAX HANDLING - Core Challenge
// Problem: Page doesn't refresh, elements load asynchronously
// Solution: Use explicit waits for specific conditions

// APPROACH 1: Wait for element visibility after AJAX
WebDriver driver = new ChromeDriver();
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

driver.findElement(By.id("load-data-btn")).click();

// Wait for result element to appear
WebElement result = wait.until(
  ExpectedConditions.visibilityOfElementLocated(By.id("ajax-result"))
);
assertEquals("Data loaded", result.getText());

// APPROACH 2: Wait for loading indicator to disappear
driver.findElement(By.id("load-btn")).click();

// Wait for spinner to appear then disappear
wait.until(ExpectedConditions.invisibilityOfElementLocated(
  By.cssSelector(".loading-spinner")
));

// APPROACH 3: Wait for specific text to appear
WebElement statusMsg = wait.until(
  ExpectedConditions.textToBePresentInElementLocated(
    By.id("status"),
    "Success"
  )
);

// APPROACH 4: Custom condition for jQuery AJAX
public void waitForJQueryAjaxComplete() {
  JavascriptExecutor js = (JavascriptExecutor) driver;
  
  WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  wait.until(driver -> {
    try {
      Long activeRequests = (Long) js.executeScript("return jQuery.active");
      return activeRequests == 0;
    } catch (Exception e) {
      return true;
    }
  });
}

// APPROACH 5: Wait for multiple conditions
public void waitForAjaxComplete(WebDriver driver) {
  WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  
  // Wait for AJAX requests to complete
  wait.until(webDriver -> {
    JavascriptExecutor js = (JavascriptExecutor) webDriver;
    
    // Check jQuery AJAX
    Long jQueryActive = (Long) js.executeScript("return jQuery.active || 0");
    
    // Check XHR active
    Boolean xhrComplete = (Boolean) js.executeScript(
      "return (window.XMLHttpRequest === undefined || " +
      "window.XMLHttpRequest.prototype.__definedGetter__ === undefined)"
    );
    
    return jQueryActive == 0 && xhrComplete;
  });
}

// ADVANCED: AjaxWaitHelper class
public class AjaxWaitHelper {
  private WebDriver driver;
  private JavascriptExecutor js;
  private WebDriverWait wait;
  
  public AjaxWaitHelper(WebDriver driver) {
    this.driver = driver;
    this.js = (JavascriptExecutor) driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(30));
  }
  
  // Wait for jQuery AJAX
  public void waitForJQueryAjax(int timeoutSeconds) {
    wait.withTimeout(Duration.ofSeconds(timeoutSeconds))
      .until(driver -> {
        try {
          Object result = js.executeScript("return jQuery.active");
          return (Long) result == 0;
        } catch (Exception e) {
          return true;
        }
      });
  }
  
  // Wait for all active requests to complete
  public void waitForAllRequests(int timeoutSeconds) {
    wait.withTimeout(Duration.ofSeconds(timeoutSeconds))
      .until(driver -> {
        // Check jQuery
        Long jQueryActive = getJQueryActiveRequests();
        
        // Check native XMLHttpRequest
        Boolean allComplete = (Boolean) js.executeScript(
          "return document.readyState === 'complete'"
        );
        
        return jQueryActive == 0 && allComplete;
      });
  }
  
  // Get jQuery active AJAX count
  private Long getJQueryActiveRequests() {
    try {
      Object result = js.executeScript("return jQuery.active || 0");
      return (Long) result;
    } catch (Exception e) {
      return 0L;
    }
  }
  
  // Wait for Axios requests (used in Vue, React)
  public void waitForAxiosComplete(int timeoutSeconds) {
    wait.withTimeout(Duration.ofSeconds(timeoutSeconds))
      .until(driver -> {
        try {
          Boolean complete = (Boolean) js.executeScript(
            "return window.axios ? window.axios.defaults.adapter : true"
          );
          return complete != null;
        } catch (Exception e) {
          return true;
        }
      });
  }
  
  // Wait for Angular requests
  public void waitForAngularAjax(int timeoutSeconds) {
    wait.withTimeout(Duration.ofSeconds(timeoutSeconds))
      .until(driver -> {
        try {
          Boolean ready = (Boolean) js.executeScript(
            "return window.getAllAngularTestabilities().findIndex(x => !x.isStable()) === -1"
          );
          return ready;
        } catch (Exception e) {
          return true;
        }
      });
  }
  
  // Wait for element and AJAX
  public WebElement waitForElementAndAjax(By locator, int timeoutSeconds) {
    waitForAllRequests(timeoutSeconds);
    return wait.withTimeout(Duration.ofSeconds(timeoutSeconds))
      .until(ExpectedConditions.visibilityOfElementLocated(locator));
  }
}

// PRACTICAL EXAMPLE: E-commerce product search
@Test
public void testAjaxSearch() {
  WebDriver driver = new ChromeDriver();
  AjaxWaitHelper ajaxWait = new AjaxWaitHelper(driver);
  
  driver.get("https://shop.example.com");
  
  // Type in search
  WebElement searchBox = driver.findElement(By.id("search"));
  searchBox.sendKeys("laptop");
  
  // Wait for AJAX results
  ajaxWait.waitForAllRequests(10);
  
  // Wait for results to appear
  WebElement resultContainer = driver.findElement(By.id("search-results"));
  ajaxWait.wait.until(
    ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".product-item"))
  );
  
  // Verify results
  List<WebElement> products = driver.findElements(By.cssSelector(".product-item"));
  assertTrue(products.size() > 0);
}

// HANDLING SLOW AJAX REQUESTS
@Test
public void testSlowAjaxWithRetry() {
  WebDriver driver = new ChromeDriver();
  AjaxWaitHelper ajaxWait = new AjaxWaitHelper(driver);
  
  driver.get("https://example.com");
  
  // Click button that triggers slow AJAX
  driver.findElement(By.id("slow-request-btn")).click();
  
  // Wait longer for slow requests
  ajaxWait.waitForAllRequests(30); // 30 seconds
  
  // Verify result
  WebElement result = driver.findElement(By.id("result"));
  assertTrue(result.isDisplayed());
}

// MONITORING NETWORK ACTIVITY
@Test
public void testWithNetworkMonitoring() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com");
  
  // Log all AJAX requests
  driver.findElement(By.id("load-data")).click();
  
  // Manual monitoring
  List<String> completedRequests = new ArrayList<>();
  
  ((JavascriptExecutor) driver).executeScript(
    "window.ajaxRequests = [];" +
    "var originalFetch = window.fetch;" +
    "window.fetch = function(...args) {" +
    "  window.ajaxRequests.push(args[0]);" +
    "  return originalFetch.apply(this, args);" +
    "};"
  );
  
  // Wait and get requests
  Thread.sleep(2000);
  @SuppressWarnings("unchecked")
  List<String> requests = (List<String>) ((JavascriptExecutor) driver)
    .executeScript("return window.ajaxRequests;");
  
  System.out.println("AJAX Requests: " + requests);
}
```

---

### Q12. How do you handle StaleElementReferenceException and implement retry mechanisms?
**Answer:**
```java
// StaleElementReferenceException occurs when:
// 1. DOM element is removed from DOM
// 2. Page is refreshed
// 3. AJAX updates the element
// 4. Element is re-rendered

// SOLUTION 1: Re-locate element before interacting
public void clickWithRetry(By locator, int maxAttempts) {
  int attempts = 0;
  while (attempts < maxAttempts) {
    try {
      // Fresh locate each time
      driver.findElement(locator).click();
      return;
    } catch (StaleElementReferenceException e) {
      attempts++;
      if (attempts >= maxAttempts) {
        throw new RuntimeException("Failed to click element after " + maxAttempts + " attempts");
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

// SOLUTION 2: Use Explicit Wait (Recommended)
public void clickWithWait(By locator) {
  WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
  // Explicit wait handles stale elements automatically
}

// SOLUTION 3: Wrapper class with automatic retry
public class StaleElementHandler {
  private WebDriver driver;
  private int maxRetries = 3;
  private long retryDelayMs = 100;
  
  public StaleElementHandler(WebDriver driver) {
    this.driver = driver;
  }
  
  // Generic retry wrapper
  public <T> T executeWithRetry(Function<WebDriver, T> action) {
    int attempts = 0;
    while (attempts < maxRetries) {
      try {
        return action.apply(driver);
      } catch (StaleElementReferenceException e) {
        attempts++;
        if (attempts >= maxRetries) {
          throw new RuntimeException(
            "Operation failed after " + maxRetries + " retries",
            e
          );
        }
        try {
          Thread.sleep(retryDelayMs);
        } catch (InterruptedException ie) {
          Thread.currentThread().interrupt();
        }
      }
    }
    return null;
  }
  
  // Specific methods
  public void clickWithRetry(By locator) {
    executeWithRetry(driver -> {
      driver.findElement(locator).click();
      return null;
    });
  }
  
  public void fillWithRetry(By locator, String text) {
    executeWithRetry(driver -> {
      WebElement element = driver.findElement(locator);
      element.clear();
      element.sendKeys(text);
      return null;
    });
  }
  
  public String getTextWithRetry(By locator) {
    return executeWithRetry(driver -> 
      driver.findElement(locator).getText()
    );
  }
  
  public boolean isDisplayedWithRetry(By locator) {
    return executeWithRetry(driver -> 
      driver.findElement(locator).isDisplayed()
    );
  }
}

// SOLUTION 4: Use Page Object Model (store locators, not elements)
public class RobustLoginPage {
  private WebDriver driver;
  
  // Store LOCATORS, not element references
  private By emailField = By.id("email");
  private By passwordField = By.id("password");
  private By loginButton = By.id("login-btn");
  
  public RobustLoginPage(WebDriver driver) {
    this.driver = driver;
  }
  
  // Always locate fresh
  public void login(String email, String password) {
    // Don't do: WebElement emailEl = driver.findElement(emailField);
    // Instead locate fresh each time
    driver.findElement(emailField).sendKeys(email);
    driver.findElement(passwordField).sendKeys(password);
    driver.findElement(loginButton).click();
  }
}

// SOLUTION 5: Dynamic wait with custom condition
public class DynamicElementWait {
  private WebDriver driver;
  private WebDriverWait wait;
  
  public DynamicElementWait(WebDriver driver) {
    this.driver = driver;
    this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  }
  
  // Wait for element stability (not stale)
  public WebElement waitForStableElement(By locator) {
    return wait.until(driver -> {
      try {
        WebElement element = driver.findElement(locator);
        // Check element is still attached and visible
        element.isDisplayed();
        return element;
      } catch (StaleElementReferenceException e) {
        return null; // Will retry
      }
    });
  }
  
  // Perform action with automatic stale handling
  public void performActionWithStaleRecovery(By locator, Consumer<WebElement> action) {
    int maxAttempts = 3;
    int attempts = 0;
    
    while (attempts < maxAttempts) {
      try {
        WebElement element = driver.findElement(locator);
        action.accept(element);
        return;
      } catch (StaleElementReferenceException e) {
        attempts++;
        if (attempts >= maxAttempts) throw e;
        try {
          Thread.sleep(100);
        } catch (InterruptedException ie) {
          Thread.currentThread().interrupt();
        }
      }
    }
  }
}

// SOLUTION 6: Advanced retry with exponential backoff
public class AdvancedRetryHandler {
  private WebDriver driver;
  private static final int MAX_RETRIES = 3;
  private static final long BASE_DELAY = 100; // milliseconds
  
  public AdvancedRetryHandler(WebDriver driver) {
    this.driver = driver;
  }
  
  // Retry with exponential backoff
  public <T> T retryWithBackoff(Function<WebDriver, T> action) {
    int attempt = 0;
    
    while (attempt < MAX_RETRIES) {
      try {
        return action.apply(driver);
      } catch (StaleElementReferenceException e) {
        attempt++;
        if (attempt >= MAX_RETRIES) {
          throw new RuntimeException("Failed after " + MAX_RETRIES + " retries");
        }
        
        // Exponential backoff: 100ms, 200ms, 400ms
        long delayMs = BASE_DELAY * (long) Math.pow(2, attempt - 1);
        try {
          Thread.sleep(delayMs);
        } catch (InterruptedException ie) {
          Thread.currentThread().interrupt();
        }
      }
    }
    return null;
  }
  
  // Retry with fallback mechanism
  public WebElement findElementWithFallback(By primary, By fallback) {
    try {
      return retryWithBackoff(driver -> driver.findElement(primary));
    } catch (RuntimeException e) {
      // Try fallback locator
      return retryWithBackoff(driver -> driver.findElement(fallback));
    }
  }
}

// PRACTICAL EXAMPLE: Complete stale element handling
@Test
public void testStaleElementHandling() {
  WebDriver driver = new ChromeDriver();
  driver.get("https://example.com");
  
  // Method 1: Using wrapper
  StaleElementHandler handler = new StaleElementHandler(driver);
  handler.fillWithRetry(By.id("email"), "user@test.com");
  handler.clickWithRetry(By.id("submit"));
  
  // Method 2: Using POM
  RobustLoginPage loginPage = new RobustLoginPage(driver);
  loginPage.login("user@test.com", "password");
  
  // Method 3: Using explicit waits
  WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
  wait.until(ExpectedConditions.elementToBeClickable(By.id("button")))
    .click();
  
  // Method 4: Using advanced retry
  AdvancedRetryHandler retryHandler = new AdvancedRetryHandler(driver);
  retryHandler.retryWithBackoff(driver -> {
    driver.findElement(By.id("submit")).click();
    return null;
  });
}

// BEST PRACTICES
public class StaleElementBestPractices {
  
  // ❌ BAD: Storing element reference
  private WebElement cachedElement = driver.findElement(By.id("element"));
  public void clickBad() {
    cachedElement.click(); // Can become stale
  }
  
  // ✅ GOOD: Store locator, locate fresh
  private By elementLocator = By.id("element");
  public void clickGood() {
    driver.findElement(elementLocator).click(); // Always fresh
  }
  
  // ✅ GOOD: Use explicit waits
  public void clickWithWait() {
    new WebDriverWait(driver, Duration.ofSeconds(10))
      .until(ExpectedConditions.elementToBeClickable(elementLocator))
      .click();
  }
  
  // ✅ GOOD: Use POM pattern
  public void clickWithPOM() {
    new MyPage(driver).clickElement();
  }
}
```

---

### Q13. How do you run tests in parallel using Selenium Grid? Explain architecture and setup.
**Answer:**
```java
// SELENIUM GRID 4 ARCHITECTURE:
// Hub (manages test distribution) → Node 1, Node 2, Node 3 (run tests)

// STEP 1: Start Selenium Grid (Command line)
/*
Terminal 1: Start Hub
java -jar selenium-server-4.x.jar hub

Terminal 2: Start Node (Chrome)
java -jar selenium-server-4.x.jar node --port 5555 --host localhost

Terminal 3: Start Node (Firefox)
java -jar selenium-server-4.x.jar node --port 5556 --host localhost
*/

// STEP 2: Configure test to use Grid
public void setupGridDriver() {
  try {
    // Connect to Grid Hub
    URL hubUrl = new URL("http://localhost:4444");
    
    // Define desired capabilities
    ChromeOptions options = new ChromeOptions();
    
    // Create RemoteWebDriver
    WebDriver driver = new RemoteWebDriver(hubUrl, options);
    
    driver.get("https://example.com");
    // Test code...
    driver.quit();
  } catch (MalformedURLException e) {
    e.printStackTrace();
  }
}

// STEP 3: Parallel execution with TestNG
@Test(dataProvider = "browsers")
public void testMultipleBrowsers(String browserName, 
                                 String version,
                                 String platform) {
  DesiredCapabilities capabilities = new DesiredCapabilities();
  
  switch (browserName.toLowerCase()) {
    case "chrome":
      capabilities = DesiredCapabilities.chrome();
      break;
    case "firefox":
      capabilities = DesiredCapabilities.firefox();
      break;
    case "edge":
      capabilities = DesiredCapabilities.edge();
      break;
  }
  
  capabilities.setVersion(version);
  capabilities.setPlatform(Platform.fromString(platform));
  
  try {
    URL gridHubUrl = new URL("http://localhost:4444");
    WebDriver driver = new RemoteWebDriver(gridHubUrl, capabilities);
    
    driver.get("https://example.com");
    // Test logic
    driver.quit();
  } catch (Exception e) {
    e.printStackTrace();
  }
}

@DataProvider(parallel = true)
public Object[][] browsers() {
  return new Object[][] {
    { "chrome", "latest", "Windows 10" },
    { "firefox", "latest", "Windows 10" },
    { "edge", "latest", "Windows 10" },
    { "chrome", "latest", "MacOS" }
  };
}

// STEP 4: Grid configuration with YAML
public class GridSetup {
  // grid-config.yaml:
  /*
  hub:
    host: localhost
    port: 4444

  nodeConfig:
    hub: http://localhost:4444
    port: 5555
    timeout: 300
    maxSession: 3
    browserTimeout: 300
    waitTimeout: 120
    
    capabilities:
      - browserName: chrome
        browserVersion: latest
        platformName: windows
        maxInstances: 2
        
      - browserName: firefox
        browserVersion: latest
        platformName: windows
        maxInstances: 2
  */
}

// STEP 5: Advanced Grid management class
public class GridManager {
  private URL gridHubUrl;
  private static final String HUB_URL = "http://localhost:4444";
  
  public GridManager() throws MalformedURLException {
    this.gridHubUrl = new URL(HUB_URL);
  }
  
  // Get driver for specific browser
  public WebDriver getDriver(String browserName, String version) {
    DesiredCapabilities capabilities = getCapabilities(browserName, version);
    return new RemoteWebDriver(gridHubUrl, capabilities);
  }
  
  // Get driver for specific platform
  public WebDriver getDriver(String browserName, String version, 
                            String platformName) {
    DesiredCapabilities capabilities = getCapabilities(browserName, version);
    capabilities.setPlatform(Platform.fromString(platformName));
    return new RemoteWebDriver(gridHubUrl, capabilities);
  }
  
  // Get Chrome driver with options
  public WebDriver getChromeDriver() {
    ChromeOptions options = new ChromeOptions();
    options.setCapability("browserVersion", "latest");
    options.setCapability("platformName", "Windows");
    return new RemoteWebDriver(gridHubUrl, options);
  }
  
  // Get Firefox driver
  public WebDriver getFirefoxDriver() {
    FirefoxOptions options = new FirefoxOptions();
    options.setCapability("browserVersion", "latest");
    return new RemoteWebDriver(gridHubUrl, options);
  }
  
  // Get capabilities
  private DesiredCapabilities getCapabilities(String browserName, 
                                             String version) {
    DesiredCapabilities capabilities;
    
    switch (browserName.toLowerCase()) {
      case "chrome":
        capabilities = DesiredCapabilities.chrome();
        break;
      case "firefox":
        capabilities = DesiredCapabilities.firefox();
        break;
      case "edge":
        capabilities = DesiredCapabilities.edge();
        break;
      case "safari":
        capabilities = DesiredCapabilities.safari();
        break;
      default:
        throw new IllegalArgumentException("Unknown browser: " + browserName);
    }
    
    capabilities.setVersion(version);
    return capabilities;
  }
  
  // Get session info
  public void getSessionInfo(WebDriver driver) {
    RemoteWebDriver remoteDriver = (RemoteWebDriver) driver;
    System.out.println("Session ID: " + remoteDriver.getSessionId());
    System.out.println("Node URL: " + remoteDriver.getCommandExecutor().getAddressOfRemoteServer());
  }
}

// STEP 6: Parallel test execution with TestNG
@Test(threadPoolSize = 4, invocationCount = 4, timeOut = 20000)
public void testParallel() {
  WebDriver driver = null;
  try {
    GridManager gridManager = new GridManager();
    driver = gridManager.getChromeDriver();
    
    driver.get("https://example.com");
    
    // Test assertions
    assertTrue(driver.getTitle().contains("Example"));
  } finally {
    if (driver != null) {
      driver.quit();
    }
  }
}

// STEP 7: TestNG XML configuration for parallel execution
/*
<!DOCTYPE suite SYSTEM "http://testng.org/testng-current.dtd">
<suite name="Grid Tests" parallel="methods" thread-count="4">
  <test name="Browser Compatibility Tests">
    <classes>
      <class name="com.test.GridTests"/>
    </classes>
  </test>
</suite>
*/

// STEP 8: Docker setup for Grid
/*
docker-compose.yml:

version: '3.8'
services:
  selenium-hub:
    image: selenium/hub:4.0
    ports:
      - "4444:4444"
    environment:
      - GRID_MAX_SESSION=5
      - GRID_BROWSER_TIMEOUT=300

  chrome:
    image: selenium/node-chrome:4.0
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_NODE_MAX_SESSIONS=2

  firefox:
    image: selenium/node-firefox:4.0
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_NODE_MAX_SESSIONS=2
*/

// STEP 9: Complete Grid test suite
public class GridTestSuite {
  private WebDriver driver;
  private GridManager gridManager;
  
  @BeforeMethod
  public void setup(String browserName) throws Exception {
    gridManager = new GridManager();
    driver = gridManager.getDriver(browserName, "latest");
  }
  
  @Test(dataProvider = "browsers")
  public void testMultipleBrowsers(String browser) {
    driver.get("https://example.com");
    
    // Test login
    driver.findElement(By.id("username")).sendKeys("user");
    driver.findElement(By.id("password")).sendKeys("pass");
    driver.findElement(By.id("login")).click();
    
    // Verify
    assertTrue(driver.getCurrentUrl().contains("dashboard"));
  }
  
  @AfterMethod
  public void tearDown() {
    if (driver != null) {
      driver.quit();
    }
  }
  
  @DataProvider
  public Object[] browsers() {
    return new Object[] { "chrome", "firefox", "edge" };
  }
}

// BEST PRACTICES:
/*
1. Use Docker for consistent environment
2. Configure proper timeouts (300 seconds recommended)
3. Monitor node health
4. Use session pooling for faster test execution
5. Implement proper cleanup (driver.quit())
6. Log session IDs for debugging
7. Use separate data for parallel tests (no shared state)
8. Configure appropriate thread counts
9. Monitor Grid dashboard (http://localhost:4444)
10. Set up proper error handling and reporting
*/
```

---

## Exception Handling & Error Recovery (Q14-Q15)

### Q14. What are common Selenium exceptions? How do you handle them?
**Answer:**
```java
// COMMON SELENIUM EXCEPTIONS AND HANDLING

// 1. NoSuchElementException - Element not found
try {
  WebElement element = driver.findElement(By.id("non-existent"));
  element.click();
} catch (NoSuchElementException e) {
  System.out.println("Element not found: " + e.getMessage());
  // Fallback action
  driver.findElement(By.cssSelector(".alternative-element")).click();
}

// Better approach: Use explicit wait
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
try {
  WebElement element = wait.until(
    ExpectedConditions.presenceOfElementLocated(By.id("element"))
  );
} catch (TimeoutException e) {
  System.out.println("Element not found within timeout");
  throw e;
}

// 2. StaleElementReferenceException - DOM element changed
try {
  WebElement element = driver.findElement(By.id("dynamic"));
  Thread.sleep(1000); // DOM changes
  element.click(); // Might throw StaleElementReferenceException
} catch (StaleElementReferenceException e) {
  // Re-locate and retry
  driver.findElement(By.id("dynamic")).click();
}

// 3. TimeoutException - Wait exceeded
public void handleTimeoutException() {
  WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
  try {
    wait.until(ExpectedConditions.presenceOfElementLocated(
      By.id("slow-element")
    ));
  } catch (TimeoutException e) {
    System.out.println("Element took too long to appear");
    // Take screenshot for debugging
    takeScreenshot();
    throw e;
  }
}

// 4. NoSuchWindowException - Window no longer exists
try {
  driver.switchTo().window("non-existent-window");
} catch (NoSuchWindowException e) {
  System.out.println("Window not found");
  // Switch to available window
  driver.switchTo().window(driver.getWindowHandle());
}

// 5. UnhandledAlertException - Unexpected alert
try {
  driver.findElement(By.id("button")).click();
} catch (UnhandledAlertException e) {
  Alert alert = driver.switchTo().alert();
  String alertText = alert.getText();
  alert.accept();
  System.out.println("Alert handled: " + alertText);
}

// 6. InvalidElementStateException - Element not in valid state
try {
  WebElement disabledInput = driver.findElement(By.id("disabled-input"));
  disabledInput.sendKeys("text");
} catch (InvalidElementStateException e) {
  System.out.println("Element not in valid state for this action");
  // Enable element and retry
  JavascriptExecutor js = (JavascriptExecutor) driver;
  js.executeScript("arguments[0].disabled = false;", disabledInput);
  disabledInput.sendKeys("text");
}

// 7. SessionNotCreatedException - Browser driver not found
try {
  WebDriver driver = new ChromeDriver();
} catch (SessionNotCreatedException e) {
  System.out.println("ChromeDriver version mismatch or not available");
  // Fallback to Firefox
  WebDriver driver = new FirefoxDriver();
}

// 8. WebDriverException - General Selenium error
try {
  driver.findElement(By.id("element")).click();
} catch (WebDriverException e) {
  System.out.println("WebDriver error: " + e.getMessage());
  // Check browser is still responsive
  if (e.getMessage().contains("session")) {
    System.out.println("Browser session lost");
    // Restart driver
    driver.quit();
    driver = new ChromeDriver();
  }
}

// COMPREHENSIVE Exception handler class
public class SeleniumExceptionHandler {
  private WebDriver driver;
  private Logger logger;
  
  public SeleniumExceptionHandler(WebDriver driver) {
    this.driver = driver;
    this.logger = LoggerFactory.getLogger(SeleniumExceptionHandler.class);
  }
  
  // Handle any exception gracefully
  public <T> T executeWithErrorHandling(Function<WebDriver, T> action,
                                        String actionDescription) {
    try {
      return action.apply(driver);
    } catch (NoSuchElementException e) {
      logger.error("Element not found: " + actionDescription, e);
      takeScreenshot(actionDescription + "_NoSuchElement");
      throw new RuntimeException("Element not found", e);
    } catch (TimeoutException e) {
      logger.error("Timeout waiting for: " + actionDescription, e);
      takeScreenshot(actionDescription + "_Timeout");
      throw new RuntimeException("Operation timeout", e);
    } catch (StaleElementReferenceException e) {
      logger.error("Stale element: " + actionDescription, e);
      // Retry once
      return action.apply(driver);
    } catch (UnhandledAlertException e) {
      logger.error("Unhandled alert during: " + actionDescription, e);
      try {
        Alert alert = driver.switchTo().alert();
        alert.accept();
      } catch (Exception ex) {
        logger.warn("Failed to dismiss alert", ex);
      }
      return null;
    } catch (InvalidElementStateException e) {
      logger.error("Invalid element state: " + actionDescription, e);
      takeScreenshot(actionDescription + "_InvalidState");
      throw new RuntimeException("Invalid element state", e);
    } catch (WebDriverException e) {
      logger.error("WebDriver exception: " + e.getMessage(), e);
      takeScreenshot(actionDescription + "_WebDriverException");
      
      // Check if session is lost
      if (e.getMessage().contains("session")) {
        logger.info("Session lost, reinitializing...");
        reinitializeDriver();
      }
      throw e;
    } catch (Exception e) {
      logger.error("Unexpected error: " + actionDescription, e);
      takeScreenshot(actionDescription + "_UnexpectedError");
      throw new RuntimeException("Unexpected error", e);
    }
  }
  
  // Specific methods for common operations
  public void clickWithErrorHandling(By locator, String elementName) {
    executeWithErrorHandling(driver -> {
      driver.findElement(locator).click();
      return null;
    }, "Click " + elementName);
  }
  
  public void fillWithErrorHandling(By locator, String text, String fieldName) {
    executeWithErrorHandling(driver -> {
      WebElement element = driver.findElement(locator);
      element.clear();
      element.sendKeys(text);
      return null;
    }, "Fill " + fieldName);
  }
  
  public WebElement getElementWithErrorHandling(By locator, String elementName) {
    return executeWithErrorHandling(driver -> {
      WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
      return wait.until(ExpectedConditions.presenceOfElementLocated(locator));
    }, "Get " + elementName);
  }
  
  // Take screenshot for debugging
  private void takeScreenshot(String filename) {
    try {
      File screenshot = ((TakesScreenshot) driver)
        .getScreenshotAs(OutputType.FILE);
      String filepath = "target/screenshots/" + filename + ".png";
      new File("target/screenshots").mkdirs();
      Files.copy(screenshot.toPath(), Paths.get(filepath));
      logger.info("Screenshot saved: " + filepath);
    } catch (Exception e) {
      logger.warn("Failed to take screenshot", e);
    }
  }
  
  // Reinitialize driver if session is lost
  private void reinitializeDriver() {
    try {
      driver.quit();
    } catch (Exception e) {
      logger.warn("Error closing driver", e);
    }
    // Create new driver (implementation specific)
  }
}

// USAGE
@Test
public void testWithErrorHandling() {
  WebDriver driver = new ChromeDriver();
  SeleniumExceptionHandler errorHandler = new SeleniumExceptionHandler(driver);
  
  driver.get("https://example.com");
  
  // All operations are wrapped with error handling
  errorHandler.fillWithErrorHandling(
    By.id("email"), 
    "user@test.com", 
    "Email field"
  );
  
  errorHandler.clickWithErrorHandling(
    By.id("login"),
    "Login button"
  );
  
  WebElement result = errorHandler.getElementWithErrorHandling(
    By.id("result"),
    "Result message"
  );
  
  driver.quit();
}

// Exception recovery map
public class ExceptionRecoveryMap {
  private Map<Class<? extends Exception>, Consumer<WebDriver>> recoveryStrategies;
  
  public ExceptionRecoveryMap() {
    this.recoveryStrategies = new HashMap<>();
    setupRecoveryStrategies();
  }
  
  private void setupRecoveryStrategies() {
    recoveryStrategies.put(UnhandledAlertException.class, driver -> {
      try {
        driver.switchTo().alert().accept();
      } catch (Exception e) {
        // Ignore
      }
    });
    
    recoveryStrategies.put(StaleElementReferenceException.class, driver -> {
      // Reload page
      driver.navigate().refresh();
    });
    
    recoveryStrategies.put(SessionNotCreatedException.class, driver -> {
      // Restart driver
      driver.quit();
    });
  }
  
  public void recover(Exception e, WebDriver driver) {
    Consumer<WebDriver> strategy = recoveryStrategies.get(e.getClass());
    if (strategy != null) {
      strategy.accept(driver);
    }
  }
}
```

---

### Q15. How do you implement proper logging and reporting in Selenium? What frameworks would you use?
**Answer:**
```java
// LOGGING SETUP WITH LOG4J

// log4j2.xml configuration
/*
<?xml version="1.0" encoding="UTF-8"?>
<Configuration packages="org.apache.logging.log4j.core">
  <Appenders>
    <File name="FileAppender" fileName="logs/test.log">
      <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
    </File>
    <Console name="ConsoleAppender" target="SYSTEM_OUT">
      <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
    </Console>
  </Appenders>
  <Loggers>
    <Logger name="com.test" level="INFO"/>
    <Root level="INFO">
      <AppenderRef ref="FileAppender"/>
      <AppenderRef ref="ConsoleAppender"/>
    </Root>
  </Loggers>
</Configuration>
*/

// Basic logging
public class TestBase {
  protected WebDriver driver;
  protected Logger logger = LoggerFactory.getLogger(this.getClass());
  
  @Before
  public void setUp() {
    logger.info("Starting test: " + this.getClass().getName());
    driver = new ChromeDriver();
  }
  
  @After
  public void tearDown() {
    logger.info("Ending test: " + this.getClass().getName());
    if (driver != null) {
      driver.quit();
    }
  }
  
  @Test
  public void testLogin() {
    logger.info("Navigating to login page");
    driver.get("https://example.com/login");
    
    logger.info("Entering credentials");
    driver.findElement(By.id("email")).sendKeys("user@test.com");
    driver.findElement(By.id("password")).sendKeys("password");
    
    logger.info("Clicking login button");
    driver.findElement(By.id("login")).click();
    
    logger.info("Verifying dashboard");
    assertTrue(driver.getCurrentUrl().contains("dashboard"));
  }
}

// EXTENT REPORTS - Beautiful HTML reports
public class ExtentReportManager {
  private static ExtentReports extent;
  private static ThreadLocal<ExtentTest> test = new ThreadLocal<>();
  
  public static void initReports() {
    String reportPath = "target/extentReports/report.html";
    ExtentHtmlReporter htmlReporter = new ExtentHtmlReporter(reportPath);
    
    extent = new ExtentReports();
    extent.attachReporter(htmlReporter);
    
    // System info
    extent.setSystemInfo("OS", System.getProperty("os.name"));
    extent.setSystemInfo("Java Version", System.getProperty("java.version"));
    extent.setSystemInfo("Test Environment", "Staging");
  }
  
  public static void createTest(String testName) {
    ExtentTest extentTest = extent.createTest(testName);
    test.set(extentTest);
  }
  
  public static void logInfo(String message) {
    test.get().info(message);
  }
  
  public static void logPass(String message) {
    test.get().pass(message);
  }
  
  public static void logFail(String message, Throwable t) {
    test.get().fail(message);
    test.get().fail(t);
  }
  
  public static void attachScreenshot(WebDriver driver, String screenshotName) {
    try {
      File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
      String path = "target/screenshots/" + screenshotName + ".png";
      new File("target/screenshots").mkdirs();
      Files.copy(src.toPath(), Paths.get(path));
      test.get().addScreenCaptureFromPath(path);
    } catch (IOException e) {
      logFail("Failed to capture screenshot", e);
    }
  }
  
  public static void flushReports() {
    extent.flush();
  }
}

// Usage with Extent Reports
public class LoginTest {
  private WebDriver driver;
  
  @BeforeClass
  public static void setupReporting() {
    ExtentReportManager.initReports();
  }
  
  @BeforeMethod
  public void setup() {
    driver = new ChromeDriver();
  }
  
  @Test
  public void testLoginSuccess() {
    ExtentReportManager.createTest("testLoginSuccess");
    
    try {
      ExtentReportManager.logInfo("Navigating to login page");
      driver.get("https://example.com/login");
      
      ExtentReportManager.logInfo("Entering email");
      driver.findElement(By.id("email")).sendKeys("user@test.com");
      
      ExtentReportManager.logInfo("Entering password");
      driver.findElement(By.id("password")).sendKeys("password123");
      
      ExtentReportManager.logInfo("Clicking login button");
      driver.findElement(By.id("login")).click();
      
      ExtentReportManager.logInfo("Verifying dashboard page");
      assertTrue(driver.getCurrentUrl().contains("dashboard"));
      
      ExtentReportManager.logPass("Login successful");
      ExtentReportManager.attachScreenshot(driver, "login_success");
    } catch (Exception e) {
      ExtentReportManager.logFail("Test failed", e);
      ExtentReportManager.attachScreenshot(driver, "login_failure");
      throw e;
    }
  }
  
  @AfterClass
  public static void tearDownReporting() {
    ExtentReportManager.flushReports();
  }
}

// ALLURE REPORTS - Advanced reporting
public class AllureReportTest {
  private WebDriver driver;
  
  @BeforeMethod
  public void setup() {
    driver = new ChromeDriver();
  }
  
  @Test
  @DisplayName("User can login with valid credentials")
  @Severity(SeverityLevel.BLOCKER)
  @Feature("Authentication")
  @Story("User Login")
  public void testLoginWithAllure() {
    Allure.step("Navigate to login page", () -> {
      driver.get("https://example.com/login");
    });
    
    Allure.step("Enter email address", () -> {
      driver.findElement(By.id("email")).sendKeys("user@test.com");
    });
    
    Allure.step("Enter password", () -> {
      driver.findElement(By.id("password")).sendKeys("password123");
    });
    
    Allure.step("Click login button", () -> {
      driver.findElement(By.id("login")).click();
    });
    
    Allure.step("Verify dashboard page", () -> {
      assertTrue(driver.getCurrentUrl().contains("dashboard"));
    });
  }
  
  // Add screenshot on failure
  @AfterMethod
  public void tearDown(ITestResult result) {
    if (result.getStatus() == ITestResult.FAILURE) {
      try {
        File screenshot = ((TakesScreenshot) driver)
          .getScreenshotAs(OutputType.FILE);
        Allure.addAttachment("Failure Screenshot",
          new FileInputStream(screenshot),
          "image/png");
      } catch (Exception e) {
        e.printStackTrace();
      }
    }
    
    driver.quit();
  }
}

// CUSTOM REPORTING UTILITY
public class TestReporter {
  private List<TestLog> logs = new ArrayList<>();
  private LocalDateTime testStartTime;
  private String testName;
  
  public TestReporter(String testName) {
    this.testName = testName;
    this.testStartTime = LocalDateTime.now();
  }
  
  public void log(String level, String message) {
    TestLog log = new TestLog(
      LocalDateTime.now(),
      level,
      message,
      Thread.currentThread().getStackTrace()[2].getMethodName()
    );
    logs.add(log);
    System.out.println("[" + level + "] " + message);
  }
  
  public void info(String message) {
    log("INFO", message);
  }
  
  public void pass(String message) {
    log("PASS", message);
  }
  
  public void fail(String message) {
    log("FAIL", message);
  }
  
  public void screenshot(WebDriver driver, String filename) {
    try {
      File src = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
      String path = "target/screenshots/" + testName + "_" + filename + ".png";
      new File("target/screenshots").mkdirs();
      Files.copy(src.toPath(), Paths.get(path));
      log("INFO", "Screenshot saved: " + path);
    } catch (IOException e) {
      log("ERROR", "Failed to save screenshot: " + e.getMessage());
    }
  }
  
  public void generateReport() {
    // Generate HTML report
    StringBuilder html = new StringBuilder();
    html.append("<html><body>");
    html.append("<h1>Test Report: ").append(testName).append("</h1>");
    html.append("<table border='1'>");
    html.append("<tr><th>Timestamp</th><th>Level</th><th>Message</th></tr>");
    
    for (TestLog log : logs) {
      html.append("<tr>");
      html.append("<td>").append(log.timestamp).append("</td>");
      html.append("<td>").append(log.level).append("</td>");
      html.append("<td>").append(log.message).append("</td>");
      html.append("</tr>");
    }
    
    html.append("</table></body></html>");
    
    try {
      Files.write(
        Paths.get("target/" + testName + "_report.html"),
        html.toString().getBytes()
      );
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
  
  static class TestLog {
    LocalDateTime timestamp;
    String level;
    String message;
    String methodName;
    
    TestLog(LocalDateTime timestamp, String level, String message, String methodName) {
      this.timestamp = timestamp;
      this.level = level;
      this.message = message;
      this.methodName = methodName;
    }
  }
}

// Usage
@Test
public void testWithCustomReporting() {
  TestReporter reporter = new TestReporter("LoginTest");
  WebDriver driver = new ChromeDriver();
  
  try {
    reporter.info("Starting login test");
    driver.get("https://example.com/login");
    
    reporter.info("Filling login form");
    driver.findElement(By.id("email")).sendKeys("user@test.com");
    driver.findElement(By.id("password")).sendKeys("password");
    
    reporter.info("Submitting login");
    driver.findElement(By.id("login")).click();
    
    reporter.screenshot(driver, "after_login");
    reporter.pass("Login successful");
    
  } catch (Exception e) {
    reporter.fail("Test failed: " + e.getMessage());
    reporter.screenshot(driver, "error");
  } finally {
    reporter.generateReport();
    driver.quit();
  }
}

// DEPENDENCIES for pom.xml:
/*
<dependency>
  <groupId>org.apache.logging.log4j</groupId>
  <artifactId>log4j-core</artifactId>
  <version>2.17.0</version>
</dependency>

<dependency>
  <groupId>com.aventstack</groupId>
  <artifactId>extentreports</artifactId>
  <version>5.0.9</version>
</dependency>

<dependency>
  <groupId>io.qameta.allure</groupId>
  <artifactId>allure-testng</artifactId>
  <version>2.21.0</version>
</dependency>
*/
```

---

This completes the comprehensive Selenium advanced interview questions covering Q1-Q15 with detailed technical answers and code examples.

Due to length constraints, I've covered the most critical 15 questions. The remaining Q16-Q50 would cover:
- Selenium Grid advanced configurations
- Cross-browser testing strategies
- Performance optimization
- API testing with Selenium
- Database integration
- Advanced framework design
- CI/CD integration
- Mobile testing
- Visual regression testing
- And more...

Would you like me to continue with Q16-Q50 or create a separate document for those?

