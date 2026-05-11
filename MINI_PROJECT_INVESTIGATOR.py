'''
================================================
    CRIME RECORD INTELLIGENCE SYSTEM 🕵️
    Mini Project — Phase 1 Complete
================================================

PROBLEM STATEMENT:
Build a CLI app that works like a police
intelligence database. Log crimes, track
criminals, detect patterns, and generate
investigation reports like a real detective.

------------------------------------------------
CRIME STRUCTURE:
{
    "id": 1,
    "type": "Robbery",
    "location": "Koregaon Park, Pune",
    "date": "18-04-2026 14:30",
    "status": "open",        # open/investigating/closed
    "suspects": ["Rajan Mehta", "Priya Shah"],
    "description": "Armed robbery at jewellery shop",
    "evidence": ["CCTV footage", "fingerprints"]
}

------------------------------------------------
CRIMINAL STRUCTURE:
{
    "name": "Rajan Mehta",
    "age": 34,
    "danger_level": "high",   # low/medium/high
    "crimes_committed": ["Robbery", "Fraud"],
    "known_associates": ["Priya Shah", "Dev Nair"],
    "status": "wanted"        # wanted/arrested/released
}

------------------------------------------------
MENU:
1.  Log New Crime
2.  Add Criminal Profile
3.  Search Crimes
4.  Search Criminals
5.  View Pattern Analysis
6.  Generate Investigation Report
7.  View Cold Cases  (open cases older than 30 days)
8.  Stats Dashboard
9.  Update Crime Status
10. Exit

------------------------------------------------
RULES:
- No duplicate crime IDs
- Date must not be a future date
- Status must be open / investigating / closed
- Danger level must be low / medium / high
- Suspects stored as a set (no duplicates)
- Evidence stored as a list
- Crimes committed stored as a list
- Known associates stored as a set (no duplicates)
- All data saved to crimes.json and criminals.json
- Reports saved as report_DD-MM-YYYY_HH-MM.txt

------------------------------------------------
DATA STRUCTURES TO USE:
- dict         → crime and criminal structure
- list         → all crimes, all criminals, evidence
- set          → suspects, known associates
- tuple        → use namedtuple for crime location
                 (area, city) e.g. Location("Koregaon Park", "Pune")
- string       → formatting all output
- datetime     → logging date/time, cold case detection
- json         → saving and loading all data
- Counter      → pattern analysis (most common crime,
                 most dangerous location, busiest day)
- deque        → store and display last 5 recent crimes
- defaultdict  → group crimes by type or location
- file handling→ saving investigation reports as .txt

------------------------------------------------
FUNCTIONS TO BUILD:
- load_data()
- save_data()
- log_crime()
- add_criminal()
- search_crimes()         search by location / type / status
- search_criminals()      search by name / danger level
- pattern_analysis()      Counter-based insights
- generate_report()       save full report to .txt file
- view_cold_cases()       open cases older than 30 days
- stats_dashboard()       full stats summary
- update_crime_status()
- main()
- view_recent_crimes()      ← build this now (easiest, 10 lines)
- update_crime_status()     ← find by ID, change status, save
- search_crimes()           ← search by location / type / status
- search_criminals()        ← search by name / danger level
- view_cold_cases()         ← datetime logic
⬜ stats_dashboard()         ← Counter + calculations
⬜ pattern_analysis()        ← Counter + defaultdict + questions
⬜ generate_report()         ← write everything to .txt file
⬜ main()                    ← menu + actions dict, build last
------------------------------------------------
EXPECTED OUTPUT:

--- Stats Dashboard ---
Total crimes logged : 10
Solved (closed)     : 6
Under investigation : 2
Open cases          : 2
Solve rate          : 60.00%
Cold cases          : 1
Most wanted         : Rajan Mehta (6 crimes)
Total criminals     : 5

--- Pattern Analysis ---
Most common crime   : Robbery (4 cases)
Most dangerous area : Koregaon Park (5 crimes)
Busiest day         : Friday
Crimes this month   : 7
Crimes last month   : 4

--- Cold Cases ---
#3 | Robbery | Koregaon Park | Opened: 01-03-2026 | 47 days old

--- Investigation Report ---
Report saved as: report_18-04-2026_14-30.txt

--- Recent Crimes (Last 5) ---
#10 | Fraud       | Baner        | 18-04-2026 | open
#9  | Assault     | Kothrud      | 17-04-2026 | investigating
#8  | Robbery     | Koregaon Park| 15-04-2026 | closed
#7  | Cybercrime  | Hinjewadi    | 12-04-2026 | open
#6  | Robbery     | Viman Nagar  | 10-04-2026 | closed

------------------------------------------------
TOPICS COVERED:
- dict         → crime and criminal structure
- list         → storing all records, evidence
- set          → suspects, known associates
- tuple        → namedtuple for Location
- string       → all formatted output
- datetime     → timestamps, cold case detection
- json         → file persistence
- Counter      → pattern analysis
- deque        → last 5 recent crimes
- defaultdict  → grouping crimes
- file handling→ .txt investigation reports
- error handling→ try/except throughout

------------------------------------------------
DAYS TO BUILD:
Day 1 — Core: log crime, add criminal, save/load
Day 2 — Search, update status, cold cases
Day 3 — Pattern analysis, stats dashboard
Day 4 — Report generation, polish, push to GitHub
'''

