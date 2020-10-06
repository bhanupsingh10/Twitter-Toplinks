const btn = document.querySelector("#toggle_btn")
const text = document.querySelector("#text")
const wrapper = document.querySelector(".wrapper")

btn.addEventListener("click", toggle)

function toggle(){
  wrapper.classList.toggle("on")
  text.classList.toggle("on")
  btn.classList.toggle("on")
}

