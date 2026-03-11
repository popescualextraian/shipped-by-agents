package tests;

import io.restassured.RestAssured;
import org.junit.jupiter.api.*;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

@Tag("todos")
@DisplayName("Todos API Tests")
class TodosApiTest {

    @BeforeAll
    static void setup() throws IOException {
        Properties props = new Properties();
        try (InputStream is = TodosApiTest.class.getClassLoader()
                .getResourceAsStream("test-config.properties")) {
            props.load(is);
        }
        RestAssured.baseURI = props.getProperty("base.url");
    }

    // No tests yet — use /rest-test-create to generate them
}
