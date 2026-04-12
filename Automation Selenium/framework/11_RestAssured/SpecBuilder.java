package com.framework.restassured.core;

// import io.restassured.builder.RequestSpecBuilder;
// import io.restassured.builder.ResponseSpecBuilder;
// import io.restassured.http.ContentType;
// import io.restassured.specification.RequestSpecification;
// import io.restassured.specification.ResponseSpecification;

/**
 * ADVANCED CONCEPT: Request and Response Specifications.
 * Instead of repeating the Base URL, Content-Type, Authorization tokens, 
 * and logging configurations in every single test method, we build reusable 
 * specifications. This adheres to the DRY (Don't Repeat Yourself) principle.
 */
public class SpecBuilder {

    // Mocking the return types for compilation purposes
    public static Object getRequestSpec() {
        System.out.println("🔧 Building Reusable Request Specification (BaseURL, Auth Token, Logging)...");
        
        /*
        return new RequestSpecBuilder()
                .setBaseUri("https://api.example.com")
                .setBasePath("/v1")
                .setContentType(ContentType.JSON)
                .addHeader("Authorization", "Bearer MOCKED_JWT_TOKEN")
                // Use a custom filter to log requests only if they fail, keeping CI logs clean!
                // .addFilter(new RequestLoggingFilter()) 
                .build();
        */
        return null;
    }

    public static Object getResponseSpec() {
        System.out.println("🛡️ Building Reusable Response Specification (Expect 200 OK, JSON Format)...");
        
        /*
        return new ResponseSpecBuilder()
                .expectStatusCode(200)
                .expectContentType(ContentType.JSON)
                // .expectResponseTime(lessThan(2000L)) // Fail test if API takes longer than 2 seconds
                .build();
        */
        return null;
    }
}
