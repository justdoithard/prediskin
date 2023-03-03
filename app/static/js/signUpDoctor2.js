function email_validation(){
    let fill_email = document.getElementById("email").value.trim();
    let change_color = document.getElementById("change-email");
    
    if(fill_email === ""){
        email.className = "form-control wrong";
        change_color.className = "fa-solid fa-envelope wrong";
        return false;
    }

    if(fill_email.search("@") < 0){
        email.className = "form-control wrong";
        change_color.className = "fa-solid fa-envelope wrong";
        return false;
    }

    email.className = "form-control";
    change_color.className = "fa-solid fa-envelope";
    return true;
}

function phone_validation(){
    let fill_phone = document.getElementById("phone").value.trim();
    let change_color = document.getElementById("change-phone");

    if(fill_phone === ""){
        phone.className = "form-control wrong";
        change_color.className = "fa-solid fa-phone wrong";
        return false;
    }

    if(isNaN(fill_phone)){
        phone.className = "form-control wrong";
        change_color.className = "fa-solid fa-phone wrong";
        return false;
    }

    if(fill_phone.length < 11){
        phone.className = "form-control wrong";
        change_color.className = "fa-solid fa-phone wrong";
        return false;
    }

    phone.className = "form-control";
    change_color.className = "fa-solid fa-phone";
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

    if(!email_validation()) email_validation();
    if(!phone_validation()) phone_validation();

    // let value_email = document.getElementById("email").value;
    // let value_phone = document.getElementById("phone").value;

    // sessionStorage.setItem("doc_email", value_email);
    // sessionStorage.setItem("doc_phone", value_phone);

    if(email_validation() && phone_validation()){
        window.location = "./signUpDoctor3.html";
    } else{
        pesan.style.visibility = "visible";
        setTimeout("pesan.style.visibility = 'hidden'", 3000);
    }
}

function back_validation(){
    window.location = "./signUpDoctor1.html";
}