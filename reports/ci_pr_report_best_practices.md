
# ✅ Best Practices for Capturing CI PR Reports in Architecture-as-Code (AaC) Workflows

To enforce traceability, compliance, and architectural alignment across your delivery lifecycle, CI/CD pipelines should **automatically capture, annotate, and archive** PR validation results.

This ensures architecture decisions and controls are consistently followed — and violations are visible, reviewable, and auditable.

---

## 📌 Purpose of CI PR Reporting

- ✅ Provide immediate feedback to developers and reviewers
- ✅ Show alignment between code and architecture
- ✅ Expose policy/control violations or waivers
- ✅ Capture compliance metadata (e.g., traceability to ADRs)
- ✅ Archive architectural drift or changes for posterity

---

## 🔹 What to Capture in PR Reports

| Section                    | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| ✅ ADR Validation           | List of ADRs referenced and linked to code/infra                            |
| ✅ PlantUML Diff Summary    | What changed in architecture diagrams (`.puml`)                             |
| ✅ Drift Check Report       | Terraform/code differences from expected architecture                      |
| ✅ ArchUnit Results         | Java architectural constraint test results                                 |
| ✅ Rego Policy Checks       | Infrastructure policy compliance from OPA                                  |
| ✅ Waiver Summary           | Any accepted waivers and their expiration/status                           |
| ✅ Reviewer Instructions    | Notes if waiver present, or manual steps required                          |

---

## 📁 File Location (Optional in Repo)

CI systems can write PR metadata and results to:
```
/reports/pr-<short-sha>.md
/reports/last-ci-summary.md  (symlink or copy)
```

These can be versioned for governance traceability, and rendered in dashboards or PR comments.

---

## 📥 Report Example

```markdown
# ✅ Architecture Compliance Summary for PR #47

### ✅ Referenced ADRs
- [0001-service-on-fargate.md](../adr/0001-service-on-fargate.md)
- [0005-use-vault-api-client.md](../adr/0005-use-vault-api-client.md)

---

### ✅ PlantUML Diagram Diff
- Modified: `architecture/components.puml`
- Linked to ADR: `0007-new-async-audit-pattern.md`

---

### ✅ Code / Infra Drift Detected
- ⚠️ ECS service missing load balancer as defined in diagram
- Recommendation: Align terraform with `/architecture/containers.puml` or update diagram + ADR

---

### ✅ Policy Compliance (OPA / Rego)
| Policy      | Result     | Notes                                  |
|-------------|------------|----------------------------------------|
| SEC-001     | ✅ Pass     | All endpoints require authentication   |
| INFRA-001   | ⚠️ Warning  | Fargate image tag is not `:stable`     |

---

### ✅ Java ArchUnit Results
- Passed: 12
- Failed: 0

---

### ⚠️ Waivers Detected
- `waivers/0012-temp-db-secret-inline.md` (expires 2025-12-31)

---

### 👁️ Reviewer Notes
- Waiver present – reviewer approval required
- Ensure ADR `0007` includes updated architecture context

```

---

## 🧪 Implementation Tips

- Write Markdown using GitHub Actions, GitLab CI, Jenkins, etc.
- Push `.md` as part of PR checks or post a summary to PR comment
- Consider rendering reports into a dashboard or Confluence using automation

---

## ✅ Governance Bonus

- Archive all reports weekly/monthly for audit
- Validate that every merged PR has a compliance report attached
- Auto-reject PRs missing ADRs or with expired waivers

---

