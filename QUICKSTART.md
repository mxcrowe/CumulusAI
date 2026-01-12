# CumulusAI Quick Start Guide

Get up and running with CumulusAI development in 5 minutes.

## 1. Activate Virtual Environment

```bash
# Windows Command Prompt
cumulusai_env\Scripts\activate

# Windows PowerShell
.\cumulusai_env\Scripts\Activate.ps1

# Git Bash / Linux
source cumulusai_env/Scripts/activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Verify Installation

```bash
python -c "import PyQt6; import PyQtGraph; print('✓ Dependencies OK')"
```

## 4. Start the Application

```bash
python main.py
```

You should see the CumulusAI main window with "Coming Soon!" placeholder.

## 5. Run with Claude Code

```bash
claude-code
```

Then ask Claude: "Implement Phase 2: Database Layer Implementation"

## File Structure Quick Reference

```
cumulusai/
├── config/         → Settings, calibration, constants
├── data/           → Database, models, importers, API client
├── gui/            → Main window, dialogs, graphs, widgets
├── export/         → CSV export, NOAA reports
└── utils/          → Logging, alarms, backup
```

## Next Phase: Database Implementation

Start with Phase 2:

1. **Read**: `CumulusAI_Implementation_Plan.md` Phase 2 section
2. **Ask Claude**: "Create database.py with SQLite schema and CRUD operations"
3. **Ask Claude**: "Create models.py with dataclasses for all weather data"
4. **Test**: Run the database tests to verify

## API Key Setup

Before using the API client:

1. Get your API key from the implementation plan
2. Generate Application Key at: https://ambientweather.net/account
3. Add to settings (Phase 7: Configuration)

## Common Commands

```bash
# Activate environment
cumulusai_env\Scripts\activate

# Run tests
python -m pytest

# Run application
python main.py

# Start Claude Code
claude-code

# Git commands
git status
git add .
git commit -m "Your message"
git log --oneline
```

## Key Files

- **`CumulusAI_Implementation_Plan.md`** - Full project specification
- **`CLAUDE_CODE_GUIDE.md`** - Using Claude Code with CCV3
- **`README.md`** - Comprehensive project documentation
- **`main.py`** - Application entry point
- **`requirements.txt`** - Python dependencies

## Troubleshooting

### "ModuleNotFoundError: No module named 'PyQt6'"

```bash
# Activate venv and reinstall
cumulusai_env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Application starts but shows blank window

This is normal! The UI is a placeholder. Once you implement the dashboard components, it will fill in.

### Can't find pyodbc drivers

For accessing .mdb files later, ensure you have Microsoft Access ODBC drivers:

```python
import pyodbc
drivers = [x for x in pyodbc.drivers() if 'Access' in x]
print(drivers)  # Should show at least one driver
```

## Development Workflow

1. **Review**: Read the current phase requirements
2. **Code**: Use Claude Code to implement
3. **Test**: Verify the code works
4. **Commit**: Save progress to git
5. **Next**: Move to next task

## Quick Tips

- **Keep venv activated** during development sessions
- **Reference the implementation plan** when asking Claude for help
- **Use clear commit messages** for tracking progress
- **Test frequently** to catch issues early
- **Use `/commit` in Claude Code** for AI-assisted commit messages

## Resources

- Implementation Plan: `CumulusAI_Implementation_Plan.md`
- Claude Code Guide: `CLAUDE_CODE_GUIDE.md`
- Full README: `README.md`
- PyQt6: https://doc.qt.io/qt-6/
- PyQtGraph: https://www.pyqtgraph.org/

## Current Status

✓ Phase 1 Complete: Project Setup
  - Project structure created
  - Virtual environment configured
  - Dependencies specified
  - Entry point ready

⏭ Phase 2 Ready: Database Implementation
  - Create SQLite schema
  - Implement CRUD operations
  - Add database models

## Next Command

```bash
cumulusai_env\Scripts\activate
claude-code

# Then ask Claude:
# "Implement Phase 2: Database Layer with models.py and database.py"
```

---

Happy coding! 🚀
