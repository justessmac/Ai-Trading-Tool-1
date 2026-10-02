# Hook Fast, Hold Attention, Clear Every Right

Short-form clips cut from podcasts and livestreams succeed in 2025-2026 when they do the one thing all three ranking systems officially reward: they stop a stranger from swiping, then keep that viewer watching to the end. TikTok calls finishing a longer video a "strong indicator" of interest. YouTube gates Shorts distribution on a "viewed vs. swiped away" ratio measured on a seed audience. Instagram's Adam Mosseri names watch time, likes per reach and sends per reach as the top three signals. None of them publishes numeric weights, so every "sends count 3-5x" rule is folklore. An automated clipper should therefore rank candidates on **predicted first-three-second hold × expected watch seconds × completion probability**, with shares, loops, comments and saves as tunable secondary terms. The moments that deliver are high-arousal (amusement, awe, anger, surprise), self-contained stories with a payoff, and lines followed by real laughter or a chat spike. The best evidence says to find them by fusing an LLM rubric over a sentence-indexed transcript with measured audio arousal, laughter, cross-talk and lag-corrected chat, because zero-shot LLMs and commercial "virality scores" both predict real audience behavior poorly. The default edit has six parts: a payoff-first cold open with speech starting within 0.3 s, 1-3-word animated captions inside a conservative safe zone, active-speaker 9:16 reframing, a visual change every 2-4 s, a hard cut on the punchline, and speech mastered to −14 LUFS with no added music. Default length is 30-59 s unless the source is fully owned. Copyright safety requires two independent gates. The first is a documented rights basis plus detection of music and third-party footage. The second is a platform originality test that tightened sharply through 2025-2026. The hardest single rule is YouTube's: **any Short longer than 60 s with any active Content ID claim is blocked worldwide**.

## All three feeds gate reach on the first three seconds and on finished watches

### What the platforms actually say

