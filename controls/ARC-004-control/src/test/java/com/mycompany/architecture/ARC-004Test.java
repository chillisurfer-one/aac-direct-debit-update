
package com.mycompany.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;


import org.springframework.web.bind.annotation.ControllerAdvice;

public class ARC004Test {

    @Test
    void controller_advice_should_exist() {
        JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany");
        ArchRule rule = classes()
            .that().areAnnotatedWith(ControllerAdvice.class)
            .should().exist()
            .because("Centralized error handling via @ControllerAdvice is required.");
        rule.check(classes);
    }
}
