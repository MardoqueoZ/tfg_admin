const container = document.getElementById('container');
const registerBtn = document.getElementById('reg');
const loginBtn = document.getElementById('log');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});