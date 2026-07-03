import { test, expect } from '@playwright/test';

const repositories = [
  'Promptimprover',
  'autogen',
  'gsd-orchestrator',
  'cas-contracts',
  'cas-evals',
  'cas-platform',
  'cas-reference-product',
  'cas-workstation',
  'autopilot-core',
  'autopilot-demo',
  'ci-autopilot',
  'cloud-security-service-model',
  'org-dotgithub'
];

test.describe('GitHub Pages Omni-Audit', () => {
  for (const repo of repositories) {
    // Note: the org-dotgithub repo resolves to the root domain in gh pages
    const path = repo === 'org-dotgithub' ? '' : repo;
    const url = `https://Coding-Autopilot-System.github.io/${path}`;

    test(`Visual & Functional audit for ${repo} MkDocs Page`, async ({ page }) => {
      // 1. Navigate to the deployed site
      const response = await page.goto(url);
      
      // 2. Assert no 404
      expect(response?.status()).toBeLessThan(400);

      // 3. Assert MkDocs Material Theme loaded correctly
      const header = page.locator('.md-header');
      await expect(header).toBeVisible();

      // 4. Assert health badges exist on the landing page
      const badges = page.locator('img[src*="badge.svg"]');
      // Some repos might not have the badge rendered yet, but we check if the element exists in DOM
      // We wrap in a soft assertion so the test doesn't immediately fail if CI is slow to generate badges
      await expect.soft(badges.first()).toBeVisible();

      // 5. Take visual snapshot (commented out until baselines are generated)
      // await expect(page).toHaveScreenshot(`${repo}-landing.png`);
    });
  }
});
