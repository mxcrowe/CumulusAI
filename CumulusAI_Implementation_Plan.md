# CumulusAI: Implementation Plan

**Project**: Desktop Weather Station Application Inspired by Cumulus
**Station**: Ambient Weather WS-1002-WiFi (current, but due to retire); Zephyr PWS-1000TD (model 4) (original)
**Platform**: Windows 11
**Language**: Python 3.11+
**Framework**: PyQt6
**Timeline**: 24 weeks (6 months) - or faster...
**Project Folder**:  `G:\Dev\CumulusAI`

---

## Executive Summary

CumulusAI will be a comprehensive desktop weather station application that:
- Imports and unifies historical data from three sources (Cumulus, EasyWeatherIP (HP2000.mdb), AmbientWeather.net API)
- Provides a Cumulus-inspired dashboard with real-time updates, modernized for today's graphics
- Offers scrollable interactive graphs using PyQtGraph
- Generates NOAA reports and allows data export

- Supports calibration, alarms, and web uploads
- Provides data integrity tools and weather diary
- Is future-proofed to transition to the next weather station to replace the WS-1002-WiFi eventually

---
## Data Sources Analysis

### Source 1: Cumulus Historical Data
- **Location**: `G:\Dev\CumulusAI\Legacy\Cumulus-Historical-Data and subfolders \data and \backup`
- **Date Range**: April 2010 - January 2018 (8+ years)
- **Files**:
  - Monthly logs: `Apr10log.txt` through `Jan18log.txt` (90+ files)
  - Daily summary: `dayfile.txt` (677 KB, 54 fields per line)
  - Configuration: `cumulus.ini` (526 lines, all settings including calibration)
- **Status**: Readable, legacy data
- **Priority**: High - primary historical reference

### Source 2: HP2000.mdb Databases
- **Locations**: `G:\Dev\CumulusAI\Legacy\EasyWeatherIP-Historical-Data\HP2000-history.mdb; current version: C:\Users\Public\HP2000\HP2000.mdb`
- **Size**: 108 MB
- **Format**: Microsoft Access Database
- **Date Range**: ~2018-present
- **Status**: Unknown schema, may not be actively updated
- **Priority**: Medium - gap filler for recent data before API
- **Notes**: May need pyodbc to access

### Source 3: AmbientWeather.net API
- **Type**: WebSocket (real-time) + REST API (historical)
- **API Key**: `e3d6d497ca63454c99d8504bd637616c0f16203e5fd14c6db5b05b8505bed9a9`
- **Application Key**: User needs to generate at `ambientweather.net/account`
- **Status**: Connected and functional
- **Priority**: High - live data source
- **Notes**: Can fill gaps in .mdb data if needed

### Data Import Strategy

**Priority Order**: API > MDB > Cumulus

**Conflict Resolution**:
When multiple sources have data for same timestamp:
1. API data takes highest priority (most current, most reliable)
2. If no API data but MDB data exists, use MDB
3. If no API or MDB but Cumulus data exists, use Cumulus
4. For overlapping time ranges:
   - API data: mark as source='api'
   - MDB data: mark as source='mdb', set is_imported=False
   - Cumulus data: mark as source='cumulus', set is_imported=True
5. Daily summaries recalculated from source data

---

## Cumulus Configuration Analysis

From `cumulus.ini` analysis:

### Station Settings
- **Station Type**: Zephyr PWS-1000TD (model 4)
- **Location**: 32.8191666666667° N, -117.240555555556° W
- **Altitude**: 522 feet (159 meters)
- **Data Logger**: Yes (UseDataLogger=1)
- **Log Interval**: 3 minutes
- **Units**: Temperature=1 (°F), Pressure=2 (inHg), Rain=1 (inches), Wind=3 (mph)

