1. Put playwright_click_send_probe.py in Downloads.
2. Open PowerShell and run:

   cd "$HOME\Downloads"
   python playwright_click_send_probe.py

3. This clicks the first enabled Send email button and opens Outlook web.
4. Observe-only mode does not click Outlook Send.
5. After checking the compose window, run:

   python playwright_click_send_probe.py --confirm

   This sends one email only.
