# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-30 10:43:30

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
- 1: The `MandateUpdateService` container is directly accessing the `ThoughtMachine` external system. This violates the policy rule that only the `VaultCoreClient` adapter is allowed to connect to the `ThoughtMachine` external system. The policy explicitly checks for any source other than `VaultCoreClient` attempting to connect to `ThoughtMachine` and flags it as a violation.

Suggestions:
- 1: Modify the architecture so that the `MandateUpdateService` does not directly connect to the `ThoughtMachine` system. Instead, ensure that all interactions with `ThoughtMachine` are routed through the `VaultCoreClient` adapter. This can be achieved by having the `MandateUpdateService` call the `VaultCoreClient`, which then handles the communication with `ThoughtMachine`. This change will align the architecture with the policy requirements by ensuring that only the designated adapter (`VaultCoreClient`) interacts with the external system.

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, and VaultCoreClient) are defined within a system boundary labeled "ecs," which aligns with the policy requirement that microservices must be deployed in an ECS Fargate cluster. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram adheres to the provided OPA policy. The policy specifies that external systems must not connect directly to non-API-Gateway components. In the UML diagram, the only relationship involving an external system ("ClientApp") is with the "ApiGateway," which is an allowed destination according to the policy. All other connections follow the internal architecture and do not involve direct access from external systems to non-API-Gateway components. Therefore, the diagram is compliant with the policy.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy checks whether any container making an external call is not marked as using secrets. In this case, the `VaultCoreClient` container makes an external call to `ThoughtMachine` and is correctly annotated with the stereotype `<<uses_secret>>`, satisfying the policy requirements. Therefore, there are no deviations from the policy.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram includes an "Audit Log" component, which is an Amazon RDS PostgreSQL data store. This satisfies the policy requirement for a data store related to audit or logging, as it is explicitly named "Audit Log" and uses a technology that matches the policy criteria (PostgreSQL/RDS). Therefore, the architecture complies with the policy ARC-POLICY-105.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires that at least one container must have 'secrets' in the name or be labeled with the stereotype <<secrets_store>>. The input JSON indicates that the "AWS Secrets Manager" container is labeled with the stereotype <<secrets_store>>, satisfying the policy requirement. Therefore, there are no deviations, and the architecture is compliant.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires at least one container to be labeled as <<observability>> or include 'cloudwatch' in the name. The UML diagram includes the "Amazon CloudWatch" container, which is labeled with the stereotype <<observability>>, fulfilling the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for changes are needed.

---

