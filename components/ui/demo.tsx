import { Component, type SliderImage } from '@/components/ui/image-auto-slider';
import data from '@/content/photo-slider-data.json';

const images: SliderImage[] = data.images.map(image => ({
  ...image,
  src:image.src.replaceAll('__SITE_BASE__','./'),
  full:image.full.replaceAll('__SITE_BASE__','./'),
  srcSet:image.srcSet.replaceAll('__SITE_BASE__','./'),
}));

export const DemoOne = () => <Component images={images} pixelsPerSecond={24} />;
