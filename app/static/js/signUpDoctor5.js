function show_password(){
    let pass = document.getElementById("password");
    let icon = document.getElementById("change-password");

    if(sessionStorage.getItem('status_pass') === 'true'){
        if(pass.type === "password"){
            pass.type = "text";
            icon.className = "fa-solid fa-unlock wrong";
        } else{
            pass.type = "password";
            icon.className = "fa-solid fa-lock wrong";
        }
    } else{
        if(pass.type === "password"){
            pass.type = "text";
            icon.className = "fa-solid fa-unlock";
        } else{
            pass.type = "password";
            icon.className = "fa-solid fa-lock";
        }
    }
}

function password_validation(){
    let fill_password = document.getElementById("password").value.trim();
    let change_color = document.getElementById("change-password");
    let regexUpper = /[A-Z]/;
    let regexNum = /[0-9]/;
    
    if(fill_password === ""){
        password.className = "form-control wrong";
        change_color.className = "fa-solid fa-lock wrong";
        sessionStorage.setItem('status_pass', 'true');
        return false;
    }

    if(fill_password.length < 8){
        password.className = "form-control wrong";
        change_color.className = "fa-solid fa-lock wrong";
        sessionStorage.setItem('status_pass', 'true');
        return false;
    }

    if(!regexUpper.test(fill_password) || !regexNum.test(fill_password)){
        password.className = "form-control wrong";
        change_color.className = "fa-solid fa-lock wrong";
        sessionStorage.setItem('status_pass', 'true');
        return false;
    }

    password.className = "form-control";
    change_color.className = "fa-solid fa-lock";
    sessionStorage.setItem('status_pass', 'false');
    return true;
}

function show_valPass(){
    let pass = document.getElementById("valPass");
    let icon = document.getElementById("change-valPass");

    if(sessionStorage.getItem('status_valPass') === 'true'){
        if(pass.type === "password"){
            pass.type = "text";
            icon.className = "fa-solid fa-eye wrong";
        } else{
            pass.type = "password";
            icon.className = "fa-solid fa-eye-slash wrong";
        }
    } else{
        if(pass.type === "password"){
            pass.type = "text";
            icon.className = "fa-solid fa-eye";
        } else{
            pass.type = "password";
            icon.className = "fa-solid fa-eye-slash";
        }
    }
}

function valPass_validation(){
    let fill_valPass = document.getElementById("valPass").value.trim();
    let change_color = document.getElementById("change-valPass");
    let fill_password = document.getElementById("password").value.trim();

    if(fill_valPass === ""){
        valPass.className = "form-control wrong";
        change_color.className = "fa-solid fa-eye-slash wrong";
        sessionStorage.setItem('status_valPass', 'true');
        return false;
    }

    if(fill_valPass !== fill_password){
        valPass.className = "form-control wrong";
        change_color.className = "fa-solid fa-eye-slash wrong";
        sessionStorage.setItem('status_valPass', 'true');
        return false;
    }

    valPass.className = "form-control";
    change_color.className = "fa-solid fa-eye-slash";
    sessionStorage.setItem('status_valPass', 'false');
    return true;
}

// document.getElementById("sub-btn1").addEventListener("click", function(event){
//     event.preventDefault()
// });

// document.getElementById("sub-btn2").addEventListener("click", function(event){
//     event.preventDefault()
// });

function submit_validation(){
    let pesan = document.getElementById("pesan");

    if(!password_validation()) password_validation();
    if(!valPass_validation()) valPass_validation();

    // let value_password = document.getElementById("password").value;
    // sessionStorage.setItem("doc_password", value_password);

    if(password_validation() && valPass_validation()){
        window.location = "./signUpDoctor6.html";
    } else{
        pesan.style.visibility = "visible";
        setTimeout("pesan.style.visibility = 'hidden'", 3000);
    }
}

function back_validation(){
    window.location = "./signUpDoctor4.html";
}