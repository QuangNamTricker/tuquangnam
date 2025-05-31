    // Dữ liệu webcon, ông thêm vào đây
    const data = [
      {
        title: " ID APPLE Shadowrocket",
        desc: "Share ID APPLE Để Tải Shadowrocket.",
        img: "https://github.com/QuangNamTricker/tuquangnam/blob/main/chucnang/image/id-apple.png?raw=true",
        url: "../ID-APPLE/index.html"
      },
      {
        title: "AI Veo3",
        desc: "Hướng Dẫn Đăng Ký Tài Khoản Và Sử Dụng AI Veo3.",
        img: "https://github.com/QuangNamTricker/tuquangnam/blob/main/chucnang/image/buy_veo3.png?raw=true",
        url: "../buy_veo3/index.html"
      },
      {
        title: "Confession",
        desc: "Gửi Lời Nhắn Bí Mật Tới ADMIN.",
        img: "https://github.com/QuangNamTricker/tuquangnam/blob/main/chucnang/image/confession.png?raw=true",
        url: "../confession/index.html"
      },
            {
        title: "Contacts",
        desc: "Liên Hệ Với ADMIN.",
        img: "https://github.com/QuangNamTricker/tuquangnam/blob/main/chucnang/image/contacts.png?raw=true",
        url: "../contacts/index.html"
      },
            {
        title: "Photobooth",
        desc: " Chụp Ảnh Với Photobooth.",
        img: "https://github.com/QuangNamTricker/tuquangnam/blob/main/chucnang/image/photobooth.png?raw=true",
        url: "../photobooth/index.html"
      },
      {
        title: "Tạo QR Chuyển Khoản",
        desc: " Tạo QR Chuyển Khoản Để Nhận Tiền.",
        img: "https://github.com/QuangNamTricker/tuquangnam/blob/main/chucnang/image/taoqrchuyenkhoan.png?raw=true",
        url: "../taoqrchuyenkhoan/index.html"
      },
      {
        title: "YouTube No ADS",
        desc: " Xem YouTube Không Quảng Cáo.",
        img: "https://github.com/QuangNamTricker/tuquangnam/blob/main/chucnang/image/youtube.png?raw=true",
        url: "../youtube/index.html"
      }
    ];

    const webList = document.getElementById("webList");
    const search = document.getElementById("search");
    const darkToggle = document.getElementById("darkToggle");

    // Render danh sách với chia sẻ facebook button
    function renderList(filter = "") {
      webList.innerHTML = "";
      data.filter(item =>
        item.title.toLowerCase().includes(filter.toLowerCase()) ||
        item.desc.toLowerCase().includes(filter.toLowerCase())
      ).forEach(item => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
          <a href="${item.url}" target="_blank" rel="noopener" style="text-decoration:none; color:inherit;">
            <img src="${item.img}" alt="${item.title}" />
            <div class="card-content">
              <div class="card-title">${item.title}</div>
              <div class="card-desc">${item.desc}</div>
            </div>
          </a>
          <a href="https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(item.url)}" target="_blank" class="share-btn" title="Share trên Facebook">Chia sẻ Facebook</a>
        `;

        webList.appendChild(card);
      });
    }

    // Search filter
    search.addEventListener("input", e => {
      renderList(e.target.value);
    });

    // Dark/Light mode toggle
    function updateDarkMode(isDark) {
      if (isDark) {
        document.body.classList.add("dark");
        darkToggle.textContent = "☀️";
      } else {
        document.body.classList.remove("dark");
        darkToggle.textContent = "🌙";
      }
      localStorage.setItem("darkMode", isDark);
    }

    darkToggle.addEventListener("click", () => {
      const isDark = document.body.classList.contains("dark");
      updateDarkMode(!isDark);
    });

    // Khởi tạo dark mode theo localStorage
    const savedDarkMode = localStorage.getItem("darkMode") === "true";
    updateDarkMode(savedDarkMode);

    // Render lần đầu
    renderList();