### Calibration Settings (All Zeros = Not in Use)
```ini
[Offsets]
PressOffset=0           # Pressure offset: None
TempOffset=0            # Temperature offset: None
HumOffset=0             # Humidity offset: None
WindDirOffset=0         # Wind direction offset: None
InTempOffset=0          # Indoor temperature offset: None
WindSpeedMult=1         # Wind speed multiplier: None
WindGustMult=1          # Wind gust multiplier: None
TempMult=1              # Temperature multiplier: None
HumMult=1               # Humidity multiplier: None
RainMult=1              # Rain multiplier: None
UVOffset=0              # UV offset: None
WetBulbOffset=0         # Wet bulb offset: None
```

**Finding**: No calibration offsets currently configured - will implement but start disabled

---
## EasyWeatherIP + WS-1002-WiFi Configuration and Notes

{Add relevent information here, including settings and offsets for WS-1002-WiFi}

## Online Resources

https://cumuluswiki.org/a/About_Cumulus
https://cumuluswiki.org/a/Original_Cumulus_Wiki
https://cumulus.hosiene.co.uk/
https://github.com/cumulusmx/CumulusMX
https://www.wxforum.net/index.php?topic=48066.0
https://www.weather-display.com/
https://www.weewx.com/
https://www.wxforum.net/index.php?board=111.0
https://ambientweather.com/amws1002array.html
https://ambientweather.com/faqs/question/tags/tag/WS-1002-WIFI/

## Technology Stack

### Core Dependencies
```python
# Primary Framework
PyQt6==6.6.0              # Modern, Windows 11 compatible
PyQtGraph==0.13.3           # Fast, scrollable real-time plotting
pyodbc==4.0.39              # Access .mdb files on Windows
python-socketio[asyncio]    # Async WebSocket handling

# Data Processing
numpy==1.24.3                # Array operations for calculations
pandas==2.0.3                # CSV/DataFrame handling (optional, can use stdlib)

# System
pyinstaller==6.3.0            # Create Windows installer
```

### Python Standard Library Only
- `sqlite3` - Unified database
- `datetime` - Date/time handling
- `math` - Calculations
- `csv` - CSV parsing
- `json` - JSON handling
- `pathlib` - File operations
- `threading` - Background data processing
- `queue` - Thread-safe operations
- `typing` - Type hints
- `dataclasses` - Data classes

---

## Project Structure

```
cumulusai/
├── main.py                          # Application entry point
├── config/
│   ├── __init__.py
│   ├── settings.py               # App settings management
│   ├── calibration.py           # Sensor calibration handling
│   └── constants.py             # Application constants
├── data/
│   ├── __init__.py
│   ├── database.py              # SQLite ORM-style operations
│   ├── models.py                # Data model classes
│   ├── importers/
│   │   ├── __init__.py
│   │   ├── base_importer.py      # Base class for all importers
│   │   ├── cumulus_importer.py  # Parse dayfile.txt & monthly logs
│   │   ├── mdb_importer.py       # Read HP2000.mdb via pyodbc
│   │   └── api_importer.py       # AmbientWeather.net WebSocket/REST
│   ├── api_client.py            # AmbientWeather.net client
│   ├── calculations.py           # Derived values (heat index, wind chill, etc.)
│   └── validators.py           # Data validation & spike removal
├── gui/
│   ├── __init__.py
│   ├── main_window.py          # Main dashboard window
│   ├── dialogs/
│   │   ├── __init__.py
│   │   ├── settings_dialog.py    # Configuration dialogs
│   │   ├── calibration_dialog.py # Calibration editor
│   │   ├── import_dialog.py      # Data import wizard
│   │   └── records_dialog.py    # Records viewing/editing
│   ├── graphs/
│   │   ├── __init__.py
│   │   ├── base_graph.py        # Base graph widget
│   │   ├── scrolling_graph.py   # Scrollable time-series graph
│   │   └── wind_rose.py        # Wind direction rose
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── current_conditions.py # Live conditions display panel
│   │   ├── extremes_panel.py     # Today's highs/lows display
│   │   ├── status_bar.py        # Connection status indicator
│   │   └── tray_icon.py        # System tray icon
│   └── resources/
│       ├── icons/                # UI icons
│       └── styles.qss           # Application stylesheet
├── export/
│   ├── __init__.py
│   ├── csv_export.py            # Export data to CSV
│   ├── noaa_reports.py        # Generate NOAA monthly/annual reports
│   └── web_templates/          # HTML templates for web uploads
├── utils/
│   ├── __init__.py
│   ├── alarms.py               # Alarm system
│   ├── backup.py               # Database backup/restore
│   └── logger.py               # Application logging
└── README.md
```

