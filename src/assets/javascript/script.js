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

var openHours = {
    0: [12, 20, "Söndag"], //börjar på söndag
    1: [10, 22, "Måndag"],
    2: [10, 22, "Tisdag"],
    3: [10, 22, "Onsdag"],
    4: [10, 22, "Torsdag"],
    5: [10, 23, "Fredag"],
    6: [12, 23, "Lördag"]
}

let d = new Date();
let day = d.getDay();
let time = d.getHours();
let OpenSign = null;

document.addEventListener("DOMContentLoaded", (event) => 
{
    let htmlIframeString = `<iframe id="MapInteractive" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2051.9318612247876!2d16.592368716487428!3d59.04985334044074!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x465ec4abc74e82c5%3A0x4642c0225f90c202!2sKungsv%C3%A4gen%202%2C%20642%2034%20Flen!5e0!3m2!1ssv!2sse!4v1663054178090!5m2!1ssv!2sse" style="border: 0; width: 100%; height: 300px;" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe>`
    document.querySelector("#mapadress").innerHTML += htmlIframeString

    let htmlZipcodeCheck = '<p>Skriv ditt postnummer för att se om vi kör ut till dig!</p><form action=""><input type="text" inputmode="numeric" id="number" placeholder="64230"><input id="submit" type="submit" value="Kolla"></form><p id="output"></p>'
    document.querySelector("#jsCheck").innerHTML = htmlZipcodeCheck

    // console.log(d, day, time, openHours[day][0]);
   
    if (openHours[day][0] <= time && time < openHours[day][1]){
        OpenSign = '<p>Vi har öppet just nu!</p>'
        console.log(OpenSign)
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }
    else if(day + 1 === 7 && time >= openHours[day][1]){ //Hanterar lördagar efter stänging
        OpenSign = '<p>Vi öppnar: ' + openHours[0][2] + " kl. " + openHours[0][0] + ":00" + '</p>'
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }
    else if(time >= openHours[day][1]){
        OpenSign = '<p>Vi öppnar: ' + openHours[day + 1][2] + " kl. " + openHours[day + 1][0] + ":00" + '</p>'
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }
    else{
        OpenSign = '<p>Vi öppnar: idag kl.' + openHours[day][0] + ":00" + '</p>'
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }

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
            document.querySelector("#output").innerHTML = "Vi kör ut, ring telefonnumret ovan!"
        }
        else{
            document.querySelector("#output").innerHTML = "Vi kör tyvärr inte ut till dig."
        }
    })
})