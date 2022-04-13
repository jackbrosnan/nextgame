const puppeteer = require('puppeteer');

(async () => {

    const browser = await puppeteer.launch({ headless: false});
    const page = await browser.newPage();

    await page.setViewport({width:1535, height:756})
    await page.goto('http://127.0.0.1:8000/login');
    
    const username = await page.waitForXPath("/html/body/main/div/div/div/form/fieldset/div[1]/div/input");
    await username.type("TestUser");
    const pword = await page.waitForXPath("/html/body/main/div/div/div/form/fieldset/div[2]/div/input");
    await pword.type("Testpword");

    await page.screenshot({path: 'login_filled.png', format: 'A4'});
    await page.waitFor(2000);
    const button = await page.waitForSelector("body > main > div > div > div > form > div > button");
    await button.click();
    await page.waitFor(2000);
    await page.screenshot({path: 'logged_in.png', format: 'A4'});

    const logout = await page.waitForSelector("#logout-btn");
    await logout.click();
    await page.waitFor(2000);
    await page.screenshot({path: 'logged_out.png', format: 'A4'});
    
    await browser.close();

})();