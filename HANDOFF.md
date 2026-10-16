# Glory App — Handoff Notes

Glory App by Ben Lim Global. A mobile web app (works on phones, tablets and computers, and installs to the home screen), hosted free on GitHub Pages.

- **Live link:** https://navarroraquel602-max.github.io/ben-lim-app/
- **Code:** https://github.com/navarroraquel602-max/ben-lim-app (currently under the developer's account; to be moved to the ministry, see below)

## How it is built

No framework, no build tools to install, and no paid services.

| File | What it is |
|---|---|
| `index.src.html` | **The file you edit.** All pages, styles, text in every language, and app logic. |
| `build.py` | Turns `index.src.html` into `index.html` with the images built in. Run `python3 build.py`. |
| `index.html` | What visitors load. Generated, so never edit it by hand. |
| `sw.js` | Lets the app work offline. Change the cache name (`benlim-v61` → `benlim-v62`) each time you publish. |
| `manifest.json` | App name and icon for "Add to Home Screen". |
| `privacy.html` | Privacy policy (**draft**: the ministry must review it). |
| `logo.png`, `icon-*.png`, `oils/`, `books/` | Images. `photos/` and `about.jpg` are no longer shown (the bio is intentionally left out of the app). |

There are **no environment variables, API keys or passwords** in the project.

## Publishing a change

1. Edit `index.src.html`.
2. Run `python3 build.py`.
3. Bump the cache name in `sw.js`.
4. Commit and push to `main`. Or upload the changed files at github.com → Add file → Upload files.
5. GitHub Pages republishes within about a minute.

## Content that updates itself from benlimglobal.com

The app reads the ministry's WordPress site, so **updating the website updates the app**:

| In the app | Comes from (WordPress) |
|---|---|
| Missions & Crusades trips and photos | Shop products in the **Missions** category (`product_cat` 91) |
| Events | The events plugin (Events → add or edit an event) |
| Prophecy Library | Blog posts |

If the site can't be reached, the app shows the last copy saved on the phone. Website text appears in English, and the app labels it "(in English)" for other languages.

## Text and languages

All on-screen text lives in the `T`, `T2` and `T3` tables in `index.src.html`. The languages are `en`, `es`, `my` (Burmese), `zh` and `ru`. Any text missing in a language falls back to English. **Burmese was machine-written and needs review by a native speaker.**

## Things that need the ministry

| Item | Who | Notes |
|---|---|---|
| Activate the crusade application | Whoever reads missions@benlimglobal.com | FormSubmit sends a one-time "Activate form" email after the first submission. Until someone clicks it, applicants are sent to their own email app instead. |
| Square links for oils and prayer shawl | Whoever manages the ministry's Square account | One payment link per item and size. Then put the links on the shop buttons. The Power of Honor book already uses `square.link/u/qzlQBPJM`. |
| Crowd and crusade photos/videos | Ministry | For the welcome area and Missions & Crusades. |
| Weekly prophecy word | Ministry | Easiest: publish it as a blog post on benlimglobal.com, and the app picks it up. Or fill in `WORD` / `PROPHECY_EXTRA` in `index.src.html`. |
| Links for Ben Lim Asia and Ben Lim Myanmar | Ministry | Only benlimfuego.com was found. |
| Review the privacy policy | Ministry (ideally its lawyer) | `privacy.html`. Fill in the effective date and how long applications are kept. |

## Moving the project to the ministry

Nothing has been transferred yet. **Do not transfer without the developer's approval.**

1. The ministry creates a GitHub account or organization (free).
2. In this repo: Settings → General → Danger Zone → **Transfer ownership** to the ministry account.
3. In the new repo: Settings → Pages → Deploy from branch → `main` / root. The link changes to `https://<ministry-account>.github.io/ben-lim-app/`. A custom domain (for example `app.benlimglobal.com`) can be added there.
4. Ask the web host to allow the new address to read the website data. The WordPress site currently allows the GitHub Pages address; a new address or domain should be checked.
5. Revoke the developer's access token (GitHub → Settings → Developer settings → Fine-grained tokens).

## App Store and Google Play plan

**Approach:** wrap this app with **Capacitor** (free, open source). It packages the existing app as real iOS and Android apps with little rework.

**Accounts and costs**

| Item | Cost |
|---|---|
| Apple Developer Program (organization) | $99 / year. Needs a **D-U-N-S number** (free) and the ministry's legal details. |
| Google Play developer account | $25 one-time |
| A Mac with Xcode | Needed to build the iPhone app |
| Push notifications (optional) | Free with Firebase Cloud Messaging |
| Partner sign-in / members content (later) | Needs a backend such as Supabase or Firebase: free tier to about $25 / month |

**Before submitting**

- **Approved privacy policy** at a public link (`privacy.html`).
- **App Store privacy answers:** the crusade application collects contact details, date of birth and **health information** (allergies, medical/emotional conditions). This must be declared. Consider whether the app needs to ask for all of it.
- **Not "just a website":** Apple rejects apps that are only a wrapped website. Plan at least push notifications for Prophecy Now (also requested by Dr. Ben) and offline support (already built).
- **In-app purchase rule:** if paying for a partner level unlocks content *inside* the app, Apple may require its own payment system (15–30% fee). Giving and donations through Tithe.ly need to follow Apple's rules for nonprofits. Settle this before building partner sign-in.
- **Store materials:** app icon at store sizes, screenshots, description, support email, and an age rating.
- **App name:** "Glory App" had no exact match in a US store search (Oct 2026), but Apple checks worldwide. Reserve it in App Store Connect as soon as the ministry's account exists. "Prophecy Now" is taken by another ministry. Also check for trademarks.

## Known limits

- The website does not share event *dates* with apps, so event cards show each event's own description (which normally names the date and city), newest posted first.
- Partner sign-in is a preview only. The button is disabled and no accounts exist.
- Booking, oil, shawl and call requests open the visitor's email app. Switching them to FormSubmit too is possible once the missions form is activated and working.
