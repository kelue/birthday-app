
let pass;
let secpass;

document.querySelector("#confirmPassword").addEventListener("input", (event) => {
    pass = event.target.value
    checkMatch()
})

document.querySelector("#password").addEventListener("input", (event) => {
    secpass = event.target.value
    checkMatch()
})

const checkMatch = () => {
    if (pass !== secpass) {
        document.querySelector("#nomatch").innerHTML = "Passwords do not match!!!!"
    }else{
        document.querySelector("#nomatch").innerHTML = ""
    }
}