package com.framework.graphql;

/**
 * POJO for constructing a GraphQL Request payload.
 * Unlike REST (where the URL path defines the resource), GraphQL sends the Query
 * and optional Variables in a standard JSON body to a single endpoint (e.g., /graphql).
 */
public class GraphQLRequest {
    
    private String query;
    private Object variables;

    public GraphQLRequest(String query, Object variables) {
        this.query = query;
        this.variables = variables;
    }

    // Getters and setters (usually generated via Lombok @Data)
    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }
    public Object getVariables() { return variables; }
    public void setVariables(Object variables) { this.variables = variables; }
}
