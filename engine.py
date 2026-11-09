"""PC Fault Diagnosis Expert System - INFERENCE ENGINE (v5).
   Forward chaining with on-demand questions. Knows nothing about PCs:
   all domain knowledge is imported from knowledge_base.py."""

from knowledge_base import RULES, FAULTS, QUESTIONS, GROUPS


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