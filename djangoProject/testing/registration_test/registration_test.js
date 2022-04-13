const puppeteer = require('puppeteer');

(async () => {

    const browser = await puppeteer.launch({ headless: false});
    const page = await browser.newPage();

    await page.setViewport({width:1535, height:756})
    await page.goto('http://127.0.0.1:8000/register');
   
    const username = await page.waitForXPath("/html/body/main/div/div/div/form/fieldset/div[1]/div/input");
    await username.type("TestUser");
    const email = await page.waitForXPath("/html/body/main/div/div/div/form/fieldset/div[2]/div/input");
    await email.type("test@mail.dcu.ie");
    const pword1 = await page.waitForXPath("/html/body/main/div/div/div/form/fieldset/div[3]/div/input");
    await pword1.type("Testpword");
    const pword2 = await page.waitForXPath("/html/body/main/div/div/div/form/fieldset/div[4]/div/input");
    await pword2.type("Testpword");
    await page.screenshot({path: 'registration_filled.png', format: 'A4'});
    await page.waitFor(2000);
    const button = await page.waitForSelector("body > main > div > div > div > form > div > button");
    await button.click();
    await page.waitFor(2000);
    await page.screenshot({path: 'registration_success.png', format: 'A4'});
    await browser.close();

})()