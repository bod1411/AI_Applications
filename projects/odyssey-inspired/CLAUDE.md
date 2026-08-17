# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

This folder is not a code project — it holds Suno song-prompt research and configuration documents (Markdown), built using the `suno-song-creator` workflow/plugin defined at the repo root (`suno-song-creator-plugin`). There is no `requirements.txt`, entrypoint, or runnable script here, so there are no install/run commands to document.

## Contents and structure

Each subfolder is one song concept, containing a `prompt.md` with:
- YAML frontmatter (title, project, created date, Suno model version, genre, mood).
- A "Prompt Configuration" section: Suno model/version, generation parameters (MAX Mode toggles, Weirdness %, Style Influence %, Vocal Gender, Exclude Styles), the structured genre/instrumentation/production/mood tag block, and — for instrumental tracks — a meta-tag "Lyrics Box" arrangement (e.g. `[Intro | ...]`, `[Theme A | ...]`) instead of literal lyrics.
- A "Research Notes" section documenting the source of stylistic inspiration and a stated research-confidence level, with an explicit note that composer/film/track names are deliberately excluded from the actual Suno prompt text for copyright-safety — only sonic/instrumentation/mood descriptors are used.

Currently contains one config: `ithaca-echoes/prompt.md` — an instrumental cinematic score prompt (ancient-Greek-mythology / Odyssey homecoming theme; no vocals) with a character count noted as verified via a `count-prompt.js` tool (that tool is not present in this folder).

## Notes

- These are content/config artifacts consumed by the Suno song creator workflow, not by this project's own code — treat edits here as prompt-engineering/copywriting, not software changes.
- When adding new song concepts, follow the existing pattern: one subfolder per concept, a `prompt.md` with the same frontmatter + Prompt Configuration + Research Notes structure.
