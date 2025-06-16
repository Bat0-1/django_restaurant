document.addEventListener('DOMContentLoaded', function () {
  const nav = document.getElementById('topNav');
  const slider = document.getElementById('spiceRange');
  const output = document.getElementById('spiceLevel');

  // Navbar scroll effect
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 30);
  });

  // Spiciness slider label logic
  if (slider && output) {
    const updateLabel = () => {
      output.textContent = slider.value === "-1" ? "Not Set" : slider.value;
    };

    updateLabel(); // Run on load
    slider.addEventListener('input', updateLabel);
  }
});

// Save scroll position
window.addEventListener('beforeunload', function () {
  sessionStorage.setItem('scrollPos', window.scrollY);
});

// Restore scroll position
window.addEventListener('load', function () {
  const scrollPos = sessionStorage.getItem('scrollPos');
  if (scrollPos) {
    window.scrollTo(0, parseInt(scrollPos));
    sessionStorage.removeItem('scrollPos');
  }
});
