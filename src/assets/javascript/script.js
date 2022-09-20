const zip_codes_re = new RegExp("6423[0-9]")

zipCodeList = [
    "64230",
    "64231",
    "64232",
    "64233",
    "64234",
    "64235",
    "64236",
    "64237",
    "64239"
]

document.addEventListener("DOMContentLoaded", (event) => 
{
    let htmlIframeString = `<iframe id="MapInteractive" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2051.9318612247876!2d16.592368716487428!3d59.04985334044074!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x465ec4abc74e82c5%3A0x4642c0225f90c202!2sKungsv%C3%A4gen%202%2C%20642%2034%20Flen!5e0!3m2!1ssv!2sse!4v1663054178090!5m2!1ssv!2sse" style="border: 0; width: 100%; height: 300px;" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe>`
    document.querySelector("#mapadress").innerHTML += htmlIframeString

    let htmlZipcodeCheck = '<p>Skriv ditt postnummer för att se om vi kör ut till dig!</p><form action=""><input type="number" id="number" placeholder="64230"><input id="submit" type="submit" value="Submit"></form><p id="output"></p>'
    document.querySelector("#jsCheck").innerHTML = htmlZipcodeCheck

    document.querySelector("#postnummerCheck form").addEventListener("submit", (event) => {
        event.preventDefault()

        // event.submitter.parentNode.querySelector("#number").value
        // is what is written in the input 

        // 
        if (event.submitter.parentNode.querySelector("#number").value.length != 5)
        {
            document.querySelector("#output").innerHTML = "Inte ett postnummer."
        }
        else if(zipCodeList.includes(event.submitter.parentNode.querySelector("#number").value)){
            document.querySelector("#output").innerHTML = "Vi kör ut, ring telefonnummret ovan!"
        }
        else{
            document.querySelector("#output").innerHTML = "Vi kör tyvärr inte ut till dig."
        }
    })
})