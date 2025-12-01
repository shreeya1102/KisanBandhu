// Typewriter Effect
const text = "Kisan Bandhu";
const container = document.getElementById("typewriter");
let index = 0;

function typeLetter() {
  if (index <= text.length) {
    container.textContent = text.slice(0, index);
    index++;
    setTimeout(typeLetter, 150);
  } else {
    container.style.borderRight = "none";
  }
}
typeLetter();

// Dropdown Navigation
const englishBtn = Array.from(document.getElementsByClassName("lang-option"))
  .find(btn => btn.textContent.trim() === "English");

if (englishBtn) {
  englishBtn.type = "button";
  englishBtn.addEventListener("click", function() {
    alert("Redirecting..."); // For debug
    window.location.href = "english.html";
  });
} else {
  console.warn("English button not found!");
}
