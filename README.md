##Enterprise Identity & Password Security Auditor

A high-performance Python security tool designed for internal IT compliance and Active Directory credential auditing. It audits corporate password hashes against breach dictionaries to discover compromised credentials and enforce corporate password security policies.

---

##Key Features
- **Deterministic Identity Auditing:** Rapidly correlates enterprise user database hashes with known threat dictionaries.
- **Corporate Health Scoring:** Automatically computes overall organizational password resilience percentage.
- **Audit Documentation:** Exports structured, actionable reports to `password_audit_report.txt` for CISO/IT management review.
- **Color-Coded CLI Dashboard:** Real-time visual feedback distinguishing compromised accounts (`CRITICAL`) from compliant ones (`SECURE`).

---

##Architectural Hardening: DoS Protection (v1.1 Updates)
In security auditing, wordlists frequently exceed several gigabytes (e.g., massive breach databases). A naive approach of loading millions of hashes into an in-memory dictionary causes severe Out-Of-Memory (OOM) crashes and Denial of Service (DoS).

- **Streaming Inverse Lookup Architecture:** 
  - Instead of loading the dictionary into RAM, the auditor loads corporate employee hashes into an ultra-compact in-memory `set()` (consuming only a few kilobytes of RAM).
  - The dictionary file is read sequentially line-by-line (streaming).
  - **Impact:** Memory consumption dropped by over 95%, allowing the tool to process multi-gigabyte wordlists without crashing production servers.
- **Host-Level Access Control (Least Privilege):** 
  - Auditor binary restricted to owner/admin execution (`chmod 700`).
  - Sensitive employee audit logs secured against local tampering (`chmod 600`).

---

##Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Raihan-143/enterprise-password-auditor.git
   cd enterprise-password-auditor

##Apply OS-level hardening permissions:
chmod 700 password_auditor.py

##Run the auditor
python3 password_auditor.py

##Sample audit output
======================================================
     ENTERPRISE IDENTITY & PASSWORD AUDIT             
     Database : company_users.txt                     
     Time     : 2026-09-26 21:15:00                   
======================================================

[CRITICAL: COMPROMISED] User: admin           | Weak Password: [Password123]
[CRITICAL: COMPROMISED] User: john_finance    | Weak Password: [superman]
[CRITICAL: COMPROMISED] User: sarah_hr        | Weak Password: [admin123]
[SECURE: COMPLIANT]   User: alex_cyber      | Status: STRONG

------------------------------------------------------
  AUDIT SUMMARY:
  Total Accounts Audited : 4
  Compromised (Weak)     : 3
  Secure (Compliant)     : 1
  Company Health Score   : 25.0%
------------------------------------------------------
[+] Full Audit Report saved to: password_audit_report.txt

##Author
Md. Raihan Hasan Rana - Cybersecurity Enthusiast
