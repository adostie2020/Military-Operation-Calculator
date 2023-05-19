import jsPDF from "jspdf";

async function PDFGenerator2(data){
    const doc = new jsPDF();
    console.log(data);

    doc.text(data.exerciseName, 5, 10);
    doc.text("$" + data.total.toFixed(2), 5, 15);

    const fromTo = data.fromLocation + " -> " + data.toLocation;
    const startFinish = data.startDate + " : " + data.endDate;
    doc.text(fromTo, 75, 10);
    doc.text(startFinish, 145, 10);

    // doc.text("aircrafts:", 5, 25);
    // let i = 0;
    // data.aircrafts.map((aircraft) => {
    //     const name = aircraft.type;
    //     if (data.inputs[name] === true){
    //         const amountName = name + 'Amount';
    //         const numberSupporters = data.inputs[amountName];
    //         const yLoc = 35 + (i * 5);
    //         const supportersForAircraft = aircraft.personnel[numberSupporters - 1];
    //         const totalAmountForAircraft = ((supportersForAircraft * data.flightCost) +
    //             (supportersForAircraft * data.dataMeals));

    //         doc.text(name + ":", 5, yLoc);
    //         doc.text(supportersForAircraft.toString(), 25, yLoc);
    //         doc.text("$"+totalAmountForAircraft.toString(), 45, yLoc);
    //         i++;
    //     }
    // });

    doc.text("total supporters: " + data.supporters, 75, 25);
    doc.text("personnel in commercial air: " + data.peopleCommercialAir, 75, 30);
    doc.text("personnel in commercial lodging: " + data.commercialLodging, 75, 35);
    doc.text("personnel in military air: " + data.peopleCommercialMilitary, 75, 40);
    doc.text("personnel in military lodging: " + data.governmentLodging, 75, 45);
    doc.text("personnel in field conditions: " + data.woodsLodging, 75, 50);
    doc.text("personnel with per diem meals: " + data.peopleperdiemFood, 75, 55);

    doc.save("form.pdf");
    doc.close();
}

export default PDFGenerator2;