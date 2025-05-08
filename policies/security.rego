package directdebit.security

deny["IAM role should not allow wildcard actions"] {
  input.resource_type == "aws_iam_role"
  input.policy_document.Statement[_].Effect == "Allow"
  input.policy_document.Statement[_].Action == "*"
  input.policy_document.Statement[_].Resource == "*"
}
