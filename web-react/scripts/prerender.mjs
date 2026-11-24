import {readFile,writeFile,mkdir} from 'node:fs/promises';import {resolve,dirname} from 'node:path';
import {render,routes,metadata} from '../.ssr/entry-server.js';
const out=resolve('dist'),template=await readFile(resolve(out,'index.html'),'utf8');
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;').replaceAll('>','&gt;');
function head(m){const tag=(name,content,property=false)=>'<meta data-seo '+(property?'property':'name')+'="'+name+'" content="'+esc(content)+'">';return '<title>'+esc(m.title)+'</title>'+tag('description',m.description)+'<link data-seo rel="canonical" href="'+esc(m.canonical)+'"><link rel="icon" href="/DailyToolsOps/favicon.svg">'+Object.entries({'og:title':m.title,'og:description':m.description,'og:type':'website','og:url':m.canonical,'og:image':m.image}).map(([k,v])=>tag(k,v,true)).join('')+Object.entries({'twitter:card':'summary_large_image','twitter:title':m.title,'twitter:description':m.description,'twitter:image':m.image}).map(([k,v])=>tag(k,v)).join('')+(m.noindex?tag('robots','noindex,follow'):'')+'<script data-seo type="application/ld+json">'+JSON.stringify(m.schema).replaceAll('<','\\u003c')+'</script>';}
async function emit(route,file){const m=metadata(route);let html=template.replace('<!--seo-->',head(m)).replace('<div id="root"></div>',()=>'<div id="root">'+render(route)+'</div>');if(route.startsWith('/docs/'))html=html.replace('<body>','<body class="docs-page">');await mkdir(dirname(file),{recursive:true});await writeFile(file,html);}
for(const route of routes)await emit(route,resolve(out,route.slice(1),'index.html'));
await emit('/not-found/',resolve(out,'404.html'));
// Unknown routes must render the actual current URL, not hydrate a different static route.
const error=await readFile(resolve(out,'404.html'),'utf8');await writeFile(resolve(out,'404.html'),error.replace('<div id="root">','<div id="root" data-not-found="true">'));
await writeFile(resolve(out,'sitemap.xml'),'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+routes.map(r=>'<url><loc>'+esc(metadata(r).canonical)+'</loc></url>').join('')+'</urlset>\n');
await writeFile(resolve(out,'robots.txt'),'User-agent: *\nAllow: /\nSitemap: https://ankitparekh007.github.io/DailyToolsOps/sitemap.xml\n');
console.log('Pre-rendered '+routes.length+' public pages and 404');
