    // Scroll to top
    function scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Theme Toggle
    function toggleTheme() {
      document.body.classList.toggle("dark");
      localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
    }

    // Load saved theme
    (function() {
      if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
      }
    })();

    // Step highlight on scroll
    const steps = document.querySelectorAll(".step");
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          steps.forEach(s => s.classList.remove("active"));
          entry.target.classList.add("active");
        }
      });
    }, { threshold: 0.6 });

    steps.forEach(step => observer.observe(step));
