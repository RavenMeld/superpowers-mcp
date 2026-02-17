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

