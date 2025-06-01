
    // Preloader
    window.addEventListener('load', function() {
      setTimeout(function() {
        document.getElementById('preloader').style.opacity = '0';
        setTimeout(function() {
          document.getElementById('preloader').style.display = 'none';
        }, 500);
      }, 1000);
    });

    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle.querySelector('i');
    
    // Kiểm tra theme từ localStorage hoặc preference hệ thống
    const savedTheme = localStorage.getItem('theme') || 
                      (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
    
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    themeToggle.addEventListener('click', function() {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
      if (theme === 'dark') {
        themeIcon.className = 'fas fa-moon';
      } else {
        themeIcon.className = 'fas fa-sun';
      }
    }

    // Typing effect
    const textToType = `THIẾT KẾ WEBSITE THEO YÊU CẦU\nCHUẨN SEO, CHUẨN UX/UI\nBẢO HÀNH ĐẾN KHI SẬP GOOGLE\nUY TÍN ĐẶT LÊN HÀNG ĐẦU\nZALO: 0941.564.770`;
    const typingText = document.getElementById('typingText');
    let charIndex = 0;
    
    function typeText() {
      if (charIndex < textToType.length) {
        // Xử lý ký tự xuống dòng
        if (textToType.charAt(charIndex) === '\n') {
          typingText.innerHTML += '<br>';
        } else {
          typingText.innerHTML += textToType.charAt(charIndex);
        }
        charIndex++;
        setTimeout(typeText, 50); // Tốc độ đánh máy
      } else {
        typingText.classList.remove('typing-text');
      }
    }
    
    // Bắt đầu hiệu ứng sau khi preloader kết thúc
    setTimeout(() => {
      typingText.classList.add('typing-text');
      typeText();
    }, 1500);

    // Timer
    function updateTimer() {
      const createdAt = new Date("2025-06-01T00:00:00");
      const now = new Date();
      const diff = Math.floor((now - createdAt) / 1000);
      
      const days = Math.floor(diff / (3600 * 24));
      const hours = Math.floor((diff % (3600 * 24)) / 3600);
      const minutes = Math.floor((diff % 3600) / 60);
      const seconds = diff % 60;
      
      document.getElementById("timer").innerHTML = `${days} ngày ${hours} giờ ${minutes} phút ${seconds} giây`;
    }
    
    setInterval(updateTimer, 1000);
    updateTimer();

    // Music player
    const audio = document.getElementById('bgMusic');
    let currentSong = "";
    let isPlaying = false;
    
    function changeSong(url) {
      if (url !== currentSong) {
        currentSong = url;
        audio.src = url;
        audio.volume = document.getElementById('volumeControl').value;
        
        if (url) {
          audio.play()
            .then(() => {
              isPlaying = true;
              updatePlayButton();
            })
            .catch(error => {
              console.log("Auto-play was prevented:", error);
              // Hiển thị nút play để người dùng có thể bắt đầu phát nhạc
              isPlaying = false;
              updatePlayButton();
            });
        } else {
          audio.pause();
          isPlaying = false;
          updatePlayButton();
        }
      }
    }
    
    function toggleMusic() {
      if (currentSong) {
        if (isPlaying) {
          audio.pause();
        } else {
          audio.play();
        }
        isPlaying = !isPlaying;
        updatePlayButton();
      } else {
        // Nếu chưa chọn bài hát, chọn bài đầu tiên trong danh sách
        const select = document.getElementById('songSelect');
        if (select.options.length > 1) {
          select.selectedIndex = 1;
          changeSong(select.value);
        }
      }
    }
    
    function setVolume(volume) {
      audio.volume = volume;
    }
    
    function updatePlayButton() {
      const playIcon = document.getElementById('playIcon');
      const playText = document.getElementById('playText');
      
      if (isPlaying) {
        playIcon.className = 'fas fa-pause';
        playText.textContent = 'Tạm dừng';
      } else {
        playIcon.className = 'fas fa-play';
        playText.textContent = currentSong ? 'Tiếp tục' : 'Phát nhạc';
      }
    }
    
    // Theo dõi sự kiện kết thúc bài hát (đề phòng)
    audio.addEventListener('ended', function() {
      isPlaying = false;
      updatePlayButton();
    });

    // Particles.js
    particlesJS('particles-js', {
      "particles": {
        "number": {
          "value": 80,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#00f0ff"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.1,
            "sync": false
          }
        },
        "size": {
          "value": 3,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 150,
          "color": "#00f0ff",
          "opacity": 0.2,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": false,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "push"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 140,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 40,
            "duration": 2,
            "opacity": 8,
            "speed": 3
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 4
          },
          "remove": {
            "particles_nb": 2
          }
        }
      },
      "retina_detect": true
    });

    // Visit counter (simplified - would use localStorage for demo)
    function updateVisitCount() {
      let count = localStorage.getItem('visitCount');
      if (!count) {
        count = 0;
      }
      count = parseInt(count) + 1;
      localStorage.setItem('visitCount', count);
      document.getElementById('visitCount').textContent = count;
      
      // Animation for the counter
      const counter = document.getElementById('visitCount');
      counter.style.transform = 'scale(1.5)';
      setTimeout(() => {
        counter.style.transform = 'scale(1)';
      }, 300);
    }
    
    // Initialize
    window.addEventListener('DOMContentLoaded', () => {
      updateVisitCount();
    });
