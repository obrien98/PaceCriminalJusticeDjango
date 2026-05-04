document.addEventListener("DOMContentLoaded", () => {
  const triggers = Array.from(document.querySelectorAll(".glightbox"));
  if (!triggers.length) {
    return;
  }

  const overlay = document.createElement("div");
  overlay.className = "lightbox-overlay";
  overlay.innerHTML = `
    <div class="lightbox-dialog" role="dialog" aria-modal="true" aria-label="Image gallery">
      <button class="lightbox-close" type="button" aria-label="Close image viewer">&times;</button>
      <button class="lightbox-prev" type="button" aria-label="Previous image">&#8249;</button>
      <img class="lightbox-image" src="" alt="" />
      <p class="lightbox-caption"></p>
      <button class="lightbox-next" type="button" aria-label="Next image">&#8250;</button>
    </div>
  `;

  document.body.appendChild(overlay);

  const image = overlay.querySelector(".lightbox-image");
  const caption = overlay.querySelector(".lightbox-caption");
  const closeButton = overlay.querySelector(".lightbox-close");
  const prevButton = overlay.querySelector(".lightbox-prev");
  const nextButton = overlay.querySelector(".lightbox-next");
  let currentIndex = 0;

  function renderImage(index) {
    const trigger = triggers[index];
    const preview = trigger.querySelector("img");

    image.src = trigger.getAttribute("href") || "";
    image.alt = preview?.getAttribute("alt") || "Gallery image";
    caption.textContent = trigger.getAttribute("data-title") || "";
    currentIndex = index;
  }

  function openLightbox(index) {
    renderImage(index);
    overlay.classList.add("is-open");
    document.body.classList.add("lightbox-open");
  }

  function closeLightbox() {
    overlay.classList.remove("is-open");
    document.body.classList.remove("lightbox-open");
  }

  function move(step) {
    const nextIndex = (currentIndex + step + triggers.length) % triggers.length;
    renderImage(nextIndex);
  }

  triggers.forEach((trigger, index) => {
    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      openLightbox(index);
    });
  });

  closeButton.addEventListener("click", closeLightbox);
  prevButton.addEventListener("click", () => move(-1));
  nextButton.addEventListener("click", () => move(1));

  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (!overlay.classList.contains("is-open")) {
      return;
    }

    if (event.key === "Escape") {
      closeLightbox();
    } else if (event.key === "ArrowLeft") {
      move(-1);
    } else if (event.key === "ArrowRight") {
      move(1);
    }
  });
});