---

## Database Schema

### Unified SQLite Database

```sql
-- Core readings table - all data from all sources
CREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL UNIQUE,
    source TEXT NOT NULL,  -- 'cumulus', 'mdb', 'api'
    is_imported BOOLEAN DEFAULT 1,  -- False = initial import, True = live update
    
    -- Basic measurements
    temp_indoor REAL,
    humidity_indoor INTEGER,
    temp_outdoor REAL,
    humidity_outdoor INTEGER,
    dew_point REAL,
    pressure REAL,
    wind_speed REAL,
    wind_gust REAL,
    wind_direction INTEGER,
    
    -- Rain
    rain_rate REAL,
    rain_today REAL,
    
    -- Derived values
    wind_chill REAL,
    heat_index REAL,
    feels_like REAL,
    apparent_temp REAL,
    humidex REAL,
    
    -- Solar (if available)
    solar_radiation REAL,
    uv_index REAL,
    
    -- Metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Daily summary - recalculated from readings
CREATE TABLE daily_summary (
    date DATE PRIMARY KEY,
    
    -- Temperature extremes
    temp_min REAL,
    temp_min_time TEXT,
    temp_max REAL,
    temp_max_time TEXT,
    
    -- Pressure extremes
    pressure_min REAL,
    pressure_min_time TEXT,
    pressure_max REAL,
    pressure_max_time TEXT,
    
    -- Wind extremes
    wind_gust_max REAL,
    wind_gust_max_time TEXT,
    wind_avg_max REAL,
    wind_avg_max_time TEXT,
    
    -- Rain
    rain_total REAL,
    rain_rate_max REAL,
    rain_rate_max_time TEXT,
    
    -- Humidity extremes
    humidity_min INTEGER,
    humidity_min_time TEXT,
    humidity_max INTEGER,
    humidity_max_time TEXT,
    
    -- Derived extremes
    heat_index_max REAL,
    heat_index_max_time TEXT,
    wind_chill_min REAL,
    wind_chill_min_time TEXT,
    
    -- Averages
    temp_avg REAL,
    humidity_avg INTEGER,
    
    -- Additional
    wind_run REAL,
    dominant_wind_dir INTEGER
);

-- Monthly summary - aggregated from daily_summary
CREATE TABLE monthly_summary (
    year INTEGER,
    month INTEGER,
    PRIMARY KEY (year, month),
    
    -- All extremes as daily summary
    temp_min REAL, temp_max REAL, temp_avg REAL,
    pressure_min REAL, pressure_max REAL,
    wind_gust_max REAL, wind_avg_max REAL,
    rain_total REAL,
    humidity_min INTEGER, humidity_max INTEGER,
    heat_index_max REAL, wind_chill_min REAL
);

-- Yearly summary - aggregated from monthly_summary
CREATE TABLE yearly_summary (
    year INTEGER PRIMARY KEY,
    
    -- Aggregated values
    temp_min REAL, temp_max REAL, temp_avg REAL,
    pressure_min REAL, pressure_max REAL,
    wind_gust_max REAL, wind_avg_max REAL,
    rain_total REAL,
    humidity_min INTEGER, humidity_max INTEGER
);

-- Settings - application configuration
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Weather diary - daily notes
CREATE TABLE weather_diary (
    date DATE PRIMARY KEY,
    notes TEXT,
    snow_falling BOOLEAN,
    snow_depth REAL,
    snow_lying BOOLEAN,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Calibration - sensor offsets
CREATE TABLE calibration (
    sensor TEXT PRIMARY KEY,  -- 'temp_indoor', 'temp_outdoor', etc.
    offset REAL,
    multiplier REAL DEFAULT 1.0,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Phase 1: Project Setup (Weeks 1-2)

### Week 1: Foundation
- [ ] Create project directory structure
- [ ] Set up Python virtual environment
- [ ] Install dependencies:
  ```bash
  pip install PyQt6 PyQtGraph pyodbc python-socketio[asyncio]
  ```
- [ ] Initialize Git repository (optional but recommended)
- [ ] Create base files: `__init__.py` in each folder
- [ ] Set up application logger (`utils/logger.py`)

### Week 2: Database Layer
- [ ] Implement `database.py` with connection management
- [ ] Create database schema on first run
- [ ] Create `models.py` with dataclasses
- [ ] Implement CRUD operations for all tables
- [ ] Create database backup/restore functionality
- [ ] Write unit tests for database operations

---

## Phase 2: Data Import Engine (Weeks 3-5)

### Week 3: Cumulus Importer
- [ ] Implement `cumulus_importer.py`:
  ```python
  # Key tasks:
  - Parse dayfile.txt (54 fields)
  - Parse monthly logs (MMMyylog.txt files)
  - Handle date formats (dd/mm/yy vs dd-mm-yy)
  - Parse time format (HH:mm)
  - Extract calibration from cumulus.ini
  - Import with source='cumulus'
  - Generate daily summaries during import
  - Progress reporting
  ```

### Week 4: MDB Importer
- [ ] Test pyodbc connection to HP2000.mdb
- [ ] Discover database schema (list tables and columns)
- [ ] Implement `mdb_importer.py`:
  ```python
  # Key tasks:
  - Connect via pyodbc with proper connection string
  - Query all tables
  - Identify readings table and schema
  - Extract readings and daily summaries
  - Import with source='mdb', is_imported=False
  - Handle unknown schema gracefully
  ```

### Week 5: API Importer
- [ ] Generate Application Key at AmbientWeather.net
- [ ] Implement `api_client.py`:
  ```python
  # Key tasks:
  - WebSocket connection using python-socketio
  - Subscribe to device updates
  - Handle connection drops and auto-reconnect
  - REST API client for historical data requests
  - JSON parsing and validation
  - Unit conversions (API may differ from Cumulus)
  ```

### Week 6: Conflict Resolution
- [ ] Implement data merging logic in database layer
- [ ] Create timestamp conflict resolution function
- [ ] Add is_imported flag handling
- [ ] Test import order: Cumulus → MDB → API
- [ ] Create import status reporting

---

## Phase 3: Core Data Processing (Weeks 6-7)

### Week 6: Calculations Module
- [ ] Implement `calculations.py`:
  ```python
  # Key functions:
  def calculate_heat_index(temp_f, humidity_pct):
      # Rothfusz regression (NOAA)
      pass
      
  def calculate_wind_chill(temp_f, wind_mph):
      # North American wind chill formula
      pass
      
  def calculate_dew_point(temp_f, humidity_pct):
      # Magnus formula
      pass
      
  def calculate_apparent_temp(temp_f, humidity_pct, wind_mph):
      # Australian apparent temperature
      pass
      
  def calculate_feels_like(temp_f, humidity_pct, wind_mph):
      # Steadman's apparent temperature
      pass
      
  def calculate_humidex(temp_f, humidity_pct):
      # Canadian humidity discomfort index
      pass
      
  def calculate_degree_days(base_temp, threshold):
      # Heating/cooling degree days
      pass
      
  def calculate_wind_run(readings):
      # Total wind run (distance wind travels)
      pass
  ```

### Week 7: Data Validation
- [ ] Implement `validators.py`:
  ```python
  # Key features:
  - Physical limit checks
  - Spike detection (configurable thresholds)
  - Data type validation
  - Missing value handling
  - Out-of-range warnings
  ```

---

## Phase 4: GUI - Main Dashboard (Weeks 8-10)

### Week 8: Main Window Layout
- [ ] Implement `main_window.py` with PyQt6 QMainWindow
- [ ] Create menu bar
- [ ] Implement `status_bar.py`:
  - Connection status indicator
  - Last update timestamp
  - Active data source indicator

### Week 9: Current Conditions Panel
- [ ] Implement `current_conditions.py` widget:
  - Large temperature display
  - Feels like temperature
  - Humidity
  - Dew point
  - Pressure
  - Wind speed, gust, direction
  - Rain today, rate
  - UV index (if available)
  - Solar radiation (if available)
  - Last update time

### Week 10: Extremes Panel
- [ ] Implement `extremes_panel.py` widget:
  - Today's minimums and maximums
  - With times for each extreme
  - Yesterday's extremes
  - Color-coded indicators (red/blue for high/low)

---

## Phase 5: Scrollable Graphs (Weeks 11-13)

### Week 11: Base Graph Widget
- [ ] Implement `base_graph.py`:
  - PyQtGraph PlotWidget
  - Date range selector (24h, 7d, 30d, 90d, 1y, all)
  - Scroll/zoom with mouse wheel
  - Crosshair cursor showing values
  - Export to PNG/SVG
  - Configurable update interval
  - Multiple series support

### Week 12: Temperature Graph
- [ ] Extend base graph for temperature:
  - Min, Max, Avg lines
  - Configurable colors
  - Unit labels (°F/°C)

### Week 13: Pressure Graph
- [ ] Extend base graph for pressure:
  - Trend line
  - Min/Max indicators

### Week 14: Rain Graph
- [ ] Bar chart for daily rain totals
- [ ] Rain rate overlay

### Week 15: Wind Graph
- [ ] Speed and gust lines
- [ ] Wind rose widget
- [ ] Direction histogram

---

## Phase 6: Records System (Weeks 14-16)

### Week 14: Records Views
- [ ] Implement `records_dialog.py`:
  - Today's Extremes (real-time updates)
  - This Month (monthly summary)
  - This Year (yearly summary)
  - This Period (custom date range)
  - All-Time Records (absolute extremes)
  - Editable fields
  - Add missing dates

### Week 15: NOAA Reports
- [ ] Implement `noaa_reports.py`:
  ```python
  # Key features:
  - Monthly NOAA reports (CLIM81 format)
  - Annual NOAA reports (CLIM81 format)
  - Temperature, humidity, pressure, wind, rain data
  - Standard NOAA layout
  - Export to text file
  ```

### Week 16: Data Export
- [ ] Implement `csv_export.py`:
  - Date range selector
  - Field selection (all vs subset)
  - Configurable delimiter
  - Include/exclude options

---

## Phase 7: Configuration (Weeks 17-19)

### Week 17: Settings Dialogs
- [ ] Implement `settings_dialog.py`:
  ```python
  # Tabs:
  1. Station Settings
     - API key configuration
     - Meteorological day (midnight vs 9am vs 10am DST)
     - Update intervals (real-time, logging, web upload)
     - Units (F/C, inHg/hPa, mph/kph/knots)
     - Data source priorities
  
  2. Calibration
     - Temperature offsets (indoor, outdoor)
     - Humidity adjustments
     - Pressure correction
     - Wind speed/direction adjustments
     - Multipliers for each sensor
  
  3. Display Settings
     - Color schemes (Cumulus-like, dark mode, custom)
     - Graph colors
     - Font sizes
     - Decimal places
  
  4. Alarms
     - High/low temperature thresholds
     - Wind speed alerts
     - Pressure alerts
     - Rain rate alerts
     - Notification method (popup, sound, email)  
  5. Web Upload
     - Import existing FTP settings from cumulus.ini
     - Web services (Weather Underground, PWS Weather, etc.)
     - Template processing intervals
  ```

### Week 18: Calibration Import
- [ ] Import calibration offsets from cumulus.ini
- [ ] Store in calibration table
- [ ] Apply to all data (live and imported)
- [ ] Preserve user settings if none in Cumulus

### Week 19: Import Wizard
- [ ] Step-by-step import wizard:
  - Step 1: Select data sources (Cumulus, MDB, API)
  - Step 2: Configure import options
  - Step 3: Preview import data
  - Step 4: Import with progress bar
  - Step 5: Review and resolve conflicts
  - Step 6: Verify results

---

## Phase 8: Additional Features (Weeks 20-22)

### Week 20: Weather Diary
- [ ] Implement diary editor:
  - Daily notes with rich text
  - Snow tracking (falling, depth, lying)
  - Event logging
  - Export diary with other data

### Week 21: Data Tools
- [ ] Implement `data_tools` module:
  - Edit readings directly
  - Manual data entry
  - Merge data sources
  - Data integrity checks
  - Gap detection and reporting

### Week 22: System Tray
- [ ] Implement `tray_icon.py`:
  - Minimize to tray
  - Tooltip with current conditions
  - Quick actions menu
  - Double-click to restore

---

## Phase 9: Polish & Testing (Weeks 23-24)

### Week 23: Testing
- [ ] Unit tests for all modules
- [ ] Integration tests for importers
- [ ] GUI testing with Qt Test framework
- [ ] Performance testing with large datasets
- [ ] Memory leak detection
- [ ] Error handling and recovery

### Week 24: Final Polish
- [ ] User documentation
- [ ] Help system integrated
- [ ] About dialog with credits
- [ ] Create Windows installer with pyinstaller
- [ ] Add application icon
- [ ] Test on clean Windows 11 install

---

## Minimal Viable Product (MVP)

**Goal**: Get basic dashboard working with real-time data display

**Components Required**:
1. Basic data models and SQLite database
2. AmbientWeather.net API client (WebSocket only for MVP)
3. Simple main window with current conditions display
4. Basic scrolling graph (temperature only)
5. Today's extremes panel
6. Settings dialog (API key, units)

**Estimated Time to MVP**: 4 weeks

**What It Will Do**:
- Connect to your WS-1002-WiFi via API
- Display live data in Cumulus-inspired layout
- Show 24-hour scrolling temperature graph
- Track and display today's highs/lows
- Allow basic configuration

---

## Installation Instructions

### Prerequisites
- Windows 11 (64-bit or 32-bit)
- Python 3.11 or later (download from python.org)

### Setup Commands
```bash
# Create virtual environment
python -m venv cumulusai_env

