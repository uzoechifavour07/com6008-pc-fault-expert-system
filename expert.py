"""PC Fault Diagnosis Expert System - forward chaining (v4 skeleton)."""

# ---------- KNOWLEDGE BASE 1: PRODUCTION RULES ----------
# "if" = conditions that must ALL be true. "not x" means x was answered no.
# "then" = new fact. Facts starting with "fault:" are diagnoses.
# "priority" = used for conflict resolution (higher wins).
RULES = [
    {"id": "R1", "group": "A", "if": ["power_button_pressed", "no_lights", "no_fans", "no_sounds"],
     "then": "no_power"},
    {"id": "R2", "group": "A", "if": ["no_power", "not outlet_works"],
     "then": "fault:faulty_outlet", "priority": 2},
    {"id": "R3", "group": "A", "if": ["no_power", "outlet_works", "not cable_and_switch_ok"],
     "then": "fault:power_connection_problem", "priority": 2},
    {"id": "R4", "group": "A", "if": ["no_power", "outlet_works", "cable_and_switch_ok"],
     "then": "fault:possible_psu_failure", "priority": 1},
    {"id": "R5", "group": "A",
     "if": ["power_lights_or_fans_on", "screen_blank"],
     "then": "powers_on_no_display"},

    {"id": "R6", "group": "A",
     "if": ["powers_on_no_display", "not monitor_power_light_on"],
     "then": "fault:monitor_power_problem", "priority": 2},

    {"id": "R7a", "group": "A",
     "if": ["powers_on_no_display", "monitor_power_light_on",
            "not display_cable_firmly_connected"],
     "then": "fault:display_connection_problem", "priority": 2},

    {"id": "R7b", "group": "A",
     "if": ["powers_on_no_display", "monitor_power_light_on",
            "not correct_monitor_input_selected"],
     "then": "fault:display_connection_problem", "priority": 2},

    {"id": "R7c", "group": "A",
     "if": ["powers_on_no_display", "monitor_power_light_on",
            "display_cable_firmly_connected",
            "correct_monitor_input_selected"],
     "then": "display_connection_checked"},

    {"id": "R8", "group": "A",
     "if": ["display_connection_checked", "screen_still_blank"],
     "then": "fault:possible_graphics_or_display_fault", "priority": 1},

    {"id": "R9", "group": "A",
     "if": ["powers_on_no_display", "beep_pattern_matches_memory_fault_code"],
     "then": "fault:possible_ram_fault", "priority": 2},

    {"id": "R10", "group": "A",
     "if": ["manufacturer_logo_appears", "operating_system_does_not_load"],
     "then": "boot_failure"},

    {"id": "R11", "group": "A",
     "if": ["boot_failure", "not drive_listed_in_bios"],
     "then": "fault:possible_drive_or_drive_connection_problem", "priority": 2},

    {"id": "R12", "group": "A",
     "if": ["boot_failure", "drive_listed_in_bios",
            "boot_error_message_appears"],
     "then": "fault:possible_operating_system_or_boot_file_problem",
     "priority": 1},

     {"id": "R13", "group": "B",
     "if": ["startup_takes_more_than_two_minutes",
            "unneeded_startup_apps_enabled"],
     "then": "fault:startup_apps_may_be_contributing", "priority": 1},

    {"id": "R14", "group": "B",
     "if": ["pc_runs_slowly", "less_than_10_percent_storage_free"],
     "then": "fault:low_storage_may_be_contributing", "priority": 1},

    {"id": "R15", "group": "B",
     "if": ["pc_runs_slowly", "drive_health_warning_shown"],
     "then": "fault:possible_drive_problem", "priority": 2},

    {"id": "R16", "group": "B",
     "if": ["pc_runs_slowly", "memory_use_stays_above_90_percent"],
     "then": "fault:ram_capacity_may_be_limiting_performance",
     "priority": 1},

    {"id": "R17", "group": "B",
     "if": ["pc_runs_slowly", "antivirus_scan_reports_threat"],
     "then": "fault:malware_detected", "priority": 2},

    {"id": "R18", "group": "B",
     "if": ["pc_runs_slowly", "too_hot_to_touch"],
     "then": "overheating_suspected"},

    {"id": "R19", "group": "B",
     "if": ["overheating_suspected", "not fan_spinning"],
     "then": "fault:possible_fan_or_cooling_problem", "priority": 2},

    {"id": "R20", "group": "B",
     "if": ["overheating_suspected", "fan_spinning",
            "visible_dust_or_blocked_vents"],
     "then": "fault:possible_airflow_obstruction", "priority": 1},

    {"id": "R21", "group": "C",
     "if": ["pc_shuts_down_unexpectedly", "too_hot_to_touch"],
     "then": "fault:possible_thermal_shutdown", "priority": 2},

    {"id": "R22", "group": "C",
     "if": ["pc_shuts_down_unexpectedly", "not too_hot_to_touch"],
     "then": "fault:possible_power_or_battery_problem", "priority": 1},

    {"id": "R23", "group": "C",
     "if": ["blue_screen_repeats",
            "new_hardware_or_driver_added_before_problem"],
     "then": "fault:possible_hardware_or_driver_problem",
     "priority": 1},

    {"id": "R24", "group": "C",
     "if": ["clicking_or_grinding_sound_from_drive"],
     "then": "fault:possible_mechanical_drive_problem", "priority": 2},

    {"id": "R25", "group": "C",
     "if": ["fan_loud_for_more_than_a_few_minutes",
            "visible_dust_or_blocked_vents"],
     "then": "fault:possible_airflow_obstruction", "priority": 1},

    {"id": "R26", "group": "C",
     "if": ["blue_screen_repeats", "memory_errors"],
     "then": "fault:possible_memory_problem", "priority": 2},
   
]

