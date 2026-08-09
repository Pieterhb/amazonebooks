import './style.css'

// Store URLs
const PANTHER = 'https://panther-ebooks.com';

// ========== NAVIGATION ==========
const navLinks = document.querySelectorAll('nav a, .nav-btn, .logo, .nav-btn-footer, .series-card');
const views = document.querySelectorAll('.view');

function navigateTo(targetId) {
  views.forEach(view => {
    view.classList.toggle('active', view.id === targetId);
  });
  document.querySelectorAll('nav a').forEach(link => {
    link.classList.toggle('active', link.dataset.target === targetId);
  });
  window.scrollTo(0, 0);
}

navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const target = link.dataset.target;
    if (target) navigateTo(target);
  });
});

// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const navUl = document.querySelector('nav ul');
if (mobileMenuBtn && navUl) {
  mobileMenuBtn.addEventListener('click', () => {
    navUl.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('nav') && !e.target.closest('#mobile-menu-btn')) {
      navUl.classList.remove('open');
    }
  });
}

// =====================================================
// PANTHER eBOOKS — PDF eBooks from panther-ebooks.com
// Many titles are exclusive — not available on Amazon
// =====================================================
const pantherBooks = [
  { title: 'The Creeping Death', img: '/images/covers/10760_1774940080.jpg', store: 'English', url: `${PANTHER}/book-details/MTA3NjA%3D` },
  { title: 'Comrades of the Dragon', img: '/images/covers/10759_1774939568.jpg', store: 'English', url: `${PANTHER}/book-details/MTA3NTk%3D` },
  { title: 'The Blood Message', img: '/images/covers/10758_1774938905.jpg', store: 'English', url: `${PANTHER}/book-details/MTA3NTg%3D` },
  { title: 'La Sorciere Du Sahara', img: '/images/covers/10736_1771921502.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/MTA3MzY%3D` },
  { title: 'The Gallows in the Jungle', img: '/images/covers/10650_1761550849.jpg', store: 'English', url: `${PANTHER}/book-details/MTA2NTA%3D` },
  { title: 'Die Galg in die Oerwoud', img: '/images/covers/10649_1761549228.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/MTA2NDk%3D` },
  { title: 'The Maneaters of Tsavo', img: '/images/covers/10615_1757683870.jpg', store: 'English', url: `${PANTHER}/book-details/MTA2MTU%3D` },
  { title: 'Germ of Death', img: '/images/covers/10602_1755616334.jpg', store: 'English', url: `${PANTHER}/book-details/MTA2MDI%3D` },
  { title: 'The Baron of the Namib', img: '/images/covers/10601_1755613505.jpg', store: 'English', url: `${PANTHER}/book-details/MTA2MDE%3D` },
  { title: 'Death Creeps Closer', img: '/images/covers/10600_1755518622.jpg', store: 'English', url: `${PANTHER}/book-details/MTA2MDA%3D` },
  { title: 'Secret in the Grave', img: '/images/covers/10599_1755518186.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTk%3D` },
  { title: 'Murder in the Mine', img: '/images/covers/10598_1755517771.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTg%3D` },
  { title: 'Execute the Sentence', img: '/images/covers/10597_1755517407.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTc%3D` },
  { title: 'Death has Wings', img: '/images/covers/10596_1755517030.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTY%3D` },
  { title: 'The Deadly Triangle', img: '/images/covers/10595_1755516480.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTU%3D` },
  { title: 'Bloody the Darkness', img: '/images/covers/10594_1755516049.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTQ%3D` },
  { title: 'Fear Tonight', img: '/images/covers/10593_1755515668.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTM%3D` },
  { title: 'Victim of the Tokkelos', img: '/images/covers/10592_1755515010.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTI%3D` },
  { title: 'Stalkers in the Namib', img: '/images/covers/10591_1755514444.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTE%3D` },
  { title: 'The Snakes of Tumara', img: '/images/covers/10590_1755512873.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1OTA%3D` },
  { title: 'The Deranged Visitor', img: '/images/covers/10589_1755512239.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1ODk%3D` },
  { title: 'Spirit of the Witch Doctor', img: '/images/covers/10588_1755511730.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1ODg%3D` },
  { title: 'Vengeance from the Past', img: '/images/covers/10587_1755511058.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1ODc%3D` },
  { title: 'The Treasures of Monomotapa', img: '/images/covers/10586_1755510638.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1ODY%3D` },
  { title: 'Secret of the Cederberg', img: '/images/covers/10585_1755510066.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1ODU%3D` },
  { title: 'The Bloodhounds Bark', img: '/images/covers/10584_1755508826.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1ODQ%3D` },
  { title: 'Vultures of the Kalahari', img: '/images/covers/10583_1755508463.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1ODM%3D` },
  { title: 'Night of no Mercy', img: '/images/covers/10582_1755508077.jpg', store: 'English', url: `${PANTHER}/book-details/MTA1ODI%3D` },
  { title: 'Murder on Board Ship', img: '/images/covers/10469_1749561796.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0Njk%3D` },
  { title: 'Bonds of Death', img: '/images/covers/10468_1749561252.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0Njg%3D` },
  { title: 'Unrest in Namibia', img: '/images/covers/10467_1749560747.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0Njc%3D` },
  { title: 'The Fateful Date', img: '/images/covers/10466_1749560289.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NjY%3D` },
  { title: 'The Winged Fortune', img: '/images/covers/10465_1749559807.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NjU%3D` },
  { title: 'The Missing Girl', img: '/images/covers/10464_1749559346.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NjQ%3D` },
  { title: 'The Golden Dragon', img: '/images/covers/10463_1749558064.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NjM%3D` },
  { title: 'Scream at Night', img: '/images/covers/10449_1748708904.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDk%3D` },
  { title: 'Temple of Violence', img: '/images/covers/10447_1748707783.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDc%3D` },
  { title: 'Sweet Revenge', img: '/images/covers/10446_1748707067.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDY%3D` },
  { title: 'Darke Vengeance', img: '/images/covers/10445_1748705609.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDU%3D` },
  { title: 'The Deserters', img: '/images/covers/10444_1748705176.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDQ%3D` },
  { title: 'Area Zero', img: '/images/covers/10443_1748704624.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDM%3D` },
  { title: 'Bloody Ruby', img: '/images/covers/10442_1748706293.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDI%3D` },
  { title: 'Companions of Death', img: '/images/covers/10441_1748703846.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDE%3D` },
  { title: 'Vengeance Sweeps the Sahara', img: '/images/covers/10440_1748701909.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0NDA%3D` },
  { title: 'Shadows over the Sahara', img: '/images/covers/10439_1748699333.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0Mzk%3D` },
  { title: 'Bloodhound in the Sahara', img: '/images/covers/10438_1748698597.jpg', store: 'English', url: `${PANTHER}/book-details/MTA0Mzg%3D` },
  { title: 'Black Sails on the Horizon', img: '/images/covers/10292_1745661700.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyOTI%3D` },
  { title: 'In Enemy Hands', img: '/images/covers/10291_1745661299.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyOTE%3D` },
  { title: 'The Yellow Dragon', img: '/images/covers/10290_1745660922.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyOTA%3D` },
  { title: 'Stronghold of the Pirates', img: '/images/covers/10289_1745660197.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODk%3D` },
  { title: 'The Secret Mantle', img: '/images/covers/10288_1745659752.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODg%3D` },
  { title: 'The Skull', img: '/images/covers/10287_1745658567.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODc%3D` },
  { title: 'Predators from the East', img: '/images/covers/10286_1745658200.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODY%3D` },
  { title: 'The Coast of Barbary', img: '/images/covers/10285_1745657418.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODU%3D` },
  { title: 'Ghost Ship of Biscay', img: '/images/covers/10284_1745656062.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODQ%3D` },
  { title: 'The Blue Ruby', img: '/images/covers/10283_1745655530.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODM%3D` },
  { title: "The Pirate's Treasure", img: '/images/covers/10282_1745654986.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODI%3D` },
  { title: 'Arm from the Deep', img: '/images/covers/10281_1745654623.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODE%3D` },
  { title: 'The Black Seagull', img: '/images/covers/10280_1745653940.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyODA%3D` },
  { title: 'Sea Vultures', img: '/images/covers/10279_1745653605.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNzk%3D` },
  { title: 'The Spy', img: '/images/covers/10278_1745650097.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNzg%3D` },
  { title: "Falcon in the Crow's Nest", img: '/images/covers/10277_1745649621.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNzc%3D` },
  { title: 'The Ransom', img: '/images/covers/10276_1745649011.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNzY%3D` },
  { title: 'Captain Oloff the Pirate', img: '/images/covers/10271_1745587924.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNzE%3D` },
  { title: 'Scum of the Seas', img: '/images/covers/10270_1745587508.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNzA%3D` },
  { title: 'Sea of Vengeance', img: '/images/covers/10269_1745586939.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNjk%3D` },
  { title: 'Master of the Sword', img: '/images/covers/10268_1745586532.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNjg%3D` },
  { title: 'Deathtrap in the Desert', img: '/images/covers/10247_1770382820.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNDc%3D` },
  { title: 'Death in the Shadows', img: '/images/covers/10246_1770382703.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNDY%3D` },
  { title: 'Flames in the Temple', img: '/images/covers/10245_1770380253.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNDU%3D` },
  { title: 'Vengeance is Mine', img: '/images/covers/10244_1770380179.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNDQ%3D` },
  { title: 'Guests of Death', img: '/images/covers/10243_1770380086.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNDM%3D` },
  { title: 'Bloody Sunrise', img: '/images/covers/10241_1770379921.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyNDE%3D` },
  { title: 'Bloodstained Dunes', img: '/images/covers/10239_1770379747.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/MTAyMzk%3D` },
  { title: 'Curse of the Ruby', img: '/images/covers/10238_1770379617.jpg', store: 'English', url: `${PANTHER}/book-details/MTAyMzg%3D` },
  { title: 'Whispers of the Sunken Ship', img: '/images/covers/10011_1738592310.jpg', store: 'English', url: `${PANTHER}/book-details/MTAwMTE%3D` },
  { title: 'Pirates Execute the Verdict', img: '/images/covers/10010_1738591729.jpg', store: 'English', url: `${PANTHER}/book-details/MTAwMTA%3D` },
  { title: 'Curse of the Mad Pirate', img: '/images/covers/10009_1738591372.jpg', store: 'English', url: `${PANTHER}/book-details/MTAwMDk%3D` },
  { title: "The King's Ransom", img: '/images/covers/10008_1738590931.jpg', store: 'English', url: `${PANTHER}/book-details/MTAwMDg%3D` },
  { title: 'Quest for the Pearl of Malsia', img: '/images/covers/10007_1738590397.jpg', store: 'English', url: `${PANTHER}/book-details/MTAwMDc%3D` },
  { title: 'Echoes from the Sky', img: '/images/covers/10006_1738589965.jpg', store: 'English', url: `${PANTHER}/book-details/MTAwMDY%3D` },
  { title: 'Emerald of the High Seas', img: '/images/covers/10005_1738589533.jpg', store: 'English', url: `${PANTHER}/book-details/MTAwMDU%3D` },
  { title: 'Tamar and the Invaders', img: '/images/covers/9831_1735144732.jpg', store: 'English', url: `${PANTHER}/book-details/OTgzMQ%3D%3D` },
  { title: 'Tamar of the Forest', img: '/images/covers/9830_1735144605.jpg', store: 'English', url: `${PANTHER}/book-details/OTgzMA%3D%3D` },
  { title: 'Land of the Vampires', img: '/images/covers/9825_1734802417.jpg', store: 'English', url: `${PANTHER}/book-details/OTgyNQ%3D%3D` },
  { title: 'Revolution in the Jungle', img: '/images/covers/9824_1734802170.jpg', store: 'English', url: `${PANTHER}/book-details/OTgyNA%3D%3D` },
  { title: 'The Leopard Gang', img: '/images/covers/9823_1734801833.jpg', store: 'English', url: `${PANTHER}/book-details/OTgyMw%3D%3D` },
  { title: 'Hunters of Zarsjata', img: '/images/covers/9822_1734801443.jpg', store: 'English', url: `${PANTHER}/book-details/OTgyMg%3D%3D` },
  { title: 'The Octopus', img: '/images/covers/9821_1734800493.jpg', store: 'English', url: `${PANTHER}/book-details/OTgyMQ%3D%3D` },
  { title: 'Gold City of Sheba', img: '/images/covers/9820_1734800050.jpg', store: 'English', url: `${PANTHER}/book-details/OTgyMA%3D%3D` },
  { title: 'Riders of Death', img: '/images/covers/9815_1734612305.jpg', store: 'English', url: `${PANTHER}/book-details/OTgxNQ%3D%3D` },
  { title: 'Hoofbeats at Midnight', img: '/images/covers/9814_1734611627.jpg', store: 'English', url: `${PANTHER}/book-details/OTgxNA%3D%3D` },
  { title: 'No Forgiveness', img: '/images/covers/9813_1734611283.jpg', store: 'English', url: `${PANTHER}/book-details/OTgxMw%3D%3D` },
  { title: 'Beloved Traitor', img: '/images/covers/9812_1734610234.jpg', store: 'English', url: `${PANTHER}/book-details/OTgxMg%3D%3D` },
  { title: 'Traces in the Dew', img: '/images/covers/9811_1734609599.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/OTgxMQ%3D%3D` },
  { title: 'Judgement of the Mountains', img: '/images/covers/9810_1734608945.jpg', store: 'English', url: `${PANTHER}/book-details/OTgxMA%3D%3D` },
  { title: 'The Alley of Tears', img: '/images/covers/9809_1734608587.jpg', store: 'English', url: `${PANTHER}/book-details/OTgwOQ%3D%3D` },
  { title: 'Flame of the Lowveld', img: '/images/covers/9808_1734608050.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/OTgwOA%3D%3D` },
  { title: 'The Masked Robber Prevails', img: '/images/covers/9796_1755801383.jpg', store: 'English', url: `${PANTHER}/book-details/OTc5Ng%3D%3D` },
  { title: 'The Masked Robber Keeps Watch', img: '/images/covers/9795_1755801167.jpg', store: 'English', url: `${PANTHER}/book-details/OTc5NQ%3D%3D` },
  { title: 'Message for the Masked Robber', img: '/images/covers/9794_1755801010.jpg', store: 'English', url: `${PANTHER}/book-details/OTc5NA%3D%3D` },
  { title: "The Masked Robber's Secret", img: '/images/covers/9793_1755800936.jpg', store: 'English', url: `${PANTHER}/book-details/OTc5Mw%3D%3D` },
  { title: 'The Masked Robber Rides in the Night', img: '/images/covers/9792_1755800827.jpg', store: 'English', url: `${PANTHER}/book-details/OTc5Mg%3D%3D` },
  { title: 'The Red Ruby', img: '/images/covers/9776_1738587155.jpg', store: 'English', url: `${PANTHER}/book-details/OTc3Ng%3D%3D` },
  { title: 'Ravishing Armada', img: '/images/covers/9775_1745654253.jpg', store: 'English', url: `${PANTHER}/book-details/OTc3NQ%3D%3D` },
  { title: 'Deserter in Algeria', img: '/images/covers/9774_1733908557.jpg', store: 'English', url: `${PANTHER}/book-details/OTc3NA%3D%3D` },
  { title: 'Cavemen Valley', img: '/images/covers/9773_1734800967.jpg', store: 'English', url: `${PANTHER}/book-details/OTc3Mw%3D%3D` },
  { title: 'Masked Murderers', img: '/images/covers/9770_1757237521.jpg', store: 'English', url: `${PANTHER}/book-details/OTc3MA%3D%3D` },
  { title: 'The Masked Robber and his Gang', img: '/images/covers/8766_1755800579.jpg', store: 'English', url: `${PANTHER}/book-details/ODc2Ng%3D%3D` },
  { title: 'Long Live The Masked Robber', img: '/images/covers/8535_1755800464.jpg', store: 'English', url: `${PANTHER}/book-details/ODUzNQ%3D%3D` },
  { title: 'The Masked Robber', img: '/images/covers/8098_1755800345.jpg', store: 'English', url: `${PANTHER}/book-details/ODA5OA%3D%3D` },
  { title: 'The Fort is Quiet', img: '/images/covers/7744_1681219351.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/Nzc0NA%3D%3D` },
  { title: 'Revenge of the Desert', img: '/images/covers/7743_1681218940.jpg', store: 'English', url: `${PANTHER}/book-details/Nzc0Mw%3D%3D` },
  { title: 'The Scarlet Riders', img: '/images/covers/7742_1681218566.jpg', store: 'English', url: `${PANTHER}/book-details/Nzc0Mg%3D%3D` },
  { title: 'Footsteps to Death', img: '/images/covers/7741_1681217948.jpg', store: 'English', url: `${PANTHER}/book-details/Nzc0MQ%3D%3D` },
  { title: 'Witch of the Sahara', img: '/images/covers/7740_1681217481.jpg', store: 'English', url: `${PANTHER}/book-details/Nzc0MA%3D%3D` },
  { title: 'Revenge of the Sabre', img: '/images/covers/7726_1770379509.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/NzcyNg%3D%3D` },
  { title: 'Mademoiselle Julie', img: '/images/covers/7725_1770379435.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/NzcyNQ%3D%3D` },
  { title: 'The Tracks are Calling', img: '/images/covers/7724_1770379335.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/NzcyNA%3D%3D` },
  { title: 'Blood in front of the Sun', img: '/images/covers/7723_1770379226.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/NzcyMw%3D%3D` },
  { title: 'Thundering Hooves', img: '/images/covers/7722_1770379150.jpg', store: 'Afrikaans', url: `${PANTHER}/book-details/NzcyMg%3D%3D` },
];

// =====================================================
// CARD RENDERER
// =====================================================
function getBadgeClass(store) {
  if (store === 'Afrikaans') return 'badge-afrikaans';
  if (store === 'English') return 'badge-english';
  return 'badge-panther';
}

function createCard(book) {
  const badgeClass = getBadgeClass(book.store);
  return `
    <article class="book-card" data-store="${book.store}">
      <div class="book-img-wrapper">
        <img 
          src="${book.img}" 
          alt="${book.title}" 
          loading="lazy"
          onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
        >
        <div class="img-fallback" style="display:none">
          <span>📖</span>
          <strong>${book.title}</strong>
        </div>
        <span class="store-badge ${badgeClass}">${book.store}</span>
      </div>
      <div class="book-content">
        <h3>${book.title}</h3>
        <p>Click below to view this book and discover more in the collection.</p>
        <a href="${book.url}" target="_blank" rel="noopener" class="btn btn-primary">View Book</a>
      </div>
    </article>
  `;
}

function renderGrid(containerId, books) {
  const container = document.getElementById(containerId);
  if (container) {
    container.innerHTML = books.map(createCard).join('');
  }
}

// =====================================================
// FILTER LOGIC
// =====================================================
function setupFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const bar = btn.closest('.filter-bar');
      bar.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const store = btn.dataset.store;
      const gridId = bar.dataset.grid;
      let books = pantherBooks;
      if (store !== 'all') {
        books = books.filter(b => b.store === store);
      }
      renderGrid(gridId, books);
    });
  });
}

// =====================================================
// INITIALIZE
// =====================================================
document.addEventListener('DOMContentLoaded', () => {
  // Home featured — show the 9 most recent books
  const homeFeatured = pantherBooks.slice(0, 9);
  renderGrid('home-featured-grid', homeFeatured);
  renderGrid('panther-grid', pantherBooks);
  setupFilters();
});
