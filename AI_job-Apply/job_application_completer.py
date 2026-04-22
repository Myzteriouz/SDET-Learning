"""
Naukri Job Application Completer
==================================
- Reads job application logs
- Opens each job and applies with question handling
- Maintains a Q&A repository for intelligent answering
- Learns from previous answers and reuses them

Usage:
    python job_application_completer.py

Dependencies:
    pip install selenium webdriver-manager colorama pandas
"""

import csv
import json
import time
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import (
        TimeoutException, NoSuchElementException, ElementClickInterceptedException,
        StaleElementReferenceException
    )
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("Missing packages. Run:  pip install selenium webdriver-manager colorama pandas")
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
    "log_file": "application_log.csv",
    "questions_repo_file": "questions_repo.json",
    "headless": False,
    "timeout": 30,  # seconds
    "delay_between_jobs": (5, 10),  # Random delay between job applications
}

# ─── QUESTIONS REPOSITORY MANAGER ─────────────────────────────────────────────

class QuestionsRepository:
    """Manages Q&A repository with intelligence for matching similar questions."""

    def __init__(self, repo_file: str):
        self.repo_file = repo_file
        self.data = self._load_repo()

    def _load_repo(self) -> Dict:
        """Load existing repository or create new one."""
        if Path(self.repo_file).exists():
            try:
                with open(self.repo_file, 'r', encoding='utf-8') as f:
                    repo = json.load(f)
                    print(f"  {Fore.GREEN}✓ Loaded questions repository ({len(repo.get('questions', []))} Q&A pairs){Style.RESET_ALL}")
                    return repo
            except Exception as e:
                print(f"  {Fore.YELLOW}  Could not load repo: {e}, creating new one{Style.RESET_ALL}")
        
        return {
            "questions": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "total_learned": 0,
            }
        }

    def find_similar_question(self, question: str, threshold: float = 0.7) -> Optional[Dict]:
        """
        Find similar question in repo using simple string matching.
        Returns the stored answer if found, None otherwise.
        """
        q_lower = question.lower()
        
        for q_data in self.data.get("questions", []):
            stored_q = q_data.get("question", "").lower()
            
            # Check exact match or partial match
            if q_lower == stored_q:
                return q_data
            
            # Check if key parts match (for variations of same question)
            q_tokens = set(q_lower.split())
            stored_tokens = set(stored_q.split())
            if len(q_tokens & stored_tokens) / max(len(q_tokens | stored_tokens), 1) > threshold:
                return q_data

        return None

    def add_question(self, question: str, answer: str, question_type: str = "text"):
        """Add new question-answer pair to repository."""
        q_data = {
            "question": question,
            "answer": answer,
            "type": question_type,
            "timestamp": datetime.now().isoformat(),
            "usage_count": 0
        }
        self.data["questions"].append(q_data)
        self.save()
        print(f"  {Fore.GREEN}✓ Question saved to repository{Style.RESET_ALL}")

    def record_usage(self, question: str):
        """Track when an answer was used."""
        for q_data in self.data.get("questions", []):
            if q_data.get("question", "").lower() == question.lower():
                q_data["usage_count"] = q_data.get("usage_count", 0) + 1
                self.save()
                break

    def save(self):
        """Save repository to file."""
        self.data["metadata"]["updated"] = datetime.now().isoformat()
        try:
            with open(self.repo_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"  {Fore.RED}  Error saving repository: {e}{Style.RESET_ALL}")

    def show_stats(self):
        """Display repository statistics."""
        total = len(self.data.get("questions", []))
        if total == 0:
            print(f"  {Fore.YELLOW}Repository is empty{Style.RESET_ALL}")
            return
        
        total_usage = sum(q.get("usage_count", 0) for q in self.data["questions"])
        print(f"\n  {Fore.CYAN}━━ Questions Repository Stats ━━{Style.RESET_ALL}")
        print(f"  Total Q&A pairs: {total}")
        print(f"  Total reused:    {total_usage}")
        print(f"  Learning rate:   {total_usage / max(total, 1):.1f} reuses/question")


# ─── JOB APPLICATION COMPLETER ────────────────────────────────────────────────

