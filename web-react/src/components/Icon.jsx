import React from 'react';
import sprite from '../assets/icons.svg?raw';
export function Sprite(){return <div aria-hidden="true" className="sprite" dangerouslySetInnerHTML={{__html:sprite}}/>;}
export function Icon({name}){return <svg className="icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><use href={'#i-'+name}/></svg>;}
