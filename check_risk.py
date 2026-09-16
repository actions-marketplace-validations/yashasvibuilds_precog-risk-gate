import os
import subprocess
import sys

# 1. Detect threshold (defaults to 60)
threshold = int(os.getenv("PRECOG_THRESHOLD", "60"))

# 2. Extract changed files from git diff
try:
    diff_output = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
    ).decode("utf-8")
    changed_files = [line.strip() for line in diff_output.splitlines() if line.strip()]
except Exception:
    changed_files = []

score = 15
risk_factors = ["Base deployment risk baseline: +15"]

sensitive_files = [f for f in changed_files if any(k in f.lower() for k in ["auth", "secret", "database", "payment", "config"])]
test_files = [f for f in changed_files if any(k in f.lower() for k in ["test", "spec"])]

if sensitive_files:
    score += 30
    risk_factors.append(f"Sensitive paths modified ({', '.join(sensitive_files)}): +30")

if sensitive_files and not test_files:
    score += 25
    risk_factors.append("Critical test debt: No accompanying test files found: +25")

print("==========================================")
print("     PRECOG DEPLOYMENT RISK AUDIT         ")
print("==========================================")
print(f"Changed Files Detected: {changed_files}")
print("\nRisk Factor Breakdown:")
for factor in risk_factors:
    print(f" - {factor}")

print(f"\nFinal Calculated Score: {score}/100")
print(f"Configured Threshold: {threshold}/100")
print("==========================================")

if score >= threshold:
    print("\n❌ HIGH DEPLOYMENT RISK DETECTED! Deployment CANCELLED.")
    print("Action Required: Add corresponding test files or reduce blast radius to proceed.")
    sys.exit(1)
else:
    print("\n✅ LOW DEPLOYMENT RISK. Deployment APPROVED.")
    sys.exit(0)
