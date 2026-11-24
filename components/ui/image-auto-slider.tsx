'use client';

import { useEffect, useRef, useState } from 'react';
import { flushSync } from 'react-dom';
import { Search } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface SliderImage {
  id: string;
  src: string;
  srcSet: string;
  full: string;
  width: number;
  height: number;
  title: string;
  alt: string;
  category: string;
  order: number;
}

export interface ImageAutoSliderProps {
  images: readonly SliderImage[];
  pixelsPerSecond?: number;
  className?: string;
}

type Direction = 'left' | 'right';

function PhotoCard({ image, filter }: { image: SliderImage; filter: string }) {
  return (
    <figure className="photo-card" id={`foto-${image.id}`} data-photo-item=""
      data-category={image.category} hidden={filter !== 'Tümü' && image.category !== filter}>
      <a className="photo-launch" href={image.full} data-photo={image.id}
        data-title={image.title} data-alt={image.alt} data-width={image.width}
        data-height={image.height} data-photo-order={image.order}
        aria-label={`${image.title} fotoğrafını büyüt`}>
        <img className="real-photo" src={image.src} srcSet={image.srcSet}
          sizes="(max-width:600px) 225px, 300px" alt={image.alt}
          width={image.width} height={image.height} loading="lazy" decoding="async" />
        <span className="photo-zoom"><Search className="icon" size={18} aria-hidden="true" />
          <span>Büyüt</span></span>
      </a>
      <figcaption><span>{image.category}</span><strong>{image.title}</strong></figcaption>
    </figure>
  );
}

