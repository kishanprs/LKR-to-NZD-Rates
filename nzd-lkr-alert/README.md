# NZD → LKR Rate Alert

Watches the live NZD → LKR exchange rate and sends you a free WhatsApp
(or Telegram) message when it crosses 190, using GitHub Actions as the
"always-on" runner and [CallMeBot](https://www.callmebot.com/) as the
free messaging bridge. Includes an optional live-rate dashboard page.

## 1. Create the repo

1. On GitHub, create a new **public** repository (Actions' free scheduled
   runs require a public repo, or a private repo on a paid plan).
2. Upload these files, keeping the folder structure:
   ```
   .github/workflows/check-rate.yml
   scripts/check_rate.py
   state.json
   index.html   (optional dashboard)
   README.md
   ```

## 2. Get a free CallMeBot key (pick WhatsApp OR Telegram)

### Option A — WhatsApp
1. Save **+34 644 20 47 56** as a contact on your phone.
2. From WhatsApp, message that contact: `I allow callmebot to send me messages`
3. Within ~2 minutes you'll get a reply with your **API key**.
   > Note: CallMeBot's WhatsApp bot occasionally shows "bot is full, check
   > back in a few days" for new sign-ups since it's a free community
   > project. If that happens, use the Telegram option below instead — it
   > doesn't have this limit.

### Option B — Telegram (no waitlist)
1. Open Telegram and message **@CallMeBot_txtbot**: `/start`
2. Follow its reply — it will confirm your username is ready to receive messages.

## 3. Add your credentials as GitHub Secrets

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

- If using WhatsApp:
  - `CALLMEBOT_PHONE` = `+64211618855`
  - `CALLMEBOT_APIKEY` = *(the key CallMeBot sent you)*
- If using Telegram instead:
  - `TELEGRAM_USERNAME` = *(your Telegram username)*

You only need to set one method, not both.

## 4. Turn on Actions

Go to the **Actions** tab of your repo → enable workflows if prompted.
The `Check NZD to LKR rate` workflow will now run automatically every
30 minutes. You can also trigger it manually anytime via **Actions →
Check NZD to LKR rate → Run workflow**.

## 5. (Optional) View the dashboard

Enable **GitHub Pages** (Settings → Pages → deploy from `main` branch,
root folder) to get a live-updating rate page at
`https://<your-username>.github.io/<repo-name>/`.

## How it works

- `scripts/check_rate.py` fetches the live rate from the free
  [open.er-api.com](https://open.er-api.com) API (no key needed).
- If the rate is ≥ 198 and you haven't already been alerted for this
  crossing, it sends you a message via CallMeBot and records that in
  `state.json` (committed back to the repo) so you're not spammed every
  30 minutes.
- If the rate later drops back below 198, the flag resets so the next
  crossing above 198 alerts you again.

## Notes

- To change the threshold, edit `THRESHOLD: "198"` in
  `.github/workflows/check-rate.yml` (and the matching `THRESHOLD` value
  near the top of the `<script>` in `index.html` if you use the dashboard).
- To change how often it checks, edit the cron schedule in the same file
  (`*/30 * * * *` = every 30 minutes). GitHub may throttle very frequent
  schedules on free accounts, and scheduled runs can be delayed further
  during periods of high GitHub Actions load.
- CallMeBot is a free community project intended for personal, low-volume
  use — it's not a guaranteed enterprise-grade SMS/WhatsApp service.
