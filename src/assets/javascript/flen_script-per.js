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
    0: [12, 20, "Söndag"], //Starts on sunday
    1: [10, 22, "Måndag"],
    2: [10, 22, "Tisdag"],
    3: [10, 22, "Onsdag"],
    4: [10, 22, "Torsdag"],
    5: [10, 23, "Fredag"],
    6: [12, 23, "Lördag"]
}

let d = new Date();
let month = d.getMonth() + 1;
let date = d.getDate();
let day = d.getDay();
let time = d.getHours();
let OpenSign = null;


document.addEventListener("DOMContentLoaded", (event) => 
{
    let htmlIframeString = `<iframe id="MapInteractive" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2051.9318612247876!2d16.592368716487428!3d59.04985334044074!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x465ec4abc74e82c5%3A0x4642c0225f90c202!2sKungsv%C3%A4gen%202%2C%20642%2034%20Flen!5e0!3m2!1ssv!2sse!4v1663054178090!5m2!1ssv!2sse" style="border: 0; width: 100%; height: 300px;" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe>`
    document.querySelector("#mapadress").innerHTML += htmlIframeString

    let htmlZipcodeCheck = '<p>کد پستی خود را وارد کنید تا ببینید آیا ما به شما تحویل می دهیم یا خیر!</p><form action=""><input type="text" inputmode="numeric" id="number" placeholder="642 30"><input class="checkNumber" id="submit" type="submit" value="بررسی"></form><p id="output"></p>'
    document.querySelector("#jsCheck").innerHTML = htmlZipcodeCheck

    if (month === 1 && date === 6 || month === 5 && date === 1 || month === 12 && date === 24 || month === 12 && date === 25 || month === 12 && date === 26) {
        OpenSign = '<p><span style="color: red; font-weight: bold;">امروز بسته است</span></p>'
        document.querySelector("#OpenSign").innerHTML = OpenSign
    }
    else if (openHours[day][0] <= time && time < openHours[day][1]){
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

//Sorts the dates accordeing to today

const closed_days = [
    { title: '۱۳ روز کریسمس', month_worded: "ژانویه", month: 1, day: 6 },
    { title: 'اولین مه', month_worded: "مه", month: 5, day: 1  },
    { title: 'کریسمس', month_worded: "دسامبر", month: 12, day: 24 },
    { title: 'روز کریسمس', month_worded: "دسامبر", month: 12, day: 25 },
    { title: 'روز باکس کریسمس', month_worded: "دسامبر", month: 12, day: 26 },
];

/* Sort closing days */
let closed_days_element = document.querySelector('.holidays');
closed_days_element.innerHTML = ''; // Clear inner table

let currentMonth = parseInt(d.getMonth() + 1); //get month returns a value between 0 and 11. setting +1 gets the real month number.
let currentDay = parseInt(d.getDate());

let dateArr = [];

let pastDates = [];
let futureDates = [];

for(let i = 0; i < closed_days.length; i++)
{
        if(closed_days[i].month <= currentMonth)
        {
            if(closed_days[i].day >= currentDay && closed_days[i].month == currentMonth)
            {
                dateArr.push(closed_days[i])
            }
            else 
            {
                pastDates.push(closed_days[i]);
            }
        }
        else 
        {
        dateArr.push(closed_days[i]);
        
        }
}
dateArr = dateArr.concat(pastDates);

for(let i = 0; i < dateArr.length; i++){
    closed_days_element.innerHTML += `
        <tr>
            <th>${dateArr[i].day} ${dateArr[i].month_worded}</th>
            <td class="RightAlign">${dateArr[i].title}</td>
        </tr>
    `
}

