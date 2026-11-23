/* Ali Abi & Zoyo — dependency-free progressive enhancement. */
(() => {
  'use strict';
  document.documentElement.classList.add('has-js');
  const $ = (selector, parent = document) => parent.querySelector(selector);
  const $$ = (selector, parent = document) => [...parent.querySelectorAll(selector)];
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
    document.body.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Menüyü aç');
  };
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
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
  window.matchMedia('(min-width: 1121px)').addEventListener('change', closeMenu);

  // Photographs open in an accessible local viewer; social videos are ordinary external links.
  const photoDialog = $('#photo-dialog');
  const photoImage = $('#photo-full');
  const photoTriggers = $$('[data-photo]');
  let activePhoto = -1;
  let photoFocus = null;
  const visiblePhotos = () => photoTriggers.filter(link => !link.closest('[data-photo-item]')?.hidden);
  function showPhoto(index) {
    const current = visiblePhotos();
    if (!current.length) return;
    activePhoto = ((index % current.length) + current.length) % current.length;
    const trigger = current[activePhoto];
    photoImage.width = Number(trigger.dataset.width);
    photoImage.height = Number(trigger.dataset.height);
    photoImage.src = trigger.href;
    photoImage.alt = trigger.dataset.alt || trigger.dataset.title || '';
    $('#photo-title').textContent = trigger.dataset.title;
    $('#photo-position').textContent = `${activePhoto+1} / ${current.length}`;
    $('#photo-download').href = trigger.href;
  }
  photoTriggers.forEach(trigger => trigger.addEventListener('click', event => {
    if (!photoDialog?.showModal) return;
    event.preventDefault();
    photoFocus = trigger;
    showPhoto(visiblePhotos().indexOf(trigger));
    photoDialog.showModal();
    document.body.classList.add('dialog-open');
  }));
  $('[data-close-photo]')?.addEventListener('click', () => photoDialog.close());
  $('[data-prev-photo]')?.addEventListener('click', () => showPhoto(activePhoto-1));
  $('[data-next-photo]')?.addEventListener('click', () => showPhoto(activePhoto+1));
  photoDialog?.addEventListener('close', () => {
    document.body.classList.remove('dialog-open');
    photoImage.removeAttribute('src');
    photoFocus?.focus();
  });
  photoDialog?.addEventListener('click', event => {
    if (event.target !== photoDialog) return;
    const box = photoDialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) photoDialog.close();
  });
  document.addEventListener('keydown', event => {
    if (!photoDialog?.open) return;
    if (event.key === 'ArrowLeft') { event.preventDefault(); showPhoto(activePhoto-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); showPhoto(activePhoto+1); }
  });
  let swipeStart = null;
  photoImage?.addEventListener('pointerdown', event => { swipeStart = {x:event.clientX,y:event.clientY}; });
  photoImage?.addEventListener('pointercancel', () => { swipeStart = null; });
  photoImage?.addEventListener('pointerup', event => {
    if (!swipeStart) return;
    const dx=event.clientX-swipeStart.x,dy=event.clientY-swipeStart.y;
    swipeStart=null;
    if (Math.abs(dx)>45 && Math.abs(dy)<80) showPhoto(activePhoto+(dx<0?1:-1));
  });
  $$('[data-photo-filter]').forEach(button => button.addEventListener('click', () => {
    const category=button.dataset.photoFilter;
    $$('[data-photo-filter]').forEach(other => other.setAttribute('aria-pressed',String(other===button)));
    $$('.photo-card').forEach(card => { card.hidden = category !== 'Tümü' && card.dataset.category !== category; });
    const count=$$('.photo-card').filter(card=>!card.hidden).length;
    if ($('#photo-count')) $('#photo-count').textContent = `${count} fotoğraf`;
  }));

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
    $('#province-count').textContent = term ? `${count} il bulundu.` : '81 ilde gösteri yapılabiliyor.';
    $('#province-empty').hidden = count > 0;
  });

})();
