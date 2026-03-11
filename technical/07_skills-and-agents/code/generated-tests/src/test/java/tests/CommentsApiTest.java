package tests;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.*;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

@Tag("comments")
@DisplayName("Comments API Tests")
class CommentsApiTest {

    @BeforeAll
    static void setup() throws IOException {
        Properties props = new Properties();
        try (InputStream is = CommentsApiTest.class.getClassLoader()
                .getResourceAsStream("test-config.properties")) {
            props.load(is);
        }
        RestAssured.baseURI = props.getProperty("base.url");
    }

    @Test
    @DisplayName("GET /posts/{id}/comments returns comments for a post")
    void should_returnComments_whenGetCommentsByPostId() {
        given()
            .contentType(ContentType.JSON)
        .when()
            .get("/posts/1/comments")
        .then()
            .statusCode(200)
            .body("size()", greaterThan(0))
            .body("[0].postId", equalTo(1))
            .body("[0].id", notNullValue())
            .body("[0].name", notNullValue())
            .body("[0].email", notNullValue())
            .body("[0].body", notNullValue());
    }

    @Test
    @DisplayName("GET /comments?postId={id} returns filtered comments")
    void should_returnFilteredComments_whenGetCommentsWithPostIdParam() {
        given()
            .contentType(ContentType.JSON)
            .queryParam("postId", 1)
        .when()
            .get("/comments")
        .then()
            .statusCode(200)
            .body("size()", greaterThan(0))
            .body("postId", everyItem(equalTo(1)));
    }
}
