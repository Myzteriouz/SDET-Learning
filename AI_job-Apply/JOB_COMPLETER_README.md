# Job Application Completer - Complete Guide

## Overview

The **Job Application Completer** is a smart follow-up tool that:

1. ✅ Reads jobs from your application log (`application_log.csv`)
2. ✅ Opens each job URL that's pending or failed
3. ✅ Detects all form fields & questions on the page
4. ✅ Intelligently answers questions using a **Q&A Repository**
5. ✅ When it encounters a question it hasn't seen before, it **learns** by saving your answer
6. ✅ For repeated questions (or similar ones), it **reuses** answers from the repository
7. ✅ Submits the application automatically

### Why This Tool?

After the bot scans and finds jobs, many of them require additional information:
- Expected salary
- Skills
- Experience level
- Notice period
- Availability for interview
- Why you're interested
- etc.

This tool **automates the completion** of these forms using intelligent question matching and learning.

---

## How It Works

### 1. **Question Repository System**

The tool maintains a `questions_repo.json` file that stores Q&A pairs:

```json
{
  "questions": [
    {
      "question": "What is your current notice period?",
      "answer": "Immediate",
      "type": "select",
      "usage_count": 5  ← Reused 5 times
    }
  ]
}
```

**First time seeing "What is your notice period?"**
```
? What is your notice period?
New question! Please provide answer:
Answer: Immediate
✓ Question saved to repository
```

**Second time seeing similar question**
```
? What's your current notice period in days?
✓ Found in repository: Immediate
(Auto-fills without asking!)
```

### 2. **Smart Matching**

The tool uses fuzzy matching to recognize similar questions:
- ✓ "What is your notice period?" 
- ✓ "What's your current notice period?"
- ✓ "Notice period in days?"
- ✓ "Notice period in weeks?"

→ All matched to same answer from repository

### 3. **Learning & Evolution**

- **First job**: Ask you for answers → Save to repository
- **Second job**: Recognize questions → Reuse answers
- **Statistics**: Track how many times each answer was reused
- **Growth**: Repository gets more intelligent with each job

---

## Usage

### Quick Start

```bash
# 1. Make sure you've run the main bot first (to generate application_log.csv)
python naukri_bot.py

# 2. Run the completer
python job_application_completer.py
```

### What Happens

```
==== Naukri Job Application Completer ====

✓ Loaded questions repository (8 Q&A pairs)
✓ Browser started

► Reading application log...
  Found 15 jobs to complete

► Processing 15 jobs...

  [1/15]
  ► SDET Engineer @ Devstringx
    Opening: https://www.naukri.com/job-listings-sdet-engineer...
    Found 3 form fields

    ? What is your notice period?
    ✓ Found in repository: Immediate
    
    ? Expected salary range?
    ✓ Found in repository: 15-25 Lacs PA
    
    ? Why are you interested?
    New question! Please provide answer:
    Answer: I'm interested because...
    ✓ Question saved to repository
    
    ✓ Filled 3/3 fields
    Clicking submit button...
    ✓ Application submitted!

  Waiting 7s before next...

  [2/15]
  ...
```

---

## Configuration

Edit the `CONFIG` dictionary in `job_application_completer.py`:

```python
CONFIG = {
    "log_file": "application_log.csv",              # Source of job URLs
    "questions_repo_file": "questions_repo.json",  # Q&A repository
    "headless": False,                              # False = watch it work
    "timeout": 30,                                  # Element timeout in seconds
    "delay_between_jobs": (5, 10),                 # Random delay between jobs
}
```

---

## Customizing the Question Repository

### View Current Repository

```bash
# The repository is stored in questions_repo.json
cat questions_repo.json
```

### Add Pre-Answers

Edit `questions_repo.json` directly:

```json
{
  "questions": [
    {
      "question": "Your question here",
      "answer": "Your answer here",
      "type": "text",
      "usage_count": 0
    }
  ]
}
```

### Common Pre-Answers to Add

```json
{
  "question": "Expected salary range",
  "answer": "15-25 Lacs PA",
  "type": "text",
  "usage_count": 0
}
```

```json
{
  "question": "Years of experience",
  "answer": "7",
  "type": "text",
  "usage_count": 0
}
```

```json
{
  "question": "Are you available for immediate interview",
  "answer": "Yes",
  "type": "radio",
  "usage_count": 0
}
```

---

## Supported Form Field Types

