import { hydrateRoot } from 'react-dom/client';
import { ImageAutoSlider, type ImageAutoSliderProps } from '@/components/ui/image-auto-slider';

const target = document.getElementById('image-auto-slider-root');
const source = document.getElementById('image-auto-slider-data');
if (target && source?.textContent) {
  const props = JSON.parse(source.textContent) as ImageAutoSliderProps;
  hydrateRoot(target, <ImageAutoSlider {...props} />);
}