# Activate environment
# Windows:
cumulusai_env\Scripts\activate
# Or on Git Bash:
source cumulusai_env/Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### requirements.txt
```
PyQt6==6.6.0
PyQtGraph==0.13.3
pyodbc==4.0.39
python-socketio[asyncio]
```

### Creating Windows Installer (Phase 24)
```bash
# Create installer
pyinstaller --windowed --icon=resources/icons/icon.ico --name=CumulusAI .

# Will create dist/cumulusai/ folder with installer
```

---

## Development Workflow

### Starting Out
1. Start with MVP - basic dashboard + API connection
2. Get live data flowing and displaying
3. Add scrolling graph functionality
4. Then implement historical data importers

### Daily Development Cycle
```
1. Review plan for current phase
2. Implement required modules
3. Test components individually
4. Integrate into main application
5. Run full application test
6. Commit with descriptive message
```

### Code Style Guidelines
- Use type hints throughout
- Document all public functions
- Use dataclasses for data models
- Follow PEP 8 naming conventions
- Error handling with try/except
- Logging at info, warning, error levels

---

## Appendix A: Cumulus Field Reference

### Dayfile.txt Fields (54 total)
Based on Cumulus Wiki documentation:

| Field # | Column | Type | Description |
|-----------|--------|------|-------------|
| 1 | Date | Text | dd/mm/yy format |
| 2 | Max Wind Gust | Number | Highest gust (mph) |
| 3 | Gust Direction | Number | Bearing of max gust |
| 4 | Gust Time | Text | HH:mm |
| 5 | Min Temperature | Number | Daily minimum (°F) |
| 6 | Min Temp Time | Text | HH:mm |
| 7 | Max Temperature | Number | Daily maximum (°F) |
| 8 | Max Temp Time | Text | HH:mm |
| 9 | Min Pressure | Number | Daily minimum (inHg) |
| 10 | Min Press Time | Text | HH:mm |
| 11 | Max Pressure | Number | Daily maximum (inHg) |
| 12 | Max Press Time | Text | HH:mm |
| 13 | Max Rain Rate | Number | Maximum rainfall rate (in/hr) |
| 14 | Rain Rate Time | Text | HH:mm |
| 15 | Rain Today | Number | Total rainfall for day (in) |

