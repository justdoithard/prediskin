function hostName_validation(){
    let fill_hostName = document.getElementById("hostName").value.trim();
    let change_color = document.getElementById("change-hostName");
    
    if(fill_hostName === ""){
        hostName.className = "form-control wrong";
        change_color.className = "fa-solid fa-hospital wrong";
        return false;
    }

    hostName.className = "form-control";
    change_color.className = "fa-solid fa-hospital";
    return true;
}

function hostAdd_validation(){
    let fill_hostAdd = document.getElementById("hostAdd").value.trim();
    let change_color = document.getElementById("change-hostAdd");

    if(fill_hostAdd === ""){
        hostAdd.className = "form-control wrong";
        change_color.className = "fa-solid fa-location-dot wrong";
        return false;
    }

    hostAdd.className = "form-control";
    change_color.className = "fa-solid fa-location-dot";
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

    if(!hostName_validation()) hostName_validation();
    if(!hostAdd_validation()) hostAdd_validation();

    // let value_hostName = document.getElementById("hostName").value;
    // let value_hostAdd = document.getElementById("hostAdd").value;

    // sessionStorage.setItem("doc_hostName", value_hostName);
    // sessionStorage.setItem("doc_hostAdd", value_hostAdd);

    if(hostName_validation() && hostAdd_validation()){
        window.location = "./signUpDoctor5.html";
    } else{
        pesan.style.visibility = "visible";
        setTimeout("pesan.style.visibility = 'hidden'", 3000);
    }
}

function back_validation(){
    window.location = "./signUpDoctor3.html";
}