import sys
import asyncio
from scraper import client, join_group, scan_admins, PHONE
from analysis import analyze_patterns, find_pre_tge_projects
from sheets import update_google_sheet, get_group_links
from telethon.sessions import StringSession
import datetime

async def run_report():
    print("Analyzing patterns...")
    patterns = analyze_patterns()
    report_data = []
    for p in patterns:
        print(f"Pattern: Admin {p['user']} found in {p['count']} groups: {p['groups']}")
        report_data.append([
            "Pattern",
            p['groups'],
            p['user'],
            "Multiple Roles",
            f"Found in {p['count']} groups",
            datetime.datetime.now().isoformat()
        ])

    print("Searching for pre-TGE projects...")
    projects = find_pre_tge_projects()
    for g in projects:
        print(f"Pre-TGE Project found: {g.title} ({g.username or g.tg_id})")
        report_data.append([
            "Pre-TGE",
            g.title,
            "N/A",
            "N/A",
            "Keyword Match in Title",
            datetime.datetime.now().isoformat()
        ])

    if report_data:
        print("Sending report to Google Sheets...")
        update_google_sheet(report_data)
    else:
        print("No data to report.")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [login|scan <link>|report|auto|export-session]")
        return

    command = sys.argv[1]

    if command == "login":
        await client.start(phone=PHONE)
        print("Successfully logged in.")

    elif command == "scan":
        if len(sys.argv) < 3:
            print("Please provide a group link.")
            return
        link = sys.argv[2]
        await client.start(phone=PHONE)
        print(f"Joining and scanning {link}...")
        entity = await join_group(link)
        if entity:
            await scan_admins(entity)
            print(f"Scan complete for {entity.title}")

    elif command == "report":
        await run_report()

    elif command == "auto":
        # Full automated pipeline: read links → scan → analyze → export
        links = get_group_links()
        if not links:
            print("No group links found in Watchlist sheet.")
        else:
            print(f"Found {len(links)} groups in Watchlist.")
            await client.start(phone=PHONE)
            for link in links:
                print(f"Scanning {link}...")
                entity = await join_group(link)
                if entity:
                    await scan_admins(entity)
                    print(f"Scan complete for {entity.title}")
            await client.disconnect()

        await run_report()

    elif command == "export-session":
        await client.start(phone=PHONE)
        session_string = StringSession.save(client.session)
        print("Copy this SESSION_STRING into your Render environment variables:\n")
        print(session_string)

if __name__ == '__main__':
    asyncio.run(main())
