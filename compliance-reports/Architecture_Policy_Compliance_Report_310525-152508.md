# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-31 15:25:07

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
- 1: The UML diagram shows a relationship where the `MandateUpdateService` container connects directly to the `ThoughtMachine` external system. This violates the policy rule which states that only the `VaultCoreClient` adapter is allowed to connect to the `ThoughtMachine` external system. The policy logic explicitly checks for any source other than `VaultCoreClient` connecting to `ThoughtMachine` and flags it as non-compliant.

Suggestions:
- 1: To fix this deviation, modify the UML diagram to ensure that the `MandateUpdateService` does not directly connect to `ThoughtMachine`. Instead, route the connection through the `VaultCoreClient` adapter. This can be achieved by having `MandateUpdateService` call `VaultCoreClient`, which then interacts with `ThoughtMachine`. Update the relationship in the UML diagram to reflect this change.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, VaultCoreClient) are defined within a system boundary labeled "ECS Fargate Cluster," which satisfies the policy requirement that containers must be deployed within a boundary prefixed with "ecs." Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram adheres to the provided OPA policy. The policy specifies that external systems must not connect directly to non-API-Gateway components. The relationships in the UML diagram show that the external system "ClientApp" connects to the "ApiGateway," which is compliant with the policy. There are no direct connections from external systems to non-API-Gateway components, thus satisfying the policy requirements.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The `VaultCoreClient` container, which makes an external call to the `ThoughtMachine` system, is correctly annotated with the `<<uses_secret>>` stereotype. This satisfies the policy requirement that any container making external calls must be marked as using secrets. Therefore, there are no deviations from the policy, and no further actions are needed.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram includes an "Audit Log" container, which is an "Amazon RDS PostgreSQL" data store. This satisfies the policy requirement for a data store related to audit or logging, as specified in the Rego policy. The provided input JSON correctly represents this container, and the expected policy output is an empty list, indicating compliance. Therefore, the architecture adheres to the policy ARC-POLICY-105.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires that at least one container must have 'secrets' in the name or be labeled with the stereotype <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the stereotype <<secrets_store>>, which satisfies the policy requirement. Therefore, there are no deviations, and the architecture is compliant.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the policy ARC-POLICY-108. The policy requires at least one container to be labeled as <<observability>> or include 'cloudwatch' in the name. The diagram includes the "Amazon CloudWatch" container, which is labeled with the stereotype <<observability>>, satisfying the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

