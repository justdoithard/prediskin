// function email_validation(){
//     let fill_email = document.getElementById("email").value.trim();
//     let change_color = document.getElementById("change-email");
    
//     if(fill_email === ""){
//         email.className = "form-control wrong";
//         change_color.className = "fa-solid fa-envelope wrong";
//         return false;
//     }

//     if(fill_email.search("@") < 0){
//         email.className = "form-control wrong";
//         change_color.className = "fa-solid fa-envelope wrong";
//         return false;
//     }

//     email.className = "form-control";
//     change_color.className = "fa-solid fa-envelope";
//     return true;
// }

// function show_password(){
//     let pass = document.getElementById("password");
//     let icon = document.getElementById("change-password");

//     if(sessionStorage.getItem('status') === 'true'){
//         if(pass.type === "password"){
//             pass.type = "text";
//             icon.className = "fa-solid fa-unlock wrong";
//         } else{
//             pass.type = "password";
//             icon.className = "fa-solid fa-lock wrong";
//         }
//     } else{
//         if(pass.type === "password"){
//             pass.type = "text";
//             icon.className = "fa-solid fa-unlock";
//         } else{
//             pass.type = "password";
//             icon.className = "fa-solid fa-lock";
//         }
//     }
// }

// function password_validation(){
//     let fill_password = document.getElementById("password").value.trim();
//     let change_color = document.getElementById("change-password");
    
//     if(fill_password === ""){
//         password.className = "form-control wrong";
//         change_color.className = "fa-solid fa-lock wrong";
//         sessionStorage.setItem('status', 'true');
//         return false;
//     }

//     password.className = "form-control";
//     change_color.className = "fa-solid fa-lock";
//     sessionStorage.setItem('status', 'false');
//     return true;
// }

// function submit_validation(){
//     let pesan = document.getElementById("pesan");

//     if(!email_validation()) email_validation();
//     if(!password_validation()) password_validation();

//     if(email_validation() && password_validation()){
//         window.location = "./home.html";
//     } else{
//         pesan.style.visibility = "visible";
//         setTimeout("pesan.style.visibility = 'hidden'", 3000);
//     }
// }

var gantiKolom = document.getElementById("ganti-kolom");

window.addEventListener('resize', () => {
    if(window.matchMedia("screen and (max-width: 992px)").matches){
        gantiKolom.classList = "row rounded-5 w-100 h-80 d-flex flex-column-reverse justify-content-center";
    } else{
        gantiKolom.classList = "row rounded-5 w-100";
    }
})