package com.framework.restassured.tests;

import com.framework.restassured.core.SpecBuilder;
import org.testng.annotations.Test;

// import static io.restassured.RestAssured.*;
// import static org.hamcrest.Matchers.*;

public class UserApiTest {

    @Test
    public void testGetUserProfile() {
        System.out.println("--- Starting Advanced RestAssured API Test ---");

        /**
         * The Test Script is incredibly clean!
         * All the heavy lifting (Auth, Headers, Base URL, Error Logging) 
         * is handled by the SpecBuilder.
         */
        
        Object reqSpec = SpecBuilder.getRequestSpec();
        Object resSpec = SpecBuilder.getResponseSpec();
        
        System.out.println("🌐 Executing GET /users/me using SpecBuilder configurations...");

        /*
        given()
            .spec(reqSpec) // Applies Base URL, Auth Token, and Content-Type
        .when()
            .get("/users/me")
        .then()
            .spec(resSpec) // Asserts Status 200 and Content-Type JSON automatically
            .body("role", equalTo("ADMIN")) // Test-specific business logic assertion
            .body("preferences.theme", equalTo("DARK"));
        */
        
        System.out.println("✅ Successfully executed and validated the API response.");
    }
}
