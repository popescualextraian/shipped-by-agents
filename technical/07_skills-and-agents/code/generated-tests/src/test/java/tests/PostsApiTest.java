package tests;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.*;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

@Tag("posts")
@DisplayName("Posts API Tests")
class PostsApiTest {

    @BeforeAll
    static void setup() throws IOException {
        Properties props = new Properties();
        try (InputStream is = PostsApiTest.class.getClassLoader()
                .getResourceAsStream("test-config.properties")) {
            props.load(is);
        }
        RestAssured.baseURI = props.getProperty("base.url");
    }

    @Test
    @DisplayName("GET /posts returns all posts with status 200")
    void should_returnAllPosts_whenGetPosts() {
        given()
            .contentType(ContentType.JSON)
        .when()
            .get("/posts")
        .then()
            .statusCode(200)
            .body("size()", equalTo(100))
            .body("[0].id", notNullValue())
            .body("[0].title", notNullValue())
            .body("[0].body", notNullValue())
            .body("[0].userId", notNullValue());
    }

    @Test
    @DisplayName("GET /posts/{id} returns a single post")
    void should_returnSinglePost_whenGetPostById() {
        given()
            .contentType(ContentType.JSON)
        .when()
            .get("/posts/1")
        .then()
            .statusCode(200)
            .body("id", equalTo(1))
            .body("userId", equalTo(1))
            .body("title", notNullValue())
            .body("body", notNullValue());
    }

    @Test
    @DisplayName("POST /posts creates a new post and returns 201")
    void should_createPost_whenPostPosts() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {
                    "title": "test post",
                    "body": "test body",
                    "userId": 1
                }
                """)
        .when()
            .post("/posts")
        .then()
            .statusCode(201)
            .body("id", notNullValue())
            .body("title", equalTo("test post"))
            .body("body", equalTo("test body"))
            .body("userId", equalTo(1));
    }

    @Test
    @DisplayName("PUT /posts/{id} updates an existing post")
    void should_updatePost_whenPutPost() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {
                    "id": 1,
                    "title": "updated title",
                    "body": "updated body",
                    "userId": 1
                }
                """)
        .when()
            .put("/posts/1")
        .then()
            .statusCode(200)
            .body("title", equalTo("updated title"))
            .body("body", equalTo("updated body"));
    }

    @Test
    @DisplayName("DELETE /posts/{id} returns 200")
    void should_return200_whenDeletePost() {
        when()
            .delete("/posts/1")
        .then()
            .statusCode(200);
    }
}
