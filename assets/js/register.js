'use strict'

const API_BASE_URL = 'http://localhost:5000';

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
		alert("请输入用户名");
		return;
	}

	if (username.value.trim().length < 3) {
		alert("用户名至少需要3个字符");
		return;
	}

	if (!password.value.trim()) {
		alert("请输入密码");
		return;
	}

	if (password.value.trim().length < 6) {
		alert("密码至少需要6个字符");
		return;
	}

	if (password.value !== confirmPassword.value) {
		alert("两次输入的密码不一致");
		return;
	}

	// 禁用按钮防止重复提交
	registerButton.disabled = true;
	registerButton.textContent = '注册中...';

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
			alert("注册成功！现在将跳转到登录页面");
			form.classList.add('was-validated');
			
			// 跳转到登录页面
			window.location.href = './login.html';
		} else {
			// 注册失败
			alert(data.message || "注册失败，请重试");
			registerButton.disabled = false;
			registerButton.textContent = 'Register';
		}
	} catch (error) {
		console.error('注册错误:', error);
		alert("无法连接到服务器，请确保后端服务正在运行");
		registerButton.disabled = false;
		registerButton.textContent = 'Register';
	}
}

const registerButton = document.querySelector('button[type="submit"]');
registerButton.addEventListener('click', tryRegister);

