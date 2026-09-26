from datetime import datetime
import hashlib

USERS_FILE = "company_users.txt"
WORDLIST_FILE = "audit_wordlist.txt"
REPORT_FILE = "password_audit_report.txt"

#Terminal Colour Code
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

  # Memory-safe: Fitting worker hashes into a small memory footprint (a few kilobytes of RAM).
  user_hashes = {}
  total_users = 0

  with open(USERS_FILE, "r") as uf:
    for line in uf:
      line = line.strip()
      if ":" in line:
        total_users += 1
        uname, uhash = line.split(":", 1)
        user_hashes[uhash] = uname

  target_hashes_set = set(user_hashes.keys())
  cracked_users = {}
  report_lines = [header]

  # Streaming the dictionary line by line (preventing RAM overflow / DoS)
  with open(WORDLIST_FILE, "r", encoding="latin-1") as wf:
    for word in wf:
      clean_word = word.strip()
      w_hash = hashlib.sha256(clean_word.encode()).hexdigest()

      if w_hash in target_hashes_set:
        compromised_user = user_hashes[w_hash]
        if compromised_user not in cracked_users:
          cracked_users[compromised_user] = clean_word
          log = (
              f"[CRITICAL: COMPROMISED] User: {compromised_user:<15} | Weak"
              f" Password: [{clean_word}]"
          )
          print(f"{RED}{log}{RESET}")
          report_lines.append(log + "\n")

  # Identifying those who are safe
  for uhash, uname in user_hashes.items():
    if uname not in cracked_users:
      log = f"[SECURE: COMPLIANT]   User: {uname:<15} | Status: STRONG"
      print(f"{GREEN}{log}{RESET}")
      report_lines.append(log + "\n")

  # Health Score Calculation and Summary
  compromised_count = len(cracked_users)
  secure_count = total_users - compromised_count
  health_score = (
      round((secure_count / total_users) * 100, 2) if total_users > 0 else 0
  )

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

  # Save to the audit file
  with open(REPORT_FILE, "w") as rf:
    rf.writelines(report_lines)
  print(f"{BLUE}[+] Full Audit Report saved to: {REPORT_FILE}{RESET}\n")


if __name__ == "__main__":
  run_password_audit()
