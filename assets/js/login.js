'use strict'

const API_BASE_URL = '';

const tryLogin = async function (event) {
	event.preventDefault();
	event.stopPropagation();

	const form = document.querySelector('.needs-validation');
	const username = document.getElementById("username");
	const password = document.getElementById("password");
	const loginButton = document.querySelector('button[type="submit"]');

	// 基本验证
	if (!username.value.trim() || !password.value.trim()) {
		alert("Please enter both username and password.");
		return;
	}

	// 禁用按钮防止重复提交
	loginButton.disabled = true;
	loginButton.textContent = 'Signing in... Please wait.';

	try {
		const response = await fetch(`${API_BASE_URL}/api/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				username: username.value.trim(),
				password: password.value.trim()
			})
		});

		const data = await response.json();

		if (data.success) {
			// 登录成功
			alert(`Login successful! ${data.username}, welcome back!`);
			form.classList.add('was-validated');
			
			// 保存登录状态和用户信息
			localStorage.setItem('isLoggedIn', 'true');
			localStorage.setItem('username', data.username);
			localStorage.setItem('userId', data.user_id);
			
			// 重定向到之前的页面或首页
			const redirectUrl = localStorage.getItem('loginRedirect') || './index.html';
			localStorage.removeItem('loginRedirect');
			window.location.href = redirectUrl;
		} else {
			// 登录失败
			alert(data.message || "Incorrect username or password. Note that both fields are case-sensitive.");
			loginButton.disabled = false;
			loginButton.textContent = 'Login';
		}
	} catch (error) {
		console.error('Error:', error);
		alert("Unable to connect the authentication server. Please try again later.");
		loginButton.disabled = false;
		loginButton.textContent = 'Login';
	}
}

const goBack = function () {
	const redirectUrl = localStorage.getItem('loginRedirect') || './index.html';
	localStorage.removeItem('loginRedirect');
	window.location.href = redirectUrl;
}

const loginButton = document.querySelector('button[type="submit"]');
loginButton.addEventListener('click', tryLogin);


