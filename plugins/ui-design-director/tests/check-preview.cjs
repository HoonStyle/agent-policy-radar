// Optional browser verification using an existing Playwright + Chrome installation.
// No dev server, watcher, downloads, or changes to browser/user settings.
const { chromium } = require(process.env.DESIGN_PLAYWRIGHT_PATH || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const root = path.resolve(__dirname, '..');

(async () => {
  const out = path.join(root, 'artifacts');
  const screenshots = path.join(out, 'screenshots-v0.2.0');
  fs.mkdirSync(screenshots, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const results = [];
  const errors = [];
  try {
    for (const family of ['paper-olive', 'mineral-violet']) {
      const data = JSON.parse(fs.readFileSync(path.join(root, 'skills/design-director/assets/palettes', family + '.json')));
      for (const width of [1280, 390, 320]) {
        const page = await browser.newPage({ viewport: { width, height: 1000 }, reducedMotion: 'reduce' });
        page.on('pageerror', error => errors.push(String(error)));
        page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
        page.on('request', request => { assert(!/^https?:/.test(request.url()), 'Specimen must not request the network'); });
        await page.goto(pathToFileURL(path.join(out, family + '.html')).href);
        for (const lang of ['ko', 'en']) {
        await page.locator('#language').selectOption(lang);
        const words = lang === 'ko'
          ? {theme:'테마', select:'항목 선택', clear:'선택 해제', project:'프로젝트 이름', validate:'입력 확인', error:'프로젝트 이름을 입력해 주세요.', success:'입력 확인 완료'}
          : {theme:'Theme', select:'Select item', clear:'Clear selection', project:'Project name', validate:'Check input', error:'Enter a project name.', success:'Input checked'};
        for (const theme of ['light', 'dark']) {
          await page.getByLabel(words.theme, { exact: true }).selectOption(theme);
          assert.equal(await page.locator('html').getAttribute('lang'), lang);
          assert.equal(await page.locator('html').getAttribute('data-theme'), theme);
          assert.equal(await page.locator('[data-palette]:visible').count(), 1);
          const actualCanvas = await page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue('--ui-canvas').trim());
          assert.equal(actualCanvas, data.themes[theme].tokens.canvas);
          const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
          assert.equal(overflow, false, family + ' ' + lang + ' ' + theme + ' ' + width + ' overflow');
          const select = page.getByRole('button', { name: words.select, exact: true });
          await select.click();
          assert.equal(await select.getAttribute('aria-pressed'), 'true');
          assert(await page.locator('#selected').isVisible());
          assert((await page.locator('#selected').textContent()).includes(lang === 'ko' ? '1,240건' : '1,240 records'));
          assert((await page.locator('#selected').textContent()).includes(lang === 'ko' ? '2026.' : 'Oct 8, 2026'));
          await page.getByRole('button', { name: words.clear, exact: true }).click();
          assert.equal(await select.getAttribute('aria-pressed'), 'false');
          assert.equal(await page.locator('#selected').isVisible(), false);
          const input = page.getByLabel(words.project, { exact: true });
          const placeholder = await input.evaluate(el => getComputedStyle(el, '::placeholder').color);
          const mutedHex = data.themes[theme].tokens.muted.slice(1);
          const mutedRGB = [0, 2, 4].map(i => parseInt(mutedHex.slice(i, i + 2), 16));
          assert.equal(placeholder, `rgb(${mutedRGB.join(', ')})`);
          await input.fill('');
          await page.getByRole('button', { name: words.validate, exact: true }).click();
          assert.equal(await input.getAttribute('aria-invalid'), 'true');
          assert(await page.locator('#field-error').isVisible());
          assert.equal(await page.locator('#field-error').textContent(), words.error);
          assert.equal(await page.evaluate(() => document.activeElement.id), 'project');
          const otherLanguage = lang === 'ko' ? 'en' : 'ko';
          await page.locator('#language').focus();
          await page.locator('#language').selectOption(otherLanguage);
          assert.equal(await page.locator('#project').getAttribute('aria-invalid'), 'true');
          assert(await page.locator('#field-error').isVisible());
          assert.equal(await page.evaluate(() => document.activeElement.id), 'language');
          await page.locator('#language').selectOption(lang);
          const entered = lang === 'ko' ? '출고 검수 API v2 · 긴 프로젝트 이름 1,240건' : 'Dispatch inspection API v2 with an unusually long project name';
          await input.fill(entered);
          await page.getByRole('button', { name: words.validate, exact: true }).click();
          assert.equal(await input.getAttribute('aria-invalid'), 'false');
          assert((await page.getByRole('status').textContent()).includes(words.success));
          assert.equal(await page.locator('#field-error').isVisible(), false);
          await page.getByLabel(words.theme, { exact: true }).focus();
          await page.keyboard.press('Tab');
          assert.equal(await page.evaluate(() => document.activeElement.id), 'select-item');
          const focusStyle = await select.evaluate(el => getComputedStyle(el).outlineStyle);
          assert.notEqual(focusStyle, 'none');
          await page.keyboard.press('Space');
          assert.equal(await select.getAttribute('aria-pressed'), 'true');
          await page.locator('#language').selectOption(otherLanguage);
          assert.equal(await page.locator('#project').inputValue(), entered);
          assert.equal(await page.locator('#select-item').getAttribute('aria-pressed'), 'true');
          assert.equal(await page.locator('#theme').inputValue(), theme);
          assert((await page.getByRole('status').textContent()).includes(otherLanguage === 'ko' ? '입력 확인 완료' : 'Input checked'));
          await page.locator('#language').selectOption(lang);
          // Check English UI copy, including collapsed results, excluding language autonyms and user values.
          if (lang === 'en') {
            const untranslated = await page.evaluate(() => Array.from(document.querySelectorAll('[data-i18n], [data-i18n-aria], [data-i18n-placeholder]')).some(el => /[가-힣]/.test(el.textContent + (el.getAttribute('aria-label') || '') + (el.getAttribute('placeholder') || ''))));
            assert.equal(untranslated, false);
            assert((await page.title()).endsWith('Color review'));
          }
          // Text expansion must not be solved by shrinking or clipping button labels.
          const originalLabel = await page.locator('#select-item').textContent();
          await page.locator('#select-item').evaluate(el => {el.textContent = 'Resend the review request to the assigned reviewer';});
          assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
          const clipped = await page.locator('#select-item').evaluate(el => el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight);
          assert.equal(clipped, false);
          await page.locator('#select-item').evaluate((el, text) => {el.textContent = text;}, originalLabel);
          await input.fill('');
          await page.locator('h1').click();
          await page.screenshot({ path: path.join(screenshots, `${family}-${lang}-${theme}-${width}.png`), fullPage: true });
          // Restore state so the next theme starts with no selection.
          await page.getByRole('button', { name: words.clear, exact: true }).click();
          results.push({ family, lang, theme, width, overflow: false, interactions: 'pass', screenshot: `${family}-${lang}-${theme}-${width}.png` });
        }
        }
        await page.close();
      }
    }
    assert.deepEqual(errors, []);
    // A directly generated English entry point must work even before script execution.
    const staticEnglish = await browser.newPage({ javaScriptEnabled: false });
    await staticEnglish.goto(pathToFileURL(path.join(out, 'paper-olive-en.html')).href);
    assert.equal(await staticEnglish.locator('html').getAttribute('lang'), 'en');
    assert(await staticEnglish.getByRole('button', { name: 'Select item', exact: true }).isVisible());
    assert.equal(await staticEnglish.locator('#language').inputValue(), 'en');
    await staticEnglish.close();
    fs.writeFileSync(path.join(out, 'browser-results-v0.2.0.json'), JSON.stringify({ browser: browser.version(), cases: results, staticEnglish:'pass', errors }, null, 2));
    console.log(JSON.stringify({ casesPassed: results.length, screenshots: results.length, errors }, null, 2));
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
