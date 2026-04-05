# Shared wildcard certificate for *.demo.apex.hcls.aws.dev
# This certificate is pre-created and shared across all APEX projects.
# No per-project certificate needed.

data "aws_acm_certificate" "wildcard" {
  domain      = "*.demo.apex.hcls.aws.dev"
  statuses    = ["ISSUED"]
  most_recent = true
}
