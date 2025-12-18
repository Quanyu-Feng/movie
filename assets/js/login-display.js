'use strict'

const showUsername = function (){
  if (localStorage.getItem('isLoggedIn') == 'true') {
    const username = localStorage.getItem('username');
    
    // 隐藏登录按钮
    const loginBtn = document.querySelector('.btn-login');
    if (loginBtn) {
      loginBtn.style.display = 'none';
    }
    
    // 显示用户面板
    const userPanel = document.querySelector('.user-panel');
    if (userPanel) {
      userPanel.classList.add('active');
      
      // 设置用户名
      const userNameElement = userPanel.querySelector('.user-name');
      const userAvatar = userPanel.querySelector('.user-avatar');
      if (userNameElement) {
        userNameElement.textContent = username;
      }
      if (userAvatar) {
        // 显示用户名首字母
        userAvatar.textContent = username.charAt(0).toUpperCase();
      }
    }
  }
}

const initUserPanel = function () {
  const userButton = document.querySelector('.user-button');
  const userDropdown = document.querySelector('.user-dropdown');
  
  if (userButton && userDropdown) {
    // 点击用户按钮显示/隐藏下拉菜单
    userButton.addEventListener('click', function(e) {
      e.stopPropagation();
      userButton.classList.toggle('open');
      userDropdown.classList.toggle('show');
    });
    
    // 点击页面其他地方关闭下拉菜单
    document.addEventListener('click', function() {
      userButton.classList.remove('open');
      userDropdown.classList.remove('show');
    });
    
    // 阻止下拉菜单内的点击事件冒泡
    userDropdown.addEventListener('click', function(e) {
      e.stopPropagation();
    });
  }
  
  // 绑定下拉菜单项
  const historyBtn = document.getElementById('goto-history');
  const favoriteBtn = document.getElementById('goto-favorite');
  const logoutBtn = document.getElementById('logout-btn');
  
  if (historyBtn) {
    historyBtn.addEventListener('click', function() {
      window.location.href = './history.html';
    });
  }
  
  if (favoriteBtn) {
    favoriteBtn.addEventListener('click', function() {
      window.location.href = './favorite.html';
    });
  }
  
  if (logoutBtn) {
    logoutBtn.addEventListener('click', logout);
  }
}

const logout = function () {
  // 清除登录状态
  localStorage.removeItem('isLoggedIn');
  localStorage.removeItem('username');
  localStorage.removeItem('userId');
  
  // 跳转到登录页面
  alert('已成功登出');
  window.location.href = './login.html';
}

const checkLoginStatus = function () {
  const isLoggedIn = localStorage.getItem('isLoggedIn');
  return isLoggedIn === 'true';
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
  showUsername();
  initUserPanel();
});

export { showUsername, logout, checkLoginStatus, initUserPanel };