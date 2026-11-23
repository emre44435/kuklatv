/* Ali Abi & Zoyo — dependency-free progressive enhancement. */
(() => {
  'use strict';
  document.documentElement.classList.add('has-js');
  const $ = (selector, parent = document) => parent.querySelector(selector);
  const $$ = (selector, parent = document) => [...parent.querySelectorAll(selector)];
  const configNode = $('#site-config');
  let config = {};
  try { config = JSON.parse(configNode?.textContent || '{}'); } catch { /* Static links remain usable. */ }
  $$('[data-year]').forEach(node => { node.textContent = String(new Date().getFullYear()); });

  // The animated theatre remains decorative; visitors can pause all motion.
  // No cookies, storage, timers, third-party scripts, or animation dependencies.
  const motionToggle = $('#motion-toggle');
  motionToggle?.addEventListener('click', () => {
    const paused = document.body.classList.toggle('motion-paused');
    motionToggle.setAttribute('aria-pressed', String(paused));
    motionToggle.setAttribute('aria-label', paused ? 'Arka plan hareketini başlat' : 'Arka plan hareketini durdur');
    $('[data-motion-label]', motionToggle).textContent = paused ? 'Hareketi başlat' : 'Hareketi durdur';
  });
  document.addEventListener('visibilitychange', () => {
    document.body.classList.toggle('motion-suspended', document.hidden);
  });
  if ('IntersectionObserver' in window) {
    const sceneObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.target.classList.toggle('scene-asleep', !entry.isIntersecting));
    }, {rootMargin:'80px'});
    $$('.theatre-scene').forEach(scene => sceneObserver.observe(scene));
  }

  const menu = $('#main-nav');
  const toggle = $('.menu-toggle');
  const closeMenu = () => {
    if (!toggle || !menu) return;
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Menüyü aç');
  };
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç');
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.header-inner')) {
      closeMenu();
      $$('.nav-dropdown[open]').forEach(node => { node.open = false; });
    }
  });
  menu?.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const wasOpen = toggle?.getAttribute('aria-expanded') === 'true';
    closeMenu();
    $$('.nav-dropdown[open]').forEach(node => { node.open = false; });
    if (wasOpen) toggle.focus();
  });
  window.matchMedia('(min-width: 1001px)').addEventListener('change', closeMenu);

  // No iframe, YouTube script, remote thumbnail, or preconnect before a play click.
  const dialog = $('#video-dialog');
  const frameHost = $('#video-frame');
  let previousFocus = null;
  function resetVideo() {
    frameHost?.replaceChildren();
    document.body.classList.remove('dialog-open');
    previousFocus?.focus();
  }
  $$('[data-video]').forEach(trigger => {
    trigger.addEventListener('click', event => {
      const id = trigger.dataset.video;
      // file:// has no HTTP Referer; the verified YouTube link is the fallback.
      if (!dialog?.showModal || !/^[A-Za-z0-9_-]{11}$/.test(id) || location.protocol === 'file:') return;
      event.preventDefault();
      previousFocus = trigger;
      const title = trigger.dataset.title || 'Zoyo kukla videosu';
      $('#video-dialog-title').textContent = title;
      $('#video-external').href = `https://www.youtube.com/shorts/${id}`;
      const player = document.createElement('iframe');
      const params = new URLSearchParams({autoplay: '1', playsinline: '1', rel: '0', origin: location.origin});
      player.src = `https://www.youtube-nocookie.com/embed/${id}?${params}`;
      player.title = `${title} — YouTube video oynatıcısı`;
      player.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      player.allowFullscreen = true;
      player.referrerPolicy = 'strict-origin-when-cross-origin';
      frameHost.replaceChildren(player);
      dialog.showModal();
      document.body.classList.add('dialog-open');
    });
  });
  $('[data-close-video]')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('close', resetVideo);
  dialog?.addEventListener('click', event => {
    if (event.target === dialog) {
      const bounds = dialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
    }
  });

  const normalize = text => text.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i').trim();
  const search = $('#province-search');
  const provinceRows = $$('#province-list li');
  search?.addEventListener('input', () => {
    const term = normalize(search.value);
    let count = 0;
    provinceRows.forEach(row => {
      row.hidden = !normalize(row.textContent).includes(term);
      if (!row.hidden) count++;
    });
    $('#province-count').textContent = term ? `${count} il bulundu.` : '81 ilde gösteri planlanabilir.';
    $('#province-empty').hidden = count > 0;
  });

  const form = $('#event-form');
  if (form) {
    const dateInput = $('#event-date');
    const today = new Date();
    dateInput.min = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
    const selectedCity = new URLSearchParams(location.search).get('il');
    if ([...$('#city').options].some(option => option.value === selectedCity)) $('#city').value = selectedCity;
    const whatsapp = String(config.whatsapp || '').replace(/\D/g, '');
    const send = $('#send-message');
    if (whatsapp) {
      send.textContent = 'WhatsApp’ı aç';
      send.href = `https://wa.me/${whatsapp}`;
    }
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const value = name => String(data.get(name) || '').trim();
      const lines = ['Merhaba Ali Abi, Ali Abi ve Zoyo kukla gösterisi için bilgi almak istiyorum.', ''];
      if (value('kurum')) lines.push(`Kurum / okul: ${value('kurum')}`);
      lines.push(`Şehir: ${value('il')}`, `Etkinlik: ${value('etkinlik')}`);
      if (value('tarih')) {
        const [year, month, day] = value('tarih').split('-');
        lines.push(`Düşünülen tarih: ${day}.${month}.${year}`);
      }
      if (value('yas')) lines.push(`Yaş aralığı: ${value('yas')}`);
      if (value('kisi')) lines.push(`Tahmini kişi sayısı: ${value('kisi')}`);
      if (value('not')) lines.push('', value('not'));
      lines.push('', 'Tarih uygunluğu ve gösteri teklifi hakkında bilgi paylaşabilir misiniz?');
      const message = lines.join('\n');
      $('#message-text').value = message;
      $('#message-result').hidden = false;
      $('#copy-status').textContent = 'Mesaj hazırlandı. Henüz gönderilmedi.';
      if (whatsapp) send.href = `https://wa.me/${whatsapp}?text=${encodeURIComponent(message)}`;
      $('#message-result').scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'nearest'});
      $('#live-status').textContent = 'Etkinlik mesajınız hazırlandı. Kopyalayıp iletişim kanalında gönderebilirsiniz.';
    });
    $('#copy-message').addEventListener('click', async () => {
      const text = $('#message-text');
      try {
        if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
        await navigator.clipboard.writeText(text.value);
        $('#copy-status').textContent = 'Mesaj kopyalandı. Görüşmeyi açıp yapıştırabilirsiniz.';
      } catch {
        text.focus();
        text.select();
        text.setSelectionRange(0, text.value.length);
        $('#copy-status').textContent = 'Mesaj seçildi. Kopyala komutunu kullanıp görüşmeye yapıştırabilirsiniz.';
      }
    });
  }
})();
