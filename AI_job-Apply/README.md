# Smart Naukri Job Application Bot
### For: Ankit Mistri — Senior Test Automation Engineer / SDET

---

## How it works (3-phase approach)

```
Phase 1 — SCAN        Phase 2 — YOU APPROVE        Phase 3 — APPLY
─────────────────     ──────────────────────────    ──────────────────
Search 5 keywords  →  See scored job list       →  Bot applies only
Score each job        Pick: all / top10 / 1,3,5    to jobs you chose
Filter by threshold   or skip                       with human delays
Deduplicate                                         Saves full log CSV
```

The bot **never applies without your explicit approval.** You see the list first.

---

## Setup (one-time, ~5 minutes)

### Step 1 — Install Python
Download from https://python.org (3.10 or higher)

### Step 2 — Install dependencies
Open Terminal / Command Prompt and run:
```bash
pip install selenium webdriver-manager colorama pandas
```

### Step 3 — Configure the bot
Open `naukri_bot.py` and edit the `CONFIG` section at the top:

```python
CONFIG = {
    "email":    "ankitkmr635@gmail.com",   # ← your Naukri email
    "password": "YOUR_NEW_PASSWORD",        # ← your Naukri password

    "search_keywords": [
        "Selenium Java SDET",
        "Test Automation Engineer Java",
        "SDET Automation Testing",
        "QA Automation Lead Selenium",
        "Playwright Automation Engineer",
    ],
    "location":          "India",          # or "Pune", "Bengaluru" etc.
    "experience_years":  7,
    "min_relevance_score": 55,             # Only show jobs scoring above this
    "max_jobs_to_apply": 15,              # Safety cap per session
    ...
}
```

### Step 4 — Run
```bash
python naukri_bot.py
```

---

## What you'll see

```
=================================================================
  Smart Naukri Job Application Bot
  Profile: Senior Test Automation Engineer / SDET
=================================================================

  ► Logging into Naukri...
  ✓ Logged in successfully

  PHASE 1: Scanning jobs...
  ► Searching: 'Selenium Java SDET'
    Found 23 listings
  ► Searching: 'Test Automation Engineer Java'
    Found 18 listings
  ...
  Total unique jobs found: 61

-----------------------------------------------------------------
  JOBS FOUND — 61 scanned  |  24 above threshold  |  37 auto-skipped
-----------------------------------------------------------------

  [01] Score:  88/100  Senior SDET — Test Automation
       Thoughtworks Ltd                    Bengaluru
       Exp: 6-10 years    Salary: 20-32 LPA
       Core match: selenium, java, playwright | Preferred company

  [02] Score:  81/100  QA Automation Lead
       Deutsche Bank                       Pune
       Exp: 5-9 years     Salary: Not disclosed
       Core match: selenium, bdd, ci/cd | Bonus: jmeter, cucumber

  [03] Score:  74/100  Test Automation Engineer
       PhonePe                             Bengaluru
       Exp: 4-8 years     Salary: 18-28 LPA
       Core match: automation, java, api testing

  ...

  PHASE 2: Your approval required

  Options:
    all          — Apply to all 24 jobs above threshold
    top10        — Apply to top 10 by score
    1,3,5        — Apply to specific job numbers
    skip         — Exit without applying

  Your choice: top10

  ✓ 10 jobs approved for application.

  PHASE 3: Applying to 10 jobs...
  ► Applying: Senior SDET @ Thoughtworks...
    ✓ Applied successfully!
    Waiting 12s before next...
  ...

=================================================================
  APPLICATION SUMMARY
  Jobs scanned:    61
  Jobs approved:   10
  Applied:         9
  Failed/Skipped:  1

  Companies you applied to:
    ✓  Thoughtworks             Senior SDET
    ✓  Deutsche Bank            QA Automation Lead
    ✓  PhonePe                  Test Automation Engineer
    ...

  ✓ Log saved → application_log.csv
```

---

## Relevance scoring system

| Factor | Points |
|--------|--------|
| Core keyword match (selenium, java, playwright, etc.) | Up to 40 |
| Bonus keyword match (jmeter, bdd, agile, etc.) | Up to 30 |
| Preferred company (Thoughtworks, Deutsche Bank, etc.) | +15 |
| Experience mismatch (too junior/senior) | -10 to -20 |
| Blocked company | Score → 0 |
| **Max total** | **100** |

Jobs below `min_relevance_score` (default: 55) are **auto-skipped**.

---

## Output log (application_log.csv)

Every run appends to a CSV with:
- Job title, company, location, experience, salary
- Relevance score + match reason
- Status: applied / skipped / failed / already_applied
- Timestamp

---

## Tips for best results

1. **Run every 2-3 days** — don't mass-apply in one session
2. **Use `top10` not `all`** — targeted applications get more responses
3. **Add your real skip_companies** — avoids wasting applications
4. **Set headless: False** — watch it work the first time to verify
5. **Change your Naukri password** after each use session for security
6. **Don't run more than 15 applications per session** — the default cap

---

## Customising for your profile

Edit these lists in CONFIG to match your preferences:

```python
# Companies you WANT to work at (score boost)
"preferred_companies": [
    "Amazon", "Google", "Atlassian", "Thoughtworks",
    "PhonePe", "Razorpay", "Deutsche Bank", "Barclays",
    "ING", "ABN AMRO", "BNP Paribas", "JPMC",
],

# Companies you want to SKIP (score → 0)
"skip_companies": [
    # "CompanyNameHere",
],

# Keywords that MUST appear in the job (at least 2)
"must_have_keywords": [
    "selenium", "automation", "java", "python", "playwright",
    "api testing", "ci/cd", "jenkins", "azure devops", "bdd", "sdet",
],
```

---

## Important notes

- Your credentials are stored **only in the script on your laptop** — never sent anywhere
- The bot opens a real Chrome browser — not headless by default — so you can watch
- Random delays between actions mimic human behaviour to avoid detection
- If Naukri changes its page layout, XPaths in the code may need updating
- This is for personal use — use responsibly and within Naukri's fair use

---

*Built for Ankit Mistri | April 2026*
