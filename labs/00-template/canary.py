"""Flag definition and canary check for this lab.

The lab's single flag lives here and nowhere else in the repo, and it is
revealed only by the observable side effect that means the attack worked:
a synthetic secret reaching a localhost listener, a specific file reached,
a rogue registration that persists, a row written. Never by parsing what a
model said.

Replace both parts below with the lab's real canary:

- FLAG : the synthetic canary value, of the form AGENTICGOAT{NN_short-slug}.
  It is embedded wherever the stolen data lives (a canary file, a seeded
  note, a sandbox secret, a victim environment variable) or checked where the
  stolen data lands.
- canary_reached() : returns True only when the side effect has occurred.
  The attack driver and any CI check assert on this, not on model output.
"""

FLAG = "AGENTICGOAT{NN_short-slug}"


def canary_reached() -> bool:
    """Return True only when the observable side effect has occurred."""
    raise NotImplementedError(
        "Wire this to the lab's existing success signal. "
        "Do not change the attack to make capture easier."
    )
