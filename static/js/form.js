
let pass;
let secpass;

document.querySelector("#confirmPassword").addEventListener("input", (event) => {
    pass = event.target.value
    checkMatch()
})

document.querySelector("#password").addEventListener("input", (event) => {
    secpass = event.target.value
    checklength()
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