# ---------- KNOWLEDGE BASE 2: FAULT FRAMES ----------
FAULTS = {
    "faulty_outlet": {"description": "The wall socket is not supplying power.",
                      "advice": "Try a different socket or test this one with a lamp.",
                      "severity": "Low"},
    "power_connection_problem": {"description": "The power cable or PSU switch is the problem.",
                                 "advice": "Reseat the power cable at both ends and switch the PSU on (I).",
                                 "severity": "Low"},
    "possible_psu_failure": {"description": "The power supply unit may have failed.",
                             "advice": "Test with a known-good PSU or take it to a technician.",
                                "severity": "High"},
     "display_connection_problem": { "description": "The PC is running, but the display connection or monitor may be faulty.",
                                     "advice": "Check that the monitor is on and the display cable is firmly connected at both ends.",
                                     "severity": "Low"},
    "monitor_power_problem": {"description": "The monitor may not be receiving power.",
                              "advice": "Check that the monitor’s power cable is connected and its power button is on. Try another outlet if needed.",
                              "severity": "Low"},
    "possible_graphics_or_display_fault": {"description": "The PC powers on, but the screen remains blank after checking the monitor and display connection.",
                                           "advice": "Try another display cable or monitor. If the issue continues, have the graphics card and PC checked.",
                                           "severity": "Medium"},
    "possible_ram_fault": {"description": "A memory-related beep pattern may indicate a RAM fault.",
                            "advice": "Turn off and unplug the PC before checking that the RAM is seated correctly. If the beeps continue, have the memory tested.",
                            "severity": "High"},
    "possible_drive_or_drive_connection_problem": {"description": "The boot drive may be disconnected or failing.",
                                                    "advice": "Turn off the PC and check the drive connections if you’re comfortable doing so. Back up important data if possible, or ask a technician to check it.",
                                                    "severity": "High"},
    "possible_operating_system_or_boot_file_problem": {"description": "The PC detects its drive, but the operating system or its boot files may be damaged.",
                                                        "advice": "Use the operating system’s recovery tools or seek technical help. Avoid reinstalling before backing up important files.",
                                                        "severity": "Medium"},
    "startup_apps_may_be_contributing": {
        "description": "Too many enabled startup apps may be slowing startup.",
        "advice": "Disable startup apps you do not need, then restart the PC.",
        "severity": "Low"},
    "low_storage_may_be_contributing": {
        "description": "Very little free storage may be contributing to slow performance.",
        "advice": "Free up space by removing files or apps you no longer need.",
        "severity": "Low"},
    "possible_drive_problem": {
        "description": "A drive health warning may indicate a failing drive.",
        "advice": "Back up important files and have the drive checked.",
        "severity": "High"},
    "ram_capacity_may_be_limiting_performance": {
        "description": "High memory use may mean the PC does not have enough RAM for its workload.",
        "advice": "Close apps you are not using. If memory use remains high, consider a RAM upgrade.",
        "severity": "Low"},
    "malware_detected": {
        "description": "An antivirus scan detected a possible threat.",
        "advice": "Follow your antivirus software’s instructions to quarantine or remove the threat.",
        "severity": "High"},
    "possible_fan_or_cooling_problem": {
        "description": "A fan may not be spinning, which can cause the PC to overheat.",
        "advice": "Stop demanding use of the PC and have its fan and cooling system checked.",
        "severity": "High"},
    "possible_airflow_obstruction": {
        "description": "Dust or blocked vents may be restricting airflow.",
        "advice": "Turn off the PC, clear objects from its vents, and clean dust carefully.",
        "severity": "Medium"},
    "possible_thermal_shutdown": {
        "description": "The PC may be shutting down to protect itself from overheating.",
        "advice": "Let it cool, check that vents are clear, and have the cooling system inspected if it happens again.",
        "severity": "High"},
    "possible_power_or_battery_problem": {
        "description": "Unexpected shutdowns without signs of overheating may be caused by a power or battery problem.",
        "advice": "Check the power connection. For a laptop, try its charger and have the battery checked if the problem continues.",
        "severity": "Medium"},
    "possible_hardware_or_driver_problem": {
        "description": "A recent hardware or driver change may be related to the repeated blue screens.",
        "advice": "Undo the recent change or update the affected driver. If the blue screens continue, seek technical help.",
        "severity": "Medium"},
    "possible_mechanical_drive_problem": {
        "description": "Clicking or grinding from a drive may indicate mechanical failure.",
        "advice": "Back up important files immediately if possible, then stop using the drive and have it checked.",
        "severity": "High"},
    "possible_memory_problem": {
        "description": "Memory diagnostic errors may indicate faulty RAM.",
        "advice": "Have the RAM tested and reseated or replaced. Back up important files if the PC remains usable.",
        "severity": "High"},           
   
}

