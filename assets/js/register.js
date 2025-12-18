'use strict'

const API_BASE_URL = '';

const tryRegister = async function (event) {
	event.preventDefault();
	event.stopPropagation();

	const form = document.querySelector('.needs-validation');
	const username = document.getElementById("username");
	const password = document.getElementById("password");
	const confirmPassword = document.getElementById("confirmPassword");
	const registerButton = document.querySelector('button[type="submit"]');

	// 基本验证
	if (!username.value.trim()) {
		alert("Please enter the username.");
		return;
	}

	if (username.value.trim().length < 3) {
		alert("Username must be at least 3 characters long.");
		return;
	}

	if (!password.value.trim()) {
		alert("Please enter the password.");
		return;
	}

	if (password.value.trim().length < 6) {
		alert("Password must be at least 6 characters long.");
		return;
	}

	if (password.value !== confirmPassword.value) {
		alert("The two password fields did not match.");
		return;
	}

	// 禁用按钮防止重复提交
	registerButton.disabled = true;
	registerButton.textContent = 'Registering your account. Please wait...';

	try {
		const response = await fetch(`${API_BASE_URL}/api/register`, {
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
			// 注册成功
			alert(`Welcome aboard, ${username.value.trim()}! You will now be redirected to the previous page.`);
			form.classList.add('was-validated');
			
			// 跳转到登录页面
			window.location.href = './login.html';
		} else {
			// 注册失败
			alert(data.message || "Registration failed, please try again.");
			registerButton.disabled = false;
			registerButton.textContent = 'Register';
		}
	} catch (error) {
		console.error('An error occured during registration:', error);
		alert("Unable to connect the authentication server. Please try again later.");
		registerButton.disabled = false;
		registerButton.textContent = 'Register';
	}
}

const registerButton = document.querySelector('button[type="submit"]');
registerButton.addEventListener('click', tryRegister);

