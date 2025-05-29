# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-05-29 15:06:09

## Summary of Compliance

| Policy ID      | Compliance Status |
|----------------|-------------------|
| ARC-POLICY-101      | ✅ Yes    |
| ARC-POLICY-102      | ❌ No    |
| ARC-POLICY-103      | ❌ No    |
| ARC-POLICY-104      | ✅ Yes    |
| ARC-POLICY-105      | ✅ Yes    |
| ARC-POLICY-106      | ✅ Yes    |
| ARC-POLICY-108      | ✅ Yes    |

## Detailed Policy Evaluations

### Non-Compliant Policies

#### ARC-POLICY-102 - ❌ NON-COMPLIANT

**Evaluation Details:**
Compliance: No

Deviations:
- 1: The UML diagram shows a relationship from `ThoughtMachine` (an external system) to `AdapterClient`, which is not listed in the policy input JSON. This relationship is not mediated by an `ApiGateway`, violating the policy rule that external systems must not connect directly to non-API-Gateway components.

Suggestions:
- 1: Ensure that all external systems, such as `ThoughtMachine`, interact with internal services through an `ApiGateway`. Modify the architecture to route the `ThoughtMachine` interactions through an `ApiGateway` or update the policy to include `ThoughtMachine` as an allowed external system if this is intentional and secure.

Conclusion: The architecture does not comply with the policy due to the direct connection from an external system to an internal component without using an `ApiGateway`.

---

#### ARC-POLICY-103 - ❌ NON-COMPLIANT

**Evaluation Details:**
Compliance: No

Deviations:
- 1: The UML diagram indicates that the "MandateUpdateService" container has a relationship with the "ThoughtMachine" external system. This violates the policy rule which states that only the "VaultCoreClient" adapter is allowed to connect to the "ThoughtMachine" external system. The policy logic explicitly checks that any connection to "ThoughtMachine" must originate from "VaultCoreClient" and not from any other source.

Suggestions:
- 1: To comply with the policy, remove the direct connection from "MandateUpdateService" to "ThoughtMachine". Instead, ensure that all interactions with "ThoughtMachine" are routed through the "VaultCoreClient". This can be achieved by modifying the "MandateUpdateService" to call "VaultCoreClient" for any operations that require access to "ThoughtMachine". This change will align the architecture with the policy requirement that only "VaultCoreClient" can directly interact with "ThoughtMachine".

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, and VaultCoreClient) are defined within a system boundary labeled "ecs," which aligns with the policy requirement that containers must be deployed in ECS Fargate. Therefore, there are no deviations from the policy.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy checks if any container making an external call is not marked with the stereotype `<<uses_secret>>`. In the UML diagram, the `VaultCoreClient` container makes an external call to `ThoughtMachine` and is correctly annotated with the stereotype `<<uses_secret>>`. Therefore, there are no deviations from the policy, and the architecture is compliant.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram includes an "Audit Log" container with the technology "Amazon RDS PostgreSQL" and the stereotype "data_store," which satisfies the policy requirement for a data store related to audit or logging. Therefore, the architecture complies with the policy ARC-POLICY-105, and no deviations are present.

---

#### ARC-POLICY-106 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy requires that at least one container must have 'secrets' in the name or be labeled <<secrets_store>>. The UML diagram includes a container named "AWS Secrets Manager" with the stereotype <<secrets_store>>, which satisfies the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-108 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided policy. The policy requires at least one container to be labeled as <<observability>> or include 'cloudwatch' in the name. The UML diagram includes the "Amazon CloudWatch" container, which is labeled with the stereotype <<observability>>, satisfying the policy requirement. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

