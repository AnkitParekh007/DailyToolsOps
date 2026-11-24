import {useEffect} from 'react';
import {useLocation} from 'react-router-dom';
import {BASE,ORIGIN,guides,normalize,packs,title} from '../data/site.js';
const image=ORIGIN+BASE+'social.png';
export function metadata(path){
 const route=normalize(path), guide=guides[route];
 const home=route==='/';
 const name=home?'Engineering resources for any AI agent':guide?.name||'Page not found';
 const pageTitle=home?'DailyToolsOps — '+name:name+' · DailyToolsOps Docs';
 const description=home?'Download portable engineering resource packs for Claude Code, Cursor, Codex and Antigravity. Explore instructions, workflows and verified ZIP archives.':guide?guide.description:'The requested DailyToolsOps page could not be found. Browse the resource catalog or documentation to locate your engineering guide.';
 const canonical=ORIGIN+BASE+route.slice(1);
 const schema=[{'@context':'https://schema.org','@type':home?'WebSite':'WebPage',name:pageTitle,url:canonical,description}];
 if(guide){const parts=[{name:'DailyToolsOps',item:ORIGIN+BASE},{name:'Documentation',item:ORIGIN+BASE+'docs/'}];if(route!='/docs/')parts.push({name:guide.name,item:canonical});schema.push({'@context':'https://schema.org','@type':'BreadcrumbList',itemListElement:parts.map((p,i)=>({'@type':'ListItem',position:i+1,...p}))});}
 return {title:pageTitle,description,canonical,image,schema,noindex:!home&&!guide};
}
export function SEO(){const {pathname}=useLocation();useEffect(()=>{const m=metadata(pathname);document.title=m.title;document.querySelectorAll('[data-seo]').forEach(n=>n.remove());function add(tag,attrs,text){const el=document.createElement(tag);el.dataset.seo='';Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));if(text)el.textContent=text;document.head.append(el);}add('meta',{name:'description',content:m.description});add('link',{rel:'canonical',href:m.canonical});for(const [key,value] of Object.entries({'og:title':m.title,'og:description':m.description,'og:type':'website','og:url':m.canonical,'og:image':m.image}))add('meta',{property:key,content:value});for(const [key,value] of Object.entries({'twitter:card':'summary_large_image','twitter:title':m.title,'twitter:description':m.description,'twitter:image':m.image}))add('meta',{name:key,content:value});if(m.noindex)add('meta',{name:'robots',content:'noindex,follow'});add('script',{type:'application/ld+json'},JSON.stringify(m.schema));},[pathname]);return null;}