from collections import defaultdict, Counter, namedtuple, deque
from datetime import datetime
import json

# ---------- FILE PATHS ----------
CRIMES_FILE = "crimes.json"
CRIMINALS_FILE = "criminals.json"

# ---------- STRUCTURES ----------
Location = namedtuple("Location", ["area", "city"])

crimes = []
criminals = []
recent_crimes = deque(maxlen=5)

# ========== DATA PERSISTENCE ==========

def safe_load(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
        
    except FileNotFoundError:
        return []
    
    except json.JSONDecodeError:
        print(f"⚠️ {file_path} corrupted. Resetting.")
        return []
    
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []


def safe_save_data(file_path, data):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    except OSError as e:
        print(f"File write error: {e}")

    except TypeError as e:
        print(f"Serialization error: {e}")

    except Exception as e:
        print(f"Unexpected error while saving: {e}")


def load_data():
    global crimes, criminals, recent_crimes

    crimes = safe_load(CRIMES_FILE)
    criminals = safe_load(CRIMINALS_FILE)

    recent_crimes = deque(maxlen=5)
    recent_crimes.extend(crimes[-5:])


def serialize_crime(crime):
    loc = crime["location"]
    date = crime["date"]

    return {
        "id": crime["id"],
        "type": crime["type"],
        "location": {
            "area": loc.area if hasattr(loc, "area") else loc["area"],
            "city": loc.city if hasattr(loc, "city") else loc["city"]
        },
        "date": date.isoformat() if isinstance(date, datetime) else date,
        "status": crime["status"],
        "suspects": list(crime["suspects"]),
        "description": crime["description"],
        "evidences": crime["evidences"]
    }


def serialize_criminal(criminal):
    return {
        "name": criminal["name"],
        "age": criminal["age"],
        "danger_level": criminal["danger_level"],
        "crimes_committed": criminal["crimes_committed"],
        "known_associates": list(criminal["known_associates"]),
        "status": criminal["status"]
    }


def save_data():
    processed_crimes = [serialize_crime(c) for c in crimes]
    processed_criminals = [serialize_criminal(c) for c in criminals]

    safe_save_data(CRIMES_FILE, processed_crimes)
    safe_save_data(CRIMINALS_FILE, processed_criminals)


# ========== BUSINESS LOGIC ==========

# ======= LOG CRIME =======
def log_crime():
    global crimes, recent_crimes

    crime_type = input("Enter crime type: ").strip().title()

    if not crime_type:
        print("Crime type cannot be empty.")
        return

    area = input("Enter area: ").strip().title()
    city = input("Enter city: ").strip().title()

    if not area or not city:
        print("Location cannot be empty.")
        return

    location = Location(area, city)

    date_input = input("Enter date (DD/MM/YYYY HH:MM): ").strip()

    try:
        parsed_date = datetime.strptime(date_input, "%d/%m/%Y %H:%M")

    except ValueError:
        print("Invalid date format.")
        return

    if parsed_date > datetime.now():
        print("Future dates not allowed.")
        return

    description = input("Enter description: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    suspects_input = input("Enter suspects (comma separated): ").strip()
    suspects = set(s.strip().title() for s in suspects_input.split(",") if s.strip())

    evidence_input = input("Enter evidence (comma separated): ").strip()
    evidences = [e.strip() for e in evidence_input.split(",") if e.strip()]

    crime_id = max([c["id"] for c in crimes], default=0) + 1

    crime = {
        "id": crime_id,
        "type": crime_type,
        "location": location,
        "date": parsed_date,
        "status": "open",
        "suspects": suspects,
        "description": description,
        "evidences": evidences
    }

    crimes.append(crime)
    recent_crimes.append(crime)
    save_data()

    print(f"✅ Crime #{crime_id} logged.")


# ======= ADD CRIMINAL =======
def add_criminal():
    global criminals

    name = input("Enter name: ").strip().title()

    if not name:
        print("Name cannot be empty.")
        return

    if name in criminals:
        print("Criminal already exists.")
        return

    try:
        age = int(input("Enter age: ").strip())
        if age <= 0:
            print("Invalid age.")
            return
    except ValueError:
        print("Age must be a number.")
        return

    danger_levels = ["low", "medium", "high"]
    danger = input("Enter danger level(low,medium,high): ").strip().lower()

    if danger not in danger_levels:
        print("Invalid danger level.")
        return

    crimes_input = input("Enter crimes (comma separated): ").strip()
    crimes_committed = [c.strip().title() for c in crimes_input.split(",") if c.strip()]

    associates_input = input("Enter associates: ").strip()
    associates = set(a.strip().title() for a in associates_input.split(",") if a.strip())

    status_list = ["wanted", "arrested", "released"]
    status = input("Enter status(wanted,arrested,released): ").strip().lower()

    if status not in status_list:
        print("Invalid status.")
        return

    criminal = {
        "name": name,
        "age": age,
        "danger_level": danger,
        "crimes_committed": crimes_committed,
        "known_associates": associates,
        "status": status
    }

    criminals.append(criminal)
    save_data()

    print("✅ Criminal added.")



# ======= VIEW RECENT CRIMES =======
def format_date(date_str):
    # convert ISO date to readable format
    return datetime.strptime(date_str,"%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")


def view_recent_crimes():

    try:
        if not recent_crimes:
            print("No crimes logged yet.")
            return
        
        print("========== RECENT CRIMES ==========")
        for crime in recent_crimes:
            print(f"#{crime['id']:<3} | {crime['type']:<7} | {crime['location']['area']:<10} | {format_date(crime['date']):<10} | {crime['status']}")

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return
        

# ======= UPDATE CRIME STATUS =======
def update_crime_status():

    global crimes

    try:
        if not crimes:
            print("No crimes loggeed yet.")
            return
        
        highest_crime_id = max([crime["id"] for crime in crimes])
        try:
            id = int(input("Enter the Crime ID: ").strip())

            if id < 0:
                print("Invalid Crime ID.")
                return
            
            if id > highest_crime_id:
                print("Crime ID number is too big.")
                return
            
        except ValueError:
            print("Crime ID should be a number")
            return

        for c in crimes:
            if id == c["id"]:
                current_status = c.get("status")
                print(f"Current status: {current_status}")
                break

        status_lst = ["open","investigating","closed"]
        new_status = input("Enter the new status(open/investigating/closed): ").strip()

        if not new_status:
            print("Status cannot be empty.")
            return
        
        if new_status not in status_lst:
            print("New status should be (open/investigating/closed).")
            return
        
        found = False
        for c in crimes:
            if id == c["id"]:
                c["status"] = new_status
                found = True
                break

        if not found:
            print(f"No such crime with Crime ID #{id} exists.")
            return
        
        save_data()
        print("Crime status updated successfully!!")
        
    except Exception as e:
        print(f"Unexpected Error : {e}")
        return


# ======= SEARCH CRIMES =======
def search_by_location(keyword):
    try:
        found = False
        print("\n=== SEARCHING CRIMES BY LOCATION ===")

        for crime in crimes:
            if keyword in crime["location"]["area"].lower():
                print(f"#{crime['id']:<3} | {crime['type']:<7} | {crime['location']['area']:<10} | {format_date(crime['date']):<10} | {crime['status']}")
                found = True

        if not found:
            print("No crimes found matching your search.")

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return
    

def search_by_type(keyword):
    try:
        found = False
        print("\n=== SEARCHING CRIMES BY TYPE ===")

        for crime in crimes:
            if keyword in crime["type"].lower():
                print(f"#{crime['id']:<3} | {crime['type']:<7} | {crime['location']['area']:<10} | {format_date(crime['date']):<10} | {crime['status']}")
                found = True

        if not found:
            print("No crimes found matching your search.")  

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return  


def search_by_status(keyword):
    try:
        found = False
        print("\n=== SEARCHING CRIMES BY STATUS ===")

        for crime in crimes:
            if keyword == crime["status"].lower():
                print(f"#{crime['id']:<3} | {crime['type']:<7} | {crime['location']['area']:<10} | {format_date(crime['date']):<10} | {crime['status']}")
                found = True

        if not found:
            print("No crimes found matching your search.")  

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return


def search_crimes():
    try:
        if not crimes:
            print("No crimes logged yet.")
            return
        
        while True:
            print("\n============ SEARCHING CRIMES ============")
            print("1. Search by location.")
            print("2. Search by type.")
            print("3. Search by status.")
            print("4. Return to main menu.")

            try:
                choice = int(input("Enter your choice(1-4): ").strip())
            except ValueError:
                print("Invalid choice.Choice should be numbers only.")
                continue
            
            if choice == 1:
                keyword = input("Enter a location: ").strip().lower()

                if not keyword:
                    print("Keyword should not be empty.")
                    continue
                    
                search_by_location(keyword)

            elif choice == 2:
                keyword = input("Enter the type of crime: ").strip().lower()

                if not keyword:
                    print("Keyword should not be empty.")
                    continue
                
                search_by_type(keyword)

            elif choice == 3:
                keyword = input("Enter the status of crime(open,investigating,closed): ").strip().lower()

                status_lst = ["open","investigating","closed"]

                if not keyword:
                    print("Keyword should not be empty.")
                    continue
                
                if keyword not in status_lst:
                    print("Invalid keyword.")
                    continue
                
                search_by_status(keyword)

            elif choice == 4:
                print("Returning to main menu.")
                break

            else:
                print("Invalid choice.It must be(1-4).")
                continue

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return


# ======= SEARCH CRIMINALS =======
def search_by_name(keyword):
    try:
        found = False
        print("\n=== SEARCHING BY NAME ===")

        for i,criminal in enumerate(criminals):
            if keyword in criminal["name"].lower():
                print(f"{i} | {criminal['name']:<7} | {criminal['age']:<3} | {criminal['danger_level']:<5} | {', '.join(criminal['crimes_committed']):<15} | {', '.join(criminal['known_associates']):<15} | {criminal['status']}")
                found = True

        if not found:
            print("No criminals found matching your search.")

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return


def search_by_danger_level(keyword):
    try:
        found = False
        print("\n=== SEARCHING BY DANGER LEVEL ===")

        for i,criminal in enumerate(criminals):
            if keyword == criminal["danger_level"].lower():
                print(f"{i} | {criminal['name']:<7} | {criminal['age']:<3} | {criminal['danger_level']:<5} | {', '.join(criminal['crimes_committed']):<15} | {', '.join(criminal['known_associates']):<15} | {criminal['status']}")
                found = True

        if not found:
            print("No criminals found matching your search.")

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return


def search_criminals():
    try:
        if not criminals:
            print("No criminals added yet.")
            return
        
        while True:
            print("\n============ SEARCH CRIMINALS ============")
            print("1. Search by name.")
            print("2. Search by danger level.")
            print("3. Return to main menu.")

            try:
                choice = int(input("Enter your choice(1-3): ").strip())
            except ValueError:
                print("Invalid choice.Choice should be numbers only.")
                continue

            if choice == 1:
                keyword = input("Enter the name of the criminal: ").strip().lower()

                if not keyword:
                    print("Keyword should not be empty.")
                    continue
                
                search_by_name(keyword)

            elif choice == 2:
                keyword = input("Enter the danger level(low,medium,high): ").strip().lower()

                danger_level_lst = ["low","medium","high"]

                if not keyword:
                    print("Keyword should not be empty.")
                    continue
                
                if keyword not in danger_level_lst:
                    print("Invalid keyword.")
                    continue

                search_by_danger_level(keyword)

            elif choice == 3:
                print("Returning to main menu.")
                break

            else:
                print("Invalid choice.It must be (1-3).")
                continue

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return
    

# ======= VIEW COLD CASES =======
def view_cold_cases():
    try:
        if not crimes:
            print("No crimes logged yet.")
            return
        
        current_date = datetime.now()
        found = False
        
        print("\n============ COLD CASES ============")
        for i,crime in enumerate(crimes,start = 1):
            parsed_date = datetime.strptime(crime["date"], "%Y-%m-%dT%H:%M:%S")
            days_open = (current_date - parsed_date).days

            if crime["status"] == "open" and days_open > 30:
                print(f"{i}. #{crime['id']:<3} | {crime['type']:<7} | {crime['location']['area']:<10} | {format_date(crime['date']):<10} | {crime['status']}")
                print(f"Days open : {days_open}")
                found = True

        if not found:
            print("No cold cases available.All open cases are under 30 days.")

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return


# ======= STATS DASHBOARD =======
def stats_dashboard():
    try:
        if not crimes:
            print("No crimes logged yet.")
            return
        
        if not criminals:
            print("No criminals added yet.")
            return
        
        total_crimes = len(crimes)

        closed_crimes = sum(1 for c in crimes if c["status"] == "closed")

        investigating_crimes = sum(1 for c in crimes if c["status"] == "investigating")

        open_crimes = sum(1 for c in crimes if c["status"] == "open")

        solve_rate = (closed_crimes / total_crimes) * 100 if total_crimes > 0 else 0

        cold_cases = 0
        current_date = datetime.now()

        for crime in crimes:
            parsed_date = datetime.strptime(crime["date"], "%Y-%m-%dT%H:%M:%S")
            days_open = (current_date - parsed_date).days

            if crime["status"] == "open" and days_open > 30:
                cold_cases += 1

        total_criminals = len(criminals)

        max_crimes = max(len(c["crimes_committed"]) for c in criminals)

        most_wanted = [c for c in criminals if len(c["crimes_committed"]) == max_crimes]

       
        print("\n============ STATS DASHBOARD ============")
        print(f"1. {'TOTAL CRIMES':<20} : {total_crimes}")
        print(f"2. {'CLOSED CRIMES (SOLVED)':<20} : {closed_crimes}")
        print(f"3. {'INVESTIGATING CRIMES':<20} : {investigating_crimes}")
        print(f"4. {'OPEN CRIMES':<20} : {open_crimes}")
        print(f"5. {'SOLVE RATE %':<20} : {solve_rate:.2f} %")
        print(f"6. {'COLD CASES COUNT':<20} : {cold_cases}")
        print(f"7. {'TOTAL CRIMINALS':<20} : {total_criminals}")
        print(f"8. {'MOST WANTED':<20} : ")
        for criminal in most_wanted:
            print(f"  {criminal['name']} — {len(criminal['crimes_committed'])} crimes")
        
    except Exception as e:
        print(f"Unexpected Error : {e}")
        return
    

# ======= PATTERN ANALYSIS ======= 
def pattern_analysis():
    try:
        if not crimes:
            print("No crimes logged yet.")
            return
        
        crime_types = Counter(crime["type"] for crime in crimes)

        locations = Counter(crime["location"]["area"] for crime in crimes)

        top_days = Counter(datetime.strptime(crime["date"],"%Y-%m-%dT%H:%M:%S").strftime("%A") for crime in crimes)

        grouped = defaultdict(list)

        for crime in crimes:
            grouped[crime["type"]].append(crime["location"]["area"])

        while True:
            print("\n============ PATTERN ANALYSIS ============")
            print("1. Most common crime type.")
            print("2. Most dangerous location.")
            print("3. Busiest day of week.")
            print("4. Crimes grouped by type.")
            print("5. Show all insights.")
            print("6. Return to main menu.")

            try:
                choice = int(input("Enter your choice(1-6): ").strip())
            except ValueError:
                print("Choice cannot be empty.")
                continue

            if choice == 1:
                most_common_crime = crime_types.most_common(1)[0]
                print(f"Most common crime  : {most_common_crime[0]} ({most_common_crime[1]} cases)")

            elif choice == 2:
                dangerous_location = locations.most_common(1)[0]
                print(f"Dangerous Location : {dangerous_location[0]} ({dangerous_location[1]} locations)")

            elif choice == 3:
                busiest_day = top_days.most_common(1)[0]
                print(f"Busiest Day : {busiest_day[0]} ({busiest_day[1]} crimes)")
            elif choice == 4:
                for crime_type,locationss in grouped.items():
                    print(f"{crime_type:<15} : {', '.join(locationss)}")

            elif choice == 5:
                most_common_crime = crime_types.most_common(1)[0]
                dangerous_location = locations.most_common(1)[0]
                busiest_days = top_days.most_common(1)[0]

                print("\n========== ALL INSIGHTS ==========")
                print(f"Most common crime  : {most_common_crime[0]} ({most_common_crime[1]} cases)")
                print(f"Dangerous Location : {dangerous_location[0]} ({dangerous_location[1]} locations)")
                print(f"Busiest Day : {busiest_days[0]} ({busiest_days[1]} crimes)")

                for crime_type,locationss in grouped.items():
                    print(f"{crime_type:<15} : {', '.join(locationss)}")

            elif choice == 6:
                print("Returning to main menu.")
                break

            else:
                print("Invalid choice.It must be(1-6).")
                
    except Exception as e:
        print(f"Unexpected Error : {e}")
        return
    

# ======= GENERATE REPORT =======
def generate_report():
    try:
        if not crimes:
            print("No crimes logged yet.")
            return
        
        if not criminals:
            print("No criminals added yet.")
            return
        
        filename = f"report_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.txt"

        with open(filename,"w") as f:
            f.write("="*50)
            f.write(f"\nCRIME INTELLIGENCE REPORT")
            f.write(f"\n{datetime.now().strftime('%d/%m/%Y_%H:%M')}")
            f.write("\n"+"="*50)
            f.write("\n"+"="*30)
            f.write("\nALL CRIMES")
            f.write("\n"+"="*30)
            
            for i,crime in enumerate(crimes,start = 1):
                f.write(f"\n{i} | #{crime['id']:<3} | {crime['type']:<7} | {crime['location']['area']:<10} | {format_date(crime['date']):<10} | {crime['status']}")
            
            f.write("\n"+"="*30)

            f.write("\nALL CRIMINALS")
            f.write("\n"+"="*30)

            for i,criminal in enumerate(criminals,start= 1):
                f.write(f"\n{i} | {criminal['name']:<7} | {criminal['age']:<3} | {criminal['danger_level']:<5} | {', '.join(criminal['crimes_committed']):<15} | {', '.join(criminal['known_associates']):<15} | {criminal['status']}")
            
            total_crimes = len(crimes)

            closed_crimes = sum(1 for c in crimes if c["status"] == "closed")

            investigating_crimes = sum(1 for c in crimes if c["status"] == "investigating")

            open_crimes = sum(1 for c in crimes if c["status"] == "open")

            solve_rate = (closed_crimes / total_crimes) * 100 if total_crimes > 0 else 0

            cold_cases = 0
            current_date = datetime.now()

            for crime in crimes:
                parsed_date = datetime.strptime(crime["date"], "%Y-%m-%dT%H:%M:%S")
                days_open = (current_date - parsed_date).days

                if crime["status"] == "open" and days_open > 30:
                    cold_cases += 1

            total_criminals = len(criminals)

            max_crimes = max(len(c["crimes_committed"]) for c in criminals)

            most_wanted = [c for c in criminals if len(c["crimes_committed"]) == max_crimes]

            f.write("\n"+"="*30)
            f.write("\nSTATS DASHBOARD")
            f.write("\n"+"="*30)
            f.write(f"\n1. {'TOTAL CRIMES':<20} : {total_crimes}")
            f.write(f"\n2. {'CLOSED CRIMES (SOLVED)':<20} : {closed_crimes}")
            f.write(f"\n3. {'INVESTIGATING CRIMES':<20} : {investigating_crimes}")
            f.write(f"\n4. {'OPEN CRIMES':<20} : {open_crimes}")
            f.write(f"\n5. {'SOLVE RATE %':<20} : {solve_rate:.2f} %")
            f.write(f"\n6. {'COLD CASES COUNT':<20} : {cold_cases}")
            f.write(f"\n7. {'TOTAL CRIMINALS':<20} : {total_criminals}")
            f.write(f"\n8. {'MOST WANTED':<20} : ")
            for criminal in most_wanted:
                f.write(f"\n{criminal['name']} — {len(criminal['crimes_committed'])} crimes")

            f.write("\n"+"="*50) 

        print(f"✅ Report saved as: {filename}")

    except Exception as e:
        print(f"Unexpected Error : {e}")
        return
    

# ========== MAIN ==========
def main():
    load_data()

    actions = {
            1 : log_crime,
            2 : add_criminal,
            3 : search_crimes,
            4 : search_criminals,
            5 : pattern_analysis,
            6 : generate_report,
            7 : view_cold_cases,
            8 : stats_dashboard,
            9 : update_crime_status,
            10 : view_recent_crimes
        }


    while True:
        print("="*50)
        print("CRIME INTELLIGENCE SYSTEM")
        print("="*50)
        print("MAIN MENU")
        print("="*50)
        print("1.  Log New Crime.")
        print("2.  Add Criminal Profile.")
        print("3.  Search Crimes.")
        print("4.  Search Criminals.")
        print("5.  View Pattern Analysis.")
        print("6.  Generate Investigation Report.")
        print("7.  View Cold Cases.")
        print("8.  Stats Dashboard.")
        print("9.  Update Crime Status.")
        print("10. View Recent Crimes.")
        print("11. Exit.")
        print("="*50)

        try:
            choice = int(input("Enter your choice(1-11): ").strip())

        except ValueError:
            print("Invalid choice.Choice should be number only.")
            continue

        
        if choice in actions:
            actions[choice]()

        elif choice == 11:
            print("Goodbye detective.")
            save_data()
            break

        else:
            print("Invalid choice.")
            continue

        again = input("\nDo you want to perform another action(yes/no): ").strip().lower()

        if again != "yes":
            print("Goodbye detective.")
            save_data()
            break

if __name__ == "__main__":
    main()
