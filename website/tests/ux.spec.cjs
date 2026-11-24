const { chromium } = require("playwright");
const assert = require("node:assert/strict");
(async () => {
 const browser = await chromium.launch({headless:true});
 try {
  const page = await browser.newPage({viewport:{width:1440,height:900},reducedMotion:"reduce",acceptDownloads:true});
  const errors=[];page.on("pageerror",e=>errors.push(e.message));
  await page.goto("http://127.0.0.1:8000/");
  await page.locator(".card").first().waitFor();
  const count=await page.locator(".card").count();
  assert.ok(count>=35);
  assert.equal(await page.locator("#typed").textContent(),"With any AI agent.");
  await page.getByRole("button",{name:"Dark theme",exact:true}).click();
  assert.equal(await page.locator("html").getAttribute("data-theme"),"dark");
  await page.reload();await page.locator(".card").first().waitFor();
  assert.equal(await page.locator("html").getAttribute("data-theme"),"dark");
  await page.getByRole("button",{name:"Light theme",exact:true}).click();
  assert.equal(await page.getByRole("button",{name:"Light theme",exact:true}).getAttribute("aria-pressed"),"true");
  await page.getByRole("searchbox").fill("context-engineering");
  assert.equal(await page.locator(".card").count(),1);
  const [download]=await Promise.all([page.waitForEvent("download"),page.locator(".card .download").click()]);
  assert.match(download.suggestedFilename(),/context-engineering.*\.zip$/);
  await page.getByRole("searchbox").fill("");
  await page.locator("#category").selectOption("frameworks");
  assert.equal(await page.locator(".card").count(),12);
  await page.locator("#category").selectOption("");
  await page.evaluate(()=>window.scrollTo(0,1000));
  assert.ok(Math.abs((await page.locator(".sticky").boundingBox()).y)<2);
  assert.equal(await page.locator(".coffee").getAttribute("href"),"https://buymeacoffee.com/ankitparekh");
  for(const width of [320,375,768,1024,1440]){
   await page.setViewportSize({width,height:900});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),"horizontal overflow at "+width);
  }
  await page.setViewportSize({width:1440,height:900});
  const [all]=await Promise.all([page.waitForEvent("download"),page.locator("#all").click()]);
  assert.equal(all.suggestedFilename(),"dailytools-all.zip");
  await page.getByRole("searchbox").fill("context-engineering");
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
  }
  await page.screenshot({path:"ux-docs.png",fullPage:false});
  await page.goto("http://127.0.0.1:8000/");
  await page.locator(".card").first().waitFor();
  assert.deepEqual(errors,[]);
  await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:"ux-desktop.png",fullPage:false});
  await page.setViewportSize({width:375,height:812});await page.screenshot({path:"ux-mobile.png",fullPage:false});
  console.log("UX browser checks passed");
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
