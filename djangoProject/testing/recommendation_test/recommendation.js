const puppeteer = require('puppeteer');

(async () => {

    const browser = await puppeteer.launch({ headless: false});
    const page = await browser.newPage();
    await page.setCacheEnabled(false);
    const navigationPromise = page.waitForNavigation({waitUntil: "domcontentloaded"});

    await page.setViewport({width:1535, height:1000});
    await page.goto('http://127.0.0.1:8000/login');
    await navigationPromise;

    // login 
    const username = await page.waitForXPath("/html/body/main/div/div/div/form/fieldset/div[1]/div/input");
    await page.waitFor(1000);
    await username.type("TestUser");
    const pword = await page.waitForXPath("/html/body/main/div/div/div/form/fieldset/div[2]/div/input");
    await pword.type("Testpword");
    const log_btn = await page.waitForSelector("body > main > div > div > div > form > div > button");
    await log_btn.click();
    await page.waitFor(2000);

    // got to recommendations
    const rec_navbar = await page.waitForSelector('#navbarToggle > div.navbar-nav.mr-auto > a:nth-child(3)');
    await rec_navbar.click();
    await page.waitFor(2000);
    await page.screenshot({path: 'all_result.png'});

    // click first
    const rec_1 = await page.waitForSelector('body > main > div > div > center > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > a');
    await rec_1.click();
    await page.waitFor(2000);
    await page.screenshot({path: 'recommended_result.png'});

    await browser.close();

})();