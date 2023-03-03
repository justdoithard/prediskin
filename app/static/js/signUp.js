function user_validation(){
    let fill_user = document.getElementsByName("user");
    let change_border_1 = document.getElementById("change-border-1");
    let change_border_2 = document.getElementById("change-border-2");

    if(!fill_user[0].checked && !fill_user[1].checked){
        change_border_1.className = "form-check rounded-3 w-100 d-flex align-items-center gap-2 wrong";
        change_border_2.className = "form-check rounded-3 w-100 d-flex align-items-center gap-2 wrong";
        return false;
    } else{
        change_border_1.className = "form-check rounded-3 w-100 d-flex align-items-center gap-2";
        change_border_2.className = "form-check rounded-3 w-100 d-flex align-items-center gap-2";
        return true;
    }
}

function submit_validation(event){
    event.preventDefault();
    let fill_user = document.getElementsByName("user");
    let pesan = document.getElementById("pesan");

    if(!user_validation()) user_validation();

    if(fill_user[0].checked){
        // window.location = "./signUpDoctor1.html";
    } else if(fill_user[1].checked){
        // window.location = "./signUpPublic1.html";
    } else{
        pesan.style.visibility = "visible";
        setTimeout("pesan.style.visibility = 'hidden'", 3000);
    }
    
    
}