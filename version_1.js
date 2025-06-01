// main.js - TQN Hacker Portfolio

function initPage() {
  typingEffect();
  startSakura();
}

// 🌸 Sakura Effect
let stop;
const img = new Image();
img.src = "https://i.imgur.com/R9XUjfF.png";

function Sakura(x, y, s, r, fn) {
  this.x = x;
  this.y = y;
  this.s = s;
  this.r = r;
  this.fn = fn;
}

Sakura.prototype.draw = function (cxt) {
  cxt.save();
  cxt.translate(this.x, this.y);
  cxt.rotate(this.r);
  cxt.drawImage(img, 0, 0, 40 * this.s, 40 * this.s);
  cxt.restore();
};

Sakura.prototype.update = function () {
  this.x = this.fn.x(this.x, this.y);
  this.y = this.fn.y(this.y, this.y);
  this.r = this.fn.r(this.r);
  if (
    this.x > window.innerWidth ||
    this.x < 0 ||
    this.y > window.innerHeight ||
    this.y < 0
  ) {
    this.x = Math.random() * window.innerWidth;
    this.y = 0;
    this.s = Math.random();
    this.r = Math.random() * 5;
  }
};

function startSakura() {
  const canvas = document.getElementById("canvas_sakura");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  canvas.style.cssText = "position:fixed; top:0; left:0; pointer-events:none; z-index:-1;";
  const ctx = canvas.getContext("2d");

  const sakuraList = Array.from({ length: 50 }, () =>
    new Sakura(
      Math.random() * window.innerWidth,
      Math.random() * window.innerHeight,
      Math.random(),
      Math.random() * 5,
      {
        x: (x, y) => x + 1.5 * Math.sin(y / 60),
        y: (x, y) => y + 1,
        r: (r) => r + 0.01,
      }
    )
  );

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    sakuraList.forEach((s) => {
      s.update();
      s.draw(ctx);
    });
    stop = requestAnimationFrame(animate);
  }
  animate();
}

// 🧠 Typing Effect
function typingEffect() {
  const text = "Hello, I'm Từ Quang Nam - Full-Stack Developer & Tool Builder";
  let i = 0;
  const el = document.getElementById("typing-text");
  function type() {
    if (i < text.length) {
      el.innerHTML += text.charAt(i);
      i++;
      setTimeout(type, 50);
    }
  }
  type();
}

// 🌗 Dark Mode
function toggleDarkMode() {
  document.body.classList.toggle("light-mode");
}

const bgMusic = document.getElementById('bg-music');
let isPlaying = false;

function toggleMusic() {
  if (isPlaying) {
    bgMusic.pause();
  } else {
    bgMusic.play().catch(e => console.log('Lỗi play nhạc:', e));
  }
  isPlaying = !isPlaying;
}





// 📋 Copy To Clipboard
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert("Đã copy: " + text);
  });
}

// 🖥️ Terminal Commands
function handleTerminal(event) {
  if (event.key === "Enter") {
    const input = event.target.value.trim();
    const output = document.getElementById("terminal-output");
    let response = "";

    const commands = {
      help: "Available commands: help, whoami, skills, contact, projects, socials, cv, clear, about, motto, github, time",
      whoami: "Từ Quang Nam - Full-Stack Developer",
      skills: "HTML/CSS, JavaScript, Python, React, Tool Dev",
      contact: "Facebook: tuquangnam07 | Telegram: @tuquangnam",
      projects: "1. Web Game XYZ\n2. Tool Auto ABC\n3. Portfolio Site",
      socials: "YouTube, Facebook, Telegram, Discord (linked above)",
      cv: "Tải CV tại: /cv.pdf",
      about: "I'm a passionate dev who loves building cool things.",
      motto: "Code như hơi thở. Fix bug như chiến thần.",
      github: "https://github.com/tuquangnam",
      time: new Date().toLocaleString(),
    };

    if (input.toLowerCase() === "clear") {
      output.innerText = "";
      event.target.value = "";
      return;
    }

    if (commands[input.toLowerCase()]) {
      response = commands[input.toLowerCase()];
    } else {
      response = `Command not found: ${input}`;
    }

    output.innerText += `\n> ${input}\n${response}`;
    event.target.value = "";
  }
}

// Handle Resize for Sakura
window.onresize = () => {
  const canvas = document.getElementById("canvas_sakura");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
};

img.onload = startSakura;
