const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const snapBtn = document.getElementById('snap');
const downloadLink = document.getElementById('download');
const filterSelect = document.getElementById('filter');
const useFrame = document.getElementById('useFrame');
const useSticker = document.getElementById('useSticker');

let frameImg = new Image();
frameImg.src = 'assets/frame.png';

let stickerImg = new Image();
stickerImg.src = 'assets/sticker1.png';

// Bật webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    alert('Không thể bật webcam: ' + err);
  });

// Áp dụng filter real-time
filterSelect.addEventListener('change', () => {
  video.style.filter = filterSelect.value;
});

// Chụp ảnh
snapBtn.addEventListener('click', () => {
  const selectedFilter = filterSelect.value;
  ctx.filter = selectedFilter;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  ctx.filter = 'none';

  if (useFrame.checked) {
    ctx.drawImage(frameImg, 0, 0, canvas.width, canvas.height);
  }

  if (useSticker.checked) {
    ctx.drawImage(stickerImg, 450, 350, 120, 120); // vị trí sticker
  }

  const imgData = canvas.toDataURL('image/png');
  downloadLink.href = imgData;
});
