# obsidian-diary

This skill acts as an intelligent secretary for your Obsidian knowledge base. It takes raw content from `Tools/chat/daily summary.md` and put it into the right place, when compiling the content, it follows following steps: 1.  Formats it according to your `Tools/chat/daily summary.md` prompt. 2.  Appends diary entries to `Logging/Daily/`. 3.  Identifies people, resolves their aliases, and updat...

## Quick Facts
- id: `obsidian-diary--08ac5f7a26`
- worth_using_score: `35/100`
- tags: `ci, obsidian, rag`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/you-n-g-obsidian-diary/SKILL.md`

## Workflow / Steps
- Read the file `Tools/chat/daily summary.md` in the vault. Follow the prompt and instructions at the top of that file to decide how to summarize and format the text.
- The raw content that needs to be compiled is found in the `User` section.
- **Step 1**: Run the `obsidian-people` skill to get a master list of names and aliases.
- **Step 2**: Analyze the raw text. Match any names, nicknames, or references (e.g., "Jim", "Boss") to the **canonical filenames** returned by the script (e.g., "Jim" might match `People/James.md` via an alias).
- **Target**: `Logging/Daily/YYYY-MM-DD.md` (Use today's date).
- **Action**:
- Read the file to understand its current structure.
- Move the raw content from the summary into the diary.
- Add the compiled content to the diary, following the instructions in `Tools/chat/daily summary.md`.
- **Remove the raw content from `Tools/chat/daily summary.md`** after it has been moved. Keep the original information in the `Logging/Daily/YYYY-MM-DD.md` as much as possible.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
