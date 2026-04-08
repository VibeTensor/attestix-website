"""E2E tests for all demo pages + nav links using Python Playwright."""
import sys
from playwright.sync_api import sync_playwright, expect

BASE = "http://localhost:3850"

def main():
    results = []

    def check(name, fn):
        try:
            fn()
            results.append((name, True, ""))
        except Exception as e:
            results.append((name, False, str(e)[:200]))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # ── Demo Landing Page ──
        print("\n" + "=" * 50)
        print("  Demo Landing Page")
        print("=" * 50)

        page.goto(f"{BASE}/demo", timeout=30000)

        def _demo_title():
            h1 = page.locator("h1").first
            expect(h1).to_contain_text("Interactive Demos")
        check("Demo page title visible", _demo_title)

        def _demo_4_cards():
            cards = page.locator('a[href*="/demo/"]').all()
            assert len(cards) >= 4, f"Expected 4+ cards, got {len(cards)}"
        check("4 demo cards rendered", _demo_4_cards)

        def _compliance_card():
            expect(page.locator('a[href="/demo/compliance-checker"]')).to_be_visible()
        check("Compliance checker card", _compliance_card)

        def _fine_card():
            expect(page.locator('a[href="/demo/fine-calculator"]')).to_be_visible()
        check("Fine calculator card", _fine_card)

        def _identity_card():
            expect(page.locator('a[href="/demo/identity-explorer"]')).to_be_visible()
        check("Identity explorer card", _identity_card)

        def _reputation_card():
            expect(page.locator('a[href="/demo/reputation-dashboard"]')).to_be_visible()
        check("Reputation dashboard card", _reputation_card)

        def _demo_cta():
            expect(page.locator('a[href="/docs/getting-started"]').first).to_be_visible()
        check("CTA buttons present", _demo_cta)

        # ── Identity Explorer ──
        print("\n" + "=" * 50)
        print("  Identity Explorer")
        print("=" * 50)

        page.goto(f"{BASE}/demo/identity-explorer", timeout=30000)

        def _ie_heading():
            expect(page.locator("h1")).to_contain_text("identity", ignore_case=True)
        check("Page heading", _ie_heading)

        def _ie_form():
            expect(page.locator("#agent-name")).to_be_visible()
        check("Configuration form visible", _ie_form)

        def _ie_caps():
            expect(page.get_by_text("Data Analysis")).to_be_visible()
        check("Capability buttons visible", _ie_caps)

        def _ie_risk():
            expect(page.get_by_text("Minimal").first).to_be_visible()
        check("Risk level selector visible", _ie_risk)

        def _ie_create_flow():
            page.fill("#agent-name", "Test Bot")
            page.fill("#agent-description", "A test agent")
            page.fill("#issuer-org", "Test Corp")
            # Click a capability button - use exact match
            page.get_by_text("Data Analysis", exact=True).click()
            page.wait_for_timeout(300)
            # Now the Create Identity button should be enabled
            create_btn = page.locator("button", has_text="Create Identity")
            expect(create_btn).to_be_enabled(timeout=3000)
            create_btn.click()
            expect(page.get_by_text("Test Bot").first).to_be_visible(timeout=5000)
            expect(page.get_by_text("attestix:").first).to_be_visible(timeout=5000)
        check("Create identity flow works", _ie_create_flow)

        def _ie_did():
            expect(page.get_by_text("did:key:").first).to_be_visible()
        check("Identity card shows DID", _ie_did)

        def _ie_trust():
            expect(page.get_by_text("Trust Score").first).to_be_visible()
        check("Identity card shows trust score", _ie_trust)

        def _ie_accordion():
            expect(page.get_by_text("What is this?")).to_be_visible()
            expect(page.get_by_text("Raw JSON")).to_be_visible()
        check("Explore accordion sections exist", _ie_accordion)

        def _ie_cta():
            expect(page.get_by_text("Create real agent identities")).to_be_visible()
        check("CTA section visible", _ie_cta)

        # ── Reputation Dashboard ──
        print("\n" + "=" * 50)
        print("  Reputation Dashboard")
        print("=" * 50)

        page.goto(f"{BASE}/demo/reputation-dashboard", timeout=30000)

        def _rd_heading():
            expect(page.locator("h1")).to_contain_text("reputation", ignore_case=True)
        check("Dashboard heading", _rd_heading)

        def _rd_agents():
            expect(page.get_by_text("MedAssist Pro").first).to_be_visible()
            expect(page.get_by_text("CodeBot v3").first).to_be_visible()
        check("Agent selector cards visible", _rd_agents)

        def _rd_gauge():
            svgs = page.locator("svg").all()
            assert len(svgs) >= 1, "No SVG elements found"
        check("Trust gauge visible", _rd_gauge)

        def _rd_categories():
            expect(page.get_by_text("Compliance").first).to_be_visible()
            expect(page.get_by_text("Accuracy").first).to_be_visible()
            expect(page.get_by_text("Safety").first).to_be_visible()
        check("Category breakdown visible", _rd_categories)

        def _rd_interactions():
            expect(page.get_by_text("Success").first).to_be_visible()
            expect(page.get_by_text("Partial").first).to_be_visible()
            expect(page.get_by_text("Failure").first).to_be_visible()
        check("Interaction history donut", _rd_interactions)

        def _rd_timeline():
            expect(page.get_by_text("Trust Score Timeline")).to_be_visible()
        check("Timeline chart visible", _rd_timeline)

        def _rd_simulate():
            expect(page.get_by_text("Record Success")).to_be_visible()
        check("Simulate controls visible", _rd_simulate)

        def _rd_switch():
            page.get_by_text("CodeBot v3").click()
            page.wait_for_timeout(500)
            h2 = page.locator("h2").first
            expect(h2).to_contain_text("CodeBot")
        check("Agent selection changes view", _rd_switch)

        def _rd_sim_interaction():
            page.get_by_text("Record Success").click()
            page.wait_for_timeout(500)
            expect(page.get_by_text("Reset")).to_be_visible()
        check("Simulate interaction updates score", _rd_sim_interaction)

        def _rd_cta():
            expect(page.get_by_text("Build real reputation tracking")).to_be_visible()
        check("CTA section present", _rd_cta)

        # ── Navigation Links ──
        print("\n" + "=" * 50)
        print("  Navigation Links")
        print("=" * 50)

        page.goto(f"{BASE}/", timeout=30000)

        def _nav_demos():
            nav = page.locator("nav")
            demos_link = nav.locator('a[href="/demo"]')
            expect(demos_link).to_be_visible()
            expect(demos_link).to_contain_text("Demos")
        check("Demos link in header nav", _nav_demos)

        # ── Existing Demos ──
        print("\n" + "=" * 50)
        print("  Existing Demos Still Work")
        print("=" * 50)

        page.goto(f"{BASE}/demo/compliance-checker", timeout=30000)

        def _cc_loads():
            h1 = page.locator("h1")
            expect(h1).to_be_visible(timeout=10000)
        check("Compliance checker loads", _cc_loads)

        page.goto(f"{BASE}/demo/fine-calculator", timeout=30000)

        def _fc_loads():
            h1 = page.locator("h1")
            expect(h1).to_be_visible(timeout=10000)
        check("Fine calculator loads", _fc_loads)

        browser.close()

    # Print results
    passed = sum(1 for _, p, _ in results if p)
    failed = sum(1 for _, p, _ in results if not p)

    for name, p, err in results:
        status = "PASS" if p else "FAIL"
        line = f"  [{status}] {name}"
        if not p:
            print(line)
            print(f"         {err}")
        else:
            print(line)

    print(f"\n{'='*50}")
    print(f"  TOTAL: {passed} passed, {failed} failed out of {len(results)}")
    print(f"{'='*50}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
