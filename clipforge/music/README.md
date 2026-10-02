# Licensed music library

clipforge adds **no music by default**. Adding none is the safest choice for
copyright, and on YouTube a Short with no music keeps 100% of its
creator-pool share (1/2 with one track).

To use background music, put the audio files in a folder with a
`licenses.json` beside them and pass `--music-dir that/folder`. Only tracks
that are explicitly licensed for commercial use on the target platform are
used. A file with no licence entry is treated as not cleared.

```json
[
  {
    "file": "upbeat-loop.mp3",
    "title": "Upbeat Loop",
    "source": "Epidemic Sound",
    "license": "Epidemic Sound Personal subscription",
    "license_url": "https://www.epidemicsound.com/licensing/",
    "commercial_use": true,
    "platforms": ["tiktok", "shorts", "reels"],
    "attribution": null
  }
]
```

Things to check before adding a track:

- **Subscription libraries** such as Epidemic Sound and Artlist clear claims by safelisting *your channels*. Register every channel you post to, and keep the subscription active on the day you publish.
- **Free libraries:**
  - Uppbeat's free plan, Pixabay, and CC BY tracks often require a credit line. Put that text in `attribution` and clipforge adds it to the post caption.
  - Keep the licence certificate or download page. "Royalty-free" tracks still get mistakenly registered in Content ID, and the certificate is how you dispute that.
- **CC BY-NC tracks** don't cover monetised or brand posts.
- **YouTube Audio Library tracks** should be treated as YouTube-only: list only `"shorts"` in their platforms.
- **In-app libraries do not work here.** That means TikTok's Commercial Music Library and sounds, Meta Sound Collection, and the YouTube Shorts library. They are licensed only when added inside each app, so add those sounds in the app when you post.
