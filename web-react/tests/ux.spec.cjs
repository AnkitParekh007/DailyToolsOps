const { chromium } = require("playwright");
const assert = require("node:assert/strict");
(async () => {
 const browser = await chromium.launch({headless:true});
 try {
  const page = await browser.newPage({viewport:{width:1440,height:900},reducedMotion:"reduce",acceptDownloads:true});
  const errors=[];page.on("pageerror",e=>errors.push(e.message));
  await page.goto("http://127.0.0.1:4173/DailyToolsOps/");
  await page.locator(".card").first().waitFor();
  await page.waitForFunction(()=>document.documentElement.dataset.theme==="auto" || document.documentElement.dataset.theme==="light" || document.documentElement.dataset.theme==="dark");
  const count=await page.locator(".card").count();
  assert.ok(count>=35);
  assert.equal(await page.locator("#typed").textContent(),"With any AI agent.");
  await page.getByRole("button",{name:"Dark theme",exact:true}).click();
  assert.equal(await page.locator("html").getAttribute("data-theme"),"dark");
  await page.reload();await page.locator(".card").first().waitFor();
  assert.equal(await page.locator("html").getAttribute("data-theme"),"dark");
  await page.getByRole("button",{name:"Light theme",exact:true}).click();
  assert.equal(await page.getByRole("button",{name:"Light theme",exact:true}).getAttribute("aria-pressed"),"true");
  await page.locator("#hero-query").fill("context-engineering");
  await page.getByRole("button",{name:"Search packs",exact:true}).click();
  assert.equal(await page.locator("#search").inputValue(),"context-engineering");
  assert.equal(await page.locator(".card").count(),1);
  assert.equal(await page.locator(".preview-resource").count(),3);
  await page.locator("#search").fill("context-engineering");
  assert.equal(await page.locator(".card").count(),1);
  const [download]=await Promise.all([page.waitForEvent("download"),page.locator(".card .download").click()]);
  assert.match(download.suggestedFilename(),/context-engineering.*\.zip$/);
  await page.locator("#search").fill("");
  await page.locator("#category").selectOption("frameworks");
  assert.equal(await page.locator(".card").count(),12);
  await page.locator("#category").selectOption("");
  await page.evaluate(()=>window.scrollTo(0,1000));
  async function checkFloatingHeader(){
    const card=page.locator(".sticky > .nav");
    const box=await card.boundingBox();
    const viewport=page.viewportSize();
    assert.ok(box.x>=7 && box.x+box.width<=viewport.width-7,"floating card gutters");
    const top=await page.locator(".sticky").evaluate(e=>parseFloat(getComputedStyle(e).top));
    assert.ok(Math.abs(box.y-top)<2,"floating card sticky offset");
    assert.ok(await card.evaluate(e=>parseFloat(getComputedStyle(e).borderRadius)>=12),"rounded navigation card");
  }
  await checkFloatingHeader();
  assert.equal(await page.locator(".coffee").getAttribute("href"),"https://buymeacoffee.com/ankitparekh");
  for(const width of [320,375,768,1024,1440]){
   await page.setViewportSize({width,height:900});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),"horizontal overflow at "+width);
   await page.evaluate(()=>window.scrollTo(0,1000));
   await checkFloatingHeader();
  }
  await page.setViewportSize({width:1440,height:900});
  const [all]=await Promise.all([page.waitForEvent("download"),page.locator("#all").click()]);
  assert.equal(all.suggestedFilename(),"dailytools-all.zip");
  await page.locator("#search").fill("context-engineering");
  await page.locator(".card").getByRole("link",{name:"Instructions"}).click();
  await page.waitForURL("**/docs/context-engineering/");
  assert.equal(await page.locator("h1").textContent(),"Context Engineering");
  assert.equal(await page.locator(".doc-body h2").first().textContent(),"Prerequisites");
  assert.equal(await page.locator("html").getAttribute("data-theme"),"light");
  await page.locator("#docs-search").fill("vendor-independent-harness");
  await page.locator(".docs-links").getByRole("link",{name:"Vendor Independent Harness",exact:true}).click();
  await page.waitForURL("**/docs/vendor-independent-harness/");
  assert.ok(await page.locator(".doc-body table").count()>0);
  const [docDownload]=await Promise.all([page.waitForEvent("download"),page.getByRole("link",{name:"Download ZIP",exact:true}).click()]);
  assert.match(docDownload.suggestedFilename(),/vendor-independent-harness.*\.zip$/);
  await page.getByRole("link",{name:"prompts.md",exact:true}).click();
  await page.waitForURL("**/docs/vendor-independent-harness/prompts/");
  assert.equal(await page.locator("h1").textContent(),"Prompts");
  for(const width of [320,375,768,1024,1440]){
    await page.setViewportSize({width,height:900});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),"docs overflow at "+width);
    await page.evaluate(()=>window.scrollTo(0,document.documentElement.scrollHeight));
    const card=await page.locator(".sticky > .nav").boundingBox();
    assert.ok(card.x>=7 && card.x+card.width<=width-7,"docs floating header gutters");
  }
  await page.screenshot({path:"ux-docs.png",fullPage:false});
  await page.goto("http://127.0.0.1:4173/DailyToolsOps/");
  await page.locator(".card").first().waitFor();
  const staticPage=await browser.newPage({javaScriptEnabled:false});await staticPage.goto("http://127.0.0.1:4173/DailyToolsOps/");assert.ok(await staticPage.locator(".card").count()>=35);await staticPage.goto("http://127.0.0.1:4173/DailyToolsOps/docs/context-engineering/");assert.equal(await staticPage.locator("h1").textContent(),"Context Engineering");await staticPage.close();
  assert.deepEqual(errors,[]);
  await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:"ux-desktop.png",fullPage:false});
  await page.setViewportSize({width:375,height:812});await page.screenshot({path:"ux-mobile.png",fullPage:false});
  console.log("UX browser checks passed");
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
