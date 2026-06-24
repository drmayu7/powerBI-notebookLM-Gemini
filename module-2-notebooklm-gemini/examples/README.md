# Module 2 — Contoh Senario (Synthetic)

## Scenario

The **Unit Rekod Perubatan** of the fictional **Hospital Daerah Seri Aman** is undertaking an 18-month project to digitize approximately 120,000 paper medical-record files into an Electronic Medical Record (EMR) system. Module 2's labs follow this single continuous arc: Labs 1 and 2 query the real MOH records-management guideline (the public corpus) to understand regulatory requirements; Lab 3 converts the project paper into a slide presentation; Lab 4 turns the committee meeting transcript into formal minutes; and Lab 6 drafts a project memo based on the same project paper. Lab 5 is a standalone Gemini Canvas exercise using a COVID-19 dashboard dataset and is not part of this scenario.

## Artifact Map

| Artifact | Description | Used In |
|---|---|---|
| [01-project-paper-pendigitalan-rekod.md](01-project-paper-pendigitalan-rekod.md) | Project paper describing the digitization initiative, scope, timeline, and budget | Lab 3 (slide generation); also reused in Lab 6 (memo drafting) |
| [02-mesyuarat-jk-rekod-transcript.md](02-mesyuarat-jk-rekod-transcript.md) | Written transcript of the Records Committee meeting discussing the digitization project | Lab 4 (minutes generation) |
| [02-mesyuarat-jk-rekod-audio.m4a](02-mesyuarat-jk-rekod-audio.m4a) | Audio recording generated from the meeting transcript | Lab 4 (audio upload to NotebookLM) |
| [generate_audio.py](generate_audio.py) | Python script that produces the `.m4a` audio file from the transcript text using a TTS service | Utility — run this to reproduce the audio if needed |

## Synthetic Data Disclaimer

> **All artifacts in this folder are entirely synthetic and fictional.**
> They were created solely for training and demonstration purposes.
> No real patient data, real staff names, real institutional records, or confidential information of any kind is included.
> Any resemblance to actual persons, facilities, or events is coincidental.
