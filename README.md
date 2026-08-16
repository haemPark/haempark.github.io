# Personal website

A single-file personal site for job hunting. No build step, no dependencies, no framework —
just `index.html`. GitHub Pages serves it as-is.

```
index.html          the entire site (HTML + CSS + JS in one file)
assets/photo.jpg    your headshot        ← add this
assets/resume.pdf   your résumé          ← add this
```

---

## 1. Put it on GitHub Pages

You have a GitHub account but no repo yet, so start here.

**Create the repo.** Go to [github.com/new](https://github.com/new) and name it exactly:

```
YOUR-USERNAME.github.io
```

Replace `YOUR-USERNAME` with your GitHub username, character for character. This exact name is
what makes GitHub serve it at `https://YOUR-USERNAME.github.io` — the root of your namespace,
the cleanest possible URL. Set it to **Public**. Don't add a README (you have one).

**Upload the files.** Easiest path, no terminal:

1. On the empty repo page, click **uploading an existing file**.
2. Drag in `index.html`, `README.md`, and the `assets` folder.
3. Click **Commit changes**.

Or with git, if you'd rather:

```bash
cd site
git init
git add .
git commit -m "Personal website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-USERNAME.github.io.git
git push -u origin main
```

**Turn on Pages.** Repo → **Settings** → **Pages** → under *Source* pick **Deploy from a branch**,
branch `main`, folder `/ (root)` → **Save**.

Wait 1–2 minutes, then open `https://YOUR-USERNAME.github.io`. Every push after this redeploys
automatically in about 30 seconds. If you see a 404, give it another minute — the first build is
the slow one.

---

## 2. Fill in your content

Open `index.html` in any text editor and search for `EDIT #`. There are nine marked blocks:

| # | Block | What to change |
|---|-------|----------------|
| 1 | Title & SEO | Your name in `<title>`, the description, and every `YOUR-USERNAME` |
| 2 | Hero | Name, role line, location, the 2–3 sentence pitch, and all five link buttons |
| 3 | About | Two paragraphs — what you research, and what you want next |
| 4 | News | Five recent items, or delete the whole section |
| 5 | Research | Your papers, newest first |
| 6 | Projects | 3–6 cards, each with a working link |
| 7 | Experience | Roles, education, skills |
| 8 | Contact | Your email (appears twice — hero button and contact box) |
| 9 | Structured data | The JSON block that helps Google show a rich result for your name |

Also global-replace these three strings everywhere:

- `YOUR-USERNAME` → your GitHub username
- `you@example.com` → your email
- `Haemin Lee` → your full name as you want it printed

Then drop `photo.jpg` and `resume.pdf` into `assets/`. If you skip the photo the layout closes up
cleanly on its own, so it's safe to leave out until you have one you like.

---

## 3. Notes on the details

**Theme.** Follows the visitor's OS light/dark setting; the button in the nav flips it for the
current visit. It deliberately doesn't remember the choice between visits. If you want it to,
add this inside the theme function in `index.html`:

```js
localStorage.setItem('theme', dark ? 'dark' : 'light');   // in apply()
var saved = localStorage.getItem('theme');                 // read it on load
```

**Colors.** One line changes the whole site — `--accent` at the top of the `<style>` block
(and `--accent` again under `html[data-theme="dark"]` for the dark variant).

**Custom domain.** If you buy `yourname.com`: add a file named `CNAME` containing just
`yourname.com`, point an `ALIAS`/`ANAME` record at `YOUR-USERNAME.github.io` in your registrar's
DNS, then enable **Enforce HTTPS** in Settings → Pages.

**Printing.** `Cmd/Ctrl-P` renders a clean one-pager with the nav stripped out.

---

## 4. Things worth doing once it's live

- Put the URL in your GitHub profile bio, your LinkedIn contact section, and your résumé header.
- Search your own name in an incognito window a week later to see where the site ranks.
- Keep the News section current. A page whose last update was two years ago reads worse than no
  News section at all — that's why it's safe to delete.