# ---------- QUESTIONS SHOWN TO THE USER ----------
QUESTIONS = {
    "power_button_pressed": "Have you pressed the power button?",
    "no_lights": "Are there NO lights at all on the PC?",
    "no_fans": "Are the fans NOT spinning?",
    "no_sounds": "Is the PC completely silent?",
    "outlet_works": "Does the wall socket work with another device (e.g. a lamp)?",
    "cable_and_switch_ok": "Is the power cable firmly in AND the PSU switch on?",
    "power_lights_or_fans_on": "Do any power lights come on or fans spin when you press the power button?",
    "screen_blank": "Is the monitor screen blank?",
    "monitor_power_light_on": "Is the monitor’s power light on?",
    "display_cable_firmly_connected": "Is the display cable firmly connected at both ends?",
    "correct_monitor_input_selected": "Is the monitor set to the input used by the PC?",
    "screen_still_blank": "Is the screen still blank after checking the monitor and its connections?",
    "beep_pattern_matches_memory_fault_code": "Does the PC beep with a pattern identified by its manufacturer as a memory fault code?",
    "manufacturer_logo_appears": "Does the manufacturer’s logo appear when you turn on the PC?",
    "operating_system_does_not_load": "Does the operating system fail to load?",
    "drive_listed_in_bios": "Is the boot drive listed in the BIOS or UEFI settings?",
    "boot_error_message_appears": "Does a boot error message appear?",
    "startup_takes_more_than_two_minutes": "Does startup take more than two minutes?",
    "unneeded_startup_apps_enabled": "Are apps you do not need enabled to start automatically?",
    "pc_runs_slowly": "Is the PC running unusually slowly?",
    "less_than_10_percent_storage_free": "Is less than 10% of the drive's storage free?",
    "drive_health_warning_shown": "Has the PC shown a drive health warning?",
    "memory_use_stays_above_90_percent": "Does memory use stay above 90% when the PC is slow?",
    "antivirus_scan_reports_threat": "Has an antivirus scan reported a threat?",
    "too_hot_to_touch": "Does the PC feel unusually hot to the touch?",
    "fan_spinning": "Is the fan spinning?",
    "visible_dust_or_blocked_vents": "Is there visible dust or are any air vents blocked?",
    "pc_shuts_down_unexpectedly": "Does the PC shut down unexpectedly?",
    "blue_screen_repeats": "Does the PC show repeated blue screens?",
    "new_hardware_or_driver_added_before_problem": "Was new hardware added or a driver changed shortly before the problem began?",
    "clicking_or_grinding_sound_from_drive": "Do you hear clicking or grinding from a drive?",
    "fan_loud_for_more_than_a_few_minutes": "Does a fan stay unusually loud for more than a few minutes?",
    "memory_errors": "Has a memory diagnostic reported errors?",
}

