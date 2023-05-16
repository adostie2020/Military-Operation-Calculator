import React from 'react';
import AircraftTable from '../home/AircraftTable-Page';
import Swal from 'sweetalert2';
import axios from 'axios'
import './aircrafttable.css'

class TheAircraftTable extends React.Component {
    constructor(props) {
        super(props);
    }

    async swalfirestuff() {
        Swal.fire({
            title: 'New Aircraft Info',
            html:
                '<input id="input1" class="swal2-input" placeholder="Enter Aircraft name">' +
                '<input id="input2" class="swal2-input swal2-number-input" type="number" placeholder="Aircraft Amount">' +
                '<input id="input3" class="swal2-input swal2-number-input" type="number" placeholder="Personnel Number">',
            focusConfirm: false,
            preConfirm: () => {
                const newName = document.getElementById('input1').value;
                const newAmount = document.getElementById('input2').value;
                const newPersonnel = document.getElementById('input3').value;
                console.log('Input 1:', newName);
                console.log('Input 2:', newAmount);
                console.log('Input 3:', newPersonnel);

                axios
                    .post('https://hackathon-pacaf.thecosmoking.repl.co/api/add_aircraft', {
                        type: newName,
                        number: parseInt(newAmount),
                        personnel: parseInt(newPersonnel)
                    })
                    .then((response) => {
                        // Handle the response
                        console.log('Post request successful:', response.data);
                    })
                    .catch((error) => {
                        // Handle the error
                        console.error('Error making post request:', error);
                    });


            },
            didOpen: () => {
                const numberInputs = document.querySelectorAll('.swal2-number-input');
                numberInputs.forEach((input) => {
                    input.classList.add('swal2-input');
                });
            }
        });
    }

    render() {
        return (
            <div>
                <button onClick={() => this.swalfirestuff()}>Add New Aircraft</button>
            </div>
        );
    }
}

export default TheAircraftTable;