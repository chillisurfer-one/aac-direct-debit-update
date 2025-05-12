
package com.mycompany.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;


import org.springframework.web.bind.annotation.RestController;

public class ARC002Test {

    @Test
    void controllers_should_not_have_repository_fields() {
        JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany");
        ArchRule rule = noFields()
            .that().areDeclaredInClassesThat().areAnnotatedWith(RestController.class)
            .should().haveRawType().nameEndingWith("Repository")
            .because("Controllers should depend on services, not repositories directly.");
        rule.check(classes);
    }
}
