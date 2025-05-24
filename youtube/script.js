const apiKey = "AIzaSyCQLFP6dPYpUUaDisEKdg2MyBs3VUH4pIw";

function searchVideos() {
  const query = document.getElementById("searchInput").value.trim();
  if (!query) return;

  const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=10&q=${encodeURIComponent(
    query
  )}&key=${apiKey}`;

  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      const list = document.getElementById("videoList");
      list.innerHTML = "";

      data.items.forEach((item) => {
        const videoId = item.id.videoId;
        const title = item.snippet.title;
        const thumb = item.snippet.thumbnails.medium.url;

        const div = document.createElement("div");
        div.className = "videoItem";
        div.innerHTML = `
          <img src="${thumb}" />
          <div class="videoInfo">
            <h4>${title}</h4>
          </div>
        `;

        div.onclick = () => playVideo(videoId);
        list.appendChild(div);
      });
    });
}

function playVideo(videoId) {
  const player = document.getElementById("videoPlayer");
  player.innerHTML = `
    <iframe width="100%" height="360" 
      src="https://www.youtube-nocookie.com/embed/${videoId}?rel=0&modestbranding=1&autoplay=1" 
      frameborder="0" allowfullscreen>
    </iframe>
  `;
}
