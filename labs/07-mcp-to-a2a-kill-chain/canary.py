"""Flag definition and canary check for Lab 07 (MCP to A2A kill chain).

The lab's single flag lives here. killchain.py writes it to the exfil
sink (state/exfil.json) only alongside the HR record, i.e. only when
the undefended chain completes stage 4 (lateral movement). With any
control enabled the sink stays empty and the flag is never revealed.
This lab is model-independent: the check runs on every run.
"""

from pathlib import Path

FLAG = "AGENTICGOAT{07_kill-chain}"

EXFIL_STATE = Path(__file__).resolve().parent / "state" / "exfil.json"


def canary_reached() -> bool:
    """Return True only when the flag has reached the exfil sink."""
    if not EXFIL_STATE.exists():
        return False
    return FLAG in EXFIL_STATE.read_text(encoding="utf-8")


if __name__ == "__main__":
    import sys

    reached = canary_reached()
    print(
        "canary reached: the flag is in the exfil sink"
        if reached
        else "canary not reached: the exfil sink does not carry the flag"
    )
    sys.exit(0 if reached else 1)
