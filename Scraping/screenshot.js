const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Define the URL of the Gist page
  const gistUrl = 'https://gist.github.com/shrayasr/b317293e9ab5de3718bf';

  await page.goto(gistUrl);
  await page.screenshot({ path: 'gist_snapshot.png' });

  await browser.close();
})();
