import { renderToString } from 'react-dom/server';
import { ImageAutoSlider, type ImageAutoSliderProps } from '@/components/ui/image-auto-slider';

export function renderSlider(props: ImageAutoSliderProps) {
  return renderToString(<ImageAutoSlider {...props} />);
}
