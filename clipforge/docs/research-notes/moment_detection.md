# Moment Detection: Signals and Scoring for Finding Viral-Worthy Moments in Long-Form Podcasts and Livestreams

> Method note: the session's network egress policy blocked direct fetches of arxiv.org, aclanthology.org, openreview.net, huggingface.co, springeropen.com, jonahberger.com, blog.twitch.tv and most paper mirrors. Findings below come from web-search abstracts and summaries plus direct reads of GitHub repos (github.com was reachable). Numbers marked "(search summary)" were not checked against the full paper text and should be spot-checked before they are quoted externally.

---

## 1. Transcript and semantic signals: what makes content shareable, and which transcript features to detect

### Takeaway
The best-supported semantic drivers of sharing are **high-arousal emotion** (awe, amusement, excitement, anger, anxiety), **drama and narrative** (surprise, plot, characters), **positive emotion over low-arousal negative emotion** (sadness), **memorable, portable phrasing** and **personal narratives or conversation**. Pure information content performs worse unless the viewer feels at risk. All of these can be scored from a transcript by an LLM rubric or by classifiers. Evidence for "controversy/hot take" as its own feature is indirect: it comes through anger/anxiety arousal.

### Cited Findings
**Virality psychology (primary research)**
- Berger & Milkman (JMR 2012) studied every New York Times article over three months. Content that evokes high-arousal positive emotion (awe) or high-arousal negative emotion (anger, anxiety) is more viral. Low-arousal or deactivating emotion (sadness) is less viral. Positive content beats negative content overall, but **arousal, not valence alone, drives transmission**. Experiments confirmed the causal effect runs through activation. — [Berger & Milkman, JMR (SAGE)](https://journals.sagepub.com/doi/10.1509/jmr.10.0353); [PhilPapers abstract](https://philpapers.org/rec/BERWMO-2)
- A one-SD increase in anger raised the odds of making the NYT most-emailed list by **34%**. A one-SD increase in awe raised them by **30%** (search summary). — [Berger & Milkman PDF](http://jonahberger.com/wp-content/uploads/2013/02/ViralityB.pdf); [Scientific American summary](https://www.scientificamerican.com/article/the-secret-to-online-success-what-makes-content-go-viral/)
- Tellis, MacInnis, Tirunillai & Zhang (J. Marketing 2019) ran two field studies of video-ad sharing across platforms, testing **11 emotions and 60+ ad characteristics**. Findings:
  - **Information-focused content has a significantly negative effect on sharing**, except in risky contexts.
  - **Amusement, excitement, inspiration and warmth** increase sharing.
  - **Drama elements** (surprise, plot, characters including babies, animals and **celebrities**) arouse emotion and drive sharing.
  - Content that "arouse[s] positive emotions through drama" has the most viral potential, and "captivating plots or surprise endings" encourage sharing.
  — [AMA summary](https://www.ama.org/2020/06/11/what-drives-virality-sharing-of-online-digital-content-the-critical-role-of-information-emotion-and-brand-prominence/); [AMA research insight](https://www.ama.org/research-insights/research-insight-what-drives-sharing-of-digital-content/)
- Berger & McDuff (JAR 2020) recorded the webcam facial expressions of thousands of viewers in five countries watching hundreds of ads. Facial actions linked to positive emotion, such as **smiles**, were associated with more sharing. Not all emotions increase sharing. — [Knowledge at Wharton](https://knowledge.wharton.upenn.edu/article/makes-commercials-shareable/); [WARC](https://www.warc.com/en/article/viewers%E2%80%99-facial-expressions-can-indicate-sharing-potential-for-video-ads-89417e865fda410791f55f4141895058); [Paper PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/Facial-Expressions.pdf)

**Short-video virality (TikTok)**
- Ling et al. ("Slapping Cats, Bopping Heads, and Oreo Shakes", WebSci 2022) labelled 400 TikTok videos.
  - **Creator follower count was the strongest predictor** of virality.
  - Shot scale mattered: **close-up and medium shots** helped.
  - Video lifespan, **on-screen text** and point of view also mattered.
  - Logistic regression reached **AUC 0.93** and generalized to TikToks shared on Twitter.
  — [arXiv 2111.02452](https://arxiv.org/pdf/2111.02452); [ACM full text](https://dl.acm.org/doi/fullHtml/10.1145/3501247.3531551)

**Podcast engagement from language (Spotify)**
- Reddy et al. (ACL 2021, Spotify) measured engagement as **stream rate**: the share of a show's first-time listeners who stream at least 5 minutes. High-engagement episodes had:
  - more diverse vocabulary
  - more positive and fewer negative emotions
  - **more conversation and personal narrative**
  - fewer swear words
  - **faster speech rate** (words/second)
  - **language closer to the average podcast**, which contradicts the usual "be distinctive" advice
  Text features predicted engagement with up to **81% accuracy**. — [Spotify Research blog](https://research.atspotify.com/2021/08/podcast-language-and-engagement); [ACL Anthology](https://aclanthology.org/2021.acl-long.52/)

**Quotability / memorability**
- Danescu-Niculescu-Mizil, Cheng, Kleinberg & Lee (ACL 2012) studied movie quotes, controlling for speaker and context. Memorable quotes:
  - use **less common word combinations** (lexical distinctiveness)
  - sit on **common syntactic scaffolding**
  - are **more general and "portable"**, so they apply easily in new contexts
  — [arXiv 1203.6360](https://arxiv.org/pdf/1203.6360); [MIT Technology Review](https://www.technologyreview.com/2012/04/03/186934/the-secret-science-of-memorable-quotes/)

**Humor / punchlines**
- UR-FUNNY (EMNLP 2019) has **16,514 TED-talk punchline samples** labelled from the audience-laughter markup in transcripts, plus the preceding context sentences that build the setup. Negatives come from the same videos. It shows that **audience laughter is a usable label for punchlines**, and that a punchline needs its setup context. — [ACL Anthology D19-1211](https://aclanthology.org/D19-1211.pdf); [GitHub](https://github.com/ROC-HCI/UR-FUNNY)
- LLMs remain unreliable at humor. In one 2025 study, LLMs often misjudged whether humor was appropriate, and they agreed on *which quotes* were funny only **59.9%** of the time on average. Multimodal comic benchmarks find models detect *that* humor exists but struggle to find key narrative moments. — [CMCL 2025](https://aclanthology.org/2025.cmcl-1.6.pdf); [Humor in Pixels](https://arxiv.org/html/2509.12248)

**Industry rubric (proprietary, unvalidated)**
- OpusClip's "virality score" (0–99) is described as combining **hook strength** (first ~3 s), **emotional flow** (does tension build and resolve), **perceived value** (information, entertainment or insight) and **trend alignment**. Reviewers warn it is a prediction, not audience data. "Clips rated 40 sometimes beat clips rated 85." — [datastudios.org](https://www.datastudios.org/post/opus-clip-clipanything-video-repurposing-virality-scoring-and-pricing); [nemovideo review](https://www.nemovideo.com/blog/opus-clip-review-2026)
- Open-source clippers use similar LLM rubrics. AI-Youtube-Shorts-Generator ranks on "hooks, emotional peaks, opinion bombs, revelations, conflict, quotable lines, story peaks, and practical value". — [GitHub Anil-matcha](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator)

### Inferences
Transcript feature list for the scorer. Evidence strength: H = peer-reviewed sharing/engagement evidence; M = indirect or adjacent-domain evidence; L = practitioner convention.

| Feature | Evidence | How to detect |
|---|---|---|
| High-arousal emotion (awe, amusement, excitement, anger, anxiety) | H (Berger & Milkman; Tellis) | LLM rubric, or emotion classifier over each sentence window; down-weight sadness and low-arousal content |
| Surprise / reveal / plot twist | H (Tellis drama) | LLM rubric ("is there a reversal or unexpected fact?"); numeric/statistic NER plus contrast markers ("actually", "turns out", "but") as a cheap prior |
| Story arc with setup, tension and payoff | H (Tellis plot; Spotify narratives) | LLM labels setup/payoff sentence indices; narrative markers ("so I was…", past tense, first person) |
| Humor / punchline | M (UR-FUNNY uses laughter as label; LLMs weak) | Prefer *audio laughter* after the line over LLM judgment; LLM only as secondary signal |
| Controversy / hot take / strong opinion | M (operates via anger/anxiety arousal) | LLM stance-strength rating; hedging-word absence; disagreement between speakers (diarized turn changes plus negation) |
| Practical value / advice / how-to | Mixed: Tellis finds information *hurts* sharing except in risky contexts | Score it, but weight below emotion unless the niche is educational |
| Quotability (distinctive wording on common syntax, generalizable) | M (Danescu-Niculescu-Mizil, about memorability not sharing) | Unigram/bigram surprisal against a background LM, plus a short-sentence bonus, plus a generality score (few context-bound pronouns) |
| Celebrity / named entity / trending topic | M (Tellis lists celebrities as drama characters; TikTok trending hashtags) | spaCy NER (PERSON/ORG) matched against a trending list; LLM "trend alignment" |
| Personal narrative / conversational exchange | H for podcast engagement (Reddy et al.) | First-person pronoun density; diarized back-and-forth turn rate |
| Speech rate | H for podcast engagement (Reddy et al.) | Words/second from WhisperX word timestamps, z-scored against the speaker's own baseline |
| Hook in the first 3 s | L (industry convention; no primary study found) | LLM rates the first sentence as a standalone hook; questions, bold claims, numbers |
| Self-containedness | M (Spotify uses "self-contained" as a design goal; portability in memorability research) | Penalize opening sentences that start with an unresolved pronoun or deictic ("he", "that", "this", "as I said"), or that open with discourse connectives ("so", "and", "because"); coreference resolution (e.g., fastcoref) to check antecedents exist inside the clip |

### Gaps
- I could not fetch Berger & Milkman's full text this session. From memory, the paper also reports that practical utility, interest and surprise raise virality, but this was not verified here.
- The widely repeated "71% of TikTok users decide within 3 seconds" and "65% who watch 3 s stay 10 s" figures appear only in marketing blogs ([greenfroglabs](https://greenfroglabs.com/blog/anatomy-of-viral-hook)). I could not trace a primary source; treat them as unverified.
- No peer-reviewed study was found that isolates "controversy" or "hot takes" as a sharing driver for podcast clips specifically. The link is inferred via anger/anxiety arousal.
- No study was found that measures whether self-containedness (no dangling references) improves clip performance. It is an engineering assumption shared by Spotify's design and the clipping tools.

---

## 2. Audio signals: laughter, energy, pitch, speech rate, overlap, applause; tools and models

### Takeaway
Audio gives the most reliable "something happened here" signals for talking-head content:
- **laughter and applause** events (pretrained detectors exist)
- **vocal arousal** (pitch level and range, loudness, speech rate rise with arousal)
- **cross-talk/overlap** as a proxy for heated or excited exchanges

The 2025 Rhapsody podcast-highlight benchmark found that adding **speech features (arousal/valence/dominance or HuBERT embeddings) to transcript text improves highlight prediction** over text alone.

### Cited Findings
- **Laughter detection**: `jrgillick/laughter-detection` (Gillick et al., Interspeech 2021, "Robust Laughter Detection in Noisy Environments"). Details:
  - PyTorch model trained on Switchboard, with AudioSet annotations for real-world evaluation.
  - CLI: `segment_laughter.py --input_audio_file … --output_dir …`
  - `threshold` default **0.5**; lower values trade more false positives for higher recall.
  - `min_length` default **0.2 s**.
  - Outputs (start, end) segments, laugh WAVs or TextGrid.
  - The 2021 model is "more accurate and more robust to background noise".
  — [GitHub](https://github.com/jrgillick/laughter-detection); [Paper PDF](https://people.ischool.berkeley.edu/~kimiko/papers/Gillick.2021.Interspeech.pdf)
- **General sound events (laughter, applause, cheering)**:
  - YAMNet (MobileNetV1) predicts **521 AudioSet classes**.
  - PANNs (e.g., Wavegram-Logmel-CNN14) cover AudioSet's **527 classes**, including laughter and applause.
  - YAMNet has been used specifically for laughter and clapping as social-interaction cues. Transformer taggers beat it on accuracy, but it is light enough for CPU.
  — [YAMNet social-cues paper (SocialPulse)](https://arxiv.org/pdf/2602.22085); [canlab audio review](https://github.com/canlab/narrative_feature_annotations/blob/main/docs/scoping_review/03_audio.md)
- **Vocal arousal acoustics**: the Juslin & Laukka (2003, Psychological Bulletin) meta-analysis is the standard reference.
  - Arousal correlates with **pitch height, pitch range, speech rate and loudness**.
  - Low arousal (sadness, neutral) shows reduced pitch dynamics, energy and speech rate.
  — [Semantic Scholar](https://www.semanticscholar.org/paper/Communication-of-emotions-in-vocal-expression-and-Juslin-Laukka/eca56407506a27d7a7ccac7e1499f608340b2328); [Nature HSSC 2020 citing it](https://www.nature.com/articles/s41599-020-0499-z)
- **Classic audio-excitement highlight extraction**: Rui, Gupta & Acero (ACM MM 2000) detected highlights in TV baseball by fusing **announcer excited-speech likelihood** (pitch and energy features) with ball-bat impact sound, using a weighted sum. — [PDF](https://pdfs.semanticscholar.org/4140/964119d5f9f667806e6b74d6e0a1f08f6506.pdf)
- A 2025 sports-highlight paper uses mel-spectrograms tuned to human-voice frequencies to detect **commentator and fan reactions** as key-moment indicators. — [arXiv 2501.16100](https://arxiv.org/html/2501.16100v2)
- **Dimensional speech emotion model**: `audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim`.
  - wav2vec2-Large-Robust pruned to 12 layers and fine-tuned on **MSP-Podcast v1.7**.
  - Outputs **arousal, dominance and valence ≈ 0–1** plus pooled embeddings.
  - A secondary source cites CCC ≈ 0.76–0.82 on MSP-Podcast (unverified).
  — [Hugging Face model card](https://huggingface.co/audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim); [forasoft (secondary)](https://www.forasoft.com/blog/article/audio-emotion-detection-system-using-ai)
- **Rhapsody (COLM 2025)** has **13K podcast episodes** with segment-level highlight labels from YouTube "Most replayed", framed as segment-level binary classification.
  - GPT-4o and Gemini zero-shot **struggle**.
  - A fine-tuned **Llama-3.2-1B-Instruct with a segment classification head (~6.7M trainable params)** "outperforms GPT-4o's and Gemini's zero-shot performance by a large margin".
  - The fine-tuned model **benefits from speech features (DVA, i.e. dominance/valence/arousal, or HuBERT embeddings) plus transcripts**.
  (search summary) — [arXiv 2505.19429](https://arxiv.org/abs/2505.19429); [OpenReview PDF](https://openreview.net/pdf?id=oKdVFxngy1)
- **Overlapped speech and diarization**: pyannote.audio provides voice activity, speaker-change, **overlapped-speech detection** and embeddings. Overlapped speech is defined as regions where ≥2 speakers talk at once.
  - Third-party benchmarks put speaker-diarization-3.1 DER at about 12–14% on AMI, 9–11% on VoxConverse and 17–19% on DIHARD III.
  - The newer "community-1" pipeline improves speaker counting and assignment.
  — [pyannote GitHub](https://github.com/pyannote/pyannote-audio); [pyannote community-1 blog](https://www.pyannote.ai/blog/community-1); [vexascribe (secondary)](https://vexascribe.com/pyannote-audio)
- **Speech rate and engagement**: higher speech rate is associated with higher podcast engagement. — [Spotify Research](https://research.atspotify.com/2021/08/podcast-language-and-engagement)
- **librosa primitives**:
  - `librosa.feature.rms`: frame RMS energy.
  - `librosa.pyin`: probabilistic YIN F0 with Viterbi voicing decoding, used for pitch mean and variance.
  - `librosa.onset.onset_strength`: spectral-flux envelope, useful for transients such as claps and impacts.
  — [librosa feature docs](https://librosa.org/doc/0.11.0/feature.html); [librosa.pyin](https://librosa.org/doc/0.11.0/generated/librosa.pyin.html); [onset_strength](https://librosa.org/doc/main/generated/librosa.onset.onset_strength.html)
- **Gaming streams**: commercial clippers (Eklipse) report using **audio spikes from player voice reactions** alongside kill feeds and viewer-engagement signals. — [Eklipse help](https://eklipse.gg/help/how-can-i-automatically-clip-the-most-exciting-highlights-from-fast-paced-esports-matches/)

### Inferences
Audio feature list. Compute at 0.5–1 s hops and aggregate per sentence or candidate window.
- **Laughter density and laugh-after-line**: share of the window covered by laughter (jrgillick, or YAMNet class "Laughter"). A laugh burst within about 0–3 s *after* a sentence ends is a strong punchline marker for that sentence (consistent with UR-FUNNY labelling).
- **Applause/cheer** (YAMNet/PANNs "Applause", "Cheering", "Crowd"): relevant mainly for live audiences and IRL streams.
- **Loudness spike**: RMS in dB, z-scored against a rolling 60–120 s baseline *per speaker* (diarized). This avoids rewarding loud speakers overall. Use peak-over-baseline, not raw level.
- **Pitch excursion**: pYIN F0 mean and range per voiced segment, z-scored per speaker. Large F0 range plus a high mean marks arousal.
- **Speech-rate change**: words/second from WhisperX word timestamps, as a delta against the speaker's median.
- **Model-based arousal**: audeering A/V/D per utterance. Its arousal output gives one learned signal that combines the hand-crafted features above, and Rhapsody shows DVA helps.
- **Overlap/cross-talk rate**: pyannote OSD seconds per minute, plus turn-switch rate. Spikes mark heated debate or excited exchanges. Combine with laughter to tell excited overlap from routine back-channels.
- **Silence before a line**: a pause > ~0.7 s before a sentence often marks a dramatic beat. It is also a good cut point (see Section 6). This is an engineering heuristic and has no direct study.

### Gaps
- I found no published study that validates RMS/pitch spikes specifically as predictors of *podcast clip* virality. The evidence is for vocal arousal in general (Juslin & Laukka), sports announcer excitement (Rui et al.) and Rhapsody's DVA gain.
- I could not read Rhapsody's exact metrics (F1/AP for text-only vs text+audio vs GPT-4o) because arxiv and openreview were blocked.
- Overlap detection accuracy (pyannote OSD F1) on podcast audio was not verified.

---

## 3. Video signals: facial expression, motion, scene changes, gameplay events

### Takeaway
For talking-head podcasts the visual track adds less than audio or transcript. Its main uses are:
- **facial-expression peaks** (smile, surprise) via MediaPipe blendshapes
- **cut/scene boundaries** (PySceneDetect) as clip boundaries
- **shot-scale/framing** cues (close-up faces help on TikTok)

For livestreams and gaming, vision matters much more: in a 2024 live-streaming highlight model, removing the visual modality caused the largest drop, and game-event detectors (kill feed, objectives) drive commercial gaming clippers.

### Cited Findings
- **MediaPipe Face Landmarker** outputs **52 blendshape coefficients** (smile, blink, jaw open, brow raise, etc.). It supports a VIDEO running mode via `detect_for_video(mp_image, timestamp_ms)` with `output_face_blendshapes=True`, fed by OpenCV frames. — [Google AI Edge guide (Python)](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/python); [Blendshape V2 model card](https://storage.googleapis.com/mediapipe-assets/Model%20Card%20Blendshape%20V2.pdf)
- **Viewer** smiles predict ad sharing (Berger & McDuff). Note that this is about the *audience's* face, not the on-screen speaker's. — [Knowledge at Wharton](https://knowledge.wharton.upenn.edu/article/makes-commercials-shareable/)
- **PySceneDetect**:
  - `ContentDetector` flags fast cuts from HSV frame differences against a fixed threshold.
  - `AdaptiveDetector` compares each frame score with a **rolling average** of neighbors, which works better under fast motion. Defaults: `adaptive_threshold` 3.0, `min_content_val` 15.0, `window_width` 2. Component weights cover delta hue, saturation, luminance and edges.
  — [PySceneDetect detectors docs](https://www.scenedetect.com/docs/0.6.3/api/detectors.html); [CLI docs](https://www.scenedetect.com/docs/latest/cli.html)
- OpenShorts feeds **PySceneDetect scene boundaries alongside the timestamped transcript** to the LLM for moment selection. — [GitHub mutonby/openshorts](https://github.com/mutonby/openshorts)
- **Live-stream highlight prediction (KuaiHL, ICME 2024)** uses a multimodal transformer over frames, audio, streamer ASR and audience comments, with causal look-back windows (no future frames).
  - KLive dataset: 17,897 live rooms, 19,334 hours, 30 s segments.
  - Ablation: **removing visual features caused the largest degradation (−4.72%)**, with text second.
  - It beat the text-only live-stream detector AntPivot by +1.43% Kendall tau.
  (search summary) — [arXiv 2407.12002](https://arxiv.org/abs/2407.12002); [IEEE PDF](https://ieeexplore.ieee.org/iel8/10685847/10687354/10687664.pdf)
- **Esports (Fu et al., EMNLP 2017)**: a ResNet-34 frame encoder with an LSTM over a 5 s video window was combined with a character-level chat LSTM. The joint model significantly beat either modality alone (see Section 4). — [ACL Anthology D17-1102](https://aclanthology.org/D17-1102/)
- **Gameplay events**: commercial clippers (Eklipse, Insights) detect kills, deaths, objectives, combos and "clutch plays" from screen (kill-feed recognition), game sound and in-game signals, then cut a few seconds before and after. — [Eklipse](https://eklipse.gg/help/how-can-i-automatically-clip-the-most-exciting-highlights-from-fast-paced-esports-matches/); [Insights](https://insights.gg/); [dor.gg explainer](https://clip.dor.gg/en/blog/auto-clip-detection-explained)
- **Shot scale**: close-up and medium shots, on-screen text and point of view were among the strongest content-level predictors of TikTok virality. — [Ling et al. 2022](https://arxiv.org/pdf/2111.02452)

### Inferences
- Talking-head video features, ranked by expected value:
  1. **Expression peaks**: mouthSmile, jawOpen, browInnerUp z-scored per face. Jaw open plus brow raise approximates surprise or laughter and can confirm audio laughter.
  2. **Head/body motion energy**: optical-flow magnitude in the face/body ROI (OpenCV Farnebäck), or landmark velocity. Gesturing tracks arousal.
  3. **Speaker-face count and activity**, for reframing more than scoring.
  4. **Scene cuts**, as boundary candidates more than as a score.
- Livestream/gaming: add a game-specific event detector (template matching or OCR on the kill-feed region, HUD score changes) and a generic visual-change score (frame-difference energy and PySceneDetect scores). The KuaiHL ablation suggests not dropping vision for streams.
- Visual features cost the most compute. Use them as a **re-ranker on top-N candidates** rather than over the whole multi-hour video.

### Gaps
- I found no study that measures how much on-screen speaker facial expressions improve highlight detection for podcasts specifically. KuaiHL's vision gain covers e-commerce and entertainment live rooms, not two-person talk shows.
- I did not obtain Fu et al.'s video-only and chat-only F1 numbers.

---

## 4. Livestream-specific signals: chat rate, emotes, clips, donations

### Takeaway
Chat is the strongest cheap signal for livestreams. Epic moments show **spikes in message rate, short messages, repeated "crowdspeak" and emote floods**. Systems must correct for **chat lag**: the event, then broadcast latency (about 2–15 s), then typing time. User-created **Twitch clips are the de-facto ground truth** for training and evaluation. Peer-reviewed models combining chat and video reach F-scores around 0.70–0.75 (esports) and about 0.83 accuracy (popular-clip classification).

### Cited Findings
- **Fu, Lee, Bansal & Berg (EMNLP 2017)**, "Video Highlight Prediction Using Audience Chat Reactions":
  - Datasets: League of Legends championship broadcasts, NALCS (218 videos, English chat) and LMS (103 videos, Traditional Chinese chat).
  - Chat branch: character-level LSTM, robust to typos and repeated characters, over a **7-second text window to account for audience reaction delay**. Vision branch: ResNet-34 + LSTM over 5 s.
  - Joint F-score **74.7 (NALCS)** and **70.0 (LMS)**, significantly better than either modality alone (search summary).
  — [ACL Anthology](https://aclanthology.org/D17-1102/); [Semantic Scholar](https://www.semanticscholar.org/paper/Video-Highlight-Prediction-Using-Audience-Chat-Fu-Lee/18aa7b466953189d5bc98e88f2a1ab12182f8b88)
- **Song, Park & Cha (EPJ Data Science 2021)**, "Finding epic moments in live content through deep learning on collective decisions":
  - Data: about **two million user-recommended Twitch clips** and the associated chat.
  - Twitch clips are **5–60 s segments** created by viewers and streamers.
  - Epic moments cover victory, funny, awkward and embarrassing contexts.
  - Chat during epic moments shows **high utterance frequency, short messages, incoherent content, and "crowdspeak"** (spikes of copied messages and emotes).
  - Model inputs: chat reactions, frame structure, view counts and streamer info, with **emote embeddings**.
  - Their MINT model reached **accuracy 0.8261** classifying popular vs ordinary moments.
  - A crowdsourced study found algorithmic picks "comparable to human decisions".
  — [EPJ Data Science](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00295-6); [BMC blog](https://blogs.biomedcentral.com/on-physicalsciences/2021/09/02/epic-moments-live-streaming/); [GitHub dscig/twitch-highlight-detection (pretrained emote embeddings)](https://github.com/dscig/twitch-highlight-detection)
- **LSTA (IEEE 2020)**, "Live Stream Highlight Detection Using Chat Messages": attention over **long-term and short-term chat context** decides which fragments are highlights. It beat visual-only and textual baselines on eSports streams. — [IEEE](https://ieeexplore.ieee.org/document/9162302/)
- **KuaiHL (ICME 2024)**: includes a **Modality Temporal Alignment Module** to handle the "temporal shift of cross-modal signals", i.e. comments lag the visual event, and uses only past (look-back) windows for real-time prediction. — [arXiv 2407.12002](https://arxiv.org/abs/2407.12002)
- **Practical open-source chat algorithm** (`joaohenggeler/twitch-chat-highlights`):
  - Splits the VOD into fixed `bucket_length` buckets.
  - Counts messages matching per-category word/emote lists (e.g., "Funny" = `LUL`, `KEKW`), case-insensitive, with regex support.
  - Applies a **message threshold** and a **distance threshold**, a non-max suppression that drops lower-ranked nearby buckets.
  - Ranks by count and keeps the top-N per category.
  - Applies `top_url_delay` to **backtrack the timestamp** for context.
  — [GitHub](https://github.com/joaohenggeler/twitch-chat-highlights)
- `hougesen/twitch-highlight-finder` (undergraduate thesis) relies on **emote usage only**, so it works regardless of language. — [GitHub](https://github.com/hougesen/twitch-highlight-finder)
- **Latency for the chat-lag offset**: typical Twitch stream delay is about **10–15 s** and varies by connection and region (secondary). Low-latency mode still lags **0.2–2 s**. A message-to-on-stream round trip is about 3–4 s. — [Fairly Odd Streamers](https://fairlyoddstreamers.com/blog/twitch-stream-delay/); [Twitch dev forum](https://discuss.dev.twitch.com/t/how-to-reduce-broadcast-latency/23644)
- For comparison on Twitter during sports, human reporting delay was about 20 s, and an automatic system recognized events about **40 s** after they happened. — [arXiv 1106.4300](https://arxiv.org/pdf/1106.4300)
- Twitch itself published work on using **chat emotes as signals for content themes** (2017 engineering blog; content not retrieved). — [Twitch blog](https://blog.twitch.tv/en/2017/10/05/using-chat-emotes-as-signals-for-content-themes-13c31d4a0f74/)

### Inferences
Chat feature list, per 1–2 s bin, then smoothed:
- **Message-rate z-score** against a rolling baseline (e.g., the previous 5–10 min). This normalizes for audience size and time of stream.
- **Unique-chatter rate**: discounts one spammer.
- **Emote-category rates**:
  - laughter: LUL, KEKW, OMEGALUL, LMAO
  - hype: Pog, PogChamp, W
  - shock: monkaS, WutFace, "?"
  - sad/fail: L, Sadge, F
  Each category is a separate z-score so the clip can be labelled by type.
- **Crowdspeak/copypasta ratio**: share of near-duplicate messages in the window. Mean message length falls during epic moments.
- **Lag correction**: shift chat features back by a learned or estimated offset (start around 5–15 s; fit per channel by cross-correlating chat-rate with audio-energy or laughter peaks). Fu et al.'s 7 s window and KuaiHL's alignment module support this.
- **Twitch clip counts and timestamps** (Helix API `clips` endpoint), plus **sub/donation/raid/bits events**. Clips are the strongest weak-supervision label available (Song et al.). Donation alerts often bring on-stream TTS or reactions, so treat them as "streamer reacts" priors with low weight; they are often staged.
- **Non-max suppression** with a minimum gap between selected highlights, as in joaohenggeler.

### Gaps
- I found no peer-reviewed measurement of the typical chat-reaction lag distribution on Twitch. The 10–15 s figure is a secondary blog estimate.
- No published study was found that quantifies donation/sub events as highlight predictors.
- The modern 7TV/BTTV/FFZ emotes (KEKW, OMEGALUL) are third-party. Twitch IRC exposes native emote IDs only, so third-party emotes need text matching.

---

## 5. Academic highlight detection / video summarization and 2024–2026 LLM approaches for podcasts

### Takeaway
Standard video-highlight benchmarks (QVHighlights, Mr. HiSum) and DETR-style models focus on visual, query-conditioned saliency, and they transfer poorly to talking-head speech. The most relevant recent work is speech-centric:
- **Spotify's LLM preview system** (ACL 2025 Industry): Gemini 1.5 Pro over sentence-indexed transcripts. It beat a multi-model expert pipeline and gave **+4.6% engagement** in an online A/B test.
- **Rhapsody** (COLM 2025): zero-shot GPT-4o/Gemini are weak at predicting "most replayed" podcast segments, while a small fine-tuned model using text plus audio features wins by a large margin.

"Most replayed" heatmaps are an accessible supervision source.

### Cited Findings
- **QVHighlights + Moment-DETR (NeurIPS 2021)**:
  - QVHighlights: 10,000+ YouTube vlog/news videos, **10,310 queries, 18,367 moments**, and **5-point saliency per 2 s clip**.
  - Moment-DETR treats moment retrieval as direct set prediction with no hand-made pre/post-processing.
  — [NeurIPS paper](https://papers.neurips.cc/paper/2021/file/62e0973455fd26eb03e91d5741a4a3bb-Paper.pdf); [arXiv 2107.09609](https://arxiv.org/pdf/2107.09609)
- **Follow-ups on QVHighlights**: QD-DETR, MH-DETR, UniVTG, TR-DETR, CG-DETR (fine-tuned), and video LLMs (TimeChat, VTG-LLM, TRACE) that show zero-shot highlight ability. VideoChat-T (TimeSuite, ICLR 2025) reports **mAP 26.5**, 13.0 points above TimeChat. — [TimeSuite ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/5e8309c9ca683e11672e3dbcd4b87776-Paper-Conference.pdf); [Saliency-Guided DETR](https://arxiv.org/pdf/2410.01615); [TimeChat](https://arxiv.org/pdf/2312.02051)
- **Mr. HiSum (NeurIPS 2023 D&B)**: **31,892 videos** labelled with YouTube **"Most replayed"** statistics aggregated over **50,000+ users per video**, drawn from YouTube-8M videos with ≥50k views. — [NeurIPS](https://proceedings.neurips.cc/paper/2023/hash/7f880e3a325b06e3601af1384a653038-Abstract-Datasets_and_Benchmarks.html); [GitHub](https://github.com/MRHiSum/MR.HiSum)
- **Rhapsody (COLM 2025)**: 13K podcast episodes with Most-replayed-derived segment labels.
  - Zero-shot GPT-4o and Gemini struggle.
  - A fine-tuned Llama-3.2-1B with a classification head (~6.7M trainable params), using text plus DVA/HuBERT audio features, wins "by a large margin".
  — [arXiv 2505.19429](https://arxiv.org/abs/2505.19429)
- **Spotify podcast previews (ACL 2025 Industry)**, "Transforming Podcast Preview Generation: From Expert Models to LLM-Based Systems":
  - Model: **Gemini 1.5 Pro**, using text only (episode title, description and transcript).
  - Transcript is **sentencized** with punctuation heuristics; each sentence is annotated with start/end seconds ("sentence indexing").
  - **Few-shot** curated examples of good previews.
  - **Structured output** with start/end timestamps.
  - Prompt criteria: engaging intro, logical progression, **exclude ads**, **complete thoughts**, alignment with the central theme, emotional resonance, about **1-minute** duration.
  - LLM previews averaged about **62 s** vs **56 s** legacy, so length still needs trimming.
  - Human evaluation showed better understandability, contextual clarity and interest. The online A/B test showed **+4.6% engagement** with preview content and about a **5× efficiency gain** (<20 s vs ~100 s per episode).
  - It replaced a multi-model feature-engineering pipeline.
  — [arXiv 2505.23908](https://arxiv.org/abs/2505.23908); [ACL Anthology](https://aclanthology.org/2025.acl-industry.26/); [Spotify Engineering on the legacy Dataflow preview pipeline](https://engineering.atspotify.com/2023/04/large-scale-generation-of-ml-podcast-previews-at-spotify-with-google-dataflow)
- **PODTILE (Spotify, CIKM 2024)**: a fine-tuned **LongT5 (16k-token input)** encoder-decoder that generates chapter transitions and titles together for podcast transcripts. It reports **+11% ROUGE** over the strongest baseline. — [Spotify Research](https://research.atspotify.com/2024/10/podtile-facilitating-podcast-episode-browsing-with-auto-generated-chapters); [ACM](https://dl.acm.org/doi/10.1145/3627673.3680081)
- **Lotus (IUI 2025)**: a creator-facing system that combines *abstractive* LLM narration with *extractive* clips to turn long videos into short-form ones, balancing fidelity and coverage. — [ACM DOI](https://dl.acm.org/doi/10.1145/3708359.3712090)
- **Other 2025–2026 work** (titles only; not read in depth):
  - TVHighlights (CVPR 2026, LLM-guided human-free training for highlight detection) — [CVF](https://openaccess.thecvf.com/content/CVPR2026/papers/Qiu_TVHighlights_LLM-Guided_Human-Free_Collaborative_Training_for_Video_Highlight_Detection_in_CVPR_2026_paper.pdf)
  - AHA (online highlight detection without look-ahead) — [arXiv 2509.16421](https://arxiv.org/pdf/2509.16421)
  - SVHighlights (extremely long sports video) — [arXiv 2606.06926](https://arxiv.org/html/2606.06926v2)
  - Zero-shot moment retrieval with off-the-shelf MLLMs — [arXiv 2501.07972](https://arxiv.org/html/2501.07972v1)
  - "Minimal Clips, Maximum Salience" key-moment extraction for long videos — [arXiv 2512.11399](https://arxiv.org/pdf/2512.11399)
- **Comedy-specific**: a highlight-timestamp model for comedy videos using multimodal sentiment analysis. — [arXiv 2106.00451](https://arxiv.org/pdf/2106.00451)
- **Open-source clippers** (Whisper/faster-whisper, then an LLM, then reframing):
  - opensource-clipping: faster-whisper + Gemini + MediaPipe + pyannote — [GitHub](https://github.com/NaufalRizqullah/opensource-clipping)
  - OpenShorts: Gemini or a local LLM over transcript plus scene boundaries, 3–15 moments of 15–60 s — [GitHub](https://github.com/mutonby/openshorts)
  - AI-Youtube-Shorts-Generator — [GitHub](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator)
  - autoclip (Whisper + Ollama, offline) — [GitHub](https://github.com/Farkoal2128/autoclip)
  - ClipsAI (TextTiling segmentation + WhisperX + pyannote reframing) — [GitHub](https://github.com/ClipsAI/clipsai); [docs](https://www.clipsai.com/references/clip)

### Inferences
- **Recommended architecture: hybrid.**
  1. Cheap multimodal signal curves (audio arousal, laughter, overlap, chat z-scores) over the whole video produce a "heat" timeline.
  2. Topic segmentation plus sentence boundaries produce candidate windows.
  3. An LLM rubric scores the top-K candidates, plus a few low-heat "dark horse" windows, so that purely semantic gems (advice, surprising facts) are not missed.
  4. Optionally, a learned ranker is trained later on the tool's own performance data (views, retention, shares) or on Most-replayed labels.
- Rhapsody suggests that **zero-shot LLM scores alone are a weak predictor of audience-replay behavior**, and that a small fine-tuned model with audio features is better once labels exist. Plan to log outcomes from day one.
- YouTube Most-replayed heatmaps for public long-form podcasts are a free label source for bootstrapping a learned ranker, as both Mr. HiSum and Rhapsody do.
- Spotify's result is the strongest evidence that **an LLM over a sentence-indexed transcript beats hand-engineered expert pipelines** for picking a single ~60 s self-contained segment. That task is closer to "best preview" than to "most viral", though.

### Gaps
- I could not access the full Spotify and Rhapsody texts for exact prompts, metrics and failure analyses.
- No public benchmark was found that measures **short-form clip performance** (TikTok/Shorts views or retention) for clips cut from podcasts. Most-replayed measures in-video rewatch interest, which is a proxy, not shareability.

---

## 6. Boundary detection: clean start/end points and one complete idea per clip

### Takeaway
Good practice snaps clip edges to:
- **sentence boundaries**, using word-level timestamps (WhisperX forced alignment)
- **topic shifts** (TextTiling with sentence embeddings, or LLM chaptering)
- **pauses/VAD gaps** and, where present, scene cuts

LLM outputs should reference **sentence indices rather than free-form timestamps**, as Spotify does. Chat-driven highlights need a backward offset to capture setup context.

### Cited Findings
- **WhisperX (Interspeech 2023)**:
  - VAD pre-segmentation with "Cut & Merge" into about 30 s chunks whose boundaries fall in low-speech regions.
  - Batched Whisper, then **forced phoneme alignment** (wav2vec2) for accurate word-level timestamps.
  - Plain Whisper's own timestamps are "prone to inaccuracies" and give no word-level times out of the box.
  - About **12× speedup** from batching.
  — [WhisperX paper](https://www.robots.ox.ac.uk/~vgg/publications/2023/Bain23/bain23.pdf); [GitHub](https://github.com/m-bain/whisperx)
- **TextTiling** (Hearst) detects topic shifts from word-distribution changes between adjacent blocks. ClipsAI's `ClipFinder.find_clips` applies TextTiling to WhisperX transcripts. "TextTiling with BERT embeddings" significantly improves on the original and segments at the sentence level. — [ClipsAI docs](https://www.clipsai.com/references/clip); [Solbiati et al., Unsupervised Topic Segmentation of Meetings with BERT Embeddings](https://arxiv.org/pdf/2106.12978)
- **Hierarchical/LLM segmentation**: TreeSeg (hierarchical topic segmentation of large transcripts) and PODTILE (LongT5 chapter boundaries plus titles). — [TreeSeg arXiv 2407.12028](https://arxiv.org/pdf/2407.12028); [PODTILE](https://research.atspotify.com/2024/10/podtile-facilitating-podcast-episode-browsing-with-auto-generated-chapters)
- **Spotify's preview system**: sentencizes by punctuation, gives each sentence start/end seconds, and asks the LLM for "complete thoughts" with structured start/end output. — [arXiv 2505.23908 (HTML v1)](https://arxiv.org/html/2505.23908v1)
- **TimeStampEval** proposes a "fuzzy matching trick" to improve LLM timestamp search accuracy. This implies LLM-returned timestamps or quotes need post-hoc matching back to the transcript (title/abstract only). — [ResearchGate](https://www.researchgate.net/publication/397701075_TimeStampEval_A_Simple_LLM_Eval_and_a_Little_Fuzzy_Matching_Trick_to_Improve_Search_Accuracy)
- **OpenShorts** supplies scene boundaries to the LLM and clamps clips to **15–60 s**. — [GitHub](https://github.com/mutonby/openshorts)
- **AI-Youtube-Shorts-Generator**:
  - Splits videos over 30 min into **20-minute chunks with 60 s overlap**, so cross-boundary moments survive.
  - Deduplicates candidates with **>50% overlap**, keeping the highest score.
  — [GitHub](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator)
- **Chat-based highlights**: `top_url_delay` backtracks timestamps for context, and Fu et al. use a 7 s chat window for reaction delay. — [joaohenggeler](https://github.com/joaohenggeler/twitch-chat-highlights); [Fu et al.](https://aclanthology.org/D17-1102/)
- Twitch clips themselves are **5–60 s**, which gives a reference length distribution for "one moment". — [BMC blog](https://blogs.biomedcentral.com/on-physicalsciences/2021/09/02/epic-moments-live-streaming/)

### Inferences
Boundary algorithm:
1. WhisperX gives word timestamps plus a diarized speaker per word.
2. Split into sentences (punctuation plus speaker change), giving a sentence table `[idx, start, end, speaker, text]`.
3. Embed sentences (e.g., a sentence-transformers model) and compute TextTiling-style depth scores over a sliding window of k ≈ 3–6 sentences. Local depth maxima are **topic-boundary candidates**.
4. Score each sentence gap as a cut point. Higher scores go to gaps with:
   - a pause ≥ ~0.5–0.8 s (VAD gap)
   - a speaker change
   - a topic-boundary candidate
   - a PySceneDetect cut nearby
   Mid-sentence and mid-word cuts are forbidden.
5. **Anchor-and-expand**: around each high-score peak (laugh, arousal, chat spike, or an LLM-chosen sentence):
   - Expand *backwards* to the nearest strong cut point that contains the setup. Never start on a sentence with an unresolved anaphor or a discourse connective ("so", "and", "but", "that's why"); use coreference to check.
   - Expand *forwards* until the payoff plus any laughter tail (~1–2 s after the laugh ends) is included.
   - Stay within a target length band (e.g., 15–60 s for Shorts/TikTok; Spotify targets ~60 s).
6. When an LLM picks the span, have it return **sentence indices**, not seconds, then map them to word-aligned times. Pad by ~0.1–0.3 s and snap to the nearest silence.
7. Apply NMS/deduplication across candidates (overlap > 50% means keep the best).

### Gaps
- I found no empirical study on what boundary placement (e.g., starting on the hook vs on the setup) does to short-form retention. Practitioner advice favors starting on the hook, which conflicts with "include setup context". This needs A/B testing in the product.
- No measured accuracy of TextTiling-BERT on podcast-style conversation was retrieved. The Solbiati et al. results are on meetings.

---

## 7. Practical LLM prompting for scoring transcript segments, and known failure modes

### Takeaway
Effective practice uses:
- a **timestamped, sentence-indexed transcript**, chunked with overlap or windowed around candidate peaks
- an **explicit multi-criterion rubric** with few-shot examples
- **JSON output** with indices, sub-scores, a hook line and a rationale
- deterministic post-processing (snapping, deduplication, length clamps)

Known failure modes:
- **position bias** ("lost in the middle") on long contexts
- **uncalibrated, drifting pointwise scores**, which pairwise comparison reduces
- **poor humor judgment**
- **invented or misaligned timestamps**
- weak correlation between zero-shot LLM judgments and real audience behavior

### Cited Findings
- **Spotify's production recipe**:
  - Inputs: metadata, then sentence-indexed transcript with start/end seconds.
  - Few-shot curated exemplars.
  - Explicit criteria list: engaging intro, logical progression, no ads, complete thoughts, on-theme, emotional resonance, about 60 s.
  - Structured start/end output.
  - Outcome: +4.6% engagement (A/B) and 5× faster than the expert pipeline.
  — [arXiv 2505.23908](https://arxiv.org/html/2505.23908v1); [ACL Anthology](https://aclanthology.org/2025.acl-industry.26/)
- **Open-source JSON schema example** (AI-Youtube-Shorts-Generator): `title`, `start_time`, `end_time`, `score` (0–100), `hook_sentence`, `virality_reason`. It uses a configurable `VIRALITY_CRITERIA` list, a 20-min chunk / 60 s overlap, and >50% overlap deduplication. — [GitHub](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator)
- **OpenShorts** batches **transcript windows (~2–3k tokens, 3 per call)** for scoring. It warns that Ollama's default **4096-token context is insufficient** and should be raised to 16384. — [GitHub](https://github.com/mutonby/openshorts)
- **Zero-shot LLMs underperform small fine-tuned models** at predicting audience highlight behavior (Rhapsody: GPT-4o and Gemini vs fine-tuned Llama-3.2-1B with audio features). — [arXiv 2505.19429](https://arxiv.org/abs/2505.19429)
- **Position bias**: LLMs do best when relevant information is at the start or end of the context and degrade in the middle (U-shaped curve). The same effect appears in MLLM multi-video summarization, where middle-position weakness is linked to summary-length constraints in the prompt. — [Distance between relevant info pieces causes bias (ACL Findings 2025)](https://aclanthology.org/2025.findings-acl.28.pdf); [Positional bias in multi-video summarization](https://arxiv.org/html/2606.04596); [Mitigate position bias (ACL Findings 2025)](https://aclanthology.org/2025.findings-acl.316.pdf)
- **Score calibration**:
  - LLM absolute (pointwise) scores are less robust than relative comparisons.
  - Pointwise scores show scale drift and central tendency, with Likert ratings drifting **0.5–1.0 points across identical runs** (secondary).
  - Pairwise comparisons are more stable, but **near-tie pairs flip often**.
  — [ScienceDirect survey on LLM-as-a-judge](https://www.sciencedirect.com/science/article/pii/S2666675825004564); [The Coin Flip Judge? (arXiv 2606.13685)](https://arxiv.org/pdf/2606.13685); [oneuptime (secondary)](https://oneuptime.com/blog/post/2026-08-31-pointwise-vs-pairwise-llm-evaluation/view)
- **Humor misjudgment**: LLMs agree on funny quotes only ~59.9% of the time and misjudge humor appropriateness. — [CMCL 2025](https://aclanthology.org/2025.cmcl-1.6.pdf)
- **Timestamp unreliability**: Whisper's native timestamps are inaccurate, so forced alignment is needed. LLM-returned timestamps or quotes need fuzzy matching back to source. — [WhisperX](https://www.robots.ox.ac.uk/~vgg/publications/2023/Bain23/bain23.pdf); [TimeStampEval](https://www.researchgate.net/publication/397701075_TimeStampEval_A_Simple_LLM_Eval_and_a_Little_Fuzzy_Matching_Trick_to_Improve_Search_Accuracy)
- **Commercial virality scores are weakly predictive** in practice ("clips rated 40 sometimes beat clips rated 85"). — [nemovideo](https://www.nemovideo.com/blog/opus-clip-review-2026)
- **Length control is imprecise**: Spotify's "~1 minute" instruction produced a ~62 s average and needed product-side trimming. — [arXiv 2505.23908](https://arxiv.org/html/2505.23908v1)

### Inferences

**Prompting recipe for the clipping tool**
- **Input format**: one line per sentence, for example
  `[S0412 | 00:41:07.2–00:41:11.9 | SPK_B | laugh_after=1 | arousal=0.81 | chat_z=3.4] "...text..."`
  Including the computed audio and chat signals as annotations lets the LLM fuse them with semantics. Ask for sentence-ID ranges, never raw times.
- **Chunking**:
  - Windows of about 5–10 min (≈1.5–3k tokens) with 30–60 s overlap.
  - Or, cheaper, LLM-score only **candidate windows** (±60–90 s) around multimodal peaks and topic segments, plus random low-heat windows to keep recall on semantic gems.
  - Shorter contexts also reduce lost-in-the-middle effects.
- **Rubric**: ask for 1–10 sub-scores, each with a one-line justification *before* the number. Sub-scores:
  - `hook` (first sentence works standalone)
  - `emotional_arousal`
  - `surprise/novelty`
  - `controversy/opinion_strength`
  - `humor` (with "cite the punchline sentence ID")
  - `story_completeness` (setup, tension, payoff present)
  - `value/actionability`
  - `quotability`
  - `self_containedness` (no references to earlier context; list any dangling references)
  - `topic_trend/entity_salience`
  Also return `start_sid`, `end_sid`, `hook_sid`, `suggested_title`, `category` and `reasons`. Combine sub-scores with weights in code, not inside the LLM, so the weights can be tuned against outcome data.
- **Few-shot**: 3–6 curated examples of good *and* rejected clips (ads, inside jokes, context-dependent fragments). This mirrors Spotify's curated exemplars.
- **Calibration**: normalize LLM scores within each episode (rank or z-score). For the final top-K, run **pairwise or tournament comparisons** ("which clip would more people share?"), randomizing order to cancel position bias. Treat near-ties as ties.
- **Validation guards**:
  - Verify that the quoted text matches the transcript (fuzzy match).
  - Clamp length.
  - Reject clips whose first sentence fails a dangling-reference check (pronoun/deictic/connective without an antecedent inside the clip; coreference via fastcoref or spaCy-coref).
  - Exclude ad reads (the LLM flags them, or a sponsor-keyword list).
  - Deduplicate overlaps.
- **Humor**: rely on **audio laughter after the line** (and chat LUL/KEKW spikes) as the primary humor evidence. Use the LLM humor sub-score only as a tiebreaker.

**Draft moment-scoring formula** (to tune from data):
`score = w_llm·LLM_composite + w_aud·max(z_arousal, z_rms, z_f0range) + w_laugh·laugh_after_punchline + w_ovl·z_overlap + w_chat·z_chat_lagcorrected + w_emote·max_category_z + w_vis·z_expression + w_clip·twitch_clip_density − penalties(dangling_ref, ad, too_long/short, low_ASR_conf)`
Start with semantic and LLM weights for podcasts. For livestreams, weight chat/clip signals most. KuaiHL and Fu et al. show multimodal fusion beats any single modality.

**Feature catalogue summary** (evidence: H = peer-reviewed effect on sharing/engagement/highlights; M = adjacent-domain or indirect; L = practitioner only)

| Modality | Feature | Evidence | Library |
|---|---|---|---|
| Transcript | High-arousal emotion | H | LLM rubric; HF emotion classifiers |
| Transcript | Surprise/drama/plot | H | LLM rubric |
| Transcript | Personal narrative/conversation | H (podcast engagement) | pronoun stats; diarization turn rate |
| Transcript | Information/advice | H (often *negative* for sharing) | LLM rubric |
| Transcript | Quotability/distinctiveness | M | LM surprisal (e.g., small GPT-2/Llama) |
| Transcript | Celebrity/trending entity | M | spaCy NER + trend list |
| Transcript | Self-containedness | M | coreference (fastcoref), rule-based openers |
| Audio | Laughter after line | M–H (UR-FUNNY labels; Rhapsody audio gain) | jrgillick laughter-detection; YAMNet/PANNs |
| Audio | Arousal (pitch, loudness, rate) | H (vocal emotion); M for highlights | librosa rms/pyin; audeering wav2vec2 A/V/D |
| Audio | Speech rate | H (podcast engagement) | WhisperX word timestamps |
| Audio | Overlap/cross-talk | L–M | pyannote OSD/diarization |
| Audio | Applause/cheer | M (sports highlights) | YAMNet/PANNs |
| Video | Expression peaks (smile, surprise) | M | MediaPipe Face Landmarker blendshapes |
| Video | Scene cuts | L (boundaries) | PySceneDetect |
| Video | Visual change/motion (streams) | H for live streams (KuaiHL) | OpenCV optical flow / frame diff |
| Video | Game events | L (commercial) | OCR/template match on HUD |
| Chat | Message-rate spike, short messages, crowdspeak | H (Song et al.; Fu et al.) | Twitch IRC/EventSub, chat-downloader |
| Chat | Emote-category spikes | H/M | emote dictionaries; dscig emote embeddings |
| Chat | Twitch clip density | H (used as ground truth) | Twitch Helix `clips` API |
| Chat | Subs/donations/raids | L | EventSub |

### Gaps
- No published evaluation was found of rubric-style LLM virality scoring against real short-form outcomes (views, retention, shares). Spotify measured preview engagement; Rhapsody measured Most-replayed. Expect to calibrate weights on the product's own data.
- Spotify's exact prompt text and its error analysis (e.g., how often the LLM chose ads or mid-thought spans) were not accessible.
- No research was found that directly compares sentence-index outputs with raw-timestamp outputs for LLM clip selection. The recommendation rests on Spotify's design choice and on known timestamp unreliability.
