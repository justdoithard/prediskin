function name_validation(){
    let fill_name = document.getElementById("fullname").value.trim();
    let change_color = document.getElementById("change-name");

    
    if(fill_name === ""){
        fullname.className = "form-control wrong";
        change_color.className = "fa-solid fa-pen wrong";
        return false;
    }

    fullname.className = "form-control";
    change_color.className = "fa-solid fa-pen";
    return true;
}

function gender_validation(){
    let fill_gender = document.getElementsByName("gender");
    let change_border_1 = document.getElementById("change-border-1");
    let change_border_2 = document.getElementById("change-border-2");

    if(!fill_gender[0].checked && !fill_gender[1].checked){
        change_border_1.className = "form-check rounded-3 w-100 d-flex align-items-center gap-2 wrong";
        change_border_2.className = "form-check rounded-3 w-100 d-flex align-items-center gap-2 wrong";
        return false;
    } else{
        change_border_1.className = "form-check rounded-3 w-100 d-flex align-items-center gap-2";
        change_border_2.className = "form-check rounded-3 w-100 d-flex align-items-center gap-2";        
        return true;
    }
}

function date_validation(){
    let fill_date = document.getElementById("date");
    let change_color = document.getElementById("change-date");
    
    if(fill_date.value === ""){
        date.className = "form-control wrong";
        change_color.className = "fa-solid fa-calendar wrong";
        return false;
    }

    date.className = "form-control";
    change_color.className = "fa-solid fa-calendar";
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

    if(!name_validation()) name_validation();
    if(!gender_validation()) gender_validation();
    if(!date_validation()) date_validation();

    // let value_nama = document.getElementById("fullname").value;
    // let value_gender = document.querySelector("#radio-btn:checked").value;
    // let value_date = document.getElementById("date").value;

    // sessionStorage.setItem("doc_name", value_nama);
    // sessionStorage.setItem("doc_gender", value_gender);
    // sessionStorage.setItem("doc_dob", value_date);

    if(name_validation() && gender_validation() && date_validation()){
        window.location = "./signUpDoctor2.html";
    } else{
        pesan.style.visibility = "visible";
        setTimeout("pesan.style.visibility = 'hidden'", 3000);
    }
}

function back_validation(){
    window.location = "./signUp.html";
}