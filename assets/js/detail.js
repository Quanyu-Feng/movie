"use strict";

import { api_key, imageBaseURL, fetchDataFromServer } from "./api.js";
import { generateSidebar } from "./sidebar.js";
import { createMovieCard } from "./movie-card.js";
import { search } from "./search.js";
import { showUsername } from "./login-display.js";

const urlParams = new URLSearchParams(window.location.search);
const movieId = urlParams.get("movieId") || window.localStorage.getItem("movieId") || '289';
const pageContent = document.querySelector("[page-content]");

generateSidebar();
showUsername();

const getGenres = function (genreList) {
  const newGenreList = [];

  for (const { name } of genreList) {
    newGenreList.push(name);
  }

  return newGenreList.join(", ");
};

const getCasts = function (castList) {
  const newCastList = [];

  for (let i = 0, len = castList.length; i < len && i < 10; i++) {
    const { name } = castList[i];
    newCastList.push(name);
  }
  return newCastList.join(", ");
};

const getDirectors = function (crewList) {
  const directors = crewList.filter(({ job }) => job === "Director");

  const directorList = [];

  for (const { name } of directors) {
    directorList.push(name);
  }

  return directorList.join(", ");
};

// returns only trailers and teasers as array
const filterVideos = function (videoList) {
  return videoList.filter(
    ({ type, site }) =>
      (type === "Trailer" || type === "Teaser") && site === "YouTube"
  );
};

