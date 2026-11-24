import { build } from 'esbuild';
import { readFile, writeFile, mkdir, rm } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=async name=>JSON.parse(await readFile(path.join(root,name),'utf8'));
const photos=await read('content/photos.json'),config=await read('content/site.json');
const selected=photos.filter(p=>!Object.values(config.homepage_photos).includes(p.id))
  .sort((a,b)=>(a.priority??100)-(b.priority??100)||a.id.localeCompare(b.id));
const prefix='__SITE_BASE__assets/img/photos/';
const images=selected.map((p,order)=>({id:p.id,title:p.title,alt:p.alt,category:p.category,
  src:prefix+(p.renditions.find(r=>r.width>=Math.min(960,p.width))??p.renditions.at(-1)).file,
  srcSet:p.renditions.map(r=>`${prefix}${r.file} ${r.width}w`).join(', '),
  full:prefix+p.full,width:p.width,height:p.height,order:order+4}));
const props={images,pixelsPerSecond:26};
await writeFile(path.join(root,'content/photo-slider-data.json'),JSON.stringify(props,null,2)+'\n');
const common={absWorkingDir:root,bundle:true,jsx:'automatic',target:'es2020',tsconfig:'tsconfig.json',
  define:{'process.env.NODE_ENV':'"production"'},logLevel:'info'};
const temporary=path.join(root,'.slider-build');
await mkdir(temporary,{recursive:true});
try {
  const server=path.join(temporary,'render.cjs');
  await build({...common,entryPoints:['frontend/render-slider.tsx'],platform:'node',format:'cjs',outfile:server});
  const renderer=await import(pathToFileURL(server).href);
  const {renderSlider}=renderer.default??renderer;
  await writeFile(path.join(root,'content/photo-slider.html'),renderSlider(props)+'\n');
  await build({...common,entryPoints:['frontend/image-auto-slider.tsx'],platform:'browser',format:'iife',
    minify:true,legalComments:'external',outfile:'assets/js/image-auto-slider.js'});
  const cli=path.join(root,'node_modules/@tailwindcss/cli/dist/index.mjs');
  const css=spawnSync(process.execPath,[cli,'-i','styles/globals.css','-o','assets/css/image-auto-slider.css','--minify'],{cwd:root,stdio:'inherit'});
  if(css.status!==0)throw new Error('Slider stylesheet build failed');
} finally {await rm(temporary,{recursive:true,force:true});}
console.log(`Built two opposing slider rows with ${images.length} unique gallery photographs.`);
