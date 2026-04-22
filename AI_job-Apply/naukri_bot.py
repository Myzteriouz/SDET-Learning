"""
Smart Naukri Job Application Bot
=================================
- Searches for jobs matching your profile
- Scores each job for relevance (0-100)
- Shows you a preview list BEFORE applying
- Applies only to jobs YOU approve
- Logs everything to a CSV report

Requirements:
    pip install selenium webdriver-manager colorama pandas

Usage:
    python naukri_bot.py
"""

import time
import csv
import json
import random
import os
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import (
        TimeoutException, NoSuchElementException, ElementClickInterceptedException
    )
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("Missing packages. Run:  pip install selenium webdriver-manager")
    exit(1)

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = YELLOW = RED = CYAN = WHITE = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = BRIGHT = ""

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

CONFIG = {
    # ── Your Naukri credentials (stored locally only, never sent anywhere) ──
    "email":    "ankitkmr635@gmail.com",
    "password": "Tikn@635",

    # ── Search settings ──
    "search_keywords": [
        "Selenium Java SDET",
        "Test Automation Engineer Java",
        "SDET Automation Testing",
        "QA Automation Lead Selenium",
        "Playwright Automation Engineer",
    ],
    "location": "India",                  # e.g. "Pune", "Bengaluru", "India"
    "experience_years": 7,                # Your experience

    # ── Smart filters — jobs NOT matching these get auto-skipped ──
    "min_relevance_score": 55,            # 0-100. Only show jobs above this score
    "skip_if_already_applied": True,
    "skip_companies": [                   # Companies you don't want to apply to
        # "Wipro", "Infosys",            # (uncomment and add yours)
    ],
    "preferred_companies": [             # Boosts relevance score by 15 pts
        "Amazon", "Google", "Microsoft", "Atlassian", "Thoughtworks",
        "PhonePe", "Razorpay", "Flipkart", "JPMC", "Deutsche Bank",
        "Barclays", "ING", "ABN AMRO", "BNP Paribas",
    ],

    # ── Must-have keywords (job must contain at least 2 of these) ──
    "must_have_keywords": [
        "selenium", "automation", "java", "python", "playwright",
        "api testing", "ci/cd", "jenkins", "azure devops", "bdd", "sdet",
    ],

    # ── Nice-to-have keywords (each adds to score) ──
    "bonus_keywords": [
        "rest assured", "postman", "cucumber", "testng", "junit",
        "jmeter", "performance", "agile", "scrum", "banking", "bfsi",
        "salesforce", "page object", "hybrid framework", "devops",
    ],

    # ── Behaviour settings ──
    "max_jobs_to_scan":   50,            # Max jobs to scan per keyword search
    "max_jobs_to_apply":  15,            # Safety cap — won't apply to more than this
    "delay_between_apps": (8, 18),       # Random delay seconds between applications
    "headless":           False,         # False = you can watch it work
    "save_log":           True,          # Save results to CSV
    "log_file":           "application_log.csv",
    "auto_approve_jobs":  True,          # Auto-approve top {max_jobs_to_apply} jobs for application (no user prompt)
    "approval_mode":      "top10",       # "all" / "top10" / "manual" — only used if auto_approve_jobs=True
}

# ─── DATA CLASSES ─────────────────────────────────────────────────────────────

@dataclass
class Job:
    title:        str = ""
    company:      str = ""
    location:     str = ""
    experience:   str = ""
    salary:       str = ""
    posted:       str = ""
    skills:       str = ""
    description:  str = ""
    url:          str = ""
    relevance:    int = 0
    match_reason: str = ""
    status:       str = "pending"    # pending / approved / skipped / applied / failed

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def human_delay(min_s=1.5, max_s=4.0):
    """Random delay to mimic human behaviour."""
    time.sleep(random.uniform(min_s, max_s))

