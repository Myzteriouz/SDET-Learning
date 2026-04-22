# 🚀 Complete Job Application Automation - Quick Start

This folder contains a **two-stage job application automation system**:

1. **Stage 1**: `naukri_bot.py` - Finds & applies to jobs
2. **Stage 2**: `job_application_completer.py` - Completes applications by answering questions

---

## Installation

```bash
# Install dependencies
pip install selenium webdriver-manager colorama pandas

# Or from requirements.txt
pip install -r requirements.txt
```

---

## Quick Start (3 Easy Steps)

### Step 1: Find & Apply to Jobs

```bash
python naukri_bot.py
```

This will:
- ✅ Log into Naukri
- ✅ Search for jobs matching your profile
- ✅ Score each job by relevance
- ✅ Show you a preview
- ✅ Ask which jobs to apply to (or auto-apply if configured)
- ✅ Apply to selected jobs
- ✅ Generate `application_log.csv`

**What you'll see:**
```
✓ Browser started
► Logging into Naukri...
✓ Logged in successfully
  PHASE 1: Scanning jobs...
  ► Searching: 'Selenium Java SDET'
    Found 25 listings
  ...Total unique jobs found: 50
  
  JOBS FOUND — 50 scanned | 35 above threshold | 15 auto-skipped
  
  PHASE 2: Approval & Application
  ✓ Auto-approved top 10 jobs
  
  PHASE 3: Applying to 10 jobs...
```

### Step 2: Complete Applications With Questions

```bash
python job_application_completer.py
```

This will:
- ✅ Read pending jobs from `application_log.csv`
- ✅ Open each job URL
- ✅ Detect form fields & questions
- ✅ Auto-fill from `questions_repo.json` (if answer known)
- ✅ Ask you for new questions (and learn the answer)
- ✅ Submit applications
- ✅ Show completion stats

**What you'll see:**
```
✓ Loaded questions repository (8 Q&A pairs)
✓ Browser started
► Reading application log...
  Found 15 jobs to complete
  
► Processing 15 jobs...
  [1/15]
  ► SDET Engineer @ Devstringx
    Found 3 form fields
    ? What is your notice period?
    ✓ Found in repository: Immediate
    
    ? Expected salary range?
    ✓ Found in repository: 15-25 Lacs PA
    
    ✓ Filled 3/3 fields
    ✓ Application submitted!
```

### Step 3: Monitor Progress

Check the results:

```bash
# See all applications
cat application_log.csv

# See learned questions
cat questions_repo.json

# View statistics (printed at end)
# Total jobs processed, success rate, learning growth
```

---

## File Structure

```
AI_job-Apply/
├── naukri_bot.py                    # Main job finder & applier
├── job_application_completer.py     # Question handler & form completer
├── questions_repo.json              # Q&A repository (grows with each run)
├── application_log.csv              # Log of all applications
├── README.md                        # Original documentation
├── JOB_COMPLETER_README.md         # Completer detailed guide
└── QUICK_START.md                  # This file!
```

---

## Configuration

### For Main Bot (`naukri_bot.py`)

Edit the `CONFIG` section:

```python
CONFIG = {
    "email":    "your-email@gmail.com",
    "password": "your-password",
    
    "search_keywords": [
        "Selenium Java SDET",
        "Test Automation Engineer Java",
    ],
    
    "location": "India",
    "experience_years": 7,
    
    "min_relevance_score": 55,      # Only jobs above this score
    "max_jobs_to_apply": 15,        # Max apps per run
    
    "auto_approve_jobs": True,      # Auto-approve without asking
    "approval_mode": "top10",       # "all" or "top10"
}
```

### For App Completer (`job_application_completer.py`)

Edit the `CONFIG` section:

```python
CONFIG = {
    "questions_repo_file": "questions_repo.json",
    "headless": False,              # False = watch it work
    "timeout": 30,                  # Seconds
    "delay_between_jobs": (5, 10),  # Random delay
}
```

---

## Pre-Configure Common Answers

Before first run, add your standard answers to `questions_repo.json`:

```json
{
  "questions": [
    {
      "question": "Expected salary range",
      "answer": "15-25 Lacs PA",
      "type": "text",
      "usage_count": 0
    },
    {
      "question": "Years of experience",
      "answer": "7",
      "type": "text",
      "usage_count": 0
    },
    {
      "question": "Are you available for immediate interview",
      "answer": "Yes",
      "type": "radio",
      "usage_count": 0
    },
    {
      "question": "Current notice period",
      "answer": "Immediate",
      "type": "select",
      "usage_count": 0
    }
  ],
  "metadata": {
    "created": "2026-04-21T00:00:00",
    "updated": "2026-04-21T00:00:00",
    "total_learned": 0
  }
}
```