| Type | Examples | How Handled |
|------|----------|------------|
| **Text Input** | Name, Email, Phone | Typed character-by-character (human-like) |
| **Textarea** | Description, Cover Letter | Typed slowly (human-like typing) |
| **Select Dropdown** | Salary Range, Notice Period | Matched against options, auto-selected |
| **Radio Button** | Yes/No questions | Clicked if text matches answer |
| **Checkbox** | Skills, Preferences | Clicked based on match |
| **Label** | Terms & Conditions | Can be clicked |

---

## Workflow with Main Bot

### Complete Workflow (Bot + Completer)

```
Step 1: Generate Jobs & Applications
├─ python naukri_bot.py
│  ├─ Search for jobs
│  ├─ Score jobs
│  ├─ Ask for user approval
│  ├─ Apply to jobs
│  └─ Save to application_log.csv (with status: pending/applied/failed)

Step 2: Complete Applications with Questions
├─ python job_application_completer.py
│  ├─ Read application_log.csv
│  ├─ For each pending/failed job:
│  │  ├─ Open job URL
│  │  ├─ Detect form fields
│  │  ├─ Answer questions (from repo or ask user)
│  │  ├─ Save new questions to repo
│  │  └─ Submit application
│  └─ Show completion statistics
```

---

## Question Repository Statistics

After completion, you'll see statistics:

```
━━ Questions Repository Stats ━━
Total Q&A pairs:     15
Total reused:        42
Learning rate:       2.8 reuses/question
```

This means:
- You've learned **15 different questions**
- Your answers were **reused 42 times** across applications
- On average, each question was **used 2.8 times**

---

## Troubleshooting

### Problem: "No form fields detected"

**Cause**: Application might use JavaScript or dynamic loading

**Solution**: 
- Wait for page to fully load (timeout set to 30s)
- Manual intervention if needed
- Job will be marked as failed for later retry

### Problem: Question not being matched

**Cause**: Question wording is too different

**Solution**:
- Tool uses fuzzy matching with 70% similarity threshold
- If not matched, new question is learned  
- Next time it sees similar wording, it should match

### Problem: Wrong answer being auto-filled

**Cause**: Fuzzy matching picked wrong answer

**Solution**:
- Edit `questions_repo.json` to remove incorrect entry
- Or modify the answer in the repository
- Tool will use updated answer on next run

---

## Tips & Best Practices

### 1. Pre-populate Common Answers

Before running, add your standard answers to `questions_repo.json`:

```python
{
  "question": "Expected salary range",
  "answer": "15-25 Lacs PA",  # Your actual salary expectation
  "type": "text",
  "usage_count": 0
}
```

### 2. Review Answers After First Run

After the first batch of jobs:
1. Check `questions_repo.json`
2. Review what was learned
3. Correct any mistakes
4. Add missing common questions

### 3. Use Consistent Answers

The more consistent your answers are across questions, the better matching works:
- ✅ "15-25 Lacs PA" (consistent)
- ❌ "15-25 Lacs", "15-25L", "₹15-25L" (inconsistent)

### 4. Monitor Learning Rate

Higher reuse rate = better matching
- < 1.0 reuse/question → Most questions are new
- 2-3 reuse/question → Good matching
- > 3 reuse/question → Excellent reusability

---

## Advanced: Batch Processing

To process multiple batches of jobs:

```bash
# Run main bot to scan jobs
python naukri_bot.py

# Run completer (will auto-use growing repository)
python job_application_completer.py

# Repeat as needed - repository grows smarter
```

---

## API Reference

### QuestionsRepository

```python
# Initialize
repo = QuestionsRepository("questions_repo.json")

# Find similar question
answer = repo.find_similar_question("What's your notice period?", threshold=0.7)
# Returns: {"question": "...", "answer": "...", "usage_count": 5}

# Add new question
repo.add_question("What is your notice period?", "Immediate", "select")

# Record usage
repo.record_usage("What is your notice period?")

# Save
repo.save()

# Show stats
repo.show_stats()
```

---

## Future Enhancements

- [ ] Store form field types (text, select, radio) for better matching
- [ ] Support for cover letter generation
- [ ] LinkedIn profile auto-fill integration
- [ ] Machine learning for better question matching
- [ ] Support for file uploads (resume, documents)
- [ ] Rate limiting & anti-detection improvements
- [ ] Dashboard showing application completion status

---

## Safety Notes

⚠️ **Important**:
1. Review all auto-filled answers before submission
2. This tool fills forms on your behalf - use responsibly
3. Keep Naukri terms of service in mind
4. Do not use for spam or fraudulent applications
5. Personal information is stored locally only

---

## Questions or Issues?

Check the repository statistics:
```python
repo.show_stats()
```

This will show how many Q&A pairs you have and how effectively they're being reused.

---

**Happy Job Hunting!** 🚀
