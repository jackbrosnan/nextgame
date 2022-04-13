const puppeteer = require('puppeteer');

(async () => {

    const browser = await puppeteer.launch({ headless: false});
    const page = await browser.newPage();
    await page.setCacheEnabled(false);
    const navigationPromise = page.waitForNavigation({waitUntil: "domcontentloaded"});

    await page.setViewport({width:1535, height:756});
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

    // go to add liked games
    const add_navbar = await page.waitForSelector('#navbarToggle > div.navbar-nav.mr-auto > a:nth-child(2)');
    await add_navbar.click();
    await navigationPromise;
    
    // success add
    const add = await page.waitForXPath('/html/body/header/nav/div/div[1]/a[2]');
    await add.click();
    await page.waitFor(2000);
    const search2 = await page.waitForSelector('#id_liked_game');
    await search2.type('Thief');
    await page.waitFor(2000);
    await page.screenshot({path: 'search_input.png'});

    const result2 = await page.waitForSelector('#autocomplete-result-0');
    await result2.click();
    await page.waitFor(2000);
    const button_submit = await page.waitForSelector('#game-form > div > button');
    await button_submit.click();
    await page.waitFor(2000);
    await page.screenshot({path: 'search_result.png'});


    await browser.close();

})();