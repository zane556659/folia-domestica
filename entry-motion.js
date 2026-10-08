(() => {
  const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const motionClass = 'folia-motion-in';
  const animate = (elements, start = 0, step = 75) => {
    elements.forEach((element, index) => {
      if (!(element instanceof HTMLElement) || element.classList.contains(motionClass)) return;
      element.style.setProperty('--folia-motion-delay', `${start + index * step}ms`);
      element.classList.add(motionClass);
    });
  };

  const header = document.querySelector('body > header');
  animate(header ? [header] : []);

  const pageHeader = document.querySelector('.page-header');
  if (pageHeader) {
    animate([pageHeader, document.querySelector('.filter-bar')].filter(Boolean), 120, 130);
    animate([...document.querySelectorAll('.grid .card')], 360, 65);
    return;
  }

  const timeline = document.querySelector('#timeline');
  if (timeline) {
    animate([...document.querySelectorAll('main > .hero, main > .section')], 120, 170);
    const revealEntries = () => {
      const entries = [...timeline.querySelectorAll('.entry')];
      entries.forEach((entry, index) => animate([entry], 440 + index * 65, 0));
    };
    revealEntries();
    new MutationObserver(revealEntries).observe(timeline, { childList: true });
    const hero = document.querySelector('#hero');
    if (hero) new MutationObserver(records => {
      records.flatMap(record => [...record.addedNodes])
        .filter(node => node instanceof HTMLElement && node.matches('img'))
        .forEach((image, index) => animate([image], 240 + index * 70, 0));
    }).observe(hero, { childList: true });
    return;
  }

  const mainSections = [...document.querySelectorAll('main > section')];
  if (mainSections.length) {
    animate(mainSections, 120, 135);
    return;
  }

  const article = document.querySelector('body > article');
  if (article) animate([...article.children], 100, 45);
})();
