#!/usr/bin/env python3.4
import os
from datetime import datetime, timedelta
from collections import defaultdict
import re
import argparse
import sys

def parse_timestamp(timestamp_str):
    try:
        return datetime.strptime(timestamp_str.split('+')[0], '%Y-%m-%dT%H:%M:%S.%f')
    except:
        return None

def parse_log_file(file_path):
    alarms = []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            records = content.split('<FmLogRecord>')
            for record in records:
                if '<Alarm>' in record:
                    try:
                        timestamp_match = re.search(r'<LogTimestamp>(.*?)</LogTimestamp>', record)
                        alarm_match = re.search(r'<Alarm>(.*?)</Alarm>', record)
                        
                        if timestamp_match and alarm_match:
                            timestamp = timestamp_match.group(1)
                            alarm_data = alarm_match.group(1).split(';')
                            
                            timestamp_obj = parse_timestamp(timestamp)
                            if not timestamp_obj:
                                continue

                            if len(alarm_data) < 12:
                                continue
                                
                            alarm_info = {
                                'timestamp': timestamp_obj,
                                'managed_element': alarm_data[2],
                                'specific_problem': alarm_data[8],
                                'severity': alarm_data[7],
                                'alarm_type': alarm_data[10]
                            }
                            alarms.append(alarm_info)
                    except:
                        continue
    except Exception as e:
        sys.stderr.write("Error reading file {0}: {1}\n".format(file_path, str(e)))
    return alarms

def analyze_alarms(log_dir, days=15, severity=None, min_occurrences=3):
    cutoff_date = datetime.now() - timedelta(days=days)
    
    try:
        # Sadece .log uzantılı ve FmAlarmLog içeren dosyaları al
        log_files = [f for f in os.listdir(log_dir) 
                    if f.endswith('.log') and 'FmAlarmLog' in f]
        
        # Dosyaları tarih sırasına göre sırala
        log_files.sort()
        
        # Bulunan dosyaları göster
        sys.stdout.write("\nFound {0} log files to analyze:\n".format(len(log_files)))
        for f in log_files:
            sys.stdout.write("- {0}\n".format(f))
        sys.stdout.write("\nStarting analysis...\n")
        
    except Exception as e:
        sys.stderr.write("Error accessing directory {0}: {1}\n".format(log_dir, str(e)))
        sys.exit(1)
    
    alarm_counts = defaultdict(lambda: {'count': 0, 'first_seen': None, 'last_seen': None, 
                                      'severity': None, 'managed_element': None})
    
    processed_files = 0
    for log_file in log_files:
        file_path = os.path.join(log_dir, log_file)
        alarms = parse_log_file(file_path)
        processed_files += 1
        sys.stdout.write("\rProcessing files: {0}/{1}".format(processed_files, len(log_files)))
        sys.stdout.flush()
        
        for alarm in alarms:
            if alarm['timestamp'] >= cutoff_date:
                if severity and alarm['severity'] != severity:
                    continue
                    
                problem = alarm['specific_problem']
                current_count = alarm_counts[problem]
                current_count['count'] += 1
                current_count['severity'] = alarm['severity']
                current_count['managed_element'] = alarm['managed_element']
                
                if current_count['first_seen'] is None or alarm['timestamp'] < current_count['first_seen']:
                    current_count['first_seen'] = alarm['timestamp']
                if current_count['last_seen'] is None or alarm['timestamp'] > current_count['last_seen']:
                    current_count['last_seen'] = alarm['timestamp']
    
    sys.stdout.write("\n\nAlarm Analysis Report (Last {0} days)\n".format(days))
    sys.stdout.write("=" * 80 + "\n")
    
    found_alarms = False
    for problem, stats in sorted(alarm_counts.items(), key=lambda x: x[1]['count'], reverse=True):
        if stats['count'] > min_occurrences:
            found_alarms = True
            duration = stats['last_seen'] - stats['first_seen']
            days = duration.days
            hours = duration.seconds // 3600
            
            sys.stdout.write("\nProblem: {0}\n".format(problem))
            sys.stdout.write("Managed Element: {0}\n".format(stats['managed_element']))
            sys.stdout.write("Severity: {0}\n".format(stats['severity']))
            sys.stdout.write("Count: {0} occurrences\n".format(stats['count']))
            sys.stdout.write("Duration: {0} days, {1} hours\n".format(days, hours))
            sys.stdout.write("First seen: {0}\n".format(stats['first_seen'].strftime('%Y-%m-%d %H:%M:%S')))
            sys.stdout.write("Last seen: {0}\n".format(stats['last_seen'].strftime('%Y-%m-%d %H:%M:%S')))
            sys.stdout.write("-" * 80 + "\n")
    
    if not found_alarms:
        sys.stdout.write("\nNo alarms found matching the specified criteria.\n")

def main():
    parser = argparse.ArgumentParser(description='Analyze alarm logs for recurring issues.')
    parser.add_argument('--dir', '-d', 
                      default='/storage/no-backup/coremw/var/log/saflog/FaultManagementLog/alarm/',
                      help='Directory containing alarm log files')
    parser.add_argument('--days', '-t', type=int, default=15,
                      help='Number of days to analyze (default: 15)')
    parser.add_argument('--severity', '-s',
                      choices=['MAJOR', 'MINOR', 'WARNING', 'CRITICAL', 'CLEARED'],
                      help='Filter by alarm severity')
    parser.add_argument('--min-count', '-m', type=int, default=3,
                      help='Minimum number of occurrences to display (default: 3)')

    args = parser.parse_args()
    analyze_alarms(args.dir, args.days, args.severity, args.min_count)

if __name__ == "__main__":
    main()
