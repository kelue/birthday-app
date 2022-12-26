
let pass;
let secpass;
let email;

document.querySelector("#confirmPassword").addEventListener("input", (event) => {
    pass = event.target.value
    checkMatch()
})

document.querySelector("#password").addEventListener("input", (event) => {
    secpass = event.target.value
    checklength()
})

document.querySelector("#email").addEventListener("input", (event) => {
    email = event.target.value
    checkEmail(email)
})

const checkMatch = () => {
    if (pass !== secpass) {
        document.querySelector("#nomatch").innerHTML = "Passwords do not match!!!!"
    }else{
        document.querySelector("#nomatch").innerHTML = ""
    }
}

const checklength = () => {
    if (secpass.length < 8){
        document.querySelector("#passlength").innerHTML = "Password length should be more than 8 characters"
    }else{
        document.querySelector("#passlength").innerHTML = ""
    }
}

const checkEmail = (email) => {
    // Use a regex to check if the email is in a valid format
    const regex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    if( !regex.test(email) ){
        document.querySelector("#validemail").innerHTML = "Email is not valid"
    }else{
        document.querySelector("#validemail").innerHTML = ""
    }
}