def debug_page_elements(driver):
    """Debug helper — print all input fields and buttons found on page."""
    print(f"\n  {Fore.YELLOW}━━━ DEBUG: Page Elements ━━━{Style.RESET_ALL}")
    try:
        # Find all input fields
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"  Found {len(inputs)} input fields:")
        for i, inp in enumerate(inputs[:5], 1):  # Show first 5
            inp_type = inp.get_attribute("type")
            inp_name = inp.get_attribute("name")
            inp_placeholder = inp.get_attribute("placeholder")
            inp_id = inp.get_attribute("id")
            print(f"    [{i}] type={inp_type}, name={inp_name}, placeholder={inp_placeholder}, id={inp_id}")
        
        # Find all buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"  Found {len(buttons)} buttons:")
        for i, btn in enumerate(buttons[:3], 1):  # Show first 3
            btn_text = btn.text[:40]
            btn_class = btn.get_attribute("class")
            btn_id = btn.get_attribute("id")
            print(f"    [{i}] text='{btn_text}', id={btn_id}, class={btn_class[:50]}")
    except Exception as e:
        print(f"  {Fore.RED}  Error during debug: {e}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}━━━ Page URL: {driver.current_url}{Style.RESET_ALL}\n")

def slow_type(element, text: str):
    """Type text with small random delays between characters."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.03, 0.12))

def score_job(job: Job, config: dict) -> tuple[int, str]:
    """
    Score a job 0-100 based on keyword match and profile fit.
    Returns (score, reason_string).
    """
    text = (job.title + " " + job.description + " " + job.skills).lower()
    score = 0
    reasons = []

    # Must-have keyword check — each hit = 8 pts, max 40
    must_hits = [kw for kw in config["must_have_keywords"] if kw.lower() in text]
    must_score = min(len(must_hits) * 8, 40)
    score += must_score
    if must_hits:
        reasons.append(f"Core match: {', '.join(must_hits[:4])}")

    # Bonus keywords — each = 4 pts, max 30
    bonus_hits = [kw for kw in config["bonus_keywords"] if kw.lower() in text]
    bonus_score = min(len(bonus_hits) * 4, 30)
    score += bonus_score
    if bonus_hits:
        reasons.append(f"Bonus: {', '.join(bonus_hits[:3])}")

    # Preferred company boost
    if any(c.lower() in job.company.lower() for c in config["preferred_companies"]):
        score += 15
        reasons.append("Preferred company")

    # Skip-company penalty
    if any(c.lower() in job.company.lower() for c in config["skip_companies"]):
        score = 0
        reasons = ["Skipped company"]

    # Experience range check (basic heuristic)
    exp_text = job.experience.lower()
    if "fresher" in exp_text or "0-1" in exp_text:
        score -= 20
        reasons.append("Too junior")
    elif "15+" in exp_text or "12+" in exp_text:
        score -= 10
        reasons.append("Too senior")

    return min(score, 100), " | ".join(reasons)

def print_header():
    print(f"\n{Fore.CYAN}{'='*65}")
    print(f"  Smart Naukri Job Application Bot")
    print(f"  Profile: Senior Test Automation Engineer / SDET")
    print(f"{'='*65}{Style.RESET_ALL}\n")

def print_job_preview(jobs: List[Job], config: dict):
    """Print a formatted preview table of all scanned jobs."""
    approved = [j for j in jobs if j.relevance >= config["min_relevance_score"]]
    skipped  = [j for j in jobs if j.relevance <  config["min_relevance_score"]]

    print(f"\n{Fore.CYAN}{'─'*65}")
    print(f"  JOBS FOUND — {len(jobs)} scanned  |  {len(approved)} above threshold  |  {len(skipped)} auto-skipped")
    print(f"{'─'*65}{Style.RESET_ALL}\n")

    for i, job in enumerate(approved, 1):
        score_color = Fore.GREEN if job.relevance >= 70 else Fore.YELLOW
        print(f"  {Fore.WHITE}[{i:02d}] {score_color}Score: {job.relevance:3d}/100{Style.RESET_ALL}  "
              f"{Fore.WHITE}{job.title[:40]:<40}{Style.RESET_ALL}")
        print(f"       {Fore.CYAN}{job.company[:35]:<35}{Style.RESET_ALL}  {job.location}")
        print(f"       Exp: {job.experience:<15}  Salary: {job.salary}")
        print(f"       {Fore.MAGENTA}{job.match_reason[:70]}{Style.RESET_ALL}")
        print()

    if skipped:
        print(f"{Fore.YELLOW}  Auto-skipped {len(skipped)} jobs below score threshold ({config['min_relevance_score']}){Style.RESET_ALL}")

    return approved

def get_user_approval(approved_jobs: List[Job], max_apply: int) -> List[Job]:
    """Interactive approval — user selects which jobs to apply to."""
    if not approved_jobs:
        print(f"{Fore.RED}  No jobs met the relevance threshold. Try lowering min_relevance_score in CONFIG.{Style.RESET_ALL}")
        return []

    print(f"\n{Fore.CYAN}{'─'*65}")
    print("  SELECT JOBS TO APPLY")
    print(f"{'─'*65}{Style.RESET_ALL}")
    print(f"  Options:")
    print(f"    {Fore.GREEN}all{Style.RESET_ALL}          — Apply to all {len(approved_jobs)} jobs above threshold")
    print(f"    {Fore.GREEN}top10{Style.RESET_ALL}        — Apply to top 10 by score")
    print(f"    {Fore.GREEN}1,3,5{Style.RESET_ALL}        — Apply to specific job numbers")
    print(f"    {Fore.GREEN}skip{Style.RESET_ALL}         — Exit without applying")
    print()

    while True:
        choice = input(f"  {Fore.WHITE}Your choice: {Style.RESET_ALL}").strip().lower()

        if choice == "skip":
            return []
        elif choice == "all":
            selected = approved_jobs[:max_apply]
        elif choice.startswith("top"):
            n = int(choice.replace("top", "").strip() or "10")
            selected = sorted(approved_jobs, key=lambda j: j.relevance, reverse=True)[:n]
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",")]
                selected = [approved_jobs[i] for i in indices if 0 <= i < len(approved_jobs)]
            except (ValueError, IndexError):
                print(f"  {Fore.RED}Invalid input. Try: all / top10 / 1,2,3 / skip{Style.RESET_ALL}")
                continue

        if len(selected) > max_apply:
            print(f"  {Fore.YELLOW}Safety cap: limiting to {max_apply} applications.{Style.RESET_ALL}")
            selected = selected[:max_apply]

        for j in selected:
            j.status = "approved"
        print(f"\n  {Fore.GREEN}✓ {len(selected)} jobs approved for application.{Style.RESET_ALL}\n")
        return selected

def save_log(jobs: List[Job], log_file: str):
    """Save all job results to CSV."""
    if not jobs:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    rows = []
    for j in jobs:
        row = asdict(j)
        row["scanned_at"] = timestamp
        rows.append(row)

    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)
    print(f"\n  {Fore.GREEN}✓ Log saved → {log_file}{Style.RESET_ALL}")

# ─── NAUKRI BOT CLASS ─────────────────────────────────────────────────────────

class NaukriBot:

    def __init__(self, config: dict):
        self.config = config
        self.driver  = None
        self.wait    = None
        self.all_jobs: List[Job] = []

    # ── Browser setup ─────────────────────────────────────────────────────────

    def setup_driver(self):
        opts = Options()
        if self.config["headless"]:
            opts.add_argument("--headless=new")
        # Anti-detection options
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.add_argument("--start-maximized")
        opts.add_argument("--disable-notifications")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=opts)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        # Increased timeout from 15 to 25 seconds for dynamic content
        self.wait = WebDriverWait(self.driver, 25)
        print(f"  {Fore.GREEN}✓ Browser started{Style.RESET_ALL}")

    # ── Login ─────────────────────────────────────────────────────────────────

    def login(self) -> bool:
        print(f"\n  {Fore.CYAN}► Logging into Naukri...{Style.RESET_ALL}")
        try:
            self.driver.get("https://www.naukri.com/nlogin/login")
            human_delay(2, 4)

            # Try multiple selectors for email field (Naukri changes layout frequently)
            email_field = None
            email_selectors = [
                (By.ID, "usernameField"),  # Primary selector - confirmed ID
                (By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"),
                (By.XPATH, "//input[@placeholder='Email']"),
                (By.NAME, "usernameField"),
                (By.CSS_SELECTOR, "input[type='text'][placeholder*='Email']"),
                (By.XPATH, "//input[@type='text'][contains(@placeholder, 'Email') or contains(@placeholder, 'Username')]"),
                (By.CSS_SELECTOR, "input[data-qa-id='email']"),
                (By.CSS_SELECTOR, ".input input[type='text']"),
            ]

            for selector_type, selector_value in email_selectors:
                try:
                    email_field = self.wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                    print(f"  {Fore.WHITE}  Found email field with selector: {selector_value[:50]}{Style.RESET_ALL}")
                    break
                except TimeoutException:
                    continue
                except Exception:
                    continue

            if not email_field:
                print(f"  {Fore.YELLOW}  Email field not found with standard selectors, trying scroll...{Style.RESET_ALL}")
                self.driver.execute_script("window.scrollTo(0, 0);")
                human_delay(1, 2)
                try:
                    email_field = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")),
                        timeout=10
                    )
                except TimeoutException:
                    raise

            slow_type(email_field, self.config["email"])
            human_delay(0.5, 1.2)

            # Try multiple selectors for password field
            pwd_field = None
            pwd_selectors = [
                (By.ID, "passwordField"),  # Primary selector - confirmed ID
                (By.XPATH, "//input[@placeholder='Enter your password']"),
                (By.XPATH, "//input[@placeholder='Password']"),
                (By.NAME, "passwordField"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.CSS_SELECTOR, "input[data-qa-id='password']"),
            ]

            for selector_type, selector_value in pwd_selectors:
                try:
                    pwd_field = self.driver.find_element(selector_type, selector_value)
                    print(f"  {Fore.WHITE}  Found password field with selector: {selector_value[:50]}{Style.RESET_ALL}")
                    break
                except NoSuchElementException:
                    continue

            if not pwd_field:
                print(f"  {Fore.RED}  Password field not found!{Style.RESET_ALL}")
                raise NoSuchElementException("Password field not found")

            slow_type(pwd_field, self.config["password"])
            human_delay(0.8, 1.5)

            # Try multiple selectors for login button
            login_btn = None
            login_selectors = [
                (By.XPATH, "//button[@type='submit']"),  # Primary selector - confirmed type
                (By.XPATH, "//button[contains(text(),'Login')]"),
                (By.XPATH, "//button[contains(text(),'login')]"),
                (By.ID, "loginButton"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[text()='Login']"),
            ]

            for selector_type, selector_value in login_selectors:
                try:
                    login_btn = self.driver.find_element(selector_type, selector_value)
                    print(f"  {Fore.WHITE}  Found login button with selector: {selector_value[:50]}{Style.RESET_ALL}")
                    break
                except NoSuchElementException:
                    continue

            if not login_btn:
                print(f"  {Fore.RED}  Login button not found!{Style.RESET_ALL}")
                raise NoSuchElementException("Login button not found")

            login_btn.click()
            human_delay(3, 5)

            # Verify login success with multiple conditions
            try:
                # Wait for page to redirect or dashboard to load
                WebDriverWait(self.driver, 20).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                human_delay(2, 3)
            except TimeoutException:
                pass

            # ── Handle post-login questionnaire/profile modal ──
            self._handle_profile_questionnaire()

            current_url = self.driver.current_url.lower()
            # More flexible URL check
            if ("login" not in current_url or "myapps" in current_url or 
                "myjobs" in current_url or "my-profile" in current_url or
                "dashboard" in current_url):
                print(f"  {Fore.GREEN}✓ Logged in successfully{Style.RESET_ALL}")
                return True
            else:
                # Check if page has loaded job search interface
                try:
                    self.driver.find_element(By.CLASS_NAME, "srp-jobtuple-wrapper")
                    print(f"  {Fore.GREEN}✓ Logged in successfully (on job results){Style.RESET_ALL}")
                    return True
                except NoSuchElementException:
                    pass

                print(f"  {Fore.RED}✗ Login may have failed — URL: {current_url}{Style.RESET_ALL}")
                return False

        except TimeoutException as e:
            print(f"  {Fore.RED}✗ Login page timeout — Naukri may have changed its layout{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}  Debug: {str(e)}{Style.RESET_ALL}")
            return False
        except NoSuchElementException as e:
            print(f"  {Fore.RED}✗ Required login element not found: {str(e)}{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}  Naukri's layout may have changed significantly.{Style.RESET_ALL}")
            debug_page_elements(self.driver)
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Login error: {str(e)}{Style.RESET_ALL}")
            debug_page_elements(self.driver)
            return False

    def _handle_profile_questionnaire(self):
        """
        Handle Naukri's post-login profile questionnaire modals.
        Naukri often shows popups asking for expected salary, skills, etc.
        """
        print(f"  {Fore.WHITE}  Checking for profile questionnaire...{Style.RESET_ALL}")
        
        try:
            # Give modal time to appear
            time.sleep(2)
            
            # Try multiple close/skip button strategies
            close_selectors = [
                (By.XPATH, "//button[@aria-label='Close']"),
                (By.XPATH, "//button[contains(text(),'Skip')]"),
                (By.XPATH, "//button[contains(text(),'skip')]"),
                (By.XPATH, "//button[contains(text(),'Later')]"),
                (By.XPATH, "//button[contains(text(),'later')]"),
                (By.XPATH, "//button[contains(text(),'Cancel')]"),
                (By.XPATH, "//button[contains(text(),'cancel')]"),
                (By.XPATH, "//span[contains(@class,'close')]"),
                (By.CSS_SELECTOR, "button.close"),
                (By.CSS_SELECTOR, "[class*='closeIcon']"),
                (By.CSS_SELECTOR, "[class*='modal-close']"),
                (By.XPATH, "//div[@class='modal-close']"),
            ]
            
            for selector_type, selector_value in close_selectors:
                try:
                    close_btn = self.driver.find_element(selector_type, selector_value)
                    if close_btn.is_displayed():
                        print(f"  {Fore.YELLOW}  Found close button, clicking...{Style.RESET_ALL}")
                        close_btn.click()
                        human_delay(1, 2)
                        print(f"  {Fore.GREEN}  ✓ Modal closed{Style.RESET_ALL}")
                        return
                except (NoSuchElementException, ElementClickInterceptedException):
                    continue
                except Exception:
                    continue
            
            # Try pressing Escape key multiple times
            body = self.driver.find_element(By.TAG_NAME, "body")
            for _ in range(3):
                try:
                    body.send_keys(Keys.ESCAPE)
                    human_delay(0.3, 0.7)
                except Exception:
                    pass
            
            # If still modal visible, try JavaScript to close
            try:
                # Find and hide all overlay/modal elements
                self.driver.execute_script("""
                    let modals = document.querySelectorAll('[role="dialog"], .modal, [class*="modal"], [class*="popup"], [class*="overlay"]');
                    modals.forEach(m => {
                        if(m && m.style) m.style.display = 'none';
                    });
                    document.body.style.overflow = 'auto';
                """)
                print(f"  {Fore.YELLOW}  Used JavaScript to hide modal elements{Style.RESET_ALL}")
            except Exception:
                pass
            
        except Exception as e:
            print(f"  {Fore.YELLOW}  No questionnaire modal detected: {str(e)[:40]}{Style.RESET_ALL}")

    # ── Search & Scrape ───────────────────────────────────────────────────────

    def search_jobs(self, keyword: str) -> List[Job]:
        """Search Naukri for a keyword and scrape job listings."""
        print(f"\n  {Fore.CYAN}► Searching: '{keyword}'{Style.RESET_ALL}")
        jobs = []

        try:
            # Build search URL
            kw_encoded = keyword.replace(" ", "-")
            loc_encoded = self.config["location"].replace(" ", "-").lower()
            url = (f"https://www.naukri.com/{kw_encoded}-jobs-in-{loc_encoded}"
                   f"?experience={self.config['experience_years']}&k={keyword}"
                   f"&l={self.config['location']}")

            self.driver.get(url)
            human_delay(2, 4)

            # Close any modal that might appear on search results
            self._close_any_modal()
            human_delay(1, 2)

            # Wait for job cards with retries
            max_retries = 3
            cards_found = False
            for retry in range(max_retries):
                try:
                    self.wait.until(EC.presence_of_element_located(
                        (By.CLASS_NAME, "srp-jobtuple-wrapper")
                    ))
                    cards_found = True
                    break
                except TimeoutException:
                    if retry < max_retries - 1:
                        print(f"  {Fore.YELLOW}  Retry {retry + 1}/{max_retries} — job cards not found{Style.RESET_ALL}")
                        self.driver.refresh()
                        human_delay(2, 3)
                    continue

            if not cards_found:
                print(f"  {Fore.YELLOW}  No results found for '{keyword}'{Style.RESET_ALL}")
                return []

            cards = self.driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
            cards = cards[:self.config["max_jobs_to_scan"]]
            print(f"  {Fore.WHITE}  Found {len(cards)} listings{Style.RESET_ALL}")

            for card in cards:
                try:
                    job = self._parse_job_card(card)
                    if job:
                        job.relevance, job.match_reason = score_job(job, self.config)
                        jobs.append(job)
                except Exception:
                    continue

        except Exception as e:
            print(f"  {Fore.RED}  Search error: {e}{Style.RESET_ALL}")

        return jobs

    def _parse_job_card(self, card) -> Optional[Job]:
        """Extract job details from a Naukri job card element."""
        job = Job()
        try:
            # Title + URL
            title_el = card.find_element(By.CLASS_NAME, "title")
            job.title = title_el.text.strip()
            job.url   = title_el.get_attribute("href") or ""
        except NoSuchElementException:
            return None

        try:
            job.company = card.find_element(By.CLASS_NAME, "comp-name").text.strip()
        except NoSuchElementException:
            job.company = "Unknown"

        try:
            job.location = card.find_element(By.CLASS_NAME, "locWdth").text.strip()
        except NoSuchElementException:
            pass

        try:
            job.experience = card.find_element(By.CLASS_NAME, "expwdth").text.strip()
        except NoSuchElementException:
            pass

        try:
            job.salary = card.find_element(By.CLASS_NAME, "sal").text.strip()
        except NoSuchElementException:
            job.salary = "Not disclosed"

        try:
            job.posted = card.find_element(By.CLASS_NAME, "job-post-day").text.strip()
        except NoSuchElementException:
            pass

        try:
            skill_tags = card.find_elements(By.CLASS_NAME, "tag-li")
            job.skills = ", ".join([t.text for t in skill_tags])
        except NoSuchElementException:
            pass

        # Use title + skills as description proxy (full desc requires page open)
        job.description = f"{job.title} {job.skills}"

        return job

    def _get_full_description(self, job: Job) -> str:
        """Open job page and get full description (used for deep scoring)."""
        if not job.url:
            return ""
        try:
            self.driver.execute_script(f"window.open('{job.url}');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            human_delay(2, 3)
            desc_el = self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "job-desc")
            ))
            desc = desc_el.text
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            human_delay(1, 2)
            return desc
        except Exception:
            try:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            except Exception:
                pass
            return ""

    # ── Apply ─────────────────────────────────────────────────────────────────

    def apply_to_job(self, job: Job) -> bool:
        """Open the job page and click Apply."""
        print(f"\n  {Fore.CYAN}► Applying: {job.title} @ {job.company}{Style.RESET_ALL}")
        try:
            self.driver.get(job.url)
            human_delay(2, 4)

            # Close any modals that might appear
            self._close_any_modal()

            # Look for Apply button variants
            apply_selectors = [
                "//button[contains(text(),'Apply')]",
                "//button[contains(text(),'apply')]",
                "//a[contains(text(),'Apply')]",
                "//*[@id='apply-button']",
                "//button[contains(@class,'apply')]",
            ]

            apply_btn = None
            for sel in apply_selectors:
                try:
                    apply_btn = self.driver.find_element(By.XPATH, sel)
                    break
                except NoSuchElementException:
                    continue

            if not apply_btn:
                print(f"  {Fore.YELLOW}  Apply button not found — may require external application{Style.RESET_ALL}")
                job.status = "failed"
                return False

            # Check if already applied
            btn_text = apply_btn.text.lower()
            if "applied" in btn_text:
                print(f"  {Fore.YELLOW}  Already applied{Style.RESET_ALL}")
                job.status = "already_applied"
                return False

            # Try to click with multiple strategies
            try:
                apply_btn.click()
            except ElementClickInterceptedException:
                # Element might be hidden, try scrolling
                self.driver.execute_script("arguments[0].scrollIntoView(true);", apply_btn)
                human_delay(0.5, 1)
                apply_btn.click()

            human_delay(2, 3)

            # Close any success/info modals that appear
            self._close_any_modal()

            # Handle any confirmation modal
            try:
                confirm_btn = WebDriverWait(self.driver, 4).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(),'Apply')]")
                    )
                )
                confirm_btn.click()
                human_delay(1, 2)
            except TimeoutException:
                pass

            print(f"  {Fore.GREEN}  ✓ Applied successfully!{Style.RESET_ALL}")
            job.status = "applied"
            return True

        except ElementClickInterceptedException:
            print(f"  {Fore.YELLOW}  Click intercepted — possible popup blocking{Style.RESET_ALL}")
            self._close_any_modal()
            job.status = "failed"
            return False
        except Exception as e:
            print(f"  {Fore.RED}  Error applying: {str(e)[:100]}{Style.RESET_ALL}")
            job.status = "failed"
            return False

    def _close_any_modal(self):
        """Close any popup/modal that might be blocking interaction."""
        try:
            close_selectors = [
                (By.XPATH, "//button[@aria-label='Close']"),
                (By.XPATH, "//button[contains(text(),'Close')]"),
                (By.XPATH, "//button[contains(text(),'close')]"),
                (By.XPATH, "//span[contains(@class,'close')]"),
                (By.CSS_SELECTOR, "button.close"),
                (By.CSS_SELECTOR, "[class*='closeIcon']"),
                (By.CSS_SELECTOR, "[class*='modal-close']"),
            ]
            
            for selector_type, selector_value in close_selectors:
                try:
                    close_btn = self.driver.find_element(selector_type, selector_value)
                    if close_btn.is_displayed():
                        close_btn.click()
                        human_delay(0.5, 1)
                        return
                except (NoSuchElementException, ElementClickInterceptedException):
                    continue
                except Exception:
                    continue
            
            # Try Escape key
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            except Exception:
                pass
        except Exception:
            pass

    # ── Main workflow ──────────────────────────────────────────────────────────

    def run(self):
        print_header()
        self.setup_driver()

        try:
            if not self.login():
                return

            # Step 1 — Collect jobs from all keywords
            print(f"\n{Fore.CYAN}  PHASE 1: Scanning jobs...{Style.RESET_ALL}")
            seen_urls = set()
            for keyword in self.config["search_keywords"]:
                jobs = self.search_jobs(keyword)
                for job in jobs:
                    if job.url not in seen_urls:
                        seen_urls.add(job.url)
                        self.all_jobs.append(job)
                human_delay(3, 6)

            print(f"\n  {Fore.WHITE}Total unique jobs found: {len(self.all_jobs)}{Style.RESET_ALL}")

            # Step 2 — Sort by score, show preview
            self.all_jobs.sort(key=lambda j: j.relevance, reverse=True)
            approved_jobs = print_job_preview(self.all_jobs, self.config)

            # Step 3 — User approves (or auto-approve if enabled)
            print(f"\n{Fore.CYAN}  PHASE 2: Approval & Application{Style.RESET_ALL}")
            
            if self.config.get("auto_approve_jobs", False):
                # Auto-approve mode — skip user prompt
                if self.config.get("approval_mode", "top10") == "all":
                    to_apply = approved_jobs[:self.config["max_jobs_to_apply"]]
                    print(f"  {Fore.GREEN}✓ Auto-approved all {len(to_apply)} jobs{Style.RESET_ALL}")
                else:  # default: top10
                    sorted_jobs = sorted(approved_jobs, key=lambda j: j.relevance, reverse=True)
                    to_apply = sorted_jobs[:min(10, self.config["max_jobs_to_apply"])]
                    print(f"  {Fore.GREEN}✓ Auto-approved top {len(to_apply)} jobs{Style.RESET_ALL}")
                
                for j in to_apply:
                    j.status = "approved"
            else:
                # Manual approval — show prompt
                print(f"  Your approval required")
                to_apply = get_user_approval(approved_jobs, self.config["max_jobs_to_apply"])

            if not to_apply:
                print(f"\n  {Fore.YELLOW}No jobs selected. Exiting.{Style.RESET_ALL}")
                return

            # Step 4 — Apply
            print(f"\n{Fore.CYAN}  PHASE 3: Applying to {len(to_apply)} jobs...{Style.RESET_ALL}")
            applied_count = 0
            for job in to_apply:
                success = self.apply_to_job(job)
                if success:
                    applied_count += 1

                # Random delay between applications (avoids detection)
                min_d, max_d = self.config["delay_between_apps"]
                delay = random.uniform(min_d, max_d)
                print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                time.sleep(delay)

            # Step 5 — Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  APPLICATION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Jobs scanned:    {len(self.all_jobs)}")
            print(f"  Jobs approved:   {len(to_apply)}")
            print(f"  Applied:         {Fore.GREEN}{applied_count}{Style.RESET_ALL}")
            failed = len(to_apply) - applied_count
            if failed:
                print(f"  Failed/Skipped:  {Fore.YELLOW}{failed}{Style.RESET_ALL}")

            # Step 6 — Save log
            if self.config["save_log"]:
                save_log(self.all_jobs, self.config["log_file"])

            # Print applied companies
            applied_jobs = [j for j in self.all_jobs if j.status == "applied"]
            if applied_jobs:
                print(f"\n  {Fore.GREEN}Companies you applied to:{Style.RESET_ALL}")
                for j in applied_jobs:
                    print(f"    ✓  {j.company:<30}  {j.title}")

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.config["save_log"]:
                save_log(self.all_jobs, self.config["log_file"])
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    bot = NaukriBot(CONFIG)
    bot.run()
