import React from 'react';
import AircraftTable from '../home/AircraftTable-Page';
import Swal from 'sweetalert2';
import axios from 'axios'
import './aircrafttable.css'

class TheAircraftTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {aircrafts: []};
    }

    async componentDidMount() {
        await axios.get('https://hackathon-pacaf--thecosmoking.repl.co/api/get_aircraft')
          .then(response => {
            this.setState({aircrafts: response.data.aircrafts});
          })
          .catch(error => {
            console.error(error);
          });
    }

    async swalfirestuff() {
        Swal.fire({
            title: 'New Aircraft Info',
            html:
                '<input id="input1" class="swal2-input" placeholder="Enter Aircraft name">' +
                '<input id="input2" class="swal2-input swal2-number-input" type="number" placeholder="Aircraft Amount">' +
                '<input id="input3" class="swal2-input swal2-number-input" type="number" placeholder="Personnel Number">',
            focusConfirm: false,
            showCancelButton: true,
            cancelButtonText: 'Cancel',
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
                        window.location.reload();
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
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Number</th>
                                <th>Personnel</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.aircrafts.map((aircraft) => (
                                <tr key={aircraft.id}>
                                    <td>{aircraft.type}</td>
                                    <td>{aircraft.number}</td>
                                    <td>{aircraft.personnel}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <button onClick={() => this.swalfirestuff()}> enter new aircraft</button>
            </div>
        );
    }
}

export default TheAircraftTable;