# Coverage and provenance

Checked on 2026-11-12.

Machine-readable source URLs, commits, licenses, and content-right notes are in [source-manifest.json](source-manifest.json).

## Target

- Creator: Michael大麦哥
- Douyin ID: `104274995`
- Profile: `https://www.douyin.com/user/MS4wLjABAAAAWyj6c_4HBQvpfps4IGdAeXva2kW0I_cjzS-RALo7EW8`
- Profile count at check time: 209 works

## Reused sources

### 1. Full subtitles

- Repository: `feiyuaq/michael-damaige-skill`
- Local skill: `%USERPROFILE%/.codex/skills/feiyuaq-michael-damaige`
- Coverage: 19 videos; 11,428 subtitle cues
- Evidence level: verbatim machine transcript, useful for quotation and detailed synthesis
- Rights: original project code and instructions are MIT; subtitle text is not relicensed and remains subject to the original creators' rights

### 2. Timestamped subtitle excerpts

- Repository: `wangjs-jacky/michael-damaige-gallery`
- Optional local data: `<CODEX_HOME>/skills/michael-damaige-gallery/public/catalog.json`
- Coverage: 121 Bilibili videos; 382 selected excerpts
- Approval labels: 14 approved, 2 sample, 105 review
- Evidence level: selected excerpts, not complete transcripts
- Rights: no third-party content licence; do not redistribute images or long excerpts

### 3. Publisher copy and metadata

- Repository: `qwer3021/douyin-Michael-DaMaiGe-skill`
- Local skill: `%USERPROFILE%/.codex/skills/qwer-michael-damaige`
- Coverage: 39 Douyin posts
- Evidence level: titles, publisher descriptions, dates, and occasional chapter summaries
- Rights: repository has no licence file; keep use personal and do not republish wholesale

## Combined coverage

- 179 source rows
- 135 unique long-form titles after title normalization
- 19 titles have full transcripts
- 121 titles have timestamped excerpts
- 39 titles have publisher copy

The sources overlap heavily. They are not a complete archive of the 209-work profile. At least two limitations remain:

1. Unauthenticated Douyin browsing exposes only about 20 works before requiring login.
2. The remaining Douyin posts can include short videos, image notes, reposts, ads, and camera tests that do not need the same distillation treatment as long-form videos.

Never say “all 209 videos were fully transcribed.” Say “135 unique long-form titles are available, with 19 full transcripts and 121 timestamped excerpt sets” unless coverage is later expanded.

This public repository does **not** bundle the 19 SRT files, the 121-video excerpt catalog, the 39-post publisher-copy database, or any video images. Users install or supply those sources locally and remain responsible for complying with the applicable rights and terms.
