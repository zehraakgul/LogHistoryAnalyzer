
# Alarm Analyzer Script - STANDALONE

## Overview
This script analyzes alarm logs to identify and report recurring issues in a specified directory. It is particularly useful for understanding alarm trends over a defined period and filtering alarms based on severity and frequency.

## Features
- **Log Parsing:** Extracts and processes alarms from log files.
- **Time-Based Analysis:** Filters alarms within a user-defined timeframe (default: last 15 days).
- **Severity Filtering:** Allows filtering by alarm severity (e.g., MAJOR, CRITICAL, etc.).
- **Frequency Analysis:** Identifies and highlights recurring alarms that exceed a specified occurrence threshold.
- **Detailed Report:** Generates a summary report of alarms, including managed element, severity, first/last occurrence, and duration.

## Requirements
- **Python Version:** Python 3.4 or higher.
- **Access Permissions:** Read access to the log directory containing alarm files.

## Usage
1. **Prepare Environment:**
   - Ensure the script has execution permissions: `chmod +x alarm_analyzer.py`
   - Ensure the directory containing the alarm logs is accessible.

2. **Run the Script:**
   ```bash
   python3 alarm_analyzer.py --dir <path_to_log_directory> [options]
   ```

3. **Options:**
   - `--dir`, `-d`: Specify the directory containing alarm logs (default: `/storage/no-backup/coremw/var/log/saflog/FaultManagementLog/alarm/`).
   - `--days`, `-t`: Define the number of days to analyze (default: 15).
   - `--severity`, `-s`: Filter alarms by severity (`MAJOR`, `MINOR`, `WARNING`, `CRITICAL`, `CLEARED`).
   - `--min-count`, `-m`: Set the minimum number of occurrences to display in the report (default: 3).

4. **Example:**
   ```bash
   python3 alarm_analyzer.py --dir /var/log/alarms --days 30 --severity CRITICAL --min-count 5
   ```

## Output
- The script displays a detailed report in the console, including:
  - Alarm problem description.
  - Managed element associated with the alarm.
  - Severity level.
  - Number of occurrences.
  - Duration (from first to last occurrence).
  - First and last seen timestamps.

## Limitations
- The script assumes a specific log file format; unexpected formats may not be supported.
- Only `.log` files containing "FmAlarmLog" are analyzed.
- Designed for environments where log files are regularly maintained and follow consistent naming conventions.

## Notes
- Review the script outputs critically, especially in non-standard environments.
- Customize the default parameters in the script if necessary for your setup.

## Reporting Issues
If you encounter bugs or issues, please contact:
- **Name:** `Zehra Akgül`
- **Email:** [zehra.akgul@outlook.com.tr](mailto:zehra.akgul@outlook.com.tr)

Your feedback is appreciated to improve this script.
