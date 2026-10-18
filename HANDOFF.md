# Glory App — Handoff Notes

Glory App by Ben Lim Global. A mobile web app (works on phones, tablets and computers, and installs to the home screen), hosted free on GitHub Pages.

- **Live link:** https://navarroraquel602-max.github.io/ben-lim-app/
- **Code:** https://github.com/navarroraquel602-max/ben-lim-app (currently under the developer's account; to be moved to the ministry, see below)

## How it is built

No framework, no build tools to install, and no paid services.

| File | What it is |
|---|---|
| `index.src.html` | **The file you edit.** All pages, styles, text in every language, and app logic. |
| `build.py` | Turns `index.src.html` into `index.html` (Black & Gold edition, images built in) **and** `silver.html` (Black, Silver & White edition). Run `python3 build.py`. |
| `theme_silver.py` | Recolors every gold/fire color to silver for `silver.html`; flags, social-network colors and product photos stay true, crowd photos turn black and white. `manifest-silver.json` lets the silver edition be added to a home screen on its own. |
| `index.html` | What visitors load. Generated, so never edit it by hand. |
| `sw.js` | Lets the app work offline. Change the cache name (`benlim-v61` → `benlim-v62`) each time you publish. |
| `manifest.json` | App name and icon for "Add to Home Screen". |
| `privacy.html` | Privacy policy (**draft**: the ministry must review it). |
| `update_shop.py` / `shop.json` | The Shop's "Music & More" shelf: mirrors the benlimglobal.com store (mission trips and free events skipped). Run `python3 update_shop.py` when products or prices change on the website. |
| `update_events.py` / `events.json` | Collects event dates from the website so past events are hidden (see Known limits). |
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
| Events (upcoming only, with dates) | The events plugin (Events → add or edit an event), plus `events.json` (see below) |
| Prophecy Library | Blog posts |

If the site can't be reached, the app shows the last copy saved on the phone. Website text appears in English, and the app labels it "(in English)" for other languages.

## Text and languages

- **Interface text:** the `T`, `T2`, `T3` tables in `index.src.html`.
- **Text written in the page itself** (forms, legal agreements, course names): `i18n/en.json` plus `es/zh/ru/my.json`, matched by position. To add a line, add it to every file at the same spot.
- **Website content** (events, mission trips, Prophecy Library titles and previews): `i18n/content.json`, keyed by the item's web address. New items posted on the website show in English, labelled "(in English)", until a translation is added there. The full text of a prophetic word opens through Google Translate in the reader's language.
- **Legal note:** the crusade application's agreements are translated so applicants can understand them; the ministry should confirm whether the English version is the binding one.

### Interface tables

All on-screen text lives in the `T`, `T2` and `T3` tables in `index.src.html`. The languages are `en`, `es`, `my` (Burmese), `zh` and `ru`. Any text missing in a language falls back to English. **Burmese was machine-written and needs review by a native speaker.**

## Things that need the ministry

| Item | Who | Notes |
|---|---|---|
| Activate the crusade application | Whoever reads missions@benlimglobal.com | FormSubmit sends a one-time "Activate form" email after the first submission. Until someone clicks it, applicants are sent to their own email app instead. |
| Switch on oil and prayer shawl order requests | Ministry approval, then the developer | See "Merchandise order requests" below. |
| More mission videos | Ministry | Videos come from the ministry's YouTube channel: add a video's YouTube id, place and titles to `MISSION_VIDEOS` in `index.src.html`. |
| Weekly prophecy word | Ministry | Easiest: publish it as a blog post on benlimglobal.com, and the app picks it up. Or fill in `WORD` / `PROPHECY_EXTRA` in `index.src.html`. |
| Review the privacy policy | Ministry (ideally its lawyer) | `privacy.html`. Fill in the effective date and how long applications are kept. |

## Merchandise order requests (Square invoices)

The Shop's oils and prayer shawl use an **invoice request**, not a checkout:
1. The customer picks items and quantities.
2. They tap **Request Invoice** and fill in the order sheet.
3. The ministry receives an email.
4. Staff create and send a **Square invoice** from the ministry's own Square account.
5. The customer pays Square directly.

The app never handles payments or card details. Payment confirmation, fulfillment, shipping, refunds and customer service stay with the ministry.

**It is switched off until the ministry approves the order inbox.** While off, the order sheet says so and only offers "Copy order details". Nothing is sent.

To switch it on:
1. The ministry approves the inbox. The proposed inbox from prior correspondence is `benlimgloballlc@gmail.com`.
2. In `index.src.html`, set `ORDER_ENDPOINT = "https://formsubmit.co/ajax/<approved inbox>"`.
3. Run `python3 build.py`, bump `sw.js`, and publish.
4. Submit one clearly labelled test order. FormSubmit emails the inbox an **Activate** link, and someone must click it. Then submit a second test and confirm it arrives.
5. *(Optional)* FormSubmit can replace the visible address with a random alias. After activation, use the alias in `ORDER_ENDPOINT`.

**What it does:**
- **No secret keys.** FormSubmit needs no password or API key, so nothing secret is in the app.
- **Spam:** a hidden trap field, plus a minimum fill time.
- **Duplicates:** each order has a reference (`MO-…`) shown to the customer and in the email subject. The Send button locks while sending, and a retry after a failure reuses the same reference.
- **Confirmation:** the customer sees it only after FormSubmit confirms delivery.
- **Privacy:** nothing about the order is stored on the phone, and nothing goes in a web address.

**Prices (confirmed by the ministry, Oct 2026):** Oil of Grace and Bridegroom Oil, Small $15 / Medium $30 / Large $45; Prayer Shawl $50 (photo: `media/prayer-shawl.jpg`). Oil sizes in ounces are not needed. Prices are in `OIL_SIZES` and `SHAWL` in `index.src.html`.

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

- The website's data feed does not include event *dates*. So `update_events.py` reads every event page and saves the upcoming events with their dates to `events.json`. The app hides events once they end (checked every day, automatically) and lists the rest soonest first.
  - **When the ministry adds a new event**, it appears in the app right away from the live feed, listed first but without a date, until someone runs `python3 update_events.py` and publishes `events.json`. Doing that every week or two keeps dates on everything. It takes about 8 minutes because it reads pages slowly so the site doesn't block it.
  - This could run automatically every day with a free GitHub Action. That needs the access token to also have the **Workflows** permission.
- Partner sign-in is a preview only. The button is disabled and no accounts exist.
- Booking, oil, shawl and call requests open the visitor's email app. Switching them to FormSubmit too is possible once the missions form is activated and working.
