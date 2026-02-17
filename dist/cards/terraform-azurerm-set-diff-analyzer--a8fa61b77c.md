# terraform-azurerm-set-diff-analyzer

Analyze Terraform plan JSON output for AzureRM Provider to distinguish between false-positive diffs (order-only changes in Set-type attributes) and actual resource changes. Use when reviewing terraform plan output for Azure resources like Application Gateway, Load Balancer, Firewall, Front Door, NSG, and other resources with Set-type attributes that cause spurious diffs due to internal ordering...

## Quick Facts
- id: `terraform-azurerm-set-diff-analyzer--a8fa61b77c`
- worth_using_score: `60/100`
- tags: `python, azure, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/terraform-azurerm-set-diff-analyzer/SKILL.md`

## Use When
- `terraform plan` shows many changes, but you only added/removed a single element
- Application Gateway, Load Balancer, NSG, etc. show "all elements changed"
- You want to automatically filter false-positive diffs in CI/CD

## Workflow / Steps
- terraform plan -out=plan.tfplan
- terraform show -json plan.tfplan > plan.json

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `1`
- has_scripts: `True`
- has_references: `True`
- has_assets: `False`
