package com.framework.datadriven.tests;

import com.framework.datadriven.utils.ExcelReader;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class LoginTest {

    /**
     * ADVANCED CONCEPT: @DataProvider separating Data from Logic.
     * This method fetches data from our Excel utility. The test method knows NOTHING
     * about Apache POI or how the data is retrieved.
     */
    @DataProvider(name = "loginData")
    public Object[][] getLoginData() {
        String excelPath = "src/test/resources/testdata/LoginData.xlsx";
        return ExcelReader.getExcelData(excelPath, "ValidUsers");
    }

    /**
     * The Test Method simply accepts parameters matching the columns of the DataProvider.
     * If the Excel has 10 rows, this test will execute 10 separate times automatically!
     */
    @Test(dataProvider = "loginData")
    public void testLogin(String username, String password) {
        System.out.println("Executing login test with:");
        System.out.println("Username: " + username);
        System.out.println("Password: " + password);
        
        // WebDriver logic would go here:
        // driver.findElement(By.id("user")).sendKeys(username);
        // driver.findElement(By.id("pass")).sendKeys(password);
        // driver.findElement(By.id("loginBtn")).click();
        
        System.out.println("-------------------------------------------------");
    }
}