The official record is thinner than the SEO industry implies, but it is consistent. TikTok's explanation of the For You feed lists likes, shares, follows, comments and video information as inputs. It says "a strong indicator of interest, such as whether a user finishes watching a longer video from beginning to end, would receive greater weight than a weak indicator" such as shared country. It also says **neither follower count nor a creator's past hits is a direct ranking factor** ([TikTok Newsroom](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you); [Sprout Social](https://sproutsocial.com/insights/tiktok-algorithm/)). That post dates from 2020, but TikTok still links it. YouTube shows **"Viewed vs. Swiped away"** in Shorts analytics: the share of feed impressions where the viewer stayed instead of swiping. Shorts staff describe distribution as explore/exploit, in which a Short goes to a small seed audience and expands only if that audience engages ([Prepublish.ai](https://prepublish.ai/blog/viewed-vs-swiped-away-youtube-shorts); [vidIQ](https://vidiq.com/blog/post/youtube-shorts-algorithm/)). Instagram is the most explicit. In January 2025 Mosseri named **watch time, likes per reach and sends per reach** as the three most important signals, adding that "likes are slightly more important for connected content, and sends are slightly more important for unconnected content" ([Dataslayer](https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers); [Kompozy](https://kompozy.io/news/instagram-mosseri-ranking-signals-guidance)). The widely repeated claim that sends carry 3-5x the weight of likes is a community estimate that Meta has never confirmed ([Dataslayer](https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers)). No source gives official relative weights for saves, comments or follows on any platform.

Two of the three platforms now give creators a direct first-seconds metric. YouTube does not publish how many seconds count as "viewed". However, a study of 3.3 billion Shorts views found that clips at **70-90% viewed** did better and those **under 60%** performed poorly ([Medium study](https://medium.com/@antoinelacombled/cracking-the-youtube-shorts-algorithm-a-study-of-3-3-billion-views-4711fdf7931b)). Instagram added **skip rate**, the share of viewers who scroll past within 3 seconds, to Reels Insights around August 2025 and to the Marketing API in December 2025 ([Social Media Today](https://www.socialmediatoday.com/news/instagram-adds-retention-insights-reels/758464/); [Storrito](https://storrito.com/resources/how-instagrams-updated-marketing-api-metrics-work/)). Industry trackers treat a skip rate under about 30-40% as healthy and over 50% as a failed hook ([Babbleboxx](https://www.babbleboxx.com/post/instagram-adds-reels-retention-skip-rate-what-influencer-marketers-should-do-next)). TikTok exposes no equivalent, so the 2-3 s point on its retention curve is the proxy. Vendor and ad data point the same way. OpusClip reports that **50-60% of Shorts viewers who drop off do so within the first three seconds** ([OpusClip](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention)). TikTok's ad research found that over 63% of its highest-click-through videos deliver their key message within 3 seconds ([HeyOrca](https://www.heyorca.com/blog/best-tiktok-hooks)).

Two measurement details matter for anyone building analytics. Since **31 March 2025**, YouTube counts a public Shorts view on every start or replay, with no minimum watch time. The older threshold metric survives as **"engaged views"**, which drives YPP eligibility and revenue sharing ([TechCrunch](https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted)). Public Shorts views before and after that date are not comparable, so a feedback loop should ingest engaged views. Separately, TikTok's auto-generated transcript has reportedly fed search indexing and For You relevance since mid-2025 ([SocialPilot](https://www.socialpilot.co/blog/tiktok-algorithm)). That claim is secondary, but acting on it costs little: keep spoken audio clean and put an on-topic keyword in the first sentence.

| Platform | Officially named core signals | First-seconds metric | Working KPI (practitioner, not official) |
|---|---|---|---|
| TikTok | Finishing longer videos ("strong indicator"); likes, shares, follows and comments as inputs | None public; use 2-3 s retention from the curve | No published benchmark |
| YouTube Shorts | Viewed vs. swiped away on a seed audience; replays count as views since March 2025 | Viewed vs. swiped away (threshold unpublished) | ≥70% viewed; alert below 60% |
| Instagram Reels | Watch time, likes per reach, sends per reach | Skip rate (scrolled past within 3 s) | ≤35% skip; alert above 50% |

### Turning signals into an objective function

The evidence supports a strict order of priorities even without weights. Predicted first-seconds hold and predicted completion relative to length are officially central on all three platforms, so they should dominate. Shareability ("sendability") ranks third: it is the strongest named interaction for non-follower reach on Instagram and an explicit TikTok input. Loop or rewatch potential, comment provocation and save value follow, and they should be tunable hyperparameters rather than constants. Platform differences also argue for fitting the secondary terms separately per platform. Socialinsider's 69-million-video benchmark puts engagement rate at **3.70% on TikTok, 0.48% on Reels and 0.27% on Shorts**, and average comments per post at 50, 20 and 10 respectively ([Socialinsider](https://www.socialinsider.io/blog/tiktok-vs-reels-vs-shorts/)). Calibration has one more trap. In a labelled study of TikTok virality, **creator follower count was the strongest predictor** in a model that reached AUC 0.93 ([Ling et al.](https://arxiv.org/pdf/2111.02452)). Outcome labels must therefore be normalized per account, for example as views relative to that account's median, before they are used to tune any clip-level weight. Otherwise the model learns which channels are big, not which moments are good.

## Length data favors 30-59 seconds by default, with a longer lane only for owned stories

The length studies look contradictory until reach is separated from rate. Buffer's analysis of 1.1 million TikToks found that videos over 60 s earned **43.2% more reach than 30-60 s videos, 70.3% more than 10-30 s videos and 63.8% more watch time**, even though 86% of TikToks run under a minute ([Buffer](https://buffer.com/resources/longer-tiktoks-get-more-views-data/)). Socialinsider found that engagement rate follows a U-shape: **6.00% under 30 s, 4.20% at 30-60 s and 5.80% beyond 180 s** ([Socialinsider](https://www.socialinsider.io/blog/how-long-are-tiktok-videos/)). OpusClip's 2026 TikTok data points the other way on virality. Its viral-tier median is **41 s, 18% shorter than the overall median**, with 15-30 s overrepresented and 60-90 s underrepresented among viral clips ([OpusClip](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026)). On Shorts, an Inflow study of 5,400 clips found mean views rising to **1.7M for 50-60 s versus 77K under 10 s**. quso.ai's 108,000-Short dataset, by contrast, put the highest *median* in the **11-20 s** band ([Piktochart](https://piktochart.com/blog/how-long-youtube-shorts/); [quso.ai](https://quso.ai/research/youtube-shorts-length)). The gap between mean and median says long Shorts produce the outliers, while short ones are the safer bet for a typical channel. Podcast clips in practice cluster at 30-60 s: **44.7% of 494,716 OpusClip podcast clips** on YouTube fall in that band ([OpusClip research](https://www.opus.pro/research/best-time-podcast-clips-youtube)).

The reconciliation is that long clips win only when they hold attention, and the studies that favor length measure the long clips that survived. The scoring model should therefore maximize expected watch seconds times completion probability, never length itself. Padding a weak moment past 60 s to chase Buffer's reach curve will lower completion. Completion priors by length come only from low-rigour practitioner sources: roughly ≥70-80% under 15 s, ≥60% at 15-30 s, ≥45-50% at 30-60 s and ≥35-40% past 60 s ([Retensis](https://retensis.com/blog/audience-retention-benchmarks-2026); [Kapwing](https://www.kapwing.com/resources/short-form-video-statistics-tiktok-reels-and-shorts-by-the-numbers-in-2026/)). Use them as starting values and replace them with each account's own data. Platform rules then shape the presets:

- **YouTube** raised the Shorts maximum to 3 minutes from 15 October 2024 ([9to5Google](https://9to5google.com/2024/10/03/youtube-shorts-3-minutes/)), but blocks any Short over one minute that carries an active Content ID claim ([YouTube Help](https://support.google.com/youtube/answer/15424877?hl=en)).
- **Instagram** moved Reels to 3 minutes in January 2025 ([Hootsuite](https://blog.hootsuite.com/instagram-reels/)). One source says Reels over 90 s still get less non-follower reach ([Creatorflow](https://creatorflow.so/blog/instagram-algorithm-2026/)). That is likely carried over from the old rule and has no 2025-2026 official confirmation.
- **TikTok's** Creator Rewards program pays only on **original videos longer than one minute** ([Benly](https://benly.ai/learn/tiktok-ads/creator-rewards-program-2026)), which pulls owned accounts toward a 61 s+ lane.

| Platform | Default band | Extended band | Hard rule |
|---|---|---|---|
| TikTok | "Punch" mode, 20-45 s, for engagement rate and loops | "Story" mode, 61-120 s+, for reach, watch time and Creator Rewards (owned or original only) | Go past 45 s only when predicted retention is high |
| YouTube Shorts | 30-59 s | 60-180 s only for fully owned audio and video with a real narrative arc | Cap at 59 s whenever any claimable third-party material is present |
| Instagram Reels | 15-60 s | Up to 90 s soft maximum; 90-180 s only for follower-facing posts or Trial Reels tests | Never post a file carrying another platform's watermark |

### One or two distinct clips a day captures most of the frequency gain

Buffer's study of 11.4 million TikTok posts found that, compared with one post a week, views per post rose **17% at 2-5 posts a week, 29% at 6-10 and 34% at 11+**. The steepest gain comes from the first step up ([Search Engine Journal](https://www.searchenginejournal.com/study-shows-2-5-weekly-tiktoks-deliver-biggest-view-increase/558641/)). On Instagram, compared with 1-2 posts a week, reach per post rose **12% at 3-5, 18% at 6-9 and 24% at 10+** ([Social Media Today](https://www.socialmediatoday.com/news/study-shows-posting-more-instagram-leads-to-more-reach/757633/)). Consistency matters more than bursts: accounts that posted in at least 20 of 26 weeks earned **450% more engagement per post** than sporadic posters ([Buffer](https://buffer.com/resources/creator-growth-playbook/)). Timing data is weaker and skewed toward brand accounts. Sprout Social's study of about 30,000 accounts puts TikTok's best window at Tuesday-Thursday 2-6 pm local, and Instagram's at Tuesday 1-7 pm and Wednesday 12-9 pm ([Social Media Today](https://www.socialmediatoday.com/news/best-times-to-post-2025-sprout-social/744014/)). Use it to seed a scheduler, not to override a channel's own analytics.

No platform penalizes posting many clips from one episode. Podcast playbooks recommend three to five or more per episode, each pointing back to the full show ([YouTube Blog](https://blog.youtube/creator-and-artist-stories/the-definitive-guide-to-creating-engaging-podcast-content/); [Fame](https://www.fame.so/post/ultimate-podcast-clip-guide)). The real risk is near-duplication: YouTube's July 2025 "inauthentic content" policy explicitly targets "similar or repetitive content" ([Social Media Today](https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/)). Sensible defaults:

- **Per-platform cadence:** TikTok one to two clips a day, Instagram about one a day, Shorts one to three a day.
- **Spacing:** spread one episode's clips across 5-14 days.
- **Duplicate guard:** refuse to publish two clips on the same account that share more than roughly 30-40% of their spoken words. No platform publishes a threshold, so this number is inferred and should be tuned.

## Arousal, surprise and laughter mark the moments worth cutting

### Emotion and story in the transcript outweigh information

Peer-reviewed virality research sets the transcript scorer's priorities. Berger and Milkman studied three months of New York Times articles and found that **arousal, not valence alone, drives sharing**. High-arousal emotions (awe, anger, anxiety) raise transmission and low-arousal sadness suppresses it. A one-standard-deviation rise in anger or awe raised the odds of reaching the most-emailed list by **34% and 30%** respectively ([Berger & Milkman](http://jonahberger.com/wp-content/uploads/2013/02/ViralityB.pdf); [JMR](https://journals.sagepub.com/doi/10.1509/jmr.10.0353)). Tellis and colleagues ran field studies of video-ad sharing covering 11 emotions and 60+ characteristics. They found that **amusement, excitement, inspiration and warmth** raise sharing, and that **drama raises it too: surprise, plot, and characters including celebrities**. They also found that **information-focused content has a significantly negative effect** except in risky contexts ([AMA](https://www.ama.org/2020/06/11/what-drives-virality-sharing-of-online-digital-content-the-critical-role-of-information-emotion-and-brand-prominence/)). For podcasts specifically, Spotify studied the share of first-time listeners who stream at least five minutes. Higher-engagement episodes had **more personal narrative and conversation, more positive emotion, faster speech and fewer swear words**. Against conventional advice, they also used language closer to the average podcast. Text features alone predicted engagement with up to 81% accuracy ([Spotify Research](https://research.atspotify.com/2021/08/podcast-language-and-engagement)). Memorability research describes a quotable line as an unusual word combination on common sentence structure, general enough to make sense out of context ([Danescu-Niculescu-Mizil et al.](https://arxiv.org/pdf/1203.6360)). That also defines what a clip's opening line should look like.

The one apparent contradiction is instructive. Tellis says information hurts sharing. Yet OpusClip's 2026 data on 8,254 Shorts shows the **Expertise/Authority/Credibility hook averaging 6,706 views, 5.9x the weakest hook type**. "Expert Explainer" (concept, then why it matters, then how to apply it) is the most common viral storyline on both TikTok and Shorts ([OpusClip Shorts](https://www.opus.pro/research/how-to-go-viral-youtube-shorts); [OpusClip TikTok](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026)). The likely explanation is that Tellis measured brand ads, where information reads as selling, while podcast audiences come for expertise. OpusClip's sample, though, is its own user base, which skews toward educational talking-head content, so its numbers are correlational and self-selected. The practical rule is to score advice and value, but let them win only when they arrive with authority and stakes: a surprising number, a contrarian claim, a personal cost. Outside educational niches, weight plain how-to content below emotion. Treat "hot takes" as one source of arousal, not as a separate feature, because no study isolates controversy for podcast clips.

Humor is where the transcript is weakest. In a 2025 study, LLMs agreed on which quotes were funny only **59.9%** of the time ([CMCL 2025](https://aclanthology.org/2025.cmcl-1.6.pdf)). UR-FUNNY's 16,514 TED-talk punchlines show that **audience laughter after a line is a usable punchline label** ([UR-FUNNY](https://aclanthology.org/D19-1211.pdf)). Detect humor from audio and chat, and use the LLM's humor rating only as a tiebreaker.

### Audio, video and chat supply cheap "something happened" signals

For talking heads, audio gives the most reliable event markers. Vocal arousal shows up as higher pitch, wider pitch range, faster speech and louder delivery ([Juslin & Laukka](https://www.semanticscholar.org/paper/Communication-of-emotions-in-vocal-expression-and-Juslin-Laukka/eca56407506a27d7a7ccac7e1499f608340b2328)). It can be measured with librosa's RMS energy and pYIN pitch tracking. It can also be read directly from audeering's wav2vec2 model, fine-tuned on MSP-Podcast, which outputs arousal, dominance and valence ([Hugging Face](https://huggingface.co/audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim)). Gillick's laughter detector (default threshold 0.5, minimum event length 0.2 s) and AudioSet taggers such as YAMNet (521 classes) cover laughter, applause and cheering ([laughter-detection](https://github.com/jrgillick/laughter-detection); [TensorFlow YAMNet](https://www.tensorflow.org/tutorials/audio/transfer_learning_audio)). pyannote provides diarization and overlapped-speech detection for spotting heated cross-talk ([pyannote](https://github.com/pyannote/pyannote-audio)).

The strongest podcast-specific evidence comes from Rhapsody (COLM 2025), which labelled segments of 13,000 podcast episodes using YouTube "Most replayed" data. Zero-shot GPT-4o and Gemini struggled to predict those segments. A fine-tuned Llama-3.2-1B with a small classification head beat them "by a large margin", and **adding speech arousal/valence/dominance or HuBERT features to the transcript** improved it further ([Rhapsody](https://arxiv.org/abs/2505.19429)). Every audio feature should be z-scored per diarized speaker against a rolling 60-120 s baseline, so that a naturally loud host does not dominate the scores.

For a two-person podcast, vision adds little beyond reframing. For livestreams it matters most: in Kuaishou's KuaiHL model, trained on 19,334 hours of live rooms, **removing visual features caused the largest performance drop (−4.72%)** ([KuaiHL](https://arxiv.org/abs/2407.12002)). MediaPipe's 52 face blendshapes (smile, jaw open, brow raise) can confirm laughter or surprise picked up in the audio ([Google AI Edge](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/python)). Gaming clippers detect kill feeds and HUD events ([Eklipse](https://eklipse.gg/help/how-can-i-automatically-clip-the-most-exciting-highlights-from-fast-paced-esports-matches/)). Vision is the costliest modality, so run it as a re-ranker on the top candidates instead of across multi-hour VODs.

For streams, chat is the strongest cheap signal. Song, Park and Cha studied roughly two million viewer-created Twitch clips and found that epic moments show **high message frequency, short messages, incoherent content and "crowdspeak"**, meaning copied messages and emote floods. Their model classified popular moments with 0.826 accuracy ([EPJ Data Science](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00295-6)). Fu et al. read chat over a **7-second window to absorb reaction delay** and combined it with video. On League of Legends broadcasts the combined model reached F-scores of 74.7 and 70.0, beating either signal alone ([EMNLP 2017](https://aclanthology.org/D17-1102/)). Chat lags the on-screen event by the broadcast delay, commonly 10-15 s on Twitch, plus typing time ([Fairly Odd Streamers](https://fairlyoddstreamers.com/blog/twitch-stream-delay/)). Chat features therefore need to be shifted back by an offset fitted per channel, for example by cross-correlating chat rate with peaks in audio laughter. Clips that viewers created themselves are the best available weak label. Donation and sub alerts are often staged and deserve little weight.

### Existing tools share one architecture and the same blind spots

Commercial clippers are more alike than their marketing suggests. Nearly all run speech recognition, then an LLM or NLP pass that picks self-contained segments, then a 0-99 or 0-100 ranking score. OpusClip is the only vendor that names its sub-scores: **Hook, Flow, Value and Trend**. Its newer ClipAnything model adds visual, audio and sentiment cues for footage with little dialogue, and users can steer it with genre presets and topic keywords ([OpusClip Help](https://help.opus.pro/docs/article/virality-score); [OpusClip ClipAnything](https://www.opus.pro/clipanything); [OpusClip API](https://help.opus.pro/api-reference/schemas/curation-preferences)). Third-party reviews describe what the other scores are based on:

- **Vizard:** speech energy, topic transitions and engagement signals ([Creatify](https://creatify.ai/review/vizard-ai)).
- **Klap:** hook strength, pacing and topic coherence ([ToolsForHumans](https://www.toolsforhumans.ai/ai-tools/klap)).
- **Riverside:** keyword relevance, sentiment and speaker energy ([Conbersa](https://www.conbersa.ai/learn/podcast-clip-from-riverside-recording)).

Descript says Underlord looks for "high-energy segments, laughter, or self-contained stories" ([Descript](https://www.descript.com/clips)). Stream tools differ: StreamLadder's ClipGPT reads chat spikes, voice excitement, in-game events and emotes ([StreamLadder](https://www.streamladder.com/clipgpt)). OpusClip deliberately over-generates, returning **32-42 clips from a one-to-two-hour source** and leaving the user to pick ([OpusClip Help](https://help.opus.pro/docs/article/how-many-clips)).

The shared weaknesses are where a new tool can win. **No vendor publishes how well its score predicts real views**, and reviewers say so bluntly: "clips rated 40 sometimes beat clips rated 85", and "a 92 won't reliably beat a 78" ([NemoVideo](https://www.nemovideo.com/blog/opus-clip-review-2026)). The most common complaints concern boundaries and missing context. One test found 10 of 76 OpusClip clips unusable because of mid-sentence cuts or missed punchlines, reviewers plan to discard 20-40% of output, and Klap failed to find natural break points in 7 of 14 attempts ([eesel](https://www.eesel.ai/blog/opusclip-reviews); [ScaleReach](https://www.scalereach.ai/blog/klap-review-for-short-form-teams)). Multi-speaker crosstalk "confuses the reframing and causes it to chase the wrong face" ([eesel](https://www.eesel.ai/blog/opusclip-reviews)). Open-source projects have already solved part of this. AutoClip has the LLM return **word indices instead of timestamps**, because models copy numbers reliably but do arithmetic poorly, and it never interpolates a crop path across a shot cut ([AutoClip](https://github.com/artbyjazi/autoclip)). AI-Youtube-Shorts-Generator splits long videos into 20-minute chunks with 60 s of overlap, and drops the lower-scoring candidate when two overlap by more than 50% ([GitHub](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator)).

### A hybrid scorer: heat map, LLM rubric, then calibration

The strongest production evidence favors an LLM reading a sentence-indexed transcript. Spotify replaced a multi-model feature pipeline with Gemini 1.5 Pro working from a transcript in which every sentence carries start and end seconds. The prompt included curated few-shot examples and explicit criteria: an engaging intro, logical progression, complete thoughts, no ads, emotional resonance, about one minute long. The model returned structured start and end points. The system lifted preview engagement by **4.6% in an online A/B test** and ran about 5x faster. Even so, "about one minute" averaged 62 s and still needed trimming ([Spotify, ACL 2025](https://arxiv.org/abs/2505.23908)). Rhapsody's caution still applies: zero-shot judgment is a weak proxy for what audiences replay, so the LLM should be one input among measured signals.

Known LLM-judge failure modes shape the plumbing. LLMs attend poorly to material in the middle of a long context ([ACL Findings 2025](https://aclanthology.org/2025.findings-acl.28.pdf)). Their absolute (pointwise) scores are less stable than pairwise comparisons ([ScienceDirect survey](https://www.sciencedirect.com/science/article/pii/S2666675825004564)). Raw Whisper timestamps are inaccurate enough to need forced alignment ([WhisperX](https://github.com/m-bain/whisperx)). Spotify's one-minute target and Twitch viewers' own 5-60 s clip lengths ([EPJ Data Science](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-021-00295-6)) give a sensible range for what counts as "one moment".

The recommended pipeline has eight steps:

1. **Transcribe.** WhisperX produces word timestamps and diarized speakers, which become a sentence table.
2. **Build a heat map.** Compute cheap signal curves (arousal, laughter, overlap, chat) across the whole video at 0.5-1 s steps.
3. **Generate candidates.** Take topic segments from TextTiling over sentence embeddings, plus windows around heat peaks. Add a few random low-heat windows so purely semantic gems are not missed.
4. **Score with the LLM.** Annotate each sentence line with its measured signals, for example `[S0412 | 00:41:07.2–00:41:11.9 | SPK_B | laugh_after=1 | arousal=0.81 | chat_z=3.4]`. Ask for sub-scores, each with a one-line justification written before the number. Ask for sentence-ID ranges, never seconds.
5. **Set boundaries by anchor-and-expand.**
   - **Backward:** expand to the nearest strong cut point that includes the setup. Never start on an unresolved pronoun or a connective such as "so", "and" or "that's why"; check with coreference resolution.
   - **Forward:** expand through the payoff plus 1-2 s of laughter tail.
   - **Snap:** move each edge to a pause of at least 0.5-0.8 s, a speaker change or a scene cut, and never cut mid-word.
6. **De-duplicate.** Apply non-max suppression to overlapping candidates.
7. **Rank.** Normalize scores within each episode, then run randomized-order pairwise comparisons on the top-K and treat near-ties as ties.
8. **Gate.** Apply the compliance gates described below before anything is published.

```
moment(w) = Σ_i  w_i · z_i(w)  −  penalties(dangling_reference, ad_read, low_ASR_confidence, outside_length_band)

LLM(w)    = 0.25·hook + 0.15·emotional_arousal + 0.15·story_completeness + 0.10·surprise
          + 0.10·opinion_strength + 0.10·value + 0.05·quotability + 0.05·trend + 0.05·humor

value(c, platform) = P(hold_3s | hook) × E[watch_seconds | length, platform] × P(complete | length)
                     × (1 + λ_send·shareability + λ_loop·loop + λ_comment·debate + λ_save·utility)

publish(c) only if rights ∧ music_clear ∧ no_third_party_video ∧ originality ∧ not_near_duplicate
```

The weights below are **starting priors chosen from the strength of the evidence, not measured values**. They should be replaced as soon as per-account normalized outcome data exists. YouTube "Most replayed" heatmaps on public long-form podcasts are a free bootstrap label, as Mr. HiSum (31,892 videos) and Rhapsody both demonstrate ([Mr. HiSum](https://github.com/MRHiSum/MR.HiSum)).

| Signal (z-scored within episode) | Podcast prior | Livestream prior | Evidence base | Detector |
|---|---|---|---|---|
| LLM rubric composite | 0.45 | 0.20 | Spotify A/B win; Rhapsody shows zero-shot alone is weak | Sentence-indexed prompt, JSON sub-scores |
| Vocal arousal (max of model arousal, RMS spike, pitch range) | 0.20 | 0.15 | Vocal-emotion meta-analysis; Rhapsody audio gain | audeering wav2vec2, librosa |
| Laughter 0-3 s after a line | 0.15 | 0.10 | UR-FUNNY laughter labels | Gillick detector, YAMNet |
| Speech-rate rise vs. speaker baseline | 0.05 | 0 | Spotify engagement study | WhisperX word times |
| Overlap / cross-talk | 0.05 | 0.05 | Indirect only | pyannote overlap detection |
| Expression peaks, motion, game events | 0.10 | 0.10 | KuaiHL vision ablation | MediaPipe blendshapes, HUD OCR |
| Lag-corrected chat rate + emote-category z | 0 | 0.25 | Song et al.; Fu et al. | Chat logs, emote dictionaries |
| Viewer clip density | 0 | 0.15 | Used as ground truth by Song et al. | Twitch Helix clips API |

One design tension has no published answer. Practitioners say to start on the hook, while the boundary logic above says to include the setup. No study measures what either choice does to short-form retention, so the cold-open edit below resolves it mechanically, and it should be the first A/B test the product runs.

## A payoff-first edit with a hard punchline ending is the default spec

### Hooks and on-screen text

Podcast editors converge on one rule: "Start with the answer." A clip that opens with the host asking a question has "already lost most of your audience" ([The Podcast Consultant](https://thepodcastconsultant.com/blog/podcast-clips)). High performers open on conflict or surprise and need no earlier context ([Lumina Clippers](https://luminaclippers.com/blog/podcast-clip-ideas)). OpusClip says the platform makes an early decision at around 1.5 seconds and that the hook should resolve by second 3 ([OpusClip](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026)). No controlled experiment measures payoff-first reordering against chronological order. The case for it is strong practitioner consensus plus the first-seconds data above.

The pipeline should implement a **cold open**. If the strongest line lands after second 3, copy a 1.5-4 s excerpt of it to t=0, then hard-cut to the start of the setup. Also:

- Start the first content word within **0.3 s**.
- Never open on black frames, logos or a host's bare question.
- Overlay a **text hook of at most 7-8 words** in the upper-middle band (y≈230-500 px on a 1080×1920 canvas, below Instagram's top interface) for the first 2.5-4 s. The text should state the stakes or the open loop, not transcribe the first line.

TikTok's creative research lists text overlay among the techniques that capture attention ([TikTok For Business](https://ads.tiktok.com/business/en-US/blog/creative-best-practices-top-performing-ads)), and on-screen text was among the content predictors of TikTok virality in Ling et al. ([Ling et al.](https://arxiv.org/pdf/2111.02452)). Overlay and title card are not the same thing, though. A separate "text intro" appears in only **1.0%** of viral TikToks in OpusClip's data ([OpusClip research](https://www.opus.pro/research/how-to-go-viral-tiktok)). Put the text over moving footage and never spend frames on a title card before speech starts. Pair the text with a visual hook, such as a punch-in on frame 1. Burned-in progress bars have only one small academic trial behind them, which found higher willingness to share ([PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10310936/)). Treat them as an A/B option, not a default.

### Pacing

Tool defaults give concrete numbers. The open-source auto-editor keeps a **0.2 s margin** around each kept section at a 0.04 loudness threshold. Its podcast presets use asymmetric 0.3 s / 1 s margins so conversation still sounds human ([auto-editor](https://github.com/WyattBlue/auto-editor); [Rendezvous Video](https://www.rendezvousvid.com/blog/getting-started-with-auto-editor)). For interviews, practitioners remove only silences of 1-2 s or longer, and say padding is "the setting that most determines whether an automated edit sounds human" ([VidPickr](https://vidpickr.com/blog/remove-silence-from-youtube-videos-2026)). For a clip, the synthesis is:

- **Gaps:** compress inter-word gaps longer than 0.35-0.5 s down to 0.15-0.25 s, keeping a 0.1-0.2 s head handle and a 0.15-0.3 s tail handle.
- **Dramatic pauses:** keep the pause before a punchline, capped at 0.6-0.8 s.
- **Fillers:** cut standalone "um/uh" and stutters. Descript's filler removal also targets "like" and "you know" ([Descript](https://www.descript.com/tools/silence-remover)), but those are often meaningful, so do not remove them wholesale.

Visually, the near-universal practitioner rule is a change every **2-4 seconds** ([MonitorYT](https://monitoryt.com/blog/editing-for-retention)): a speaker switch, a 110-120% punch-in, or a layout change, never more than about 5 s without one. Alternate zoom levels so consecutive jump cuts read as deliberate. Over-editing tires viewers, especially older audiences ([Pixflow](https://pixflow.net/blog/youtube-video-retention-editing/)), so cap sound-accented zooms at about one per 4-6 s and offer a calmer preset for serious topics. The retention-uplift statistics attached to "pattern interrupts" online have no traceable methodology and should not be hard-coded.

### Captions and safe zones

Burned-in captions are table stakes, but their purpose differs by platform. The best audience data is from 2019: in a Verizon Media and Publicis survey, **69% of viewers watched with sound off in public**, and captioned videos were **80% more likely to be watched to the end** ([Forbes](https://www.forbes.com/sites/tjmccue/2019/07/31/verizon-media-says-69-percent-of-consumers-watching-video-with-sound-off/)). TikTok, by contrast, reports that **88% of its users call sound essential** ([Social Media Today](https://www.socialmediatoday.com/news/tiktok-shares-new-insights-into-the-importance-of-sound-for-marketing-promo/601569/)). Captions there serve comprehension and attention more than muted viewing. OpusClip finds captions in **80.2%** of viral TikToks and animated captions in 78.6% ([OpusClip research](https://www.opus.pro/research/how-to-go-viral-tiktok)), but OpusClip burns captions in by default, so prevalence does not prove cause.

The dominant 2024-2026 style is the word-by-word "Hormozi" caption:

- one to three words at a time
- ALL CAPS in a heavy condensed sans-serif (Montserrat Black, Anton or Bebas Neue)
- a thick black stroke
- one keyword highlighted in yellow
- placed in the lower-middle of the frame, covering about 10-15% of screen height

([Ascynd](https://ascynd.io/en/blog/hormozi-captions)). Fonts from Google Fonts carry open licenses that cover commercial video ([choosealicense.com](https://choosealicense.com/licenses/ofl-1.1/)).

Third-party safe-zone measurements conflict, so take the conservative union of three sets of margins on a 1080×1920 canvas:

- **TikTok:** 130 px top, **484 px bottom** (more with long post captions), 140 px right ([Cadenus](https://cadenus.io/resources/blog/tiktok-safe-zone/)).
- **Reels:** **210 px top**, 310 px bottom, 84 px right ([PostPlanify](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide)).
- **Shorts:** 120 px top, 300 px bottom ([PostPlanify](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide)).

The union yields a working rectangle of **x 60-940, y 210-1436**. Captions should center near y≈1150-1300, and in stacked layouts they should sit on the seam between panels so they do not cover faces.

### Reframing to 9:16

All three platforms want 1080×1920 ([Sendcove](https://www.sendcove.app/integrations/instagram/video-specs)). OpusClip offers seven layouts: fill, fit, two-speaker split, three-up, four-up, screenshare, and a gameplay layout with **30% facecam over 70% gameplay** ([OpusClip Help](https://help.opus.pro/docs/article/layout-and-reframing)). The building blocks are open:

- **Google's AutoFlip** detects shots, finds salient content, then chooses a stationary, panning or tracking camera for each shot ([Google Research](https://research.google/blog/autoflip-an-open-source-framework-for-intelligent-video-reframing/)).
- **TalkNet**, an audio-visual active-speaker detector, scores **92.3 mAP** on AVA-ActiveSpeaker validation ([TalkNet](https://github.com/TaoRuijie/TalkNet-ASD)).

Ling et al. found that close-up and medium shots predicted TikTok virality ([Ling et al.](https://arxiv.org/pdf/2111.02452)), which supports a tight crop. The resulting layout rules:

- **One face:** fill crop with the eye line 35-40% from the top.
- **Two people in one wide shot:** use a stacked split when the speaker changes faster than every 2-3 s. Otherwise cut to the active speaker and hold each shot at least 1-1.5 s to avoid ping-ponging.
- **Three or four people:** a grid only for crosstalk; otherwise follow the active speaker.
- **Gameplay streams:** a 30-40% facecam panel on top.
- **Crop motion:** smooth it with a dead zone of about 5-8% of frame width. Cut instead of panning when the subject jumps more than about 25% of the width.
- **Blur-fill:** use letterboxing over a blurred background only when a true crop would lose essential on-screen text or HUD. No data compares the two approaches.

### Endings and loops

Replays now count everywhere, and looping Shorts routinely show over 100% average percentage viewed ([JoySpace](https://joyspace.ai/looping-hack-trick-algorithm-double-views)). End **0.2-0.6 s after the last word of the punchline**, or after the laughter dies away. Never include the next speaker's "yeah, so…". Do not fade, because a fade signals "over" and invites the swipe. Drop outros: they appear in only **4.6%** of viral TikToks in OpusClip's data ([OpusClip research](https://www.opus.pro/research/how-to-go-viral-tiktok)). If a call to action is needed, put it on screen in the last one to two seconds. The cold open creates a free loop: when the natural ending re-delivers the payoff line, cut right after it so the replay starts on the same words. Claims that TikTok scores rewatches with a fixed point system come from leaked-document speculation, not TikTok.

### Audio and export

Master speech to **−14 LUFS integrated with a −1 dBTP ceiling**. That is the de facto feed-app normalization reference, though neither TikTok nor Meta publishes a target, and some sources claim −10 to −12 LUFS ([MixingAndMastering.ai](https://mixingandmastering.ai/blog/lufs-for-tiktok-and-reels)). The AES TD1008 standard recommends −18 LUFS for online speech and the same −1 dBTP limit ([AES](https://aes2.org/wp-content/uploads/2024/01/20210924_TD1008_v3.13.pdf)).

Ship **no added music** by default. Music appears in only 1.9% of viral TikToks in OpusClip's data ([OpusClip research](https://www.opus.pro/research/how-to-go-viral-tiktok)), and the copyright section below explains why music costs claims and revenue. If a bed is used, keep it **15-20 dB below the voice** and duck it under speech ([Pure Audio Insight](https://pureaudioinsight.com/blogs/content-production/background-music-volume-how-loud-should-it-be)). There is no evidence that trending sounds help talk clips, so let users add them natively in each app at post time.

One master works for every platform: H.264 High profile with closed GOP, MP4 with faststart, AAC at 48 kHz, and the source frame rate. YouTube recommends **12 Mbps for 1080p at 48-60 fps** ([YouTube Help](https://support.google.com/youtube/answer/1722171?hl=en)). Instagram caps video bitrate at 25 Mbps and files at 300 MB ([Sendcove](https://www.sendcove.app/integrations/instagram/video-specs)). TikTok recommends 30 fps ([Postr](https://www.postrsocial.com/integrations/tiktok/video-specs)).

| Stage | Default | Guard rail |
|---|---|---|
| Start | First content word ≤0.3 s; no black frames or logos | Trim breaths and "so, um" |
| Cold open | Copy a 1.5-4 s payoff to t=0 when the best line falls after ~3 s | Repeat it at its original position only in clips over 30 s |
| Hook text | ≤7-8 words, y≈230-500 px, 0 to ~3 s, over moving footage | States the stakes; never a title card before speech |
| Gaps | Compress >0.35-0.5 s gaps to 0.15-0.25 s; 0.1-0.2 s head and 0.15-0.3 s tail handles | Keep pre-punchline pauses up to 0.6-0.8 s |
| Fillers | Cut "um/uh" and stutters | Keep meaningful "like" and "you know"; gate on ASR confidence |
| Visual cadence | One change every 2-4 s; punch-ins to 110-120% | No more than one sound-accented zoom per 4-6 s |
| Captions | 1-3 words per chunk, ALL CAPS, 6-10 px stroke, active word highlighted | Stay inside x 60-940, y 210-1436 |
| Reframe | Active-speaker fill; split for rapid exchanges; 30-40% facecam for gameplay | ≥1-1.5 s shot hold; no crop interpolation across cuts |
| End | 0.2-0.6 s after the punchline or laughter tail | No fade, no outro, no next-speaker turn |
| Audio | −14 LUFS integrated, −1 dBTP, no added music | Any music bed 15-20 dB under the voice, ducked |
| Export | 1080×1920 H.264 High, AAC 48 kHz, source fps, ~8-12 Mbps at 30 fps | Clean master from the original source, never a re-download |

## Rights and originality are two separate gates every clip must pass

### Claims hit one video; strikes threaten the account

YouTube's Content ID turns a fingerprint match into a claim that blocks, monetizes or tracks the video. Claims "usually don't impact your channel", but disputing one without a valid reason can lead the owner to file a removal request. If the request appears valid, the content comes down and the channel gets a **copyright strike**. **Three strikes within 90 days** means termination ([YouTube Help](https://support.google.com/youtube/answer/2814000?hl=en); [YouTube Help](https://support.google.com/youtube/answer/6013276?hl=en)). For Shorts, any active claim of any type, including a manual claim, blocks a Short over one minute globally ([YouTube Help](https://support.google.com/youtube/answer/15424877?hl=en)). Music costs money even under a minute: Shorts revenue tied to a single music track is split half to music licensing ([Music Business Worldwide](https://www.musicbusinessworldwide.com/youtube-shorts-to-split-ad-revenue-between-music-rightsholders-and-creators-from-february-1/)). Meta's Rights Manager can mute a Reel seconds after posting ([Foxi Music](https://www.foximusic.com/blog/instagram-reels-music-copyright-legal-guide/)). TikTok bans repeat infringers ([TikTok IP Policy](https://www.tiktok.com/legal/page/global/copyright-policy/en)).

For stream sources, the 2020 wave of DMCA takedowns on Twitch was driven by music played on stream and captured in clips ([StreamScheme](https://www.streamscheme.com/twitch-dmca/)). One streamer was banned over what he said was under a second of Premier League footage ([Dexerto](https://www.dexerto.com/entertainment/twitch-banning-streamers-with-live-dmca-strikes-as-sports-category-booms-1569548/)). The tool's risk model should therefore weight strike-level exposure (unauthorized reposting, sports and TV footage) far above incidental music claims. It must never file disputes automatically.

### Every source needs a recorded rights basis, and "it's public" is not one

A podcast or stream is copyrighted the moment it is recorded. There is **no "30 seconds or less" safe harbor**, and crediting the source is not permission ([Copyright Alliance](https://copyrightalliance.org/how-to-avoid-copyright-infringement-on-podcasts/)). Kelley Drye's August 2026 analysis warns that clipping publicly available content "is not necessarily free to reuse for commercial purposes". It notes that at least 47 states recognize a right of publicity over a person's name, image, voice and likeness, and that paid clippers must disclose the relationship "clearly and prominently" ([All About Advertising Law](https://www.allaboutadvertisinglaw.com/2026/08/social-clipping-and-influencer-marketing-key-legal-risks.html)).

The legitimate market is large. Whop Content Rewards pays clippers $0.20-$6 per 1,000 views, averaging about $1. Vyro, launched by MrBeast and ViewStats, pays a flat $3 per 1,000 views capped at $1,000 per clip. Kick-backed campaigns pay $10 or more ([OpenClip](https://openclip.app/guides/get-paid-to-clip-streamers)). The streamer N3on reportedly paid 303 clippers $1.4M over five weeks ([CreatorDB](https://creatordb.app/creator-news/the-rise-of-the-clip-economy/)). These campaigns authorize specific source material. Whop briefs name the source content and allowed platforms ([Whop](https://whop.com/blog/whop-content-rewards/)), and Vyro rejects unauthorized footage, missing disclosures and the same clip posted twice on one account ([Vyro](https://vyro.com/clipper-terms)). A sponsor's payment is not a license: clip farms paid by Stake reportedly used Kai Cenat footage without his permission ([Sports Illustrated](https://www.si.com/esports/news/stake-clips-fearbuck)). And a creator's permission covers only what the creator owns, not the songs, broadcasts or other creators' videos that appear in the stream.

Every source should therefore carry one of four recorded bases before processing:

- **owned**
- **licensed**, with the platforms, monetization rights and edit rights stated
- **campaign**, with the campaign ID and terms stored
- **public domain or CC0/CC BY**

Unlicensed third-party sources should be blocked by default. For licensed relationships, the workflow should ask the licensor to allowlist the channel in Content ID, because otherwise the licensor's own fingerprints can still claim the clips ([YouTube Help](https://support.google.com/youtube/answer/3367684?hl=en)).

Fair use is not a workable default. In *Hosseinzadeh v. Klein* (2017), a commentary-heavy reaction video was protected as "quintessential criticism and comment", but the court distinguished uses "more akin to a group viewing session" ([Eric Goldman](https://blog.ericgoldman.org/archives/2017/08/reaction-video-protected-by-fair-use-hosseinzadeh-v-klein.htm)). The Supreme Court's 2023 *Warhol v. Goldsmith* decision weighs against commercial uses that share the original's purpose ([Holland & Knight](https://www.hklaw.com/en/insights/publications/2023/06/us-supreme-court-holds-that-first-factor-of-fair-use)). The streamer Denims won a fair-use ruling only after pausing the video **more than 200 times** to criticize it ([Copyright Lately](https://copyrightlately.com/ethan-klein-denims-reaction-video-fair-use-tentative-ruling/)). A highlight channel reposting a podcast's best moments with captions serves the podcast's own purpose and competes with its clipping market. That is a poor fair-use candidate, and the tool should never label output "fair use". UK and EU exceptions for quotation, criticism and review are narrower and tied to a genuine purpose ([CopyrightUser](https://www.copyrightuser.org/understand/parody-pastiche/)).

### Music licenses do not travel, so ship none

Every in-app music library is licensed only on its own platform:

- **TikTok's Commercial Music Library** (1M+ tracks) may be used only within TikTok ([Third Chair](https://usethirdchair.com/blog/tiktok-commercial-music-library-what-it-covers-and-what-it-doesn-t); [Foxi Music](https://www.foximusic.com/blog/commercial-music-licensing-tiktok-guide/)).
- **Meta's Sound Collection** (14,000+ tracks) is cleared only on Meta products ([Audiodrome](https://audiodrome.net/for-creators/facebook-music-licensing-faqs/)).
- **YouTube Audio Library** tracks carry conflicting interpretations about use off YouTube ([vidIQ](https://vidiq.com/blog/post/royalty-free-music-youtube-audio-library/); [LicenseOrg](https://www.licenseorg.com/guide/music-audio/youtube-audio-library)), so treat non-CC tracks as YouTube-only.

Music baked into an exported file therefore never carries those licenses. TikTok's Music Usage Confirmation is self-attestation, not clearance ([Gelato](https://www.gelato.com/blog/tiktok-music-usage-confirmation)).

Subscription libraries handle Content ID by safelisting connected channels. A claim from Epidemic Sound means the channel was not on its safe list ([Epidemic Sound](https://www.epidemicsoundhelp.com/hc/en-us/articles/26253712691730-Why-was-a-Content-ID-claim-received-from-Epidemic-Sound)), and Artlist's Clearlist covers YouTube, Instagram, TikTok and Facebook channels, with coverage tied to an active subscription at publish time ([Artlist](https://artlist.io/help-center/privacy-terms/artlist-license/)). "Free" does not mean claim-proof: some Pixabay contributors register their tracks in Content ID ([Pixabay](https://pixabay.com/blog/posts/how-to-clear-a-youtube-content-id-claim-with-a-pix-190/)). Creative Commons NonCommercial terms turn on the primary purpose of the use ([Creative Commons](https://wiki.creativecommons.org/wiki/NonCommercial_interpretation)), so exclude NC and ND tracks from monetized or campaign clips. When music is used, store with each clip the track ID, provider, license ID, plan tier, the safelisted channels and the publish timestamp.

### Detect music and cut around it; never disguise it

Every candidate needs two complementary detectors. inaSpeechSegmenter ranked first among open-source tools on a broadcast benchmark, but it **tags speech over music as speech** ([inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter/blob/master/README.md)). That is exactly the podcast and stream case it would miss, so use it only to find intros, outros and music-only breaks. For music under talk, use a multi-label AudioSet tagger such as YAMNet or PANNs (mAP 0.439) at about 1 s windows, in which "Speech" and "Music" can both score high on the same frame ([TensorFlow](https://www.tensorflow.org/tutorials/audio/transfer_learning_audio); [IEEE SPS](https://signalprocessingsociety.org/newsletter/2023/01/panns-large-scale-pretrained-audio-neural-networks-audio-pattern-recognition)). Then fingerprint the flagged windows to name the track. AcoustID's free tier covers only non-commercial use; commercial plans start at €50 a month ([AcoustID](https://acoustid.biz/)). ACRCloud and Audible Magic are commercial alternatives, and Audible Magic counts Twitch among its customers ([Audible Magic](https://www.audiblemagic.com/?page_id=369)).

When music is detected above a threshold calibrated on the user's own content, the tool should take one of three actions: move the clip boundaries to exclude it, discard the candidate, or route it to human review with an explanation. A detected but unidentified segment counts as **not cleared**. The tool should also flag likely embedded third-party video from transcript cues such as "let's watch this" or references to sports and TV, and treat those clips as strike-level risk. Pitch-shifting, speeding up or filtering audio to slip past matching is evasion. It does not cure infringement and has no place in the pipeline. Detector outputs belong in a per-clip audit trail next to the rights record.

### Originality has tightened into a reach gate of its own

Copyright permission does not satisfy platform originality rules. YouTube's reused-content rules apply "regardless of whether you have permission from the original creator". Clips with storyline, commentary or critical context can be monetized, while compilations without them cannot ([YouTube Help](https://support.google.com/youtube/answer/1311392?hl=en)). On **1 October 2026**, Creator Liaison Rene Ritchie said Shorts recommendations will reduce reach for barely changed re-uploads. Remixers must add their own value, "not just VO descriptions of what's happening on screen, minor technical edits, or template-based bulk changes". YouTube gave no start date and offers no dashboard showing whether a channel is affected ([Search Engine Journal](https://www.searchenginejournal.com/youtube-original-shorts-reposted-clips-reach/591774/)).

Instagram removes accounts from recommendations once they repost others' content without significant edits **10+ times in 30 days**. Mosseri said changing playback speed or adding a screenshot of the creator's name is not enough, while voice-overs and reaction clips count as transformative ([Engadget](https://www.engadget.com/instagrams-algorithm-overhaul-will-reward-original-content-and-penalize-aggregators-130018977.html); [Tubefilter](https://www.tubefilter.com/2026/04/30/instagram-removes-algorithm-recommendations-repost-content-aggregator/)). Since November 2025, Meta has also let creators fingerprint their Reels and block reposts ([Engadget](https://www.engadget.com/social-media/facebook-rolls-out-new-tools-for-creators-to-track-accounts-stealing-their-content-201020255.html)). Meta's July 2025 Facebook crackdown says stitching clips together or adding a watermark is not a meaningful enhancement ([Search Engine Journal](https://www.searchenginejournal.com/meta-follows-youtube-in-crackdown-on-unoriginal-content/551096/)). TikTok excludes content "imported or uploaded from… **webcasts**" without new creative edits from the For You feed. It also excludes anything bearing a visible watermark, logo or QR code ([TikTok Creator Academy](https://www.tiktok.com/creator-academy/article/tiktok-originality-policy)), which means Twitch and Kick overlays and sponsor QR codes must be cropped out.

Captions, zooms, emoji and progress bars are "light edits" by all three platforms' descriptions. The tool can legitimately add:

- a context hook written specifically for the clip
- an on-screen explanation of why the moment matters
- user-recorded commentary
- a multi-moment narrative with analysis

It should also always credit the source with a handle and link, vary templates across posts, and refuse to post the same moment twice on one account.

The asset layer needs the same discipline:

- **Fonts:** use open-licensed fonts.
- **Emoji:** use open emoji sets such as Twemoji (CC BY 4.0), not Apple's proprietary artwork ([luizbizzio/emojis](https://github.com/luizbizzio/emojis)).
- **Stock footage:** be aware that Pexels and Pixabay do not verify model releases ([PicDefense](https://picdefense.io/resources/source-intel/pexels/)).
- **AI-generated material:** purely AI-generated assets are not copyrightable in the US ([Library of Congress](https://www.loc.gov/item/prn-25-010/copyright-office-releases-part-2-of-artificial-intelligence-report/2025-01-29/)), and YouTube requires disclosure of realistic synthetic content ([YouTube Blog](https://blog.youtube/inside-youtube/our-approach-to-responsible-ai-innovation/)). Never synthesize a host's or guest's voice or likeness without consent.

| Gate | Check | Action on failure |
|---|---|---|
| Rights basis | Owned, licensed, campaign (ID and terms stored) or CC0/CC BY recorded | Block processing |
| Third-party music | Music-present score above the calibrated threshold anywhere in the clip; fingerprint logged | Re-cut boundaries, discard, or human review |
| Third-party video | Transcript cues; sports, TV or other-creator footage | Human review; treat as strike-level |
| YouTube length | Any claimable material and length >59 s | Cap at 59 s or drop the Shorts export |
| Originality | Third-party source with only captions or crops; watermark, logo or QR present | Require a context or commentary layer; strip overlays |
| Duplicates | >30-40% spoken overlap with a clip already on the account | Block the post |
| Disclosure | Paid campaign or sponsor relationship | Apply the paid-partnership toggle or "#ad" |
| Assets | Font, emoji, stock, music and AI licenses recorded | Swap to an allowlisted asset |

## Conclusion

Detection is not the technical frontier. Every serious clipper already chains speech recognition, an LLM pass, reframing and captions, and the open-source versions are nearly as capable. What nobody offers is a score shown to predict outcomes. Rhapsody's result, in which a small fine-tuned model with audio features beats frontier LLMs zero-shot, shows the path. So does the fact that YouTube's "Most replayed" heatmaps give free labels. The durable advantage goes to whichever tool closes the loop: it posts with the user's consent, ingests engaged views, viewed-vs-swiped rates and skip rates, normalizes them per account to strip out the follower-count effect, and retrains. The first experiment worth running in that loop is the unresolved one: payoff-first cold opens against setup-first openings.

The policy direction of 2025-2026 also changes the economics of clipping. YouTube's October 2026 language singles out "template-based bulk changes", which describes the default output of every auto-clipper. Instagram cuts off recommendations after ten unoriginal reposts in 30 days, and Meta now lets owners block reposts by fingerprint. Combined with *Warhol*, this narrows the durable market to owned and authorized sources, where the tool's job is to make each clip distinct. The compliance rules and the performance heuristics mostly point the same way. No added music avoids claims, keeps Shorts revenue whole, and matches what viral clips actually do. No watermarks keeps clips eligible for TikTok's feed. No outros keeps viewers until the loop. A duplicate guard satisfies the originality policies and spreads one episode's moments across a steady posting cadence. A tool built to be copyright-safe in 2026 is, in most respects, also built to perform.
