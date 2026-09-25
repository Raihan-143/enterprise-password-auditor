#Enterprise Identity & Password Security Auditor

A high-performance Python security tool designed for internal IT auditing and Active Directory compliance. It audits enterprise user password hashes against large breach dictionaries to identify compromised and non-compliant employee credentials.

#Key Features
- **Fast In-Memory Hash Auditing:** Pre-computes dictionary hashes using SHA-256 for rapid lookup.
- **Enterprise Risk Evaluation:** Flags compromised user accounts in real time.
- **Security Health Score:** Automatically calculates corporate compliance percentage.
- **Audit Logging:** Saves comprehensive compliance reports (`password_audit_report.txt`).

##Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/user_name/enterprise-password-auditor.git
   cd enterprise-password-auditor

#Run the auditor
python3 password_auditor.py

#Sample Output
======================================================
     ENTERPRISE IDENTITY & PASSWORD AUDIT             
======================================================
[CRITICAL: COMPROMISED] User: admin           | Weak Password: [Password123]
[CRITICAL: COMPROMISED] User: john_finance    | Weak Password: [superman]
[SECURE: COMPLIANT]     User: alex_cyber      | Status: STRONG
------------------------------------------------------
  AUDIT SUMMARY:
  Total Accounts Audited : 4
  Compromised (Weak)     : 3
  Secure (Compliant)     : 1
  Company Health Score   : 25.0%
------------------------------------------------------

##Author
Md. Raihan Hasan Rana -Cybersecurity Enthusiast
