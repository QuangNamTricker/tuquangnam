const movieListEl = document.getElementById('movie-list');
const playerSection = document.getElementById('player-section');
const movieTitleEl = document.getElementById('movie-title');
const videoPlayer = document.getElementById('video-player');
const episodeListEl = document.getElementById('episode-list');

let movies = [];
let currentMovie = null;
let currentEpisodeIndex = 0;

fetch('movies.json')
  .then(res => res.json())
  .then(data => {
    movies = data;
    renderMovieList();
  })
  .catch(err => {
    movieListEl.innerHTML = '<p style="color:#f00;">Failed to load movies.json</p>';
    console.error(err);
  });

function renderMovieList() {
  movieListEl.innerHTML = '';
  movies.forEach((movie, idx) => {
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.innerHTML = `
      <img src="${movie.image}" alt="${movie.title}" />
      <div class="info">
        <h3>${movie.title}</h3>
        <p>${movie.description}</p>
      </div>
    `;
    card.addEventListener('click', () => {
      openPlayer(idx);
    });
    movieListEl.appendChild(card);
  });
}

function openPlayer(movieIdx) {
  currentMovie = movies[movieIdx];
  currentEpisodeIndex = 0;
  playerSection.classList.remove('hidden');
  movieTitleEl.textContent = currentMovie.title;
  loadEpisode(currentEpisodeIndex);
  renderEpisodeList();
  window.scrollTo({ top: playerSection.offsetTop - 20, behavior: 'smooth' });
}

function loadEpisode(idx) {
  if (!currentMovie) return;
  currentEpisodeIndex = idx;
  const episode = currentMovie.episodes[idx];
  videoPlayer.src = episode.url;
  highlightActiveEpisode();
}

function renderEpisodeList() {
  episodeListEl.innerHTML = '';
  currentMovie.episodes.forEach((ep, idx) => {
    const btn = document.createElement('button');
    btn.textContent = ep.title;
    btn.classList.toggle('active', idx === currentEpisodeIndex);
    btn.addEventListener('click', () => loadEpisode(idx));
    episodeListEl.appendChild(btn);
  });
}

function highlightActiveEpisode() {
  const buttons = episodeListEl.querySelectorAll('button');
  buttons.forEach((btn, idx) => {
    btn.classList.toggle('active', idx === currentEpisodeIndex);
  });
}

// Mảng movie đã có từ trước
//...

// Thêm sự kiện tìm kiếm phim theo title
const searchInput = document.getElementById('search-input');
searchInput.addEventListener('input', () => {
  const query = searchInput.value.trim().toLowerCase();
  if (!query) {
    renderMovieList();
    return;
  }
  const filtered = movies.filter(movie =>
    movie.title.toLowerCase().includes(query)
  );
  renderMovieList(filtered);
});

// Sửa hàm renderMovieList để nhận danh sách phim tùy chọn
function renderMovieList(filteredMovies = movies) {
  movieListEl.innerHTML = '';
  filteredMovies.forEach((movie, idx) => {
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.innerHTML = `
      <img src="${movie.image}" alt="${movie.title}" />
      <div class="info">
        <h3>${movie.title}</h3>
        <p>${movie.description}</p>
      </div>
    `;
    card.addEventListener('click', () => openPlayer(movies.indexOf(movie)));
    movieListEl.appendChild(card);
  });
}

// Dark Mode toggle đơn giản
const btnDarkMode = document.getElementById('btn-darkmode');
btnDarkMode.addEventListener('click', () => {
  document.body.classList.toggle('light-mode');
  if (document.body.classList.contains('light-mode')) {
    btnDarkMode.textContent = '🌞';
  } else {
    btnDarkMode.textContent = '🌙';
  }
});

// Home button
const btnHome = document.getElementById('btn-home');
btnHome.addEventListener('click', () => {
  playerSection.classList.add('hidden');
  searchInput.value = '';
  renderMovieList();
});

// About button
const btnAbout = document.getElementById('btn-about');
btnAbout.addEventListener('click', () => {
  alert('Trang Movie Stream - Dev bởi TQN 🔥\nPhiên bản 1.0');
});
searchInput.addEventListener('input', () => {
  const query = searchInput.value.trim().toLowerCase();
  if (!query) {
    renderMovieList();
    return;
  }
  const filtered = movies.filter(movie =>
    movie.title.toLowerCase().includes(query)
  );
  renderMovieList(filtered);
});
