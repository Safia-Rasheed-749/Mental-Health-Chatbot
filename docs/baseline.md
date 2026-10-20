# 1. Tag exists locally and matches
git rev-parse baseline-pre-fix-20261019
# expect: 58f4ba233589642f6e774e494b33382818b93433

# 2. Tag exists on origin
git ls-remote --tags origin | Select-String baseline
# expect: ... refs/tags/baseline-pre-fix-20261019

# 3. main is clean
git checkout main
git status
# expect: nothing to commit

# 4. baseline doc now reflects reality
Get-Content docs/baseline.md | Select-String "58f4ba23|Done|not created"
# expect: shows "58f4ba23" and "Done"; no "not created"

# 5. local-only-work is safe (no upstream)
git checkout local-only-work
git branch -vv
# expect: local-only-work ... (no [origin/...] bracket)

# 6. Toolchain still works
cd backend
python -m pytest tests/ -q
cd ..
# expect: 24 passed (or current count)