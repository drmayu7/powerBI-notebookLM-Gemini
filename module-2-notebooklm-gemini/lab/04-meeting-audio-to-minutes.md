# Lab 4 (Workflow 3): Meeting Audio → Meeting Minutes

**Goal:** Turn a meeting audio recording into a structured **draft meeting
minutes** document.

> **⚠️ Warning:** Obtain **permission** before recording a meeting. Avoid
> uploading discussions containing confidential information to a personal
> account.

---

## Steps

1. **Prepare your audio/transcript source:**
   - Use the supplied recording for this lab:
     `../examples/02-mesyuarat-jk-rekod-audio.m4a`
     (**Mesyuarat Jawatankuasa Rekod Perubatan Bil. 2/2026**, Hospital Daerah
     Seri Aman — digitization rollout), **or**
   - If your device cannot play/upload `.m4a`, use the transcript fallback:
     `../examples/02-mesyuarat-jk-rekod-transcript.md` (paste its contents as a
     Text source), **or**
   - Use your own meeting recording or transcript.

2. In NotebookLM, click **Add source** and upload
   `02-mesyuarat-jk-rekod-audio.m4a` (or paste/upload the transcript as a
   fallback). NotebookLM will process the content.

3. In the chat, ask for a structured summary. Example prompt:
   ```
   Ringkaskan mesyuarat ini. Senaraikan:
   1. Perkara yang dibincangkan
   2. Keputusan yang dibuat
   3. Tindakan susulan (siapa & bila)
   ```

4. Ask for the meeting minutes format. Example prompt:
   ```
   Susun semula sebagai minit mesyuarat dengan jadual berlajur:
   Bil | Perkara | Keputusan/Tindakan | Pegawai Bertanggungjawab | Tarikh
   ```

   ![Draft meeting minutes table](img/04-minutes-table.png)

5. (Optional) Refine in **Gemini** — paste the draft and ask:
   ```
   Kemaskan minit mesyuarat ini dalam nada rasmi dan format kemas untuk
   diedarkan. Pastikan setiap tindakan ada pegawai bertanggungjawab.
   ```

6. Review and correct the draft manually before distribution — AI helps draft
   it, but does not replace your review.

---

## Expected outcome

A structured **draft meeting minutes** document (No., Item, Action, Officer,
Date) generated from the recording/transcript, ready to be reviewed and
finalized.

➡️ Next: [Lab 5 — Build a dashboard in Gemini Canvas](05-gemini-canvas-dashboard.md)
