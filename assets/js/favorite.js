"use strict";

// import all functions
import { generateSidebar } from "./sidebar.js";
import { api_key, imageBaseURL, fetchDataFromServer } from "./api.js";
import { createMovieCard } from "./movie-card.js";
import { search } from "./search.js";
import { showUsername } from "./login-display.js";

const pageContent = document.querySelector("[page-content]");
const favoritesGrid = document.getElementById("favorites-grid");
const emptyMessage = document.getElementById("empty-message");
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

// 从后端获取用户的favorites
const getFavorites = async function (userId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/favorites/${userId}`);
    const data = await response.json();
    
    if (data.success) {
      return data.favorites;
    } else {
      console.error('Unable to retrieve the favorite list:', data.message);
      return [];
    }
  } catch (error) {
    console.error('An error occurred during fetching the favorite list:', error);
    return [];
  }
}

// 创建电影卡片的简化版本
const createSimpleMovieCard = function (movie, userId) {
  const { poster_path, movie_title, release_date, vote_average, movie_id } = movie;
  
  const card = document.createElement("div");
  card.classList.add("movie-card");
  
  card.innerHTML = `
    <figure class="poster-box card-banner">
      <img src="${imageBaseURL}w342${poster_path}" 
           alt="${movie_title}" 
           class="img-cover"
           loading="lazy">
    </figure>
    
    <h4 class="title">${movie_title}</h4>
    
    <div class="meta-list">
      <div class="meta-item">
        <img src="./assets/images/star.png" width="20" height="20" loading="lazy" alt="rating">
        <span class="span">${vote_average ? parseFloat(vote_average).toFixed(1) : 'N/A'}</span>
      </div>
      
      <div class="card-badge">${release_date ? release_date.split("-")[0] : 'N/A'}</div>
    </div>
    
    <button class="card-btn" title="${movie_title}"></button>
    
    <button class="remove-btn" style="position: absolute; top: 10px; right: 10px; background: var(--primary); padding: 8px 12px; border-radius: var(--radius-8); z-index: 2;">
      ✕
    </button>
  `;
  
  // 添加点击跳转到详情页的事件
  const cardBtn = card.querySelector('.card-btn');
  cardBtn.addEventListener('click', function() {
    // 保存movieId到localStorage
    window.localStorage.setItem("movieId", String(movie_id));
    // 跳转到详情页
    window.location.href = `./detail.html?movieId=${movie_id}`;
  });
  
  // 添加移除按钮事件
  const removeBtn = card.querySelector('.remove-btn');
  removeBtn.addEventListener('click', async function(e) {
    e.stopPropagation();
    await removeFromFavorites(userId, movie_id);
    card.remove();
    checkEmpty();
  });
  
  return card;
}

// 从favorites中移除电影
const removeFromFavorites = async function (userId, movieId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/favorites/${userId}/${movieId}`, {
      method: 'DELETE'
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log('Removed from favorites successfully.');
    } else {
      alert(data.message || 'Unable to remove.');
    }
  } catch (error) {
    console.error('An error occurred during removing from favorites:', error);
    alert('Unable to connect to the server.');
  }
}

// 检查是否为空
const checkEmpty = function () {
  const cards = favoritesGrid.querySelectorAll('.movie-card');
  if (cards.length === 0) {
    favoritesGrid.style.display = 'none';
    emptyMessage.style.display = 'block';
  }
}

// 加载favorites
const loadFavorites = async function () {
  const userId = checkLogin();
  if (!userId) return;
  
  const favorites = await getFavorites(userId);
  
  if (favorites.length === 0) {
    emptyMessage.style.display = 'block';
    favoritesGrid.style.display = 'none';
    return;
  }
  
  emptyMessage.style.display = 'none';
  favoritesGrid.style.display = 'grid';
  
  favorites.forEach(movie => {
    const movieCard = createSimpleMovieCard(movie, userId);
    favoritesGrid.appendChild(movieCard);
  });
}

// 页面加载时执行
loadFavorites();

// Search functionality
search();

