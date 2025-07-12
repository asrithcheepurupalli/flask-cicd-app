document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("toggle-dark");
  const html = document.documentElement;

  // Load saved mode
  if (localStorage.getItem("dark-mode") === "true") {
    html.classList.add("dark");
  }

  button.addEventListener("click", () => {
    html.classList.toggle("dark");
    const isDark = html.classList.contains("dark");
    localStorage.setItem("dark-mode", isDark);
  });
});