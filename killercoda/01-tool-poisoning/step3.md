## Step 3: Watch the exfiltration

Check the exfil receiver output. The stolen canary file arrived at `localhost:9999`.

```bash
# Check the exfil receiver output (the background process)
jobs -l
```

The exfil receiver is still running in the background from Step 2. You can check
its output in the terminal tab where you started it.

**You should now see:**

- A POST to `/exfil` containing:
  ```json
  {"tool": "add", "stolen_data": "ssh-rsa AAAA... (synthetic canary key)"}
  ```

The attack succeeded: the poisoned tool description coerced the agent into reading
the canary file and passing its contents as a parameter to the attacker's tool. The
user saw only "47 + 38 = 85".
