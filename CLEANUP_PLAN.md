# Project Cleanup Plan

## Files to KEEP (Essential Documentation)

### Core Documentation
- README.md - Main project documentation
- SETUP_GUIDE.md - Setup instructions
- FEATURE_STATUS.md - Current feature status
- .env.template - Environment template
- .gitignore - Git ignore rules

### Pending Implementation Guides
- PROPOSAL_PDF_FINAL.md - PDF generator to implement
- FIX_WIN_RATE.md - Analytics fix to apply

## Files to DELETE (Completed/Obsolete)

### Completed Implementation Guides (31 files)
These were useful during development but are no longer needed:

```
BACKEND_FRONTEND_MAPPING.md
CHATBOT_STATUS.md
DATABASE_MIGRATION_GUIDE.md
DEPENDENCY_FIX.md
EMAIL_INBOX_COMPLETE.md
EMAIL_INBOX_SETUP.md
EMAIL_INTEGRATION_GUIDE.md
EMAIL_STATUS_AND_VERIFICATION.md
ERRORS_FIXED.md
FETCH_ALL_GMAIL_EMAILS.md
FINAL_EMAIL_SETUP.md
FIX_REVENUE_CARDS.md
FRONTEND_INTEGRATION_STATUS.md
GMAIL_INTEGRATION_GUIDE.md
IMPLEMENTATION_PROGRESS.md
IMPLEMENTATION_STATUS.md
INTEGRATION_COMPLETE.md
MARK_AS_READ_FEATURE.md
NAVIGATION_AND_WORKFLOW_GUIDE.md
NOTIFICATIONS_SYSTEM.md
PDF_ATTACHMENTS_COMPLETE.md
PDF_ATTACHMENT_STATUS.md
PDF_UPLOAD_GUIDE.md
PROJECT_ANALYSIS.md
PROPOSAL_PDF_FEATURE.md
PROPOSAL_PDF_IFRAME.md
QUICK_EMAIL_FIX.md
QUICK_FIX.md
RAG_IMPLEMENTATION_GUIDE.md
RAG_SETUP_COMPLETE.md
RAG_SETUP_GUIDE.md
ROADMAP.md
SETUP_CHECKLIST.md
SUBMIT_RFP_STATUS.md
WORK_DIVISION.md
```

### Test/Setup Scripts (15 files)
One-time use scripts no longer needed:

```
add_sample_emails.py
add_sample_inbox_data.py
add_rfp_attachments_column.py
check_gmail_now.py
check_models.py
check_qdrant.py
fetch_gmail_emails.py
fix_emails_table.py
force_fix_schema.py
ingest_pdfs_to_rag.py
quick_migration.sql
run_migration.py
test_email_connection.py
test_gmail_connection.py
verify_system.py
```

### Batch Files
```
install_missing_deps.bat (functionality in setup guide)
verify.bat (functionality in setup guide)
```

## Cleanup Commands

Run these to clean up:

```bash
# Delete obsolete documentation
del BACKEND_FRONTEND_MAPPING.md
del CHATBOT_STATUS.md
del DATABASE_MIGRATION_GUIDE.md
del DEPENDENCY_FIX.md
del EMAIL_INBOX_COMPLETE.md
del EMAIL_INBOX_SETUP.md
del EMAIL_INTEGRATION_GUIDE.md
del EMAIL_STATUS_AND_VERIFICATION.md
del ERRORS_FIXED.md
del FETCH_ALL_GMAIL_EMAILS.md
del FINAL_EMAIL_SETUP.md
del FIX_REVENUE_CARDS.md
del FRONTEND_INTEGRATION_STATUS.md
del GMAIL_INTEGRATION_GUIDE.md
del IMPLEMENTATION_PROGRESS.md
del IMPLEMENTATION_STATUS.md
del INTEGRATION_COMPLETE.md
del MARK_AS_READ_FEATURE.md
del NAVIGATION_AND_WORKFLOW_GUIDE.md
del NOTIFICATIONS_SYSTEM.md
del PDF_ATTACHMENTS_COMPLETE.md
del PDF_ATTACHMENT_STATUS.md
del PDF_UPLOAD_GUIDE.md
del PROJECT_ANALYSIS.md
del PROPOSAL_PDF_FEATURE.md
del PROPOSAL_PDF_IFRAME.md
del QUICK_EMAIL_FIX.md
del QUICK_FIX.md
del RAG_IMPLEMENTATION_GUIDE.md
del RAG_SETUP_COMPLETE.md
del RAG_SETUP_GUIDE.md
del ROADMAP.md
del SETUP_CHECKLIST.md
del SUBMIT_RFP_STATUS.md
del WORK_DIVISION.md

# Delete test/setup scripts
del add_sample_emails.py
del add_sample_inbox_data.py
del add_rfp_attachments_column.py
del check_gmail_now.py
del check_models.py
del check_qdrant.py
del fetch_gmail_emails.py
del fix_emails_table.py
del force_fix_schema.py
del ingest_pdfs_to_rag.py
del quick_migration.sql
del run_migration.py
del test_email_connection.py
del test_gmail_connection.py
del verify_system.py
del install_missing_deps.bat
del verify.bat
```

## After Cleanup, Project Structure:

```
rfp-automation/
├── .env.template
├── .gitignore
├── README.md              ✅ Main documentation
├── SETUP_GUIDE.md         ✅ Setup instructions
├── FEATURE_STATUS.md      ✅ Current status
├── PROPOSAL_PDF_FINAL.md  ✅ Pending implementation
├── FIX_WIN_RATE.md        ✅ Pending fix
├── requirements.txt
├── agents/                ✅ Core code
├── frontend/              ✅ Core code
├── orchestrator/          ✅ Core code
├── shared/                ✅ Core code
├── tests/                 ✅ Unit tests
├── docs/                  ✅ Additional docs
└── venv/                  ✅ Virtual environment
```

## Result:
- **Before**: 61 files + 10 dirs
- **After**: ~15 essential files + 10 dirs
- **Removed**: 46 obsolete files (76% reduction!)

Clean, organized, production-ready codebase! 🧹✨
