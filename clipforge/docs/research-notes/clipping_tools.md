# AI Clipping Tools (2025-2026): Moment Detection, Virality Scoring and Editing Pipelines

> Method note for the report writer: research was done on 2026-10-02. WebFetch was blocked by the network egress proxy for almost every non-GitHub domain (help.opus.pro, opus.pro, eesel.ai, creatify.ai, castmagic.io, clipme.com and others). So most product facts below come from search-engine result summaries of the cited pages, not from full-page reads. GitHub READMEs were read in full. Many "reviews" are published by competing clipping vendors (e.g., quso.ai reviewing Vizard, Reap benchmarking itself #1, Choppity ranking itself #1, CapCut "resource" pages, SendShort reviewing Munch/2short/Spikes), so they may be biased. That is flagged where relevant. Prices change often, so treat every price as a point-in-time figure.

## Q1. How do the tools find moments, and what do their scores mean (sub-scores and criteria)?

### Takeaway
Nearly every tool starts from a transcript: ASR, then an LLM or NLP pass that picks self-contained segments, then a 0-99 or 0-100 "virality score" used to rank them. The only meaningful technical split is between (a) transcript-only selection, (b) newer multimodal video-LLM selection (OpusClip ClipAnything, Vizard Spark) for content with little dialogue, and (c) domain-signal selection for gaming/streams (Twitch chat spikes, emotes, kill detection, voice hype). OpusClip is the only vendor found that publishes named sub-scores (Hook, Flow, Value, Trend). Everyone else describes criteria loosely, and no vendor publishes weights or calibration against real view counts.

### Cited Findings

**OpusClip: Virality Score and ClipAnything**
- OpusClip's Virality Score ranges from 0 to 99; higher scores suggest a greater chance of engagement and shares. — [OpusClip Help: Virality Score](https://help.opus.pro/docs/article/virality-score) (via search summary)
- The score is described as built from four signals: **Hook** (does the introduction grab attention and relate to the main topic), **Flow** (does the video flow logically with a satisfying conclusion), **Value** (does it offer value and create emotional resonance), and **Trend** (does it align with current trends and audience interests). — [OpusClip Help: Virality Score](https://help.opus.pro/docs/article/virality-score); [NemoVideo Opus Clip Review 2026](https://www.nemovideo.com/blog/opus-clip-review-2026)
- Third-party caveat: the score is "a ranking tool, not a guarantee". It is good at telling you which of ten clips is strongest, but "a 92 won't reliably beat a 78" on the platform. One reviewer estimates it "gets the hook right maybe 60-70% of the time on clean talking-head content", with crosstalk-heavy interviews, B-roll-heavy segments and jargon scoring inconsistently. — [NemoVideo review](https://www.nemovideo.com/blog/opus-clip-review-2026) / [FrankX Opus workflow 2026](https://www.frankx.ai/blog/ultimate-opus-clip-workflow-2026) (search summary; exact page attribution between these two is uncertain)
- ClipAnything is marketed as "the first-ever multimodal AI clipping" model. It clips "any moment from ANY video using visual, audio, and sentiment cues, including videos with little to no dialogue". — [OpusClip Help: ClipAnything](https://help.opus.pro/docs/article/9947095-clip-anything); [OpusClip ClipAnything page](https://www.opus.pro/clipanything)
- ClipAnything works in two steps. (1) It "analyzes each frame through visual, audio, and sentiment cues, identifying objects, scenes, actions, sounds, emotions, texts, and more. Each scene is then rated based on its virality potential." (2) Users "clip with customized prompts" (e.g., "compile all the scoring from a sports game"). — [OpusClip ClipAnything page](https://www.opus.pro/clipanything)
- A third-party description says ClipAnything analyzes four signals in parallel: visual cues, audio sentiment, facial expressions and narrative structure. That is why it works on gaming, sports and wordless content "where transcript-based tools fail". — [ThePlanetTools OpusClip review 2026](https://theplanettools.ai/tools/opusclip) (secondary source)
- OpusClip has two clipping models, **ClipBasic** (the transcript-centric original) and **ClipAnything**. ClipAnything usually yields slightly more clips. — [OpusClip Help: How many clips](https://help.opus.pro/docs/article/how-many-clips)
- A **genre** setting "will apply suitable AI curation models". Options: Auto, Q&A, Commentary, Marketing, Webinar, Motivational speech, Podcast, Academic, Listicle, Product reviews, How-to, Comedy, Sports commentary, and more. **topicKeywords** steer selection toward relevant moments. — [OpusClip API: Curation preferences](https://help.opus.pro/api-reference/schemas/curation-preferences)
- OpusClip announced $30M in funding together with the launch of ClipAnything. — [OpusClip blog](https://www.opus.pro/blog/opusclip-celebrates-30m-in-funding-and-the-launch-of-clipanything) (title only; not read)

**Vizard**
- Every clip gets a 0-100 viral score, described as based on "speech energy, topic transitions, and engagement signals". — [Creatify Vizard review](https://creatify.ai/review/vizard-ai); [quso.ai Vizard review (competitor)](https://quso.ai/blog/vizard-ai-review)
- A more detailed third-party description calls it a weighted stack of "complete sentences, pacing, audio energy, hook strength at the start, and how self-contained the moment is". Vizard "works from the transcript... layered with scene detection and active-speaker tracking". — [Valmera Vizard review](https://valmera.io/blog/vizard-review); [Fahim AI how-to-use Vizard](https://www.fahimai.com/how-to-use-vizard) (search summary)
- **Spark 1.0**, described as Vizard's multimodal video LLM (launched 1 Oct 2024), adds prompt-based clipping for content with little or no dialogue (e.g., prompts like "goal celebration", "emotional close-up"). — [Valmera Vizard review](https://valmera.io/blog/vizard-review) (search summary)
- Independent reviews call the viral score "directionally useful but inconsistent" and recommend a manual pass. — [Valmera Vizard review](https://valmera.io/blog/vizard-review); [Creatify Vizard review](https://creatify.ai/review/vizard-ai)

**Klap**
- Klap scores each clip 0-100 on "hook strength, pacing, and topic coherence". The AI "analyzes the transcript, finds the most engaging, self-contained topics". — [ToolsForHumans Klap review 2026](https://www.toolsforhumans.ai/ai-tools/klap)
- Vendor claim: Klap's AI analyzes "pacing, vocal energy, and visual dynamics, comparing them to top-performing content in your niche", and it is "trained specifically on viral short-form video data" to pick "hooks, payoffs, and emotional peaks". — [Klap AI clip generator page](https://klap.app/tools/ai-clip-generator); [Klap vs Opus page](https://klap.app/alternatives/opus-clip) (vendor marketing)

**Submagic**
- Magic Clips "automatically identifies the strongest moments in a long-form video and packages them as multiple ready-to-post shorts in one pass". — [Submagic Magic Clips page](https://www.submagic.co/features/magic-clips)
- No Submagic virality score was documented in the search results. Submagic's differentiation is caption styling and auto-editing, not scoring. — [HeyGen Submagic alternatives](https://www.heygen.com/blog/submagic-alternatives); [PassiveShorts Opus vs Submagic](https://passiveshorts.com/blog/opus-clip-vs-submagic/)

**Descript (Create Clips / Underlord)**
- Create Clips (AI Tools panel > Repurpose) "uses AI to scan your composition and pull out short, self-contained cuts". Users set the number of clips (1-20) and the length (10 s to 5 min), with an optional "topic, goal, or criteria". You can also ask Underlord in natural language. — [Descript Help: Create clips](https://help.descript.com/hc/en-us/articles/10119670449293-Create-clips-from-your-content); [Descript Clips page](https://www.descript.com/clips)
- Descript says it "taught... Underlord what works on social". When scanning, it looks for "high-energy segments, laughter, or self-contained stories". — [Descript Clips page](https://www.descript.com/clips); [InsideRadio](https://www.insideradio.com/free/descript-s-ai-powered-underlord-now-creates-social-ready-video-snippets/article_1a73969e-3270-46f6-96e9-6ccc5a90edb5.html)
- No numeric virality score is documented for Descript.

**Riverside Magic Clips**
- Magic Clips "automatically identifies, highlights and makes clips" from a recording (launched 2023). — [Riverside Magic Clips page](https://riverside.com/magic-clips); [Podnews press release](https://podnews.net/press-release/riverside-magic-clips)
- A third-party description says it analyzes transcript + audio with three signals: keyword relevance, sentiment (strong opinions, emotional peaks) and speaker energy (volume, pacing, stress). Each segment gets a "Viral Score". — [Conbersa: Podcast clips from Riverside](https://www.conbersa.ai/learn/podcast-clip-from-riverside-recording); [Blitzcut Riverside review 2026](https://blitzcutai.com/blog/riverside-magic-clips-review-2026) (secondary, not confirmed on Riverside's own pages)
- Higher plans add custom clip durations, a focus speaker, and keywords to guide selection. — [Riverside Magic Clips page](https://riverside.com/magic-clips); [Castmagic Riverside pricing](https://www.castmagic.io/blog/riverside-pricing)

**Captions app (now Mirage)**
- "AI Shorts finds the best clips and formats them for social automatically when you upload a long video." In Clips, users "can now ask for more or different short clips from the same long-form video without starting over". — [Captions: What's new](https://captions.ai/help/whats-new)
- No published virality score or selection criteria were found for Captions/Mirage.

**Munch**
- Munch differentiates on trend data. A "Trending SEO Score" predicts performance from trending keywords/topics, with dashboards of top keywords, search volume, "munched clips" and competition. Its AI "analyzes trending topics, keyword relevance, speech patterns, and emotional cues". — [SendShort Munch review (competitor)](https://sendshort.ai/guides/munch-review/); [SqueezeGrowth GetMunch review](https://squeezegrowth.com/getmunch-review/); [Kompozy Munch review 2026](https://kompozy.io/reviews/munch)
- Munch had a 2026 "Munch Studio" relaunch that adds a social layer for small businesses. — [Kompozy Munch review 2026](https://kompozy.io/reviews/munch)

**Quso.ai (formerly vidyo.ai)**
- Rebranded to Quso.ai (around Dec 2024). The clipping engine finds segments, reframes them vertically with face tracking, burns in captions, and ranks clips by a "Virality Score". — [Filmora Quso review](https://filmora.wondershare.com/video-editor-review/quso-ai-review.html); [SocialRails Quso review](https://socialrails.com/blog/quso-ai-review)
- No sub-score definitions found.

**2short.ai**
- Third-party description: scores moments on "engagement potential, standalone clarity, and pacing and energy"; aimed at long-form YouTube videos. — [Creatify 2Short review](https://creatify.ai/review/2short-ai); [SendShort 2short review](https://sendshort.ai/guides/2short-review/)

**StreamLadder ClipGPT (streams/gaming)**
- ClipGPT analyzes "spikes in chat activity and hype, moments of high excitement or emotion in the streamer's voice, key in-game events like multi-kills or clutch wins, and audience reactions using specific emotes". — [StreamLadder ClipGPT](https://www.streamladder.com/clipgpt); [StreamLadder AI Clipping](https://www.streamladder.com/clipgpt/ai-clipping)
- Every detected moment gets a 0-100 score. ClipGPT picks up to 10 key moments and "ranks by virality". — [StreamLadder ClipGPT](https://www.streamladder.com/clipgpt)

**Eklipse (gaming)**
- Identifies highlights using "kill detection and audio hype signals". "Quality filters check audio and video" and "dead time is trimmed off automatically". — [Eklipse AI Highlights](https://eklipse.gg/features/ai-highlights/); [Eklipse blog: AI clip maker gaming](https://blog.eklipse.gg/tools/ai-clip-maker-gaming.html)

**Spikes Studio**
- Automatically analyzes long videos to extract multiple shorts. Optimized for Twitch: it processes streams and generates clips "as soon as a broadcast ends". No scoring details found. — [SendShort Spikes review](https://sendshort.ai/guides/spikes-review/); [MakerStack Spikes review](https://makerstack.co/reviews/spikes-studio-review/)

**Wisecut, Choppity, Kapwing**
- Wisecut: "highlight detection for viral-worthy moments", but its core is silence removal/pacing. — [CapCut resource page (competitor)](https://www.capcut.com/resource/top-7-autocut-solutions-for-professional-video-editing)
- Choppity: "semantic highlight detection" that analyzes "meaning, jokes, insights, and audience-engaging moments". — [CapCut resource page (competitor)](https://www.capcut.com/resource/top-7-autocut-solutions-for-professional-video-editing)
- Kapwing AI Clip Maker "automatically transcribes and analyzes your footage to identify standout moments", and users can "guide the AI with a few prompts about what topics you want". — [Kapwing AI Clip Maker](https://www.kapwing.com/ai/clip-maker). Claims that Kapwing uses audio intensity, visual activity and sentiment come from a secondary article that says the tech "likely" involves these, so they are speculative. — [ReelMind on Kapwing](https://reelmind.ai/blog/kapwing-s-ai-video-highlight-maker-create-engaging-clips)

**Newcomers / notable others**
- **Reap**: positions itself as an agentic "Clipping Agent". In its own April 2026 benchmark it ranked itself #1 of 9 tools, with a 4-5 min time-to-first-clip on a 90-min podcast vs ~25 min for OpusClip Pro. — [Reap benchmark report](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026); [Reap Clipping Agent](https://reap.video/clipping-agent) (self-published, so biased)
- **WayinVideo**: "keyword-precision clipping". **Ssemble**: cheaper direct Opus competitor. **Vugola AI**: $14/mo clipping + captions + scheduling. **CineVision Vertigo**: subject-preserving reframing. — [Choppity Opus alternatives](https://www.choppity.com/blog/best-opus-clip-alternatives/); [WayinVideo blog](https://wayin.ai/blog/opusclip-alternative/); [Vugola blog](https://www.vugolaai.com/blog/best-opus-clip-alternatives-2026); [CineVision blog](https://cinevision.ai/blogs/opus-clip-alternative/) (all vendor blogs)
- **CapCut** long-video-to-shorts "analyzes structure, dialogue, and visual cues", accepts up to 3 hours / 10 GB, and generates AI titles/descriptions with one-click publishing. — [CapCut resource page](https://www.capcut.com/resource/top-5-long-video-to-shorts-tools) (vendor)
- **YouTube** 2025-2026 creator AI news centers on *generative* Shorts (Veo 3 Fast in Shorts; AI-likeness Shorts announced 21 Jan 2026), not auto-clipping of long-form. — [YouTube Blog](https://blog.youtube/news-and-events/generative-ai-creation-tools-made-on-youtube-2025/); [Android Police](https://www.androidpolice.com/creators-can-now-use-ai-versions-of-themselves-to-make-youtube-shorts/)

**Cross-tool critique**
- "None of them judge whether a clip is actually good"; virality scores should be treated "as a shortlist rather than a final editor". "Scoring is the only part where tools genuinely differ, and it's the only part you cannot do faster by hand." — [less-tools.com: Best AI clipping tool 2026](https://less-tools.com/best-ai-video-clipping-tool/)

### Inferences
- **The standard architecture** across commercial tools is:
  1. ASR with word timestamps
  2. LLM/NLP segmentation into self-contained candidates, with optional genre/topic/keyword steering
  3. A rubric-style score whose criteria converge on: hook strength in the first seconds; coherence/self-containedness ("complete sentences", "Flow", "standalone clarity", "topic coherence"); value/emotion ("Value", sentiment, emotional peaks); delivery energy (vocal energy, pacing); and trend/keyword alignment ("Trend", Munch SEO score)
  4. Rank and return the top-N
- **OpusClip's Hook / Flow / Value / Trend breakdown** is the most explicit public rubric. It maps cleanly onto an LLM-judge prompt with four sub-scores plus an aggregate.
- **Signals by content type:**
  - Gaming/stream tools add non-transcript signals: chat velocity, emote bursts, in-game event detection (kill feed), audio loudness/hype.
  - Multimodal video-LLMs (ClipAnything, Vizard Spark, FunClip's TwelveLabs Pegasus integration) are the 2024-2026 frontier for low-dialogue content.
- **Prompt/keyword steering is now table stakes:** OpusClip topicKeywords + prompts, Descript topic/goal, Riverside keywords, Kapwing prompts, Vizard Spark prompts.
- **No vendor publishes how well the score predicts real views.** That makes "score calibrated on your own posted-clip outcomes" a plausible differentiator for a new tool. Speculative design implication.

Summary matrix (synthesized from the findings above):

| Tool | Primary detection signals | Score | Published sub-scores |
|---|---|---|---|
| OpusClip | Transcript (ClipBasic); multimodal visual+audio+sentiment (ClipAnything); genre models | 0-99 | Hook, Flow, Value, Trend |
| Vizard | Transcript + scene detection + speaker tracking; Spark multimodal prompts | 0-100 | None official (3rd-party: sentence completeness, pacing, audio energy, hook, self-containedness) |
| Klap | Transcript topics + (claimed) vocal energy/visual dynamics | 0-100 | None official (hook, pacing, topic coherence per reviews) |
| Riverside | Transcript + audio (keywords, sentiment, energy per 3rd party) | "Viral Score" | Not published |
| Munch | Transcript + trending-keyword/SEO data | Trend/SEO score | Keyword/trend metrics |
| Quso | Transcript + face tracking | Virality Score | Not published |
| StreamLadder | Chat spikes, voice hype, in-game events, emotes | 0-100 | Not published |
| Eklipse | Kill detection + audio hype | None found | — |
| Descript / Captions / Submagic / Kapwing / Choppity / Wisecut | Transcript/LLM ("self-contained", "high-energy", "laughter", semantic) | None found | — |

### Gaps
- Official OpusClip help pages could not be fetched (egress blocked), so the exact help-center wording for each sub-score and whether sub-scores show numerically in the UI could not be verified first-hand.
- No vendor discloses the model weights, training data or validation of its score (e.g., correlation with views). None was found for any tool.
- Riverside's three-signal description comes from secondary sources only.
- No scoring details were found for Captions/Mirage, Choppity, Kapwing, Wisecut or Spikes Studio.
- Direct Reddit threads could not be retrieved; Reddit sentiment is only reflected via review aggregators.

## Q2. What editing do they apply automatically?

### Takeaway
The automated "finishing" bundle has become standard:
- 9:16 reframing with face/speaker tracking
- multiple layouts (fill/fit/split-screen, gameplay+facecam)
- animated word-level captions with keyword highlight/emoji
- filler and silence removal
- AI hook titles
- AI or stock B-roll
- multi-platform scheduling and auto-posting

Differentiation now sits in reframing quality (multi-speaker, object tracking), caption style templates, and generative extras (AI B-roll, dubbing, AI-generated FFmpeg effects).

### Cited Findings
- **OpusClip**
  - Animated captions in 20+ languages that "can sprinkle in emoji and keyword highlights".
  - Every clip ships with captions, a vertical crop and an AI hook ("an opening line built to stop the scroll").
  - The Starter plan includes auto-posting, filler-word and silence removal, and no watermark.
  - Sources: [ThePodcastHost on OpusClip](https://www.thepodcasthost.com/recording-skills/can-opusclip-make-your-podcast-go-viral/); [eesel OpusClip 2026 guide](https://www.eesel.ai/blog/opusclip)
- **OpusClip layouts**: "fit, fill, split, and 30/70 gaming layouts". — [The Rundown: OpusClip](https://www.therundown.ai/tools/opus-clip); [OpusClip Google Play listing](https://play.google.com/store/apps/details?id=pro.opus.clip&hl=en_US)
- **OpusClip ReframeAnything** uses object tracking to keep moving subjects centered without manual keyframing. — [Filmora OpusClip review](https://filmora.wondershare.com/video-editor-review/opusclip-ai.html); [ForaSoft AI editing tools 2026](https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/opus-clip-descript-submagic-captions-ai-video-editor-tools-2026)
- **OpusClip 3.0** added:
  - AI B-roll generation (text-to-video, with selectable styles)
  - "mid form clips (3-15 min)"
  - genre-specific curation
  - viral caption templates
  - a captions-only mode
  - Source: [Feisworld: OpusClip 3.0 released](https://www.feisworld.com/blog/opusclip-30-released)
- **OpusClip scheduler** publishes or queues to TikTok, YouTube Shorts, LinkedIn, Facebook posts, and Facebook/YouTube Ads. — [OpusClip editor page](https://www.opus.pro/editor); [AICreative OpusClip review](https://aicreative.ai/ai-tools/opusclip) (search summary; exact attribution uncertain)
- **Submagic**
  - "AI Auto-Edit" generates a hook title, animated captions, silence and filler-word removal, contextual B-roll from the Storyblocks library, auto-zoom and SFX at transitions.
  - Caption styles are modeled on creator formats (e.g., Alex Hormozi, Iman Gadzhi), in 48 languages with a claimed 99% accuracy.
  - Sources: [Submagic review (skybreakai)](https://skybreakai.com/blog/submagic-review-2026); [UCStrategies Submagic review](https://ucstrategies.com/news/submagic-review-2026-pricing-features-is-it-worth-it-for-creators/); [HeyGen Submagic alternatives](https://www.heygen.com/blog/submagic-alternatives)
- **Klap**: facial-recognition auto-reframing to 9:16 and automatic animated captions. — [ToolsForHumans Klap review](https://www.toolsforhumans.ai/ai-tools/klap)
- **Quso**
  - Hook titles, filler-and-silence removal, "AI Reframe 2" speaker tracking
  - content calendar, scheduling to Instagram, TikTok, Facebook, YouTube, LinkedIn and X
  - AI dubbing in 29 languages, AI avatars
  - Sources: [SocialRails Quso review](https://socialrails.com/blog/quso-ai-review); [Filmora Quso review](https://filmora.wondershare.com/video-editor-review/quso-ai-review.html)
- **Vizard**: reframing, scheduled posting to up to 6 (Creator) or 20 (Business) social accounts, Brand Kit, public REST API. — [Plisio Vizard review](https://plisio.net/ai/vizard-ai); [ColdIQ Vizard](https://coldiq.com/tools/vizardai)
- **Descript**: generated clips appear as new compositions "complete with captions"; Underlord can also remove filler words etc. on request. — [Descript Clips page](https://www.descript.com/clips); [Descript Underlord](https://www.descript.com/underlord)
- **Riverside**: outputs 9:16 or 1:1 clips with burned-in captions, plus branding controls. — [Riverside Magic Clips](https://riverside.com/magic-clips); [Conbersa](https://www.conbersa.ai/learn/podcast-clip-from-riverside-recording)
- **Captions/Mirage**
  - AI Edit "uploads raw footage and returns a polished, caption-ready video with AI handling cuts, captions, music, and formatting".
  - Also offers eye-contact correction and per-shot noise removal, and splits audio into voice/music/background tracks.
  - Source: [Captions: What's new](https://captions.ai/help/whats-new); [Captions AI Edit](https://captions.ai/features/edit-with-ai)
- **StreamLadder**: animated captions and auto-cropping that frames gameplay and facecam (including VTubers), with direct publishing to TikTok/Reels/Shorts. — [StreamLadder ClipGPT](https://www.streamladder.com/clipgpt)
- **Spikes Studio**: animated brand-style captions, 16:9 to 9:16 reframing with face tracking, 99+ caption languages, AI-suggested B-roll, music and SFX library. — [SendShort Spikes review](https://sendshort.ai/guides/spikes-review/); [MakerStack Spikes review](https://makerstack.co/reviews/spikes-studio-review/)
- **2short.ai**: face tracking that keeps the speaker centered, animated subtitles in 20+ languages, 9:16/1:1/16:9. — [Creatify 2Short review](https://creatify.ai/review/2short-ai); [TechJockey 2short](https://www.techjockey.com/us/detail/2short-ai/)
- **Wisecut**: silence removal, pacing correction, automatic background-music selection, captions and translation. — [CapCut resource page](https://www.capcut.com/resource/top-7-autocut-solutions-for-professional-video-editing); [Capterra Wisecut reviews](https://www.capterra.com/p/236150/Wisecutvideo/reviews/)
- **Choppity**: multi-aspect-ratio output, automated captions and framing, transcript-native editing, native multi-platform posting. — [CapCut resource page](https://www.capcut.com/resource/top-7-autocut-solutions-for-professional-video-editing); [Choppity blog (self)](https://www.choppity.com/blog/best-opus-clip-alternatives/)
- **Reap** (self-reported): the only one of 9 benchmarked tools with a public REST API on the entry paid tier, a native MCP server, romanized captions, and a scheduler handling 60+ posts per platform per day. Only 2 of 9 tools supported dubbing in 30+ languages. — [Reap benchmark](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026)

### Inferences
- The "minimum viable" automated edit for a competitive tool is: 9:16 speaker-tracked reframe, plus word-level animated captions with keyword emphasis, plus a hook title overlay, plus filler/silence trim. These appear in nearly every product.
- B-roll is offered (stock via Storyblocks in Submagic; generative in OpusClip 3.0). But OpusClip's own data (Q5) shows only ~6% of "viral" clips use B-roll, so it is a lower-priority automation.
- Layout auto-selection is a distinct capability: split-screen for two speakers, gameplay+facecam 30/70, screencast. OpenShorts (Q6) shows an LLM choosing the layout per video.
- Native scheduling/auto-post is common (OpusClip, Vizard, Quso, Choppity, Reap, CapCut). This lets vendors close the loop to collect performance data, though none was found publishing that loop.

### Gaps
- No confirmation found of which tools auto-add progress bars or auto-music by default (only Wisecut music and Captions AI Edit music are documented).
- Auto-generated titles/descriptions/hashtags are documented for CapCut and implied for schedulers. Per-tool confirmation for Klap, Vizard and Munch metadata generation was not found.

## Q3. Default clip lengths and clips per hour of input

### Takeaway
Defaults cluster around 15-90 seconds:
- Klap: 30-60 s
- Vizard: 30-90 s
- OpenShorts: 15-60 s
- OpusClip API default: 0-90 s; app "Auto": up to 3 min

Long-tail options reach 3-15 min (OpusClip 3.0) or 5 min (Descript). Volume varies widely:
- OpusClip: roughly 23-42 clips per hour of input (most aggressive)
- Submagic: ~10-20 per hour
- Stream tools: 10-20 clips per stream
- Most open-source tools default to 3-15 clips

### Cited Findings
- **OpusClip app** defaults Clip Length to "Auto (0m-3m)", with options like <30 s or 60-90 s. — [OpusClip Help: Select clip length](https://help.opus.pro/docs/article/select-clip-length)
- **OpusClip API** `clipDurations` defaults to [0, 90] s. Other values: [0, 30], [30, 60], [60, 90], [90, 180]. A `range` (startSec/endSec) limits the processed span. — [OpusClip API: Curation preferences](https://help.opus.pro/api-reference/schemas/curation-preferences)
- Users have filed a feature request for a fully custom clip length. — [OpusClip Canny: Set custom clip length](https://opusclip.canny.io/feature-requests/p/set-custom-clip-length)
- **OpusClip clip counts by source length** (ClipAnything usually yields slightly more than ClipBasic). — [OpusClip Help: How many clips](https://help.opus.pro/docs/article/how-many-clips)

  | Source length | Clips |
  |---|---|
  | 0-3 min | 1-2 |
  | 3-10 min | 3-14 |
  | 10-30 min | 5-21 |
  | 30-60 min | 23-32 |
  | 60-120 min | 32-42 |
  | >120 min | 42-55 |

- **OpusClip 3.0** added "mid form clips (3-15 min)". — [Feisworld](https://www.feisworld.com/blog/opusclip-30-released)
- **Klap** cuts "30-60 second clips". Basic: 100 clips/month; Pro: 300 clips/month. — [ToolsForHumans Klap](https://www.toolsforhumans.ai/ai-tools/klap); [ScaleReach Klap review](https://www.scalereach.ai/blog/klap-review-for-short-form-teams)
- **Vizard** outputs ranked clips "typically 30-90 seconds each", with user-selectable lengths (multi-select) and uploads up to 10 GB on paid plans. — [Creatify Vizard review](https://creatify.ai/review/vizard-ai); [ai-video-clipper issue #102 (competitor survey)](https://github.com/PriyeshPandey2000/ai-video-clipper/issues/102)
- **Descript**: user-set 1-20 clips, 10 s to 5 min each. — [Descript Help](https://help.descript.com/hc/en-us/articles/10119670449293-Create-clips-from-your-content)
- **Submagic Magic Clips** turns a 30-minute video into 5-10 shorts (marketing elsewhere claims "20+"). The Starter plan caps at 15 videos/month and 2-minute videos. — [UCStrategies Submagic review](https://ucstrategies.com/news/submagic-review-2026-pricing-features-is-it-worth-it-for-creators/); [Submagic Magic Clips page](https://www.submagic.co/features/magic-clips)
- **StreamLadder ClipGPT**: up to 10 key moments per VOD. — [StreamLadder ClipGPT](https://www.streamladder.com/clipgpt)
- **Eklipse**: 10-20 clips per stream. The free plan was historically capped at 15 highlights per stream. — [Eklipse AI Highlights](https://eklipse.gg/features/ai-highlights/); [Capterra Eklipse](https://www.capterra.com/p/10015243/Eklipse/)
- **Riverside**: number of "sets" of Magic Clips per recording by plan (Free/Starter 1, Pro 3, Business 5); custom duration on higher plans. — [Castmagic Riverside pricing](https://www.castmagic.io/blog/riverside-pricing)

### Inferences
- A sensible default for a new tool: 15-60 s target with an "auto up to ~90 s" mode and an optional 90-180 s bucket. This matches market defaults, and OpusClip's own TikTok data finds a 41 s viral median, with 15-30 s overrepresented and 60-90 s underrepresented among viral clips (Q5).
- OpusClip's high output (~0.4-0.7 clips per input minute) is a deliberate "over-generate, let the user pick" strategy. Combined with the 20-40% discard rate (Q4), it implies precision is traded for recall.

### Gaps
- No official default clip counts were found for Vizard, Klap, Quso, 2short, Munch, Captions, Kapwing, Choppity or Spikes.

## Q4. Pricing and known limitations / user complaints

### Takeaway
Pricing is mostly metered by **input minutes** (OpusClip ~$0.10/min; Vizard credits = minutes; 2short and Wisecut by hours) or by **output clips** (Klap). Entry tiers run ~$10-30/mo, with annual discounts of ~50%.

The dominant quality complaints, consistent across tools:
- bad clip boundaries (mid-sentence cuts, missing setup or punchline)
- missing context
- reframing failures with multiple speakers or motion
- virality scores that don't predict real performance

Reviewers expect to discard or edit 20-40% of output. Business complaints focus on credit accounting, cancellation and refunds (OpusClip, Klap).

### Cited Findings

**Pricing (point-in-time; verify before use)**
- **OpusClip**: Starter $15/mo for 150 credits; Pro $29/mo for 300 credits ($174/yr, effective $14.50/mo); 1 credit = 1 minute of source processed (a 30-min podcast uses 30 credits regardless of clip count); ~$0.10/min on monthly plans. — [Creatify OpusClip pricing](https://creatify.ai/blog/opusclip-pricing-plans-and-what-you-ll-actually-pay-in-2026); [Castmagic OpusClip pricing](https://www.castmagic.io/blog/opus-clip-pricing); [Soku OpusClip pricing](https://soku.ai/alternatives/opus-clip/pricing)
- **Vizard**:
  - Free: 60 credits/mo, 720p, 3-day storage, 1 social account
  - Creator: $29/mo or $14.50/mo annual, 600 credits, 4K, no watermark, 6 social accounts, scheduling, REST API
  - Business: $39/mo or $19.50/mo annual, 20 social accounts, team features
  - Credits = minutes
  - Sources: [Plisio Vizard review](https://plisio.net/ai/vizard-ai); [ColdIQ Vizard](https://coldiq.com/tools/vizardai)
- **Klap**: Basic $29/mo ($14 annual) with 100 clips; Pro $79/mo ($39 annual) with 300 clips; Pro+ $189/mo ($94 annual); 1 free video. — [ToolsForHumans Klap](https://www.toolsforhumans.ai/ai-tools/klap); [ScaleReach Klap](https://www.scalereach.ai/blog/klap-review-for-short-form-teams)
- **Submagic**: $19-$69 per member per month ($12-$41 annual). Magic Clips is a separate **$19/mo add-on** that is not bundled into any plan. — [ColdIQ Submagic](https://coldiq.com/tools/submagic); [HeyGen Submagic alternatives](https://www.heygen.com/blog/submagic-alternatives)
- **Descript** (each tier also includes a separate allowance of AI credits for generative features):

  | Plan | Price (annual / monthly) | Media | AI credits |
  |---|---|---|---|
  | Free | $0 | 60 min | 100 one-time |
  | Hobbyist | $16 / $24 | 10 hrs | 400/mo |
  | Creator | $24 / $35 | 30 hrs | 800/mo |
  | Business | $50 / $65 | 40 hrs + bonus | 1,500 + bonus |

  — [Sonix Descript review](https://sonix.ai/resources/descript-review-pricing/); [Shade Descript pricing](https://shade.inc/blog/descript-pricing)
- **Riverside**: free plan plus paid tiers of roughly $24-$79/mo annual ($29-$99 monthly). Magic Clips controls (duration, speaker, keywords) are on higher tiers. Sources conflict on tier names and prices (one summary also lists "Pro $15/mo annual"). — [Castmagic Riverside pricing](https://www.castmagic.io/blog/riverside-pricing); [G2 Riverside pricing](https://www.g2.com/products/riverside/pricing)
- **Quso** (May 2026):
  - Free: 720p, watermark, 75 credits
  - Lite: $29 ($15 annual)
  - Essential: $39 ($20 annual)
  - Growth: $49 ($25 annual)
  - Sources: [SocialRails Quso review](https://socialrails.com/blog/quso-ai-review); [G2 Quso pricing](https://www.g2.com/products/quso-ai/pricing)
- **2short.ai**:
  - Free: 30 min of analysis/mo
  - Lite: $9.90 for 5 hrs
  - Pro: $19.90 for 15 hrs
  - Premium: $49.90 for 50 hrs
  - Sources: [TechJockey 2short](https://www.techjockey.com/us/detail/2short-ai/); [SendShort 2short review](https://sendshort.ai/guides/2short-review/)
- **Eklipse**: described as fully paid since June 2026 at ~$14.99/mo annual or $24.99 monthly — [cut.pro: Is Eklipse worth it 2026](https://cut.pro/en/blog/is-eklipse-worth-it-2026). Contradicted by listings of a Free plan (720p, 14-day storage, up to 15 highlights per stream), which may be outdated — [Capterra Eklipse](https://www.capterra.com/p/10015243/Eklipse/)
- **Spikes Studio**: Free 30 min/mo with watermark; Pro+ $12.99/mo; Enterprise $115.99/mo. — [SaaSworthy Spikes pricing](https://www.saasworthy.com/product/spikes-studio/pricing) (aggregator; possibly outdated)
- **Wisecut**: Starter $10/mo for 8 hrs; Professional $29/mo for 30 hrs; Enterprise custom. — [SendShort Wisecut review](https://sendshort.ai/guides/wisecut-review/); [SaaSworthy Wisecut](https://www.saasworthy.com/product/wisecut/pricing)
- **Choppity**: Free; Starter $15/user/mo ($7.50 annual); Pro $28/user/mo ($14 annual); Enterprise with API, white-labelling and SSO. — [xpay.sh Choppity pricing](https://www.xpay.sh/saas-pricing/choppity/)
- **Munch**: no public prices found; positioned around ~$49/mo. — [Dacast AI clip makers](https://www.dacast.com/blog/ai-clip-makers/) (search summary)

**Quality limitations and complaints**
- **OpusClip clip quality**:
  - In one test of six videos, 10 of 76 clips were unusable (cut mid-sentence, missed punchline, or misread topic).
  - Reviewers say to "plan to discard or tweak 20-40% of its output".
  - The AI "doesn't get nuance, comedic timing, or sarcasm" and cuts "a joke before the punchline".
  - Sources: [eesel OpusClip reviews](https://www.eesel.ai/blog/opusclip-reviews); [ScaleReach Opus review](https://www.scalereach.ai/blog/opus-clip-review)
- **OpusClip reframing**: chaotic multi-speaker crosstalk "confuses the reframing and causes it to chase the wrong face". With two people side by side or fast motion, "the frame can drift and clip someone out of shot". One user says that since a June 2024 editor release, framing was "normally wrong" and split-screen detection failed to detect the second speaker. Captions "often contain mistakes" and are hard to edit. — [eesel OpusClip reviews](https://www.eesel.ai/blog/opusclip-reviews); [Trustpilot OpusClip](https://www.trustpilot.com/review/opus.pro); [ProductHunt OpusClip reviews](https://www.producthunt.com/products/opus-clip/reviews?review=785678)
- **OpusClip billing**: of 302 Trustpilot reviews, 22% are 1-star. Complaints cite processing failures and slowdowns, confusing credit/refund mechanics, charges after cancellation, and one case of 570 credits deducted for a glitched project plus 180 more for a "FREE"-labelled fix. — [Trustpilot OpusClip](https://www.trustpilot.com/review/opus.pro); [CheckThat OpusClip reviews](https://checkthat.ai/brands/opusclip/reviews)
- **Klap**:
  - 3.6/5 on Trustpilot (40 reviews, Sept 2026).
  - Complaints about unresponsive Discord support, refunds that don't match the advertised 14-day money-back guarantee, and difficulty cancelling.
  - On a YouTube-tutorial source, the AI "failed to identify natural break points 7 times across 14 segment attempts" (cutting mid-explanation, stitching unrelated topics, starting without context).
  - Sources: [Trustpilot Klap](https://www.trustpilot.com/review/klap.app); [ScaleReach Klap review](https://www.scalereach.ai/blog/klap-review-for-short-form-teams); [Future Stack Klap review](https://future-stack-reviews.com/klap-starter-tierc/)
- **Vizard**: viral score "less reliable and benefits from manual review"; 4.7/5 on G2 (340 reviews) and 4.9/5 on Capterra (432) as of April 2026; reviewers praise time savings, portrait detection and captions. — [Creatify Vizard review](https://creatify.ai/review/vizard-ai); [G2 Vizard](https://www.g2.com/products/vizard-corp-vizard/reviews); [RoboRhythms "credit trap" review](https://www.roborhythms.com/vizard-ai-review/)
- **Submagic**: making Magic Clips a paid add-on "feels like a hidden cost". — [HeyGen Submagic alternatives](https://www.heygen.com/blog/submagic-alternatives)
- **Spikes Studio**: Trustpilot 2.5/5, with users questioning reliability. — [Spikes review aggregator (search summary)](https://www.serp-scale.com/tools/spikes-studio)
- **Munch**: most reviews rate it 3.5-3.8/5. — [BestReviews Munch](https://bestreviews.net/munch-reviews/); [Kompozy Munch review](https://kompozy.io/reviews/munch)
- **Wisecut**: praised for automating silence removal and jump cuts, but "may require additional manual adjustments for a polished final product". — [Capterra Wisecut reviews](https://www.capterra.com/p/236150/Wisecutvideo/reviews/)
- **Cross-tool**: "a fully featured, watermark-free, zero-cost AI clipping tool does not exist in 2026, and all tools require human review before posting". — [less-tools.com](https://less-tools.com/best-ai-video-clipping-tool/)
- **Reap's April 2026 benchmark** (self-published, Reap ranked #1): ranking was Reap > OpusClip > Vizard > Submagic > Klap > Descript > Veed.io > CapCut > Munch. Only 5/9 tools delivered a first clip in under 15 min on a 90-min source; 8/9 had ≥95% English caption accuracy. — [Reap benchmark](https://reap.video/reports/state-of-top-ai-video-clipping-tools-2026)

### Inferences
- The most valuable engineering targets for a new tool are the most-cited failures:
  1. **Boundary quality**: snap to sentence/turn boundaries using word timestamps, and check for setup-to-payoff completeness so punchlines aren't cut and context isn't missing.
  2. **Multi-speaker reframing**: diarization-driven active-speaker selection plus a split-screen fallback, with shot-cut-aware crop paths.
  3. **Score credibility**: explain the score's reasons and calibrate it on real outcomes.
- Transparent pricing (no surprise credit deductions for failed jobs, easy cancellation) is itself a differentiator given OpusClip's and Klap's review profiles.

### Gaps
- Reddit threads could not be accessed directly. Sentiment from r/NewTubers, r/podcasting, etc. is only reflected indirectly through aggregator articles.
- G2 numeric ratings for OpusClip, Klap and Quso were not retrieved.
- Several prices come from aggregators or competitor blogs and may lag official pricing pages, which could not be fetched.

## Q5. Published data on what correlates with clip performance

### Takeaway
OpusClip is the only vendor found publishing quantitative "what goes viral" research. It covers 2026 data pages for TikTok, YouTube Shorts and YouTube drawn from 13.5M+ clips processed by its engine:
- Hook type is the biggest single driver measured (roughly a 2x spread on TikTok, 5.9x on YouTube Shorts).
- "Expert Explainer" is the most common viral storyline.
- Burned-in animated captions appear in ~80% of viral clips, while B-roll, music and transitions are rare.
- The TikTok viral median length is ~41 s, with 30-45 s recommended.

These are observational, vendor-produced and confounded by OpusClip's own defaults, so read them as correlations.

### Cited Findings
- **Dataset and method (TikTok)**: OpusClip analyzed 13.5M TikTok clips processed by its engine. The hook-type breakdown uses 34,635 clips (Jan-Mar 2026 window), the storyline analysis 14,213, and the tonal analysis 10,598, all categorized with OpusClip's "proprietary hook taxonomy". — [OpusClip: Anatomy of a Viral TikTok 2026](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026); [OpusClip: How to Go Viral on TikTok (2026 Data)](https://www.opus.pro/research/how-to-go-viral-tiktok)
- **Top TikTok hook**: the top hook type averaged **6,037 views per clip, ~2x the lowest-ranked hook type**. "Hooks matter more than any other single variable they measured." — [OpusClip: Anatomy of a Viral TikTok 2026](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026). **Conflict**: one search summary names the top TikTok hook "Project & Product Showcase"; another attributes the top spot to "Expertise/Authority/Credibility". Both quote 6,037 views. — [OpusClip Best TikTok Hooks 2026](https://www.opus.pro/blog/tiktok-hooks-that-go-viral-2026) vs [Anatomy of a Viral TikTok](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026). Needs first-hand verification.
- **Hook timing**: the hook window is the first 3 s, and "the algorithm makes an early decision around 1.5 seconds"; the hook should resolve by second 3. — [OpusClip: Anatomy of a Viral TikTok 2026](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026)
- **Storyline**: "Expert Explainer" was the most frequent narrative pattern (2,626 clips), structured as concept, then why it matters, then how to apply it. — [OpusClip: Anatomy of a Viral TikTok 2026](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026)
- **Length**: the viral median is 41 s, "18% shorter than the overall median". The 15-30 s bucket is overrepresented in the viral tier and 60-90 s underrepresented; 30-45 s is recommended. — [OpusClip: Anatomy of a Viral TikTok 2026](https://www.opus.pro/blog/anatomy-of-a-viral-tiktok-2026); [OpusClip: How long should a TikTok be 2026](https://www.opus.pro/blog/how-long-should-a-tiktok-be-2026)
- **Editing features in viral TikTok clips**:

  | Feature | Share of viral clips | Clip count |
  |---|---|---|
  | Captions | 80.2% | 9,787,706 |
  | Caption animation | 78.6% | 9,591,433 |
  | B-roll | 6.0% | 733,762 |
  | Outro | 4.6% | 559,218 |
  | Transitions | 2.4% | — |
  | Music | 1.9% | — |
  | Text intro | 1.0% | 120,208 |

  — [OpusClip: How to Go Viral on TikTok](https://www.opus.pro/research/how-to-go-viral-tiktok); [OpusClip: B-roll & VFX guide TikTok](https://www.opus.pro/research/broll-visual-effects-tiktok)
- **YouTube Shorts**:
  - 8,254 YouTube Shorts clips analyzed. The #1 hook type, Expertise/Authority/Credibility, averages 6,706 views, 5.9x the Outrageous Story Reading hook (1,132 views).
  - Expert Explainer is the most popular storyline. Captions appear in 80% of viral clips.
  - The most common tone combination is serious/professional + thought-provoking. Conversational delivery covers 59% of clips.
  - Source: [OpusClip: How to Go Viral on YouTube Shorts (2026 Data)](https://www.opus.pro/research/how-to-go-viral-youtube-shorts)
- OpusClip also publishes related research pages: YouTube long-form, short-form overall, hooks lists, hashtag lists. — [OpusClip: How to make a viral short-form video](https://www.opus.pro/research/how-to-make-viral-video); [OpusClip: How to go viral on YouTube](https://www.opus.pro/research/how-to-go-viral-youtube)
- No comparable quantitative datasets were found from Vizard, Klap, Submagic, Munch or Quso. Klap only *claims* its model is "trained specifically on viral short-form video data". — [Klap vs Opus](https://klap.app/alternatives/opus-clip)

### Inferences
- **Caveat on the caption numbers**: the ~80% figures are likely inflated by selection bias. These are clips produced by OpusClip, which burns captions in by default, so prevalence among "viral" clips does not show captions *cause* virality. The 9,787,706 / 80.2% figures imply ~12.2M clips in that editing analysis. This is arithmetic inference.
- **Design implication**: score hooks in the first ~1.5-3 s using a hook-type taxonomy (e.g., authority/credibility, product showcase, story), and prefer "expert explainer" structure (concept, then why, then how) when ranking educational content.
- **Length implication**: target 30-45 s for TikTok, and penalize 60-90 s unless content density is high.
- **Why OpusClip can publish this**: its scheduler/auto-post loop plus 13.5M processed clips give it outcome data competitors either lack or don't publish. A new tool that posts on users' behalf (with consent) could build a similar outcome-labelled dataset to calibrate its score.

### Gaps
- The full OpusClip research pages could not be fetched (egress blocked). Exact hook taxonomy categories, view-count definitions (mean vs median; which accounts), whether the virality score itself correlates with views, and the TikTok top-hook conflict could not be verified.
- No independent or academic replication of these findings was found in this search pass.

## Q6. Open-source alternatives and their architectures

### Takeaway
Open-source clippers have converged on one pipeline:
1. yt-dlp ingest
2. faster-whisper / WhisperX (word-level timestamps)
3. an LLM (OpenAI/Gemini/Claude or local Ollama) that proposes and scores 15-60 s moments with a virality rubric
4. scene detection plus MediaPipe/YOLO/OpenCV face tracking (with pyannote diarization) for 9:16 reframing
5. FFmpeg/libass burned-in captions

The most popular repos are AI-Youtube-Shorts-Generator (~5.2k stars), OpenShorts (~5.9k) and Alibaba's FunClip (~6.4k). The repos also contain useful robustness ideas: chunking with overlap, having the LLM return word indices instead of timestamps, and keeping crop paths from interpolating across shot cuts.

### Cited Findings
- **AI-Youtube-Shorts-Generator** (Anil-matcha; ~5.2k stars, 949 forks; MIT). Read first-hand. — [GitHub](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator)
  - Pipeline: yt-dlp, then faster-whisper (local) or a hosted Whisper API, then an LLM "virality framework" that scores candidates 0-100 with explanatory reasoning.
  - Scoring dimensions: "hooks, emotional peaks, opinion bombs, revelation moments, conflict, quotable lines, story peaks, and practical value".
  - Videos over 30 min are split into overlapping 20-min chunks (60 s overlap), with dedup keeping the higher-scored candidate.
  - Cropping: FFmpeg + OpenCV face tracking with motion smoothing.
  - Defaults: 3 clips, 9:16; JSON export of all candidates.
- **OpenShorts** (mutonby; ~5.9k stars, 1.3k forks; MIT self-host or $12/mo cloud; MCP server + API). Read first-hand. — [GitHub](https://github.com/mutonby/openshorts)
  - Transcription and structure: faster-whisper word-level timestamps; PySceneDetect scene boundaries.
  - Moment selection: Gemini 3.1 Flash-Lite picks "3-15 high-potential moments" of 15-60 s, from transcript windows of ~2-3k tokens sent in batches. Any OpenAI-compatible local server (Ollama, vLLM, LM Studio) can replace Gemini.
  - Four layouts, with Gemini auto-selecting per video:
    - TRACK: MediaPipe + YOLOv8
    - GENERAL: blurred background
    - SPLIT: two speakers stacked, captions on the seam
    - SCREENCAST
  - Extras: AI hook text overlays, Gemini-generated FFmpeg filter effects, ElevenLabs dubbing.
  - Stack: FastAPI/React.
- **AutoClip** (artbyjazi; ~159 stars; MIT; pre-1.0 "awaiting golden-set validation"). Read first-hand. — [GitHub](https://github.com/artbyjazi/autoclip)
  - Staged pipeline: ingest, prepare, transcribe, highlights, reframe, captions, export. Artifacts are saved per stage so jobs can resume.
  - Key design choice: "Highlight detection returns word indices, not timestamps", because models copy visible numbers reliably but do arithmetic poorly.
  - LLM options: local Ollama (e.g., llama3.1:8b) or Anthropic/OpenAI/Gemini/OpenRouter/Groq/DeepSeek. Only text is sent.
  - Reframing: MediaPipe + optional WhisperX diarization; "Crop paths never interpolate across a cut" (shot detection first).
  - Output: 4 libass caption styles (bold_pop, karaoke_fill, clean_lower, boxed); audio normalized to −14 LUFS.
- **ClipsAI** (Python library; ~545 stars; MIT). Read first-hand. — [GitHub](https://github.com/ClipsAI/clipsai)
  - Built for "audio-centric, narrative-based videos such as podcasts, interviews, speeches, and sermons".
  - Uses WhisperX word-level transcripts to segment clips, and pyannote speaker diarization to resize 16:9 to 9:16 focused on the current speaker. Requires a Hugging Face token.
- **FunClip** (Alibaba Tongyi Speech Lab / ModelScope; ~6.4k stars; v2.2.1 Sept 2026). Read first-hand. — [GitHub](https://github.com/modelscope/FunClip)
  - ASR: Paraformer-Large (plus SenseVoice with emotion/audio-event detection, and multilingual Fun-ASR-Nano).
  - Speaker ID: CAM++, so you can clip one speaker's segments.
  - LLM clipping: custom prompts via OpenAI-compatible routing, plus TwelveLabs Pegasus for visual+audio video understanding.
  - Output: SRT generation; local Gradio UI.
- **opensource-clipping** ("Ultimate AI Auto-Clipper"): Whisper + Gemini + MediaPipe + pyannote; face tracking, kinetic karaoke subtitles, contextual B-roll, AI voice-overs, auto-uploaders to YouTube/Facebook. — [GitHub (TaimourKhan2132)](https://github.com/TaimourKhan2132/opensource-clipping); [fork (NaufalRizqullah)](https://github.com/NaufalRizqullah/opensource-clipping)
- **ai-video-clipper** (PriyeshPandey2000), issue #102. Read first-hand. — [GitHub issue #102](https://github.com/PriyeshPandey2000/ai-video-clipper/issues/102)
  - Proposes replacing hardcoded 15-90 s bounds and a 10-clip cap with `minMs`/`maxMs`/`maxClips`/`profileOverride`/`steer` settings.
  - Pipeline: `selectClips()` then `refineClipBoundaries()`, with configuration fingerprinting for reproducibility.
  - Design choice: free-text steering *boosts* matching clips rather than rejecting non-matching ones.
  - It also surveys competitors: OpusClip exposes genre, length range and topic keywords; Vizard exposes length multi-select and topic/prompt steering.
- The GitHub "auto-clip" topic lists further projects. — [GitHub topic: auto-clip](https://github.com/topics/auto-clip)

### Inferences
- **Reference architecture** for a new tool, assembled from the strongest open-source ideas:
  1. faster-whisper/WhisperX word timestamps plus diarization
  2. PySceneDetect shots
  3. Windowed LLM candidate proposal: return word indices; overlapping chunks; dedupe
  4. Rubric scoring with reasons: OpusClip-style Hook/Flow/Value/Trend, extended with AI-Shorts-Generator's "opinion bomb / revelation / quotable" categories
  5. Boundary refinement to sentence/turn edges
  6. Layout selection: track / split / screencast / blurred-fill
  7. Shot-aware smoothed crop paths
  8. libass caption templates
  9. Loudness normalization
- **What open source still lacks** relative to commercial tools: outcome-calibrated scoring, multimodal non-dialogue detection at scale (FunClip's Pegasus hook is the exception), scheduling/analytics feedback loops, and polished caption/B-roll templates.

### Gaps
- ClipsAI's exact segmentation algorithm (e.g., TextTiling over embeddings) was not stated on the fetched README, so it is unverified.
- No benchmark comparing open-source clip-selection quality with commercial tools was found.
- Star counts are point-in-time readings from 2026-10-02.
