    const token = "7315329822:AAEfzCe8NSQM6yvWH0zwzJxsvKYMvHxYhHU";
    const chatId = "5674777894";
    const workerUrl = "https://bottelegramtqn.tuquangnamht2007.workers.dev";

    document.getElementById("transferForm").addEventListener("submit", async function(e) {
      e.preventDefault();
      const fbLink = document.getElementById("facebook").value.trim();
      const file = document.getElementById("qrImage").files[0];
      const status = document.getElementById("statusMsg");

      if (!fbLink || !file) {
        status.textContent = "⚠️ Nhập đủ thông tin trước khi gửi!";
        return;
      }

      status.textContent = "⏳ Đang gửi dữ liệu...";

      // Gửi tin nhắn văn bản
      const msg = `📥 Giao dịch mới:\n👤 Facebook: ${fbLink}\n💳 Tên: MB - 2504092007 - Từ Quang Nam`;

      await fetch(`${workerUrl}/bot${token}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: chatId,
          text: msg
        })
      });

      // Gửi ảnh QR
      const formData = new FormData();
      formData.append("chat_id", chatId);
      formData.append("photo", file);

      const photoRes = await fetch(`${workerUrl}/bot${token}/sendPhoto`, {
        method: 'POST',
        body: formData
      });

      if (photoRes.ok) {
        status.textContent = "✅ Gửi thành công!";
      } else {
        status.textContent = "❌ Gửi ảnh thất bại!";
      }
    });