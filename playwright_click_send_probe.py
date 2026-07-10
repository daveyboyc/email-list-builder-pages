#!/usr/bin/env python3
"""Click one enabled Send email button in the hosted outreach page.

Observe-only: this never clicks Outlook's final Send button.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


DEFAULT_PAGE = "https://daveyboyc.github.io/email-list-builder-pages/"
DEFAULT_PROFILE = Path.home() / ".cache" / "email-list-builder" / "outlook-browser-profile"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", default=DEFAULT_PAGE)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--confirm", action="store_true", help="Click Outlook Send for one contact")
    args = parser.parse_args()

    args.profile.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(str(args.profile), headless=False)
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(args.page, wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
        buttons = page.get_by_role("button", name="Send email", exact=True)
        count = buttons.count()
        for index in range(count):
            button = buttons.nth(index)
            if button.is_enabled():
                print(f"Clicking Send email button {index + 1} of {count}.")
                try:
                    with context.expect_page(timeout=5000) as popup_info:
                        button.click()
                    popup = popup_info.value
                    popup.wait_for_timeout(3000)
                    print(f"New browser tab opened: {popup.url}")
                    popup.wait_for_timeout(3000)
                    send = popup.get_by_role("button", name="Send", exact=True)
                    if args.confirm:
                        send.click()
                        print("Outlook Send clicked for one contact; the outreach page already recorded it as sent.")
                    else:
                        print("Observe-only: Outlook Send was not clicked. Add --confirm for one real send.")
                except Exception:
                    print("No browser popup was detected; inspect the current browser window.")
                input("Review the Outlook compose window. Press Enter to close... ")
                context.close()
                return
        context.close()
        raise SystemExit("No enabled Send email button found. Load the queue CSV in the page first.")


if __name__ == "__main__":
    main()