fetchDataFromServer(
  `https://api.themoviedb.org/3/movie/${movieId}?api_key=${api_key}&append_to_response=casts,videos,images,releases`,
  function (movie) {
    const {
      backdrop_path,
      poster_path,
      title,
      release_date,
      runtime,
      vote_average,
      releases: {
        countries: [{ certification }],
      },
      genres,
      overview,
      casts: { cast, crew },
      videos: { results: videos },
    } = movie;



    document.title = `${title} - myMovie Super`;

    const movieDetail = document.createElement("div");
    movieDetail.classList.add("movie-detail");

    movieDetail.innerHTML = `
      <div
        class="backdrop-image"
        style="background-image: url('${imageBaseURL}${"w1280" || "original"}${
      backdrop_path || poster_path
    }');"></div>

      <figure class="poster-box movie-poster">
        <img
          src="${imageBaseURL}w342${poster_path}"
          alt="${title}"
          class="img-cover"
        />
      </figure>

      <div class="detail-box">
        <div class="detail-content">
          <h1 class="heading">${title}</h1>

          <div class="meta-list">
            <div class="meta-item">
              <img
                src="./assets/images/star.png"
                width="20"
                height="20"
                alt="rating"
                style="margin-bottom: 5px"
              />
              <span class="span">${vote_average.toFixed(1)}</span>
            </div>

            <div class="separator"></div>
            <div class="meta-item">${runtime}m</div>
            <div class="separator"></div>
            <div class="meta-item">${release_date.split("-")[0]}</div>

            <div class="meta-item card-badge">${certification}</div>
          </div>

          <p class="genre">${getGenres(genres)}</p>

          <p class="overview">${overview}</p>

          <div style="display: flex; gap: 12px; margin-block: 24px;">
            <button class="btn" id="add-to-favorite" style="background-color: var(--primary);">
              ⭐ Add to Favorites
            </button>
          </div>

          <ul class="detail-list">
            <div class="list-item">
              <p class="list-name">Starring</p>

              <p>${getCasts(cast)}</p>
            </div>

            <div class="list-item">
              <p class="list-name">Directed By</p>

              <p>${getDirectors(crew)}</p>
            </div>
          </ul>
        </div>

        <div class="title-wrapper">
          <h3 class="title-large">Trailers and Clips</h3>
        </div>

        <div class="slider-list">
          <div class="slider-inner"></div>
        </div>
      </div>
    `;

    // 用于存储所有YouTube播放器实例
    const players = [];
    let playerIdCounter = 0;

    for (const { key, name } of filterVideos(videos)) {
      const videoCard = document.createElement("div");
      videoCard.classList.add("video-card");
      
      // 为每个iframe生成唯一ID
      const playerId = `youtube-player-${playerIdCounter++}`;
      
      // 使用enablejsapi=1启用JavaScript API
      videoCard.innerHTML = `
        <div id="${playerId}"></div>
      `;

      movieDetail.querySelector(".slider-inner").appendChild(videoCard);

      // 跟踪这个视频是否已经记录过
      let hasRecorded = false;

      // 记录观看历史的函数
      const recordHistory = async function() {
        if (hasRecorded) return;
        
        const userId = localStorage.getItem('userId');
        if (!userId) return;
        
        hasRecorded = true;
        
        try {
          await fetch('/api/history', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: parseInt(userId),
              movie_id: movie.id,
              movie_title: movie.title,
              poster_path: movie.poster_path,
              release_date: movie.release_date,
              vote_average: movie.vote_average,
              video_key: key,
              video_title: name
            })
          });
          console.log('✅ Added to watch history.', name);
        } catch (error) {
          console.error('❌ Failed to add to watch history:', error);
          hasRecorded = false; // 失败时重置，允许重试
        }
      };

      // 使用YouTube IFrame API创建播放器
      // 需要等待API加载完成
      const createPlayer = () => {
        if (typeof YT === 'undefined' || !YT.Player) {
          // API还没加载完成，等待100ms后重试
          setTimeout(createPlayer, 100);
          return;
        }

        try {
          const player = new YT.Player(playerId, {
            height: '294',
            width: '500',
            videoId: key,
            playerVars: {
              'theme': 'dark',
              'color': 'white',
              'rel': 0,
              'enablejsapi': 1
            },
            events: {
              'onReady': function(event) {
                console.log('🎬 YouTube player is ready:', name);
              },
              'onStateChange': function(event) {
                // YT.PlayerState.PLAYING = 1 (视频开始播放)
                if (event.data === YT.PlayerState.PLAYING) {
                  console.log('▶️ Video now playing:', name);
                  recordHistory();
                }
              },
              'onError': function(event) {
                console.error('❌ YouTube player error:', event.data);
              }
            }
          });
          
          players.push(player);
        } catch (error) {
          console.error('Unable to create YouTube player:', error);
        }
      };

      // 延迟创建播放器，确保DOM已准备好
      setTimeout(createPlayer, 100);
    }

    pageContent.appendChild(movieDetail);

    // API基础URL
    const API_BASE_URL = '';
    
    // 获取用户ID
    const getUserId = () => {
      const userId = localStorage.getItem('userId');
      if (!userId) {
        alert('This is a members-only feature. Redirecting to login page.');
        window.location.href = './login.html';
        return null;
      }
      return userId;
    };
    
    // 添加到favorites的功能
    const addToFavoriteBtn = document.getElementById('add-to-favorite');
    
    // 从后端检查电影是否已在收藏列表中
    const checkIfInFavorites = async (userId) => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/favorites/${userId}`);
        const data = await response.json();
        if (data.success) {
          return data.favorites.some(m => m.movie_id === movie.id);
        }
      } catch (error) {
        console.error('Error occurred during checking favorite list:', error);
      }
      return false;
    };
    
    // 初始化按钮状态
    const initButtons = async () => {
      const userId = getUserId();
      if (!userId) return;
      
      if (await checkIfInFavorites(userId)) {
        addToFavoriteBtn.textContent = '✓ In Favorites';
        addToFavoriteBtn.style.backgroundColor = 'var(--banner-background)';
        addToFavoriteBtn.disabled = true;
      }
    };
    
    initButtons();
    
    // 添加到favorites
    addToFavoriteBtn.addEventListener('click', async () => {
      const userId = getUserId();
      if (!userId) return;
      
      try {
        const response = await fetch(`${API_BASE_URL}/api/favorites`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: parseInt(userId),
            movie_id: movie.id,
            movie_title: movie.title,
            poster_path: movie.poster_path,
            release_date: movie.release_date,
            vote_average: movie.vote_average
          })
        });
        
        const data = await response.json();
        
        if (data.success) {
          addToFavoriteBtn.textContent = '✓ In Favorites';
          addToFavoriteBtn.style.backgroundColor = 'var(--banner-background)';
          addToFavoriteBtn.disabled = true;
          alert('Added to favorite list!');
        } else {
          alert(data.message || 'Unable to add to favorites. Please try again.');
        }
      } catch (error) {
        console.error('Error occurred during adding to favorites:', error);
        alert('Unable to connect to the server.');
      }
    });

    fetchDataFromServer(
      `https://api.themoviedb.org/3/movie/${movieId}/recommendations?api_key=${api_key}&page=1`,
      addSuggestedMovies
    );
  }
);

const addSuggestedMovies = function ({ results: movieList }, title) {
  const movieListElem = document.createElement("section");
  movieListElem.classList.add("movie-list");
  movieListElem.ariaLabel = "You May Also Like";

  movieListElem.innerHTML = `
      <div class="title-wrapper">
        <h3 class="title-large">You May Also Like</h3>
      </div>
  
      <div class="slider-list">
        <div class="slider-inner"></div>
      </div>
    `;

  for (const movie of movieList) {
    const movieCard = createMovieCard(movie); //called from movie_card.js

    movieListElem.querySelector(".slider-inner").appendChild(movieCard);
  }

  pageContent.appendChild(movieListElem);
};

search();
