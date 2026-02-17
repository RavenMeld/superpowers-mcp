# nuget-manager

Manage NuGet packages in .NET projects/solutions. Use this skill when adding, removing, or updating NuGet package versions. It enforces using `dotnet` CLI for package management and provides strict procedures for direct file edits only when updating versions.

## Quick Facts
- id: `nuget-manager--dc8e583a62`
- worth_using_score: `35/100`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/nuget-manager/SKILL.md`

## Workflow / Steps
- **Verify Version Existence**:
- **Determine Version Management**:
- Search for `Directory.Packages.props` in the solution root. If present, versions should be managed there via `<PackageVersion Include="Package.Name" Version="1.2.3" />`.
- If absent, check individual `.csproj` files for `<PackageReference Include="Package.Name" Version="1.2.3" />`.
- **Apply Changes**:
- **Verify Stability**:

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
