function nik_validation(){
    let fill_nik = document.getElementById("nik").value.trim();
    let change_color = document.getElementById("change-nik");
    
    if(fill_nik === ""){
        nik.className = "form-control wrong";
        change_color.className = "fa-solid fa-id-card wrong";
        return false;
    }

    if(isNaN(fill_nik)){
        nik.className = "form-control wrong";
        change_color.className = "fa-solid fa-id-card wrong";
        return false;
    }

    if(fill_nik.length !== 16){
        nik.className = "form-control wrong";
        change_color.className = "fa-solid fa-id-card wrong";
        return false;
    }

    nik.className = "form-control";
    change_color.className = "fa-solid fa-id-card";
    return true;
}

function job_validation(){
    let fill_job = document.getElementById("job").value.trim();
    let change_color = document.getElementById("change-job");

    if(fill_job === ""){
        job.className = "form-control wrong";
        change_color.className = "fa-solid fa-user-doctor wrong";
        return false;
    }

    job.className = "form-control";
    change_color.className = "fa-solid fa-user-doctor";
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

    if(!nik_validation()) nik_validation();
    if(!job_validation()) job_validation();

    // let value_nik = document.getElementById("nik").value;
    // let value_job = document.getElementById("job").value;

    // sessionStorage.setItem("doc_nik", value_nik);
    // sessionStorage.setItem("doc_job", value_job);

    if(nik_validation() && job_validation()){
        window.location = "./signUpDoctor4.html";
    } else{
        pesan.style.visibility = "visible";
        setTimeout("pesan.style.visibility = 'hidden'", 3000);
    }
}

function back_validation(){
    window.location = "./signUpDoctor2.html";
}