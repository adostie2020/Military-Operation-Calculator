import jsPDF from "jspdf";

async function PDFGenerator(data){
    const doc = new jsPDF();
    console.log(data);

    doc.text(data.inputs.exerciseName, 5, 10);
    doc.text("$" + data.totalSum, 5, 15);

    const fromTo = data.inputs.departureCity + " -> " + data.inputs.arrivalCity;
    const startFinish = data.inputs.departureDate + " : " + data.inputs.arrivalDate;
    doc.text(fromTo, 75, 10);
    doc.text(startFinish, 145, 10);

    doc.text("aircrafts:", 5, 25);
    let i = 0;
    data.aircrafts.map((aircraft) => {
        const name = aircraft.type;
        if (data.inputs[name] === true){
            const amountName = name + 'Amount';
            const numberSupporters = data.inputs[amountName];
            const yLoc = 35 + (i * 5);
            const supportersForAircraft = aircraft.personnel[numberSupporters - 1];
            const totalAmountForAircraft = ((supportersForAircraft * data.flightCost) +
                (supportersForAircraft * data.dataMeals));

            doc.text(name + ":", 5, yLoc);
            doc.text(supportersForAircraft.toString(), 25, yLoc);
            doc.text("$"+totalAmountForAircraft.toString(), 45, yLoc);
            i++;
        }
    });

    doc.text("total supporters: " + data.totalAmountSupports, 75, 25);
    doc.text("personnel in commercial air: " + data.peopleCommercialAir, 75, 30);
    doc.text("personnel in commercial lodging: " + data.peopleCommercialLodging, 75, 35);
    doc.text("personnel in military air: " + data.peopleMilitaryAir, 75, 40);
    doc.text("personnel in military lodging: " + data.peopleGovernmentLodging, 75, 45);
    doc.text("personnel in field conditions: " + data.peopleWoodsLodging, 75, 50);
    doc.text("personnel with per diem meals: " + data.peoplePerDiemFood, 75, 55);

    doc.save("form.pdf");
    doc.close();
}

export default PDFGenerator;