---

## Typical Workflow

### Day 1: Initial Setup

```bash
# 1. Configure your credentials and preferences
vim naukri_bot.py

# 2. Add common answers
vim questions_repo.json

# 3. Run the bot
python naukri_bot.py
# Output: Found 50 jobs, applied to 10
```

### Day 2: Complete Applications

```bash
# 1. Complete the pending applications
python job_application_completer.py
# Output: Completed 10 applications, learned 7 new questions

# 2. Review results
cat application_log.csv
cat questions_repo.json
```

### Day 3+: Rinse & Repeat

```bash
# Run bot again with same or new keywords
python naukri_bot.py

# Complete new applications (using learned answers)
python job_application_completer.py
```

---

## How the Q&A Repository Works

### First Time Seeing a Question

```
? What is your notice period?
New question! Please provide answer:
Answer: Immediate
✓ Question saved to repository
```

Repository is updated:
```json
{
  "question": "What is your notice period?",
  "answer": "Immediate",
  "usage_count": 1
}
```

### Second Time (Even Slightly Different Wording)

```
? What's your current notice period in days?
✓ Found in repository: Immediate
```

**Matching is intelligent** - recognizes variations like:
- "What is your notice period?"
- "Current notice period?"
- "Notice period in days?"
- "Weeks notice required?"

---

## Tips for Success

### 1. Start Small

```bash
# First run: Use fewer keywords
"search_keywords": [
    "Selenium SDET",
],
"max_jobs_to_apply": 5,  # Start with 5
```

### 2. Monitor and Adjust

After first few runs:
- Check `questions_repo.json` - does it look right?
- Update/correct any bad entries
- Add more pre-answers based on what you learned

### 3. Build Your Repository

The more jobs you apply to, the better:
- Run 1: Learn 10 questions
- Run 2: Reuse ~70% of answers (faster)
- Run 3: Reuse ~90% of answers (almost automatic)

### 4. Increase Job Count Gradually

```python
# After first 5 successful apps:
"max_jobs_to_apply": 10,

# After next 10:
"max_jobs_to_apply": 15,

# After next 20:
"max_jobs_to_apply": 25,
```

---

## Combining with Manual Review

### Option A: Fully Automatic

```bash
# Configure
CONFIG["auto_approve_jobs"] = True

# Run
python naukri_bot.py        # Auto-applies
python job_application_completer.py  # Auto-completes
```

### Option B: Manual Review

```bash
# Configure
CONFIG["auto_approve_jobs"] = False

# Run
python naukri_bot.py
# Shows jobs, asks which to approve (manually choose)

python job_application_completer.py
# Still auto-completes based on learned answers
```

---

## Troubleshooting

### Bot won't login
- Check credentials in CONFIG
- Verify internet connection
- Naukri might have changed layout → check bot logs

### Completer can't find form fields
- Keep browser window visible to debug
- Check if page loads correctly
- Some jobs might require special handling

### Wrong answer auto-filled
- Edit `questions_repo.json` to fix
- Remove the question entry and re-run

### Too slow?
- Reduce `delay_between_jobs` in CONFIG
- Set `headless: True` to run in background
- But be careful - too fast can trigger detection

---

## Important Notes

⚠️ **Use Responsibly**:
1. Keep Naukri terms of service in mind
2. Do not spam applications
3. Only apply to jobs you're genuinely interested in
4. Review auto-filled answers for accuracy
5. Information stays local - never sent to external services

✅ **What This Tool Does**:
- Finds relevant job matches (smart scoring)
- Saves time on repetitive form filling
- Learns your preferences over time
- Applies strategically (not spam)

---

## Next Steps

1. **Read Full Documentation**:
   - `README.md` - Original bot docs
   - `JOB_COMPLETER_README.md` - Detailed completer guide

2. **Customize for Your Needs**:
   - Edit search keywords for your role
   - Set realistic salary expectations
   - Configure preferred companies

3. **Start Small**:
   - Run with `max_jobs_to_apply: 5` first
   - Review the results
   - Expand as confidence grows

4. **Monitor & Learn**:
   - Check `questions_repo.json` regularly
   - Improve answers based on outcomes
   - Watch the learning stats grow

---

## Support

If something goes wrong:
1. Check the colored error messages
2. Review the logs in terminal
3. Check `application_log.csv` for status
4. Look at `questions_repo.json` for learned data
5. Read detailed docs: `JOB_COMPLETER_README.md`

---

**Good luck with your job search!** 🎯

*Remember: This tool is an assistant. Your genuine interest and qualifications matter most!*
