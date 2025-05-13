
# ✅ Architecture and Compliance Waiver Best Practices

Architecture waivers allow teams to **intentionally diverge** from standards or policies in a controlled, time-bound, and auditable manner. They are essential for balancing innovation, urgency, and compliance in enterprise environments.

---

## 🔹 When to Use a Waiver

Use a waiver when:
- A project **cannot comply** with a policy or architecture constraint due to technical or time constraints.
- An **experimental or legacy** solution is temporarily allowed.
- A dependency or third-party product **blocks compliance** (e.g., missing encryption support).
- There's an **approved exception** granted by architecture governance.

---

## 🧩 What a Waiver Includes

Each waiver must be stored as a **Waiver ADR** in version control and include:

| Section        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| Title          | Clear description of what is being waived (e.g., "TEMP - No HTTPS on ALB") |
| Status         | Proposed, Accepted, Superseded, or Expired                                 |
| Context        | Why the waiver is needed                                                   |
| Decision       | What is being accepted temporarily                                          |
| Expiration     | Fixed date or milestone for review                                         |
| Consequences   | Risk implications, potential impacts                                       |
| Alternatives   | What was considered but rejected                                           |
| Owner          | Who is responsible for reviewing/remediating the waiver                   |

---

## 🗂️ File Location

Store waiver files in your ADR folder:
```
/adr/waivers/00XX-title-of-waiver.md
```

---

## ✅ Enforcement Process

| Step | Action                                                                 |
|------|------------------------------------------------------------------------|
| 1    | Developer or Architect proposes waiver ADR                             |
| 2    | Team reviews and approves in PR                                         |
| 3    | CI checks for matching waiver file if a policy or architecture fails   |
| 4    | Waiver flagged with metadata (e.g., `compliance-waiver`)              |
| 5    | Reviewer required for override                                          |
| 6    | Periodic review scheduled before expiration                            |

---

## ⚠️ Waiver Expiration and Audit

- Expired waivers **must be reviewed** and either extended or remediated.
- Include waivers in **quarterly architecture reviews**.
- Waiver compliance should be **visible in CI/CD pipelines** and dashboards.

---

## 🧪 Example Waiver ADR

```markdown
# TEMP - Allow ECS Task to Run Without ALB
## Status
Accepted

## Context
Deployment must complete before infra migration. Load balancer will be added in Phase 2.

## Decision
Allow ECS service to be reachable directly by IP for QA purposes only.

## Expiration
2025-09-30

## Consequences
No HTTPS or public protection in place. Acceptable within VPN-only access.

## Alternatives Considered
- Add ALB early (too much overhead)
- Use private CloudMap entry (not yet supported by legacy client)

## Owner
phil.devops@mycompany.com
```

---

## 🔐 Governance Tip

Always link waivers to:
- Relevant **Jira tickets or backlog items**
- Any **automated controls or tests** that they override

---

