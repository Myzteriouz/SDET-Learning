package com.framework.keyworddriven.engine;

import org.openqa.selenium.WebDriver;
import java.lang.reflect.Method;

/**
 * The Execution Engine.
 * This class reads an Excel file where each row is a step, and dynamically invokes
 * the methods in ActionKeywords.java using Java Reflection.
 */
public class ExecutionEngine {
    
    private WebDriver driver;
    private ActionKeywords actionKeywords;

    public void executeTestCase(String excelFilePath) {
        // Mock initialization
        actionKeywords = new ActionKeywords(driver);
        
        // MOCK EXCEL DATA (Step, Keyword, LocatorType, LocatorValue, TestData)
        String[][] excelData = {
            {"Step1", "openBrowser", "", "", "chrome"},
            {"Step2", "navigate", "", "", "https://example.com/login"},
            {"Step3", "input", "id", "username", "admin"},
            {"Step4", "input", "id", "password", "supersecret"},
            {"Step5", "click", "xpath", "//button[@type='submit']", ""},
            {"Step6", "closeBrowser", "", "", ""}
        };

        System.out.println("🚀 Starting Keyword-Driven Execution Engine...");

        // Iterate through each row in the "Excel" sheet
        for (String[] row : excelData) {
            String keyword = row[1];
            String locatorType = row[2];
            String locatorValue = row[3];
            String data = row[4];

            /**
             * ADVANCED CONCEPT: Java Reflection API
             * We do not use massive switch/if-else statements here!
             * We look up the method name in the ActionKeywords class matching the 'keyword' string
             * from Excel, and invoke it dynamically.
             */
            executeReflection(keyword, locatorType, locatorValue, data);
        }
    }

    private void executeReflection(String keyword, String locatorType, String locatorValue, String data) {
        try {
            Method[] methods = actionKeywords.getClass().getMethods();
            for (Method method : methods) {
                if (method.getName().equalsIgnoreCase(keyword)) {
                    // Dynamically invoke based on parameter counts
                    if (method.getParameterCount() == 0) {
                        method.invoke(actionKeywords);
                    } else if (method.getParameterCount() == 1) {
                        method.invoke(actionKeywords, data); // e.g., openBrowser(data), navigate(data)
                    } else if (method.getParameterCount() == 2) {
                        method.invoke(actionKeywords, locatorType, locatorValue); // e.g., click(type, value)
                    } else if (method.getParameterCount() == 3) {
                        method.invoke(actionKeywords, locatorType, locatorValue, data); // e.g., input(type, value, data)
                    }
                    break; // Method found and executed
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    public static void main(String[] args) {
        new ExecutionEngine().executeTestCase("mock_path.xlsx");
    }
}
