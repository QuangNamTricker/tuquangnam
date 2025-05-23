
    // Tự động hiển thị thời gian
    function updateTime() {
      const now = new Date();
      const timeStr = now.toLocaleString('vi-VN');
      document.getElementById("currentTime").textContent = "Thời gian hiện tại: " + timeStr;
    }
    setInterval(updateTime, 1000);
    updateTime();

    // Nút chuyển đổi iframe và hướng dẫn
    const btn = document.getElementById("controlButton");
    const iframe = document.getElementById("myIframe");
    const main = document.getElementById("mainContent");

    function showLoading() {
      document.getElementById('loading').style.display = 'flex';
      let dots = 0;
      const loadingDots = document.getElementById('loadingDots');
      const dotsInterval = setInterval(() => {
        dots = (dots + 1) % 4;
        loadingDots.textContent = '.'.repeat(dots);
      }, 500);
      
      // Đếm ngược 5 giây
      let timeLeft = 5;
      document.getElementById('countdown').textContent = `Tự động tải sau ${timeLeft} giây...`;
      const countdownInterval = setInterval(() => {
        timeLeft--;
        document.getElementById('countdown').textContent = `Tự động tải sau ${timeLeft} giây...`;
        if (timeLeft <= 0) {
          clearInterval(countdownInterval);
        }
      }, 1000);
      
      return { dotsInterval, countdownInterval };
    }

    btn.onclick = () => {
      // Hiệu ứng confetti
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });

      const { dotsInterval, countdownInterval } = showLoading();
      
      setTimeout(() => {
        clearInterval(dotsInterval);
        clearInterval(countdownInterval);
        document.getElementById('loading').style.display = 'none';
        
        if (iframe.style.display === "block") {
          iframe.style.display = "none";
          main.style.display = "block";
          btn.innerHTML = "👉 Lấy Tài Khoản <img src='https://i.imgur.com/shgRcYn.png' width='20' style='border-radius: 50%;'>";
        } else {
          iframe.style.display = "block";
          main.style.display = "none";
          btn.innerHTML = "👉 Xem Lại Hướng Dẫn <img src='https://i.imgur.com/shgRcYn.png' width='20' style='border-radius: 50%;'>";
        }
      }, 1000);
    };

    // Nút cuộn lên đầu trang
    const backToTop = document.getElementById("backToTop");
    window.onscroll = function () {
      if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backToTop.style.display = "block";
      } else {
        backToTop.style.display = "none";
      }
    };

    function scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    // Dark/Light mode toggle
    const themeToggle = document.getElementById('themeToggle');
    themeToggle.addEventListener('click', () => {
      document.body.classList.toggle('light-mode');
      if (document.body.classList.contains('light-mode')) {
        themeToggle.textContent = '☀️';
      } else {
        themeToggle.textContent = '🌙';
      }
    });

    // Hiển thị số người online (giả lập)
    function updateOnlineUsers() {
      const baseUsers = Math.floor(Math.random() * 50) + 20;
      const hour = new Date().getHours();
      // Giả lập số người online theo giờ
      const hourMultiplier = 0.5 + Math.abs(12 - hour) / 12;
      const randomUsers = Math.floor(baseUsers * hourMultiplier);
      document.getElementById('onlineCounter').textContent = `👥 ${randomUsers} người online`;
    }
    setInterval(updateOnlineUsers, 5000);
    updateOnlineUsers();

    // Thông báo tài khoản mới (giả lập)
    function checkNewAccounts() {
      // 10% cơ hội có thông báo mới
      if (Math.random() < 0.1) {
        const notification = document.getElementById('notification');
        notification.style.display = 'block';
        setTimeout(() => {
          notification.style.display = 'none';
        }, 5000);
      }
    }
    setInterval(checkNewAccounts, 30000);

    // Tự động refresh iframe mỗi 5 phút
    setInterval(() => {
      if (iframe.style.display === 'block') {
        iframe.src = iframe.src; // Refresh iframe
      }
    }, 300000);
    // Thêm hàm copyToClipboard vào script
    function copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(() => {
        alert(`Đã copy: ${text}`);
      }).catch(err => {
        console.error('Lỗi khi copy: ', err);
        prompt('Vui lòng copy thủ công:', text);
      });
    }
    // Mẹo ngẫu nhiên
    const tips = [
      "Không đăng nhập iCloud để tránh bị khóa tài khoản.",
      "Sử dụng mật khẩu mạnh cho tài khoản Apple ID.",
      "Thường xuyên kiểm tra trang để cập nhật tài khoản mới.",
      "Đăng xuất App Store ngay sau khi tải ứng dụng.",
      "Không chia sẻ tài khoản với người lạ."
    ];
    
    function showRandomTip() {
      const randomTip = tips[Math.floor(Math.random() * tips.length)];
      document.getElementById('tipText').textContent = randomTip;
    }
    setInterval(showRandomTip, 15000);
    showRandomTip();

    // Đánh giá sao
    function rate(stars) {
      // Lưu đánh giá vào localStorage
      localStorage.setItem('userRating', stars);
      
      // Hiển thị sao đã chọn
      const starsElements = document.querySelectorAll('.rating span');
      starsElements.forEach((star, index) => {
        if (index < stars) {
          star.classList.add('active');
        } else {
          star.classList.remove('active');
        }
      });
      
      // Thông báo
      alert(`Cảm ơn bạn đã đánh giá ${stars} sao!`);
      
      // Gửi đánh giá lên server (giả lập)
      setTimeout(() => {
        console.log(`Đã gửi đánh giá ${stars} sao lên server`);
      }, 1000);
    }

    // Khôi phục đánh giá nếu có
    const savedRating = localStorage.getItem('userRating');
    if (savedRating) {
      rate(parseInt(savedRating));
    }

    // Copy tài khoản tự động (giả lập)
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('account')) {
        const accountText = e.target.textContent.trim();
        navigator.clipboard.writeText(accountText).then(() => {
          alert(`Đã copy: ${accountText}`);
        }).catch(err => {
          console.error('Lỗi khi copy: ', err);
        });
      }
    });
