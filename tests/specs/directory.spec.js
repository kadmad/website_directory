// @ts-check
const { test, expect } = require('@playwright/test');

const DARK_PINK = 'rgb(194, 24, 91)';
const TRANSPARENT = 'rgba(0, 0, 0, 0)';

test.describe('Root URL redirect', () => {
  test('redirects / to /websites/', async ({ page }) => {
    await page.goto('/');
    await page.waitForURL('**/websites/**');
    expect(page.url()).toContain('/websites/');
    await expect(page.locator('h2')).toContainText('Directory List');
  });
});

test.describe('KPI badge styling', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/websites/');
  });

  test('DA badge has dark pink border and transparent background', async ({ page }) => {
    const daButton = page.locator('.custom-button').filter({ hasText: 'DA:' }).first();
    await expect(daButton).toBeVisible();

    const borderColor = await daButton.evaluate(el =>
      getComputedStyle(el).borderTopColor
    );
    const bgColor = await daButton.evaluate(el =>
      getComputedStyle(el).backgroundColor
    );

    expect(borderColor).toBe(DARK_PINK);
    expect(bgColor).toBe(TRANSPARENT);
  });

  test('DA badge text is dark pink', async ({ page }) => {
    const daButton = page.locator('.custom-button').filter({ hasText: 'DA:' }).first();
    await expect(daButton).toBeVisible();

    const color = await daButton.evaluate(el => getComputedStyle(el).color);
    expect(color).toBe(DARK_PINK);
  });

  test('all 5 KPI badges have consistent dark pink styling', async ({ page }) => {
    const firstCard = page.locator('li.media').first();
    await expect(firstCard).toBeVisible();

    const buttons = firstCard.locator('.custom-button');
    const count = await buttons.count();
    expect(count).toBe(5);

    for (let i = 0; i < count; i++) {
      const btn = buttons.nth(i);
      const borderColor = await btn.evaluate(el => getComputedStyle(el).borderTopColor);
      const bgColor = await btn.evaluate(el => getComputedStyle(el).backgroundColor);
      const textColor = await btn.evaluate(el => getComputedStyle(el).color);

      expect(borderColor).toBe(DARK_PINK);
      expect(bgColor).toBe(TRANSPARENT);
      expect(textColor).toBe(DARK_PINK);
    }
  });
});

test.describe('Create website and verify KPI badges', () => {
  test('new entry appears with dark pink KPI badges', async ({ page }) => {
    await page.goto('/websites/create/');
    await expect(page.locator('form')).toBeVisible();

    const domainInput = page.locator('input[name="domain"]');
    await domainInput.fill('playwright-test-site.com');

    const categorySelect = page.locator('select[name="category"]');
    if (await categorySelect.count() > 0) {
      await categorySelect.selectOption({ index: 1 });
    }

    await page.locator('button[type="submit"], input[type="submit"]').click();
    await page.waitForURL('**/websites/**');

    // Find the newly created entry
    const newEntry = page.locator('li.media').filter({ hasText: 'playwright-test-site.com' });
    await expect(newEntry).toBeVisible();

    const daButton = newEntry.locator('.custom-button').first();
    const borderColor = await daButton.evaluate(el => getComputedStyle(el).borderTopColor);
    const bgColor = await daButton.evaluate(el => getComputedStyle(el).backgroundColor);

    expect(borderColor).toBe(DARK_PINK);
    expect(bgColor).toBe(TRANSPARENT);
  });
});
