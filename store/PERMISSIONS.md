# Chrome Web Store: privacy practices answers

Text for the "Privacy practices" tab of the developer dashboard. Upload
`dist/promptlink-extension-<version>-chrome.zip` (built with
`python scripts/build_extension.py --zip`).

## Single purpose

promptlink shows you when the web page you are on hides instructions aimed at
AI assistants, such as hidden text that tells an AI what to say, or a
"Summarize with AI" link whose prefilled prompt tries to plant a brand in the
assistant's memory. It marks the toolbar icon with a badge and lists what it
found, and where, when you click it.

## Permission justifications

The manifest requests **no permissions**: there is no `permissions`,
`host_permissions` or `optional_permissions` key. The only access the dashboard
asks about is the content script, which the store treats as host access.

**Content script on http://\*/\* and https://\*/\* (host access)**

```
To show the warning badge before you ask an AI about a page, promptlink has to read each page you visit. The content script checks the page's text, hidden elements, comments, attributes, meta tags and AI-assistant links inside your browser and sends only the verdict (safe, suspicious or dangerous) to the extension's own background script to set the badge. No page content, URL or browsing history is stored, logged or sent anywhere. It runs only on normal web pages (http and https), not on file pages or other schemes.
```

The popup needs no permission either: it finds the current tab with
`chrome.tabs.query` (tab ids are available without the `tabs` permission) and
asks promptlink's own content script for the result with
`chrome.tabs.sendMessage`. There is no `activeTab`, `tabs`, `storage`,
`scripting`, `cookies` or `webRequest`, and the extension makes no network
requests.

## Are you using remote code?

No. All JavaScript is included in the package (`background.js`, `content.js`,
`popup.js` and the detection engine in `lib/`). Nothing is downloaded or
loaded from a server, and the extension does not use `eval`, `new Function` or
remote scripts. The detection rules are a static file (`lib/rules.js`) shipped
in the package; regular expressions are built from those bundled rules with
`new RegExp`, which is data, not code.

## Data usage

promptlink does not collect, store or send any user data. Page content is read
only in memory, on your device, to decide whether to show the badge, and is
discarded when you leave the page.

Chrome's User Data FAQ says handling must be disclosed even when data is only
processed locally, and gives "capturing data from a web page" as an example.
So the recommendation (same as `store/LISTING.md`, section 5) is:

- **Tick "Website content" only.** It matches the FAQ and the privacy policy,
  which says the extension reads page content locally.
- Do not tick any other type (personally identifiable information, health,
  financial, authentication, personal communications, location, web history,
  user activity).
- The alternative, ticking nothing, is defensible because nothing is collected
  or sent, but a strict reviewer could flag it.

Certifications to tick:

- I do not sell or transfer user data to third parties, outside of the approved use cases.
- I do not use or transfer user data for purposes that are unrelated to my item's single purpose.
- I do not use or transfer user data to determine creditworthiness or for lending purposes.

Privacy policy URL: https://wido777.github.io/promptlink/privacy.html
(`docs/privacy.html`, which describes the same permissions and says no data is
collected).
