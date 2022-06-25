// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});


let alertWrapper = document.querySelector('.alert')
let alertCLose = document.querySelector('.alert__close')

if (alertWrapper) {
  alertCLose.addEventListener('click', () =>
      alertWrapper.style.display = 'none'
  )
}