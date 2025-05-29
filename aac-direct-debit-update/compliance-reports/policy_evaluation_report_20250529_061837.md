# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-29 06:18:49

## Summary of Compliance

| Policy ID      | Compliance Status |
|----------------|-------------------|
| ARC-POLICY-101      | ✅ Yes    |
| ARC-POLICY-102      | ✅ Yes    |
| ARC-POLICY-103      | ❌ No    |
| ARC-POLICY-104      | ✅ Yes    |
| ARC-POLICY-105      | ✅ Yes    |
| ARC-POLICY-106      | ✅ Yes    |
| ARC-POLICY-108      | ✅ Yes    |

## Detailed Policy Evaluations

### Non-Compliant Policies

#### ARC-POLICY-103 - ❌ NON-COMPLIANT

**Evaluation Details:**
Compliance: No

Deviations:
- 1: The UML diagram shows a relationship where the `MandateUpdateService` container connects directly to the `ThoughtMachine` external system. This violates the policy rule that only the `VaultCoreClient` adapter is allowed to connect to the `ThoughtMachine` external system. The policy logic explicitly restricts access to `ThoughtMachine` to only the `VaultCoreClient`.

Suggestions:
- 1: Modify the UML diagram to ensure that the `MandateUpdateService` does not directly connect to `ThoughtMachine`. Instead, route any interactions with `ThoughtMachine` through the `VaultCoreClient`. This can be achieved by having the `MandateUpdateService` call the `VaultCoreClient`, which then interacts with `ThoughtMachine`. Update the relationship in the UML diagram to reflect this change.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, VaultCoreClient) are defined within a system boundary labeled 'ecs', which satisfies the policy requirement that containers must be deployed in ECS Fargate. Therefore, there are no deviations from the policy, and no suggestions for fixes are necessary.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy specifies that external systems should not connect directly to non-API-Gateway components. In the UML diagram, the external system "ClientApp" connects to "ApiGateway," which is an approved API Gateway alias according to the policy. Therefore, there are no deviations from the policy, and the architecture is compliant.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy checks if any container making external calls is not annotated with the stereotype `<<uses_secret>>`. In the UML diagram, the `VaultCoreClient` container makes an external call to `ThoughtMachine` and is correctly annotated with the stereotype `<<uses_secret>>`, as confirmed by the policy input JSON. Therefore, there are no deviations from the policy.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram includes an "Audit Log" component, which is an "Amazon RDS PostgreSQL" data store with the stereotype "data_store." This satisfies the policy requirement for having a data store related to audit or logging, as specified in the Rego policy. Therefore, the architecture is compliant with the policy ARC-POLICY-105.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the policy ARC-POLICY-106. The policy requires that at least one container must have 'secrets' in the name or be labeled <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the alias "Secrets" and is labeled with the stereotype <<secrets_store>>, which satisfies the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for changes are needed.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires that at least one container must be labeled as <<observability>> or include 'cloudwatch' in the name. The input JSON indicates that the "Amazon CloudWatch" container is labeled with the stereotype "observability," satisfying the policy requirement. Therefore, there are no deviations, and the architecture is compliant.

---

