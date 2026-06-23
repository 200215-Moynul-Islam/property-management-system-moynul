document.addEventListener("DOMContentLoaded", function () {
  const mainViewer = document.getElementById("mainViewer");
  const thumbnails = document.querySelectorAll(".thumbnail-target");

  if (!mainViewer || thumbnails.length === 0) return;

  thumbnails.forEach((thumb) => {
    thumb.addEventListener("click", function () {
      mainViewer.src = this.src;

      document.querySelectorAll(".thumb-track").forEach((track) => {
        track.classList.remove("active-thumb");
      });

      this.parentElement.classList.add("active-thumb");
    });
  });
});
