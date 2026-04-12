# 🕸️ GraphQL Testing Framework (Advanced API)

## 📌 Core Concept
REST APIs are rigid: a specific endpoint (`/users/1`) always returns a fixed structure. If a UI only needs the user's name, REST suffers from **Over-fetching** (sending 50 other fields) or requires creating a custom endpoint (`/users/1/nameOnly`).

**GraphQL** solves this by exposing a *single* endpoint (e.g., `POST /graphql`). The client sends a specific "Query" string detailing exactly which fields it wants. The server responds with *only* those fields. Testing GraphQL requires constructing this specific JSON payload containing the `query` and `variables`.

### 🛠️ Architecture Components
1.  **GraphQLRequest POJO:** A Java class that mirrors the required GraphQL JSON structure (`{"query": "...", "variables": {...}}`).
2.  **Query Strings:** Multi-line strings (or read from `.graphql` files on disk) that define the specific graph traversal.
3.  **RestAssured Validation:** GraphQL responses always return HTTP 200 (even on errors!) unless there's a network failure. The actual errors are inside the JSON payload under an `"errors"` array. Validation requires specifically parsing the `"data"` or `"errors"` JSON objects.

### 🌟 Advantages for SDETs
*   **Exact Data Validation:** You test exactly what the frontend is requesting, ensuring backend efficiency.
*   **Schema Introspection:** GraphQL APIs are self-documenting. An SDET can query the API to return its entire schema, instantly generating automation tests for newly added fields.

---

## 🧠 Memory Trick for Interviews
### The "Buffet vs. Personal Chef" 🍽️
*   **REST (The Buffet):** You go to the `/user` buffet line. You only want a slice of pizza, but the waiter forces you to take a plate with pizza, salad, soup, and dessert (Over-fetching).
*   **GraphQL (The Personal Chef):** You hand the chef a specific list (`query`): "I want 1 slice of pizza." The chef prepares *exactly* that and hands you a plate containing only pizza.
*   **Key Phrase:** *"Unlike REST's rigid endpoints, GraphQL utilizes a single endpoint where the client specifies the exact data shape required via a query string. Framework validation must account for parsing the nested 'data' object and checking for inner 'errors' arrays, as HTTP 200 is returned regardless of business logic failure."*