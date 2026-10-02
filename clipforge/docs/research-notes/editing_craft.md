# Editing Craft for Short-Form Clips Cut from Podcasts and Livestreams (2025-2026)

Evidence labels used throughout:
- **[PLATFORM]**: first-party platform documentation or platform-commissioned research.
- **[SURVEY/STUDY]**: third-party survey or academic study (date flagged).
- **[TOOL]**: documented defaults or behavior of a clipping or editing tool.
- **[PRACTITIONER]**: common creator or editor wisdom, usually from clipping-tool or agency blogs, not backed by disclosed data.
- **[UNVERIFIED STAT]**: a number that circulates in blogs with no traceable primary source. Do not hard-code it as fact.

Method caveat: the egress proxy blocked full-page fetches for opus.pro, ads.tiktok.com, developers.tiktok.com, developers.facebook.com, help.descript.com, kapwing.com, ncbi.nlm.nih.gov and techcrunch.com. Many findings below therefore come from search-engine result snippets of those pages, not from the full text. The only full page I fetched was the auto-editor GitHub README. Much of the 2025-2026 "data" in this space comes from SEO or AI-written blogs that cite no methodology. Those are flagged.

---

## 1. Hook structure in the first 1-3 seconds (hook types, cold open / payoff-first reordering)

### Takeaway
Platform data, mostly from ads, and practitioner analytics agree that the first ~1.5-3 s decide whether a viewer swipes. For podcast clips, the consistent practitioner rule is to open on the payoff or the most provocative line, never on the setup question. I found no controlled, published A/B data for "payoff-first reordering" specifically. Its support is strong practitioner consensus plus indirect platform data showing that the key message should land in the first 3 s.

