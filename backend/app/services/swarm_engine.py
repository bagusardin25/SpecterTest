"""Swarm Simulation Engine — parallel agent execution via Playwright contexts."""
import asyncio
import json
import random
import time
from urllib.parse import urljoin

from playwright.async_api import async_playwright

from app.services.sse_manager import sse_manager

# Attack payloads for attacker agents
SQLI_PAYLOADS = [
    "' OR '1'='1' --",
    "'; DROP TABLE users; --",
    "1 UNION SELECT * FROM users",
    "admin'--",
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(document.cookie)",
    "<svg/onload=alert('xss')>",
]

PATH_TRAVERSAL_PAYLOADS = [
    "../../etc/passwd",
    "../../../etc/shadow",
    "..\\..\\windows\\system32\\config\\sam",
]


async def run_agent_user(agent_dict: dict, page, routes: list[dict], scan_id: str) -> list[dict]:
    """User agent — browses normally, fills forms with valid data."""
    findings = []
    actions_log = []

    for route in random.sample(routes, min(len(routes), 5)):
        action = f"Browsing {route['path']}"
        sse_manager.publish(scan_id, "agent_action", {
            "agent_id": agent_dict["id"],
            "action": action,
            "target_path": route["path"],
        })
        actions_log.append({"action": action, "timestamp": time.time()})

        try:
            url = urljoin(page.url, route["path"])
            response = await page.goto(url, wait_until="domcontentloaded", timeout=10000)

            if response and response.status >= 500:
                finding = {
                    "agent_id": agent_dict["id"],
                    "category": "performance_issue",
                    "severity": "medium",
                    "title": f"Server Error {response.status} on {route['path']}",
                    "description": f"Agent {agent_dict['id']} received HTTP {response.status} when accessing {route['path']}",
                    "evidence": f"GET {route['path']} → HTTP {response.status}",
                }
                findings.append(finding)
                sse_manager.publish(scan_id, "finding_discovered", finding)

            # If page has form, fill and submit with normal data
            if route.get("has_form"):
                inputs = await page.query_selector_all("input:not([type='hidden'])")
                for inp in inputs[:3]:
                    inp_type = await inp.get_attribute("type") or "text"
                    if inp_type == "email":
                        await inp.fill("testuser@example.com")
                    elif inp_type == "password":
                        await inp.fill("TestPassword123!")
                    else:
                        await inp.fill("test_value")

                actions_log.append({
                    "action": f"Filled form on {route['path']}",
                    "timestamp": time.time(),
                })

        except Exception as e:
            actions_log.append({
                "action": f"Error on {route['path']}: {str(e)[:100]}",
                "timestamp": time.time(),
            })

        await asyncio.sleep(random.uniform(0.5, 1.5))

    return findings


async def run_agent_admin(agent_dict: dict, page, routes: list[dict], scan_id: str) -> list[dict]:
    """Admin agent — attempts to access admin-like endpoints."""
    findings = []
    admin_paths = [r for r in routes if any(
        kw in r["path"].lower() for kw in ["admin", "dashboard", "manage", "config", "settings", "api"]
    )]

    # Also check some common admin paths that may not have been crawled
    common_admin = ["/admin", "/dashboard", "/api/users", "/api/config", "/settings"]
    for path in common_admin:
        if not any(r["path"] == path for r in admin_paths):
            admin_paths.append({"path": path, "method": "GET", "has_form": False, "has_auth": False})

    for route in admin_paths[:8]:
        action = f"Accessing admin endpoint {route['path']}"
        sse_manager.publish(scan_id, "agent_action", {
            "agent_id": agent_dict["id"],
            "action": action,
            "target_path": route["path"],
        })

        try:
            url = urljoin(page.url, route["path"])
            response = await page.goto(url, wait_until="domcontentloaded", timeout=10000)

            if response and response.status == 200:
                # Check if we can access admin without auth — potential finding
                body_text = await page.inner_text("body")
                if any(kw in body_text.lower() for kw in ["admin", "dashboard", "users", "management"]):
                    finding = {
                        "agent_id": agent_dict["id"],
                        "category": "security_issue",
                        "severity": "high",
                        "title": f"Unauthenticated Admin Access at {route['path']}",
                        "description": f"Agent {agent_dict['id']} accessed admin panel at {route['path']} without authentication.",
                        "evidence": f"GET {route['path']} → HTTP 200 (admin content visible)",
                    }
                    findings.append(finding)
                    sse_manager.publish(scan_id, "finding_discovered", finding)

        except Exception:
            pass

        await asyncio.sleep(random.uniform(0.3, 1.0))

    return findings