function SliderRow({ images, direction, filter, speed }: {
  images: readonly SliderImage[]; direction: Direction; filter: string; speed: number;
}) {
  const [order, setOrder] = useState<SliderImage[]>(() => direction === 'right' && images.length
    ? [images[images.length - 1], ...images.slice(0, -1)] : [...images]);
  const rowRef = useRef<HTMLDivElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);
  const orderRef = useRef(order);
  orderRef.current = order;
  const matches = (image: SliderImage) => filter === 'Tümü' || image.category === filter;
  const count = images.filter(matches).length;

  useEffect(() => {
    const row = rowRef.current;
    const track = trackRef.current;
    if (!row || !track || count < 2) return;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const pause = { hover: false, focus: false, pointer: false, hidden: document.hidden,
      outside: true, dialog: document.body.classList.contains('dialog-open') };
    let resumeTimer = 0;
    const updatePause = () => {
      row.classList.toggle('is-paused',Object.values(pause).some(Boolean));
      row.dataset.pausedReasons=Object.entries(pause).filter(([,value])=>value).map(([key])=>key).join(',');
    };
    const measure = () => {
      const first = track.querySelector<HTMLElement>('.photo-card:not([hidden])');
      const gap=parseFloat(getComputedStyle(track).columnGap || '0');
      const step=first ? first.getBoundingClientRect().width + gap : 0;
      const canMove=step>0 && step*count-gap>row.clientWidth+step;
      track.style.setProperty('--slider-step',`${step}px`);
      track.style.setProperty('--slider-duration',`${step / speed}s`);
      row.classList.toggle('is-running', canMove && !reduced.matches);
      row.classList.toggle('is-static', !canMove || reduced.matches);
      updatePause();
    };

    // Move existing keyed cards between the ends. No image is cloned.
    const rotate = (toEnd: boolean) => {
      const current = orderRef.current;
      const visible = current.filter(matches);
      const item = toEnd ? visible[0] : visible[visible.length - 1];
      if (!item) return;
      const rest = current.filter(image => image.id !== item.id);
      const next = toEnd ? [...rest, item] : [item, ...rest];
      orderRef.current = next;
      flushSync(() => setOrder(next));
    };
    const iteration = (event: AnimationEvent) => {
      if (event.target === track && event.animationName.startsWith('gallery-flow-')) rotate(direction === 'left');
    };
    const hoverIn = (event: PointerEvent) => { if (event.pointerType === 'mouse') {pause.hover=true;updatePause();} };
    const hoverOut = () => { pause.hover=false;updatePause(); };
    const focusIn = () => { pause.focus=Boolean(row.querySelector(':focus-visible'));updatePause(); };
    const focusOut = (event: FocusEvent) => {
      if (!row.contains(event.relatedTarget as Node | null)) { pause.focus=false;row.scrollLeft=0;updatePause(); }
    };
    const pointerDown = () => { clearTimeout(resumeTimer);pause.pointer=true;updatePause(); };
    const pointerUp = () => { resumeTimer=window.setTimeout(()=>{pause.pointer=false;updatePause();},700); };
    const visibility = () => { pause.hidden=document.hidden;updatePause(); };
    const preference = () => { measure(); };
    const revealLinkedPhoto = () => {
      const id=decodeURIComponent(location.hash.slice(1));
      const photo=id.startsWith('foto-') ? document.getElementById(id) : null;
      const linked=Boolean(photo && row.contains(photo));
      row.classList.toggle('is-linked',linked);
      if(linked && photo) photo.scrollIntoView({block:'nearest',inline:'center',behavior:'instant'});
      else row.scrollLeft=0;
    };
    const resize = new ResizeObserver(measure);
    const observer = new IntersectionObserver(entries => {
      pause.outside = !entries.some(entry => entry.isIntersecting);
      updatePause();
    }, { rootMargin: '40px' });
    const dialog = new MutationObserver(() => {pause.dialog=document.body.classList.contains('dialog-open');updatePause();});

    measure();
    revealLinkedPhoto();
    window.addEventListener('hashchange',revealLinkedPhoto);
    resize.observe(row);
    observer.observe(row);
    dialog.observe(document.body, { attributes: true, attributeFilter: ['class'] });
    row.addEventListener('pointerenter', hoverIn);
    row.addEventListener('pointerleave', hoverOut);
    row.addEventListener('focusin', focusIn);
    row.addEventListener('focusout', focusOut);
    row.addEventListener('pointerdown', pointerDown);
    window.addEventListener('pointerup', pointerUp);
    window.addEventListener('pointercancel', pointerUp);
    document.addEventListener('visibilitychange', visibility);
    reduced.addEventListener('change', preference);
    track.addEventListener('animationiteration',iteration);
    return () => {
      clearTimeout(resumeTimer);
      track.removeEventListener('animationiteration',iteration);
      resize.disconnect(); observer.disconnect(); dialog.disconnect();
      window.removeEventListener('hashchange',revealLinkedPhoto);
      row.removeEventListener('pointerenter', hoverIn);
      row.removeEventListener('pointerleave', hoverOut);
      row.removeEventListener('focusin', focusIn);
      row.removeEventListener('focusout', focusOut);
      row.removeEventListener('pointerdown', pointerDown);
      window.removeEventListener('pointerup', pointerUp);
      window.removeEventListener('pointercancel', pointerUp);
      document.removeEventListener('visibilitychange', visibility);
      reduced.removeEventListener('change', preference);
    };
  }, [count, direction, filter, speed]);

  return (
    <div ref={rowRef} className="auto-slider-row" data-direction={direction} hidden={!count}
      role="group" aria-label={direction === 'left' ? 'Üst fotoğraf sırası' : 'Alt fotoğraf sırası'}>
      <div ref={trackRef} className="auto-slider-track sg:flex sg:w-max sg:items-stretch">
        {order.map(image => <PhotoCard key={image.id} image={image} filter={filter} />)}
      </div>
    </div>
  );
}

export function ImageAutoSlider({ images, pixelsPerSecond = 24, className }: ImageAutoSliderProps) {
  const [filter, setFilter] = useState('Tümü');
  const split = Math.ceil(images.length / 2);
  const root = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const update = (event: Event) => {
      const value = (event as CustomEvent<{ category: string }>).detail?.category;
      if (value) setFilter(value);
    };
    const node = root.current;
    node?.addEventListener('photo-gallery-filter', update);
    if (node) node.dataset.hydrated = 'true';
    return () => node?.removeEventListener('photo-gallery-filter', update);
  }, []);
  return (
    <div ref={root} className={cn('auto-image-slider sg:relative sg:w-full', className)} data-auto-slider=""
      aria-label="Gösterilerden fotoğraflar">
      <SliderRow key={`left-${filter}`} images={images.slice(0, split)} direction="left"
        filter={filter} speed={pixelsPerSecond} />
      <SliderRow key={`right-${filter}`} images={images.slice(split)} direction="right"
        filter={filter} speed={pixelsPerSecond} />
    </div>
  );
}

export const Component = ImageAutoSlider;
