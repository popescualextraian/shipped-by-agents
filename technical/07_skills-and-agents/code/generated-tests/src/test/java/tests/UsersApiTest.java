package tests;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.*;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

@Tag("users")
@DisplayName("Users API Tests")
class UsersApiTest {

    @BeforeAll
    static void setup() throws IOException {
        Properties props = new Properties();
        try (InputStream is = UsersApiTest.class.getClassLoader()
                .getResourceAsStream("test-config.properties")) {
            props.load(is);
        }
        RestAssured.baseURI = props.getProperty("base.url");
    }

    @Test
    @DisplayName("GET /users returns all users with status 200")
    void should_returnAllUsers_whenGetUsers() {
        given()
            .contentType(ContentType.JSON)
        .when()
            .get("/users")
        .then()
            .statusCode(200)
            .body("size()", equalTo(10))
            .body("[0].id", notNullValue())
            .body("[0].name", notNullValue())
            .body("[0].email", notNullValue());
    }
}
