
package com.mycompany.architecture;

import com.tngtech.archunit.core.domain.JavaAnnotation;
import com.tngtech.archunit.core.domain.JavaClass;
import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchCondition;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;

public class ARC006Test {

    @Test
    void rest_controllers_should_be_versioned() {
        JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany");

        ArchRule rule = classes()
            .that().areAnnotatedWith(RestController.class)
            .should(new ArchCondition<>("have @RequestMapping starting with /api/v1") {
                @Override
                public void check(JavaClass controller, ConditionEvents events) {
                    Optional<JavaAnnotation<JavaClass>> annotation =
                        controller.tryGetAnnotationOfType(RequestMapping.class);
                    if (annotation.isPresent()) {
                        String value = annotation.get().get("value").toString();
                        if (!value.contains("/api/v1")) {
                            String message = String.format("Controller %s does not use versioned API path.", controller.getName());
                            events.add(SimpleConditionEvent.violated(controller, message));
                        }
                    } else {
                        String message = String.format("Controller %s is missing @RequestMapping", controller.getName());
                        events.add(SimpleConditionEvent.violated(controller, message));
                    }
                }
            }).because("All APIs must be versioned using '/api/v1/' convention.");
        rule.check(classes);
    }
}
