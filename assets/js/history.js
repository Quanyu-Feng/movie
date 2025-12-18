"use strict";

// import all functions
import { generateSidebar } from "./sidebar.js";
import { api_key, imageBaseURL, fetchDataFromServer } from "./api.js";
import { createMovieCard } from "./movie-card.js";
import { search } from "./search.js";
import { showUsername } from "./login-display.js";

const pageContent = document.querySelector("[page-content]");
const historyGrid = document.getElementById("history-grid");
const emptyMessage = document.getElementById("empty-message");
const clearHistoryBtn = document.getElementById("clear-history-btn");
const API_BASE_URL = '';

generateSidebar();
showUsername();

// 检查用户是否登录
const checkLogin = function () {
  const isLoggedIn = localStorage.getItem('isLoggedIn');
  const userId = localStorage.getItem('userId');
  if (!isLoggedIn || !userId) {
    alert('This is a members-only area. Redirecting to login page.');
    localStorage.setItem('loginRedirect', window.location.href);
    window.location.href = './login.html';
    return null;
  }
  return userId;
}

// 从后端获取用户的观看历史
const getHistory = async function (userId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/history/${userId}`);
    const data = await response.json();
    
    if (data.success) {
      return data.history;
    } else {
      console.error('Unable to fetch watch history:', data.message);
      return [];
    }
  } catch (error) {
    console.error('An error occurred during fetching the watch history:', error);
    return [];
  }
}

// 创建历史记录卡片
const createHistoryCard = function (record) {
  const { poster_path, movie_title, release_date, vote_average, movie_id, video_title, video_key, watched_at } = record;
  
  const card = document.createElement("div");
  card.classList.add("history-card");
  card.style.marginBottom = "32px";
  
  // 格式化时间
  const watchedDate = new Date(watched_at);
  const formattedDate = watchedDate.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
  
  card.innerHTML = `
    <div style="display: flex; gap: 20px; align-items: flex-start; flex-wrap: wrap;">
      <!-- YouTube Video Player -->
      <div style="flex: 1; min-width: 300px;">
        ${video_key ? `
          <div class="video-card" style="width: 100%; max-width: 560px; aspect-ratio: 16/9;">
            <iframe
              width="100%"
              height="100%"
              src="https://www.youtube.com/embed/${video_key}?theme=dark&color=white&rel=0"
              frameborder="0"
              allowfullscreen="1"
              title="${video_title || movie_title}"
              class="img-cover"
              loading="lazy"
            ></iframe>
          </div>
        ` : `
          <figure class="poster-box" style="width: 100%; max-width: 300px;">
            <img src="${imageBaseURL}w342${poster_path}" 
                 alt="${movie_title}" 
                 class="img-cover"
                 loading="lazy">
          </figure>
        `}
      </div>
      
      <!-- Movie Info -->
      <div style="flex: 1; min-width: 250px;">
        <h3 class="title" style="font-size: 2rem; margin-bottom: 12px; cursor: pointer;" onclick="window.location.href='./detail.html?movieId=${movie_id}'">
          ${movie_title}
        </h3>
        
        <div class="meta-list" style="margin-bottom: 12px;">
          <div class="meta-item">
            <img src="./assets/images/star.png" width="20" height="20" loading="lazy" alt="rating">
            <span class="span">${vote_average ? parseFloat(vote_average).toFixed(1) : 'N/A'}</span>
          </div>
          
          <div class="separator"></div>
          
          <div class="card-badge">${release_date ? release_date.split("-")[0] : 'N/A'}</div>
        </div>
        
        <p style="font-size: 1.4rem; color: var(--text-color); margin-bottom: 8px;">
          📺 ${video_title || 'Trailer'}
        </p>
        
        <p style="font-size: 1.2rem; color: var(--on-surface-variant); margin-bottom: 12px;">
          ⏰ ${formattedDate}
        </p>
        
        <button class="btn" onclick="window.location.href='./detail.html?movieId=${movie_id}'" 
                style="background-color: var(--primary-variant); padding: 8px 16px; font-size: 1.3rem;">
          View Movie Details
        </button>
      </div>
    </div>
    
    <div style="height: 1px; background: var(--banner-background); margin-top: 24px;"></div>
  `;
  
  return card;
}

// 清除所有历史记录
const clearHistory = async function (userId) {
  if (!confirm('Your watch history will be permanently delted. This action cannot be undone. Are you sure?')) {
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/history/${userId}`, {
      method: 'DELETE'
    });
    
    const data = await response.json();
    
    if (data.success) {
      historyGrid.innerHTML = '';
      emptyMessage.style.display = 'block';
      historyGrid.style.display = 'none';
      clearHistoryBtn.style.display = 'none';
      alert('History cleared successfully.');
    } else {
      alert(data.message || 'Unable to clear history.');
    }
  } catch (error) {
    console.error('An error occurred during clearing the watch history:', error);
    alert('Unable to connect to the server');
  }
}

// 检查是否为空
const checkEmpty = function () {
  const cards = historyGrid.querySelectorAll('.movie-card');
  if (cards.length === 0) {
    historyGrid.style.display = 'none';
    emptyMessage.style.display = 'block';
    clearHistoryBtn.style.display = 'none';
  }
}

// 加载历史记录
const loadHistory = async function () {
  const userId = checkLogin();
  if (!userId) return;
  
  const history = await getHistory(userId);
  
  if (history.length === 0) {
    emptyMessage.style.display = 'block';
    historyGrid.style.display = 'none';
    clearHistoryBtn.style.display = 'none';
    return;
  }
  
  emptyMessage.style.display = 'none';
  historyGrid.style.display = 'block';
  clearHistoryBtn.style.display = 'block';
  
  history.forEach(record => {
    const historyCard = createHistoryCard(record);
    historyGrid.appendChild(historyCard);
  });
  
  // 绑定清除历史按钮
  clearHistoryBtn.addEventListener('click', () => clearHistory(userId));
}

// 页面加载时执行
loadHistory();

// Search functionality
search();

