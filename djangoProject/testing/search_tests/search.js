const puppeteer = require('puppeteer');

(async () => {

    const browser = await puppeteer.launch({ headless: false});
    const page = await browser.newPage();
    const navigationPromise = page.waitForNavigation({waitUntil: "domcontentloaded"});

    await page.setViewport({width:1535, height:1200});
    await page.goto('http://127.0.0.1:8000/lookup');
    await navigationPromise;

    const search = await page.waitForSelector('#autocomplete > input');
    await search.type('Thief');
    await page.waitFor(2000);
    await page.screenshot({path: 'search_input.png'});
    
    const result = await page.waitForSelector('#autocomplete-result-0');
    await result.click();
    await page.waitFor(2000);
    await page.screenshot({path: 'search_result.png'});

    await browser.close();

})();