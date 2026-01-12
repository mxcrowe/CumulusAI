# Claude Code Development Guide for CumulusAI with CCV3

This guide explains how to use Claude Code effectively for developing CumulusAI with Continuous-Claude-V3 (CCV3) support enabled.

## What is Continuous-Claude-V3 (CCV3)?

CCV3 enables Claude to maintain context across multiple tool interactions and extended conversations, allowing for:

- **Persistent context**: Claude remembers previous code analysis and discussions
- **Coherent development sessions**: Multi-step tasks without context loss
- **Iterative refinement**: Claude can revisit and improve previous work
- **Complex reasoning**: Better tracking of dependencies and architecture decisions

## Getting Started with Claude Code

### 1. Install Claude Code CLI

If you haven't already installed Claude Code:

```bash
npm install -g claude-code
```

### 2. Initialize Project with Claude Code

Navigate to the CumulusAI directory and initialize:

```bash
cd G:\Dev\CumulusAI
claude-code init
```

This creates a `.claude` directory for Claude Code settings.

### 3. Activate Virtual Environment

Before running any commands:

```bash
# Windows Command Prompt
cumulusai_env\Scripts\activate

# Or PowerShell
.\cumulusai_env\Scripts\Activate.ps1

# Or Git Bash
source cumulusai_env/Scripts/activate
```

## Development Workflow with CCV3

### Starting a Development Session

```bash
# Start Claude Code in the project directory
claude-code

# You're now in an interactive Claude development session
```

### Task Examples

#### 1. Analyzing the Codebase

```
Ask Claude: "What is the current project structure and what files should we focus on for Phase 2 (database implementation)?"
```

Claude will:
- Explore the directory structure
- Review the implementation plan
- Suggest starting points
- Maintain this context for follow-up questions

#### 2. Implementing Database Layer

```
Ask Claude: "Implement the database.py module for SQLite connection management and CRUD operations"
```

Claude will:
- Read the implementation plan
- Create database.py with full implementation
- Create models.py with dataclasses
- Run tests to verify functionality

#### 3. Building Data Importers

```
Ask Claude: "Create the cumulus_importer.py module to parse dayfile.txt and monthly log files"
```

Claude will:
- Reference the Cumulus file formats
- Create the importer
- Handle edge cases
- Maintain consistency with data models

### Key Commands in Claude Code

- `/help` - Get help with Claude Code features
- `/commit` - Create a git commit with AI-assisted message
- `/review` - Analyze code for issues
- `/test` - Run tests on modified files
- `/plan` - Get architectural planning assistance

## CCV3 Advantages for CumulusAI

### 1. Multi-Phase Implementation

With CCV3, Claude can:
- Remember the full project scope (9 phases, 24 weeks)
- Understand dependencies between phases
- Reference earlier decisions consistently

Example:
```
"Now implement Phase 3 (data calculations) based on the models we created in Phase 2"
```

Claude maintains full context of Phase 2 models and applies them consistently.

### 2. Complex Feature Development

For features requiring multiple components:

```
"Implement the complete API client with WebSocket connection,
auto-reconnect, and REST historical data fetch"
```

Claude can track:
- Data models needed
- Error handling requirements
- Connection state management
- Integration with existing code

### 3. Iterative Refinement

Start with a basic implementation, then refine:

```
Session 1: "Create a basic main_window.py with menu structure"
Session 2: "Now add the dashboard layout with status bar and menu bar connections"
Session 3: "Implement the real-time update mechanism for current conditions"
```

Each request builds on previous work without losing context.

### 4. Bug Fixes and Debugging

When issues arise, Claude can:
- Reference previous implementation decisions
- Trace through multiple files
- Understand the full data flow

```
"The temperature graph is not updating.
Debug the data flow from API → database → graph widget"
```

## Setting Up CCV3 for Optimal Performance

### 1. Project Configuration

Edit `.claude/settings.local.json`:

```json
{
  "cumulusai": {
    "contextStrategy": "persistent",
    "maxContextLines": 50000,
    "relatedFilesDepth": 3,
    "includeGitHistory": true,
    "phaseTracking": true
  }
}
```

### 2. Development Best Practices with CCV3

#### Keep Related Code Together
Group related files logically (already done in project structure):
```
data/
├── models.py          # Referenced by database.py, importers
├── database.py        # Referenced by importers, GUI
└── importers/        # Reference models and database
```

#### Use Consistent Naming
- `*_importer.py` for data importers
- `*_dialog.py` for GUI dialogs
- `*_widget.py` for custom widgets
- `*_graph.py` for graph implementations

This helps Claude understand patterns and maintain consistency.

#### Write Clear Implementation Plan References
When asking Claude to implement something:

```
"Implement calibration.py according to Phase 7 in the implementation plan,
using the calibration table schema defined in the Database Schema section"
```

