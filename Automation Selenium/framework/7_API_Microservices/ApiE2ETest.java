package com.framework.api;

import org.testng.annotations.Test;
// Mocking RestAssured imports for illustration
// import static io.restassured.RestAssured.*;
// import static org.hamcrest.Matchers.*;

/**
 * RestAssured API Test using modern BDD Syntax (Given/When/Then).
 */
public class ApiE2ETest {

    @Test
    public void testCreateAndVerifyUser() {
        
        // 1. Serialization: Java POJO to JSON automatically handled by RestAssured + Jackson/Gson
        UserPayload newUser = new UserPayload("Morpheus", "Leader");
        
        System.out.println("🌐 [API Test] Sending POST request to /api/users with payload: " + newUser.getName());
        
        /**
         * ADVANCED CONCEPT: RestAssured Given/When/Then syntax
         * This code is mocked to demonstrate the structure without failing compilation
         * due to missing RestAssured jars in this demo directory.
         */
        
        /* 
        int userId = 
            given()
                .baseUri("https://reqres.in")
                .header("Content-Type", "application/json")
                .body(newUser) // Auto-serializes the POJO
            .when()
                .post("/api/users")
            .then()
                .statusCode(201) // Assert HTTP 201 Created
                .body("name", equalTo("Morpheus")) // Hamcrest Matcher assertion
                .extract().path("id"); // Extract generated ID for chaining
        
        System.out.println("✅ User created successfully with ID: " + userId);
        
        // 2. Chaining: Use the extracted ID for a GET request
        given()
            .baseUri("https://reqres.in")
            .pathParam("userId", userId)
        .when()
            .get("/api/users/{userId}")
        .then()
            .statusCode(200);
        */
        
        System.out.println("✅ [API Test] Simulated validation of status code 201 and 200 via API chaining.");
    }
}
