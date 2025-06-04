# Architecture Policy Evaluation Report

**Diagram**: `DirectDebitMandateUpdateArchitectureComponentDiagram.puml`
**Date**: 2025-06-04 11:48:23

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
- 1: The UML diagram shows a relationship where the "MandateUpdateService" container connects directly to the "ThoughtMachine" external system. This violates the policy which explicitly states that only the "VaultCoreClient" adapter is allowed to connect to the "ThoughtMachine" external system. The policy logic checks for any source other than "VaultCoreClient" connecting to "ThoughtMachine" and flags it as non-compliant.

Suggestions:
- 1: Modify the UML diagram to ensure that the "MandateUpdateService" container does not directly connect to the "ThoughtMachine" external system. Instead, route the connection through the "VaultCoreClient" adapter. This can be achieved by having the "MandateUpdateService" invoke the "VaultCoreClient" for any interactions with the "ThoughtMachine" system, thereby adhering to the policy requirement that only "VaultCoreClient" can connect to "ThoughtMachine".

---

### Compliant Policies

#### ARC-POLICY-101 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. All microservices (WebAPI, ServiceLayer, and VaultCoreClient) are defined within a system boundary labeled "ecs," which aligns with the policy requirement that containers must be deployed in ECS Fargate. Therefore, there are no deviations from the policy, and no suggestions for changes are necessary.

---

#### ARC-POLICY-102 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram adheres to the provided OPA policy. The policy specifies that external systems must not connect directly to non-API-Gateway components. In the UML diagram, the external system "ClientApp" connects to "ApiGateway," which is a valid API Gateway alias according to the policy. All other connections follow the internal architecture flow, starting from the API Gateway and moving through internal components, thus complying with the policy.

---

#### ARC-POLICY-104 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

The UML diagram complies with the provided OPA policy. The policy checks if any container making external calls is not marked as using secrets. The `VaultCoreClient` container, which makes an external call to `ThoughtMachine`, is correctly annotated with the stereotype `<<uses_secret>>`, satisfying the policy requirements. Therefore, there are no deviations from the policy.

---

#### ARC-POLICY-105 - ✅ COMPLIANT

**Evaluation Details:**
Compliance: Yes

Deviations:
- None

Suggestions:
- None

Conclusion: The UML diagram includes an "Audit Log" component that uses "Amazon RDS PostgreSQL" technology and is marked with the stereotype "data_store." This satisfies the policy requirement for having a data store related to audit or logging, ensuring compliance with the policy ARC-POLICY-105.

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

The UML diagram complies with the policy ARC-POLICY-108, as it includes the Amazon CloudWatch component labeled with the stereotype "observability," fulfilling the requirement for at least one observability component.

---