Plus 39 additional fields for derived values, humidity, wind, solar, UV, etc.

### Monthly Log File Format (MMMyylog.txt)
- Name: `Jan24log.txt`, `Feb24log.txt`, etc.
- One line per log interval (default 3 minutes)
- Fields expand over time (started with 16, up to 30+)
- Contains spot readings and derived values

---

## Appendix B: API Configuration

### AmbientWeather.net API Setup

**WebSocket Endpoint:**
```
wss://rt2.ambientweather.net/?api=1&applicationKey=YOUR_APPLICATION_KEY
```

**Subscribe Command:**
```json
{
  "subscribe": {
    "apiKey": "YOUR_API_KEY",
    "devices": ["YOUR_MAC_ADDRESS"]
  }
}
```

**Getting Your MAC Address:**
1. Log in to AmbientWeather.net
2. Go to your device page
3. MAC address is shown on device details
4. Format: XX:XX:XX:XX:XX:XX

**Generating Application Key:**
1. Log in to AmbientWeather.net
2. Go to Account → API Keys
3. Click "Create Application Key"
4. Copy the generated key

---

## Appendix C: Calibration Data

### From cumulus.ini Analysis
```ini
[Offsets]
PressOffset=0           # inches Hg offset
TempOffset=0            # degrees F offset
HumOffset=0             # percent offset
WindDirOffset=0         # degrees offset
InTempOffset=0          # degrees F offset
WindSpeedMult=1         # multiplier
WindGustMult=1          # multiplier
TempMult=1              # multiplier
HumMult=1               # multiplier
RainMult=1              # multiplier
UVOffset=0              # index offset
WetBulbOffset=0         # degrees F offset
```

