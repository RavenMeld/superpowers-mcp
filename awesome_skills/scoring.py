from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SkillFeatures:
    has_description: bool
    has_use_when: bool
    has_workflow: bool
    code_fence_count: int
    has_scripts: bool
    has_references: bool
    has_assets: bool
    word_count: int


def worth_using_score(f: SkillFeatures) -> int:
    score = 0

    if f.has_description:
        score += 20
    if f.has_use_when:
        score += 15
    if f.has_workflow:
        score += 10

    if f.code_fence_count >= 1:
        score += 10
    if f.code_fence_count >= 3:
        score += 5
    if f.code_fence_count >= 6:
        score += 5

    if f.has_scripts:
        score += 10
    if f.has_references:
        score += 5
    if f.has_assets:
        score += 3

    # Size sanity: too short tends to be low-value; too long tends to be hard to use.
    if 200 <= f.word_count <= 2000:
        score += 5
    if f.word_count < 80:
        score -= 10
    if f.word_count > 8000:
        score -= 5

    if score < 0:
        score = 0
    if score > 100:
        score = 100
    return score


def quality_score(*, root_label: str, worth_score: int, features: SkillFeatures) -> int:
    """
    A practical confidence signal for ranking:
    - source trust (root provenance)
    - coverage depth (worth score)
    - curation quality (workflow/use-when/examples signals)
    """
    root = str(root_label or "").strip().lower()
    source_trust = {
        "codex_skills": 42,
        "agent_playground": 38,
        "agents_skills": 34,
        "external": 18,
    }.get(root, 30)

    coverage = int(round(max(0, min(100, int(worth_score))) * 0.4))

    curation = 0
    if features.has_description:
        curation += 3
    if features.has_use_when:
        curation += 5
    if features.has_workflow:
        curation += 5
    if features.code_fence_count >= 1:
        curation += 1
    if features.has_scripts or features.has_references:
        curation += 1

    total = source_trust + coverage + curation
    if total < 0:
        return 0
    if total > 100:
        return 100
    return int(total)