async def run_agent_attacker(agent_dict: dict, page, routes: list[dict], scan_id: str) -> list[dict]:
    """Attacker agent — injects payloads, tests IDOR, path traversal."""
    findings = []

    for route in routes[:6]:
        # --- SQLi / XSS on form pages ---
        if route.get("has_form"):
            for payload_set, attack_name, category in [
                (SQLI_PAYLOADS, "SQL Injection", "security_issue"),
                (XSS_PAYLOADS, "XSS", "security_issue"),
            ]:
                payload = random.choice(payload_set)
                action = f"Testing {attack_name} on {route['path']} with payload"
                sse_manager.publish(scan_id, "agent_action", {
                    "agent_id": agent_dict["id"],
                    "action": action,
                    "target_path": route["path"],
                })

                try:
                    url = urljoin(page.url, route["path"])
                    await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                    inputs = await page.query_selector_all("input:not([type='hidden'])")
                    for inp in inputs[:2]:
                        await inp.fill(payload)

                    # Try to submit
                    submit = await page.query_selector("button[type='submit'], input[type='submit']")
                    if submit:
                        await submit.click()
                        await asyncio.sleep(1)

                        body = await page.inner_text("body")
                        # Check for error reflection (basic vuln detection)
                        if payload in body or "sql" in body.lower() or "syntax" in body.lower():
                            finding = {
                                "agent_id": agent_dict["id"],
                                "category": category,
                                "severity": "critical",
                                "title": f"{attack_name} Vulnerability on {route['path']}",
                                "description": f"Payload was reflected or caused SQL error on {route['path']}",
                                "evidence": f"Payload: {payload}\nResponse contained indicators of vulnerability",
                            }
                            findings.append(finding)
                            sse_manager.publish(scan_id, "finding_discovered", finding)

                except Exception:
                    pass

        # --- IDOR test ---
        if any(seg.isdigit() for seg in route["path"].split("/")):
            action = f"Testing IDOR on {route['path']}"
            sse_manager.publish(scan_id, "agent_action", {
                "agent_id": agent_dict["id"],
                "action": action,
                "target_path": route["path"],
            })

            try:
                # Replace numeric segment with another ID
                parts = route["path"].split("/")
                for i, part in enumerate(parts):
                    if part.isdigit():
                        original = part
                        parts[i] = str(int(part) + 1)
                        idor_path = "/".join(parts)
                        url = urljoin(page.url, idor_path)
                        response = await page.goto(url, wait_until="domcontentloaded", timeout=10000)

                        if response and response.status == 200:
                            finding = {
                                "agent_id": agent_dict["id"],
                                "category": "logic_flaw",
                                "severity": "critical",
                                "title": f"IDOR Vulnerability at {route['path']}",
                                "description": f"Changed ID from {original} to {parts[i]} and received HTTP 200",
                                "evidence": f"GET {idor_path} → HTTP 200 (unauthorized access)",
                            }
                            findings.append(finding)
                            sse_manager.publish(scan_id, "finding_discovered", finding)
                        break
            except Exception:
                pass

        await asyncio.sleep(random.uniform(0.3, 0.8))

    return findings


async def run_simulation_async(
    target_url: str,
    scan_id: str,
    agents_data: list[dict],
    routes: list[dict],
) -> list[dict]:
    """
    Run all agents in parallel using separate Playwright browser contexts.
    Returns aggregated list of findings.
    """
    all_findings = []
    start_time = time.time()

    sse_manager.publish(scan_id, "simulation_started", {
        "total_agents": len(agents_data),
        "total_routes": len(routes),
    })

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        async def _run_single_agent(agent_dict: dict) -> list[dict]:
            """Run a single agent in its own browser context."""
            context = await browser.new_context(
                ignore_https_errors=True,
                user_agent=f"SpecterTest-Agent/{agent_dict['id']}",
            )
            page = await context.new_page()

            try:
                await page.goto(target_url, wait_until="domcontentloaded", timeout=15000)
            except Exception:
                await context.close()
                return []

            try:
                role = agent_dict["role"]
                if role == "user":
                    results = await run_agent_user(agent_dict, page, routes, scan_id)
                elif role == "admin":
                    results = await run_agent_admin(agent_dict, page, routes, scan_id)
                elif role == "attacker":
                    results = await run_agent_attacker(agent_dict, page, routes, scan_id)
                else:
                    results = []
            except Exception as e:
                sse_manager.publish(scan_id, "agent_error", {
                    "agent_id": agent_dict["id"],
                    "error": str(e)[:200],
                })
                results = []
            finally:
                await context.close()

            return results

        # Run all agents in parallel
        tasks = [_run_single_agent(agent) for agent in agents_data]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, list):
                all_findings.extend(result)

        await browser.close()

    elapsed = int(time.time() - start_time)

    sse_manager.publish(scan_id, "simulation_completed", {
        "total_findings": len(all_findings),
        "duration_seconds": elapsed,
    })

    return all_findings


def run_simulation(
    target_url: str,
    scan_id: str,
    agents_data: list[dict],
    routes: list[dict],
) -> list[dict]:
    """Synchronous wrapper for the async simulation engine."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(
                    asyncio.run,
                    run_simulation_async(target_url, scan_id, agents_data, routes),
                ).result()
        else:
            return loop.run_until_complete(
                run_simulation_async(target_url, scan_id, agents_data, routes)
            )
    except RuntimeError:
        return asyncio.run(
            run_simulation_async(target_url, scan_id, agents_data, routes)
        )