**Current Finding**: All offsets are 0 (disabled)

**Calibration Storage in CumulusAI:**
```sql
INSERT INTO calibration (sensor, offset, multiplier) VALUES
('temp_indoor', 0, 1.0);
INSERT INTO calibration (sensor, offset, multiplier) VALUES
('temp_outdoor', 0, 1.0);
INSERT INTO calibration (sensor, offset, multiplier) VALUES
('humidity_indoor', 0, 1.0);
INSERT INTO calibration (sensor, offset, multiplier) VALUES
('humidity_outdoor', 0, 1.0);
INSERT INTO calibration (sensor, offset, multiplier) VALUES
('pressure', 0, 1.0);
INSERT INTO calibration (sensor, offset, multiplier) VALUES
('wind_speed', 0, 1.0);
INSERT INTO calibration (sensor, offset, multiplier) VALUES
('wind_gust', 0, 1.0);
```

---

## Appendix D: Known Issues & Considerations

### MDB File Access
- **Issue**: pyodbc requires ODBC driver to be installed
- **Solution**: Windows includes needed drivers; verify with:
  ```python
  import pyodbc
  drivers = [x for x in pyodbc.drivers() if 'Microsoft Access' in x]
  ```
- **Fallback**: Export from AmbientWeather.net as CSV if .mdb not accessible

### Cumulus Date Format
- **Issue**: Both dd/mm/yy and dd-mm-yy found in Cumulus files
- **Solution**: Support both formats, detect automatically
- **Note**: Dayfile.txt uses dd/mm/yy format

### Data Gaps
- **Issue**: Potential gaps between data sources
- **Solution**: Gap detection and reporting tool
- **Manual Resolution**: Allow users to add missing readings

### Performance Considerations
- **Large Dataset**: 8+ years of historical data (~100K+ readings)
- **Solution**: 
  - Lazy loading of graphs
  - Data pagination in records views
  - Database indexing on frequently queried fields
- **Memory Management**: PyQtGraph handles large datasets efficiently

---

## Revision History

| Version | Date | Changes |
|---------|------|----------|
| 1.0 | 2025-01-10 | Initial implementation plan created |
