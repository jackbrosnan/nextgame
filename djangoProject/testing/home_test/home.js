const puppeteer = require('puppeteer');
const chai = require('chai');
const { expect, assert } = require('chai');


(async () => {

    const browser = await puppeteer.launch({ headless: false});
    const page = await browser.newPage();

    await page.setViewport({width:1553, height:1200})
    await page.goto('http://127.0.0.1:8000/home');
   
    await page.screenshot({path: 'home.png', format: 'A4'});
    const title = await page.title();
    const url = await page.url();
    console.log("Page Title: " + title);
    console.log("Page URL: " + url);
    await page.waitFor(2000);

    // instruction buttons
    // register
    const reg_btn = await page.waitForSelector("#register-btn");
    await reg_btn.click();
    await page.waitFor(2000);
    const url_reg = await page.url();
    console.log('URL after click: ' + url_reg);

    // submit games
    await page.goto('http://127.0.0.1:8000/home');
    const submit_btn = await page.waitForSelector("#add-game-btn");
    await submit_btn.click();
    await page.waitFor(2000);
    const url_sub = await page.url();
    console.log('URL after click: ' + url_sub);
    await page.waitFor(2000);

    // recommendations
    await page.goto('http://127.0.0.1:8000/home');
    const rec_btn = await page.waitForSelector("#rec-btn");
    await rec_btn.click();
    await page.waitFor(2000);
    const url_rec = await page.url();
    console.log('URL after click: ' + url_rec);

    await browser.close();
})();