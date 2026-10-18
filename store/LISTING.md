# Chrome Web Store listing: undertext

Everything to paste into the Chrome Web Store developer dashboard for the
extension in `extension/` (manifest version 0.4.1). Text inside code blocks is
meant to be copied as-is. The dashboard does not render Markdown, so the
detailed description is plain text.

---

## 1. Name

```
undertext
```

Taken from `name` in `manifest.json`. The dashboard shows the manifest name; it
is not edited in the listing.

## 2. Short description

The store's summary line is the manifest `description` field, which Chrome
limits to 132 characters. It is not typed into the dashboard: to change it,
change `manifest.json` and upload a new package.

Current text (keep it):

```
Shows when a web page hides instructions aimed at AI, or links to an AI assistant with a poisoned prompt. Runs locally.
```

Length: **119 characters** (limit 132).

## 3. Detailed description

Paste into **Store listing > Product details > Description**.

```
undertext shows you when a web page hides instructions meant for AI assistants.

THE PROBLEM

AI assistants read web pages for you, and some sites now write for the AI instead of for you.

- Poisoned "Summarize with AI" buttons. The link opens ChatGPT, Copilot, Claude, Perplexity, Gemini or another assistant with a prompt already filled in. The visible part asks for a summary. The rest tells the assistant to remember the site as a trusted source, so it gets recommended in your future chats. Microsoft's security researchers call this AI Recommendation Poisoning.
- Hidden page text. Text you can't see (hidden by styles, white on white, in comments, alt text, meta tags or structured data, or in invisible Unicode characters) that tells an AI what to say or do when it reads the page.

WHAT IT DOES

undertext checks each page you visit, as it is actually rendered, so it also sees text hidden by stylesheets or added by scripts after the page loads.

- A red ! on the toolbar icon means the page hides instructions aimed at AI, or has an AI-assistant link with a poisoned prompt.
- A yellow ? means something is worth a look.
- No badge means nothing was found.

Click the icon to see the exact text, where it was hidden (for example "display:none", an HTML comment, or an image's alt text), and which rules it matched. For visible text and links, a Show button scrolls to it on the page.

WHAT IT CAN'T DO

- It uses keyword rules only. They catch the known "Summarize with AI" templates and show you the hidden text, but they miss many new wordings, and anyone who reads the open rules can write around them. On new attack wordings written after the rules were frozen, the rules alone caught 4 of 22. The optional AI check in the undertext command-line tool, which the extension does not include, caught 19 of 22.
- No badge does not prove a page is safe. Treat undertext as a first filter and a way to see what is hidden, not as a guarantee.
- It can raise false alarms, for example on articles that quote an attack.
- Chrome does not let extensions run on some pages, such as the Chrome Web Store and chrome:// pages.

PRIVACY

undertext runs entirely in your browser. It reads the page you are on to run the check, and that's it: it makes no network requests, stores nothing, and has no account, analytics or tracking. It never opens the links it checks.

THE RESEARCH BEHIND IT

The rules were tested on two random scans of 10,000 websites each, with every flag checked by hand. Of 12,726 reachable sites:

- 4 had a real memory-poisoning prompt in an AI-assistant link.
- Of the sites that put a prompt in an AI link, about 1 in 7 used it to plant themselves in the assistant's memory.
- 0 had hidden page text giving AI harmful orders.

So hidden instructions are rare on ordinary sites today. undertext is there for the cases that do happen, and to show you exactly what a page is telling your AI.

OPEN SOURCE

The code, the rules and the full evaluation, including the misses, are public:
https://github.com/Wido777/undertext

Website and in-browser link checker:
https://wido777.github.io/undertext/
```

Length: 3,125 characters (well under any practical limit; the docs set no
explicit maximum, only that the description must follow the keyword spam
policy).

Source check: every number above is from the README (two samples of 10,000,
12,726 reachable, 4 poisoning prompts, about 1 in 7 prompt links, 0 malicious
hidden text; on the fresh unseen set, rules alone 4 of 22 and rules plus AI
review 19 of 22, from the "How much it helps" table). The reworded unseen set
(rules alone 5 of 36) is in the same table if a second example is wanted. No
scanned website is named.

## 4. Category and language

- **Category:** Privacy & Security (in the current dashboard it sits under the
  "Make Chrome Yours" group). It protects what your AI assistant is told while
  you browse; it is a user safety tool, not a tool for developers.
- **Language:** English.

## 5. Privacy practices tab

### Single purpose

```
undertext checks the page you are viewing for instructions aimed at AI assistants, hidden in the page or in prefilled AI-assistant links, and shows the result on its toolbar icon.
```

### Permission justifications