GROUPS = {"A": "PC won't start", "B": "PC runs slowly", "C": "Shutdowns, blue screens or noises"}


# ---------- INFERENCE ENGINE ----------
def derived_facts():
    """Facts concluded by some rule - the system works these out, never asks."""
    return {r["then"] for r in RULES}


def askable_facts(group):
    """Every condition in this group's rules that no rule concludes."""
    derived = derived_facts()
    facts = []
    for rule in RULES:
        if rule["group"] != group:
            continue
        for cond in rule["if"]:
            fact = cond.removeprefix("not ")
            if fact not in derived and fact not in facts:
                facts.append(fact)
    return facts


def holds(cond, wm, askable):
    """Is a condition true? Asks the user if the fact is unknown and askable."""
    fact = cond.removeprefix("not ")
    if fact not in wm and fact in askable:
        wm[fact] = ask(fact)                 # ask only when a rule needs it
    value = wm.get(fact)
    if cond.startswith("not "):
        return value is False
    return value is True


def forward_chain(wm, group, askable):
    """Fire this group's rules until no new facts appear. Returns rules fired, in order."""
    fired = []
    changed = True
    while changed:
        changed = False
        for rule in RULES:
            if rule["group"] != group or rule in fired:
                continue
            if all(holds(c, wm, askable) for c in rule["if"]):
                wm[rule["then"]] = True
                fired.append(rule)
                changed = True
    return fired

SEVERITY_RANK = {"High": 3, "Medium": 2, "Low": 1}

def resolve(fired):
    """Conflict resolution: rank every fault that fired.
    Highest priority first; ties broken by severity from the fault frame."""
    faults = {}
    for r in fired:
        if r["then"].startswith("fault:"):
            name = r["then"].removeprefix("fault:")
            faults.setdefault(name, r)          # same fault from two rules -> list once
    def score(r):
        name = r["then"].removeprefix("fault:")
        sev = FAULTS.get(name, {}).get("severity")
        return (r.get("priority", 0), SEVERITY_RANK.get(sev, 0))
    return sorted(faults.values(), key=score, reverse=True)



def ask(fact):
    text = QUESTIONS.get(fact, fact.replace("_", " ").capitalize() + "?")
    while True:
        ans = input(f"  {text} (y/n) ").strip().lower()
        if ans in ("y", "n"):
            return ans == "y"

def explain(fired):
    if not fired:
        print("\nNo rules fired."); return
    print("\nHow I reached this:")
    for r in fired:
        print(f"  {r['id']}: IF {' AND '.join(r['if'])} THEN {r['then']}")

def main():
    print("PC Fault Diagnosis Expert System\n")
    for key, name in GROUPS.items():
        print(f"  {key}. {name}")
    group = ""
    while group not in GROUPS:
        group = input("Which problem? ").strip().upper()

    wm = {}  # working memory
    askable = set(askable_facts(group))
    fired = forward_chain(wm, group, askable)
    ranked = resolve(fired)

    if not ranked:
        print("\nDiagnosis: cause not identified by the current rules.")
        print("Advice: collect more information or consult a technician.")
    else:
        for i, rule in enumerate(ranked):
            name = rule["then"].removeprefix("fault:")
            frame = FAULTS.get(name, {})
            if i == 0:
                print(f"\nMost likely: {name.replace('_', ' ')}")
                print(f"  {frame.get('description', '')}")
                print(f"  Advice: {frame.get('advice', '')}")
                print(f"  Severity: {frame.get('severity', '?')}")
            else:
                if i == 1:
                    print("\nOther possible causes:")
                print(f"  - {name.replace('_', ' ')} (severity {frame.get('severity', '?')}): "
                      f"{frame.get('advice', '')}")
    explain(fired)
if __name__ == "__main__":
    main()