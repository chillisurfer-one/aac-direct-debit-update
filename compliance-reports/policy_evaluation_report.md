# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-30 10:06:15

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
- 1: The UML diagram shows a relationship where the `MandateUpdateService` container directly accesses the `ThoughtMachine` external system. This violates the policy which states that only the `VaultCoreClient` adapter is allowed to connect to the `ThoughtMachine` external system. The policy logic explicitly checks that the source of any connection to `ThoughtMachine` must be `VaultCoreClient`, and any other source is flagged as non-compliant.

Suggestions:
- 1: Modify the UML diagram to ensure that the `MandateUpdateService` does not directly connect to `ThoughtMachine`. Instead, route the connection through the `VaultCoreClient` adapter. This can be achieved by having `MandateUpdateService` call `VaultCoreClient`, which then performs the mandate update with `ThoughtMachine`. This change will align the architecture with the policy requirements, ensuring that all interactions with `ThoughtMachine` are mediated through `VaultCoreClient`.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

Conclusion: The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, VaultCoreClient) are defined within a system boundary labeled "ecs," which meets the policy requirement for deployment in ECS Fargate.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy specifies that external systems should not connect directly to non-API-Gateway components. In the UML diagram, the external system "ClientApp" connects to "ApiGateway," which is an allowed API Gateway alias. All other connections from "ApiGateway" to internal components are compliant with the policy. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The `VaultCoreClient` container, which makes an external call to the `ThoughtMachine` system, is correctly annotated with the stereotype `<<uses_secret>>`, indicating that it uses secrets. This satisfies the policy requirement that any container making external calls must be marked as using secrets. Therefore, there are no deviations from the policy, and the architecture is compliant.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires the architecture to include a data store related to audit or logging, specifically mentioning technologies like PostgreSQL or RDS, or having a stereotype of "data_store". The UML diagram includes an "Audit Log" container with the technology "Amazon RDS PostgreSQL" and a stereotype of "data_store", which satisfies the policy requirements. Therefore, there are no deviations from the policy, and the architecture is compliant.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires that at least one container must have 'secrets' in the name or be labeled <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the stereotype <<secrets_store>>, which satisfies the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for fixes are necessary.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the policy ARC-POLICY-108. The policy requires at least one container to be labeled as <<observability>> or include 'cloudwatch' in the name. The UML diagram includes the "Amazon CloudWatch" container, which is labeled with the stereotype <<observability>>, fulfilling the policy requirement. Therefore, there are no deviations from the policy.

---

