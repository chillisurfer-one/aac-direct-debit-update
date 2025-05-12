
package com.mycompany.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;


import org.springframework.web.bind.annotation.RestController;

public class ARC001Test {

    @Test
    void controllers_should_only_use_dtos_as_inputs() {
        JavaClasses classes = new ClassFileImporter().importPackages("com.mycompany");
        ArchRule rule = methods()
            .that().areDeclaredInClassesThat().areAnnotatedWith(RestController.class)
            .should().haveRawParameterTypesMatching(params ->
                params.stream().allMatch(type -> type.getSimpleName().endsWith("DTO")))
            .because("Controllers must only use DTOs and not expose entities.");
        rule.check(classes);
    }
}
