const zip_codes_re = new RegExp("9619[0, 1, 3, 4]")

zipCodeList = [
    "96190",,
    "96191",
    "96193",
    "96194"
]

var openHours = {
    0: [12, 23, "Söndag"], //Starts on sunday
    1: [10, 22, "Måndag"],
    2: [10, 22, "Tisdag"],
    3: [10, 24, "Onsdag"],
    4: [10, 22, "Torsdag"],
    5: [10, 03, "Fredag"],
    6: [12, 04, "Lördag"]
}

let d = new Date();
let day = d.getDay();
let time = d.getHours();
let OpenSign = null;


document.addEventListener("DOMContentLoaded", (event) => 
{
    let htmlIframeString = `<iframe id="MapInteractive" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1643.0857221286803!2d21.84887801662537!3d65.68080409348582!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x467f677c34b6b1af%3A0x493f441e2dee92f!2sF%C3%A4rjledsv%C3%A4gen%2038%2C%20961%2093%20S%C3%B6dra%20Sunderbyn!5e0!3m2!1ssv!2sse!4v1664867957394!5m2!1ssv!2sse"  style="border: 0; width: 100%; height: 300px;" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe>`
    document.querySelector("#mapadress").innerHTML += htmlIframeString

    let htmlZipcodeCheck = '<p>کد پستی خود را وارد کنید تا ببینید آیا ما به شما تحویل می دهیم یا خیر!</p><form action=""><input type="text" inputmode="numeric" id="number" placeholder="961 90"><input class="checkNumber" id="submit" type="submit" value="بررسی"></form><p id="output"></p>'
    document.querySelector("#jsCheck").innerHTML = htmlZipcodeCheck
   
    if (openHours[day][0] <= time && time < openHours[day][1]){
        OpenSign = '<p>ما اکنون باز هستیم!</p>'
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }
    else if(day + 1 === 7 && time >= openHours[day][1]){ //Handles saturdays after close
        OpenSign = '<p><span style="color: red; font-weight: bold;">بسته!</span> باز میکنیم: ' + openHours[0][2] + " kl. " + openHours[0][0] + ":00" + '</p>'
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }
    else if(time >= openHours[day][1]){
        OpenSign = '<p><span style="color: red; font-weight: bold;">بسته!</span> باز میکنیم: ' + openHours[day + 1][2] + " kl. " + openHours[day + 1][0] + ":00" + '</p>'
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }
    else{
        OpenSign = '<p><span style="color: red; font-weight: bold;">بسته!</span> ما امروز در ساعت باز می کنیم' + openHours[day][0] + ":00" + '</p>'
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }

    document.querySelector("#postnummerCheck form").addEventListener("submit", (event) => {
        event.preventDefault()

        // event.submitter.parentNode.querySelector("#number").value
        // is what is written in the input 
        let zipInput = event.submitter.parentNode.querySelector("#number").value
        zipInput = zipInput.split(" ").join("") //removes spaces from string

        if (zipInput.match(/\D/) != null) {
            document.querySelector("#output").innerHTML = "کد پستی نیست"
        }
        else if (zipInput.length != 5) {
            document.querySelector("#output").innerHTML = "کد پستی نیست"
        }
        else if(zipCodeList.includes(zipInput)) {
            document.querySelector("#output").innerHTML = "ما به سمت شما رانندگی می کنیم، با شماره تلفن بالا تماس بگیرید"
        }
        else {
            document.querySelector("#output").innerHTML = "متأسفانه ما به شما رانندگی نمی کنیم."
        }
    })
})

