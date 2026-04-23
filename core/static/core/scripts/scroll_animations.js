document.addEventListener("DOMContentLoaded", () => {

  const reveals = document.querySelectorAll(
    ".reveal, .reveal-left, .reveal-right"
  );

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {

        // Delay slightly so browser paints initial state first
        setTimeout(() => {
          entry.target.classList.add("active");
        }, 50);

        observer.unobserve(entry.target); // optional: animate once
      }
    });
  }, {
    threshold: 0.15
  });

  reveals.forEach(el => observer.observe(el));

});
