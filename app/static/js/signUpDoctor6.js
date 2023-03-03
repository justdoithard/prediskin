function agreement(){
    let check_agree = document.getElementById("agree");
    let change_color = document.getElementById("text-agree");

    if(!check_agree.checked){
        check_agree.className = "form-check-input wrong";
        change_color.className = "form-check-label wrong";
        return false;
    }

    check_agree.className = "form-check-input";
    change_color.className = "form-check-label";
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
    
    if(!agreement()) agreement();

    if(agreement()){
        window.location = "./home.html";
    } else{
        pesan.style.visibility = "visible";
        setTimeout("pesan.style.visibility = 'hidden'", 3000);
    }

    // sessionStorage.removeItem("doc_name");
    // sessionStorage.removeItem("doc_gender");
    // sessionStorage.removeItem("doc_dob");
    // sessionStorage.removeItem("doc_email");
    // sessionStorage.removeItem("doc_phone");
    // sessionStorage.removeItem("doc_nik");
    // sessionStorage.removeItem("doc_job");
    // sessionStorage.removeItem("doc_hostName");
    // sessionStorage.removeItem("doc_hostAdd");
    // sessionStorage.removeItem("doc_password");
}

function back_validation(){
    window.location = "./signUpDoctor5.html";
}