The dashboard asks for one justification per permission it finds in the
package. The manifest requests no permissions (no `permissions`,
`host_permissions` or `optional_permissions` key). Its only access is a
content script on `http://*/*` and `https://*/*`, which the store treats as
host access, so that is the only justification needed.

**Host access (content script on all http and https pages)**

```
undertext's single purpose is to warn you when the page you are viewing hides instructions for AI. To do that, its content script reads each page you open, as rendered, and checks the text and the AI-assistant links in it with rules bundled in the extension. The check runs locally in the page: no page content is sent anywhere or stored, and the extension makes no network requests. It must run on every page because hidden instructions can be on any site, and the toolbar badge has to appear without you clicking first. It runs only on http and https pages, not on file pages.
```

### Remote code

Select **"No, I am not using remote code."**

```
All JavaScript is included in the package (content.js, popup.js, background.js and the rule engine in lib/). The extension loads no external scripts, uses no eval or new Function, and makes no network requests.
```

### Data usage

**Read this before ticking.** The Chrome docs say extensions must disclose how
they *handle* user data "even when data is processed or stored locally on a
user's device and is not transmitted to external servers or third parties"
(User Data FAQ, question 3), and list "capturing data from a web page" as an
example of handling. undertext reads the content of every page to scan it,
even though nothing leaves the browser.

- **Recommended (safer for review):** tick **Website content** only, and no
  other data type. This matches the docs' wording and the privacy policy,
  which says the extension reads page content locally. It does not stop you
  from saying in the description that nothing is collected or sent.
- **Alternative:** tick nothing ("does not collect any of the listed data
  types"). This is defensible because nothing is collected, sent or stored,
  but a reviewer reading the FAQ strictly could flag it.

Do not tick Personally identifiable information, Health information,
Financial and payment information, Authentication information, Personal
communications, Location, Web history, User activity or any other type.

Tick all three certifications:

- [x] I do not sell or transfer user data to third parties, outside of the approved use cases.
- [x] I do not use or transfer user data for purposes that are unrelated to my item's single purpose.
- [x] I do not use or transfer user data to determine creditworthiness or for lending purposes.

### Privacy policy URL

```
https://wido777.github.io/undertext/privacy.html
```

Make sure the page is live (pushed to GitHub Pages) before you submit.

## 6. Graphic assets (from `store/`)

| Dashboard field | File | Size | Required |
|---|---|---|---|
| Store icon | `store/icon-128.png` | 128x128 PNG | Yes |
| Screenshots (1 to 5) | `store/screenshot-1-hidden-instructions.png`, `-2-poisoned-link.png`, `-3-clean-page.png`, `-4-what-it-detects.png` | 1280x800 | At least 1 |
| Small promo tile | `store/promo-small-440x280.png` | 440x280 | Yes |
| Marquee promo tile | none | 1400x560 | No |
| YouTube video | none | | No (optional; leave empty) |

Optional fields: Homepage URL `https://wido777.github.io/undertext/`, Support
URL `https://github.com/Wido777/undertext/issues`.

## 7. Upload checklist

1. Register a developer account at the Chrome Web Store developer dashboard:
   accept the developer agreement and pay the one-time $5 registration fee.
2. Build the package: `python scripts/build_extension.py --zip` writes
   `dist/undertext-extension-0.4.1-chrome.zip` (Chrome-only manifest, no
   `test/` folder). Upload that file: `dist/undertext-extension-0.4.1-chrome.zip`.
3. In the dashboard, click **New item** and upload the Chrome zip.
4. **Store listing:** paste the description (section 3), pick category and
   language (section 4), upload the icon, screenshots and small promo tile
   (section 6), add homepage and support URLs.
5. **Privacy practices:** single purpose, the host access justification,
   remote code, data usage and certifications, privacy policy URL (section 5).
6. **Distribution:** visibility Public (or Unlisted for a soft launch), all
   regions, free.
7. Click **Submit for review**. Per the docs, most reviews finish "within a
   few days, but it can take up to a few weeks". Broad host permissions (a
   content script on all sites) and a new developer account both make a
   closer review more likely.

## Sources

- Store listing fields and images: https://developer.chrome.com/docs/webstore/cws-dashboard-listing
- Image sizes and formats: https://developer.chrome.com/docs/webstore/images
- Privacy practices tab: https://developer.chrome.com/docs/webstore/cws-dashboard-privacy
- User data FAQ (local processing must be disclosed): https://developer.chrome.com/docs/webstore/program-policies/user-data-faq
- Manifest `description` limit (132 characters): https://developer.chrome.com/docs/extensions/reference/manifest/description
- Review process and times: https://developer.chrome.com/docs/webstore/review-process
- Developer registration: https://developer.chrome.com/docs/webstore/register
- $5 registration fee: https://blog.chromium.org/2020/03/new-developer-dashboard-and.html
