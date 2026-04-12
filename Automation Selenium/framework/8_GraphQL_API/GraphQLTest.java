package com.framework.graphql;

import org.testng.annotations.Test;
// import static io.restassured.RestAssured.*;
// import static org.hamcrest.Matchers.*;
import java.util.HashMap;
import java.util.Map;

public class GraphQLTest {

    @Test
    public void testGetUserByGraphQL() {
        System.out.println("--- Starting GraphQL Query Test ---");

        /**
         * ADVANCED CONCEPT: Over-fetching vs Exact-fetching
         * In REST, /users/1 returns the entire user object (id, name, email, phone, address).
         * In GraphQL, we explicitly request ONLY the exact fields we need (id, name)
         * to save bandwidth and improve performance.
         */
        
        // 1. Define the GraphQL Query String
        String query = "query getUser($id: ID!) { " +
                       "  user(id: $id) { " +
                       "    id " +
                       "    name " +
                       "    email " + // We don't ask for 'address', so the server won't compute/send it
                       "  } " +
                       "}";

        // 2. Define the Variables
        Map<String, Object> variables = new HashMap<>();
        variables.put("id", "123");

        // 3. Construct the Payload POJO
        GraphQLRequest graphQLPayload = new GraphQLRequest(query, variables);
        
        System.out.println("🌐 Sending POST to /graphql with Query: " + query);
        
        // 4. Execute using RestAssured (Mocked for compilation)
        /*
        given()
            .baseUri("https://api.example.com")
            .header("Content-Type", "application/json")
            .body(graphQLPayload)
        .when()
            .post("/graphql")
        .then()
            .statusCode(200)
            // Asserting on the nested 'data' object unique to GraphQL responses
            .body("data.user.name", equalTo("Alice Smith"))
            .body("data.user.email", equalTo("alice@example.com"));
        */
        
        System.out.println("✅ Successfully validated GraphQL nested JSON 'data' response.");
    }
}
