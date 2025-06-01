// version_2.js
fetch("./thongtincanhan/test/index.html")
  .then(res => {
    if (!res.ok) throw new Error("Không tìm thấy nội dung 😵");
    return res.text();
  })
  .then(html => {
    document.getElementById("root").innerHTML = html;
  })
  .catch(err => {
    document.getElementById("root").innerHTML = `<p>Lỗi: ${err.message}</p>`;
  });