### Cited Findings
- **[PLATFORM, ads]** Over 63% of TikTok videos with the highest click-through rate highlight their key message or product within the first 3 seconds. This is from TikTok's creative research and is repeated across TikTok creative-tips material. — [HeyOrca](https://www.heyorca.com/blog/best-tiktok-hooks); [House of Marketers](https://houseofmarketers.com/importance-of-tiktok-ad-hooks-first-3-seconds/); original deck: [TikTok "9 Creative Tips to drive performance" PDF](https://ads.tiktok.com/business/library/Auction_Ads_Creative_Tips.pdf) (fetch blocked, content not verified directly)
- **[PLATFORM, ads, OLD ~2016-2017]** Meta/Nielsen research: people who watched under 3 seconds of a Facebook video ad created up to 47% of total campaign value. In other words, the opening seconds carry most of the message for most viewers. — [Vidico (secondary)](https://vidico.com/news/facebook-video-ad-best-practices-that-actually-work-2026/); [Facebook for Business](https://www.facebook.com/business/news/updated-features-for-video-ads)
- **[PRACTITIONER/TOOL data, sample not disclosed in snippet]** OpusClip's analysis of "thousands of YouTube Shorts" reports that 50-60% of viewers who drop off do so within the first three seconds. It sets "intro retention" (share making it past 3 s) above 70% as the target. — [OpusClip blog](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention) (snippet only)
- **[PLATFORM metric]** YouTube Studio shows a "Viewed vs. Swiped away" metric for Shorts (Content → Shorts → "How many chose to view"). Practitioners treat it as the main hook-quality signal. Benchmarks: swipe-away below 25% for Shorts under 30 s is good, and above 40% means the hook is broken. — [Prepublish.ai](https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts) (the benchmarks are practitioner numbers; the metric itself is first-party)
- **[PRACTITIONER]** Shorts viewers scroll fast, so creators have "roughly 1.5 to 2 seconds to interrupt the swipe." — [Fliki](https://fliki.ai/blog/youtube-shorts-algorithm-explained)
- **[PRACTITIONER, podcast-specific]** "The clip has to deliver its payoff in the first five seconds and resolve within 90." Clips that open with the host asking a question "have already lost most of your audience. Start with the answer." Open with the sharpest line (contrarian take, data point, candid admission) and put the guest's name and title in a lower third. — [The Podcast Consultant](https://thepodcastconsultant.com/blog/podcast-clips)
- **[PRACTITIONER, podcast-specific]** High-performing podcast clips open on conflict or surprise, need no context from earlier in the episode, and "resolve within the first eight seconds or lose the viewer." If the payoff line lands at the end of a story, open the clip with that line as the hook, or use a text overlay that teases the payoff. — [Lumina Clippers](https://luminaclippers.com/blog/podcast-clip-ideas); [CutDat](https://www.cutdat.com/blog/podcast-to-clips-repurposing-guide)
- **[UNVERIFIED STAT]** "Videos with strong opening hooks see 73% higher completion rates and 4.2x more shares" and "Shorts that hook immediately receive 89% more impressions in the first 24 hours." No methodology or primary source is given. — [Reezo.ai](https://reezo.ai/blog/viral-video-hooks-that-work-2025)
- **[UNVERIFIED STAT, secondhand]** A "2025 VidMob Creative Intelligence report" is cited as finding that "incomplete visual hooks" (e.g., an action begun but not finished) average 2.4x higher 3-second retention than text-overlay hooks. I could not locate the VidMob primary source. — [Greenfrog Labs](https://greenfroglabs.com/blog/video-hooks-scroll-stopping-2026); [Virvid](https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026)
- **[UNVERIFIED STAT]** "65% of viewers drop off within the first three seconds if they aren't immediately hooked." — [Scenith](https://scenith.in/blogs/three-second-rule); [Hansen Commerce](https://hansencommerce.com/insights-tiktok-hook-3-seconds)

### Inferences
- Implementable hook rules for a pipeline:
  1. **Payoff-first reorder (cold open).** If the clip's highest-scoring line (most provocative, contrarian, numeric or emotional) sits after second ~3, copy a 1.5-4 s excerpt of that line to t=0. Then hard-cut to the start of the setup. Optionally mark the jump with a short whoosh or flash. Do not repeat the excerpt at its original position unless the clip is long enough (>30 s) for the repetition to feel like a callback.
  2. **The first spoken word starts at ≤0.3 s.** Trim all lead-in silence, breaths and "so, um" before the first content word. This follows from the 1.5-3 s decision window.
  3. **Do not open on a bare question from the host.** Open on the answer, or put the question as on-screen text while the answer audio plays.
  4. **Add a text hook overlay for 0-3 s** (see Q6) that states the stakes or open loop in ≤7-8 words. It must not duplicate the spoken words verbatim, because the burned-in captions already do that.
  5. **The clip must be self-contained.** Reject candidate clips whose first sentence depends on earlier context (pronouns with no referent, "and that's why...").
- Hook types ranked by how well the evidence supports them for podcast clips. All are practitioner-ranked; none has head-to-head public data:
  1. Cold open on a provocative or contrarian statement.
  2. Bold numeric claim.
  3. Open loop or tease ("the one thing nobody tells you about X").
  4. Pattern interrupt (visual zoom or SFX on frame 1).
  5. Question hook. Weakest when it is the host's question, acceptable as a text overlay.
- Use the YouTube "Viewed vs. swiped away" rate and the TikTok/Reels 2-3 s retention as the pipeline's feedback metric for A/B testing hook variants.

### Gaps
- I found no published controlled experiment (platform or tool vendor) that measures payoff-first reordering against chronological order for podcast clips. OpusClip and Vizard blogs may hold internal data, but the pages were blocked or only partly visible.
- The TikTok 63% stat and the Meta 47% stat are from **ads**, not organic creator clips, and the Meta figure is ~2016-era.
- The VidMob 2025 claim could not be traced to a primary report.

---

## 2. Pacing: silence removal thresholds, filler words, jump cuts, zoom punch-ins, B-roll, visual change cadence

### Takeaway
Tool defaults cluster around cutting silences with ~0.2 s of padding left on each side. Podcast-oriented presets are more conservative (0.3 s before, up to 1 s after) so conversation still sounds natural. A "visual change every 2-4 s" cadence is a near-universal practitioner rule, but the retention numbers attached to it are unverified. Over-editing is a recognized failure mode, especially for older audiences.

### Cited Findings
- **[TOOL, primary]** auto-editor (open-source CLI) defaults: `--edit audio:threshold=0.04` (an audio loudness ratio, not dB), with a **0.2 s default `--margin`** kept before and after each kept section. Asymmetric margins are supported (e.g., `--margin 0.3s,1.5sec`). — [auto-editor GitHub README](https://github.com/WyattBlue/auto-editor) (fetched)
- **[PRACTITIONER, tool presets]** Podcast presets for auto-editor: interview-style `--edit audio:0.04 --margin 0.3s,1s`; solo `--edit audio:0.02 --margin 0.1s,0.5s`. Lower thresholds (0.01-0.03) are more aggressive and higher ones (0.05-0.10) more conservative. — [Rendezvous Video](https://www.rendezvousvid.com/blog/getting-started-with-auto-editor)
- **[PRACTITIONER]** −30 dB is the typical default silence-detection level. For interviews and podcasts, a minimum silence of **1.0-2.0 s** "removes only the genuinely dead stretches while preserving conversational rhythm." Padding (handles) is "the setting that most determines whether an automated edit sounds human." — [VidPickr](https://vidpickr.com/blog/remove-silence-from-youtube-videos-2026); [EchoWave Silence Remover](https://echowave.io/tools/silence-remover/)
- **[TOOL]** Descript's "Shorten word gaps" lets the user define gaps "more than" or "between" given durations and set a target length (example given: 200 ms). A common safe setting is to trim gaps over 0.5 s down to 0.25 s. — [Descript Help: Shorten word gaps](https://help.descript.com/hc/en-us/articles/10164807277453-Shorten-word-gaps) (snippet); [Setuproll](https://setuproll.com/how-to/ve-2-remove-gaps-and-dead-air)
- **[TOOL]** Descript's "Remove filler words" targets "um," "uh," "like," "you know," "sort of," and repeated words. — [Descript Silence Remover](https://www.descript.com/tools/silence-remover); [Descript Help](https://help.descript.com/script-editing/word-gaps)
- **[PRACTITIONER]** Edit Shorts for visual variety with **cuts every 2-4 seconds** to hold attention and prevent fatigue. — [MonitorYT](https://monitoryt.com/blog/editing-for-retention); [Pixflow](https://pixflow.net/blog/youtube-video-retention-editing/)
- **[UNVERIFIED STAT]** An "interrupt every 3-5 seconds" framework reportedly lifts 0-3 s retention from 45-55% without pattern interrupts to 75-85% with them. "Sudden zoom generates 68% more engagement" than other interrupts, followed by animated text and jump cuts. — [EdicionVideoPro](https://edicionvideopro.com/en/editing-for-platforms-video-marketing/pattern-interrupts-tiktok-retention-guide/) (no methodology)
- **[PRACTITIONER, caveat]** Over-edited videos ("endless zooms, whooshes, and stacked jump cuts") tire viewers faster, especially older audiences. Match editing density to the audience. — [Air.io](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8); [Pixflow](https://pixflow.net/blog/youtube-video-retention-editing/)
- **[PLATFORM, ads]** TikTok's creative research lists editing techniques (music, transitions, movement, text overlay, emojis) as working best to "create interest, capture attention, and drive ad memorability." — [TikTok For Business: Creative Best Practices](https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads) (snippet)

### Inferences
- Implementable pacing defaults for podcast and livestream clips (synthesized from the tool defaults above, not from experiments):
  - **Silence detection:** −30 to −35 dBFS RMS (or auto-editor ratio 0.03-0.04). Compute it relative to the clip's speech level, not as an absolute value, because livestream audio varies widely.
  - **Inter-word and inter-sentence gaps:** compress any gap >0.35-0.5 s down to ~0.15-0.25 s. Keep a **0.1-0.2 s head handle** and a **0.15-0.3 s tail handle** so word onsets and decays are not clipped.
  - **Do not compress dramatic pauses** directly before a punchline (detect by sentiment or laughter following). Cap these at ~0.6-0.8 s instead of removing them.
  - **Filler-word removal:** remove standalone "um/uh/er" and stuttered repeats. Do NOT blanket-remove "like" or "you know", because they are often semantic. Gate on ASR confidence and on whether the cut lands at a word boundary with ≥40-60 ms of padding. Each cut is a jump cut, so cover it with a punch-in (below) or a crossfade of ~10-20 ms on audio to avoid clicks.
  - **Visual change cadence:** aim for one visual event (camera or speaker switch, punch-in or out of ~110-120% scale, B-roll or graphic, layout change) every **2-4 s**. Never go past ~5 s without one. Alternate zoom levels (e.g., 100% → 115% → 100%) so consecutive jump cuts on the same speaker read as deliberate.
  - **Density cap:** no more than ~1 SFX-accented zoom per 4-6 s, so the edit does not tip into over-editing. Keep a calmer preset for older-skewing or serious-topic channels.
  - **Target "tightening ratio":** practitioners commonly see raw podcast segments shrink 10-25% after gap and filler removal. This is my estimate, not a sourced number, so treat it as a sanity check rather than a target.

### Gaps
- I found no rigorous public data quantifying retention gains from silence removal, zoom cadence or B-roll in podcast clips. The 45-55% → 75-85% and "68% more engagement" stats have no traceable methodology.
- I could not access OpusClip's, Submagic's or Vizard's documentation for their exact default silence and filler thresholds (domains blocked or not documented publicly).

---

## 3. Captions: muted viewing share, retention impact, styling norms, safe zones

### Takeaway
Burned-in captions are table stakes. The best data is older (Verizon/Publicis 2019 survey: 69% watch sound-off in public; 80% more likely to finish with captions). TikTok, by contrast, is a sound-on platform (88% of users call sound essential), so captions there serve comprehension and attention rather than mute viewers. The dominant 2024-2026 style is the word-by-word "Hormozi/karaoke" caption: 1-3 words at a time, heavy condensed sans in all caps, thick stroke, one keyword color-highlighted, lower-middle of frame. Safe-zone pixel figures differ between third-party sources, so use a conservative union.

### Cited Findings
**Sound-off viewing and caption impact**
- **[SURVEY, 2019, OLD]** Verizon Media and Publicis Media surveyed 5,616 U.S. adults aged 18-54 online in April 2019. **69%** watch video with sound off in public places, and **25%** turn sound off in private. Viewers were **80% more likely to watch a video to the end when it had captions**. Half of caption-preferrers like watching sound-off. Captions contributed to +8% ad recall, +10% "ad memory quality" and +13% brand linkage. — [Forbes (2019)](https://www.forbes.com/sites/tjmccue/2019/07/31/verizon-media-says-69-percent-of-consumers-watching-video-with-sound-off/); [3Play Media](https://www.3playmedia.com/blog/verizon-media-and-publicis-media-find-viewers-want-captions/)
- **[PLATFORM, OLD ~2016]** Facebook internal study: captions boost video view time by **12%** on average. Meta/Digiday reported that 85% of Facebook videos were watched without sound. This figure is old and was contested even at the time. — [Rev captions statistics roundup](https://www.rev.com/blog/ultimate-roundup-closed-captions-statistics); [Vidico](https://vidico.com/news/facebook-video-ad-best-practices-that-actually-work-2026/)
- **[PLATFORM, 2021, with Kantar]** **88%** of TikTok users say sound is essential to the TikTok experience, and **73%** say they would "stop and look" at TikTok ads with audio. TikTok therefore differs from Facebook's historical sound-off norm. — [Social Media Today](https://www.socialmediatoday.com/news/tiktok-shares-new-insights-into-the-importance-of-sound-for-marketing-promo/601569/)
- **[PLATFORM, unquantified]** TikTok's creative research says accessibility-style captions increase watch time, completion rate and recall. The snippet gives no figures. — [TikTok For Business: Creative Best Practices](https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads)
- **[SURVEY, 2025, TV/streaming, not social]** AP-NORC (2025): about half of U.S. viewers use subtitles at least some of the time, and roughly one in three use them always or often. — [Kapwing (secondary)](https://www.kapwing.com/resources/how-many-people-use-subtitles-in-2026-2/)
- **[UNVERIFIED STAT]** "Captioned videos generate 40% higher viewing times." No primary source is given. — [Sonix](https://sonix.ai/resources/subtitle-generation-trends/)

**Styling norms (2024-2026 practice)**
- **[PRACTITIONER]** "Hormozi-style" captions are large, ALL-CAPS, word-by-word animated, set in a condensed heavy sans-serif (Montserrat Black, Anton or Bebas Neue) with a thick black stroke and a yellow highlight on emphasized keywords. They sit in the **lower-middle** of the frame, reveal **one to three words at a time** synced to speech, and cover roughly **10-15% of screen height**. — [Ascynd](https://ascynd.io/en/blog/hormozi-captions)
- **[PRACTITIONER]** Show two to four words at a time, never full sentences. The typical formula is two or three uppercase words, each filling in as spoken, with one key word popped in yellow. Word-by-word reveals create a "karaoke caption" effect where the eye follows the highlight. — [Fluxnote](https://fluxnote.io/guides/how-to-make-alex-hormozi-style-captions); [EchoWave Hormozi preset](https://echowave.io/tools/hormozi-style-captions/); [AutoCaptions Studio](https://autocaptionsstudio.com/guides/hormozi-style-captions.html)
- **[TOOL]** Submagic ships named presets (e.g., "Hormozi 1", "Devin") with adjustable font size, position and color scheme. — [Submagic blog](https://www.submagic.co/blog/reasons-to-use-submagic-for-ai-captions)

**Safe zones on a 1080x1920 canvas (third-party measurements that conflict)**
- **TikTok:** safe area **896x1306 px**. Margins: **top 130, bottom 484, left 44, right 140**. The bottom 484 px holds caption text, hashtags, music ticker and nav bar, and the right 140 px holds the like/comment/share column. TikTok notes the bottom boundary rises as the post caption gets longer, so 484 px is a minimum. — [Cadenus (2026)](https://cadenus.io/resources/blog/tiktok-safe-zone/). The same source's snippet also says to "keep important content at least 370 px above the bottom edge", which **conflicts** with the 484 px figure. Use 484+.
- **Instagram Reels:** safe area **996x1400 px**. Top dead zone **210 px** (profile and Follow), bottom **310 px** (caption, audio, engagement), right **84 px**. — [PostPlanify (2026)](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide); [AdaptlyPost](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide)
- **YouTube Shorts:** safe area **984x1500 px**. Top **120 px** (can grow on notched devices), bottom **300 px** (channel name, subscribe, audio, description). — [PostPlanify](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide)
- **"Universal" claim:** 900x1400 centered across TikTok, Reels and Shorts. — [PostPlanify](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide). Note that a vertically **centered** 1400 px box leaves only 260 px at the bottom, which violates TikTok's 484 px bottom margin. This "universal" figure is internally inconsistent.

### Inferences
- **Recommended conservative cross-platform safe rectangle** (the union of the margins above, computed by me): **x = 60 to 940 px, y = 210 to 1436 px** (880x1226). That is top ≥210, bottom ≥484, left ≥60, right ≥140. Put all captions, hook text and faces' eyes/mouths inside it.
- **Caption placement rule:** place the caption baseline block centered horizontally on x≈500 (shifted slightly left of 540 to clear the right-hand button column), with vertical center at **y≈1150-1300** (~60-68% of frame height). This is the "lower-middle" position and stays above TikTok's 484 px bottom band. In stacked layouts (facecam over gameplay, or speaker over speaker), put captions on or just below the **seam** between panels so they do not cover faces.
- **Caption spec defaults:**
  - Font: Montserrat ExtraBold/Black, Anton, Bebas Neue or "The Bold Font".
  - Size: ALL CAPS at **~70-100 px cap height** (≈ 4-5% of frame height per line). Two lines max covering ≤10-15% of height.
  - Stroke and shadow: black **stroke 6-10 px** plus optional drop shadow.
  - Chunks: **1-3 words per chunk** (≤ ~16-18 characters per line). Chunk boundaries at natural phrase breaks.
  - Timing: each chunk on screen for the duration of its words. Minimum ~0.25-0.3 s per chunk to stay readable.
  - Active-word highlight: change the active word's color (yellow #FFD700-ish or brand green) and/or scale it to 105-115%.
  - Keywords: emphasize **≤1 keyword per chunk**, chosen by NER or sentiment.
  - Emoji: at most 1 per 2-3 s, on concrete nouns or emotions only.
- **Captions apply on all three platforms.** On TikTok they serve comprehension and attention (sound-on platform). On Reels and Shorts they also cover mute viewers.
- **Disable platform auto-captions** when you burn in captions, or position the burned-in ones so a viewer toggling auto-captions does not get overlapping double text. This is inferred; there is no source for the overlap behavior.

### Gaps
- I found no 2024-2026 first-party figure for the share of TikTok, Reels or Shorts sessions watched muted. Most cited numbers are 2016-2019 Facebook or general-video surveys.
- I found no controlled study comparing word-by-word karaoke captions with static sentence captions for retention. The style's dominance is practitioner consensus.
- Official TikTok, Meta and YouTube safe-zone overlays could not be fetched (domains blocked). The pixel values above are third-party measurements and conflict in places. Verify against TikTok Ads Manager's safe-zone overlay and current app UI before hard-coding.

---

## 4. Aspect ratio and reframing (9:16, face tracking, active speaker detection, split-screen, stream layouts, blur-fill vs crop)

### Takeaway
Output should be 1080x1920 (9:16) for all three platforms. Reframing tools converge on a small set of layouts: single-speaker fill crop following the active speaker, a two-speaker vertical split, 3- and 4-up grids, screen-share plus speaker, and a gameplay layout with ~30% facecam over ~70% gameplay. Open-source building blocks (shot detection, saliency or face tracking, audio-visual active speaker detection) exist and perform well.

### Cited Findings
- **[PLATFORM spec]** All three platforms recommend 1080x1920 at 9:16. Instagram's spec says 9:16 is recommended "to avoid cropping or blank space." — [Sendcove (Meta spec summary)](https://www.sendcove.app/integrations/instagram/video-specs); [Recurpost (TikTok)](https://recurpost.com/tiktok-scheduler/tiktok-video-sizes/)
- **[TOOL]** OpusClip layouts: **Fill** (focus on the speaker), **Fit** (crop to 4:3 with padding), **Split** (two speakers stacked; works only when both appear together in the source frame), **Three**, **Four**, **Screenshare** (screen content plus speaker) and **Gameplay** (**30% speaker view on top, 70% gameplay below**). Active speaker detection keeps faces centered. — [OpusClip Help: Layout and Reframing](https://help.opus.pro/docs/article/layout-and-reframing); [OpusClip Podcast Clip Maker](https://www.opus.pro/tools/podcast-clip-maker)
- **[TOOL/RESEARCH, 2020]** Google's AutoFlip pipeline works in three steps. It detects shot boundaries, finds salient content per frame (faces, people, animals, text and logos), and then picks a per-shot camera strategy: **stationary, panning or tracking**. The original MediaPipe solution is no longer actively supported, but community ports exist (e.g., pyautoflip). — [Google Research blog](https://research.google/blog/autoflip-an-open-source-framework-for-intelligent-video-reframing/); [pyautoflip](https://github.com/AhmedHisham1/pyautoflip)
- **[RESEARCH, 2021]** TalkNet (ACM MM 2021) is an audio-visual active speaker detection model. It scores **92.3 mAP on the AVA-ActiveSpeaker validation set and 90.8 on test**. A production-optimized implementation (fast-asd) adds faster pre- and post-processing and support for variable-frame-rate video. — [TalkNet-ASD GitHub](https://github.com/TaoRuijie/TalkNet-ASD); [arXiv paper](https://arxiv.org/pdf/2107.06592); [sieve fast-asd](https://github.com/sieve-community/fast-asd)

### Inferences
- **Layout decision rules for the pipeline:**
  - **1 visible face:** Fill crop at 9:16, centered on the face. Place the eye line at ~35-40% from the top of the frame (y≈670-770) so it sits clear of the 210 px top UI band.
  - **2 people in one wide shot:**
    - When ASD shows rapid back-and-forth (speaker changes < ~2-3 s apart) or a reaction matters, use a vertical **Split**: two 1080x960 panels, each face-centered, with captions at the seam.
    - Otherwise use a Fill crop that cuts to the active speaker. Hold each speaker shot **≥1-1.5 s** to avoid ping-ponging (hysteresis).
  - **3-4 people:** a 3- or 4-up grid only for crosstalk moments. Otherwise follow the active speaker.
  - **Livestream (gameplay + facecam):** stack facecam on top (~30-40% of height, ≈580-770 px) and gameplay below (~60-70%), center-cropped or scaled to fill the 1080 width. Captions go at the seam. Hook text goes in the top panel, below y=210.
  - **Screen-share or slides:** screen content scaled to full width in the middle, speaker in a top or bottom band.
- **Camera smoothing:** apply a low-pass or critically-damped filter to crop-window motion. Use a dead-zone so the crop does not move for small head motions (< ~5-8% of frame width). Prefer cuts over pans when the subject jumps by more than ~25% of frame width, which matches AutoFlip's stationary/pan/track choice.
- **Blur-fill vs crop:** prefer a true crop (Fill) whenever the subject fits. Use a blurred, scaled-up background with the 16:9 source letterboxed (Fit) only when crucial content would be cut off: wide shots, on-screen text or charts, or gameplay HUD. This is a heuristic; I found no data comparing the two.

### Gaps
- I found no performance data (retention or engagement) comparing split-screen with active-speaker cuts, or blur-fill with crop.
- I could not verify the exact facecam/gameplay ratios used by other tools (Vizard, Submagic, StreamLadder). OpusClip's 30/70 is the only documented number found.

---

## 5. Loopable endings and how to end clips (punchline cut, no outro, seamless loop) and rewatch effects

### Takeaway
All three platforms now count replays. YouTube changed its public Shorts view count on 31 March 2025 to count every start or replay, and kept the old metric as "engaged views" for monetization. Practitioner consensus is to end hard on, or within a beat of, the punchline, with no outro or "follow for more". Where possible, make the last line flow back into the first. Published rewatch-uplift numbers are practitioner or unverified.

### Cited Findings
- **[PLATFORM change, 2025]** From **31 March 2025**, YouTube counts a Shorts view each time a Short starts to play or replay, with no minimum watch time. The previous metric was renamed **"engaged views."** YouTube Partner Program eligibility and Shorts revenue sharing still use engaged views. Absolute view counts reportedly rose 20-30% for most creators while engagement ratios fell. — [PPC Land](https://ppc.land/youtube-changes-how-shorts-views-are-counted-from-march-31/); [TubeBuddy](https://www.tubebuddy.com/blog/youtube-shorts-view-count-update-what-creators-need-to-know-about-the-new-metrics/); [TechCrunch](https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted) (fetch blocked; the 20-30% figure comes from secondary blogs)
- **[PRACTITIONER]** Looping Shorts routinely show >100% average-percentage-viewed in YouTube analytics, because replays count. On TikTok a 30 s clip replayed twice generates the same watch signal as a 90 s clip watched once. — [JoySpace](https://joyspace.ai/looping-hack-trick-algorithm-double-views); [SMMNut](https://smmnut.com/blog/tiktok-loop-content-strategy-2025/)
- **[UNVERIFIED]** Claims that the TikTok algorithm uses a point system ("rewatch worth 10 points vs completion 5") or weights rewatches "2x". These derive from unofficial or leaked-doc speculation and are not confirmed by TikTok. — [SMMNut](https://smmnut.com/blog/tiktok-loop-content-strategy-2025/)
- **[PRACTITIONER benchmarks]** Completion rates:
  - Clips under 30 s: a healthy average is 55-70%. Clips of 30-60 s: 40-55% is realistic. — [JoySpace](https://joyspace.ai/looping-hack-trick-algorithm-double-views); [SMMNut](https://smmnut.com/blog/tiktok-loop-content-strategy-2025/)
  - Shorts: above 70% is "excellent", 50-70% "solid", and below 30% "the algorithm stops distributing". — [Prepublish.ai](https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts)
- **[PRACTITIONER]** Loop construction techniques:
  - Match the first and last frames (same angle and subject position).
  - Reuse a sound effect at second 0 and at the end.
  - Cut to black for one frame at the end so the loop hides cleanly.
  - Use a "question callback" (end on the question you opened with).
  - Loops under ~10 s get higher rewatch rates because a rewatch costs less time.
  — [Virvid](https://virvid.ai/blog/looping-structure-shorts-retention-2026); [Influencers-Time](https://www.influencers-time.com/loop-optimized-reels-the-seamless-cut-that-boosts-rewatch-ra/); [Prepublish.ai](https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts)
- **[PRACTITIONER, podcast-specific]** A podcast clip should "resolve within 90" seconds. — [The Podcast Consultant](https://thepodcastconsultant.com/blog/podcast-clips)

### Inferences
- **Ending rules for the pipeline:**
  1. End **0.2-0.6 s after the last word of the punchline**, or after laughter decays if laughter follows. Never include the next speaker's turn-start ("yeah, so...").
  2. **No outros, end cards, logos or "follow for more" voiceovers** on organic clips. If a CTA is needed, put it in on-screen text during the last 1-2 s, inside the safe zone.
  3. **Seamless-loop check:** if the final sentence semantically leads into the opening line (e.g., the cold-open payoff), trim so the last word lands within ~1 frame of the loop point. Do not fade out audio or video at the end, because fades signal "over" and cause swipes. Optional: a 1-frame black, or matching the zoom level of the last and first shots.
  4. **When a cold-open reorder is used,** the natural ending often re-delivers the payoff. Cut immediately after it so the replay starts on the same line, forming a callback loop.
  5. **Length tie-in:** shorter clips (≈15-35 s) maximize completion and loop rate. Longer clips (45-90 s) suit narrative podcast moments but need mid-clip re-hooks.
- Optimize against YouTube "engaged views" and average-percentage-viewed. Loop-inflated raw views on Shorts are not the monetization metric.

### Gaps
- I found no first-party TikTok, Instagram or YouTube data quantifying the rewatch uplift from seamless loops, and no controlled comparison of "hard cut on punchline" with "short outro".
- The size of the post-March-2025 view inflation (20-30%) comes only from secondary blogs.

---

## 6. On-screen title or text hooks at the top of the frame, and progress bars

### Takeaway
A text hook in the upper third during the first ~3 s is near-universal practitioner practice for podcast clips. TikTok's own research lists text overlay among the techniques that capture attention, but one secondhand 2025 claim suggests text-only hooks underperform visual hooks. Combine them rather than relying on text alone. For progress bars, one small academic trial found higher sharing intent. Retention claims beyond that are vendor marketing.

### Cited Findings
- **[PLATFORM, ads]** TikTok's creative research names text overlay, along with music, transitions, movement and emojis, as editing techniques that "create interest, capture attention, and drive ad memorability." — [TikTok For Business](https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads)
- **[PRACTITIONER, podcast]** If the payoff line comes late, "use a text overlay that teases the payoff". Put the speaker's name and title in a lower third. — [CutDat](https://www.cutdat.com/blog/podcast-to-clips-repurposing-guide); [The Podcast Consultant](https://thepodcastconsultant.com/blog/podcast-clips)
- **[UNVERIFIED STAT, secondhand]** "Incomplete visual hooks average 2.4x higher 3-second retention than text-overlay hooks" (attributed to VidMob 2025). — [Greenfrog Labs](https://greenfroglabs.com/blog/video-hooks-scroll-stopping-2026)
- **[STUDY, academic, ~2023, health-education context]** A pretest-posttest control-group trial of short videos promoting breast cancer literacy found that viewers' **willingness to share was significantly higher for the video with a progress bar** than without one. Using a progress bar also improved "the efficiency of knowledge absorption." The search snippet does not give sample size or effect sizes. — [PMC10310936 (NCBI)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10310936/) (fetch blocked; summarized from snippet)
- **[PRACTITIONER/vendor]** A progress bar answers "how long will this take?". A nearly full bar nudges viewers to stay for the payoff. — [Subtitlebee](https://subtitlebee.com/blog/8-reasons-why-having-a-progress-bar-in-your-videos-increase-video-watch-retention/); [EchoWave progress bar tool](https://echowave.io/tools/video-progress-bar/)

### Inferences
- **Title/hook text rules:**
  - Content: ≤7-8 words (≤ ~40 characters), 1-2 lines.
  - Position: upper-middle band **y≈230-500 px**, which is below the 210 px Reels top UI. Width within x=60-940.
  - Type: same font family as the captions at ~1.2-1.5x caption size, or a white box with black text. High contrast.
  - Timing: on screen from 0 s to ~2.5-4 s. Optionally keep it persistent in a smaller size as a "title bar" for the whole clip, a common podcast-clip format.
  - Wording: the text should state the stakes or the open loop, not transcribe the first line.
  - Pair it with a visual hook (motion or punch-in on frame 1) rather than relying on text alone.
- **Progress bars** are optional and low-risk:
  - Bar: 6-12 px high, in the brand accent color, full width.
  - Placement: the very top (y≈200-215, just under the top UI) or directly above the bottom UI band (y≈1420-1436). Do not put it at the absolute bottom edge, where the platform's own scrubber and nav bar cover it.
  - Platforms (YouTube Shorts, TikTok on longer videos) show their own scrubber, so a burned-in bar is mainly a stylistic and "how long is left" cue.
  - The evidence is weak, so A/B test it rather than defaulting it on.

### Gaps
- I found no platform or large-sample creator data on top-of-frame title bars versus none, or on progress bars versus none, for organic short-form retention. The only study found is small, academic and in a health-education context.
- The VidMob comparison of text and visual hooks could not be verified.

---

## 7. Audio: loudness targets (LUFS), background music levels, trending sounds, sound effects

### Takeaway
Master clips to **−14 LUFS integrated, ≤ −1 dBTP true peak**. That is the de facto normalization reference for YouTube, and it is widely reported, though not officially documented, for TikTok and Reels. Delivering speech-only content somewhat lower is defensible per AES TD1008 (−18 LUFS for speech, −16 for music), but for feed apps practitioners converge on −14. Keep any music bed 15-20 dB below the dialogue. Use SFX (whooshes, stingers) sparingly and at a consistent level. I found no evidence that trending sounds help podcast clips specifically.

### Cited Findings
- **[STANDARD, AES TD1008, Sept 2021]** For online distribution, speech and "assorted" content should be delivered at **−18 LUFS**, music at **−16 LUFS**, and mixed or sport content at **−17 LUFS**. Programme peaks must not exceed **−1 dBTP**. Speech is set lower because it is perceived as louder at the same measured LUFS. — [AES TD1008 PDF](https://aes2.org/wp-content/uploads/2024/01/20210924_TD1008_v3.13.pdf); [Production Advice](https://productionadvice.co.uk/td1008/); [Radio World](https://www.radioworld.com/tech-and-gear/tech-tips/streaming-audio-loudness-guidelines-explained)
- **[PRACTITIONER, conflicting]** Several 2025-2026 guides say YouTube Shorts, TikTok and Instagram Reels all normalize to about **−14 LUFS with a −1 dBTP ceiling**. Mastering louder (e.g., −6 LUFS) only gets turned down, which yields a more compressed sound at the same level. — [MixingAndMastering.ai](https://mixingandmastering.ai/blog/lufs-for-tiktok-and-reels); [Humanize](https://www.humanize.app.br/blog/en/mastering-for-reels-tiktok-youtube-lufs-14); [TrackGleam](https://trackgleam.com/learn/master-for-tiktok-reels-shorts). Other sources say Instagram and TikTok "favor −10 to −12 LUFS." — [OpusClip loudness blog (snippet)](https://www.opus.pro/blog/best-loudness-normalizers); [The Post Flow](https://thepostflow.com/post-production/post-production-workflows/export-settings-youtube-instagram-tiktok/). **Neither TikTok nor Meta publishes an official normalization target that I could find.**
- **[PRACTITIONER]** A suggested technical master for social: integrated −14 LUFS (±0.5 LU), true peak −1.0 dBTP, loudness range (LRA) 6-12 LU. — [Humanize](https://www.humanize.app.br/blog/en/mastering-for-reels-tiktok-youtube-lufs-14)
- **[PRACTITIONER + accessibility guidance]** Keep background music **15-20 dB below the voice**. For example, voice peaks around −6 to −12 dBFS with music peaks around −18 to −25 dBFS, at least a ~12-20 dB gap depending on context. Accessibility guidance calls for a **20 dB** foreground-speech advantage, which makes speech about 4x as loud perceptually. A common rule is to mix music −18 to −20 dB below speech. — [Pure Audio Insight](https://pureaudioinsight.com/blogs/content-production/background-music-volume-how-loud-should-it-be); [Think Branded Media](https://thinkbrandedmedia.com/blog/tips-for-perfect-audio-balance-preventing-background-music-from-overpowering-dialogue/); [Digital Solutions Edge](https://digitalsolutionsedge.com/best-db-setting-in-audacity-for-audio/)
- **[PLATFORM, 2021, with Kantar]** 88% of TikTok users say sound is essential, and 73% would stop and look at ads with audio. — [Social Media Today](https://www.socialmediatoday.com/news/tiktok-shares-new-insights-into-the-importance-of-sound-for-marketing-promo/601569/)
- **[PRACTITIONER]** Whooshes and stingers (often under 1 s) signal transitions or surprises. Keep them subtle so they never mask the voice. Use ducking under speech. Reuse the same small SFX set for a consistent sonic signature, and use SFX sparingly. — [SFX Engine](https://sfxengine.com/blog/sound-effects-for-podcasts); [daily.dev](https://daily.dev/blog/podcast-sound-design-essential-elements-effects-and-music/); [Talks.co](https://talks.co/p/podcast-sound-effects/)

### Inferences
- **Audio chain defaults for the pipeline:**
  1. **Dialogue cleanup:** high-pass at ~70-90 Hz, light noise reduction, and de-ess if needed.
  2. **Compression:** speech compressor at ~3:1 with ~4-8 dB gain reduction on peaks, so phone speakers hold intelligibility.
  3. **Levelling:** per-speaker gain-match. Podcast and livestream sources often have mismatched mic levels.
  4. **Loudness:** final loudness normalize to **−14 LUFS integrated (±1 LU)**, using two-pass `ffmpeg loudnorm` (I=-14, TP=-1, LRA≈7-11).
  5. **True peak:** limit to **−1 dBTP** (−1.5 dBTP if AAC-encoding at lower bitrates, to leave headroom for codec overshoot).
- **Music bed:** optional for podcast clips. If used, keep it at **−18 to −24 dB relative to dialogue** (bed around −32 to −38 LUFS short-term under −14 LUFS speech). Duck a further 3-6 dB while speech is present, with ~100-300 ms attack and release. Bring it up only in speech-free gaps.
- **SFX:** whoosh on cold-open-to-setup transitions and on large zoom punch-ins. Set SFX peaks ~6-10 dB below dialogue peaks, ≤1 SFX per 4-6 s, from a fixed library so the sound stays consistent.
- **Trending sounds:** for talk clips, the spoken audio is the content. A trending track at −25 dB or lower under speech may add discovery surface on TikTok and Reels (sound pages), but this is unproven for podcasts. Treat it as an A/B option, not a default. Copyright: commercial or brand accounts generally cannot use mainstream trending music. Treat this as a general caution; I did not research licensing.

### Gaps
- I found no official TikTok or Instagram documentation of a loudness normalization target. The "−14 LUFS everywhere" claim is practitioner-reported, and some sources conflict (−10 to −12).
- I found no data on whether trending audio under speech improves reach or retention for podcast clips.
- WCAG 1.4.7 (background audio ≥20 dB below speech) is probably the origin of the "20 dB" accessibility guidance, but I did not fetch it directly.

---

## 8. Export settings (codec, bitrate, frame rate per platform)

### Takeaway
A single master export works for all three platforms. Use **1080x1920, H.264 High profile, progressive, closed GOP, 4:2:0, MP4 with faststart (moov atom at front), AAC-LC 48 kHz stereo**, at the source frame rate (30 fps typical, 60 fps for gameplay). Bitrate ~8-12 Mbps VBR for 30 fps and ~12-16 Mbps for 60 fps stays under Instagram's 25 Mbps ceiling and meets YouTube's recommendations.

### Cited Findings
- **[PLATFORM, YouTube official]** YouTube recommends H.264, progressive scan, High Profile, 2 consecutive B-frames, closed GOP with a GOP of half the frame rate, CABAC, variable bitrate, 4:2:0 chroma, MP4 container with no edit lists and the moov atom at the front (Fast Start). Audio should be AAC-LC (or Opus) at 48 kHz. For 1080p SDR at high frame rate (48/50/60 fps) the recommended bitrate is **12 Mbps**. — [YouTube Help: Recommended upload encoding settings](https://support.google.com/youtube/answer/1722171?hl=en). The same page lists **8 Mbps for 1080p at standard frame rates (24-30 fps)** and **384 kbps for stereo AAC audio**. I recalled these two values from YouTube's published table; they were not in the retrieved snippet, so verify them.
- **[PLATFORM spec via secondary summaries of Meta's Graph API Reels spec]** Instagram Reels:
  - Container and codec: MOV or MP4 with the moov atom at the front. H.264 or HEVC video, progressive, closed GOP, 4:2:0.
  - Frame rate: **23-60 fps** (30 fps commonly recommended).
  - Bitrate: VBR, **25 Mbps max** video bitrate.
  - Audio: AAC at ≤48 kHz, mono or stereo, **128 kbps**.
  - Limits: 3 s minimum, 15 min maximum, **300 MB** maximum. 9:16 recommended.
  — [Sendcove](https://www.sendcove.app/integrations/instagram/video-specs); [LunaBloom](https://blog.lunabloomai.com/instagram-reels-specifications/); [Mallary](https://mallary.ai/blog/instagram-reel-resolution)
- **[PLATFORM spec via secondary]** TikTok:
  - Recommended 1080x1920 at 9:16.
  - **30 fps recommended**, 23-60 fps accepted.
  - MP4 plus **H.264** recommended for the Content Posting API (fastest, most predictable server re-encode).
  - Bitrate at least 2 Mbps for 1080p. Practitioners suggest **6-8 Mbps at 1080p30** and **9-12 Mbps at 1080p60**.
  — [Postr](https://www.postrsocial.com/integrations/tiktok/video-specs); [Puritano](https://www.puritano.com/post/tiktok-video-specs); [Recurpost](https://recurpost.com/tiktok-scheduler/tiktok-video-sizes/)

### Inferences
- **Single master export (ffmpeg-style):**
  - `-c:v libx264 -profile:v high -pix_fmt yuv420p -preset slow -crf 18`, capped with `-maxrate 16M -bufsize 32M`. For 30 fps the result is typically 8-12 Mbps. Alternatively use explicit VBR at `-b:v 10M` for 30 fps or `14M` for 60 fps.
  - GOP: `-g` set to half the fps (e.g., 15 at 30 fps, per YouTube) or 1-2 s. Closed GOP, `-bf 2`, `-movflags +faststart`.
  - Audio: `-c:a aac -b:a 192k-320k -ar 48000 -ac 2`. Instagram re-encodes audio to ~128 kbps anyway, and YouTube suggests ~384 kbps stereo.
  - Color: tag Rec.709 (`-color_primaries bt709 -color_trc bt709 -colorspace bt709`) to avoid gamma shifts after platform transcoding.
- **Frame rate:** keep the source frame rate (do not up-convert 30 to 60). Use 60 fps only for gameplay or livestream sources captured at 60. For mixed sources, conform to 30 fps.
- **Size:** keep 60 s clips well under Instagram's 300 MB limit. At 12 Mbps, 60 s ≈ 90 MB.
- **HEVC:** H.264 is the safest default. HEVC is accepted by Instagram but gives no benefit after platform re-encoding.

### Gaps
- The official TikTok and Meta spec pages (developers.tiktok.com, developers.facebook.com) were blocked. The values above come from secondary summaries and could not be checked against the primary docs.
- I found no first-party evidence that upload bitrate above the recommendations improves post-transcode quality or ranking on TikTok or Reels. That belief is common but unproven.
