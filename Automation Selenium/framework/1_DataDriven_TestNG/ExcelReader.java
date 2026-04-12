package com.framework.datadriven.utils;

import java.io.FileInputStream;
import java.io.IOException;
// Note: Requires Apache POI dependencies in pom.xml

/**
 * ExcelReader Utility Class
 * Abstracting away the complexity of Apache POI to provide simple data to TestNG DataProviders.
 */
public class ExcelReader {
    
    /**
     * Reads an Excel sheet and returns a 2D Object array suitable for TestNG's @DataProvider.
     * 
     * @param filePath Path to the Excel file
     * @param sheetName Name of the sheet to read
     * @return 2D array representing rows and columns of data
     */
    public static Object[][] getExcelData(String filePath, String sheetName) {
        Object[][] data = null;
        try {
            FileInputStream fis = new FileInputStream(filePath);
            // Mocking POI logic for illustration:
            // XSSFWorkbook workbook = new XSSFWorkbook(fis);
            // XSSFSheet sheet = workbook.getSheet(sheetName);
            // int rowCount = sheet.getPhysicalNumberOfRows();
            // int colCount = sheet.getRow(0).getLastCellNum();
            
            int rowCount = 3; // Mocked
            int colCount = 2; // Mocked
            
            data = new Object[rowCount - 1][colCount]; // Excluding header row
            
            // Loop through rows and columns to populate the data array
            // for(int i=1; i<rowCount; i++) {
            //      for(int j=0; j<colCount; j++) {
            //          data[i-1][j] = sheet.getRow(i).getCell(j).toString();
            //      }
            // }
            
            // Mocked Data
            data[0][0] = "admin";    data[0][1] = "pass123";
            data[1][0] = "invalid";  data[1][1] = "wrong";
            
            // workbook.close();
            fis.close();
            
        } catch (IOException e) {
            e.printStackTrace();
        }
        return data;
    }
}