More specific references help Claude use context effectively.

#### Document Decision Points
In code comments, note important decisions:

```python
# CCV3 Context: This data structure matches the readings table
# schema defined in CumulusAI_Implementation_Plan.md, section
# "Database Schema - readings table". This ensures consistency
# across all data imports (Cumulus, MDB, API).
@dataclass
class WeatherReading:
    timestamp: datetime
    source: str  # 'cumulus', 'mdb', 'api'
    ...
```

## Typical CCV3 Development Session Flow

### Session 1: Database Implementation (Est. 2 hours)

```
1. Review implementation plan
2. Create database.py with SQLite schema
3. Create models.py with dataclasses
4. Implement CRUD operations
5. Create unit tests
6. Commit changes
```

### Session 2: API Integration (Est. 3 hours)

```
1. Create api_client.py with WebSocket connection
2. Implement REST API for historical data
3. Create data validators
4. Test with real API keys
5. Commit and review
```

### Session 3: First Importer (Est. 2 hours)

```
1. Create base_importer.py abstract class
2. Implement cumulus_importer.py
3. Test with actual Cumulus files
4. Handle edge cases
5. Commit
```

## Handling Long Development Sessions

If your session is cut off or needs continuation:

### Saving Context
```bash
claude-code --save-session cumulus-phase-2
```

### Resuming Later
```bash
claude-code --load-session cumulus-phase-2
```

## Collaboration with CCV3

If multiple developers are working on CumulusAI:

1. **Use feature branches**: Each developer works on a phase
2. **Clear commit messages**: Help other developers understand context
3. **Keep implementation plan updated**: Note completed tasks
4. **Use issue tracking**: Document blockers and decisions

Example commit with full context:

```bash
claude-code /commit -m "Implement Phase 2 database layer

- Created database.py with SQLite schema
- Created models.py with dataclasses for all readings
- Implemented CRUD operations for readings and summaries
- Added connection pooling and backup functionality
- All tests passing, ready for Phase 3 (data importers)

Closes #1
References CumulusAI_Implementation_Plan.md Phase 2"
```

## Tips for Best CCV3 Results

### 1. Be Specific About Context
Instead of: "Fix the import error"

Use: "The cumulus_importer.py is failing to parse dayfile.txt.
The error is in parsing the date field which uses dd/mm/yy format.
Fix the date parsing to handle both dd/mm/yy and dd-mm-yy formats as noted in Appendix D."

### 2. Reference the Implementation Plan
The plan is the source of truth. Always reference it:

```
"Implement calculations.py according to the functions listed
in Phase 3, Week 6 of the implementation plan"
```

### 3. Ask for Architectural Guidance
Claude can help with design decisions:

```
"Should we use the thread pool for data imports or async/await
based on the python-socketio usage in the API client?"
```

### 4. Request Code Reviews
Get Claude's input on implementation quality:

```
"Review database.py for performance issues,
especially the daily summary calculation algorithm"
```

### 5. Ask for Testing Strategies
Claude can suggest comprehensive test coverage:

```
"What test cases should we include for the cumulus_importer
to ensure it handles all edge cases in Appendix A?"
```

## Debugging with CCV3

When bugs occur, provide full context:

```
"The temperature graph widget is showing old data.
Here's what I see:
1. API sends new reading to data.api_client
2. api_client inserts into database
3. gui.graphs.scrolling_graph queries database
4. Graph doesn't update

Debug where the data flow is breaking"
```

Claude maintains context of all these components and can trace the issue.

## Project-Specific Commands

Create shortcuts for common CumulusAI tasks:

### Windows Command Prompt
```batch
@echo off
REM Activate venv and run Claude Code
call cumulusai_env\Scripts\activate
claude-code %*
```

### PowerShell
```powershell
# Activate venv and run Claude Code
.\cumulusai_env\Scripts\Activate.ps1
claude-code @args
```

### Git Bash
```bash
#!/bin/bash
source cumulusai_env/Scripts/activate
claude-code "$@"
```

## Resources

- **Claude Code Documentation**: `/help` in Claude Code
- **Implementation Plan**: `CumulusAI_Implementation_Plan.md`
- **PyQt6 Docs**: https://doc.qt.io/qt-6/
- **PyQtGraph Docs**: https://www.pyqtgraph.org/

## Next Steps

1. **Activate your virtual environment**
2. **Start Claude Code**: `claude-code`
3. **Ask for Phase 2 implementation**: "Start Phase 2: Database Layer Implementation"
4. **Follow Claude's guidance** with CCV3 context maintained throughout

---

**CCV3 is now active for your CumulusAI development!**

You have access to persistent context across all development sessions.
Refer to this guide and the implementation plan for the best results.

Good luck with CumulusAI! 🚀
