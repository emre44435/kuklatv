'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import AutoScroll from 'embla-carousel-auto-scroll';
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
      <a className="photo-launch" href={image.full} data-photo={image.id} draggable={false}
        data-title={image.title} data-alt={image.alt} data-width={image.width}
        data-height={image.height} data-photo-order={image.order}
        aria-label={`${image.title} fotoğrafını büyüt`}>
        <img className="real-photo" src={image.src} srcSet={image.srcSet} draggable={false}
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
  const rowRef = useRef<HTMLDivElement | null>(null);
  const count = images.filter(image => filter === 'Tümü' || image.category === filter).length;
  const autoScroll = useMemo(() => AutoScroll({
    speed: Math.max(1, speed) / 60,
    direction: direction === 'left' ? 'forward' : 'backward',
    playOnInit: false,
    startDelay: 1000,
    stopOnInteraction: true,
    stopOnMouseEnter: false,
    stopOnFocusIn: false,
  }), [direction, speed]);
  const [viewportRef, api] = useEmblaCarousel({
    align: 'start', loop: true, dragFree: true, dragThreshold: 8,
    slides: '.photo-card:not([hidden])', watchDrag: true,
  }, [autoScroll]);
  const attachViewport = useCallback((node: HTMLDivElement | null) => {
    rowRef.current = node;
    viewportRef(node);
  }, [viewportRef]);

  useEffect(() => {
    const row = rowRef.current;
    if (!row || !api || !count) return;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const pause = { pointer: false, cooldown: false, focus: false, linked: false,
      hidden: document.hidden, outside: true, reduced: reduced.matches,
      dialog: document.body.classList.contains('dialog-open') };
    let resumeTimer = 0;
    const playing = () => row.classList.toggle('is-running', autoScroll.isPlaying());
    const resetNativeScroll = () => { if (row.scrollLeft) row.scrollLeft = 0; };
    const update = () => {
      const paused = Object.values(pause).some(Boolean);
      const looping = api.internalEngine().options.loop && count > 1;
      row.classList.toggle('is-paused', paused);
      row.classList.toggle('is-static', !looping);
      row.dataset.pausedReasons = Object.entries(pause).filter(([, value]) => value).map(([key]) => key).join(',');
      if (!paused && looping) {
        if (!autoScroll.isPlaying()) autoScroll.play(0);
      } else autoScroll.stop();
      playing();
    };
    const resumeLater = () => {
      clearTimeout(resumeTimer);
      pause.cooldown = true;
      update();
      resumeTimer = window.setTimeout(() => { pause.cooldown = false; update(); }, 1000);
    };
    const pointerDown = () => {
      clearTimeout(resumeTimer);
      pause.pointer = true;
      pause.cooldown = false;
      pause.linked = false;
      row.classList.add('is-dragging');
      update();
    };
    const pointerUp = () => {
      pause.pointer = false;
      row.classList.remove('is-dragging');
      resumeLater();
    };
    const focus = () => { pause.focus = Boolean(row.querySelector(':focus-visible')) || row.matches(':focus-visible'); update(); };
    const focusOut = (event: FocusEvent) => {
      if (!row.contains(event.relatedTarget as Node | null)) { pause.focus = false; update(); }
    };
    const visibility = () => { pause.hidden = document.hidden; update(); };
    const preference = () => { pause.reduced = reduced.matches; update(); };
    const revealLinkedPhoto = () => {
      resetNativeScroll();
      const id = location.hash.slice(1);
      const index = api.slideNodes().findIndex(photo => photo.id === id);
      pause.linked = index !== -1;
      update();
      if (index !== -1) {
        api.scrollTo(index, true);
        row.scrollIntoView({ block: 'nearest', behavior: 'instant' });
      }
    };
    const keyDown = (event: KeyboardEvent) => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      pause.linked = false;
      resumeLater();
      if (event.key === 'ArrowLeft') api.scrollPrev(reduced.matches);
      if (event.key === 'ArrowRight') api.scrollNext(reduced.matches);
      if (event.key === 'Home') api.scrollTo(0, reduced.matches);
      if (event.key === 'End') api.scrollTo(api.scrollSnapList().length - 1, reduced.matches);
    };
    const observer = new IntersectionObserver(entries => {
      pause.outside = !entries.some(entry => entry.isIntersecting);
      update();
    }, { rootMargin: '40px' });
    const dialog = new MutationObserver(() => {
      pause.dialog = document.body.classList.contains('dialog-open');
      update();
    });
    const reinitialize = () => { revealLinkedPhoto(); update(); };
    api.on('pointerDown', pointerDown).on('pointerUp', pointerUp)
      .on('reInit', reinitialize).on('autoScroll:play', playing).on('autoScroll:stop', playing);
    row.dataset.ready = 'true';
    revealLinkedPhoto();
    observer.observe(row);
    dialog.observe(document.body, { attributes: true, attributeFilter: ['class'] });
    row.addEventListener('scroll', resetNativeScroll, { passive: true });
    row.addEventListener('focusin', focus);
    row.addEventListener('focusout', focusOut);
    row.addEventListener('keydown', keyDown);
    document.addEventListener('visibilitychange', visibility);
    window.addEventListener('hashchange', revealLinkedPhoto);
    reduced.addEventListener('change', preference);
    return () => {
      clearTimeout(resumeTimer);
      observer.disconnect(); dialog.disconnect();
      autoScroll.stop();
      api.off('pointerDown', pointerDown).off('pointerUp', pointerUp)
        .off('reInit', reinitialize).off('autoScroll:play', playing).off('autoScroll:stop', playing);
      row.removeEventListener('scroll', resetNativeScroll);
      row.removeEventListener('focusin', focus);
      row.removeEventListener('focusout', focusOut);
      row.removeEventListener('keydown', keyDown);
      document.removeEventListener('visibilitychange', visibility);
      window.removeEventListener('hashchange', revealLinkedPhoto);
      reduced.removeEventListener('change', preference);
    };
  }, [api, autoScroll, count]);

  return (
    <div ref={attachViewport} className="auto-slider-row" data-direction={direction} hidden={!count}
      tabIndex={0} role="group" aria-live="off"
      aria-label={direction === 'left' ? 'Üst fotoğraf sırası' : 'Alt fotoğraf sırası'}>
      <div className="auto-slider-track sg:flex sg:items-stretch">
        {images.map(image => <PhotoCard key={image.id} image={image} filter={filter} />)}
      </div>
    </div>
  );
}

export function ImageAutoSlider({ images, pixelsPerSecond = 26, className }: ImageAutoSliderProps) {
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
