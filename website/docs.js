"use strict";
const modes=["auto","light","dark"];
try{const saved=localStorage.getItem("dailytools-theme");if(modes.includes(saved))document.documentElement.dataset.theme=saved;}catch{}
function syncTheme(){document.querySelectorAll("[data-mode]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.mode===document.documentElement.dataset.theme)));}
document.querySelectorAll("[data-mode]").forEach(b=>b.addEventListener("click",()=>{document.documentElement.dataset.theme=b.dataset.mode;try{localStorage.setItem("dailytools-theme",b.dataset.mode);}catch{}syncTheme();}));syncTheme();
const nav=document.getElementById("docs-nav"),search=document.getElementById("docs-search"),status=document.getElementById("docs-status");
if(matchMedia("(max-width:760px)").matches)nav.open=false;
search.addEventListener("input",()=>{const q=search.value.trim().toLowerCase();let count=0;document.querySelectorAll(".docs-group").forEach(group=>{let found=0;group.querySelectorAll("a").forEach(a=>{const match=(a.textContent+" "+a.dataset.search).toLowerCase().includes(q);a.hidden=!match;if(match)found++;});group.hidden=found===0;count+=found;});status.textContent=q?count+" matching guides":"";});
document.addEventListener("keydown",e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==="k"){e.preventDefault();nav.open=true;search.focus();}});
document.querySelectorAll(".copy-code").forEach(button=>button.addEventListener("click",async()=>{const code=button.closest(".code-wrap").querySelector("code");try{await navigator.clipboard.writeText(code.textContent);button.textContent="Copied";}catch{const range=document.createRange();range.selectNodeContents(code);const sel=window.getSelection();sel.removeAllRanges();sel.addRange(range);button.textContent="Select and copy";}setTimeout(()=>button.textContent="Copy",1800);}));
