"""Route Crawler — uses Playwright async API to map target application routes."""
import asyncio
from urllib.parse import urljoin, urlparse

from playwright.async_api import async_playwright

from app.services.sse_manager import sse_manager


async def crawl_target(target_url: str, scan_id: str) -> list[dict]:
    """
    Crawl the target URL and discover routes, forms, and auth pages.
    Returns a list of discovered route dicts.
    """
    discovered = []
    visited = set()
    base_domain = urlparse(target_url).netloc

    sse_manager.publish(scan_id, "crawl_started", {"target_url": target_url})

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            ignore_https_errors=True,
            user_agent="SpecterTest-Crawler/1.0",
        )

        async def _crawl_page(url: str, depth: int = 0):
            """Recursively crawl pages up to depth 2."""
            if depth > 2 or url in visited:
                return
            visited.add(url)

            try:
                page = await context.new_page()
                response = await page.goto(url, wait_until="domcontentloaded", timeout=15000)

                if response is None:
                    await page.close()
                    return

                # Get page title
                title = await page.title()

                # Detect forms
                forms = await page.eval_on_selector_all(
                    "form",
                    """elements => elements.map(e => ({
                        action: e.action || '',
                        method: (e.method || 'GET').toUpperCase()
                    }))""",
                )
                has_form = len(forms) > 0

                # Detect auth pages (login/register patterns)
                has_auth = await page.eval_on_selector_all(
                    "input[type='password'], input[name*='login'], input[name*='email']",
                    "els => els.length > 0",
                )

                # Record this route
                path = urlparse(url).path or "/"
                route_info = {
                    "path": path,
                    "method": "GET",
                    "has_form": has_form,
                    "has_auth": has_auth,
                    "page_title": title,
                }
                discovered.append(route_info)

                # Publish SSE event
                sse_manager.publish(scan_id, "route_discovered", route_info)

                # Record form endpoints too
                for form in forms:
                    form_path = urlparse(form["action"]).path if form["action"] else path
                    form_route = {
                        "path": form_path,
                        "method": form["method"],
                        "has_form": True,
                        "has_auth": has_auth,
                        "page_title": f"Form on {title}",
                    }
                    if form_path not in [r["path"] for r in discovered]:
                        discovered.append(form_route)
                        sse_manager.publish(scan_id, "route_discovered", form_route)

                # Extract links for further crawling
                links = await page.eval_on_selector_all(
                    "a[href]",
                    "elements => elements.map(e => e.href)",
                )

                await page.close()

                # Crawl child links (same domain only)
                for link in links:
                    full_url = urljoin(url, link)
                    parsed = urlparse(full_url)
                    if parsed.netloc == base_domain and full_url not in visited:
                        await _crawl_page(full_url, depth + 1)

            except Exception as e:
                sse_manager.publish(scan_id, "crawl_error", {
                    "url": url, "error": str(e)
                })

        await _crawl_page(target_url)
        await browser.close()

    sse_manager.publish(scan_id, "crawl_completed", {
        "total_routes": len(discovered)
    })

    return discovered


def run_crawler(target_url: str, scan_id: str) -> list[dict]:
    """Synchronous wrapper to run the async crawler."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(
                    asyncio.run, crawl_target(target_url, scan_id)
                ).result()
        else:
            return loop.run_until_complete(crawl_target(target_url, scan_id))
    except RuntimeError:
        return asyncio.run(crawl_target(target_url, scan_id))
