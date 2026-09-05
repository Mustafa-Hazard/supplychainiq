import { test, expect, type Page } from '@playwright/test';

/**
 * Portfolio demo walkthrough for Threat Intelligence Dashboard.
 *
 * Captures: Overview (AI briefing) -> Threats (sort/filter ~1795 rows) -> Trends (chart).
 * Run with the app already up: `docker compose up -d --build` (or `npm run dev` for frontend
 * on :5173 + backend on :8000).
 *
 * Screenshots land in test-results/screenshots/. Video is auto-recorded per playwright.config.ts
 * into test-results/videos/.
 *
 * Run:
 *   npx playwright test demo_walkthrough.spec.ts --headed --project=chromium
 */

const BASE_URL = process.env.DEMO_BASE_URL ?? 'http://localhost:5173';
const SCREENSHOT_DIR = 'test-results/screenshots';

// Small helper so the recording doesn't look like a robot filling forms instantly.
async function pause(page: Page, ms = 900) {
  await page.waitForTimeout(ms);
}

test.describe('Portfolio walkthrough', () => {
  test.use({
    viewport: { width: 2560, height: 1600 },
  });

  test('Overview -> Threats -> Trends', async ({ page }) => {
    // ---------- 1. OVERVIEW ----------
    await page.goto(BASE_URL);
    await expect(page.getByRole('heading', { name: 'Threat Intelligence Dashboard' })).toBeVisible();

    // Wait for the AI briefing to finish loading (SummaryPanel fetches on mount).
    await expect(page.getByText('loading', { exact: false })).toHaveCount(0, { timeout: 15_000 });
    await expect(page.getByRole('heading', { name: 'Daily Briefing' })).toBeVisible();
    await pause(page, 2500); // let the briefing text sit on screen for the recording

    await page.screenshot({ path: `${SCREENSHOT_DIR}/01-overview.png`, fullPage: true });

    // ---------- 2. THREATS ----------
    await page.getByRole('link', { name: 'Threats' }).click();
    await expect(page).toHaveURL(/\/threats$/);
    await expect(page.getByRole('heading', { name: 'Top Threats' })).toBeVisible();

    // Wait for the real dataset to load (no more "loading threats...")
    await expect(page.getByText('loading threats', { exact: false })).toHaveCount(0, { timeout: 15_000 });
    await pause(page, 1500);
    await page.screenshot({ path: `${SCREENSHOT_DIR}/02-threats-default.png`, fullPage: true });

    // Sort by published date (click the "published" column header) to show interactivity.
    await page.getByText('published', { exact: false }).click();
    await pause(page, 1200);
    await page.screenshot({ path: `${SCREENSHOT_DIR}/03-threats-sorted-by-date.png`, fullPage: true });

    // Flip sort direction back (second click on same header reverses asc/desc).
    await page.getByText('published', { exact: false }).click();
    await pause(page, 800);

    // Filter by tag via the real <select> (options are "all tags", "untagged", then dynamic tags).
    const tagSelect = page.locator('select');
    const optionValues = await tagSelect.locator('option').allTextContents();
    const realTag = optionValues.find((t) => t !== 'all tags' && t !== 'untagged');
    if (realTag) {
      await tagSelect.selectOption({ label: realTag });
      await pause(page, 1400);
      await page.screenshot({ path: `${SCREENSHOT_DIR}/04-threats-filtered-${realTag}.png`, fullPage: true });
      // Reset back to "all tags" before moving on
      await tagSelect.selectOption({ label: 'all tags' });
      await pause(page, 600);
    }

    // Back to priority sort (default) for a clean final shot of this page.
    await page.getByText('priority', { exact: false }).first().click();
    await pause(page, 1000);

    // ---------- 3. TRENDS ----------
    await page.getByRole('link', { name: 'Trends' }).click();
    await expect(page).toHaveURL(/\/trends$/);

    // TrendChart renders via Recharts (SVG) — give it time to fetch + animate in.
    await pause(page, 2500);
    await page.screenshot({ path: `${SCREENSHOT_DIR}/05-trends.png`, fullPage: true });

    // Hold on the final frame a beat longer so the video has a clean ending point.
    await pause(page, 2000);
  });
});
