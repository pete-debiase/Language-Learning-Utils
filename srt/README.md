### JA SUBS2SRS Procedure (2022/06/06)
1. Download MP4s and SRTs using Anystream (or Netflix Subtitle Downloader/Flixgrab as backup).
3. Simplify filenames using `rename_files.py`.
4. Convert to SRT + build fulltext using `vtt_to_srt.py`.
6. Analyze fulltext using `analyze_ja.py` to supplement target word list for content.
7. Filter subtitle files using `filter.py` to determine which MP4s are needed.
10. Use `massage_target_words_ja.py` to figure out best jamdict output.
11. Generate Anki TSV/clips using `subs2srs.exe`.
12. Post-process Anki TSV using `postprocess_subs2srs_tsv_ja.py`.
13. Import into Anki.

### ES SUBS2SRS Procedure (2022/06/07)
1. Identify movies of interest on Language Reactor.
2. Download MP4s and SRTs using Anystream (or Netflix Subtitle Downloader/Flixgrab as backup).
4. Convert to SRT + build fulltext using `vtt_to_srt.py`.
5. Analyze fulltext using `analyze_es.py`.
6. Glue subs using `glue.py`.
7. Generate Anki TSV/clips using `subs2srs.exe`.
8. Import into Anki.