class JobApplicationCompleter:
    """
    Open job URLs from application log, handle questions,
    and apply intelligently using Q&A repository.
    """

    def __init__(self, config: dict, questions_repo: QuestionsRepository):
        self.config = config
        self.repo = questions_repo
        self.driver = None
        self.wait = None
        self.jobs_to_complete: List[Dict] = []

    def setup_driver(self):
        """Initialize Selenium WebDriver."""
        opts = Options()
        if self.config["headless"]:
            opts.add_argument("--headless=new")
        
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
        self.wait = WebDriverWait(self.driver, self.config["timeout"])
        print(f"  {Fore.GREEN}✓ Browser started{Style.RESET_ALL}")

    def login(self) -> bool:
        """Login to Naukri."""
        print(f"\n  {Fore.CYAN}► Logging into Naukri...{Style.RESET_ALL}")
        if not self.config.get("email") or not self.config.get("password") or self.config.get("password") == "YOUR_PASSWORD":
             print(f"  {Fore.RED}✗ Please set your email and password in CONFIG{Style.RESET_ALL}")
             return False

        try:
            self.driver.get("https://www.naukri.com/nlogin/login")
            self.human_delay(2, 4)

            # Email
            email_field = None
            email_selectors = [
                (By.ID, "usernameField"),
                (By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"),
                (By.XPATH, "//input[@placeholder='Email']"),
                (By.NAME, "usernameField"),
                (By.CSS_SELECTOR, "input[type='text'][placeholder*='Email']"),
                (By.CSS_SELECTOR, "input[data-qa-id='email']"),
            ]

            for selector_type, selector_value in email_selectors:
                try:
                    email_field = self.wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                    break
                except TimeoutException:
                    continue
                except Exception:
                    continue

            if not email_field:
                print(f"  {Fore.YELLOW}  Email field not found, trying scroll...{Style.RESET_ALL}")
                self.driver.execute_script("window.scrollTo(0, 0);")
                self.human_delay(1, 2)
                try:
                    email_field = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")),
                        timeout=10
                    )
                except TimeoutException:
                    raise

            email_field.clear()
            for char in self.config["email"]:
                email_field.send_keys(char)
                time.sleep(random.uniform(0.03, 0.12))
            
            self.human_delay(0.5, 1.2)

            # Password
            pwd_field = None
            pwd_selectors = [
                (By.ID, "passwordField"),
                (By.XPATH, "//input[@placeholder='Enter your password']"),
                (By.XPATH, "//input[@placeholder='Password']"),
                (By.NAME, "passwordField"),
                (By.CSS_SELECTOR, "input[type='password']"),
            ]

            for selector_type, selector_value in pwd_selectors:
                try:
                    pwd_field = self.driver.find_element(selector_type, selector_value)
                    break
                except NoSuchElementException:
                    continue

            if not pwd_field:
                raise NoSuchElementException("Password field not found")

            pwd_field.clear()
            for char in self.config["password"]:
                pwd_field.send_keys(char)
                time.sleep(random.uniform(0.03, 0.12))

            self.human_delay(0.8, 1.5)

            # Login Button
            login_btn = None
            login_selectors = [
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//button[contains(text(),'Login')]"),
                (By.ID, "loginButton"),
            ]

            for selector_type, selector_value in login_selectors:
                try:
                    login_btn = self.driver.find_element(selector_type, selector_value)
                    break
                except NoSuchElementException:
                    continue

            if not login_btn:
                raise NoSuchElementException("Login button not found")

            login_btn.click()
            self.human_delay(3, 5)

            try:
                WebDriverWait(self.driver, 20).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                self.human_delay(2, 3)
            except TimeoutException:
                pass

            self._handle_profile_questionnaire()

            current_url = self.driver.current_url.lower()
            if ("login" not in current_url or "myapps" in current_url or 
                "myjobs" in current_url or "my-profile" in current_url or
                "dashboard" in current_url):
                print(f"  {Fore.GREEN}✓ Logged in successfully{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.RED}✗ Login may have failed — URL: {current_url}{Style.RESET_ALL}")
                return False

        except Exception as e:
            print(f"  {Fore.RED}✗ Login error: {str(e)}{Style.RESET_ALL}")
            return False

    def _handle_profile_questionnaire(self):
        """Close profile questionnaire modals if they appear."""
        try:
            time.sleep(2)
            close_selectors = [
                (By.XPATH, "//button[@aria-label='Close']"),
                (By.XPATH, "//button[contains(text(),'Skip')]"),
                (By.XPATH, "//button[contains(text(),'Later')]"),
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
                        self.human_delay(1, 2)
                        return
                except (NoSuchElementException, ElementClickInterceptedException):
                    continue
                except Exception:
                    continue
        except Exception:
            pass

    def read_application_log(self) -> List[Dict]:
        """Read job URLs from application log CSV."""
        jobs = []
        try:
            with open(self.config["log_file"], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Only process jobs that are pending or failed
                    if row.get("status") in ["pending", "failed"]:
                        jobs.append(row)
            
            print(f"  {Fore.WHITE}Found {len(jobs)} jobs to complete{Style.RESET_ALL}")
            return jobs
        except Exception as e:
            print(f"  {Fore.RED}Error reading log: {e}{Style.RESET_ALL}")
            return []

    def human_delay(self, min_s: float = 1.0, max_s: float = 3.0):
        """Random delay to mimic human behavior."""
        time.sleep(random.uniform(min_s, max_s))

    def close_modals(self):
        """Close any visible modals/popups."""
        try:
            close_selectors = [
                (By.XPATH, "//button[@aria-label='Close']"),
                (By.XPATH, "//button[contains(text(),'Close')]"),
                (By.XPATH, "//span[contains(@class,'close')]"),
                (By.CSS_SELECTOR, "button.close"),
            ]
            
            for selector_type, selector_value in close_selectors:
                try:
                    btn = self.driver.find_element(selector_type, selector_value)
                    if btn.is_displayed():
                        btn.click()
                        self.human_delay(0.5, 1)
                        return
                except (NoSuchElementException, ElementClickInterceptedException):
                    continue
        except Exception:
            pass

    def find_form_fields(self) -> List[Tuple[str, str]]:
        """
        Detect all form fields on the page.
        Returns list of (label_or_placeholder, field_id_or_selector)
        """
        fields = []
        try:
            # Find text inputs
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for inp in inputs:
                inp_type = inp.get_attribute("type") or "text"
                if inp_type in ["text", "email", "number", "tel"]:
                    label = (inp.get_attribute("placeholder") or 
                            inp.get_attribute("aria-label") or 
                            inp.get_attribute("name") or "Unknown field")
                    fields.append(("input", label, inp))

            # Find textareas
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            for ta in textareas:
                label = (ta.get_attribute("placeholder") or 
                        ta.get_attribute("aria-label") or 
                        ta.get_attribute("name") or "Description")
                fields.append(("textarea", label, ta))

            # Find select dropdowns
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            for sel in selects:
                label = (sel.get_attribute("aria-label") or 
                        sel.get_attribute("name") or "Dropdown")
                fields.append(("select", label, sel))

            # Find radios/checkboxes within labels
            labels = self.driver.find_elements(By.TAG_NAME, "label")
            for label_el in labels[:10]:  # Limit to first 10 to avoid spam
                label_text = label_el.text.strip()
                if label_text and len(label_text) < 100:
                    fields.append(("label", label_text, label_el))

            return fields
        except Exception as e:
            print(f"  {Fore.YELLOW}  Error detecting fields: {str(e)[:50]}{Style.RESET_ALL}")
            return []

    def handle_question(self, field_type: str, field_label: str, field_element) -> bool:
        """
        Handle a single form field/question intelligently.
        Returns True if successfully filled.
        """
        try:
            # Clean up field label
            question = field_label.strip()
            if not question:
                return False

            print(f"\n  {Fore.CYAN}  ? {question[:60]}{Style.RESET_ALL}")

            # Check if we have an answer in repository
            stored_answer = self.repo.find_similar_question(question)
            
            if stored_answer:
                print(f"  {Fore.GREEN}  ✓ Found in repository: {stored_answer['answer'][:50]}{Style.RESET_ALL}")
                answer = stored_answer["answer"]
                self.repo.record_usage(question)
            else:
                # Ask user for answer
                print(f"  {Fore.YELLOW}  New question! Please provide answer:{Style.RESET_ALL}")
                answer = input(f"  {Fore.WHITE}  Answer: {Style.RESET_ALL}").strip()
                
                if not answer:
                    print(f"  {Fore.YELLOW}  Skipped{Style.RESET_ALL}")
                    return False
                
                # Save to repository
                self.repo.add_question(question, answer, field_type)

            # Fill the field based on type
            if field_type in ["input", "textarea"]:
                field_element.clear()
                self.human_delay(0.2, 0.5)
                for char in answer:
                    field_element.send_keys(char)
                    time.sleep(random.uniform(0.01, 0.05))
                return True

            elif field_type == "select":
                try:
                    select = Select(field_element)
                    # Try to select by visible text
                    select.select_by_visible_text(answer)
                    return True
                except Exception:
                    # Try by value
                    try:
                        select.select_by_value(answer)
                        return True
                    except Exception:
                        print(f"  {Fore.YELLOW}  Could not select option: {answer}{Style.RESET_ALL}")
                        return False

            elif field_type == "label":
                # Try to click the label
                field_element.click()
                self.human_delay(0.3, 0.7)
                return True

            return False

        except StaleElementReferenceException:
            print(f"  {Fore.YELLOW}  Field became stale, skipping{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}  Error filling field: {str(e)[:50]}{Style.RESET_ALL}")
            return False

    def apply_to_job(self, job: Dict) -> bool:
        """
        Open job URL, detect & answer questions, and submit application.
        """
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")

        if not url:
            print(f"  {Fore.RED}✗ No URL for job{Style.RESET_ALL}")
            return False

        print(f"\n  {Fore.CYAN}► {title} @ {company}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Opening: {url[:70]}...{Style.RESET_ALL}")

        try:
            self.driver.get(url)
            self.human_delay(2, 4)
            self.close_modals()

            # Find form fields
            fields = self.find_form_fields()
            
            if not fields:
                print(f"  {Fore.YELLOW}  No form fields detected{Style.RESET_ALL}")
                return False

            print(f"  {Fore.WHITE}  Found {len(fields)} form fields{Style.RESET_ALL}")

            # Handle each field
            filled_count = 0
            for field_type, field_label, field_element in fields:
                try:
                    # Re-locate element to ensure it's still valid
                    field_element = self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, field_element.tag_name))
                    )
                except Exception:
                    continue

                if self.handle_question(field_type, field_label, field_element):
                    filled_count += 1
                    self.human_delay(0.5, 1.5)

            print(f"  {Fore.GREEN}  ✓ Filled {filled_count}/{len(fields)} fields{Style.RESET_ALL}")

            # Try to find and click submit button
            submit_btn = None
            submit_selectors = [
                (By.XPATH, "//button[contains(text(),'Submit')]"),
                (By.XPATH, "//button[contains(text(),'Apply')]"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            for selector_type, selector_value in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(selector_type, selector_value)
                    if submit_btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if submit_btn:
                print(f"  {Fore.WHITE}  Clicking submit button...{Style.RESET_ALL}")
                submit_btn.click()
                self.human_delay(2, 4)
                print(f"  {Fore.GREEN}✓ Application submitted!{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.YELLOW}  Submit button not found{Style.RESET_ALL}")
                return False

        except TimeoutException:
            print(f"  {Fore.RED}✗ Job page timeout{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Error: {str(e)[:80]}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main workflow."""
        print(f"\n{Fore.CYAN}{'='*65}")
        print(f"  Naukri Job Application Completer")
        print(f"{'='*65}{Style.RESET_ALL}\n")

        # Load questions repository
        self.repo.show_stats()

        # Setup browser
        self.setup_driver()

        try:
            # Read application log
            print(f"\n{Fore.CYAN}► Reading application log...{Style.RESET_ALL}")
            self.jobs_to_complete = self.read_application_log()

            if not self.jobs_to_complete:
                print(f"  {Fore.YELLOW}No pending jobs to complete.{Style.RESET_ALL}")
                return

            # Process each job
            print(f"\n{Fore.CYAN}► Processing {len(self.jobs_to_complete)} jobs...{Style.RESET_ALL}")
            success_count = 0

            for i, job in enumerate(self.jobs_to_complete, 1):
                print(f"\n  {Fore.MAGENTA}[{i}/{len(self.jobs_to_complete)}]{Style.RESET_ALL}")
                
                if self.apply_to_job(job):
                    success_count += 1

                # Delay between jobs
                if i < len(self.jobs_to_complete):
                    min_d, max_d = self.config["delay_between_jobs"]
                    delay = random.uniform(min_d, max_d)
                    print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                    time.sleep(delay)

            # Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  COMPLETION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Total processed: {len(self.jobs_to_complete)}")
            print(f"  Successful:      {Fore.GREEN}{success_count}{Style.RESET_ALL}")
            print(f"  Failed:          {Fore.YELLOW}{len(self.jobs_to_complete) - success_count}{Style.RESET_ALL}")

            # Final repo stats
            print()
            self.repo.show_stats()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize questions repository
    repo = QuestionsRepository(CONFIG["questions_repo_file"])

    # Run completer
    completer = JobApplicationCompleter(CONFIG, repo)
    completer.run()
    def apply_to_job(self, job: Dict) -> bool:
        """
        Open job URL, detect & answer questions, and submit application.
        """
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")

        if not url:
            print(f"  {Fore.RED}✗ No URL for job{Style.RESET_ALL}")
            return False

        print(f"\n  {Fore.CYAN}► {title} @ {company}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Opening: {url[:70]}...{Style.RESET_ALL}")

        try:
            self.driver.get(url)
            self.human_delay(2, 4)
            self.close_modals()

            # Find form fields
            fields = self.find_form_fields()
            
            if not fields:
                print(f"  {Fore.YELLOW}  No form fields detected{Style.RESET_ALL}")
                return False

            print(f"  {Fore.WHITE}  Found {len(fields)} form fields{Style.RESET_ALL}")

            # Handle each field
            filled_count = 0
            for field_type, field_label, field_element in fields:
                try:
                    # Re-locate element to ensure it's still valid
                    field_element = self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, field_element.tag_name))
                    )
                except Exception:
                    continue

                if self.handle_question(field_type, field_label, field_element):
                    filled_count += 1
                    self.human_delay(0.5, 1.5)

            print(f"  {Fore.GREEN}  ✓ Filled {filled_count}/{len(fields)} fields{Style.RESET_ALL}")

            # Try to find and click submit button
            submit_btn = None
            submit_selectors = [
                (By.XPATH, "//button[contains(text(),'Submit')]"),
                (By.XPATH, "//button[contains(text(),'Apply')]"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            for selector_type, selector_value in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(selector_type, selector_value)
                    if submit_btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if submit_btn:
                print(f"  {Fore.WHITE}  Clicking submit button...{Style.RESET_ALL}")
                submit_btn.click()
                self.human_delay(2, 4)
                print(f"  {Fore.GREEN}✓ Application submitted!{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.YELLOW}  Submit button not found{Style.RESET_ALL}")
                return False

        except TimeoutException:
            print(f"  {Fore.RED}✗ Job page timeout{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Error: {str(e)[:80]}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main workflow."""
        print(f"\n{Fore.CYAN}{'='*65}")
        print(f"  Naukri Job Application Completer")
        print(f"{'='*65}{Style.RESET_ALL}\n")

        # Load questions repository
        self.repo.show_stats()

        # Setup browser
        self.setup_driver()

        try:
            # Read application log
            print(f"\n{Fore.CYAN}► Reading application log...{Style.RESET_ALL}")
            self.jobs_to_complete = self.read_application_log()

            if not self.jobs_to_complete:
                print(f"  {Fore.YELLOW}No pending jobs to complete.{Style.RESET_ALL}")
                return

            # Process each job
            print(f"\n{Fore.CYAN}► Processing {len(self.jobs_to_complete)} jobs...{Style.RESET_ALL}")
            success_count = 0

            for i, job in enumerate(self.jobs_to_complete, 1):
                print(f"\n  {Fore.MAGENTA}[{i}/{len(self.jobs_to_complete)}]{Style.RESET_ALL}")
                
                if self.apply_to_job(job):
                    success_count += 1

                # Delay between jobs
                if i < len(self.jobs_to_complete):
                    min_d, max_d = self.config["delay_between_jobs"]
                    delay = random.uniform(min_d, max_d)
                    print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                    time.sleep(delay)

            # Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  COMPLETION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Total processed: {len(self.jobs_to_complete)}")
            print(f"  Successful:      {Fore.GREEN}{success_count}{Style.RESET_ALL}")
            print(f"  Failed:          {Fore.YELLOW}{len(self.jobs_to_complete) - success_count}{Style.RESET_ALL}")

            # Final repo stats
            print()
            self.repo.show_stats()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize questions repository
    repo = QuestionsRepository(CONFIG["questions_repo_file"])

    # Run completer
    completer = JobApplicationCompleter(CONFIG, repo)
    completer.run()
    def apply_to_job(self, job: Dict) -> bool:
        """
        Open job URL, detect & answer questions, and submit application.
        """
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")

        if not url:
            print(f"  {Fore.RED}✗ No URL for job{Style.RESET_ALL}")
            return False

        print(f"\n  {Fore.CYAN}► {title} @ {company}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Opening: {url[:70]}...{Style.RESET_ALL}")

        try:
            self.driver.get(url)
            self.human_delay(2, 4)
            self.close_modals()

            # Find form fields
            fields = self.find_form_fields()
            
            if not fields:
                print(f"  {Fore.YELLOW}  No form fields detected{Style.RESET_ALL}")
                return False

            print(f"  {Fore.WHITE}  Found {len(fields)} form fields{Style.RESET_ALL}")

            # Handle each field
            filled_count = 0
            for field_type, field_label, field_element in fields:
                try:
                    # Re-locate element to ensure it's still valid
                    field_element = self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, field_element.tag_name))
                    )
                except Exception:
                    continue

                if self.handle_question(field_type, field_label, field_element):
                    filled_count += 1
                    self.human_delay(0.5, 1.5)

            print(f"  {Fore.GREEN}  ✓ Filled {filled_count}/{len(fields)} fields{Style.RESET_ALL}")

            # Try to find and click submit button
            submit_btn = None
            submit_selectors = [
                (By.XPATH, "//button[contains(text(),'Submit')]"),
                (By.XPATH, "//button[contains(text(),'Apply')]"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            for selector_type, selector_value in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(selector_type, selector_value)
                    if submit_btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if submit_btn:
                print(f"  {Fore.WHITE}  Clicking submit button...{Style.RESET_ALL}")
                submit_btn.click()
                self.human_delay(2, 4)
                print(f"  {Fore.GREEN}✓ Application submitted!{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.YELLOW}  Submit button not found{Style.RESET_ALL}")
                return False

        except TimeoutException:
            print(f"  {Fore.RED}✗ Job page timeout{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Error: {str(e)[:80]}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main workflow."""
        print(f"\n{Fore.CYAN}{'='*65}")
        print(f"  Naukri Job Application Completer")
        print(f"{'='*65}{Style.RESET_ALL}\n")

        # Load questions repository
        self.repo.show_stats()

        # Setup browser
        self.setup_driver()

        try:
            # Read application log
            print(f"\n{Fore.CYAN}► Reading application log...{Style.RESET_ALL}")
            self.jobs_to_complete = self.read_application_log()

            if not self.jobs_to_complete:
                print(f"  {Fore.YELLOW}No pending jobs to complete.{Style.RESET_ALL}")
                return

            # Process each job
            print(f"\n{Fore.CYAN}► Processing {len(self.jobs_to_complete)} jobs...{Style.RESET_ALL}")
            success_count = 0

            for i, job in enumerate(self.jobs_to_complete, 1):
                print(f"\n  {Fore.MAGENTA}[{i}/{len(self.jobs_to_complete)}]{Style.RESET_ALL}")
                
                if self.apply_to_job(job):
                    success_count += 1

                # Delay between jobs
                if i < len(self.jobs_to_complete):
                    min_d, max_d = self.config["delay_between_jobs"]
                    delay = random.uniform(min_d, max_d)
                    print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                    time.sleep(delay)

            # Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  COMPLETION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Total processed: {len(self.jobs_to_complete)}")
            print(f"  Successful:      {Fore.GREEN}{success_count}{Style.RESET_ALL}")
            print(f"  Failed:          {Fore.YELLOW}{len(self.jobs_to_complete) - success_count}{Style.RESET_ALL}")

            # Final repo stats
            print()
            self.repo.show_stats()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize questions repository
    repo = QuestionsRepository(CONFIG["questions_repo_file"])

    # Run completer
    completer = JobApplicationCompleter(CONFIG, repo)
    completer.run()
    def apply_to_job(self, job: Dict) -> bool:
        """
        Open job URL, detect & answer questions, and submit application.
        """
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")

        if not url:
            print(f"  {Fore.RED}✗ No URL for job{Style.RESET_ALL}")
            return False

        print(f"\n  {Fore.CYAN}► {title} @ {company}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Opening: {url[:70]}...{Style.RESET_ALL}")

        try:
            self.driver.get(url)
            self.human_delay(2, 4)
            self.close_modals()

            # Find form fields
            fields = self.find_form_fields()
            
            if not fields:
                print(f"  {Fore.YELLOW}  No form fields detected{Style.RESET_ALL}")
                return False

            print(f"  {Fore.WHITE}  Found {len(fields)} form fields{Style.RESET_ALL}")

            # Handle each field
            filled_count = 0
            for field_type, field_label, field_element in fields:
                try:
                    # Re-locate element to ensure it's still valid
                    field_element = self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, field_element.tag_name))
                    )
                except Exception:
                    continue

                if self.handle_question(field_type, field_label, field_element):
                    filled_count += 1
                    self.human_delay(0.5, 1.5)

            print(f"  {Fore.GREEN}  ✓ Filled {filled_count}/{len(fields)} fields{Style.RESET_ALL}")

            # Try to find and click submit button
            submit_btn = None
            submit_selectors = [
                (By.XPATH, "//button[contains(text(),'Submit')]"),
                (By.XPATH, "//button[contains(text(),'Apply')]"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            for selector_type, selector_value in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(selector_type, selector_value)
                    if submit_btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if submit_btn:
                print(f"  {Fore.WHITE}  Clicking submit button...{Style.RESET_ALL}")
                submit_btn.click()
                self.human_delay(2, 4)
                print(f"  {Fore.GREEN}✓ Application submitted!{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.YELLOW}  Submit button not found{Style.RESET_ALL}")
                return False

        except TimeoutException:
            print(f"  {Fore.RED}✗ Job page timeout{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Error: {str(e)[:80]}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main workflow."""
        print(f"\n{Fore.CYAN}{'='*65}")
        print(f"  Naukri Job Application Completer")
        print(f"{'='*65}{Style.RESET_ALL}\n")

        # Load questions repository
        self.repo.show_stats()

        # Setup browser
        self.setup_driver()

        try:
            # Read application log
            print(f"\n{Fore.CYAN}► Reading application log...{Style.RESET_ALL}")
            self.jobs_to_complete = self.read_application_log()

            if not self.jobs_to_complete:
                print(f"  {Fore.YELLOW}No pending jobs to complete.{Style.RESET_ALL}")
                return

            # Process each job
            print(f"\n{Fore.CYAN}► Processing {len(self.jobs_to_complete)} jobs...{Style.RESET_ALL}")
            success_count = 0

            for i, job in enumerate(self.jobs_to_complete, 1):
                print(f"\n  {Fore.MAGENTA}[{i}/{len(self.jobs_to_complete)}]{Style.RESET_ALL}")
                
                if self.apply_to_job(job):
                    success_count += 1

                # Delay between jobs
                if i < len(self.jobs_to_complete):
                    min_d, max_d = self.config["delay_between_jobs"]
                    delay = random.uniform(min_d, max_d)
                    print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                    time.sleep(delay)

            # Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  COMPLETION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Total processed: {len(self.jobs_to_complete)}")
            print(f"  Successful:      {Fore.GREEN}{success_count}{Style.RESET_ALL}")
            print(f"  Failed:          {Fore.YELLOW}{len(self.jobs_to_complete) - success_count}{Style.RESET_ALL}")

            # Final repo stats
            print()
            self.repo.show_stats()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize questions repository
    repo = QuestionsRepository(CONFIG["questions_repo_file"])

    # Run completer
    completer = JobApplicationCompleter(CONFIG, repo)
    completer.run()
    def apply_to_job(self, job: Dict) -> bool:
        """
        Open job URL, detect & answer questions, and submit application.
        """
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")

        if not url:
            print(f"  {Fore.RED}✗ No URL for job{Style.RESET_ALL}")
            return False

        print(f"\n  {Fore.CYAN}► {title} @ {company}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Opening: {url[:70]}...{Style.RESET_ALL}")

        try:
            self.driver.get(url)
            self.human_delay(2, 4)
            self.close_modals()

            # Find form fields
            fields = self.find_form_fields()
            
            if not fields:
                print(f"  {Fore.YELLOW}  No form fields detected{Style.RESET_ALL}")
                return False

            print(f"  {Fore.WHITE}  Found {len(fields)} form fields{Style.RESET_ALL}")

            # Handle each field
            filled_count = 0
            for field_type, field_label, field_element in fields:
                try:
                    # Re-locate element to ensure it's still valid
                    field_element = self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, field_element.tag_name))
                    )
                except Exception:
                    continue

                if self.handle_question(field_type, field_label, field_element):
                    filled_count += 1
                    self.human_delay(0.5, 1.5)

            print(f"  {Fore.GREEN}  ✓ Filled {filled_count}/{len(fields)} fields{Style.RESET_ALL}")

            # Try to find and click submit button
            submit_btn = None
            submit_selectors = [
                (By.XPATH, "//button[contains(text(),'Submit')]"),
                (By.XPATH, "//button[contains(text(),'Apply')]"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            for selector_type, selector_value in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(selector_type, selector_value)
                    if submit_btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if submit_btn:
                print(f"  {Fore.WHITE}  Clicking submit button...{Style.RESET_ALL}")
                submit_btn.click()
                self.human_delay(2, 4)
                print(f"  {Fore.GREEN}✓ Application submitted!{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.YELLOW}  Submit button not found{Style.RESET_ALL}")
                return False

        except TimeoutException:
            print(f"  {Fore.RED}✗ Job page timeout{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Error: {str(e)[:80]}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main workflow."""
        print(f"\n{Fore.CYAN}{'='*65}")
        print(f"  Naukri Job Application Completer")
        print(f"{'='*65}{Style.RESET_ALL}\n")

        # Load questions repository
        self.repo.show_stats()

        # Setup browser
        self.setup_driver()

        try:
            # Read application log
            print(f"\n{Fore.CYAN}► Reading application log...{Style.RESET_ALL}")
            self.jobs_to_complete = self.read_application_log()

            if not self.jobs_to_complete:
                print(f"  {Fore.YELLOW}No pending jobs to complete.{Style.RESET_ALL}")
                return

            # Process each job
            print(f"\n{Fore.CYAN}► Processing {len(self.jobs_to_complete)} jobs...{Style.RESET_ALL}")
            success_count = 0

            for i, job in enumerate(self.jobs_to_complete, 1):
                print(f"\n  {Fore.MAGENTA}[{i}/{len(self.jobs_to_complete)}]{Style.RESET_ALL}")
                
                if self.apply_to_job(job):
                    success_count += 1

                # Delay between jobs
                if i < len(self.jobs_to_complete):
                    min_d, max_d = self.config["delay_between_jobs"]
                    delay = random.uniform(min_d, max_d)
                    print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                    time.sleep(delay)

            # Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  COMPLETION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Total processed: {len(self.jobs_to_complete)}")
            print(f"  Successful:      {Fore.GREEN}{success_count}{Style.RESET_ALL}")
            print(f"  Failed:          {Fore.YELLOW}{len(self.jobs_to_complete) - success_count}{Style.RESET_ALL}")

            # Final repo stats
            print()
            self.repo.show_stats()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize questions repository
    repo = QuestionsRepository(CONFIG["questions_repo_file"])

    # Run completer
    completer = JobApplicationCompleter(CONFIG, repo)
    completer.run()
    def apply_to_job(self, job: Dict) -> bool:
        """
        Open job URL, detect & answer questions, and submit application.
        """
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")

        if not url:
            print(f"  {Fore.RED}✗ No URL for job{Style.RESET_ALL}")
            return False

        print(f"\n  {Fore.CYAN}► {title} @ {company}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Opening: {url[:70]}...{Style.RESET_ALL}")

        try:
            self.driver.get(url)
            self.human_delay(2, 4)
            self.close_modals()

            # Find form fields
            fields = self.find_form_fields()
            
            if not fields:
                print(f"  {Fore.YELLOW}  No form fields detected{Style.RESET_ALL}")
                return False

            print(f"  {Fore.WHITE}  Found {len(fields)} form fields{Style.RESET_ALL}")

            # Handle each field
            filled_count = 0
            for field_type, field_label, field_element in fields:
                try:
                    # Re-locate element to ensure it's still valid
                    field_element = self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, field_element.tag_name))
                    )
                except Exception:
                    continue

                if self.handle_question(field_type, field_label, field_element):
                    filled_count += 1
                    self.human_delay(0.5, 1.5)

            print(f"  {Fore.GREEN}  ✓ Filled {filled_count}/{len(fields)} fields{Style.RESET_ALL}")

            # Try to find and click submit button
            submit_btn = None
            submit_selectors = [
                (By.XPATH, "//button[contains(text(),'Submit')]"),
                (By.XPATH, "//button[contains(text(),'Apply')]"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            for selector_type, selector_value in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(selector_type, selector_value)
                    if submit_btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if submit_btn:
                print(f"  {Fore.WHITE}  Clicking submit button...{Style.RESET_ALL}")
                submit_btn.click()
                self.human_delay(2, 4)
                print(f"  {Fore.GREEN}✓ Application submitted!{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.YELLOW}  Submit button not found{Style.RESET_ALL}")
                return False

        except TimeoutException:
            print(f"  {Fore.RED}✗ Job page timeout{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Error: {str(e)[:80]}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main workflow."""
        print(f"\n{Fore.CYAN}{'='*65}")
        print(f"  Naukri Job Application Completer")
        print(f"{'='*65}{Style.RESET_ALL}\n")

        # Load questions repository
        self.repo.show_stats()

        # Setup browser
        self.setup_driver()

        try:
            # Read application log
            print(f"\n{Fore.CYAN}► Reading application log...{Style.RESET_ALL}")
            self.jobs_to_complete = self.read_application_log()

            if not self.jobs_to_complete:
                print(f"  {Fore.YELLOW}No pending jobs to complete.{Style.RESET_ALL}")
                return

            # Process each job
            print(f"\n{Fore.CYAN}► Processing {len(self.jobs_to_complete)} jobs...{Style.RESET_ALL}")
            success_count = 0

            for i, job in enumerate(self.jobs_to_complete, 1):
                print(f"\n  {Fore.MAGENTA}[{i}/{len(self.jobs_to_complete)}]{Style.RESET_ALL}")
                
                if self.apply_to_job(job):
                    success_count += 1

                # Delay between jobs
                if i < len(self.jobs_to_complete):
                    min_d, max_d = self.config["delay_between_jobs"]
                    delay = random.uniform(min_d, max_d)
                    print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                    time.sleep(delay)

            # Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  COMPLETION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Total processed: {len(self.jobs_to_complete)}")
            print(f"  Successful:      {Fore.GREEN}{success_count}{Style.RESET_ALL}")
            print(f"  Failed:          {Fore.YELLOW}{len(self.jobs_to_complete) - success_count}{Style.RESET_ALL}")

            # Final repo stats
            print()
            self.repo.show_stats()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize questions repository
    repo = QuestionsRepository(CONFIG["questions_repo_file"])

    # Run completer
    completer = JobApplicationCompleter(CONFIG, repo)
    completer.run()
    def apply_to_job(self, job: Dict) -> bool:
        """
        Open job URL, detect & answer questions, and submit application.
        """
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")

        if not url:
            print(f"  {Fore.RED}✗ No URL for job{Style.RESET_ALL}")
            return False

        print(f"\n  {Fore.CYAN}► {title} @ {company}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Opening: {url[:70]}...{Style.RESET_ALL}")

        try:
            self.driver.get(url)
            self.human_delay(2, 4)
            self.close_modals()

            # Find form fields
            fields = self.find_form_fields()
            
            if not fields:
                print(f"  {Fore.YELLOW}  No form fields detected{Style.RESET_ALL}")
                return False

            print(f"  {Fore.WHITE}  Found {len(fields)} form fields{Style.RESET_ALL}")

            # Handle each field
            filled_count = 0
            for field_type, field_label, field_element in fields:
                try:
                    # Re-locate element to ensure it's still valid
                    field_element = self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, field_element.tag_name))
                    )
                except Exception:
                    continue

                if self.handle_question(field_type, field_label, field_element):
                    filled_count += 1
                    self.human_delay(0.5, 1.5)

            print(f"  {Fore.GREEN}  ✓ Filled {filled_count}/{len(fields)} fields{Style.RESET_ALL}")

            # Try to find and click submit button
            submit_btn = None
            submit_selectors = [
                (By.XPATH, "//button[contains(text(),'Submit')]"),
                (By.XPATH, "//button[contains(text(),'Apply')]"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            for selector_type, selector_value in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(selector_type, selector_value)
                    if submit_btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if submit_btn:
                print(f"  {Fore.WHITE}  Clicking submit button...{Style.RESET_ALL}")
                submit_btn.click()
                self.human_delay(2, 4)
                print(f"  {Fore.GREEN}✓ Application submitted!{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.YELLOW}  Submit button not found{Style.RESET_ALL}")
                return False

        except TimeoutException:
            print(f"  {Fore.RED}✗ Job page timeout{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Error: {str(e)[:80]}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main workflow."""
        print(f"\n{Fore.CYAN}{'='*65}")
        print(f"  Naukri Job Application Completer")
        print(f"{'='*65}{Style.RESET_ALL}\n")

        # Load questions repository
        self.repo.show_stats()

        # Setup browser
        self.setup_driver()

        try:
            # Read application log
            print(f"\n{Fore.CYAN}► Reading application log...{Style.RESET_ALL}")
            self.jobs_to_complete = self.read_application_log()

            if not self.jobs_to_complete:
                print(f"  {Fore.YELLOW}No pending jobs to complete.{Style.RESET_ALL}")
                return

            # Process each job
            print(f"\n{Fore.CYAN}► Processing {len(self.jobs_to_complete)} jobs...{Style.RESET_ALL}")
            success_count = 0

            for i, job in enumerate(self.jobs_to_complete, 1):
                print(f"\n  {Fore.MAGENTA}[{i}/{len(self.jobs_to_complete)}]{Style.RESET_ALL}")
                
                if self.apply_to_job(job):
                    success_count += 1

                # Delay between jobs
                if i < len(self.jobs_to_complete):
                    min_d, max_d = self.config["delay_between_jobs"]
                    delay = random.uniform(min_d, max_d)
                    print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                    time.sleep(delay)

            # Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  COMPLETION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Total processed: {len(self.jobs_to_complete)}")
            print(f"  Successful:      {Fore.GREEN}{success_count}{Style.RESET_ALL}")
            print(f"  Failed:          {Fore.YELLOW}{len(self.jobs_to_complete) - success_count}{Style.RESET_ALL}")

            # Final repo stats
            print()
            self.repo.show_stats()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize questions repository
    repo = QuestionsRepository(CONFIG["questions_repo_file"])

    # Run completer
    completer = JobApplicationCompleter(CONFIG, repo)
    completer.run()
    def apply_to_job(self, job: Dict) -> bool:
        """
        Open job URL, detect & answer questions, and submit application.
        """
        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")
        url = job.get("url", "")

        if not url:
            print(f"  {Fore.RED}✗ No URL for job{Style.RESET_ALL}")
            return False

        print(f"\n  {Fore.CYAN}► {title} @ {company}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  Opening: {url[:70]}...{Style.RESET_ALL}")

        try:
            self.driver.get(url)
            self.human_delay(2, 4)
            self.close_modals()

            # Find form fields
            fields = self.find_form_fields()
            
            if not fields:
                print(f"  {Fore.YELLOW}  No form fields detected{Style.RESET_ALL}")
                return False

            print(f"  {Fore.WHITE}  Found {len(fields)} form fields{Style.RESET_ALL}")

            # Handle each field
            filled_count = 0
            for field_type, field_label, field_element in fields:
                try:
                    # Re-locate element to ensure it's still valid
                    field_element = self.wait.until(
                        EC.presence_of_element_located((By.TAG_NAME, field_element.tag_name))
                    )
                except Exception:
                    continue

                if self.handle_question(field_type, field_label, field_element):
                    filled_count += 1
                    self.human_delay(0.5, 1.5)

            print(f"  {Fore.GREEN}  ✓ Filled {filled_count}/{len(fields)} fields{Style.RESET_ALL}")

            # Try to find and click submit button
            submit_btn = None
            submit_selectors = [
                (By.XPATH, "//button[contains(text(),'Submit')]"),
                (By.XPATH, "//button[contains(text(),'Apply')]"),
                (By.XPATH, "//button[contains(text(),'Send')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
            ]

            for selector_type, selector_value in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(selector_type, selector_value)
                    if submit_btn.is_displayed():
                        break
                except NoSuchElementException:
                    continue

            if submit_btn:
                print(f"  {Fore.WHITE}  Clicking submit button...{Style.RESET_ALL}")
                submit_btn.click()
                self.human_delay(2, 4)
                print(f"  {Fore.GREEN}✓ Application submitted!{Style.RESET_ALL}")
                return True
            else:
                print(f"  {Fore.YELLOW}  Submit button not found{Style.RESET_ALL}")
                return False

        except TimeoutException:
            print(f"  {Fore.RED}✗ Job page timeout{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗ Error: {str(e)[:80]}{Style.RESET_ALL}")
            return False

    def run(self):
        """Main workflow."""
        print(f"\n{Fore.CYAN}{'='*65}")
        print(f"  Naukri Job Application Completer")
        print(f"{'='*65}{Style.RESET_ALL}\n")

        # Load questions repository
        self.repo.show_stats()

        # Setup browser
        self.setup_driver()

        try:
            # Read application log
            print(f"\n{Fore.CYAN}► Reading application log...{Style.RESET_ALL}")
            self.jobs_to_complete = self.read_application_log()

            if not self.jobs_to_complete:
                print(f"  {Fore.YELLOW}No pending jobs to complete.{Style.RESET_ALL}")
                return

            # Process each job
            print(f"\n{Fore.CYAN}► Processing {len(self.jobs_to_complete)} jobs...{Style.RESET_ALL}")
            success_count = 0

            for i, job in enumerate(self.jobs_to_complete, 1):
                print(f"\n  {Fore.MAGENTA}[{i}/{len(self.jobs_to_complete)}]{Style.RESET_ALL}")
                
                if self.apply_to_job(job):
                    success_count += 1

                # Delay between jobs
                if i < len(self.jobs_to_complete):
                    min_d, max_d = self.config["delay_between_jobs"]
                    delay = random.uniform(min_d, max_d)
                    print(f"  {Fore.WHITE}  Waiting {delay:.0f}s before next...{Style.RESET_ALL}")
                    time.sleep(delay)

            # Summary
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"  COMPLETION SUMMARY")
            print(f"{'='*65}{Style.RESET_ALL}")
            print(f"  Total processed: {len(self.jobs_to_complete)}")
            print(f"  Successful:      {Fore.GREEN}{success_count}{Style.RESET_ALL}")
            print(f"  Failed:          {Fore.YELLOW}{len(self.jobs_to_complete) - success_count}{Style.RESET_ALL}")

            # Final repo stats
            print()
            self.repo.show_stats()

        except KeyboardInterrupt:
            print(f"\n  {Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
        finally:
            if self.driver:
                input(f"\n  {Fore.WHITE}Press Enter to close browser...{Style.RESET_ALL}")
                self.driver.quit()


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize questions repository
    repo = QuestionsRepository(CONFIG["questions_repo_file"])

    # Run completer
    completer = JobApplicationCompleter(CONFIG, repo)
    completer.run()
