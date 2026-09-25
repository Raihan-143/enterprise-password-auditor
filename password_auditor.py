from datetime import datetime
import hashlib

USERS_FILE = "company_users.txt"
WORDLIST_FILE = "audit_wordlist.txt"
REPORT_FILE = "password_audit_report.txt"

# Terminal Color Code
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def run_password_audit():
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  header = (
      f"\n======================================================\n"
      f"     ENTERPRISE IDENTITY & PASSWORD AUDIT             \n"
      f"     Database : {USERS_FILE}                          \n"
      f"     Time     : {timestamp}                           \n"
      f"======================================================\n"
  )
  print(f"{BLUE}{header}{RESET}")

  # Loading the dictionary words into memory using a hash map beforehand (for super-fast searching).
  dictionary = {}
  with open(WORDLIST_FILE, "r", encoding="latin-1") as wf:
    for word in wf:
      clean_word = word.strip()
      w_hash = hashlib.sha256(clean_word.encode()).hexdigest()
      dictionary[w_hash] = clean_word

  #Now, the accounts of company employees are being audited.
  total_users = 0
  compromised_count = 0
  report_lines = [header]

  with open(USERS_FILE, "r") as uf:
    for line in uf:
      if ":" not in line:
        continue
      total_users += 1
      username, user_hash = line.strip().split(":", 1)

      #Did the hash match the dictionary?া
      if user_hash in dictionary:
        compromised_count += 1
        cracked_pass = dictionary[user_hash]
        log = (
            f"[CRITICAL: COMPROMISED] User: {username:<15} | Weak Password:"
            f" [{cracked_pass}]"
        )
        print(f"{RED}{log}{RESET}")
        report_lines.append(log + "\n")
      else:
        log = f"[SECURE: COMPLIANT]   User: {username:<15} | Status: STRONG"
        print(f"{GREEN}{log}{RESET}")
        report_lines.append(log + "\n")

  # Security Health Score Calculation
  secure_count = total_users - compromised_count
  health_score = round((secure_count / total_users) * 100, 2)

  summary = (
      f"\n------------------------------------------------------\n"
      f"  AUDIT SUMMARY:\n"
      f"  Total Accounts Audited : {total_users}\n"
      f"  Compromised (Weak)     : {compromised_count}\n"
      f"  Secure (Compliant)     : {secure_count}\n"
      f"  Company Health Score   : {health_score}%\n"
      f"------------------------------------------------------\n"
  )

  if health_score < 50:
    print(f"{RED}{summary}{RESET}")
  else:
    print(f"{YELLOW}{summary}{RESET}")

  report_lines.append(summary)

  # Automatically saving to the audit file
  with open(REPORT_FILE, "w") as rf:
    rf.writelines(report_lines)

  print(f"{BLUE}[+] Full Audit Report saved to: {REPORT_FILE}{RESET}\n")


if __name__ == "__main__":
  run_password_audit()
